#!python3
"""
decision optimization helpers
"""
from io import StringIO
from itertools import compress
from multiprocessing import cpu_count
from os import environ, pathsep
from pathlib import Path
from platform import system as platform_system
from shutil import which

import pyomo.environ
from pyomo.opt import SolverFactory

SOLVER = {
    "cbc": f"ratioGap=0.005 seconds=300 threads={cpu_count() - 1}",
    "glpk": "mipgap=0.005 tmlim=300",
    "ipopt": "",
    "gurobi": "MIPGap=0.005 TimeLimit=300",
    "cplex_direct": "mipgap=0.005 timelimit=300",
    "cplex_persistent": "mipgap=0.005 timelimit=300",
}


def check_solver_availability(SOLVER):
    # check availability
    solver_exception_msg = ""
    solver_available = [False] * len(SOLVER)
    for i, solver in enumerate(SOLVER):
        try:
            if SolverFactory(solver).available():
                solver_available[i] = True
        except Exception as e:
            solver_exception_msg += f"solver:{solver}, problem:{e}\n"
    # prepare hints
    value_hints = []
    for i, (k, v) in enumerate(SOLVER.items()):
        if solver_available[i]:
            value_hints += [f"{k}: {v}"]
        else:
            value_hints += [f"{k}: {v} MUST SET EXECUTABLE"]
    return value_hints, solver_exception_msg


def check_solver_availabilityBASED():
    pyomo_solvers_list = pyo.SolverFactory.__dict__["_cls"].keys()
    solvers_filter = []
    for s in pyomo_solvers_list:
        try:
            solvers_filter.append(pyo.SolverFactory(s).available())
        except (ApplicationError, NameError, ImportError) as e:
            solvers_filter.append(False)
    pyomo_solvers_list = list(compress(pyomo_solvers_list, solvers_filter))
    return pyomo_solvers_list


def add_cbc_to_path():
    """Add cbc to path if it is not already there"""
    if which("cbc.exe") is None and "__file__" in globals():
        cbc_exe = Path(__file__).parent / "cbc" / "bin" / "cbc.exe"
        if cbc_exe.is_file():
            environ["PATH"] += pathsep + str(cbc_exe.parent)
            QgsMessageLog.logMessage(f"Added {cbc_exe} to path", TAG, Qgis.Info)


class FileLikeFeedback(StringIO):
    def __init__(self, feedback, std):
        super().__init__()
        if std:
            self.print = feedback.pushConsoleInfo
        else:
            self.print = feedback.pushWarning
        # self.std = std
        # self.feedback = feedback
        # self.feedback.pushDebugInfo(f"{self.std} FileLikeFeedback init")

    def write(self, msg):
        # self.feedback.pushDebugInfo(f"{self.std} FileLikeFeedback write")
        super().write(msg)
        self.flush()

    def flush(self):
        self.print(super().getvalue())
        super().__init__()
        # self.feedback.pushDebugInfo(f"{self.std} FileLikeFeedback flush")


# class FileLikeFeedback:
#     def __init__(self, feedback):
#         super().__init__()
#         self.feedback = feedback
#     def write(self, msg):
#        self.msg+=msg
#     def flush(self):
#        self.feedback.pushConsoleInfo(self.msg)
#        self.msg = ""


def parse_results(self, feedback, results):
    status = results.solver.status
    termCondition = results.solver.termination_condition
    feedback.pushConsoleInfo(f"Solver status: {status}, termination condition: {termCondition}")
    if (
        status in [SolverStatus.error, SolverStatus.aborted, SolverStatus.unknown]
        and termCondition != TerminationCondition.intermediateNonInteger
    ):
        feedback.reportError(f"Solver status: {status}, termination condition: {termCondition}")
        return {self.OUTPUT_layer: None, "SOLVER_STATUS": status, "SOLVER_TERMINATION_CONDITION": termCondition}
    if termCondition in [
        TerminationCondition.infeasibleOrUnbounded,
        TerminationCondition.infeasible,
        TerminationCondition.unbounded,
    ]:
        feedback.reportError(f"Optimization problem is {termCondition}. No output is generated.")
        return {self.OUTPUT_layer: None, "SOLVER_STATUS": status, "SOLVER_TERMINATION_CONDITION": termCondition}
    if not termCondition == TerminationCondition.optimal:
        feedback.pushWarning(
            "Output is generated for a non-optimal solution! Try running again with different solver options or"
            " tweak the layers..."
        )
