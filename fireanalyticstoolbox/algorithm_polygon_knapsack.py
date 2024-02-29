#!python3
"""
Neighbors from: 2014 Ujaval Gandhi, neighbors.py
"""
import numpy as np

VALUE = "VALUE"
WEIGHT = "WEIGHT"

layer = iface.activeLayer()
field_names = layer.fields().names()

if WEIGHT not in field_names:
    print(f"ERROR {layer=}, attribute {WEIGHT=} not found, using area as weight")
    if not layer.isEditable():
        layer.startEditing()
    layer.dataProvider().addAttributes([QgsField(WEIGHT, QVariant.Double)])
    layer.updateFields()
    for f in layer.getFeatures():
        geom = f.geometry()
        f[WEIGHT] = int(geom.length())
        layer.updateFeature(f)
    layer.commitChanges()
else:
    assert layer.fields().field(WEIGHT).isNumeric()

if VALUE not in field_names:
    print(f"ERROR {layer=}, attribute {VALUE=} not found, using perimeter as value")
    if not layer.isEditable():
        layer.startEditing()
    layer.dataProvider().addAttributes([QgsField(VALUE, QVariant.Double)])
    layer.updateFields()
    for f in layer.getFeatures():
        geom = f.geometry()
        f[VALUE] = int(geom.area())
        layer.updateFeature(f)
    layer.commitChanges()
else:
    assert layer.fields().field(VALUE).isNumeric()


print(layer)

dp = layer.dataProvider()
fnm = dp.fieldNameMap()

value_data = []
weight_data = []
qfr = QgsFeatureRequest().setSubsetOfAttributes([VALUE, WEIGHT], layer.fields())
for feat in dp.getFeatures(qfr):
    """
    attr = feat.attributes()
    values += [ attr[fnm[VALUE]]]
    weights += [ attr[fnm[WEIGHT]]]
    """
    value_data += [feat.attribute(VALUE)]
    weight_data += [feat.attribute(WEIGHT)]

value_data = np.array(value_data)
weight_data = np.array(weight_data)

value_data[1] = np.nan
weight_data[3] = np.nan

no_indexes = np.where(np.isnan(value_data) | np.isnan(weight_data))[0]
assert len(value_data) == len(weight_data)
N = len(value_data)
mask = np.ones(N, dtype=bool)
mask[no_indexes] = False

weight_sum = weight_data[mask].sum()
capacity = np.round(weight_sum * 0.5)

from pyomo import environ as pyo

m = pyo.ConcreteModel()
m.N = pyo.RangeSet(0, N - len(no_indexes) - 1)
m.Cap = pyo.Param(initialize=capacity)
m.We = pyo.Param(m.N, within=pyo.Reals, initialize=weight_data[mask])
m.Va = pyo.Param(m.N, within=pyo.Reals, initialize=value_data[mask])
m.X = pyo.Var(m.N, within=pyo.Binary)
obj_expr = pyo.sum_product(m.X, m.Va, index=m.N)
m.obj = pyo.Objective(expr=obj_expr, sense=pyo.maximize)


def capacity_rule(m):
    return pyo.sum_product(m.X, m.We, index=m.N) <= m.Cap


m.capacity = pyo.Constraint(rule=capacity_rule)
