"""Monitor that mediates requests and responses between ABU domains."""

from __future__ import annotations

from dataclasses import dataclass

from src_solution.abu.tcb.domains import ALLOWED_FLOWS, Domain, DomainMessage
from src_solution.abu.tcb.event_log import EventLevel, EventLog
from src_solution.abu.tcb.policies import (
    MissionRequest,
    PolicyDecision,
    SafetyPolicy,
)


@dataclass(frozen=True)
class MonitorResponse:
    """Controlled response emitted by the security monitor."""

    accepted: bool
    reason: str
    target: Domain
    payload: dict[str, object]


class SecurityMonitor:
    """Reference monitor for trusted request and response checks."""

    def __init__(
        self,
        *,
        policy: SafetyPolicy | None = None,
        event_log: EventLog | None = None,
    ) -> None:
        self.policy = policy or SafetyPolicy()
        self.event_log = event_log or EventLog()

    def authorize_flow(self, message: DomainMessage) -> PolicyDecision:
        """Check that an inter-domain request is allowed."""
        if (message.source, message.target) not in ALLOWED_FLOWS:
            self.event_log.record(
                EventLevel.WARNING,
                f"blocked flow {message.source.value}->{message.target.value}",
                domain="security_monitor",
                action="authorize_flow",
            )
            return PolicyDecision(False, "flow_not_allowed")
        return PolicyDecision(True, "flow_allowed")

    def admit_mission(self, message: DomainMessage) -> MonitorResponse:
        """Authorize a mission command from the digital mine to the TCB."""
        flow = self.authorize_flow(message)
        if not flow.allowed:
            return MonitorResponse(False, flow.reason, Domain.DIGITAL_MINE, {})

        payload = message.safe_payload()
        mission = MissionRequest(
            mission_id=str(payload.get("mission_id", "")),
            depth_m=float(payload.get("depth_m", 0.0)),
            azimuth_deg=float(payload.get("azimuth_deg", 0.0)),
            requested_by=str(payload.get("requested_by", "unknown")),
            certificate_id=(
                str(payload["certificate_id"])
                if payload.get("certificate_id")
                else None
            ),
            emergency_stop=bool(payload.get("emergency_stop", False)),
        )
        decision = self.policy.evaluate_mission(mission)
        level = EventLevel.INFO if decision.allowed else EventLevel.WARNING
        self.event_log.record(
            level,
            f"mission {mission.mission_id}: {decision.reason}",
            domain="security_monitor",
            action="admit_mission",
        )
        return MonitorResponse(
            accepted=decision.allowed,
            reason=decision.reason,
            target=Domain.CONTROL if decision.allowed else Domain.DIGITAL_MINE,
            payload={
                "mission_id": mission.mission_id,
                "normalized_depth_m": decision.normalized_depth_m,
            },
        )
