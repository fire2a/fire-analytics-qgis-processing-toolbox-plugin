#!python3
"""
POLYGON TREATMENT SENSIBLE INSTANCE GENERATOR

Inputs:
1. Config dictionary (num_treatments and ranges for values and costs)
2. Existing polygon layer (selected in QGIS (iface.activeLayer))

Outputs: A feasible instance
1. Current status in the attributes of the polygons (also attributes.csv: treatment, value, value/m2, area)
2. Possible treatments in treatments.csv (fid, treatment, value, value/m2, cost, cost/m2)
3. treatment names, total area and budget in params.txt

USAGE: RUN IN THE QGIS PYTHON CONSOLE
- overwrites existing attributes and csv.files (check last line for the path)
- then solve using the polygon treatment algorithm
"""

import string
from os import getcwd

import numpy as np
import pandas as pd

config = {
    "num_treatments": 5,
    "values": [1000, 2000],
    "costs": [100, 200],
}

#
# treatments are just 3 letter words
#
treat_names = ["".join(np.random.choice(list(string.ascii_uppercase), size=3)) for _ in range(config["num_treatments"])]
treat_names.sort()
print(f"{treat_names=}")

params_file = open("params.txt", "w")
params_file.write(f"{treat_names=}\n")

#
# current status into polygon attributes
#
attr_names = ["treatment", "value", "value/m2", "area"]
# get
layer = iface.activeLayer()
# create fields
fields = QgsFields()
fields.append(QgsField("treatment", QVariant.String))
for atna in attr_names[1:]:
    fields.append(QgsField(atna, QVariant.Double))

layer.startEditing()
layer.dataProvider().addAttributes(fields)
layer.updateFields()
# generate OVERWRITING
attributes = []
for feat in layer.getFeatures():
    area = feat.geometry().area()
    attributes += [
        [
            feat.id(),
            str(np.random.choice(treat_names)),
            np.random.uniform(*config["values"]),
            np.random.uniform(*config["values"]) / area,
            float(area),
        ]
    ]
    for i, atna in enumerate(attr_names):
        feat[atna] = attributes[-1][i + 1]
    layer.updateFeature(feat)
layer.commitChanges()
# also csv
dfa = pd.DataFrame(attributes, columns=["fid"] + attr_names)
dfa.to_csv("attributes.csv", index=False)
print(dfa)

#
# target treatment table
#
target_cols = ["fid", "treatment", "value", "value/m2", "cost", "cost/m2"]
treat_table = []
for feat in layer.getFeatures():
    possible_targets = treat_names.copy()
    possible_targets.remove(feat["treatment"])
    for trgt in np.random.choice(possible_targets, replace=False, size=np.random.randint(1, len(possible_targets))):
        # fid, treatment, value, value/m2, cost, cost/m2
        treat_table += [
            [
                feat.id(),
                trgt,
                np.random.uniform(*config["values"]),
                np.random.uniform(*config["values"]) / feat["area"],
                np.random.uniform(*config["costs"]),
                np.random.uniform(*config["costs"]) / feat["area"],
            ]
        ]

dft = pd.DataFrame(treat_table, columns=target_cols)
# also csv
dft.to_csv("treatments.csv", index=False)
print(dft)

budget = (dft["cost"].mean() + dft["cost/m2"].mean() * dfa["area"].mean()) * len(dfa) * 0.618
params_file.write(f"{budget=}\n")
print(f"{budget=}")

area = dfa["area"].mean() * len(dfa) * 0.618
params_file.write(f"{area=}\n")
print(f"{area=}")

params_file.close()
print("files are @", getcwd())
