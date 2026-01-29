# TESTING

## TL;DR
```bash
python3 -m venv venv --system-site-packages
source venv/bin/activate
pip install -r requirements-test.txt
bash -c "source venv/bin/activate && pytest"
```
Some simulator children processes sometimes linger blocking the terminal.
Because `C2F > QProcess > QgsProcessingAlgorithm > QGIS > pytest` is a long way to go,
Encapsulating the test run in a separate bash shell helps to isolate the lingering processes.

## some options

1. enabling logging output `pytest --log-cli-level=INFO`
2. enabling clearing the cache `pytest --cache-clear` for failing tests
3. just collecting `pytest --collect-only` when adding new tests
4. there's a mock test for replacing download when needed

## files

1. `requirements-test.txt`
2. `pyproject.toml::[tool.pytest]`
3. `test/test_*.py`
