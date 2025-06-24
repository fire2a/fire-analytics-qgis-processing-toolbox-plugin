#!python
"""Test script for the qgis processing plugin"""
import sys
from os import environ, pathsep
from pathlib import Path
from platform import system as platform_system
from shutil import which

import pytest
# SET QGIS
from qgis.core import QgsApplication, QgsCoordinateReferenceSystem, QgsRasterLayer

if platform_system() == "Windows":
    QgsApplication.setPrefixPath("C:\\PROGRA~1\\QGIS33~1.1", True)  # FIXME
else:
    QgsApplication.setPrefixPath("/usr", True)
qgs = QgsApplication([], False)
qgs.initQgis()

# Append the path where processing plugin can be found
if platform_system() == "Windows":
    sys.path.append("C:\\PROGRA~1\\QGIS33~1.1\\apps\\qgis\\python\\plugins")  # FIXME
else:
    sys.path.append("/usr/share/qgis/python/plugins")

# SET PROCESSING PLUGIN
import processing
from processing.core.Processing import Processing

Processing.initialize()
# Append the path where your processing plugin is
if platform_system() == "Windows":
    sys.path.append(
        "C:\\Users\\FernandoBadilla\\AppData\\Roaming\\QGIS\\QGIS3\\profiles\\default\\python\\plugins"
    )  # FIXME
else:
    sys.path.append("/home/fdo/.local/share/QGIS/QGIS3/profiles/default/python/plugins/")
# Add the algorithm provider
from fireanalyticstoolbox.fireanalyticstoolbox_provider import FireToolboxProvider

provider = FireToolboxProvider()
QgsApplication.processingRegistry().addProvider(provider)


def help_print():
    """algorithmHelp doesn't return anything, must be captured in a buffer"""
    from contextlib import redirect_stdout
    from io import StringIO

    buf = StringIO()
    with redirect_stdout(buf):
        processing.algorithmHelp("fire2a:instancedownloader")
    output = buf.getvalue()
    assert isinstance(output, str)
    assert "Instance Downloader" in output


@pytest.fixture
def instance_download():
    """Test the instance downloader algorithm"""

    alg = "fire2a:instancedownloader"
    params = {"FileDestination": "TEMPORARY_OUTPUT", "INSTANCE": 1, "Unzip": True}

    result = processing.run(alg, params)

    assert result is not None
    assert "OUTPUT" in result
    assert result["OUTPUT"] is not None
    assert isinstance(Path(result["OUTPUT"]), Path)
    assert Path(result["OUTPUT"]).is_file()
    return Path(result["OUTPUT"]).parent / "Kitral" / "Portezuelo"


@pytest.fixture
def simulation(instance_download):
    """Test the simulate algorithm"""
    # check files
    instance_download = Path("/tmp/processing_rGXZBA/f174ed44fd5f4e0a8807e7e30463f22b/Kitral/Portezuelo-asc")
    elevation = instance_download / "elevation.asc"
    fuels = instance_download / "fuels.asc"
    weather = instance_download / "Weather.csv"
    for afile in [elevation, fuels, weather]:
        assert afile.is_file(), f"File {afile} does not exist"
    # assign crs to rasters
    elevation = QgsRasterLayer(str(elevation), "elevation")
    fuels = QgsRasterLayer(str(fuels), "fuels")
    crs = QgsCoordinateReferenceSystem("EPSG:32719")
    assert crs.isValid(), f"CRS {crs.authid()} is not valid"
    elevation.setCrs(crs)
    fuels.setCrs(crs)
    assert elevation.isValid(), "Elevation layer is not valid"
    assert fuels.isValid(), "Fuels layer is not valid"
    # run the algorithm
    alg = "fire2a:cell2firesimulator"
    params = {
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
        "InstanceDirectory": "TEMPORARY_OUTPUT",
        "InstanceInProject": False,
        "LiveAndDeadFuelMoistureContentScenario": 2,
        "NumberOfSimulations": 3,
        "OtherCliArgs": "",
        "OutputOptions": [1, 2, 3, 4, 0, 5, 6, 7, 8, 9, 10, 11, 12],
        "RandomNumberGeneratorSeed": 123,
        "ResultsDirectory": "TEMPORARY_OUTPUT",
        "ResultsInInstance": False,
        "SetFuelLayerStyle": False,
        "SimulationThreads": 3,
        "WeatherDirectory": "",
        "WeatherFile": str(weather),
        "WeatherMode": 0,
    }

    result = processing.run(alg, params)
    """
    [ins] In [30]: result
    Out[30]: 
    {'Byram Surface Intensity': '/tmp/processing_rGXZBA/2abddc9bf012404bb3d10ffc36ba2593/ResultsDirectory/SurfaceIntensity/SurfaceIntensity2.asc',
     'Crown Fire Fuel Consumption Ratio': None,
     'Crown Fire Scar': None,
     'Crown Flame Length': None,
     'Crown Intensity': None,
     'Final Fire Scar': '/tmp/processing_rGXZBA/2abddc9bf012404bb3d10ffc36ba2593/ResultsDirectory/Grids/Grids1/ForestGrid0.csv',
     'Hit Rate Of Spread': '/tmp/processing_rGXZBA/2abddc9bf012404bb3d10ffc36ba2593/ResultsDirectory/RateOfSpread/ROSFile2.asc',
     'Ignition Points': None,
     'InstanceDirectory': '/tmp/processing_rGXZBA/f6f7acbe72704065b2360e34d73ca439/InstanceDirectory',
     'LogFile': '/tmp/processing_rGXZBA/2abddc9bf012404bb3d10ffc36ba2593/ResultsDirectory/LogFile.txt',
     'Max Flame Length': None,
     'OutputOptions': [1, 2, 3, 4, 0, 5, 6, 7, 8, 9, 10, 11, 12],
     'Propagation Directed Graph': '/tmp/processing_rGXZBA/2abddc9bf012404bb3d10ffc36ba2593/ResultsDirectory/Messages/MessagesFile2.csv',
     'Propagation Fire Scars': '/tmp/processing_rGXZBA/2abddc9bf012404bb3d10ffc36ba2593/ResultsDirectory/Grids/Grids1/ForestGrid0.csv',
     'ResultsDirectory': '/tmp/processing_rGXZBA/2abddc9bf012404bb3d10ffc36ba2593/ResultsDirectory',
     'Surface Burn Fraction': None,
     'Surface Flame Length': '/tmp/processing_rGXZBA/2abddc9bf012404bb3d10ffc36ba2593/ResultsDirectory/SurfaceFlameLength/SurfaceFlameLength2.asc'}
     """
     assert Path(result["InstanceDirectory"]).is_dir(), "Instance directory does not exist"
     assert Path(result["ResultsDirectory"]).is_dir(), "Results directory does not exist"
     assert Path(result["LogFile"]).is_file(), "Log file does not exist"
     assert Path(result["Ignition Points"]).is_file(), "Final fire scar file does not exist"
     return result


def bundle(simulation):
    """Test the bundle algorithm"""
    alg = "fire2a:simulationresultsprocessing"
    params = {
        "BaseLayer": "/home/fdo/source/fire/C2F-W/data/Kitral/Portezuelo-asc/elevation.asc",
        "EnablePropagationDiGraph": True,
        "EnablePropagationScars": True,
        "OutputDirectory": "TEMPORARY_OUTPUT",
        "ResultsDirectory": "/tmp/processing_kRxcoc",
    }

    result = processing.run(alg, params)

    assert result is not None
    assert "OUTPUT" in result
    assert result["OUTPUT"] is not None
    assert isinstance(Path(result["OUTPUT"]), Path)
    assert Path(result["OUTPUT"]).is_file()
    return Path(result["OUTPUT"])
