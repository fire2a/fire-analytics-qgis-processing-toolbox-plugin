#!python3
"""
POLYGON TREATMENT SENSIBLE INSTANCE GENERATOR

Inputs:
1. Config dictionary (num_treatments and ranges for values and costs)

Outputs: A feasible instance
1. Current status in "current_treatment.tif" and "current_value.tif"
2. Possible treatments in
3. treatment names, total area and budget in params.txt

USAGE: RUN IN THE QGIS PYTHON CONSOLE
- overwrites existing tif rasters and csv.files(check last line for the path)
- then solve using the polygon treatment algorithm
"""
import string
from os import getcwd

import numpy as np

np.set_printoptions(precision=2)  # , formatter={'float_kind': '{: 0.2f}'.format})

# config = {
values = [1000, 2000]
costs = [100, 200]
px_area = 1
W = 200
H = 200
TR = 5
TM = 3
nodata = -1
# }

# treatments are random three letter words
treat_names = ["".join(np.random.choice(list(string.ascii_lowercase), 3)) for _ in range(TR)]
team_names = ["".join(np.random.choice(list(string.ascii_uppercase), 2)) for _ in range(TR)]

# helper for putting random no data values
rnd_idx = lambda: (np.random.choice(range(H)), np.random.choice(range(W)))
rnd_idxs = lambda n: [(np.random.choice(range(H)), np.random.choice(range(W))) for _ in range(n)]
nodata_idx = []

# current
current_treatment = np.random.choice(range(TR), (H, W))
current_value = np.random.uniform(*values, size=(H, W))

# print how many nodata before
print(f"{len(np.where(current_treatment == nodata)[0])=}, {len(np.where(current_value == nodata)[0])=}")

# 1 nodata
for arr in [current_treatment, current_value]:
    arr[rnd_idx()] = nodata
    nodata_idx += list(zip(*np.where(arr == nodata)))

# many nodata
for arr in [current_treatment, current_value]:
    for idx in rnd_idxs(2):
        arr[idx] = nodata
        nodata_idx += list(zip(*np.where(arr == nodata)))

# print how many nodata after
print(f"{len(np.where(current_treatment == nodata)[0])=}, {len(np.where(current_value == nodata)[0])=}")

# treatment costs
treat_cost = np.random.uniform(*costs, size=(TR, TR))
treat_cost[np.eye(TR, dtype=bool)] = 0

# treatment value
target_value = np.random.uniform(*values, size=(TR, H, W))

num_values = np.array(target_value.shape).prod()
print(f"{num_values=}")

# put nodata wherever current_treatment
target_value[current_treatment == np.arange(TR)[:, None, None]] = nodata
target_value

# some more nodata
for t in range(TR):
    if np.random.rand() < 0.2:
        for idx in rnd_idxs(2):
            target_value[t, idx] = nodata

num_nodata_values = len(np.where(target_value == nodata)[0])
percent_nodata_values = num_nodata_values / num_values
print(f"{num_nodata_values=}, {percent_nodata_values=:.2f} ")


# view
print(f"{W=}, {H=}, {TR=}, {TM=}")
print(f"{treat_names=}")
print(f"{team_names=}")
print(f"{current_treatment=}, {current_treatment.shape=}")
print("current_treatment\n", np.vectorize(lambda tr: treat_names[tr])(current_treatment))
print(f"{current_value=}, {current_value.shape=}")
print(f"{treat_cost=}, {treat_cost.shape=}")

# assert each pixel has a valid treatment
assert np.all(np.any(target_value[:, w, h] != nodata) for w in range(W) for h in range(H))

# for each pixel (h, w), get the indexes of valid treatments
tr, hh, ww = np.where(target_value != nodata)
feasible_set = set(zip(tr, hh, ww))
feasible_set2d = set(zip(hh, ww))
print(f"{len(feasible_set)=}, {len(feasible_set2d)=}")

feasible_ratio = len(feasible_set) / (W * H * TR)
print(f"{feasible_ratio=: 0.2f}")

feasible_ratio2d = len(feasible_set2d) / (W * H)
print(f"{feasible_ratio2d=: 0.2f}")

nodata_idx += list(zip(*np.where(current_treatment == nodata)))

area = feasible_ratio * 0.618 * (W * H * TR) * px_area
print(f"{area=: 0.2f}")

budget = treat_cost[treat_cost != 0].mean() * area
print(f"{budget=: 0.2f}")

# teams
team_cost = np.random.uniform(*costs, size=TM)

team_area = np.array([(0.5 + np.random.rand()) * area / TM for _ in range(TM)])
team_budget = np.array([(0.5 + np.random.rand()) * budget / TM for _ in range(TM)])

team_treat_area = np.array([[(0.5 + np.random.rand()) * area / TR / TM for _ in range(TR)] for _ in range(TM)])
team_treat_budget = np.array([[(0.5 + np.random.rand()) * budget / TR / TM for _ in range(TR)] for _ in range(TM)])

#
# write files
with open("raster_params.txt", "w") as params_file:
    params_file.write(f"{treat_names=}\n")
    params_file.write(f"{area=}\n")
    params_file.write(f"{budget=}\n")
# treat matrix
from pandas import DataFrame

DataFrame(treat_cost, index=treat_names, columns=treat_names).to_csv("raster_treatment_costs.csv", float_format="%.6f")

# rasters to tifs
from osgeo.gdal import GDT_Float32, GDT_Int16, GetDriverByName, UseExceptions

UseExceptions()

for name, data, dtype in zip(
    ["current_treatment", "current_value"], [current_treatment, current_value], [GDT_Int16, GDT_Float32]
):
    ds = GetDriverByName("GTiff").Create(name + ".tif", W, H, 1, dtype)
    ds.SetGeoTransform((0, px_area, 0, 0, 0, px_area))  # specify coords
    # ds.SetProjection(base_raster.crs().authid())  # export coords to file
    band = ds.GetRasterBand(1)
    band.SetUnitType(name)
    if 0 != band.SetNoDataValue(nodata):
        feedback.pushWarning(f"Set No Data failed for {name}")
    if 0 != band.WriteArray(data):
        feedback.pushWarning(f"WriteArray failed for {name}")
    ds.FlushCache()  # write to disk
    ds = None

name = "target_value"
data = target_value
dtype = GDT_Float32
ds = GetDriverByName("GTiff").Create(name + ".tif", W, H, TR, dtype)
ds.SetGeoTransform((0, px_area, 0, 0, 0, px_area))  # specify coords
# ds.SetProjection(base_raster.crs().authid())  # export coords to file
for i in range(TR):
    band = ds.GetRasterBand(i + 1)
    band.SetUnitType(name)
    if 0 != band.SetNoDataValue(nodata):
        feedback.pushWarning(f"Set No Data failed for {name}")
    if 0 != band.WriteArray(data[i]):
        feedback.pushWarning(f"WriteArray failed for {name}")
    band = None
ds.FlushCache()  # write to disk
ds = None

print("files are @", getcwd())
