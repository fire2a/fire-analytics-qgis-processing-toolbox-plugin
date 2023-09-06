from processing.gui.wrappers import WidgetWrapper
from qgis.core import (QgsFieldProxyModel, QgsMapLayerProxyModel,
                       QgsProcessing, QgsProcessingAlgorithm,
                       QgsProcessingParameterMatrix)
from qgis.gui import QgsFieldComboBox, QgsMapLayerComboBox
from qgis.PyQt.QtCore import QCoreApplication, Qt, QVariant
from qgis.PyQt.QtWidgets import (QComboBox, QCompleter, QGridLayout, QLabel,
                                 QWidget)


class AddLayoutTable(QgsProcessingAlgorithm):
    INPUT_PARAMS = "INPUT_PARAMS"

    def __init__(self):
        super().__init__()

    def name(self):
        return "widgetwrapperdemo"

    def displayName(self):
        return "Widget Wrapper Demo"

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
        test_param = QgsProcessingParameterMatrix(self.INPUT_PARAMS, "Input Parameters")
        test_param.setMetadata({"widget_wrapper": {"class": CustomParametersWidget}})
        self.addParameter(test_param)

    def processAlgorithm(self, parameters, context, feedback):
        # Retrieve the list of parameters returned by the custom widget wrapper
        input_params_list = self.parameterAsMatrix(parameters, "INPUT_PARAMS", context)
        # Access the list items to retrieve each parameter object
        node_lyr = input_params_list[0]
        node_fld = input_params_list[1]
        # Check whether Type of input field is String or Integer
        if node_lyr.fields()[node_lyr.fields().lookupField(node_fld)].type() == QVariant.String:
            node_id = input_params_list[2]
        elif node_lyr.fields()[node_lyr.fields().lookupField(node_fld)].isNumeric():
            node_id = int(input_params_list[2])
        else:
            node_id = "None"

        node_feats = [ft for ft in node_lyr.getFeatures() if ft[node_fld] == node_id]

        for feat in node_feats:
            continue
            # Do something with feat

        # Just for demonstration we can return the input parameters to check their values...
        return {"Input Node Layer": node_lyr, "Node Field": node_fld, "Node ID": node_id, "Node Features": node_feats}


# Widget Wrapper class
class CustomParametersWidget(WidgetWrapper):
    def createWidget(self):
        self.cpw = CustomWidget()
        return self.cpw

    def value(self):
        # This method gets the parameter values and returns them in a list...
        # which will be retrieved and parsed in the processAlgorithm() method
        self.lyr = self.cpw.getLayer()
        self.fld = self.cpw.getField()
        self.node_id = self.cpw.getFieldValue()
        return [self.lyr, self.fld, self.node_id]


# Custom Widget class
class CustomWidget(QWidget):
    def __init__(self):
        super(CustomWidget, self).__init__()
        self.lyr_lbl = QLabel("Input Nodes Layer", self)
        self.lyr_cb = QgsMapLayerComboBox(self)
        self.fld_lbl = QLabel("Node ID Field")
        self.fld_cb = QgsFieldComboBox(self)
        self.id_lbl = QLabel("Node ID")
        self.id_cb = QComboBox(self)
        self.layout = QGridLayout(self)
        self.layout.addWidget(self.lyr_lbl, 0, 0, 1, 1, Qt.AlignRight)
        self.layout.addWidget(self.lyr_cb, 0, 1, 1, 2)
        self.layout.addWidget(self.fld_lbl, 1, 0, 1, 1, Qt.AlignRight)
        self.layout.addWidget(self.fld_cb, 1, 1, 1, 2)
        self.layout.addWidget(self.id_lbl, 2, 0, 1, 1, Qt.AlignRight)
        self.layout.addWidget(self.id_cb, 2, 1, 1, 2)
        # Set filter on the map layer combobox (here we show only point layers)
        self.lyr_cb.setFilters(QgsMapLayerProxyModel.PointLayer)
        self.fld_cb.setLayer(self.lyr_cb.currentLayer())
        # Set filters on field combobox (here we show only string and integer fields)
        self.fld_cb.setFilters(QgsFieldProxyModel.Int | QgsFieldProxyModel.LongLong | QgsFieldProxyModel.String)
        self.lyr_cb.layerChanged.connect(self.layerChanged)
        self.populateIds()
        self.fld_cb.fieldChanged.connect(self.populateIds)

    def layerChanged(self):
        self.fld_cb.setLayer(self.lyr_cb.currentLayer())

    def populateIds(self):
        """Populate the Node ID combo box with all unique values in the selected field"""
        self.id_cb.clear()

        if node_lyr := self.lyr_cb.currentLayer():
            id_fld = self.fld_cb.currentField()
            fld_idx = node_lyr.fields().lookupField(id_fld)
            id_vals = node_lyr.uniqueValues(fld_idx)
            self.id_cb.addItems([str(val) for val in id_vals])
            # Make combo box editable and set up a QCompleter
            self.id_cb.setEditable(True)
            completer = QCompleter([str(val) for val in id_vals], self)
            completer.setCaseSensitivity(Qt.CaseInsensitive)
            # Default is Qt.MatchStartsWith... (change if you want)
            completer.setFilterMode(Qt.MatchContains)
            self.id_cb.setCompleter(completer)

    def getLayer(self):
        return self.lyr_cb.currentLayer()

    def getField(self):
        return self.fld_cb.currentField()

    def getFieldValue(self):
        return self.id_cb.currentText()
