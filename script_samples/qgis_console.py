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


"""
This code performs 37 deterministic simulations from specific weather files. Then, each one is plot
in the qgis interface as a directed graph. 
"""
import os
fuels = '/home/rodrigo/code/fire2am-kitral/C2F/data/Portezuelo/fuels.asc'

for i in range(1,37): 
    simulation = processing.run(
        "fire2a:cell2firesimulator", 
        { 'CbdRaster' : None, 
        'CbhRaster' : None, 
        'CcfRaster' : None, 
        'ElevationRaster' : '/home/rodrigo/code/fire2am-kitral/C2F/data/Portezuelo/elevation.asc', 
        'EnableCrownFire' : False, 
        'FoliarMoistureContent' : 66,
        'FuelModel' : 1, 
        'FuelRaster' : fuels, 
        'IgnitionMode' : 2, 
        'IgnitionPointVectorLayer' : '/home/rodrigo/code/fire2am-kitral/C2F/data/Portezuelo/ignition.shp', 
        'IgnitionProbabilityMap' : None, 
        'IgnitionRadius' : 0, 
        'InstanceDirectory' : "TEMPORARY_OUTPUT", 
        'InstanceInProject' : True, 
        'LiveAndDeadFuelMoistureContentScenario' : 2,
        'NumberOfSimulations' : 1, 
        'OutputOptions' : [0,2], 
        'PvRaster' : None, 
        'RandomNumberGeneratorSeed' : 123, 
        'ResultsDirectory' : "TEMPORARY_OUTPUT", 
        'ResultsInInstance' : True, 
        'SimulationThreads' : 7, 
        'WeatherDirectory' : '', 
        'WeatherFile' : f'/home/rodrigo/code/jupyter_notebooks/Weathers/Weather{i}.csv', 
        'WeatherMode' : 0 },) 

    digraph = processing.run(
        "fire2a:propagationdigraph",
        { 'BaseLayer' : fuels, 
        'PropagationDirectedGraph' : "TEMPORARY_OUTPUT", 
        'SampleMessagesFile' : simulation.get('Propagation Directed Graph') })
    
    QgsProject.instance().addMapLayer(digraph['PropagationDirectedGraph'])


