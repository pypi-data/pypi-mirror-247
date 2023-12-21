from dataclasses import dataclass, replace
from typing import Self

from dbnomics_fetcher_toolbox.bisect.errors import NoMoreBisectionError
from dbnomics_fetcher_toolbox.bisect.partitions.protocol import PartitionId

__all__ = ["IntRangeBisectionPartition"]


@dataclass(frozen=True, kw_only=True)
class IntRangeBisectionPartition:
    depth: int = 0
    max_range: int | None = None
    max_value: int
    min_value: int

    def bisect(self) -> tuple[Self, Self]:
        if self.max_value == self.min_value:
            raise NoMoreBisectionError(partition=self)

        delta = self.range // 2
        middle_value = self.min_value + delta
        new_depth = self.depth + 1
        left_partition = replace(self, depth=new_depth, max_value=middle_value)
        right_partition = replace(self, depth=new_depth, min_value=middle_value + 1)
        return left_partition, right_partition

    @property
    def id(self) -> PartitionId:
        return f"{self.min_value}-{self.max_value}"

    @property
    def range(self) -> int:  # noqa: A003
        return self.max_value - self.min_value

    @property
    def should_bisect_before_process(self) -> bool:
        return self.max_range is not None and self.range >= self.max_range
