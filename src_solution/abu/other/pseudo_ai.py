"""Non-trusted helper logic that may use heavier dependencies such as numpy."""

from __future__ import annotations

import numpy as np


def estimate_drilling_score(depth_samples: list[float]) -> float:
    """Return a non-critical score used only as operator advice."""
    if not depth_samples:
        return 0.0
    values = np.array(depth_samples, dtype=float)
    return float(values.mean() / (values.std() + 1.0))
