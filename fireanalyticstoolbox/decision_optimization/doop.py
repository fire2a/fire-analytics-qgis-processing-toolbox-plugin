#!python3
"""
decision optimization helpers
"""
from contextlib import redirect_stderr, redirect_stdout
from io import StringIO
from multiprocessing import cpu_count
from os import environ, pathsep
from pathlib import Path
from platform import system as platform_system
from re import compile, sub
from shutil import which

import pyomo.environ
from pyomo.common.errors import ApplicationError
from pyomo.opt import SolverFactory, SolverStatus, TerminationCondition
from qgis.core import QgsMessageLog

from ..config import TAG

one_or_more_newlines = compile(r"\n+")

SOLVER = {
    "cbc": f"ratioGap=0.005 seconds=300 threads={cpu_count() - 1}",
    "glpk": "mipgap=0.005 tmlim=300",
    "ipopt": "",
    "gurobi": "MIPGap=0.005 TimeLimit=300",
    "cplex_direct": "mipgap=0.005 timelimit=300",
    # "cplex_persistent": "mipgap=0.005 timelimit=300", needs tweak opt.set_ to work
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
    """taken from pyomo source code"""
    from itertools import compress

    from pyomo import environ as pyo

    pyomo_solvers_list = pyo.SolverFactory.__dict__["_cls"].keys()
    solvers_filter = []
    for s in pyomo_solvers_list:
        try:
            solvers_filter.append(pyo.SolverFactory(s).available())
        except (ApplicationError, NameError, ImportError) as e:
            solvers_filter.append(False)
    pyomo_solvers_list = list(compress(pyomo_solvers_list, solvers_filter))
    return pyomo_solvers_list


def add_cbc_to_path(qgs_message_log=None):
    """Add cbc to path if it is not already there"""
    from qgis.core import QgsMessageLog

    qml_print = lambda x, y: QgsMessageLog.logMessage(x, TAG) if qgs_message_log else print(x)

    if which_cbc := which("cbc.exe"):
        qml_print(f"cbc.exe already in {which_cbc=}", qgs_message_log)
        return True
    if which("cbc.exe") is None and "__file__" in globals():
        cbc_exe = Path(__file__).parents[1] / "cbc" / "bin" / "cbc.exe"
        if cbc_exe.is_file():
            environ["PATH"] += pathsep + str(cbc_exe.parent)
            qml_print(f"Added {cbc_exe.parent=} to path", qgs_message_log)
            return True
        else:
            qml_print(f"{cbc_exe} file not found!", qgs_message_log)
    qml_print("add_cbc_to_path: nothing done", qgs_message_log)
    return False


class FileLikeFeedback(StringIO):
    """File-like object to redirect stdout and stderr to QgsProcessingFeedback use with context manager to capture output from pyomo messages"""

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
        # msg = self.getvalue()
        # QgsMessageLog().logMessage(f"{type(msg)=}", TAG)
        self.print(sub(one_or_more_newlines, "\n", super().getvalue()))
        # self.print(msg)
        # self.print(super().getvalue())
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


def pyomo_init_algorithm(self, config):
    """sets the pyomo algorithm parameters
    Reserves the following variables in the algorithm:
    SOLVER: solver name and options
    EXECUTABLE: path to the solver executable
    CUSTOM_OPTIONS_STRING: custom options to pass to the solver
    """
    from qgis.core import QgsProcessingParameterDefinition, QgsProcessingParameterFile, QgsProcessingParameterString

    # SOLVERS
    value_hints, self.solver_exception_msg = check_solver_availability(SOLVER)
    # solver string combobox (enums
    qpps = QgsProcessingParameterString(
        name="SOLVER",
        description="Solver: recommended options string [and executable STATUS]",
    )
    qpps.setMetadata(
        {
            "widget_wrapper": {
                "value_hints": value_hints,
                "setEditable": True,  # not working
            }
        }
    )
    qpps.setFlags(qpps.flags() | QgsProcessingParameterDefinition.FlagAdvanced)
    self.addParameter(qpps)
    # options_string
    qpps2 = QgsProcessingParameterString(
        name="CUSTOM_OPTIONS_STRING",
        description="Override options_string (type a single space ' ' to not send any options to the solver)",
        defaultValue="",
        optional=True,
    )
    qpps2.setFlags(qpps2.flags() | QgsProcessingParameterDefinition.FlagAdvanced)
    self.addParameter(qpps2)
    # executable file
    qppf = QgsProcessingParameterFile(
        name="EXECUTABLE",
        description=self.tr("Set solver executable file [REQUIRED if STATUS]"),
        behavior=QgsProcessingParameterFile.File,
        extension="exe" if platform_system() == "Windows" else "",
        optional=True,
    )
    qppf.setFlags(qppf.flags() | QgsProcessingParameterDefinition.FlagAdvanced)
    self.addParameter(qppf)


def pyomo_run_model(self, parameters, context, feedback, model, display_model=True):
    """runs a pyomo model reading parameters from a QgsProcessingAlgorithm form, returns the results object
    Reserves the following variables in the algorithm:
    SOLVER: solver name and options
    EXECUTABLE: path to the solver executable
    CUSTOM_OPTIONS_STRING: custom options to pass to the solver
    """
    executable = self.parameterAsString(parameters, "EXECUTABLE", context)
    feedback.pushDebugInfo(f"exesolver_string:{executable}")

    solver_string = self.parameterAsString(parameters, "SOLVER", context)
    # feedback.pushDebugInfo(f"solver_string:{solver_string}")

    solver_string = solver_string.replace(" MUST SET EXECUTABLE", "")

    solver, options_string = solver_string.split(": ", 1) if ": " in solver_string else (solver_string, "")
    # feedback.pushDebugInfo(f"solver:{solver}, options_string:{options_string}")

    if len(custom_options := self.parameterAsString(parameters, "CUSTOM_OPTIONS_STRING", context)) > 0:
        if custom_options == " ":
            options_string = None
        else:
            options_string = custom_options
    feedback.pushDebugInfo(f"options_string: {options_string}\n")

    if executable:
        opt = SolverFactory(solver, executable=executable)
        # FIXME if solver is cplex_persistent
        # opt.set_instance(model)
    else:
        opt = SolverFactory(solver)

    feedback.setProgress(20)
    feedback.setProgressText("pyomo model built, solver object created 20%")

    pyomo_std_feedback = FileLikeFeedback(feedback, True)
    pyomo_err_feedback = FileLikeFeedback(feedback, False)
    with redirect_stdout(pyomo_std_feedback), redirect_stderr(pyomo_err_feedback):
        if options_string:
            results = opt.solve(model, tee=True, options_string=options_string)
        else:
            results = opt.solve(model, tee=True)
        # TODO
        # # Stop the algorithm if cancel button has been clicked
        # if feedback.isCanceled():
        # print("DISPLAY")
        if display_model:
            model.display()
    return results


def feed_print(feedback, msg, level=0):
    if feedback:
        if level == 0:
            feedback.pushConsoleInfo(msg)
        elif level == 1:
            feedback.pushWarning(msg)
        elif level >= 2:
            feedback.reportError(msg)
    else:
        print(msg)


def pyomo_parse_results(results, feedback=None):
    """Parse the results of a Pyomo optimization problem. Returns a tuple with the return code and a dictionary with the solver status and termination condition

    Args:
        results: Pyomo results object
        feedback[optional]: QgsProcessingFeedback object to print messages in a QgsProcessingAlgorithm, else just print(message)

    Returns:
        tuple: (return code, dict)
            return codes:
                    0: optimal solution found
                    1: non optimal solution found
                    2: solver problem: error, aborted or unknown solver status
                    3: instance problem: infeasible or unbounded
            dict:
                SOLVER_STATUS: Solver status
                SOLVER_TERMINATION_CONDITION: Solver termination condition
    """
    status = results.solver.status
    termination_condition = results.solver.termination_condition
    retdic = {"SOLVER_STATUS": status, "SOLVER_TERMINATION_CONDITION": termination_condition}
    msg = f"Solver {status=} and {termination_condition=}\n"
    retval = 0
    feed_print(feedback, msg, retval)

    if (
        status in [SolverStatus.error, SolverStatus.aborted, SolverStatus.unknown]
        and termination_condition != TerminationCondition.intermediateNonInteger
    ):
        msg = "No solution found! Maybe solver or user error?\n"
        retval = 2
        feed_print(feedback, msg, retval)
        return retval, retdic

    if termination_condition in [
        TerminationCondition.infeasibleOrUnbounded,
        TerminationCondition.infeasible,
        TerminationCondition.unbounded,
    ]:
        msg = f"Optimization is {termination_condition}. No solution found! Check instance data coherence!\n"
        retval = 3
        feed_print(feedback, msg, retval)
        return retval, retdic

    if not termination_condition == TerminationCondition.optimal:
        msg = "Non-optimal solution found! Check the [mip|ratio|tolerance]gap that estimates how far the solution is from the optimal one!\nTweak solver options or simplify the instance to get better results!\n"
        retval = 1
        feed_print(feedback, msg, retval)
        return retval, retdic
    # TODO are there more cases?
    return retval, retdic


def simplest_pyomo_solve(model):
    print("PPRINT")
    print(model.pprint())

    # Solve
    solver = "cbc"
    executable = None
    if executable:
        opt = SolverFactory(solver, executable=executable)
    else:
        opt = SolverFactory(solver)

    options_string = None
    if options_string:
        results = opt.solve(model, tee=True, options_string=options_string)
    else:
        results = opt.solve(model, tee=True)

    print("DISPLAY")
    print(model.display())
    return model
