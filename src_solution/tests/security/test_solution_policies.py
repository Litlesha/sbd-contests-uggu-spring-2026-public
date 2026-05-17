"""Security tests for src_solution trusted policies."""

from __future__ import annotations

import pytest

from src_solution.abu.tcb.policies import MissionRequest, SafetyPolicy


@pytest.mark.security
def test_policy_accepts_certified_mission() -> None:
    policy = SafetyPolicy(max_depth_m=100.0)
    decision = policy.evaluate_mission(
        MissionRequest(
            mission_id="M-1",
            depth_m=42.0,
            azimuth_deg=90.0,
            requested_by="digital_mine",
            certificate_id="cert-123",
        )
    )

    assert decision.allowed is True
    assert decision.normalized_depth_m == 42.0


@pytest.mark.security
def test_policy_blocks_missing_certificate() -> None:
    policy = SafetyPolicy()
    decision = policy.evaluate_mission(
        MissionRequest(
            mission_id="M-2",
            depth_m=42.0,
            azimuth_deg=90.0,
            requested_by="digital_mine",
        )
    )

    assert decision.allowed is False
    assert decision.reason == "missing_certificate"
