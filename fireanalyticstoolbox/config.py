#!python3
from os import sep
from pathlib import Path

from qgis.PyQt.QtCore import QCoreApplication, QSettings, QTranslator  # type: ignore

TAG = "fire2a"


def jolo(string: str) -> str:
    return string.replace(" ", "").lower()


class aConfig:
    """Object to install the translator and provide base names centralized for all the plugin (mostly simulator and post processing)"""

    def tr(self, string: str, context="aConfig") -> str:
        return QCoreApplication.translate(context, string)

    def __init__(self):
        locale = QSettings().value("locale/userLocale")[0:2]
        locale_path = Path(__file__).parent / "i18n" / f"{locale}.qm"

        if locale_path.is_file():
            translator = QTranslator()
            translator.load(str(locale_path))
            QCoreApplication.installTranslator(translator)

        self.SIM_INPUTS = {
            "fuels": {"units": "categorical", "description": self.tr("Fuel")},
            "elevation": {"units": "m", "description": self.tr("Elevation")},
            "cbh": {"units": "m", "description": "\ncbh: " + self.tr("Canopy Base Height")},
            "cbd": {"units": "kg/m3", "description": "cbd: " + self.tr("Canopy Bulk Density")},
            "ccf": {"units": "0,1", "description": "ccf: " + self.tr("Canopy Cover Fraction")},
            "hm": {"units": "m", "description": "hm: " + self.tr("Canopy Height")},
            "py": {
                "units": "0,1",
                "description": self.tr("Probability map") + self.tr(" (requires generation mode 1)"),
            },
        }

        self.STATS = [
            {
                "name": self.tr("Hit Rate Of Spread"),
                "dir": "RateOfSpread",
                "file": "ROSFile",
                "ext": "asc",
                "arg": "out-ros",
                "unit": "m/min",
                "dtype": "float32",
            },
            {
                "name": self.tr("Surface Flame Length"),
                "dir": "SurfaceFlameLength",
                "file": "SurfaceFlameLength",
                "ext": "asc",
                "arg": "out-fl",
                "unit": "m",
                "dtype": "float32",
            },
            {
                "name": self.tr("Byram Surface Intensity"),
                "dir": "SurfaceIntensity",
                "file": "SurfaceIntensity",
                "ext": "asc",
                "arg": "out-intensity",
                "unit": "kW/m",
                "dtype": "float32",
            },
            {
                "name": self.tr("Crown Fire Scar"),
                "dir": "CrownFire",
                "file": "Crown",
                "ext": "asc",
                "arg": "out-crown",
                "unit": "bool",
                "dtype": "int16",
            },
            {
                "name": self.tr("Crown Fire Fuel Consumption Ratio"),
                "dir": "CrownFractionBurn",
                "file": "Cfb",
                "ext": "asc",
                "arg": "out-cfb",
                "unit": "ratio",
                "dtype": "float32",
            },
            {
                "name": self.tr("Surface Burn Fraction"),
                "suffix": self.tr(" (only Canada FBP)"),
                "dir": "SurfFractionBurn",
                "file": "Sfb",
                "ext": "asc",
                "arg": "out-sfb",
                "unit": "ton",
                "dtype": "float32",
            },
            {
                "name": self.tr("Crown Intensity"),
                "suffix": self.tr(" (only Spain S&B)"),
                "dir": "CrownIntensity",
                "file": "CrownIntensity",
                "ext": "asc",
                "arg": "out-intensity",
                "unit": "kW/m",
                "dtype": "float32",
            },
            {
                "name": self.tr("Crown Flame Length"),
                "suffix": self.tr(" (only Spain S&B)"),
                "dir": "CrownFlameLength",
                "file": "CrownFlameLength",
                "ext": "asc",
                "arg": "out-fl",
                "unit": "m",
                "dtype": "float32",
            },
            {
                "name": self.tr("Max Flame Length"),
                "suffix": self.tr(" (only Spain S&B)"),
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
        self.SIM_OUTPUTS = [
            {
                "name": self.tr("Final Fire Scar"),
                "dir": "Grids" + sep + "Grids",
                "file": "ForestGrid",
                "ext": "csv",
                "arg": "final-grid",
                "unit": "bool",
            },
            {
                "name": self.tr("Propagation Fire Scars"),
                "dir": "Grids" + sep + "Grids",
                "file": "ForestGrid",
                "ext": "csv",
                "arg": "grids",
                "unit": "bool",
            },
            {
                "name": self.tr("Propagation Directed Graph"),
                "dir": "Messages",
                "file": "MessagesFile",
                "ext": "csv",
                "arg": "output-messages",
                "unit": "simtime",
            },
            {
                "name": self.tr("Ignition Points"),
                "dir": "IgnitionsHistory",
                "file": "ignitions_log",
                "ext": "csv",
                "arg": "ignitionsLog",
                "unit": "cell_id",
            },
        ]
        self.SIM_OUTPUTS.extend(self.STATS)

        METRICS = {
            "bp": self.tr("Burn Probability"),
            "bc": self.tr("Betweenness Centrality"),
            "dpv": self.tr("Downstream Protection Value"),
        }
        simpp = self.tr("Simulator Post Processing")
        simm = self.tr("Simulator Risk Metrics")
        self.NAME = {
            "simpp": simpp,
            "simm": simm,
            "layer_group": simpp + " Group",
            "bc": METRICS["bc"] + self.tr(" Propagation Metric"),
            "dpv": METRICS["dpv"] + self.tr(" Propagation Metric"),
            "bp": METRICS["bp"] + self.tr(" Propagation Metric"),
            "fuel_models": ["0. Scott & Burgan", "1. Kitral", "2. Canadian Forest Fire Behavior Prediction System"],
            "fuel_tables": ["spain_lookup_table.csv", "kitral_lookup_table.csv", "fbp_lookup_table.csv"],
            "ignition_modes": [
                self.tr("0. Uniformly distributed random ignition point(s)"),
                self.tr("1. Probability map distributed random ignition point(s)"),
                self.tr("2. Single point on a (Vector)Layer"),
            ],
            "weather_modes": [
                self.tr("0. Single weather file scenario"),
                self.tr("1. Random draw from multiple weathers in a directory"),
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
