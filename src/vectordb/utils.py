"""General utilities for entire project."""
import datetime
import time
from dataclasses import dataclass
from typing import Optional, Sequence

import pandas as pd

__all__: Sequence[str] = (
    "timer",
    "sep",
)


@dataclass(frozen=False)
class timer:
    """Provides nanosecond-level timing precision."""

    _start_ns: Optional[int] = None
    _end_ns: Optional[int] = None

    def __enter__(self) -> "timer":
        """Sets the start time.

        Raises ValueError if the timer has already been started.
        """
        if self._start_ns is not None:
            msg = "Cannot restart a timer!"
            raise ValueError(msg)
        self._start_ns = time.time_ns()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):  # type: ignore
        """Sets the end time.

        Raises ValueError if the timer has not been started or if it has already completed.
        """
        if self._start_ns is None:
            msg = "Must start a timer before ending it!"
            raise ValueError(msg)
        if self._end_ns is not None:
            msg = "Timer has already stopped!"
            raise ValueError(msg)
        self._end_ns = time.time_ns()

    @property
    def duration(self) -> datetime.timedelta:
        """The duration, converted from nanoseconds to a timedelta instance.

        Raises ValueError if the timer has not completed.
        """
        if self._start_ns is None or self._end_ns is None:
            msg = "Cannot calculate duration if timer has not run to completion!"
            raise ValueError(msg)
        start = pd.Timestamp(ts_input=self._start_ns, unit="ns")
        end = pd.Timestamp(ts_input=self._end_ns, unit="ns")
        return end - start  # type: ignore

    @property
    def nanoseconds(self) -> int:
        """The exact measured duration, in nanoseconds.

        Raises ValueError if the timer has not completed.
        """
        if self._start_ns is None or self._end_ns is None:
            msg = "Cannot calculate duration if timer has not run to completion!"
            raise ValueError(msg)
        return self._end_ns - self._start_ns

    @property
    def seconds(self) -> float:
        """The duration, in fractional seconds.

        Raises ValueError if the timer has not completed.
        """
        if self._start_ns is None or self._end_ns is None:
            msg = "Cannot calculate duration if timer has not run to completion!"
            raise ValueError(msg)
        return self.nanoseconds / 1e9


def sep(n: int = 20) -> None:
    """Print a separator of `n` "-" characters."""
    print("-" * n)
