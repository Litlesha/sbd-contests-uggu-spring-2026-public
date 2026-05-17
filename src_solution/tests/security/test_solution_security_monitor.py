"""Security monitor tests for domain isolation and mediated requests."""

from __future__ import annotations

import pytest

from src_solution.abu.tcb.domains import Domain, DomainMessage
from src_solution.abu.tcb.event_log import EventLog
from src_solution.abu.tcb.security_monitor import SecurityMonitor


@pytest.mark.security
def test_security_monitor_blocks_forbidden_domain_flow() -> None:
    log = EventLog()
    monitor = SecurityMonitor(event_log=log)
    message = DomainMessage(
        source=Domain.AI_OTHER,
        target=Domain.CONTROL,
        action="direct_control",
        payload={"mission_id": "M-3"},
    )

    decision = monitor.authorize_flow(message)

    assert decision.allowed is False
    assert decision.reason == "flow_not_allowed"
    assert "blocked flow" in log.read_full_tail()


@pytest.mark.security
def test_security_monitor_admits_valid_digital_mine_request() -> None:
    monitor = SecurityMonitor(event_log=EventLog())
    message = DomainMessage(
        source=Domain.DIGITAL_MINE,
        target=Domain.TCB,
        action="mission_request",
        payload={
            "mission_id": "M-4",
            "depth_m": 120.0,
            "azimuth_deg": 180.0,
            "requested_by": "digital_mine",
            "certificate_id": "cert-ok",
        },
    )

    response = monitor.admit_mission(message)

    assert response.accepted is True
    assert response.target is Domain.CONTROL
    assert response.payload["normalized_depth_m"] == 120.0
