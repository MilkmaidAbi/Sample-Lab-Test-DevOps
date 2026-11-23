# Part D: model answers

1. **Why not commit `__pycache__/` and `.pytest_cache/`?**
   They are generated automatically: compiled `.pyc` bytecode and pytest's run cache. They are rebuilt on every machine, differ between Python versions, add noise to every commit and can cause merge conflicts. Only source files belong in Git, so they go in `.gitignore`.

2. **Positive vs negative test case.**
   A positive test gives **valid** input and checks the expected result, e.g. `add_reading(data, " b ", "26.5", "60", "45") == 0`. A negative test gives **invalid or unexpected** input and checks the function rejects or handles it, e.g. `add_reading(data, "A", "hot", "50", "50") == 2`, or `get_hottest_reading([]) is None`.

3. **Why `max(readings, key=lambda r: r["temperature"])` is wrong.**
   `csv.DictReader` stores every value as a **string**, so `max` compares the text character by character, not the numbers. `"9.5"` starts with `"9"`, which is greater than `"3"` or `"2"`, so it returns **R003 (9.5 °C)**, the coldest reading, instead of R004 (35.2 °C). Fix: `key=lambda r: float(r["temperature"])`.

4. **`if __name__ == "__main__":`**
   `__name__` is `"__main__"` only when the file is run directly. When pytest **imports** `greenhouse.py`, it is `"greenhouse"`, so `main()` does not run. Without the guard, importing would start the menu loop and call `input()`. Pytest would then fail with `OSError: pytest: reading from stdin while output is captured!`, and `load_readings("readings.csv")` could also raise `FileNotFoundError` depending on the working folder.

5. **V-model and DEF-02.**
   Unit testing is the partner of the **software development / coding** phase: it verifies each function against its detailed design and requirements. DEF-02 was not caught because `get_reading_by_id()` had **no unit test**. The only ID ever tried was `R001`, the first record, which happens to work. A test with a second record (e.g. `R004`) and a not-found ID exposes the `return None` inside the loop immediately.
