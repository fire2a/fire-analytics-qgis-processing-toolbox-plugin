#!python3
"""
image = layer.previewAsImage(QSize(400, 400))
self.assertFalse(image.isNull())
self.assertTrue(image.save(os.path.join(temp_dir.path(), 'expected.png'), "PNG"))
"""
from pathlib import Path

import numpy as np
from qgis.core import *
from qgis.PyQt.QtCore import QByteArray  # , QVariant

from .algorithm_utils import get_output_raster_format


class RasterTutorial(QgsProcessingAlgorithm):
    IN = "InputRaster"
    OUT = "OutPutRaster"

    def groupId(self):
        return "zexperimental"

    def name(self):
        return "rastertutorial"

    def displayName(self):
        return "raster tutorial"

    def createInstance(self):
        return RasterTutorial()

    def shortHelpString(self):
        extension_list = QgsRasterFileWriter.supportedFormatExtensions(QgsRasterFileWriter.RasterFormatOptions())
        extension_list.sort()
        extension_vertical_list = "\n".join(extension_list)
        return f"(Check algorithm_raster_tutorial.py\nSupported raster formats by extension:\n{extension_list} {extension_vertical_list}"

    def initAlgorithm(self, config):
        self.addParameter(QgsProcessingParameterRasterLayer(self.IN, "Input Raster"))
        self.addParameter(QgsProcessingParameterRasterDestination(self.OUT, "Output Raster"))

    def checkParameterValues(self, parameters, context):
        src_raster = self.parameterAsRasterLayer(parameters, self.IN, context)
        if not src_raster.isValid():
            return False, f"Input raster {src_raster} not valid"
        dst_fname = self.parameterAsOutputLayer(parameters, self.OUT, context)
        dst_ext = Path(dst_fname).suffix[1:]
        if dst_ext not in QgsRasterFileWriter.supportedFormatExtensions(QgsRasterFileWriter.RasterFormatOptions()):
            return False, f"Output raster format .{dst_ext} not supported"
        if QgsRasterFileWriter.driverForExtension(dst_ext) == "":
            return False, f"Output raster extension .{dst_ext} not supported"
        return True, ""

    def processAlgorithm(self, parameters, context, feedback):
        feedback.pushDebugInfo("processAlgorithm start")
        feedback.pushDebugInfo(f"context args: {context.asQgisProcessArguments()}")
        # INPUT
        src_raster = self.parameterAsRasterLayer(parameters, self.IN, context)
        # src_raster = iface.activeLayer()
        feedback.pushDebugInfo(f"src_raster: {src_raster}\n")
        # get data
        src_provider = src_raster.dataProvider()
        if src_raster.bandCount() == 1:
            src_block = src_provider.block(1, src_raster.extent(), src_raster.width(), src_raster.height())
            src_nodata = None
            if src_block.hasNoDataValue():
                src_nodata = src_block.noDataValue()
            np_dtype = qgis2numpy_dtype(src_provider.dataType(1))
            src_data = np.frombuffer(src_block.data(), dtype=np_dtype).reshape(src_raster.height(), src_raster.width())
        else:
            src_data = []
            src_nodata = []
            np_dtype = []
            for i in range(src_raster.bandCount()):
                src_block = src_provider.block(i + 1, src_raster.extent(), src_raster.width(), src_raster.height())
                src_nodata += [None]
                if src_block.hasNoDataValue():
                    src_nodata[-1] = src_block.noDataValue()
                np_dtype += [qgis2numpy_dtype(src_provider.dataType(i + 1))]
                src_data += [
                    np.frombuffer(src_provider.data(), dtype=np_dtype[-1]).reshape(
                        src_raster.height(), src_raster.width()
                    )
                ]
            src_data = np.array(src_data)
        feedback.pushDebugInfo(
            f"src_data: {src_data}\nsrc_data.shape: {src_data.shape}\nsrc_data.dtype: {src_data.dtype}\n"
        )
        # OUTPUT
        dst_fname = self.parameterAsOutputLayer(parameters, self.OUT, context)
        dst_name = Path(dst_fname).stem
        dst_format = get_output_raster_format(dst_fname, feedback)
        feedback.pushDebugInfo(f"dst_fname: {dst_fname}\ndst_name: {dst_name}\ndst_format: {dst_format}")
        #
        file_writer = QgsRasterFileWriter(dst_fname)
        #

        # JUST COPY
        # pipe = QgsRasterPipe()
        # if not pipe.set(src_provider.clone()):
        #     feedback.reportError("Cannot set pipe provider")
        #     raise QgsProcessingException("Cannot set pipe provider")
        # projector = QgsRasterProjector()
        # projector.setCrs(src_provider.crs(), src_provider.crs())
        # if not pipe.insert(2, projector):
        #     feedback.reportError("Cannot set pipe projector")
        #     raise QgsProcessingException("Cannot set pipe projector")
        # if 0 != file_writer.writeRaster(pipe, src_provider.xSize(), src_provider.ySize(), src_provider.extent(), src_provider.crs()):
        #     feedback.reportError("Cannot write raster")
        #     raise QgsProcessingException("Cannot write raster")

        assert src_raster.height() == src_data.shape[0]
        assert src_raster.width() == src_data.shape[1]

        # CREATE GPKG
        if src_raster.bandCount() == 1:
            # dst_name = 'hola'
            # file_writer = QgsRasterFileWriter('hola.gpkg')
            file_writer.setOutputFormat("gpkg")
            file_writer.setCreateOptions(["RASTER_TABLE=" + dst_name, "APPEND_SUBDATASET=YES"])
            # file_writer.setCreateOptions(["RASTER_TABLE=hola", "APPEND_SUBDATASET=YES"])
            src_data = np.float32(src_data)
            bites = QByteArray(src_data.tobytes())
            # block = QgsRasterBlock(src_provider.dataType(1), src_raster.width(), src_raster.height()) # Qgis.Float32
            block = QgsRasterBlock(Qgis.Float32, src_raster.width(), src_raster.height())  # Qgis.Float32
            block.setData(bites)
            feedback.pushDebugInfo(f"block: {block}{block.isValid()}")
            # provider = file_writer.createOneBandRaster(src_provider.dataType(1), src_raster.width(), src_raster.height(), src_raster.extent(), src_raster.crs())
            provider = file_writer.createOneBandRaster(
                Qgis.Float32, src_raster.width(), src_raster.height(), src_raster.extent(), src_raster.crs()
            )
            if not provider.isEditable():
                if not provider.setEditable(True):
                    raise QgsProcessingException("Cannot set provider editable")
            if not provider.writeBlock(block, 1, 0, 0):
                raise QgsProcessingException("Cannot write block")
            if src_nodata:
                if not provider.setNoDataValue(1, float(src_nodata)):
                    raise QgsProcessingException("Cannot set nodata")
            if provider.isEditable():
                if not provider.setEditable(False):
                    raise QgsProcessingException("Cannot set provider NOT editable")
            feedback.pushDebugInfo(f"provider: {provider}{provider.isValid()}")
            # del provider, block, bites, file_writer
        # TODO multiband
        # else:
        #    pass

        return {self.OUT: dst_fname}


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
