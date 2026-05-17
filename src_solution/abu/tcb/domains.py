"""Security domains and monitor-mediated messages."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from types import MappingProxyType
from typing import Mapping


class Domain(str, Enum):
    """Isolated ABU domains."""

    DIGITAL_MINE = "digital_mine"
    TCB = "tcb"
    CONTROL = "control"
    TELEMETRY = "telemetry"
    AI_OTHER = "ai_other"


@dataclass(frozen=True)
class DomainMessage:
    """Message that must pass through the security monitor."""

    source: Domain
    target: Domain
    action: str
    payload: Mapping[str, object]

    def safe_payload(self) -> Mapping[str, object]:
        """Expose payload as read-only data to trusted code."""
        return MappingProxyType(dict(self.payload))


ALLOWED_FLOWS: frozenset[tuple[Domain, Domain]] = frozenset(
    {
        (Domain.DIGITAL_MINE, Domain.TCB),
        (Domain.TCB, Domain.CONTROL),
        (Domain.CONTROL, Domain.TCB),
        (Domain.TELEMETRY, Domain.TCB),
        (Domain.AI_OTHER, Domain.TCB),
        (Domain.TCB, Domain.DIGITAL_MINE),
    }
)
