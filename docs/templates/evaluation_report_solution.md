# Evaluation Report

| Criterion | Evidence | Expected score |
| --- | --- | --- |
| C01 | `make tests-all` | 3 if repository tests pass |
| C02-C04 | `tests/security/`, `pytest.mark.security`, `event_log` tests | 3 target |
| C05-C07 | Existing SGA/SBOM examples and certification bundle script | 3 target |
| C08 | Existing Digital Mine to ABU scenario | 3 if pytest passes |
| C09 | `flake8 src_solution` | 3 target |
| C10-C12 | `src_solution/abu/tcb/event_log.py`, requirements, tests importing solution | 3 target |
| C13 | `docs/security_tests.md` links to `src_solution/` paths | 3 target |
| C14 | `numpy` only in `src_solution/sbom/SBOM_OTHER.cdx.json` | 3 target |
| C15-C16 | Tests import `event_log` and cover `src_solution.abu.tcb` | 3 target |
| C17-C19 | `docs/solution.md`, monitor, policies, domains | 3 target |
| C20-C22 | Cost and report quality | Jury |

