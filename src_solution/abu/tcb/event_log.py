"""Append-only event log for trusted ABU decisions."""

from __future__ import annotations

from collections import deque
from dataclasses import dataclass
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from threading import RLock


class EventLevel(str, Enum):
    """Severity levels used by the ABU security journal."""

    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


@dataclass(frozen=True)
class EventRecord:
    """Normalized journal entry."""

    timestamp: str
    level: EventLevel
    domain: str
    action: str
    message: str

    def as_line(self) -> str:
        return (
            f"{self.timestamp}\t{self.level.value}\t{self.domain}\t"
            f"{self.action}\t{self.message}"
        )


class EventLog:
    """Small durable journal with a bounded in-memory ring buffer."""

    def __init__(
        self,
        log_dir: Path | None = None,
        ring_size: int = 64,
    ) -> None:
        self._dir = log_dir
        self._ring: deque[EventRecord] = deque(maxlen=max(1, ring_size))
        self._lock = RLock()
        self._full_path = (
            self._dir / "abu_events.log" if self._dir else None
        )
        if self._dir is not None:
            self._dir.mkdir(parents=True, exist_ok=True)

    def record(
        self,
        level: EventLevel,
        message: str,
        *,
        domain: str = "system",
        action: str = "event",
    ) -> EventRecord:
        """Record an event and return the normalized entry."""
        record = EventRecord(
            timestamp=datetime.now(timezone.utc).isoformat(),
            level=level,
            domain=domain,
            action=action,
            message=message,
        )
        line = record.as_line() + "\n"
        with self._lock:
            self._ring.append(record)
            if self._full_path is not None:
                with self._full_path.open("a", encoding="utf-8") as handle:
                    handle.write(line)
        return record

    def ring_snapshot(self) -> list[EventRecord]:
        """Return recent events from oldest to newest."""
        with self._lock:
            return list(self._ring)

    def read_full_tail(self, limit: int = 20) -> str:
        """Return the last lines from the durable journal."""
        if self._full_path is None or not self._full_path.exists():
            return "\n".join(
                item.as_line() for item in self.ring_snapshot()[-limit:]
            )
        lines = self._full_path.read_text(encoding="utf-8").splitlines()
        return "\n".join(lines[-limit:])
