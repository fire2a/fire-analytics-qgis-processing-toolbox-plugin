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
from re import compile as re_compile
from re import sub as re_sub
from shutil import which

from pyomo.common.errors import ApplicationError
from pyomo.opt import SolverFactory, SolverManagerFactory, SolverStatus, TerminationCondition

from ..config import TAG

one_or_more_newlines = re_compile(r"\n+")

if platform_system() == "Windows":
    SOLVER = {"cbc": "ratioGap=0.005 seconds=300"}
else:
    SOLVER = {"cbc": f"ratioGap=0.005 seconds=300 threads={cpu_count() - 1}"}

SOLVER.update(
    {
        "glpk": "mipgap=0.005 tmlim=300",
        "ipopt": "",
        "gurobi": "MIPGap=0.005 TimeLimit=300",
        "cplex": "mipgap=0.005 timelimit=300",
        # "cplex_direct": "mipgap=0.005 timelimit=300",
        # "cplex_persistent": "mipgap=0.005 timelimit=300", needs tweak opt.set_ to work
    }
)
NEOS_SOLVER = [
    "bonmin",
    "cbc",
    "conopt",
    "couenne",
    "cplex",
    "filmint",
    "filter",
    "ipopt",
    "knitro",
    "l-bfgs-b",
    "lancelot",
    "lgo",
    "loqo",
    "minlp",
    "minos",
    "minto",
    "mosek",
    "octeract",
    "ooqp",
    "path",
    "raposa",
    "snopt",
]
 


def init_ndarray(data, model, *args):
    """Function to initialize a pyomo element with a numpy ndarray with the same shape as data
    Args:
        data: numpy ndarray
        model: pyomo model
        args: pyomo indices
    Returns:
        callable pyomo initializer

    sample usage:
        from functools import partial
        arr = np.random.rand(3, 4)
        model = ConcreteModel()
        model.A = Set(initialize=range(3))
        model.B = Set(initialize=range(4))
        model.Pa = Param(model.A, model.B, initialize=partial(init_ndarray, data))
    """
    # print(f"{data.shape=}, {args=}")
    return data[args]


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
        except (ApplicationError, NameError, ImportError):
            solvers_filter.append(False)
    pyomo_solvers_list = list(compress(pyomo_solvers_list, solvers_filter))
    return pyomo_solvers_list


def qml_print(msg, qgs_message_log=None):
    # qml_print = lambda x, y: y.logMessage(x, TAG) if qgs_message_log else print(x)
    if qgs_message_log:
        # from qgis.core import QgsMessageLog
        # QgsMessageLog().logMessage(msg, TAG)
        qgs_message_log().logMessage(msg, TAG)
    else:
        print(msg)

def add_cbc_to_path(qgs_message_log=None):
    """Add cbc to path if it is not already there"""
    if cbc := which("cbc.exe"):
        qml_print(f"ready {cbc=}", qgs_message_log)
        return
    if "__file__" in globals():
        cbc = Path(__file__).parents[1] / "cbc" / "bin" / "cbc.exe"
        if cbc.is_file():
            environ["PATH"] += pathsep + str(cbc.parent)
        else:
            qml_print(f"file not found! {cbc=}", qgs_message_log)
    if cbc := which("cbc.exe"):
        qml_print(f"available in path {cbc=}", qgs_message_log)
        return
    qml_print("CBC SOLVER NOT available in path", qgs_message_log)

def add_cplex_to_path(qgs_message_log=None):
    if cplex:= which("cplex.exe"):
        qml_print(f"ready {cplex=}", qgs_message_log)
        return
    try: 
        programfiles = Path(environ.get('programfiles'))
        if cplexstudio := sorted((programfiles / "IBM"/ "ILOG").glob("CPLEX*")):
            cplexstudio = cplexstudio[-1]
            for apath in ["opl/bin/x64_win64","opl/oplide","cplex/bin/x64_win64","cpoptimizer/bin/x64_win64"]:
                bpath = cplexstudio / apath
                if bpath.is_dir():
                    environ["PATH"] += pathsep + str(bpath)
                    qml_print(f"Added to path {bpath}", qgs_message_log)
                else:
                    qml_print(f"NOT added to path {bpath}, not a directory", qgs_message_log)
        else:
            qml_print(f"ibm ilog CPLEX SOLVER not found in {programfiles=}", qgs_message_log)
    except Exception as e:
        qml_print(f"Adding ibm ilog CPLEX error, {e}", qgs_message_log)
    if cplex:= which("cplex.exe"):
        qml_print(f"{cplex=}", qgs_message_log)
        return
    qml_print("ibm ilog CPLEX SOLVER NOT available in path", qgs_message_log)


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
        self.print(re_sub(one_or_more_newlines, "\n", super().getvalue()))
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
    DISPLAY_MODEL: display the model in the console
    """
    from qgis.core import (QgsProcessingParameterBoolean, QgsProcessingParameterDefinition, QgsProcessingParameterFile,
                           QgsProcessingParameterString)

    # boolean parameter to display the model
    qppb = QgsProcessingParameterBoolean(
        name="DISPLAY_MODEL",
        description="Display the pyomo model in the console (disabled for rasters, can easily clog & crash QGIS, use for debugging small models only!)",
        defaultValue="False",
        optional=False,
    )
    qppb.setFlags(qppb.flags() | QgsProcessingParameterDefinition.FlagAdvanced)
    self.addParameter(qppb)

    # SOLVERS
    value_hints, self.solver_exception_msg = check_solver_availability(SOLVER)
    # solver string combobox (enums
    qpps = QgsProcessingParameterString(
        name="SOLVER",
        description="============\nLOCAL SOLVER\nName: recommended options string [and executable STATUS]",
        # optional=True,
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
        description=self.tr("Override options_string (type a single space ' ' to not send any options to the solver)"),
        defaultValue="",
        optional=True,
    )
    qpps2.setFlags(qpps2.flags() | QgsProcessingParameterDefinition.FlagAdvanced)
    self.addParameter(qpps2)
    # executable file
    qppf = QgsProcessingParameterFile(
        name="EXECUTABLE",
        description=self.tr("Set solver executable file [required if status is 'MUST SET EXECUTABLE']"),
        behavior=QgsProcessingParameterFile.File,
        optional=True,
    )
    qppf.setExtension("exe" if platform_system() == "Windows" else "")
    qppf.setFlags(qppf.flags() | QgsProcessingParameterDefinition.FlagAdvanced)
    self.addParameter(qppf)
    # NEOS
    qpps = QgsProcessingParameterString(
        name="NEOS_EMAIL",
        description="============\nNEOS CLOUD SOLVER\n(not available for Pyomo+MsWindows)\nRegistered email (visit https://neos-guide.org/)",
        defaultValue="",
        optional=True,
    )
    qpps.setFlags(qpps.flags() | QgsProcessingParameterDefinition.FlagAdvanced)
    self.addParameter(qpps)
    qpps = QgsProcessingParameterString(
        name="NEOS_SOLVER",
        description="Solver name",
        defaultValue="cplex",
        optional=True,
    )
    qpps.setMetadata(
        {
            "widget_wrapper": {
                "value_hints": NEOS_SOLVER,
            }
        }
    )
    qpps.setFlags(qpps.flags() | QgsProcessingParameterDefinition.FlagAdvanced)
    self.addParameter(qpps)
    # options_string
    qpps2 = QgsProcessingParameterString(
        name="NEOS_CUSTOM_OPTIONS_STRING",
        description=self.tr("Custom options string"),
        defaultValue="",
        optional=True,
    )
    qpps2.setFlags(qpps2.flags() | QgsProcessingParameterDefinition.FlagAdvanced)
    self.addParameter(qpps2)


def pyomo_run_model(self, parameters, context, feedback, model, display_model=None):
    """runs a pyomo model reading parameters from a QgsProcessingAlgorithm form, returns the results object
    Reserves the following variables in the algorithm:
    SOLVER: Local solver name and options
    EXECUTABLE: path to the solver executable
    CUSTOM_OPTIONS_STRING: custom options to pass to the solver
    DISPLAY_MODEL: display the model in the console
    NEOS_SOLVER: solver for NEOS server
    NEOS_EMAIL: email for NEOS server
    NEOS_CUSTOM_OPTIONS_STRING: custom options to pass to the NEOS server
    """
    executable = self.parameterAsString(parameters, "EXECUTABLE", context)
    # feedback.pushDebugInfo(f"exesolver_string:{executable}")

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

    # neos
    if neos_email := self.parameterAsString(parameters, "NEOS_EMAIL", context):
        environ["NEOS_EMAIL"] = neos_email
        neos_solver_manager = SolverManagerFactory("neos")
        neos_solver = self.parameterAsString(parameters, "NEOS_SOLVER", context)
        neos_options_string = self.parameterAsString(parameters, "NEOS_CUSTOM_OPTIONS_STRING", context)
        feedback.pushDebugInfo(f"{neos_email=}, {neos_solver=}")
    else:
        if executable:
            opt = SolverFactory(solver, executable=executable)
            # FIXME if solver is cplex_persistent
            # opt.set_instance(model)
        else:
            opt = SolverFactory(solver)

    if display_model is None:
        display_model = self.parameterAsBool(parameters, "DISPLAY_MODEL", context)

    feedback.setProgress(33)
    feedback.setProgressText("Solver object created 33%")

    pyomo_std_feedback = FileLikeFeedback(feedback, True)
    pyomo_err_feedback = FileLikeFeedback(feedback, False)
    with redirect_stdout(pyomo_std_feedback), redirect_stderr(pyomo_err_feedback):
        if options_string:
            if neos_email:
                feedback.pushDebugInfo(f"send to neos; {solver=}, options={options_string}")
                results = neos_solver_manager.solve(
                    model, solver=neos_solver, tee=True, options_string=neos_options_string
                )
                feedback.pushDebugInfo(f"neos returned {results}")
            else:
                results = opt.solve(model, tee=True, options_string=options_string)
        else:
            if neos_email:
                feedback.pushDebugInfo("send to neos; {solver=}")
                results = neos_solver_manager.solve(model, solver=neos_solver, tee=True)
                feedback.pushDebugInfo(f"neos returned {results}")
            else:
                results = opt.solve(model, tee=True)
        # TODO
        # # Stop the algorithm if cancel button has been clicked
        # if feedback.isCanceled():
        # print("DISPLAY")
        if display_model:
            model.display()
    feedback.setProgress(90)
    feedback.setProgressText("Solver finished!")
    return results


def printf(msg, feedback=None, level=-1):
    """Utility to print messages in a QgsProcessingAlgorithm. If feedback is None, print to console.
    Args:
        msg string: message to print
        feedback: QgsProcessingFeedback object
        level int:  -1 debug, 0 info, 1 warning, 2 error
    """
    if feedback:
        if level == -1:
            feedback.pushDebugInfo(msg)
        elif level == 0:
            feedback.pushConsoleInfo(msg)
        elif level == 1:
            feedback.pushWarning(msg)
        elif level >= 2:
            feedback.reportError(msg)
        if feedback.isCanceled():
            from qgis.core import QgsProcessingException

            raise QgsProcessingException("Algorithm cancelled by user")
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

    if status in [SolverStatus.error, SolverStatus.aborted, SolverStatus.unknown] and termination_condition not in [
        TerminationCondition.intermediateNonInteger,
        TerminationCondition.maxTimeLimit,
        TerminationCondition.maxIterations,
    ]:
        msg += "No solution found! Maybe solver or user error?\n"
        retval = 2
        printf(msg, feedback, level=retval)
        return retval, retdic

    if termination_condition in [
        TerminationCondition.infeasibleOrUnbounded,
        TerminationCondition.infeasible,
        TerminationCondition.unbounded,
    ]:
        msg += f"Optimization is {termination_condition}. No solution found! Check instance data coherence!\n"
        retval = 3
        printf(msg, feedback, level=retval)
        return retval, retdic

    if not termination_condition == TerminationCondition.optimal:
        msg += (
            "Non-optimal solution found! Check the [mip|ratio|tolerance]gap that estimates how far the solution is from"
            " the optimal one!\nTweak solver options or simplify the instance to get better results!\n"
        )
        retval = 1
        printf(msg, feedback, retval)
        return retval, retdic
    printf(msg + "good enough", feedback, level=retval)
    return retval, retdic


def simplest_pyomo_solve(model):
    """
    model=m
    """
    print("PPRINT")
    print(model.pprint())

    # Solve
    solver = "gurobi"  # cbc
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

    """
    from pickle import dump, load
    dump(results, open('results.pickle','wb'))
    results = load(open('results.pickle','rb'))
    """

    print("DISPLAY")
    print(model.display())
    return model
