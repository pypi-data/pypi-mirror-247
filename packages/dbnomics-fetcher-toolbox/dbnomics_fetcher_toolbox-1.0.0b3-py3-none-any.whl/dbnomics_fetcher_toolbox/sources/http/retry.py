from datetime import timedelta
from typing import TYPE_CHECKING, Final

import daiquiri
import requests.exceptions
from humanfriendly import format_timespan
from tenacity import (
    Retrying,
    retry_if_exception,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential,
)

if TYPE_CHECKING:
    from tenacity import RetryCallState


__all__ = [
    "default_retrying_retry",
    "default_retrying_stop",
    "default_retrying_wait",
    "default_retrying",
    "retry_if_bad_http_status_code",
]


logger = daiquiri.getLogger(__name__)


def log_before_attempt(retry_state: "RetryCallState") -> None:
    logger.debug("Loading source, attempt %d", retry_state.attempt_number)


def log_before_sleep(retry_state: "RetryCallState") -> None:
    assert retry_state.next_action is not None
    sleep_duration = retry_state.next_action.sleep
    logger.debug("Sleeping %s", format_timespan(sleep_duration))


def log_failed_attempt(retry_state: "RetryCallState") -> None:
    outcome = retry_state.outcome
    assert outcome is not None

    msg = "Error loading source"

    duration = retry_state.seconds_since_start
    if duration is not None:
        msg += f" after {format_timespan(duration)}"

    msg += f", attempt {retry_state.attempt_number}"

    try:
        outcome.result()
    except Exception:
        logger.exception(msg)
    else:
        logger.error(msg)


def should_retry_http_status_code(exception: BaseException) -> bool:
    http_codes_to_retry = [408, 425, 429, 500, 502, 503, 504]

    if isinstance(exception, requests.exceptions.HTTPError):
        status_code = exception.response.status_code  # type: ignore[union-attr]
        return status_code in http_codes_to_retry

    return False


retry_if_bad_http_status_code = retry_if_exception(predicate=should_retry_http_status_code)


default_retrying_retry: Final = retry_if_bad_http_status_code | retry_if_exception_type(
    (requests.exceptions.ChunkedEncodingError, requests.exceptions.ConnectionError, requests.exceptions.Timeout)
)
default_retrying_stop: Final = stop_after_attempt(5)
default_retrying_wait: Final = wait_exponential(max=timedelta(minutes=5), multiplier=1.5)
default_retrying: Final = Retrying(
    after=log_failed_attempt,
    before=log_before_attempt,
    before_sleep=log_before_sleep,
    retry=default_retrying_retry,
    stop=default_retrying_stop,
    wait=default_retrying_wait,
)
