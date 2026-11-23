# Marking guide (100 marks)

## Quick auto-check
Copy `solutions/test_greenhouse.py` into your attempt as `test_hidden.py` and run `python -m pytest -v test_hidden.py`.
It has 11 tests. Each one was checked to **fail** on the typical mistakes listed under Part B, so a pass is meaningful.

## Part A: setup and Git (15)
| Marks | Check |
|---|---|
| 3 | Starter files committed at the repo root with message `Add starter code` |
| 4 | `.gitignore` contains at least `__pycache__/` and `.pytest_cache/` (`*.pyc` is a bonus); commit `Add gitignore`; no cache files on GitHub at any point |
| 6 | `README.md`: H1 `Smart Greenhouse Monitor` (2), description sentence (1), H2 `Requirements Traceability` + a Markdown table that renders, with the 3 columns and REQ-01..05 rows (3) |
| 2 | Commit message `Add readme`, all pushed |

## Part B: Python (35)
| Marks | REQ | Lose marks for |
|---|---|---|
| 5 | REQ-01 | case-sensitive match (−2), not stripping spaces (−2), not returning `[]` when nothing matches (−1) |
| 7 | REQ-02 | comparing strings instead of numbers (min/max wrong for zone A) (−3), average not rounded to 2 d.p. (−1), wrong keys (−2), not returning `None` for an empty zone (−1) |
| 5 | REQ-03 | no `float()` (picks R003 "9.5") (−3), `>=` so the **last** tied reading wins (R008, not R004) (−1), empty not `None` (−1) |
| 7 | REQ-04 | each wrong boundary (`>` vs `>=` at 35/30, `<=` vs `<` at 20/35) (−1 each, max −4), summary missing zero keys (−2), CRITICAL not taking priority (−1) |
| 8 | REQ-05 | wrong check order (−2), ID = count + 1 instead of highest + 1 (−2), 0/100 not inclusive (−1), zone not stored uppercase / values not stored as strings (−1), crashes on `"hot"` or `""` instead of returning 2 (−2) |
| 3 | REQ-06 | option 5 messages not exact (−1), `q` doesn't quit (−1), no `Invalid option` (−1) |

Git in Part B (included above; deduct from the REQ total, max −6): branch `feature/requirements` exists on GitHub (−2 if missing); 3 exact commit messages in order (−1 each); merged into `main`; tag `v1.0` annotated with message `Requirements implemented` and pushed (−2 if missing or lightweight).

## Part C: defects and tests (40)
| Marks | Check |
|---|---|
| 4 | DEF-01 fixed (`* 9 / 5 + 32`), given test unchanged and passing |
| 6 | DEF-02: `Add failing test for DEF-02` commit exists **before** the fix, and that test **does fail** when checked out on that commit (3); fix moves `return None` after the loop (3) |
| 20 | Table 3 tests: about 3 marks each for zone / stats / hottest / summary, 4 for classify, 4 for add_reading. Full marks only with normal + empty/not-found + **every** boundary (BMI-style: 35.0/34.9, 30.0/29.9, 19.9/20, 34.9/35). Floats compared with `pytest.approx` (or exact rounded values). Tests must not read the CSV. |
| 3 | README traceability table completed |
| 3 | `Fix DEF-01 and DEF-02` + `Implement PyTest test cases` exact messages, all pushed, everything green |
| 4 | Tag `v2.0` (annotated, message `Defects fixed and tested`) pushed (2) + GitHub Release titled `Greenhouse Monitor v2.0` from it (2) |

## Part D: review (10)
2 marks each, compared with `solutions/ANSWERS.md`. Q2 needs examples from **your** test file. Q3 must name **R003** and explain string comparison.

## Grade bands (self-check)
85+: you're over-prepared for the real one · 70–84: solid, re-drill whatever you lost marks on · 50–69: redo REQ-04/05 and their tests from scratch · <50: go through study sheet §1.9 and §3 again, then retake this tomorrow.
