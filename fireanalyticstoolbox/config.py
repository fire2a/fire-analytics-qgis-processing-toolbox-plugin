#!python3
def jolo(string: str) -> str:
    return string.replace(" ", "").lower()

STATS = [
    {"name": "Hit Rate Of Spread", "dir": "RateOfSpread", "file": "ROSFile", "arg": "out-ros"},
    {"name": "Flame Length", "dir": "FlameLength", "file": "FL", "arg": "out-fl"},
    {"name": "Byram Intensity", "dir": "Intensity", "file": "Intensity", "arg": "out-intensity"},
    {"name": "Crown Fire Scar", "dir": "CrownFire", "file": "Crown", "arg": "out-crown"},
    {"name": "Crown Fire Fuel Consumption Ratio", "dir": "CrownFractionBurn", "file": "Cfb", "arg": "out-cfb"},
]
# NO CAMBIAR DE ORDEN
# check algorithm_simulatior.py > FireSimulatorAlgorithm > postProcessing
SIM_OUTPUTS = [
    {"name": "Final Fire Scar", "dir": "Grids/Grids", "file": "ForestGrid", "arg": "final-grid"},
    {"name": "Propagation Fire Scars", "dir": "Grids/Grids", "file": "ForestGrid", "arg": "grids"},
    {"name": "Propagation Directed Graph", "dir": "Messages", "file": "MessagesFile", "arg": "output-messages"},
]
SIM_OUTPUTS.extend(STATS)

METRICS = [
    "Burn Probability",
    "Betweenness Centrality",
    "Downstream Protection Value",
]
ALGO_NAME = {
    "IN_LOG":"Log File",
    "post_sim": "Simulator Post Processing",
    "messages": "Messages",
    "statistics": "Statistics",
    "ignition_points": "Ignition Points",
    "raster_knapsack": "Raster Knapsack",
    "clusterize": "Clusterize",
    "sandbox": "Sandbox",
    "simulator": "Simulator",
}
TAG = "fire2a"
