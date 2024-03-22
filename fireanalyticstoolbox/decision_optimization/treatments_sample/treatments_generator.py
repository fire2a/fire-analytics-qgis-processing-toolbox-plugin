#!python3
"""
polygon treatment sensible instance generator
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

# names
treat_names = ["".join(np.random.choice(list(string.ascii_uppercase), size=3)) for _ in range(config["num_treatments"])]
treat_names.sort()
print(f"{treat_names=}")

params_file = open("params.txt", "w")
params_file.write(f"{treat_names=}")

# polygon current attributes
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

# generate
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
dfa = pd.DataFrame(attributes, columns=["fid"] + attr_names)
print(dfa)
dfa.to_csv("attributes.csv", index=False)

# target treatment table
target_cols = ["fid", "treatment", "value", "value/m2", "cost", "cost/m2"]
treat_table = []
for feat in layer.getFeatures():
    possible_targets = treat_names.copy()
    possible_targets.remove(feat["treatment"])
    for trgt in np.random.choice(possible_targets, replace=False, size=np.random.randint(1, len(possible_targets))):
        # fid, treatment, value, value/m2, cost, cost/m2
        treat_table += [
            [
                feat["fid"],
                trgt,
                np.random.uniform(*config["values"]),
                np.random.uniform(*config["values"]) / feat["area"],
                np.random.uniform(*config["costs"]),
                np.random.uniform(*config["costs"]) / feat["area"],
            ]
        ]

dft = pd.DataFrame(treat_table, columns=target_cols)
print(dft)
dft.to_csv("treatments.csv", index=False)

params_file.close()

# re-read
print(f"{treat_names=}")
dfa = pd.read_csv("attributes.csv")
dft = pd.read_csv("treatments.csv")
treat_names = np.unique(dft["treatment"].to_list() + dfa["treatment"].to_list()).tolist()
print(f"{treat_names=}")

# generate treatment cube
treat_cube = np.zeros((len(dfa), len(treat_names), len(treat_names)), dtype=bool)

for i, current in dfa.iterrows():
    # get targets
    targets = dft[dft["fid"] == current["fid"]]
    for _, target in targets.iterrows():
        treat_cube[i, treat_names.index(current["treatment"]), treat_names.index(target["treatment"])] = True

# each feature has at least one target
# and no targets outside its current
treat_idxs = list(range(len(treat_names)))
for i, current in dfa.iterrows():
    j = treat_names.index(current["treatment"])
    assert any(treat_cube[i, j, :])
    other_idxs = treat_idxs.copy()
    other_idxs.remove(j)
    for k in other_idxs:
        assert not any(treat_cube[i, k, :])

budget = (dft["cost"].mean() + dft["cost/m2"].mean() * dfa["area"].mean()) * len(dfa) * 0.618
print(f"{budget=}")

area = dfa["area"].mean() * len(dfa) * 0.618
print(f"{area=}")

with open("params.txt", "w") as f:
    f.write(f"{treat_names=}\n{budget=}\n{area=}")

print("files are @", getcwd())
