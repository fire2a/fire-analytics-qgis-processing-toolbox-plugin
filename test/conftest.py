#!python
"""Pytest configuration and fixtures for Fire Analytics Toolbox tests."""

import logging
import sys
from pathlib import Path

import pytest


@pytest.fixture(scope="session")
def sandbox(tmp_path_factory):
    return tmp_path_factory.mktemp("sandbox")


@pytest.fixture(scope="session")
def fire2a_provider(qgis_app, qgis_processing):
    """
    Register the Fire Analytics Toolbox provider with QGIS processing.

    Returns the registered provider instance.
    """
    toolbox_dir = str(Path(__file__).parent.parent)
    # print(f"{toolbox_dir=}")
    if toolbox_dir in sys.path:
        logging.warning(f"Toolbox path:{toolbox_dir} already in sys.path")
    else:
        sys.path.insert(0, toolbox_dir)

    from fireanalyticstoolbox.fireanalyticstoolbox_provider import FireToolboxProvider

    registry = qgis_app.processingRegistry()
    assert registry.providerById("fire2a") is None, "Fire2a provider already registered"
    registry.addProvider(FireToolboxProvider())

    provider = registry.providerById("fire2a")
    assert registry.providerById("fire2a") is not None, "Fire2a provider failed to register"

    fire2a_algos = [algo.id() for algo in provider.algorithms()]
    # print(f"Fire2a algorithms: {fire2a_algos}")
    assert len(fire2a_algos) > 0, "No fire2a algorithms found"

    yield provider

    # Cleanup: remove provider after tests
    registry.removeProvider(provider)


def DISABLED_pytest_collection_modifyitems(items):
    """specify order of test execution
    https://medium.com/@thananjayan1988/pytest-control-order-of-test-class-and-module-execution-d1f93656ce8a

    Using pytest-dependency instead https://pytest-dependency.readthedocs.io/
    """
    # print(items)
    # items_bak = items.copy()
    order = {
        "test_01_download_instance": 1,
        "test_02_simulate[1]": 2,
        "test_03_loadresults[1]": 3,
        "test_04_propagationdigraph[1]": 4,
        "test_02_simulate[3]": 5,
        "test_04_propagationdigraph[1]": 6,
        "test_03_loadresults[3]": 7,
    }
    items.sort(key=lambda item: order.get(item.name, 9999))
    # pytest --collect-only
