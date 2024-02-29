#!python3
"""

Ideas from:
 2014 Ujaval Gandhi, neighbors.py
"""

VALUE = "VALUE"
WEIGHT = "WEIGHT"

layer = iface.activeLayer()
features = {f.id(): f for f in layer.getFeatures()}
field_names = layer.fields().names()

if VALUE not in field_names:
    print(f"ERROR {layer=}, attribute {VALUE=} not found, using perimeter as value")
    layer.startEditing()
    layer.dataProvider().addAttributes([QgsField(VALUE, QVariant.Int)])
    layer.updateFields()
    for f in layer.getFeatures():
        geom = f.geometry()
        f[VALUE] = int(geom.length())
        layer.updateFeature(f)
    layer.commitChanges()
else:
    assert layer.fields().field(VALUE).isNumeric()
    

if WEIGHT not in field_names:
    print(f"ERROR {layer=}, attribute {WEIGHT=} not found, using area as weight")
    layer.startEditing()
    layer.dataProvider().addAttributes([QgsField(WEIGHT, QVariant.Int)])
    layer.updateFields()
    for f in layer.getFeatures():
        geom = f.geometry()
        f[VALUE] = int(geom.area())
        layer.updateFeature(f)
    layer.commitChanges()
else:
    assert layer.fields().field(WEIGHT).isNumeric()

print(layer)
print(features)

# if VALUE in features[next(iter(features))].fields().names():
#     value_field = VALUE
