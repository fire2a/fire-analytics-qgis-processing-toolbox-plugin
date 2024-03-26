#!python3
from itertools import product

import numpy as np
import pandas as pd
from pyomo import environ as pyo
from pyomo.common.errors import ApplicationError
from pyomo.opt import SolverFactory, SolverStatus, TerminationCondition

dfa = pd.read_csv("attributes.csv")
dft = pd.read_csv("treatments.csv")
treat_names = np.unique(dft["treatment"].to_list() + dfa["treatment"].to_list()).tolist()
print(f"{treat_names=}")
budget = (dft["cost"].mean() + dft["cost/m2"].mean() * dfa["area"].mean()) * len(dfa) * 0.618
print(f"{budget=}")
area = dfa["area"].mean() * len(dfa) * 0.618
print(f"{area=}")

# generate treatment cube
treat_cube = np.zeros((len(dfa), len(treat_names), len(treat_names)), dtype=bool)

for i, current in dfa.iterrows():
    # get targets
    targets = dft[dft["fid"] == current["fid"]]
    for _, target in targets.iterrows():
        treat_cube[i, treat_names.index(current["treatment"]), treat_names.index(target["treatment"])] = True

# Mixed Integer Linear Programming
m = pyo.ConcreteModel(name="polygon_treatment")

# Sets
m.N = pyo.Set(initialize=dfa.fid)
m.T = pyo.Set(initialize=treat_names)
m.FeasibleSet = pyo.Set(
    initialize=[
        (i, j, k)
        for i, j, k in product(m.N, m.T, m.T)
        if treat_cube[dfa[dfa.fid == i].index[0], treat_names.index(j), treat_names.index(k)]
    ]
)

# Params
m.area = pyo.Param(m.N, within=pyo.Reals, initialize=dfa.set_index("fid")["area"].to_dict())
m.current_value = pyo.Param(m.N, within=pyo.Reals, initialize=dfa.set_index("fid")["value"].to_dict())
m.current_valuem2 = pyo.Param(m.N, within=pyo.Reals, initialize=dfa.set_index("fid")["value/m2"].to_dict())
m.target_value = pyo.Param(
    m.N, m.T, within=pyo.Reals, initialize=dft.set_index(["fid", "treatment"])["value"].to_dict()
)
m.target_valuem2 = pyo.Param(
    m.N, m.T, within=pyo.Reals, initialize=dft.set_index(["fid", "treatment"])["value/m2"].to_dict()
)
m.cost = pyo.Param(m.N, m.T, within=pyo.Reals, initialize=dft.set_index(["fid", "treatment"])["cost"].to_dict())
m.costm2 = pyo.Param(m.N, m.T, within=pyo.Reals, initialize=dft.set_index(["fid", "treatment"])["cost/m2"].to_dict())

# initialize=df_stands[treatments].stack().to_dict(),

# Variables
m.X = pyo.Var(
    m.FeasibleSet,
    within=pyo.Binary,
)
# Constraints
m.at_most_one_treatment = pyo.Constraint(
    m.N, rule=lambda m, ii: sum(m.X[i, j, k] for i, j, k in m.FeasibleSet if i == ii) <= 1
)

m.area_capacity = pyo.Constraint(rule=lambda m: sum(m.X[i, j, k] * m.area[i] for i, j, k in m.FeasibleSet) <= area)

m.budget_capacity = pyo.Constraint(
    rule=lambda m: sum(m.X[i, j, k] * (m.cost[i, k] + m.costm2[i, k] * m.area[i]) for i, j, k in m.FeasibleSet)
    <= budget
)

# Objective
m.obj = pyo.Objective(
    expr=sum(
        m.X[i, j, k] * (m.target_value[i, k] + m.target_valuem2[i, k] * m.area[i])
        + (1 - m.X[i, j, k]) * (m.current_value[i] + m.current_valuem2[i] * m.area[i])
        for i, j, k in m.FeasibleSet
    ),
    sense=pyo.maximize,
)
print("PPRINT")
print(m.pprint())

# Solve
solver = "cbc"
executable = None
if executable:
    opt = SolverFactory(solver, executable=executable)
else:
    opt = SolverFactory(solver)

options_string = None
if options_string:
    results = opt.solve(m, tee=True, options_string=options_string)
else:
    results = opt.solve(m, tee=True)

print("DISPLAY")
print(m.display())
# for i, j, k in m.AllSets:
#     print(i, j, k, pyo.value(m.X[i, j, k], exception=False))
