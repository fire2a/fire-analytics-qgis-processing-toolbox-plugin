#!/bin/env python3
"""
see https://github.com/fdobad/qgis-easy-dependencies-plugin/blob/main/README.md
"""
from configparser import ConfigParser
from distutils.version import LooseVersion
from importlib import import_module, reload
from importlib.metadata import PackageNotFoundError, distribution
from pathlib import Path
from re import match as re_match
from subprocess import run as subprocess_run
from platform import system as platform_system

from qgis.core import Qgis, QgsMessageLog
from qgis.PyQt.QtWidgets import QCheckBox, QMessageBox


def run():
    # get the plugin name from metadata.txt
    cp = ConfigParser()
    cp.read(Path(__file__).parent / "metadata.txt")
    plugin_name = cp.get("general", "name")

    # SWITCH COMENT IN PRODUCTION
    # config_file = Path().cwd() / "dependencies_handler.txt"
    config_file = Path(__file__).parent / "dependencies_handler.txt"
    if not config_file.is_file():
        QgsMessageLog().logMessage(
            f"Plugin {plugin_name}: dependencies_handler.txt not found! (create this file to enable checking)",
            tag="Plugins",
            level=Qgis.Critical,
        )
        return
    config = ConfigParser()
    config.read(config_file)

    if config.get("general", "enabled", fallback="True") == "False":
        QgsMessageLog().logMessage(
            f"Plugin {plugin_name}: checking & installing dependencies is disabled (to enable edit {config_file})",
            tag="Plugins",
            level=Qgis.Warning,
        )
        return
    requirement = config.get("general", "plugin_dependencies", fallback="")

    match = re_match(r"(.*?)([=<>!]{1,2})([\d.]+)", requirement)
    if match:
        req_pkg_name = match.group(1)
        req_operator = match.group(2)
        req_version = match.group(3)

    try:
        found_version = distribution(req_pkg_name).version
        if LooseVersion(req_version) != LooseVersion(found_version):
            msg = "version mismatch, found: " + found_version
        else:
            QgsMessageLog().logMessage(
                f"Plugin {plugin_name}: {requirement} satisfied!", tag="Plugins", level=Qgis.Success
            )
            return

    except PackageNotFoundError:
        msg = "is not installed"

    response = QMessageBox.question(
        None,
        f"Plugin '{plugin_name}'",
        f"Allow automatic pip install of {requirement}?\n\n"
        f"Because: {msg}\n\n"
        + "Probably need to restart QGIS afterwards (if the plugin gets hidden or toggling the checkbox from plugin manager's installed list doesn't make it available)",
        QMessageBox.Yes | QMessageBox.No,
        QMessageBox.No,
    )
    if response == QMessageBox.Yes:
        if platform_system() == "Darwin":
            cwd = sys.prefix
            right_here = "./"
            QgsMessageLog().logMessage(f"Plugin {plugin_name}: Using Python in {cwd}", tag="Plugins", level=Qgis.Success)
        else:
            cwd = None
            right_here = ""
        result = subprocess_run([right_here+"python3", "-m", "pip", "install", requirement], capture_output=True, text=True, cwd=cwd)
        if result.returncode == 0:
            msg = [f"pip install {requirement} success!"]
            QgsMessageLog().logMessage(f"Plugin {plugin_name}: {msg[-1]}", tag="Plugins", level=Qgis.Success)
            QgsMessageLog().logMessage(
                f"Plugin {plugin_name}: pip log\n" + result.stdout, tag="Plugins", level=Qgis.Warning
            )
            ok = False
            try:
                for module_name in get_module_names(req_pkg_name):
                    module = import_module(module_name)
                    reload(module)
                    msg += [f"reload {module_name} success!"]
                    QgsMessageLog().logMessage(f"Plugin {plugin_name}: {msg[-1]}", tag="Plugins", level=Qgis.Success)
                    ok = True
            except Exception:
                msg += [f"reloading {req_pkg_name} packages failed!"]
                QgsMessageLog().logMessage(f"Plugin {plugin_name}: {msg[-1]}", tag="Plugins", level=Qgis.Critical)
                ok = False
            msg = "\n".join(msg)
            if ok:
                QMessageBox.information(None, f"Plugin '{plugin_name}'", f"{plugin_name}:\n{msg}")
            else:
                QMessageBox.warning(None, f"Plugin '{plugin_name}'", f"{plugin_name}:\n{msg}")
            return
        msg = f"pip install {requirement} failed!\nerror: " + result.stderr
        QgsMessageLog().logMessage(f"Plugin {plugin_name}: {msg}", tag="Plugins", level=Qgis.Critical)
        QMessageBox.critical(None, f"Plugin '{plugin_name}'", f"{plugin_name}:\n{msg}")
    elif response == QMessageBox.No:
        QgsMessageLog().logMessage(f"{plugin_name}: User declined installation!", tag="Plugins", level=Qgis.Warning)

        qmb = QMessageBox(
            QMessageBox.Warning,
            f"Plugin '{plugin_name}'",
            f"{plugin_name}: User declined installation! Please resolve manually in QGIS Python Console, typing:\n\n\t!pip install {requirement}\n",
        )
        qcb = QCheckBox("Do not attempt to check and install dependencies again!")
        qmb.setCheckBox(qcb)
        qmb.exec_()
        if qcb.isChecked():
            config.set("general", "enabled", "False")
            with open(config_file, "w") as f:
                config.write(f)
            QgsMessageLog().logMessage(
                f"Plugin {plugin_name}: User disabled installation!", tag="Plugins", level=Qgis.Warning
            )
        else:
            QgsMessageLog().logMessage(
                f"{plugin_name}: checking & installing dependencies normal exit", tag="Plugins", level=Qgis.Info
            )


def get_module_names(distribution_name="your-package-name"):
    try:
        dist_info = distribution(distribution_name)
        unique_parents = set()

        for file in dist_info.files:
            path = Path(str(file))
            if name := path.parent.name:
                if name != "__pycache__" and name.find(".") == -1:
                    unique_parents.add(path.parent.name)

        return unique_parents

    except PackageNotFoundError as e:
        QgsMessageLog().logMessage(
            f"Plugin:{plugin_name}: {e} attempting to get module names", tag="Plugins", level=Qgis.Critical
        )
        return []
