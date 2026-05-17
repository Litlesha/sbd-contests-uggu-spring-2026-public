"""Coverage tests for src_solution.abu.tcb."""

from __future__ import annotations

from src_solution.abu.tcb.domains import Domain, DomainMessage
from src_solution.abu.tcb.event_log import EventLog
from src_solution.abu.tcb.policies import MissionRequest, SafetyPolicy
from src_solution.abu.tcb.security_monitor import SecurityMonitor


def test_tcb_policy_blocks_emergency_stop() -> None:
    policy = SafetyPolicy(require_certificate=False)
    decision = policy.evaluate_mission(
        MissionRequest(
            mission_id="M-5",
            depth_m=10.0,
            azimuth_deg=0.0,
            requested_by="test",
            emergency_stop=True,
        )
    )

    assert decision.allowed is False
    assert decision.reason == "emergency_stop"


def test_monitor_rejects_out_of_range_depth() -> None:
    monitor = SecurityMonitor(
        policy=SafetyPolicy(max_depth_m=10.0),
        event_log=EventLog(),
    )
    message = DomainMessage(
        source=Domain.DIGITAL_MINE,
        target=Domain.TCB,
        action="mission_request",
        payload={
            "mission_id": "M-6",
            "depth_m": 100.0,
            "azimuth_deg": 5.0,
            "requested_by": "digital_mine",
            "certificate_id": "cert",
        },
    )

    response = monitor.admit_mission(message)

    assert response.accepted is False
    assert response.reason == "depth_limit_exceeded"
