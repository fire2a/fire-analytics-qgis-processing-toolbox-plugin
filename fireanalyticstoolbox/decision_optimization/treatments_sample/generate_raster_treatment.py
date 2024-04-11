#!python3
"""
RASTER TREATMENT & TEAMS SENSIBLE INSTANCE GENERATOR

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
from pandas import DataFrame

np.set_printoptions(precision=2)  # , formatter={'float_kind': '{: 0.2f}'.format})

# config = {
values = [1000, 2000]
costs = [100, 200]
px_area = 1
W = 200  # width
H = 200  # height
R = 5  # treatments
E = 3  # teams
nodata = -1
# }

# treatments are random three letter words
treat_names = ["".join(np.random.choice(list(string.ascii_lowercase), 3)) for _ in range(R)]
print(f"{treat_names=}")

team_names = ["".join(np.random.choice(list(string.ascii_uppercase), 2)) for _ in range(E)]
print(f"{team_names=}")


# helper for putting random no data values
rnd_idx = lambda: (np.random.choice(range(H)), np.random.choice(range(W)))
rnd_idxs = lambda n: [(np.random.choice(range(H)), np.random.choice(range(W))) for _ in range(n)]
nodata_idx = []

#
# current
#
current_treatment = np.random.choice(range(R), (H, W))
current_value = np.random.uniform(*values, size=(H, W))

# add some nodata
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

#
# treatment costs
#
treat_cost = np.random.uniform(*costs, size=(R, R))
treat_cost[np.eye(R, dtype=bool)] = 0

#
# treatment values
#
target_value = np.random.uniform(*values, size=(R, H, W))

# add some nodata
num_values = np.array(target_value.shape).prod()
print(f"{num_values=}")

# put nodata wherever current_treatment
target_value[current_treatment == np.arange(R)[:, None, None]] = nodata
target_value

# some more nodata
for t in range(R):
    if np.random.rand() < 0.2:
        for idx in rnd_idxs(2):
            target_value[t, idx] = nodata

num_nodata_values = len(np.where(target_value == nodata)[0])
percent_nodata_values = num_nodata_values / num_values
print(f"{num_nodata_values=}, {percent_nodata_values=:.2f} ")


# view
print(f"{W=}, {H=}, {R=}, {E=}")
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

feasible_ratio = len(feasible_set) / (W * H * R)
print(f"{feasible_ratio=: 0.2f}")

feasible_ratio2d = len(feasible_set2d) / (W * H)
print(f"{feasible_ratio2d=: 0.2f}")

nodata_idx += list(zip(*np.where(current_treatment == nodata)))

area = feasible_ratio * 0.618 * (W * H * R) * px_area
treat_areas = np.array([(0.5 + np.random.rand()) * area / R for _ in range(R)])
print(f"{area=: 0.2f}, {treat_areas=}, {treat_areas.sum()/area=: 0.3f}")

budget = treat_cost[treat_cost != 0].mean() * area
treat_budgets = np.array([(0.5 + np.random.rand()) * budget / R for _ in range(R)])
print(f"{budget=: 0.2f}, {treat_budgets=}, {treat_budgets.sum()/budget=: 0.3f}")

# teams
team_on_cost = np.random.uniform(*costs, size=E)
team_area = np.array([(0.5 + np.random.rand()) * area / E for _ in range(E)])
team_budget = np.array([(0.5 + np.random.rand()) * budget / E for _ in range(E)])
print(f"{team_on_cost=}")
print(f"{team_area=}, {team_area.sum()/area=: 0.3f}")
print(f"{team_budget=}, {team_budget.sum()/budget=: 0.3f}")

# binary treatment ability
team_ability = np.random.randint(2, size=(E, R))
# each treatment has at least one able team
for r in range(R):
    if team_ability[:, r].sum() == 0:
        team_ability[np.random.randint(E), r] = 1
assert np.all(team_ability.sum(axis=0) > 0)

#
# write files
with open("raster_params.txt", "w") as params_file:
    params_file.write(f"{H=}\n")
    params_file.write(f"{W=}\n")
    params_file.write(f"{R=}\n")
    params_file.write(f"{E=}\n")
    params_file.write(f"{treat_names=}\n")
    params_file.write(f"{team_names=}\n")
    params_file.write(f"{area=}\n")
    params_file.write(f"{budget=}\n")

# treat matrix
DataFrame(treat_cost, index=treat_names, columns=treat_names).to_csv("raster_treatment_costs.csv", float_format="%.4f")

# treat area budget
DataFrame({"area": treat_areas, "budget": treat_budgets, "treatment": treat_names}).set_index("treatment").to_csv(
    "raster_treatment_params.csv", float_format="%.4f"
)

# teams
adict = {"on_cost": team_on_cost, "area": team_area, "budget": team_budget, "team": team_names}
adict.update(dict(zip(treat_names, team_ability.T)))
DataFrame(adict).set_index("team").to_csv("raster_team_params.csv", float_format="%.4f")


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
ds = GetDriverByName("GTiff").Create(name + ".tif", W, H, R, dtype)
ds.SetGeoTransform((0, px_area, 0, 0, 0, px_area))  # specify coords
# ds.SetProjection(base_raster.crs().authid())  # export coords to file
for i in range(R):
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
