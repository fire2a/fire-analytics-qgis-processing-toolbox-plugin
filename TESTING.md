# TESTING

## TL;DR

Install QGIS, in a system-aware python virtual environment testing dependencies and fire2a-lib.  
Place the C2F-W binary and run pytest.  

```bash
sudo apt install qgis qgis-plugin-grass python3-venv python3-pip

python3 -m venv venv --system-site-packages
source venv/bin/activate
pip install -r requirements-test.txt

pip install fire2a-lib                            # or clone and pip install -e .
ln -s ../path/to/C2F-W firetoolbox/simulator/C2F  # symlink or copy C2F-W code or release

pytest
```

Don't close the QGIS raised windows during the tests! 
Your terminal may get blocked for a while.

`C2F > QProcess > QgsProcessingAlgorithm > QGIS > pytest` is a long way to go... 

## Microsoft Headache

1. Install QGIS
2. Open OSGeo4W Shell

    python-qgis.bat -c exit()
    pip install fire2a-lib                            
    pip install -r requirements-test.txt
    pytest

## some options

1. enabling logging output `pytest --log-cli-level=INFO`
2. enabling clearing the cache `pytest --cache-clear` for failing tests
3. just collecting `pytest --collect-only` when adding new tests
4. there's a mock test for replacing download when needed

## check this files

1. `requirements-test.txt`
2. `pyproject.toml::[tool.pytest]`
3. `test/test_*.py`
