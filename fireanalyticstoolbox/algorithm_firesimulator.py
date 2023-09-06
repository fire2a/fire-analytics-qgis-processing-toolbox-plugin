from processing.gui.wrappers import WidgetWrapper
from qgis.core import (QgsFieldProxyModel, QgsMapLayerProxyModel,
                       QgsProcessing, QgsProcessingAlgorithm,
                       QgsProcessingParameterMatrix, QgsMessageLog)
from qgis.gui import QgsFieldComboBox, QgsMapLayerComboBox
from qgis.PyQt.QtCore import QCoreApplication, Qt, QVariant
from qgis.PyQt.QtWidgets import (QComboBox, QCompleter, QGridLayout, QLabel,
                                 QWidget)

from .simulator.cell2fire2asimulator_dialog import Fire2aSimulatorDialog


class FireSimulatorAlgorithm(QgsProcessingAlgorithm):
    INPUT_PARAMS = "INPUT_PARAMS"

    def __init__(self):
        super().__init__()

    def name(self):
        return "cell2firesimulator"

    def displayName(self):
        return "(Cell2)Fire Simulator"

    def group(self):
        return self.tr(self.groupId())

    def groupId(self):
        return "experimental"

    def shortHelpString(self):
        return "Example of using a custom widget wrapper."

    def helpUrl(self):
        return "https://qgis.org"

    def createInstance(self):
        return type(self)()

    def initAlgorithm(self, config=None):
        test_param = QgsProcessingParameterMatrix(self.INPUT_PARAMS, "Input Parameters", headers=["Parameter", "ValueA", "ValueB", "ValueC", "ValueD", "ValueE", "ValueF"])
        QgsMessageLog.logMessage(f"test_param: {test_param.asPythonString()}", "FireSimulatorAlgorithm")
        test_param.setMetadata({"widget_wrapper": {"class": CustomParametersWidget}})
        self.addParameter(test_param)

    def processAlgorithm(self, parameters, context, feedback):
        # Retrieve the list of parameters returned by the custom widget wrapper
        input_params_list = self.parameterAsMatrix(parameters, "INPUT_PARAMS", context)
        # Access the list items to retrieve each parameter object
        names = ['fuel model', '1', '2', '3', '4', '5', '6']
        # Just for demonstration we can return the input parameters to check their values...
        return dict(zip(names,input_params_list))


# Widget Wrapper class
class CustomParametersWidget(WidgetWrapper):
    def createWidget(self):
        self.cpw = Fire2aSimulatorDialog()
        return self.cpw

    def value(self):
        # This method gets the parameter values and returns them in a list...
        # which will be retrieved and parsed in the processAlgorithm() method
        return [
            self.cpw.comboBox.currentText(),
            self.cpw.radioButton.isChecked(),
            self.cpw.radioButton_2.isChecked(),
            self.cpw.mMapLayerComboBox.currentLayer().publicSource(),
            self.cpw.mQgsFileWidget.filePath(),
            self.cpw.mQgsDoubleSpinBox.value(),
            self.cpw.mQgsDoubleSpinBox_2.value(),
        ]

