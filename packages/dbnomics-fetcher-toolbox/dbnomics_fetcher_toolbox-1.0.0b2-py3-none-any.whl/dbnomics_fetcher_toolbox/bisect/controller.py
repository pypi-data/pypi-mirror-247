import collections
from abc import ABC, abstractmethod
from functools import reduce
from pathlib import Path
from typing import TYPE_CHECKING, Generic, TypeVar

import daiquiri
from contexttimer import Timer
from dbnomics_data_model.json_utils import load_json_file, parse_json_data_as, save_json_file
from humanfriendly.text import pluralize

from dbnomics_fetcher_toolbox._internal.file_utils import format_file_path_with_size
from dbnomics_fetcher_toolbox._internal.formatting_utils import format_timer
from dbnomics_fetcher_toolbox.bisect.partitions.protocol import BisectionPartition
from dbnomics_fetcher_toolbox.errors.downloader import ResourceLoadError
from dbnomics_fetcher_toolbox.resource import Resource
from dbnomics_fetcher_toolbox.sources.json.msgspec import MsgspecJsonSource
from dbnomics_fetcher_toolbox.types import ResourceFullId

if TYPE_CHECKING:
    from dbnomics_fetcher_toolbox.resource_group import ResourceGroup

__all__ = ["BisectionController"]


logger = daiquiri.getLogger(__name__)

T = TypeVar("T")
TBisectionPartition = TypeVar("TBisectionPartition", bound=BisectionPartition)


class BisectionController(ABC, Generic[T, TBisectionPartition]):
    def __init__(self, *, resource_group: "ResourceGroup", root_partition: TBisectionPartition) -> None:
        self._resource_group = resource_group

        self._deque: collections.deque[TBisectionPartition] = collections.deque([root_partition])
        self._failed_partition_ids = self._load_failed_partition_ids()
        self.loaded_values: list[T] = []

    def start(self) -> None:
        logger.debug("Starting bisection process...")

        with Timer() as timer:
            partition_position = 1
            while self._deque:
                partition = self._deque.popleft()
                if partition.should_bisect_before_process:
                    logger.debug(
                        "Bisecting partition #%d %r before processing it",
                        partition_position,
                        partition.id,
                        depth=partition.depth,
                    )
                    self._bisect(partition, position=partition_position)
                else:
                    self._process_partition(partition, position=partition_position)
                partition_position += 1

            resource = self._create_partition_resource(partition=None, position=partition_position)
            merged_values = reduce(self._merge_loaded_values, self.loaded_values)
            self._resource_group.process_resource(resource, source=MsgspecJsonSource(merged_values))

        logger.debug(
            "End of bisection process: %s were processed",
            pluralize(partition_position, "partition"),
            duration=format_timer(timer),
        )

    def _bisect(self, partition: TBisectionPartition, *, position: int) -> None:
        left_partition, right_partition = partition.bisect()
        logger.debug(
            "Partition #%d %r has been bisected in 2 sub-partitions: %r and %r",
            position,
            partition.id,
            left_partition.id,
            right_partition.id,
            depth=partition.depth,
        )
        self._deque.extendleft([right_partition, left_partition])

    @abstractmethod
    def _create_partition_resource(self, *, partition: TBisectionPartition | None, position: int) -> Resource[T]:
        ...

    @property
    def _failed_partitions_json_file(self) -> Path:
        cache_dir = self._resource_group._downloader._cache_dir  # noqa: SLF001
        group_dir = cache_dir / self._resource_group.id
        return group_dir / "failed_partitions.json"

    def _load_failed_partition_ids(self) -> set[ResourceFullId]:
        if not self._resource_group._downloader._resume_mode:  # noqa: SLF001
            return set()

        failed_partitions_json_file = self._failed_partitions_json_file
        if not failed_partitions_json_file.is_file():
            return set()

        failed_partitions_json_data = load_json_file(failed_partitions_json_file)
        failed_partitions_json = parse_json_data_as(failed_partitions_json_data, type=list[str])
        return {ResourceFullId.parse(value) for value in failed_partitions_json}

    def _load_resume_status(self, resource: Resource[T]) -> tuple[bool, T | None]:
        if not self._resource_group._downloader._resume_mode:  # noqa: SLF001
            return False, None

        partition_resource_full_id = ResourceFullId.from_group_and_resource(self._resource_group, resource)
        if partition_resource_full_id in self._failed_partition_ids:
            logger.debug("Resume mode: skipping previously failed partition")
            return True, None

        cache_dir = self._resource_group._downloader._cache_dir  # noqa: SLF001
        cache_file = cache_dir / resource.file
        if not cache_file.is_file():
            return False, None

        logger.debug("Resume mode: reloading partition data from cache file %s", format_file_path_with_size(cache_file))
        cached_value = resource.parser.parse_file(cache_file)
        return False, cached_value

    @abstractmethod
    def _merge_loaded_values(self, accumulator: T, value: T) -> T:
        ...

    def _process_partition(self, partition: TBisectionPartition, *, position: int) -> None:
        logger.debug("Starting to process partition #%d %r...", position, partition.id, depth=partition.depth)

        resource = self._create_partition_resource(partition=partition, position=position)

        failed, cached_value = self._load_resume_status(resource)
        if failed:
            self._bisect(partition, position=position)
            return
        if cached_value is not None:
            self.loaded_values.append(cached_value)
            return

        try:
            loaded_value = self._process_partition_resource(resource, partition=partition, position=position)
        except ResourceLoadError:
            self._register_partition_failure(resource)
            self._bisect(partition, position=position)
            return
        except Exception:
            logger.exception(
                "Error processing partition #%d %r, aborting bisection process",
                position,
                partition.id,
                depth=partition.depth,
            )
            raise

        self.loaded_values.append(loaded_value)

        logger.debug("Partition #%d %r has been processed successfully", position, partition.id, depth=partition.depth)

    @abstractmethod
    def _process_partition_resource(self, resource: Resource[T], *, partition: TBisectionPartition, position: int) -> T:
        ...

    def _register_partition_failure(self, partition_resource: Resource[T]) -> None:
        partition_resource_full_id = ResourceFullId.from_group_and_resource(self._resource_group, partition_resource)
        failed_partitions = self._failed_partition_ids
        failed_partitions.add(partition_resource_full_id)

        failed_partitions_json_file = self._failed_partitions_json_file
        failed_partitions_json_file.parent.mkdir(exist_ok=True)
        failed_partitions_json = sorted(map(str, failed_partitions))
        save_json_file(failed_partitions_json_file, failed_partitions_json)
