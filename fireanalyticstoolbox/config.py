#!python3
from os import sep


def jolo(string: str) -> str:
    return string.replace(" ", "").lower()


TAG = "fire2a"

SIM_INPUTS = {
    "fuels": {"units": "categorical", "description": "Fuel"},
    "elevation": {"units": "m", "description": "Elevation"},
    "cbh": {"units": "m", "description": "\ncbh: Canopy Base Height"},
    "cbd": {"units": "kg/m3", "description": "cbd: Canopy Bulk Density"},
    "ccf": {"units": "0,1", "description": "ccf: Canopy Cover Fraction"},
    "hm": {"units": "m", "description": "hm: Canopy Height"},
    "py": {"units": "0,1", "description": "Probability map (requires generation mode 1)"},
}

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
        "name": "Surface Flame Length",
        "dir": "SurfaceFlameLength",
        "file": "SurfaceFlameLength",
        "ext": "asc",
        "arg": "out-fl",
        "unit": "m",
        "dtype": "float32",
    },
    {
        "name": "Byram Surface Intensity",
        "dir": "SurfaceIntensity",
        "file": "SurfaceIntensity",
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
    {
        "name": "Surface Burn Fraction",
        "suffix": " (only Canada FBP)",
        "dir": "SurfFractionBurn",
        "file": "Sfb",
        "ext": "asc",
        "arg": "out-sfb",
        "unit": "ton",
        "dtype": "float32",
    },
    {
        "name": "Crown Intensity",
        "suffix": " (only Spain S&B)",
        "dir": "CrownIntensity",
        "file": "CrownIntensity",
        "ext": "asc",
        "arg": "out-intensity",
        "unit": "kW/m",
        "dtype": "float32",
    },
    {
        "name": "Crown Flame Length",
        "suffix": " (only Spain S&B)",
        "dir": "CrownFlameLength",
        "file": "CrownFlameLength",
        "ext": "asc",
        "arg": "out-fl",
        "unit": "m",
        "dtype": "float32",
    },
    {
        "name": "Max Flame Length",
        "suffix": " (only Spain S&B)",
        "dir": "MaxFlameLength",
        "file": "MaxFlameLength",
        "ext": "asc",
        "arg": "out-fl",
        "unit": "m",
        "dtype": "float32",
    },
]
# NO CAMBIAR DE ORDEN
# check algorithm_simulatior.py > FireSimulatorAlgorithm > postProcessing
SIM_OUTPUTS = [
    {
        "name": "Final Fire Scar",
        "dir": "Grids" + sep + "Grids",
        "file": "ForestGrid",
        "ext": "csv",
        "arg": "final-grid",
        "unit": "bool",
    },
    {
        "name": "Propagation Fire Scars",
        "dir": "Grids" + sep + "Grids",
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
    {
        "name": "Ignition Points",
        "dir": "IgnitionsHistory",
        "file": "ignitions_log",
        "ext": "csv",
        "arg": "ignitionsLog",
        "unit": "cell_id",
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
    "bp": "Burn Probability Propagation Metric",
    "fuel_models": ["0. Scott & Burgan", "1. Kitral", "2. Canadian Forest Fire Behavior Prediction System"],
    "fuel_tables": ["spain_lookup_table.csv", "kitral_lookup_table.csv", "fbp_lookup_table.csv"],
    "ignition_modes": [
        "0. Uniformly distributed random ignition point(s)",
        "1. Probability map distributed random ignition point(s)",
        "2. Single point on a (Vector)Layer",
    ],
    "weather_modes": [
        "0. Single weather file scenario",
        "1. Random draw from multiple weathers in a directory",
        # "2. Sequential draw from multiple weathers in a directory",
    ],
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
