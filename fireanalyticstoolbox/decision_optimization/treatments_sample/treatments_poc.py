#!python3
"""
ipython

On a landscape several stands can be evaluated for different treatments; considering budgeting costs and area as constraints; Also land valuation pre-treatment as objective. The goal is to maximize the value of the choosen stand treatments.

- Stands can be treated with one of several feasible treatments.
-- Each stand has an area, a current treatment, a fixed cost if a change is made, a current value and values under target treatments
- Treatments have per-area costs.
"""
import string
from itertools import product

import numpy as np
import pandas as pd
from pyomo import environ as pyo
from pyomo.common.errors import ApplicationError
from pyomo.opt import SolverFactory, SolverStatus, TerminationCondition

# sets
num_treatments = 5
treatments = ["".join(np.random.choice(list(string.ascii_uppercase), size=3)) for _ in range(num_treatments)]
treatments
treat_cost = np.random.rand(num_treatments, num_treatments)
treat_cost[np.diag_indices(num_treatments)] = 0  # tril_indices triangular lower
treat_cost

## polygons : area, actual_treatment, actual_value
num_stands = 10
df_stands = pd.DataFrame.from_dict({trtmnt: np.random.rand(num_stands) * 1000 for trtmnt in treatments})
df_stands["area"] = np.random.rand(num_stands) * 10
df_stands["actual_treatment"] = np.random.choice(treatments, size=num_stands)
df_stands["actual_value"] = df_stands.apply(lambda x: x[x["actual_treatment"]], axis=1)
df_stands["fixed_cost"] = np.random.rand(num_stands) * 10
df_stands

## budget
budget = (
    (df_stands["fixed_cost"].mean() + treat_cost[~np.eye(num_treatments, dtype=bool)].mean() * df_stands["area"].mean())
    * num_treatments
    * 0.618
)
budget
## area
area = df_stands["area"].mean() * num_stands * 0.618
area

treat_isfeasible = np.random.randint(2, size=(num_stands, num_treatments, num_treatments))
treat_isfeasible[:, np.eye(num_treatments, dtype=bool)] = 0
# assert every stand has a feasible treatment
assert np.all(treat_isfeasible.sum(axis=1).sum(axis=1) > 0)
# TODO actual treatment should be considering calculating this

# Mixed Integer Linear Programming
m = pyo.ConcreteModel(name="treatment")
# Sets
m.S = pyo.Set(initialize=range(num_stands))
m.T = pyo.Set(initialize=treatments)
m.NonDiagonal = pyo.Set(initialize=[(j, k) for j, k in product(m.T, m.T) if j != k])

# scalar params
m.Budget = pyo.Param(initialize=budget)
m.Area = pyo.Param(initialize=area)

# 1d params
m.fixed_cost = pyo.Param(m.S, within=pyo.Reals, initialize=df_stands["fixed_cost"].to_dict())
m.area = pyo.Param(m.S, within=pyo.Reals, initialize=df_stands["area"].to_dict())
m.actual_treatment = pyo.Param(m.S, within=m.T, initialize=df_stands["actual_treatment"].to_dict())
m.actual_value = pyo.Param(m.S, within=pyo.Reals, initialize=df_stands["actual_value"].to_dict())


# 2d params
m.target_value = pyo.Param(
    m.S,
    m.T,
    within=pyo.Reals,
    initialize=df_stands[treatments].stack().to_dict(),
)
m.treat_cost = pyo.Param(
    m.T,
    m.T,
    within=pyo.Reals,
    initialize={(treatments[j], treatments[k]): v for (j, k), v in np.ndenumerate(treat_cost) if j != k},
)

# 3d params
m.feasible = pyo.Param(
    m.S,
    m.T,
    m.T,
    within=pyo.Binary,
    initialize={(i, treatments[j], treatments[k]): v for (i, j, k), v in np.ndenumerate(treat_isfeasible) if j != k},
)

# derived set
m.AllSets = pyo.Set(
    initialize=[
        (i, j, k)
        for i, (j, k) in product(m.S, m.NonDiagonal)
        if m.feasible[i, j, k] == 1 and m.actual_treatment[i] == j
    ]
)

# Variables
m.X = pyo.Var(
    m.AllSets,
    within=pyo.Binary,
    bounds={(i, j, k): (0, m.feasible[i, j, k]) for i, j, k in m.AllSets},
)


# EQUIVALENTE
# A
def at_most_one_treatment_rule(m, ii):
    return sum(m.X[i, j, k] for i, j, k in m.AllSets if m.feasible[i, j, k] == 1 and i == ii) <= 1


m.at_most_one_treatment = pyo.Constraint(m.S, rule=at_most_one_treatment_rule)
# B
"""
m.at_most_one_treatment = pyo.ConstraintList()
for i in m.S:
    m.at_most_one_treatment.add(
        sum(m.X[i, j, k] for ii, j, k in m.AllSets if m.feasible[i, j, k] == 1 and i == ii) <= 1
    )
"""


m.area_capacity = pyo.Constraint(rule=lambda m: sum(m.X[i, j, k] * m.area[i] for i, j, k in m.AllSets) <= m.Area)

m.budget_capacity = pyo.Constraint(
    rule=lambda m: sum(m.X[i, j, k] * (m.fixed_cost[i] + m.treat_cost[j, k] * m.area[i]) for i, j, k in m.AllSets)
    <= m.Budget
)

# Objective
m.obj = pyo.Objective(
    expr=sum(m.X[i, j, k] * (m.target_value[i, k] - m.actual_value[i]) for i, j, k in m.AllSets),
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
