# Security Tests

| Goal | Test | Code under test |
| --- | --- | --- |
| SG-01: mission commands require certificates and safe limits | `tests/security/test_solution_policies.py` | `src_solution/abu/tcb/policies.py` |
| SG-02: untrusted advisory code cannot directly command control | `tests/security/test_solution_security_monitor.py` | `src_solution/abu/tcb/security_monitor.py`, `src_solution/abu/tcb/domains.py` |
| SG-03: trusted decisions are journaled | `tests/test_solution_event_log.py` | `src_solution/abu/tcb/event_log.py` |
| SG-04: Digital Mine requests pass only through the monitor | `tests/security/test_solution_security_monitor.py` | `src_solution/abu/tcb/security_monitor.py` |

The security marker is used by the solution tests so they can be run separately:
`pytest -m security tests/security`.

