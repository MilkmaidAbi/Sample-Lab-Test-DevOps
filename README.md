# Sample Lab Test (HARD): ET0735 DevOps for AIoT

A harder practice version of **Lab Test 1** (Git · Python · PyTest), written in the same format as the official Sample Lab Test 1 (Fitness Tracker).

| File | What it is |
|---|---|
| [`LabTest.md`](LabTest.md) | **The paper.** Read this first. |
| `starter/greenhouse.py` | The application, with function stubs to implement and two planted defects |
| `starter/test_greenhouse.py` | The test file (one given test, which currently fails) |
| `starter/readings.csv` | Sensor data, loaded as a list of dictionaries (values are strings!) |

## How to sit it
1. Set a **90-minute timer**. Cheatsheet only, no AI.
2. Copy the files in `starter/` into the root of your attempt repository and follow `LabTest.md` from Part A.

## Solutions and marking (no peeking)
The `solutions` branch has a reference solution, a full **hidden test suite**, model answers for Part D, and a marking guide (`MARKING.md`).
To mark yourself, copy `solutions/test_greenhouse.py` into your attempt (as `test_hidden.py`) and run `python -m pytest -v`. Every test should pass against your code.

```bash
git fetch origin
git checkout solutions
```
