#!python
# from IPython.terminal.embed import InteractiveShellEmbed
# InteractiveShellEmbed()()
import contextlib
from io import StringIO
from pathlib import Path
from shutil import copy, move

import pytest
from qgis.core import QgsCoordinateReferenceSystem, QgsProject, QgsRasterLayer, QgsVectorLayer


def get_algo_help(algo_id: str, processing_module) -> str:
    """Capture and return the help output of a processing algorithm."""
    stdout_capture = StringIO()
    with contextlib.redirect_stdout(stdout_capture):
        processing_module.algorithmHelp(algo_id)
    return stdout_capture.getvalue()


# LOCAL OVERRIDE FOR TESTING WITHOUT DOWNLOADING
# @pytest.mark.dependency()
# def test_download_instance(qgis_app, fire2a_provider, sandbox):
#     download_dir = Path("~/source/fire/C2F-W/data/Kitral/Portezuelo-asc").expanduser()
#     data_dir = sandbox / "data"
#     data_dir.mkdir()
#     copy(download_dir / "fuels.asc", data_dir)
#     copy(download_dir / "elevation.asc", data_dir)
#     copy(download_dir / "Weather.csv", data_dir)


@pytest.mark.dependency()
def test_download_instance(qgis_app, fire2a_provider, sandbox):
    import processing

    download_dir = sandbox / "Kitral/Portezuelo-asc"
    data_dir = sandbox / "data"

    file_dst = sandbox / "download.zip"
    print(f"{file_dst=}")

    algo_name = "fire2a:instancedownloader"
    algo_help = get_algo_help(algo_name, processing)
    print(algo_name, algo_help)
    assert len(algo_help) > 0, f"Algorithm {algo_name} help is empty"
    output01 = processing.run(
        algo_name,
        {"FileDestination": str(file_dst), "INSTANCE": 1, "Open": False, "Unzip": True},
    )
    assert file_dst.is_file(), "Downloaded data file does not exist"
    assert output01["OUTPUT"] == str(file_dst), "Output path mismatch with provided destination"

    assert download_dir.is_dir(), "Unzipped data directory does not exist"
    files = [f.name for f in download_dir.iterdir() if f.is_file() and f.stat().st_size > 0]
    assert "fuels.asc" in files, "Expected file 'fuels.asc' not found in download directory"
    assert "elevation.asc" in files, "Expected file 'elevation.asc' not found in download directory"
    assert "Weather.csv" in files, "Expected file 'Weather.csv' not found in download directory"

    move(download_dir, data_dir)


# A implicit
# @pytest.mark.parametrize("number_of_simulations", [1, 3])
# @pytest.mark.dependency(depends=["test_download_instance"])
# B explicit
@pytest.mark.parametrize(
    "number_of_simulations",
    [
        pytest.param(1, marks=pytest.mark.dependency(depends=["test_download_instance"], name="test_simulate[1]")),
        pytest.param(3, marks=pytest.mark.dependency(depends=["test_download_instance"], name="test_simulate[3]")),
    ],
)
def test_simulate(qgis_app, fire2a_provider, sandbox, number_of_simulations):
    import processing

    data_dir = sandbox / "data"
    if not data_dir.is_dir():
        pytest.skip("Data directory not found, skipping simulation test")
    instance_dir = sandbox / f"instance_{number_of_simulations}"
    results_dir = sandbox / f"results_{number_of_simulations}"

    c2f = next(algo for algo in fire2a_provider.algorithms() if algo.id() == "fire2a:cell2firesimulator")
    rc, msg = c2f.canExecute()
    assert rc, "cell2firesimulator can't execute: " + msg

    # set up layers
    crs = QgsCoordinateReferenceSystem("EPSG:32718")
    fuels = QgsRasterLayer(str(data_dir / "fuels.asc"), "fuels")
    elevation = QgsRasterLayer(str(data_dir / "elevation.asc"), "elevation")
    fuels.setCrs(crs)
    elevation.setCrs(crs)
    assert fuels.isValid(), "Fuels raster layer is not valid"
    assert elevation.isValid(), "Elevation raster layer is not valid"

    algo_name = "fire2a:cell2firesimulator"
    algo_help = get_algo_help(algo_name, processing)
    print(algo_name, algo_help)
    assert len(algo_help) > 0, f"Algorithm {algo_name} help is empty"
    output02 = processing.run(
        algo_name,
        {
            "CbdRaster": None,
            "CbhRaster": None,
            "CcfRaster": None,
            "DryRun": False,
            "ElevationRaster": elevation,
            "EnableCrownFire": False,
            "FireBreaksRaster": None,
            "FoliarMoistureContent": 66,
            "FuelModel": 1,
            "FuelRaster": fuels,
            "HmRaster": None,
            "IgnitionMode": 0,
            "IgnitionPointVectorLayer": None,
            "IgnitionProbabilityMap": None,
            "IgnitionRadius": 0,
            "InstanceDirectory": str(instance_dir),
            "InstanceInProject": False,
            "LiveAndDeadFuelMoistureContentScenario": 2,
            "NumberOfSimulations": number_of_simulations,
            "OtherCliArgs": "",
            "OutputOptions": [1, 2, 3, 4, 0, 5, 6, 7, 8, 9, 10, 11, 12],
            "RandomNumberGeneratorSeed": 123,
            "ResultsDirectory": str(results_dir),
            "ResultsInInstance": False,
            "SetFuelLayerStyle": False,
            "SimulationThreads": 3,
            "WeatherDirectory": "",
            "WeatherFile": str(data_dir / "Weather.csv"),
            "WeatherMode": 0,
        },
    )
    for k, v in output02.items():
        if isinstance(v, str) and Path(v).is_file():
            print(f"Checking output file for key {k}: {v}")
            assert Path(v).stat().st_size > 0, f"Output file {k} is empty: {v}"

    print(Path(output02["LogFile"]).read_text())


@pytest.mark.parametrize(
    "number_of_simulations",
    [
        pytest.param(1, marks=pytest.mark.dependency(depends=["test_simulate[1]"])),
        pytest.param(3, marks=pytest.mark.dependency(depends=["test_simulate[3]"])),
    ],
)
def test_loadresults(qgis_app, fire2a_provider, sandbox, number_of_simulations):
    import processing

    data_dir = sandbox / "data"
    instance_dir = sandbox / f"instance_{number_of_simulations}"
    results_dir = sandbox / f"results_{number_of_simulations}"
    if not instance_dir.is_dir() or not results_dir.is_dir():
        pytest.skip("Instance or results directory not found, skipping load results test")
    loaded_dir = sandbox / "loaded"

    crs = QgsCoordinateReferenceSystem("EPSG:32718")
    fuels = QgsRasterLayer(str(data_dir / "fuels.asc"), "fuels")
    fuels.setCrs(crs)

    algo_name = "fire2a:simulationresultsprocessing"
    algo_help = get_algo_help(algo_name, processing)
    print(algo_name, algo_help)
    assert len(algo_help) > 0, f"Algorithm {algo_name} help is empty"
    output03 = processing.run(
        algo_name,
        {
            "BaseLayer": fuels,
            "EnablePropagationDiGraph": True,
            "EnablePropagationScars": True,
            "ResultsDirectory": str(results_dir),
            "OutputDirectory": str(loaded_dir),
        },
    )
    print(output03)
    # TODO make bundle algo output files into loaded dir


@pytest.mark.parametrize(
    "number_of_simulations",
    [
        pytest.param(1, marks=pytest.mark.dependency(depends=["test_simulate[1]"])),
        pytest.param(3, marks=pytest.mark.dependency(depends=["test_simulate[3]"])),
    ],
)
@pytest.mark.qgis_show_map(timeout=5, zoom_to_common_extent=True)
def test_04_propagationdigraph(qgis_app, fire2a_provider, sandbox, number_of_simulations):
    import processing

    data_dir = sandbox / "data"
    instance_dir = sandbox / f"instance_{number_of_simulations}"
    results_dir = sandbox / f"results_{number_of_simulations}"
    if not instance_dir.is_dir() or not results_dir.is_dir():
        pytest.skip("Instance or results directory not found, skipping load propagation digraph test")

    crs = QgsCoordinateReferenceSystem("EPSG:32718")
    fuels = QgsRasterLayer(str(data_dir / "fuels.asc"), "fuels")
    fuels.setCrs(crs)

    any_message_file = next((Path(results_dir / "Messages").rglob("MessagesFile*.csv")), None)
    if any_message_file is None:
        pytest.skip("No message files found in results, skipping propagation digraph test")

    algo_name = "fire2a:propagationdigraph"
    algo_help = get_algo_help(algo_name, processing)
    print(algo_name, algo_help)
    assert len(algo_help) > 0, f"Algorithm {algo_name} help is empty"

    digraph_path = sandbox / "propagation_digraph.gpkg"
    output04 = processing.run(
        algo_name,
        {
            "BaseLayer": fuels,
            "SampleMessagesFile": str(any_message_file),
            "PropagationDirectedGraph": str(digraph_path),
            "PickledMessages": str(sandbox / "messages.pickle"),
        },
    )
    print(output04)

    # Load the geopackage into QGIS
    if digraph_path.exists():
        # Load the vector layer from geopackage
        digraph_layer = QgsVectorLayer(str(digraph_path), "Propagation DiGraph", "ogr")
        if digraph_layer.isValid():
            QgsProject.instance().addMapLayer(digraph_layer)
            print(f"Loaded propagation digraph layer with {digraph_layer.featureCount()} features")
        else:
            print(f"Warning: Could not load digraph layer from {digraph_path}")

    # The map will be displayed here for 30 seconds due to @pytest.mark.qgis_show_map
    # TODO output directory must exist
