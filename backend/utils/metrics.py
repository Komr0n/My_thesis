from __future__ import annotations

import time
from contextlib import contextmanager
from dataclasses import dataclass, field
from typing import Dict


@dataclass
class TimingCollector:
    timings: Dict[str, float] = field(default_factory=dict)
    start_time: float = field(default_factory=time.perf_counter)

    @contextmanager
    def track(self, key: str):
        start = time.perf_counter()
        try:
            yield
        finally:
            end = time.perf_counter()
            self.timings[key] = (end - start) * 1000

    def total(self) -> float:
        return (time.perf_counter() - self.start_time) * 1000
