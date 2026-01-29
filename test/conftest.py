#!python3
"""Pytest configuration and fixtures for Fire Analytics Toolbox tests."""

# from IPython.terminal.embed import InteractiveShellEmbed

# InteractiveShellEmbed()()

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
    assert toolbox_dir not in sys.path, "Toolbox path:{toolbox_dir} already in sys.path"
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
