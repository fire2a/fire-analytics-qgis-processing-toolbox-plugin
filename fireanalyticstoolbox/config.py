#!python3
def jolo(string: str) -> str:
    return string.replace(" ", "").lower()


TAG = "fire2a"
STATS = [
    {"name": "Hit Rate Of Spread", "dir": "RateOfSpread", "file": "ROSFile", "arg": "out-ros", "unit": "m/min", "ext":"asc"},
    {"name": "Flame Length", "dir": "FlameLength", "file": "FL", "arg": "out-fl", "unit": "m", "ext":"asc"},
    {"name": "Byram Intensity", "dir": "Intensity", "file": "Intensity", "arg": "out-intensity", "unit": "kW/m", "ext":"asc"},
    {"name": "Crown Fire Scar", "dir": "CrownFire", "file": "Crown", "arg": "out-crown", "unit": "bool", "ext":"asc"},
    {
        "name": "Crown Fire Fuel Consumption Ratio",
        "dir": "CrownFractionBurn",
        "file": "Cfb",
        "arg": "out-cfb",
        "unit": "ratio",
        "ext":"asc",
    },
]
# NO CAMBIAR DE ORDEN
# check algorithm_simulatior.py > FireSimulatorAlgorithm > postProcessing
SIM_OUTPUTS = [
    {"name": "Final Fire Scar", "dir": "Grids/Grids", "file": "ForestGrid", "arg": "final-grid", "unit": "bool"},
    {"name": "Propagation Fire Scars", "dir": "Grids/Grids", "file": "ForestGrid", "arg": "grids", "unit": "bool"},
    {
        "name": "Propagation Directed Graph",
        "dir": "Messages",
        "file": "MessagesFile",
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
