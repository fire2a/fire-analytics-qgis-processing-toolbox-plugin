#!python3
import os
from pathlib import Path
from tempfile import NamedTemporaryFile

import numpy as np
from processing.algs.gdal.GdalUtils import GdalUtils
from qgis.core import (Qgis, QgsColorRampShader, QgsMessageLog, QgsPalettedRasterRenderer, QgsProcessingFeedback,
                       QgsProcessingLayerPostProcessorInterface, QgsProcessingParameterRasterDestination,
                       QgsRasterBlock, QgsRasterFileWriter, QgsRasterShader, QgsSingleBandPseudoColorRenderer)
from qgis.PyQt.QtCore import QByteArray
from qgis.PyQt.QtGui import QColor

from .config import TAG


def get_vector_driver_from_filename(filename):
    return GdalUtils.getVectorDriverFromFileName(filename)


def get_output_raster_format(filename: str, feedback: QgsProcessingFeedback = None):
    """Gets a valid GDAL output raster driver name, warns if not found, defaults to GTiff.

    Args:
        filename (str): The name with extension of the raster. (Not implemented for suffixes with multiple dots, e.g. mpv.gz)
        feedback (QgsProcessingFeedback): The feedback object to push warnings to.

    Returns:
        str: The GDAL short format name for extension.

    Sample usage:
        driver_name = get_output_raster_format(filename, feedback)
        dst_ds = gdal.GetDriverByName(raster_format).Create(filename, W, H, 1, GDT_Float32)

    Based/copied from qgis.python.grassprovider.grass_utils.py GrassUtils
    """
    ext = os.path.splitext(filename)[1].lower()
    ext = ext.lstrip(".")
    if ext:
        supported = GdalUtils.getSupportedOutputRasters()
        for name in list(supported.keys()):
            exts = supported[name]
            if ext in exts:
                return name
    if feedback:
        feedback.pushWarning(f"Using GTiff format! No supported GDAL raster format from {filename=} {ext=} found.")
    return "GTiff"


def check_gdal_readable_raster(filename):
    """Based/copied from qgis.python.grassprovider.grass_utils.py GrassUtils"""
    ext = os.path.splitext(filename)[1].lower()
    ext = ext.lstrip(".")
    if ext:
        supported = GdalUtils.getSupportedRasters()
        for name in list(supported.keys()):
            exts = supported[name]
            if ext in exts:
                return True
    return False


def array2rasterInt16(data, name, geopackage, extent, crs, nodata=None):
    """numpy array to gpkg casts to name"""
    data = np.int16(data)
    h, w = data.shape
    bites = QByteArray(data.tobytes())
    block = QgsRasterBlock(Qgis.CInt16, w, h)
    block.setData(bites)
    fw = QgsRasterFileWriter(str(geopackage))
    fw.setOutputFormat("gpkg")
    fw.setCreateOptions(["RASTER_TABLE=" + name, "APPEND_SUBDATASET=YES"])
    provider = fw.createOneBandRaster(Qgis.Int16, w, h, extent, crs)
    provider.setEditable(True)
    if nodata != None:
        provider.setNoDataValue(1, nodata)
    provider.writeBlock(block, 1, 0, 0)
    provider.setEditable(False)


def get_raster_data(layer):
    """raster layer into numpy array
        slower alternative:
            for i in range(lyr.width()):
                for j in range(lyr.height()):
                    values.append(block.value(i,j))
    # npArr = np.frombuffer( qByteArray)  #,dtype=float)
    # return npArr.reshape( (layer.height(),layer.width()))
    """
    if layer:
        provider = layer.dataProvider()
        if numpy_dtype := qgis2numpy_dtype(provider.dataType(1)):
            block = provider.block(1, layer.extent(), layer.width(), layer.height())
            qByteArray = block.data()
            return np.frombuffer(qByteArray, dtype=numpy_dtype)


def get_raster_info(layer):
    if layer:
        return {
            "width": layer.width(),
            "height": layer.height(),
            "extent": layer.extent(),
            "crs": layer.crs(),
            "cellsize_x": layer.rasterUnitsPerPixelX(),
            "cellsize_y": layer.rasterUnitsPerPixelY(),
        }


def get_raster_nodata(layer, feedback):
    if layer:
        dp = layer.dataProvider()
        if dp.sourceHasNoDataValue(1):
            ndv = dp.sourceNoDataValue(1)
            feedback.pushInfo(f" nodata: {ndv}")
            return ndv


def qgis2numpy_dtype(qgis_dtype: Qgis.DataType) -> np.dtype:
    """Conver QGIS data type to corresponding numpy data type
    https://raw.githubusercontent.com/PUTvision/qgis-plugin-deepness/fbc99f02f7f065b2f6157da485bef589f611ea60/src/deepness/processing/processing_utils.py
    This is modified and extended copy of GDALDataType.

    * ``UnknownDataType``: Unknown or unspecified type
    * ``Byte``: Eight bit unsigned integer (quint8)
    * ``Int8``: Eight bit signed integer (qint8) (added in QGIS 3.30)
    * ``UInt16``: Sixteen bit unsigned integer (quint16)
    * ``Int16``: Sixteen bit signed integer (qint16)
    * ``UInt32``: Thirty two bit unsigned integer (quint32)
    * ``Int32``: Thirty two bit signed integer (qint32)
    * ``Float32``: Thirty two bit floating point (float)
    * ``Float64``: Sixty four bit floating point (double)
    * ``CInt16``: Complex Int16
    * ``CInt32``: Complex Int32
    * ``CFloat32``: Complex Float32
    * ``CFloat64``: Complex Float64
    * ``ARGB32``: Color, alpha, red, green, blue, 4 bytes the same as QImage.Format_ARGB32
    * ``ARGB32_Premultiplied``: Color, alpha, red, green, blue, 4 bytes  the same as QImage.Format_ARGB32_Premultiplied
    """
    if qgis_dtype == Qgis.DataType.Byte:
        return np.uint8
    if qgis_dtype == Qgis.DataType.UInt16:
        return np.uint16
    if qgis_dtype == Qgis.DataType.Int16:
        return np.int16
    if qgis_dtype == Qgis.DataType.Float32:
        return np.float32
    if qgis_dtype == Qgis.DataType.Float64:
        return np.float64


def run_alg_styler_bin(display_name, color0=(2, 2, 2), color1=(222, 222, 222), layer_bands=1):
    """Create a New Post Processor class and returns it"""

    class LayerPostProcessor(QgsProcessingLayerPostProcessorInterface):
        instance = None
        name = display_name
        bands = layer_bands
        color_zero = color0
        color_one = color1

        lst = [
            QgsColorRampShader.ColorRampItem(0, QColor(*color_zero)),
            QgsColorRampShader.ColorRampItem(1, QColor(*color_one)),
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


def write_log(feedback, name="", file_name=None):
    if not file_name:
        file_name = Path(NamedTemporaryFile(prefix=f"algorithm_{name}_log_", suffix=".html", delete=False).name)
    if not isinstance(file_name, Path):
        file_name = Path(file_name)
    feedback.pushInfo(f"this output is written to: {file_name}")
    with open(file_name, "w") as f:
        f.write(feedback.htmlLog())
    text_file_name = file_name.with_suffix(".txt")
    with open(text_file_name, "w") as f:
        f.write(feedback.textLog())
    QgsMessageLog.logMessage(name + " " + file_name.as_uri(), tag=TAG, level=Qgis.Info)


class QgsProcessingParameterRasterDestinationAIIGrid(QgsProcessingParameterRasterDestination):
    """overrides the defaultFileExtension method to gpkg
    ALTERNATIVE:
    from types import MethodType
    QPPRD = QgsProcessingParameterRasterDestination(self.OUTPUT_layer, self.tr("Output layer"))
    def _defaultFileExtension(self):
        return "asc"
    QPPRD.defaultFileExtension = MethodType(_defaultFileExtension, QPPRD)
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def defaultFileExtension(self):
        return "asc"


class QgsProcessingParameterRasterDestinationGpkg(QgsProcessingParameterRasterDestination):
    """overrides the defaultFileExtension method to gpkg
    ALTERNATIVE:
    from types import MethodType
    QPPRD = QgsProcessingParameterRasterDestination(self.OUTPUT_layer, self.tr("Output layer"))
    def _defaultFileExtension(self):
        return "gpkg"
    QPPRD.defaultFileExtension = MethodType(_defaultFileExtension, QPPRD)
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def defaultFileExtension(self):
        return "gpkg"


def run_alg_style_raster_legend(
    labels,
    offset=0,
):
    """Create a New Post Processor class and returns it

    # Just simply creating a new instance of the class was not working
    # for details see https://gis.stackexchange.com/questions/423650/qgsprocessinglayerpostprocessorinterface-only-processing-the-last-layer
    """

    class LayerPostProcessor(QgsProcessingLayerPostProcessorInterface):
        instance = None
        lbls = labels
        ofst = offset

        def postProcessLayer(self, layer, context, feedback):
            if layer.isValid():
                colors = colormap_to_hex_list("gnuplot", len(self.lbls) + 4)[2:-2]

                lst = []
                for i, lbl in enumerate(self.lbls):
                    lst += [
                        QgsColorRampShader.ColorRampItem(i + self.ofst, QColor(*colors[i]), f"{i + self.ofst}: {lbl}")
                    ]
                class_data = QgsPalettedRasterRenderer.colorTableToClassData(lst)

                qprr = QgsPalettedRasterRenderer(layer.dataProvider(), 1, class_data)
                layer.setRenderer(qprr)

        # Hack to work around sip bug!
        @staticmethod
        def create() -> "LayerPostProcessor":
            LayerPostProcessor.instance = LayerPostProcessor()
            return LayerPostProcessor.instance

    return LayerPostProcessor.create()


def colormap_to_hex_list(colormap: str = "gnuplot", num_colors: int = 10) -> list:
    from matplotlib import colormaps
    from matplotlib.colors import LinearSegmentedColormap, ListedColormap, to_hex

    cm = colormaps.get(colormap)
    if isinstance(cm, LinearSegmentedColormap):
        return (cm(np.linspace(0, 1, num_colors)) * 255).astype(int)
    elif isinstance(cm, ListedColormap):
        return (cm.resampled(num_colors).colors * 255).astype(int)
    return []

from qgis.PyQt.QtWidgets import QGraphicsScene, QGraphicsView, QWidget, QVBoxLayout, QGraphicsProxyWidget
from matplotlib.backends.backend_qtagg import FigureCanvas, NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
class MatplotlibFigures(QGraphicsScene):
    def __init__(self, parent = None, graphicsView = None):
        super(MatplotlibFigures, self).__init__(parent)
        self.canvass = []
        self.proxy_widgets = []
        self.resize = []
        self.cv = -1
        self.graphicsView = graphicsView
        self.oldResizeEvent = self.graphicsView.resizeEvent
        self.graphicsView.resizeEvent = self.resizeEvent
        self.graphicsView.setScene(self)
    def resizeEvent(self, QResizeEvent):
        if self.cv == -1:
            return
        if not self.resize[self.cv]:
            return
        oldSize = QResizeEvent.oldSize()
        ow = oldSize.width()
        oh = oldSize.height()
        size = QResizeEvent.size()
        w = size.width()
        h = size.height()
        ds = abs(w-ow)+abs(h-oh)
        if ds < 4:
            return
        if ds < 8:
            self.fit2gv(self.cv)
            return
        self.proxy_widgets[self.cv].resize(w-5,h-5)
        self.oldResizeEvent( QResizeEvent)
    def new(self, w = None, h = None, **kwargs):
        if w and h:
            canvas = FigureCanvas( Figure( figsize=(w, h), **kwargs))
            self.resize += [ False ]
        else:
            canvas = FigureCanvas( Figure( **kwargs))
            self.resize += [ True ]
        proxy_widget = QGraphicsProxyWidget()
        widget = QWidget()
        layout = QVBoxLayout()
        layout.addWidget( NavigationToolbar(canvas))
        layout.addWidget( canvas)
        widget.setLayout( layout)
        proxy_widget.setWidget(widget)
        proxy_widget.setVisible(False)
        self.addItem(proxy_widget)
        self.canvass += [ canvas ]
        self.proxy_widgets += [ proxy_widget]
        return canvas
    def resize2gv(self, idx):
        w = self.graphicsView.size().width() - 5
        h = self.graphicsView.size().height() - 5
        self.proxy_widgets[idx].resize(w,h)
    def fit2gv(self, idx):
        self.graphicsView.fitInView( self.proxy_widgets[idx])
    def show(self, idx):
        if self.cv == idx:
            return
        if self.resize[idx]:
            self.resize2gv(idx)
        self.proxy_widgets[idx].setVisible(True)
        self.proxy_widgets[self.cv].setVisible(False)
        self.cv = idx
