#!python3

from pathlib import Path
from tempfile import NamedTemporaryFile

from qgis.core import Qgis, QgsMessageLog

from .config import TAG


def write_log(feedback, name="", file_name=None):
    if not file_name:
        file_name = Path(NamedTemporaryFile(prefix=f"algorithm_{name}_log_", suffix=".html", delete=False).name)
    feedback.pushInfo(f"this output is written to: {file_name}")
    with open(file_name, "w") as f:
        f.write(feedback.htmlLog())
    QgsMessageLog.logMessage(name + " " + file_name.as_uri(), tag=TAG, level=Qgis.Info)
