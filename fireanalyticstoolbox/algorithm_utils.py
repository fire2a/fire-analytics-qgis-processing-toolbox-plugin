#!python3

from tempfile import NamedTemporaryFile

from qgis.core import (Qgis, QgsColorRampShader, QgsMessageLog, QgsPalettedRasterRenderer,
                       QgsProcessingLayerPostProcessorInterface)
from qgis.PyQt.QtGui import QColor

from .config import TAG


def write_log(feedback, name="", file_name=None):
    if not file_name:
        file_name = NamedTemporaryFile(prefix=f"algorithm_{name}_log_", suffix=".html", delete=False).name
    feedback.pushInfo(f"this output is written to: {file_name}")
    with open(file_name, "w") as f:
        f.write(feedback.htmlLog())
    QgsMessageLog.logMessage("file://" + file_name, tag=TAG, level=Qgis.Info)


def run_alg_styler_bin(display_name, color0=(2, 2, 2), color1=(222, 222, 222), layer_bands=1):
    """Create a New Post Processor class and returns it"""

    class LayerPostProcessor(QgsProcessingLayerPostProcessorInterface):
        instance = None
        name = display_name
        bands = layer_bands

        lst = [
            QgsColorRampShader.ColorRampItem(0, QColor(*color0)),
            QgsColorRampShader.ColorRampItem(1, QColor(*color1)),
        ]
        class_data = QgsPalettedRasterRenderer.colorTableToClassData(lst)  # <-

        def postProcessLayer(self, layer, context, feedback):
            feedback.pushInfo(f"Inside postProcessLayer: {self.name}")
            if layer.isValid():
                prov = layer.dataProvider()
                layer.setName(self.name)
                feedback.pushInfo(f"Layer valid, set name: {self.name}")
                for band in range(1, self.bands + 1):
                    renderer = QgsPalettedRasterRenderer(prov, band, self.class_data)
                    layer.setRenderer(renderer)
            else:
                feedback.pushInfo(f"Layer not valid: {self.name}")

        # Hack to work around sip bug!
        @staticmethod
        def create() -> "LayerPostProcessor":
            LayerPostProcessor.instance = LayerPostProcessor()
            return LayerPostProcessor.instance

    return LayerPostProcessor.create()
