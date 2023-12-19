import logging
import random
import time
from enum import Enum
from typing import Any, Callable, Optional, Sequence, Tuple, Type, Union

logger = logging.getLogger(__name__)


MS_IN_SEC = 1000


class RetryStrategy(Enum):
    """retry mechanism"""

    CONSTANT = "CONSTANT"
    LINEAR = "LINEAR"
    EXPONENTIAL = "EXPONENTIAL"


DEFAULT_STRATEGY = RetryStrategy.CONSTANT


class Retry:
    """handling retry check and wait"""

    def __init__(
        self,
        count: int,
        base_ms: int,
        jitter_ms: int,
        strategy: Optional[RetryStrategy] = None,
    ):
        self._max = count
        self._base = base_ms
        self._jitter = jitter_ms
        self._strategy = strategy or DEFAULT_STRATEGY
        self.count = 0

    def jitter(self) -> int:
        """compute random jitter in ms"""
        min_ = self._jitter // 2
        max_ = int(self._jitter * 1.5)
        return random.randrange(min_, max_)

    def base(self) -> int:
        """compute base wait time in ms"""
        base = self._base
        if self._strategy == RetryStrategy.CONSTANT:
            return base
        if self._strategy == RetryStrategy.LINEAR:
            return base * self.count
        # exponential
        scaled = float(base) / MS_IN_SEC
        return int(scaled**self.count * MS_IN_SEC)

    def check(self, error: BaseException, log_exc_info: bool = False) -> bool:
        """
        Check whether retry should happen or not.
        If log_exc_info is True, it will add a more extensive log (most notably
        including the traceback).
        """
        if self.count >= self._max:
            return False

        exc_info = error if log_exc_info else None
        logger.warning("Caught a retryable exception", exc_info=exc_info)

        self.count += 1
        wait_ms = self.base() + self.jitter()
        wait_s = float(wait_ms) / MS_IN_SEC
        logger.warning(f"Attempting a new call in {wait_s} seconds")
        time.sleep(wait_s)
        return True


WrapperReturnType = Union[Tuple[BaseException, None], Tuple[None, Any]]


def retry(
    exceptions: Sequence[Type[BaseException]],
    count: int = 1,
    base_ms: int = 0,
    jitter_ms: int = 1,
    strategy: Optional[RetryStrategy] = None,
    log_exc_info: bool = False,
) -> Callable:
    """retry decorator"""

    exceptions_ = tuple(e for e in exceptions)

    def _wrapper(callable: Callable) -> Callable:
        def _try(*args, **kwargs) -> WrapperReturnType:
            try:
                return None, callable(*args, **kwargs)
            except exceptions_ as err:
                return err, None

        def _func(*args, **kwargs) -> Any:
            retry = Retry(count, base_ms, jitter_ms, strategy)
            while True:
                err, result = _try(*args, **kwargs)
                if err is None:
                    return result
                if retry.check(err, log_exc_info):
                    continue
                raise err

        return _func

    return _wrapper
