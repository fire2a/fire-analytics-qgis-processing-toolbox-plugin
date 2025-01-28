#!python3
"""
1. Enables a python script to run the QGIS environment,
without launching the QGIS GUI.
2. Enables a user located processing plugin to be loaded

Programmers must:
1. Adjust the path to the QGIS installation 
(on windows also adjust qgis versions)

2. load the QGIS python environment to run

Helpful commands:
call "%USERPROFILE%\source\pyenv\python-qgis-cmd.bat"
%autoindent
ipython

References:
https://fire2a.github.io/docs/qgis-cookbook
https://gis.stackexchange.com/a/408738
https://gis.stackexchange.com/a/172849
"""
import sys
from platform import system as platform_system
from shutil import which
from os import pathsep, environ

from qgis.core import QgsApplication, QgsRasterLayer
#
## PART 1
#

if platform_system() == 'Windows':
    QgsApplication.setPrefixPath("C:\\PROGRA~1\\QGIS33~1.1", True)
else:
    QgsApplication.setPrefixPath("/usr", True)
qgs = QgsApplication([], False)
qgs.initQgis()

# Append the path where processing plugin can be found
if platform_system() == 'Windows':
    sys.path.append('C:\\PROGRA~1\\QGIS33~1.1\\apps\\qgis\\python\\plugins')
else:
    sys.path.append("/usr/share/qgis/python/plugins")

import processing
from processing.core.Processing import Processing

Processing.initialize()

#
## PART 2
#

# Append the path where your processing plugin is
if platform_system() == 'Windows':
    sys.path.append("C:\\Users\\FernandoBadilla\\AppData\\Roaming\\QGIS\\QGIS3\\profiles\\default\\python\\plugins")
else:
    sys.path.append("/home/fdo/.local/share/QGIS/QGIS3/profiles/default/python/plugins/")
# Add the algorithm provider
from fireanalyticstoolbox.fireanalyticstoolbox_provider import FireToolboxProvider

provider = FireToolboxProvider()
QgsApplication.processingRegistry().addProvider(provider)

#
## PART 3 - Run your algorithm
#
print(processing.algorithmHelp("fire2am:rasterknapsackoptimization"))

### add cbc solver to path
extension = '.exe' if platform_system() == 'Windows' else ''
if which('cbc'+extension) is None:
    # CHANGE THIS
    cbc_executable = Path('cbc','bin','cbc'+extension)
    if cbc_executable.is_file():
        environ["PATH"] += pathsep + str(cbc_executable.parent)
# check
if which('cbc'+extension) is None:
    print('cbc not found! exiting')
    sys.exit(0)

# CHOOSE
# Value and Weight input
#   Accepted data types:
#   - QgsRasterLayer
# value = iface.activeLayer()
value = QgsRasterLayer('raster.asc','raster_name')
#   - str: layer ID
value = value.id()
#   - str: layer name
value = value.name()
#   - str: layer source
# value =  "/path/to/raster.any_supported_extension"
value = layer.publicSource()
#   - QgsProperty ? TODO

result = processing.run(
    "fire2am:rasterknapsackoptimization",
    {
        "INPUT_ratio": 0.06,
        "INPUT_value": value,
        "INPUT_weight": None,
        "OUTPUT_csv": "TEMPORARY_OUTPUT",
        "OUTPUT_layer": "TEMPORARY_OUTPUT",
        "SOLVER": "cbc: ratioGap=0.001 seconds=300",
        "CUSTOM_OPTIONS_STRING": "",
    },
)
print(result)
