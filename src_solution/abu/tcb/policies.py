"""Safety and security policies for ABU mission admission."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class MissionRequest:
    """Mission request normalized at the trust boundary."""

    mission_id: str
    depth_m: float
    azimuth_deg: float
    requested_by: str
    certificate_id: str | None = None
    emergency_stop: bool = False


@dataclass(frozen=True)
class PolicyDecision:
    """Decision returned by trusted policy evaluation."""

    allowed: bool
    reason: str
    normalized_depth_m: float | None = None


@dataclass(frozen=True)
class SafetyPolicy:
    """Deterministic rules for the trusted computing base."""

    max_depth_m: float = 5000.0
    min_depth_m: float = 1.0
    require_certificate: bool = True

    def evaluate_mission(self, mission: MissionRequest) -> PolicyDecision:
        """Validate mission limits, certificate presence, and stop state."""
        if mission.emergency_stop:
            return PolicyDecision(False, "emergency_stop")
        if self.require_certificate and not mission.certificate_id:
            return PolicyDecision(False, "missing_certificate")
        if mission.depth_m < self.min_depth_m:
            return PolicyDecision(False, "depth_too_small")
        if mission.depth_m > self.max_depth_m:
            return PolicyDecision(False, "depth_limit_exceeded")
        if not 0.0 <= mission.azimuth_deg <= 360.0:
            return PolicyDecision(False, "azimuth_out_of_range")
        return PolicyDecision(
            True,
            "allowed",
            normalized_depth_m=float(mission.depth_m),
        )
