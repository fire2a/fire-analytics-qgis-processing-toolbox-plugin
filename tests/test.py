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


def test_help_print():
    """algorithmHelp doesn't return anything, must be captured in a buffer"""
    from contextlib import redirect_stdout
    from io import StringIO

    buf = StringIO()
    with redirect_stdout(buf):
        processing.algorithmHelp("fire2a:instancedownloader")
    output = buf.getvalue()
    assert isinstance(output, str)
    assert "Instance Downloader" in output


def test_download_simulate_bundle():
    """Test the instance downloader algorithm"""

    # download
    alg = "fire2a:instancedownloader"
    params = {"FileDestination": "TEMPORARY_OUTPUT", "INSTANCE": 1, "Unzip": True}

    instance = processing.run(alg, params)

    assert isinstance(instance, dict), "Instance is not a dictionary"
    assert "OUTPUT" in instance, "Instance dictionary does not contain OUTPUT key"
    assert instance["OUTPUT"] is not None, "Instance OUTPUT is None"
    assert Path(instance["OUTPUT"]).is_file(), "Instance OUTPUT is not a file"
    instance_dir = Path(instance["OUTPUT"]).parent / "Kitral" / "Portezuelo-asc"
    assert instance_dir.is_dir(), f"Instance directory {instance} does not exist"

    # simulate
    # prepare non-crs rasters
    elevation = instance_dir / "elevation.asc"
    fuels = instance_dir / "fuels.asc"
    weather = instance_dir / "Weather.csv"
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
    # run
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
    simulation = processing.run(alg, params)
    # [ins] In [30]: result
    # Out[30]:
    # {'Byram Surface Intensity': '/tmp/processing_rGXZBA/2abddc9bf012404bb3d10ffc36ba2593/ResultsDirectory/SurfaceIntensity/SurfaceIntensity2.asc',
    #  'Crown Fire Fuel Consumption Ratio': None,
    #  'Crown Fire Scar': None,
    #  'Crown Flame Length': None,
    #  'Crown Intensity': None,
    #  'Final Fire Scar': '/tmp/processing_rGXZBA/2abddc9bf012404bb3d10ffc36ba2593/ResultsDirectory/Grids/Grids1/ForestGrid0.csv',
    #  'Hit Rate Of Spread': '/tmp/processing_rGXZBA/2abddc9bf012404bb3d10ffc36ba2593/ResultsDirectory/RateOfSpread/ROSFile2.asc',
    #  'Ignition Points': None,
    #  'InstanceDirectory': '/tmp/processing_rGXZBA/f6f7acbe72704065b2360e34d73ca439/InstanceDirectory',
    #  'LogFile': '/tmp/processing_rGXZBA/2abddc9bf012404bb3d10ffc36ba2593/ResultsDirectory/LogFile.txt',
    #  'Max Flame Length': None,
    #  'OutputOptions': [1, 2, 3, 4, 0, 5, 6, 7, 8, 9, 10, 11, 12],
    #  'Propagation Directed Graph': '/tmp/processing_rGXZBA/2abddc9bf012404bb3d10ffc36ba2593/ResultsDirectory/Messages/MessagesFile2.csv',
    #  'Propagation Fire Scars': '/tmp/processing_rGXZBA/2abddc9bf012404bb3d10ffc36ba2593/ResultsDirectory/Grids/Grids1/ForestGrid0.csv',
    #  'ResultsDirectory': '/tmp/processing_rGXZBA/2abddc9bf012404bb3d10ffc36ba2593/ResultsDirectory',
    #  'Surface Burn Fraction': None,
    #  'Surface Flame Length': '/tmp/processing_rGXZBA/2abddc9bf012404bb3d10ffc36ba2593/ResultsDirectory/SurfaceFlameLength/SurfaceFlameLength2.asc'}
    assert isinstance(simulation, dict), "Simulation is not a dictionary"
    assert Path(simulation["InstanceDirectory"]).is_dir(), "Instance directory does not exist"
    assert Path(simulation["ResultsDirectory"]).is_dir(), "Results directory does not exist"
    assert Path(simulation["LogFile"]).is_file(), "Log file does not exist"
    assert Path(simulation["Ignition Points"]).is_file(), "Final fire scar file does not exist"

    # bundle
    alg = "fire2a:simulationresultsprocessing"
    params = {
        "BaseLayer": fuels,
        "EnablePropagationDiGraph": True,
        "EnablePropagationScars": True,
        "OutputDirectory": "TEMPORARY_OUTPUT",
        "ResultsDirectory": simulation["ResultsDirectory"],
    }

    bundle = processing.run(alg, params)
    # In [5]: bundle
    # Out[5]:
    # {'BurnProbability': '/tmp/processing_lxYJnx/98ad30b4b76f44d395637182563f64f4/BurnProbability.tif',
    #  'Byram Surface Intensity': '/tmp/processing_lxYJnx/4565fd22b4c84b07ac9c0ac184ed7360/OutputRaster.tif',
    #  'Byram Surface IntensityStats': '/tmp/processing_lxYJnx/303dc391b3824e41aaf2e81bbbbece73/OutputRasterStats.tif',
    #  'Hit Rate Of Spread': '/tmp/processing_lxYJnx/ad1ccb7b9d1648eda9458c8351a6a47a/OutputRaster.tif',
    #  'Hit Rate Of SpreadStats': '/tmp/processing_lxYJnx/94f73198b1734bb2a9de62b8890dbfbd/OutputRasterStats.tif',
    #  'IgnitionPoints': 'Output_ignition_point_s__layer_427a60cb_ac0a_44db_aa87_d5b5ece9385d',
    #  'OutputDirectory': PosixPath('/tmp/processing_lxYJnx/1313c4db4eb548158dc0c2cf2d04bf1e/OutputDirectory'),
    #  'PropagationDirectedGraph': 'Output_propagation_digraph_layer_7894b205_d022_4dc4_a26c_d8bbd2c8d220',
    #  'ScarPolygon': 'Output_propagation_scars_polygons_521f28e4_ac37_45fa_991c_1ee8471b1a02',
    #  'ScarRaster': '/tmp/processing_lxYJnx/858f8de25c0e4739a4df4ff4931ccc9d/ScarRaster.tif',
    #  'Surface Flame Length': '/tmp/processing_lxYJnx/e0faac0dc5d14eccb79508483725cdcb/OutputRaster.tif',
    #  'Surface Flame LengthStats': '/tmp/processing_lxYJnx/5409f02e62e148e989b662ef41b987dc/OutputRasterStats.tif'}

    for k, v in bundle.items():
        if k in ["IgnitionPoints", "PropagationDirectedGraph", "ScarPolygon"]:
            continue
        if k == "OutputDirectory":
            # assert v.is_dir(), f"Output directory {v} does not exist"
            # FIXME : non of the results go inside nor is created ?
            continue
        assert Path(v).is_file(), f"Bundle file {k} does not exist: {v}"

    # FIXME
    # from qgis.core import QgsMapLayer, QgsVectorLayer

    # ip = QgsVectorLayer(bundle["IgnitionPoints"], "Ignition Points", "memory")
    # sp = QgsVectorLayer(bundle["ScarPolygon"], "Scar Polygon", "memory")
    # pdg = QgsVectorLayer(
    #     bundle["PropagationDirectedGraph"], "Propagation DiGraph", "memory"
    # )

    # assert ip.isValid(), "Ignition Points layer is not valid"
    # assert sp.isValid(), "Scar Polygon layer is not valid"
    # assert pdg.isValid(), "Propagation DiGraph layer is not valid"

    # FIXME
    # /home/fdo/source/fire/lib/src/fire2a/cell2fire.py:670: RuntimeWarning: invalid value encountered in sqrt
    #   stddev = np_sqrt(sumsquared / N - (summed / N) ** 2)
