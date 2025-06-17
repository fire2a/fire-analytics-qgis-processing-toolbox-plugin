#!python3


def get_color_table(feedback, amin, amax, cm=colormaps.get("magma")):
    """set colormap for a band"""
    acm = (array(to_rgba_array(cm.colors)) * 255).astype(int)
    ramp = linspace(amin, amax + 1, 255, dtype=int)
    colors = None
    colors = gdal.ColorTable()
    for i in range(254):
        ret = colors.CreateColorRamp(int(ramp[i]), tuple(acm[i]), int(ramp[i + 1]), tuple(acm[i + 1]))
        feedback.pushDebugInfo(f"i: {i}, {tuple(acm[i])}, {i+1}, {tuple(acm[i+1])}, {ret}")
    return colors


# def get_color_table(feedback, cm = colormaps.get('magma')):
#     """set colormap for a band"""
#     acm = (array(to_rgba_array(cm.colors))*255).astype(int)
#     colors = gdal.ColorTable()
#     for i in range(254):
#         ret = colors.CreateColorRamp(i, tuple(acm[i]), i+1, tuple(acm[i+1]))
#         feedback.pushDebugInfo(f"i: {i}, {tuple(acm[i])}, {i+1}, {tuple(acm[i+1])}, {ret}")
#     return colors


class RasterPostProcessor(QgsProcessingLayerPostProcessorInterface):
    def __init__(self, display_name, layer_color1, layer_color2):
        super().__init__()
        self.name = display_name
        self.color1 = layer_color1
        self.color2 = layer_color2

    def postProcessLayer(self, layer, context, feedback):
        feedback.pushInfo(f"Inside postProcessLayer: {self.name}")
        if layer.isValid():
            feedback.pushInfo(f"Layer valid: {self.name}")
            layer.setName(self.name)

            prov = layer.dataProvider()
            stats = prov.bandStatistics(1, QgsRasterBandStats.All, layer.extent(), 0)
            min = stats.minimumValue
            max = stats.maximumValue
            renderer = QgsSingleBandPseudoColorRenderer(layer.dataProvider(), band=1)
            color_ramp = QgsGradientColorRamp(QColor(*self.color1), QColor(*self.color2))
            renderer.setClassificationMin(min)
            renderer.setClassificationMax(max)
            renderer.createShader(color_ramp)
            layer.setRenderer(renderer)
        else:
            feedback.pushInfo(f"Layer not valid: {self.name}")


class Renamer(QgsProcessingLayerPostProcessorInterface):
    def __init__(self, layer_name):
        self.name = layer_name
        super().__init__()

    def postProcessLayer(self, layer, context, feedback):
        layer.setName(self.name)


def run_alg_styler(display_name, layer_color1, layer_color2):
    """Create a New Post Processor class and returns it"""

    # Just simply creating a new instance of the class was not working
    # for details see https://gis.stackexchange.com/questions/423650/qgsprocessinglayerpostprocessorinterface-only-processing-the-last-layer
    class LayerPostProcessor(QgsProcessingLayerPostProcessorInterface):
        instance = None
        name = display_name
        color1 = layer_color1
        color2 = layer_color2

        def postProcessLayer(self, layer, context, feedback):
            feedback.pushInfo(f"Inside postProcessLayer: {self.name}")
            if layer.isValid():
                feedback.pushInfo(f"Layer valid: {self.name}")
                layer.setName(self.name)

                prov = layer.dataProvider()
                stats = prov.bandStatistics(1, QgsRasterBandStats.All, layer.extent(), 0)
                min = stats.minimumValue
                max = stats.maximumValue
                renderer = QgsSingleBandPseudoColorRenderer(layer.dataProvider(), band=1)
                color_ramp = QgsGradientColorRamp(QColor(*self.color1), QColor(*self.color2))
                renderer.setClassificationMin(min)
                renderer.setClassificationMax(max)
                renderer.createShader(color_ramp)
                layer.setRenderer(renderer)
            else:
                feedback.pushInfo(f"Layer not valid: {self.name}")

        # Hack to work around sip bug!
        @staticmethod
        def create() -> "LayerPostProcessor":
            LayerPostProcessor.instance = LayerPostProcessor()
            return LayerPostProcessor.instance

    return LayerPostProcessor.create()


def get_gdal_extensions():
    from osgeo import gdal

    ext = []
    for i in range(gdal.GetDriverCount()):
        drv = gdal.GetDriver(i)
        if drv.GetMetadataItem(gdal.DCAP_RASTER):
            print(drv.GetMetadataItem(gdal.DMD_LONGNAME), drv.GetMetadataItem(gdal.DMD_EXTENSIONS))
            if item := drv.GetMetadataItem(gdal.DMD_EXTENSIONS):
                ext.extend(item.split(" "))


def match_any_file_except(ext="xml"):
    return f"*.[!{ext}]"


class WeatherBuilder(QgsProcessingAlgorithm):
    """Cell2Fire"""

    OUTPUT_FOLDER = "OutputFolder"
    OUTPUT_FOLDER_IN_CURRENT_PROJECT = "CreateOutputFolderInCurrentProject"
    FUEL_MODEL = "FuelModel"
    WEAFILE = "WeatherFile"
    WEADIR = "WeatherDirectory"
    WEASCN = "WeatherScenarios"
    WEADIST = "WeatherDistribution"

    def initAlgorithm(self, config):
        """
        Here we define the inputs and output of the algorithm, along
        with some other properties.
        """
        project_path = QgsProject().instance().absolutePath()
        weadistfile = Path(project_path, "WeathersDistribution.csv")
        if not weadistfile.is_file():
            weadistfile = Path(self.plugin_dir, "simulator", "WeathersDistribution.csv")
        self.addParameter(
            QgsProcessingParameterFile(
                name=self.WEAFILE,
                description=self.tr(
                    "Two column csv file describing the number of times each scenario should be repeated"
                ),
                behavior=QgsProcessingParameterFile.File,
                extension="csv",
                defaultValue=str(weadistfile) if weadistfile.is_file() else None,
                optional=True,
                fileFilter="",
            )
        )
        weascenfile = Path(project_path, "WeatherScenarios.csv")
        self.addParameter(
            QgsProcessingParameterFile(
                name=self.WEAFILE,
                description=self.tr("Weather Scenarios files"),
                behavior=QgsProcessingParameterFile.File,
                extension="csv",
                defaultValue=str(weascenfile) if weascenfile.is_file() else None,
                optional=True,
                fileFilter="",
            )
        )
        self.addParameter(
            QgsProcessingParameterFolderDestination(
                name=self.OUTPUT_FOLDER,
                description=self.tr("Output directory", "BaseContext")
                + " "
                + self.tr("(destructive action warning: empties contents if already exists)"),
                defaultValue=None,
                optional=True,
                createByDefault=True,
            )
        )
