"""Compatibility health check used by repository smoke tests."""


def tcb_health() -> str:
    """Return the health state of the trusted code package."""
    return "ok"
