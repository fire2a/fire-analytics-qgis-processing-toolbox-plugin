#!QGIS python console
"""
This script must run at QGIS python console,
notice how QgsProject and iface are used but never imported

Uses the "Fire2a:Raster Knapsack Optimization" as an example
"""
from qgis import processing
result = processing.run(
    "Fire2a:Raster Knapsack Optimization",
    {
        "INPUT_ratio": 0.06,
        "INPUT_value": iface.activeLayer(),
        "INPUT_weight": None,
        "OUTPUT_csv": "TEMPORARY_OUTPUT",
        "OUTPUT_layer": "TEMPORARY_OUTPUT",
        "SOLVER": "cbc: ratioGap=0.001 seconds=300",
        "CUSTOM_OPTIONS_STRING": "",
    },
)
QgsProject.instance().addMapLayer(result['OUTPUT_layer'])
