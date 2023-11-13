#!python3
from os import sep
def jolo(string: str) -> str:
    return string.replace(" ", "").lower()


TAG = "fire2a"
STATS = [
    {
        "name": "Hit Rate Of Spread",
        "dir": "RateOfSpread",
        "file": "ROSFile",
        "ext": "asc",
        "arg": "out-ros",
        "unit": "m/min",
        "dtype": "float32",
    },
    {
        "name": "Flame Length",
        "dir": "FlameLength",
        "file": "FL",
        "ext": "asc",
        "arg": "out-fl",
        "unit": "m",
        "dtype": "float32",
    },
    {
        "name": "Byram Intensity",
        "dir": "Intensity",
        "file": "Intensity",
        "ext": "asc",
        "arg": "out-intensity",
        "unit": "kW/m",
        "dtype": "float32",
    },
    {
        "name": "Crown Fire Scar",
        "dir": "CrownFire",
        "file": "Crown",
        "ext": "asc",
        "arg": "out-crown",
        "unit": "bool",
        "dtype": "int16",
    },
    {
        "name": "Crown Fire Fuel Consumption Ratio",
        "dir": "CrownFractionBurn",
        "file": "Cfb",
        "ext": "asc",
        "arg": "out-cfb",
        "unit": "ratio",
        "dtype": "float32",
    },
]
# NO CAMBIAR DE ORDEN
# check algorithm_simulatior.py > FireSimulatorAlgorithm > postProcessing
SIM_OUTPUTS = [
    {
        "name": "Final Fire Scar",
        "dir": "Grids"+sep+"Grids",
        "file": "ForestGrid",
        "ext": "csv",
        "arg": "final-grid",
        "unit": "bool",
    },
    {
        "name": "Propagation Fire Scars",
        "dir": "Grids"+sep+"Grids",
        "file": "ForestGrid",
        "ext": "csv",
        "arg": "grids",
        "unit": "bool",
    },
    {
        "name": "Propagation Directed Graph",
        "dir": "Messages",
        "file": "MessagesFile",
        "ext": "csv",
        "arg": "output-messages",
        "unit": "simtime",
    },
]
SIM_OUTPUTS.extend(STATS)

METRICS = [
    "Burn Probability",
    "Betweenness Centrality",
    "Downstream Protection Value",
]
simpp = "Simulator Post Processing"
simm = "Simulator Risk Metrics"
NAME = {
    "simpp": simpp,
    "simm": simm,
    "layer_group": simpp + " Group",
    "bc": "Betweenness Centrality Propagation Metric",
    "dpv": "Downstream Protection Value Propagation Metric",
    # "IN_LOG": "Log File",
    # "post_sim": "Simulator Post Processing",
    # "messages": "Messages",
    # "statistics": "Statistics",
    # "ignition_points": "Ignition Points",
    # "raster_knapsack": "Raster Knapsack",
    # "clusterize": "Clusterize",
    # "sandbox": "Sandbox",
    # "simulator": "Simulator",
}
