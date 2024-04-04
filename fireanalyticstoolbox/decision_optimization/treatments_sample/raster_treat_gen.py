#!python3

import string

import numpy as np

# random three letter words
treat_names = ["".join(np.random.choice(list(string.ascii_lowercase), 3)) for _ in range(3)]

W, H = 3, 4
T = len(treat_names)

rnd_idx = lambda: (np.random.choice(range(H)), np.random.choice(range(W)))
nodata = -1
nodata_idx = []

# current
current_treatment = np.random.choice(range(T), (H, W))
current_value = np.random.rand(H, W)

# put in a random index a nodata value
current_value[rnd_idx()] = nodata
nodata_idx += list(zip(*np.where(current_value == nodata)))
current_treatment[rnd_idx()] = nodata
nodata_idx += list(zip(*np.where(current_treatment == nodata)))

# treatment costs
treat_cost = np.random.rand(T, T)
treat_cost[np.eye(T, dtype=bool)] = 0

# treatment value
target_value = np.random.rand(T, H, W)
# put nodata wherever current_treatment
target_value[current_treatment == np.arange(T)[:, None, None]] = nodata
target_value


print(f"{W=}, {H=}, {T=}")
print(f"{treat_name=}")
print(f"{current_treatment=}, {current_treatment.shape=}")
print(f"{current_value=}, {current_value.shape=}")
print(f"{treat_cost=}, {treat_cost.shape=}")


# assert each pixel has a valid treatment
assert np.all(np.any(target_value[:, w, h] != np.nan) for w in range(W) for h in range(H))

# for each pixel (h, w), get the indexes of treatment values that are not nan
tr, hh, ww = np.where(~np.isnan(target_value))

feasible_set = {(h, w, t) for t, h, w in zip(tr, hh, ww)}
# ver
display(np.where(np.isnan(target_value)), target_value, np.where(~np.isnan(target_value)), sep="\n")
