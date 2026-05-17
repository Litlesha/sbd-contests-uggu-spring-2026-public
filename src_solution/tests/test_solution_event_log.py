"""Repository-level tests importing src_solution and event_log."""

from __future__ import annotations

from src_solution.abu.tcb.event_log import EventLevel, EventLog


def test_solution_event_log_keeps_ring_and_tail(tmp_path) -> None:
    event_log = EventLog(tmp_path, ring_size=2)
    event_log.record(EventLevel.INFO, "one", domain="tcb", action="test")
    event_log.record(EventLevel.WARNING, "two", domain="tcb", action="test")
    event_log.record(EventLevel.ERROR, "three", domain="tcb", action="test")

    snapshot = event_log.ring_snapshot()

    assert len(snapshot) == 2
    assert snapshot[0].message == "two"
    assert "three" in event_log.read_full_tail()
