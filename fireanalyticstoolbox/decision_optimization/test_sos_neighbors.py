#!python3
from itertools import product

import numpy as np
from pyomo import environ as pyo
from pyomo.common.errors import ApplicationError
from pyomo.opt import SolverFactory, SolverStatus, TerminationCondition

# from doop import (FileLikeFeedback, add_cbc_to_path, pyomo_init_algorithm, pyomo_parse_results, pyomo_run_model)

np.random.seed(0)
N = 10
value_data = np.random.randint(1, 10, N)
weight_data = np.random.randint(1, 10, N)
capacity = weight_data.sum() * 0.618

H, W = 50, 60
value_data2d = np.random.randint(1, 10, size=(H, W))
weight_data2d = np.random.randint(1, 5, size=(H, W))
capacity2d = weight_data.sum() * 0.3618


def do_knapsack_2nb():
    """knapsack 2 neighbors"""
    N = len(value_data)
    m = pyo.ConcreteModel()
    m.N = pyo.RangeSet(0, N - 1)
    m.C = pyo.RangeSet(1, N - 2)

    m.Cap = pyo.Param(initialize=capacity)
    m.We = pyo.Param(m.N, within=pyo.Reals, initialize=weight_data)
    m.Va = pyo.Param(m.N, within=pyo.Reals, initialize=value_data)
    m.X = pyo.Var(m.N, within=pyo.Binary)
    m.Y = pyo.Var(m.N, within=pyo.Binary)

    m.objective = pyo.Objective(
        sense=pyo.maximize, expr=lambda m: sum((m.X[i] * 1.1 + 0.9 * m.Y[i]) * m.Va[i] for i in m.N)
    )

    m.sos_at_most_one = pyo.SOSConstraint(m.N, sos=1, rule=lambda m, i: [m.X[i], m.Y[i]])

    m.neighbors = pyo.Constraint(m.C, rule=lambda m, i: m.X[i] <= m.Y[i - 1] + m.Y[i + 1])
    m.neighbor0 = pyo.Constraint(rule=lambda m: m.X[0] <= m.Y[1])
    m.neighborN = pyo.Constraint(rule=lambda m: m.X[N - 1] <= m.Y[N - 2])

    m.capacity = pyo.Constraint(rule=lambda m: sum((m.X[i] + m.Y[i]) * m.We[i] for i in m.N) <= m.Cap)
    return m


def do_knapsack_4nb():
    """knapsack 4 neighbors"""
    N = len(value_data)
    m = pyo.ConcreteModel()
    m.N = pyo.RangeSet(0, N - 1)
    m.C = pyo.RangeSet(2, N - 3)

    m.Cap = pyo.Param(initialize=capacity)
    m.We = pyo.Param(m.N, within=pyo.Reals, initialize=weight_data)
    m.Va = pyo.Param(m.N, within=pyo.Reals, initialize=value_data)
    m.X = pyo.Var(m.N, within=pyo.Binary)
    m.Y = pyo.Var(m.N, within=pyo.Binary)

    m.objective = pyo.Objective(
        sense=pyo.maximize, expr=lambda m: sum((m.X[i] * 1.1 + 0.9 * m.Y[i]) * m.Va[i] for i in m.N)
    )

    m.sos_at_most_one = pyo.SOSConstraint(m.N, sos=1, rule=lambda m, i: [m.X[i], m.Y[i]])

    m.neighbors = pyo.Constraint(m.C, rule=lambda m, i: m.X[i] <= sum(m.Y[i + j] for j in range(-2, 3) if i != j))
    m.neighbor0 = pyo.Constraint(rule=lambda m: m.X[0] <= m.Y[1] + m.Y[2])
    m.neighborN2 = pyo.Constraint(rule=lambda m: m.X[N - 1] <= m.Y[N - 2] + m.Y[N - 3])

    m.capacity = pyo.Constraint(rule=lambda m: sum((m.X[i] + m.Y[i]) * m.We[i] for i in m.N) <= m.Cap)
    return m


def do_2d_knapsack_nb(nb=1, wx=1, wy=1, wnb=1):
    """knapsack 2 neighbors"""
    m = pyo.ConcreteModel("2d knapsack neighbors")
    m.H = pyo.RangeSet(0, H - 1)
    m.W = pyo.RangeSet(0, W - 1)
    m.Map = pyo.Set(initialize=m.H * m.W)
    m.MapC = pyo.Set(initialize=[(h, w) for h, w in product(m.H, m.W) if h > 0 and w > 0 and h < H - 1 and w < W - 1])

    m.num_nb = pyo.Param(initialize=nb)
    # m.num_nb = pyo.Param(initialize=nb, mutable=True)

    m.Cap = pyo.Param(initialize=capacity2d)
    m.We = pyo.Param(m.Map, within=pyo.Reals, initialize=dict(np.ndenumerate(weight_data2d)))
    m.Va = pyo.Param(m.Map, within=pyo.Reals, initialize=dict(np.ndenumerate(value_data2d)))
    m.X = pyo.Var(m.Map, within=pyo.Binary)
    m.Y = pyo.Var(m.Map, within=pyo.Binary)
    m.NB = pyo.Var(m.Map, within=pyo.Reals, bounds=(0.0, 10.0))

    m.objective = pyo.Objective(
        sense=pyo.maximize,
        expr=lambda m: sum((wx * m.X[i] + wy * m.Y[i] - wnb * m.NB[i] / max(1,m.num_nb)) * m.Va[i] for i in m.Map),
    )

    m.sos_at_most_one = pyo.SOSConstraint(m.Map, sos=1, rule=lambda m, h, w: [m.X[h, w], m.Y[h, w]])

    m.neighbors = pyo.Constraint(
        m.MapC,
        rule=lambda m, h, w: (
            0,
            m.X[h, w] * m.num_nb
            - sum(m.Y[h + i, w + j] for i, j in product(range(-1, 2), range(-1, 2)) if (i, j) != (0, 0))
            - m.NB[h, w],
            0,
        ),
    )

    # fmt: off
    m.neighborS = pyo.Constraint(m.W - {0, W-1}, rule=lambda m, w: (0, m.X[0  , w  ] * min(3,m.num_nb) - sum(m.Y[1  , w+i] for i in range(-1, 2)) - m.NB[0  , w  ], 0))
    m.neighborN = pyo.Constraint(m.W - {0, W-1}, rule=lambda m, w: (0, m.X[H-1, w  ] * min(3,m.num_nb) - sum(m.Y[H-2, w+i] for i in range(-1, 2)) - m.NB[H-1, w  ], 0))
    m.neighborW = pyo.Constraint(m.H - {0, H-1}, rule=lambda m, h: (0, m.X[h  , 0  ] * min(3,m.num_nb) - sum(m.Y[h+i, 1  ] for i in range(-1, 2)) - m.NB[h  , 0  ], 0))
    m.neighborE = pyo.Constraint(m.H - {0, H-1}, rule=lambda m, h: (0, m.X[h  , W-1] * min(3,m.num_nb) - sum(m.Y[h+i, W-2] for i in range(-1, 2)) - m.NB[h  , W-1], 0))

    m.neighborNW = pyo.Constraint(rule=(0, m.X[0  , 0  ] * min(3,m.num_nb) - m.Y[0  , 1  ] - m.Y[1  , 0  ] - m.Y[1  , 1  ] - m.NB[0  , 1  ], 0))
    m.neighborNE = pyo.Constraint(rule=(0, m.X[0  , W-1] * min(3,m.num_nb) - m.Y[0  , W-2] - m.Y[1  , W-1] - m.Y[1  , W-2] - m.NB[0  , W-2], 0))
    m.neighborSW = pyo.Constraint(rule=(0, m.X[H-1, 0  ] * min(3,m.num_nb) - m.Y[H-2, 0  ] - m.Y[H-1, 1  ] - m.Y[H-2, 1  ] - m.NB[H-2, 0  ], 0))
    m.neighborSE = pyo.Constraint(rule=(0, m.X[H-1, W-1] * min(3,m.num_nb) - m.Y[H-2, W-1] - m.Y[H-1, W-2] - m.Y[H-2, W-2] - m.NB[H-2, W-1], 0))
    # fmt: on

    m.capacity = pyo.Constraint(rule=lambda m: sum((m.X[i] + m.Y[i]) * m.We[i] for i in m.Map) <= m.Cap)
    return m


def simplest_pyomo_solve(model, print_model=True, tee=True):
    from multiprocessing import cpu_count

    SOLVER = {
        "cbc": f"ratioGap=0.005 seconds=300 threads={cpu_count() - 1}",
        "glpk": "mipgap=0.005 tmlim=300",
        "ipopt": "",
        "gurobi": "MIPGap=0.005 TimeLimit=300",
        "cplex_direct": "mipgap=0.005 timelimit=300",
        # "cplex_persistent": "mipgap=0.005 timelimit=300", needs tweak opt.set_ to work
    }
    if print_model:
        print("MODEL")
        print(model.pprint())

    # Solve
    solver = "gurobi"
    # solver = "cbc"
    executable = None
    if executable:
        opt = SolverFactory(solver, executable=executable)
    else:
        opt = SolverFactory(solver)

    options_string = SOLVER[solver]
    if options_string:
        results = opt.solve(model, tee=tee, options_string=options_string)
    else:
        results = opt.solve(model, tee=tee)

    if print_model:
        print("DISPLAY")
        print(model.display())
    return model


def graph_results2d(m, wx, wy, wnb):
    from matplotlib import pyplot as plt

    xx = np.array([pyo.value(m.X[i], exception=False) for i in m.Map]).reshape(H, W)
    yy = np.array([pyo.value(m.Y[i], exception=False) for i in m.Map]).reshape(H, W)
    zz = np.where(xx == 1, 1, np.where(yy == 1, 2, 0))

    xsum = xx.sum()
    ysum = yy.sum()
    both = xsum + ysum
    zsum = zz.sum()

    # neighbors constraint body
    # center
    nbc = np.array([pyo.value(m.neighbors[h, w], exception=False) for h, w in m.MapC]).reshape(H - 2, W - 2)
    # center west & east
    nbw = np.array([m.neighborS[h].body() for h in m.H - {0, H - 1}]).reshape(H - 2, 1)
    nbe = np.array([m.neighborS[h].body() for h in m.H - {0, H - 1}]).reshape(H - 2, 1)
    # south & north
    nbs = [m.neighborSW.body()] + [m.neighborS[w].body() for w in m.W - {0, W - 1}] + [m.neighborSE.body()]
    nbn = [m.neighborNW.body()] + [m.neighborN[w].body() for w in m.W - {0, W - 1}] + [m.neighborNE.body()]
    # stack center
    nb = np.hstack((nbw, nbc, nbe))
    # stack north, center & south
    nb = np.vstack((nbs, nb, nbn))
    nbsum = nb.sum()

    print(f"sums x:{xsum:.1f}, y:{ysum:.1f}, both:{both:.1f}, z:{zsum:.1f}, nb:{nbsum:.1f}")

    # two axes plot
    fig, ax = plt.subplots(2, 3)
    cap = 100 * m.capacity.body() / m.capacity.upper()
    title = (
        f"knapsack2d obj:{pyo.value(m.objective):.3f}, cap{cap:.3f} nb:{m.num_nb.value}, wx:{wx}, wy:{wy}, wnb:{wnb}"
    )
    fig.suptitle(title)

    ax[0, 0].set_title("value")
    ax[1, 0].set_title("weight")
    ax[0, 1].set_title("neighbors {nbsum:.1f}")
    ax[1, 1].set_title(f"X {xsum:.1f}")
    ax[0, 2].set_title(f"Y {ysum:.1f}")
    ax[1, 2].set_title(f"both {both:.1f}")

    ax[0, 0].matshow(value_data2d)
    ax[1, 0].matshow(weight_data2d)
    ax[0, 1].matshow(nb)
    ax[1, 1].matshow(xx)
    ax[0, 2].matshow(yy)
    ax[1, 2].matshow(zz)

    title = title.replace(" ", "_").replace(":", "").replace(",", "")
    plt.savefig(title + ".png")
    # plt.clf()
    # plt.cla()
    plt.close()
    # plt.show(block=False)
    print("=============", title, "=============")


def graph_results(m):
    from matplotlib import pyplot as plt

    xx = np.array([pyo.value(m.X[i], exception=False) for i in m.N])
    yy = np.array([pyo.value(m.Y[i], exception=False) for i in m.N])
    zz = np.where(xx == 1, 1, np.where(yy == 1, 2, 0))
    data = np.stack((xx, yy, zz), axis=1).T

    # two axes plot
    fig, ax = plt.subplots(2, 1)
    ax[0].plot(value_data, color="blue")
    ax[0].plot(weight_data, color="red")
    ax[1].matshow(data, cmap="terrain")
    plt.show(block=False)


# 1d knapsack
# m = do_knapsack_4nb()
# m = do_knapsack_4nb()
# m = simplest_pyomo_solve(m)
# graph_results(m)

# 2d knapsack

# nb = 0
m = do_2d_knapsack_nb(nb=0, wx=1, wy=1, wnb=1)
m = simplest_pyomo_solve(m, print_model=False, tee=False)
graph_results2d(m, 1, 1, 1)
# nb [1, 8]
for nb, wx, wy, wnb in product(range(1, 9), [1, 10, 100], [1, 10, 100], [0.01, 1, 100]):
    if wx == wy == wnb == 1:
        print('skip 1,1,1')
        continue
    if wx == wy == wnb == 100:
        print('skip 100,100,100')
        continue
    m = do_2d_knapsack_nb(nb, wx, wy, wnb)
    m = simplest_pyomo_solve(m, print_model=False, tee=False)
    graph_results2d(m, wx, wy, wnb)

# def main():
#     m = do_knapsack(value_data, weight_data, capacity)
#     m = simplest_pyomo_solve(m)
#     graph_results(m)
#
# if __name__ == "__main__":
#     main()
