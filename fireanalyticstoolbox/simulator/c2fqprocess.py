from qgis.core import Qgis, QgsMessageLog
from qgis.PyQt.QtCore import QProcess

# exitCode()
ExitStatus = {
    QProcess.NormalExit: "NormalExit",  # 0
    QProcess.CrashExit: "CrashExit",  # 1
}
# state()
ProcessState = {
    QProcess.NotRunning: "NotRunning",  # 0
    QProcess.Starting: "Running",  # 1
    QProcess.Running: "Starting",  # 2
}
# error()
ProcessError = {
    QProcess.FailedToStart: "FailedToStart",  # 0
    QProcess.Crashed: "Crashed",  # 1
    QProcess.Timedout: "Timedout",  # 2
    QProcess.ReadError: "ReadError",  # 3
    QProcess.WriteError: "WriteError",  # 4
    QProcess.UnknownError: "UnknownError",  # 5
}


def nlog(*args, **kwargs):
    QgsMessageLog.logMessage(f"{args} {kwargs}", "Cell2FireQProcess", Qgis.Info)


class C2F(QProcess):
    """fire simulation qprocess calls the c2fsb repo main.py"""

    def __init__(self, parent=None, proc_dir=None, on_finished=None, feedback=None, log_file=None):
        super().__init__(parent)
        self.setInputChannelMode(QProcess.ForwardedInputChannel)
        self.setProcessChannelMode(QProcess.SeparateChannels)
        self.readyReadStandardOutput.connect(self.read_standard_output)
        self.readyReadStandardError.connect(self.read_standard_error)
        self.stateChanged.connect(self.on_state_changed)
        if proc_dir:
            self.setWorkingDirectory(str(proc_dir))
            self.proc_dir = proc_dir
        else:
            self.proc_dir = None
        self.finished.connect(self.on_finished)
        self.after = on_finished
        self.feedback = feedback
        self.started = None
        self.ended = None
        self.state_code = None
        self.error_code = None
        self.exit_code = None
        self.log_file = open(log_file, "w") 
        self.log_stat("init")

    def log_stat(self, msg):
        self.state_code = self.state()
        self.error_code = self.error()
        self.exit_code = self.exitCode()
        nlog(
            title="simulation",
            text="log_stat",
            msg=msg,
            started=self.started,
            ended=self.ended,
            state=ProcessState.get(self.state_code, "!Unknown"),
            error=ProcessError.get(self.error_code, "!Unknown"),
            exit_code=ExitStatus.get(self.exit_code, "!Unknown"),
        )
        # TODO make the nlog kwargs a dict and log_file them
        # self.log_file.write('log_stat: ' + msg + '\n')

    def append_message(self, msg, stderr=False):
        if stderr:
            self.feedback.pushWarning(msg)
        else:
            self.feedback.pushConsoleInfo(msg)
        self.log_file.write(msg + "\n")

    def start(self, cmd, proc_dir=None):
        self.log_stat("start INI")
        if not self.ended:
            if self.state_code in (QProcess.ProcessState.Running, QProcess.ProcessState.Starting):
                nlog(
                    "Can't start simulation, process already running",
                    title="simulation",
                    text="start",
                    level=Qgis.Warning,
                )
                return
        if proc_dir:
            self.setWorkingDirectory(str(proc_dir))
            self.proc_dir = proc_dir
        self.append_message(f"== process working directory {self.proc_dir}")
        self.append_message(f"== process command {cmd}")
        super().start(cmd)
        self.started = True
        self.ended = False
        self.log_stat("start END")

    def terminate(self):
        self.log_stat("terminate")
        if self.state_code != QProcess.ProcessState.NotRunning:
            super().terminate()
            nlog(
                "Terminate signal sent!",
                title="simulation",
                text="terminate",
                level=Qgis.Success,
            )
        else:
            nlog(
                "Can't send terminate signal!",
                title="simulation",
                text="terminate",
                current_state=ProcessState.get(self.state_code, "!Unknown"),
                ended=self.ended,
                level=Qgis.Warning,
            )

    def kill(self):
        self.log_stat("kill")
        if self.state_code != QProcess.ProcessState.NotRunning:
            super().kill()
            nlog(
                "Kill signal sent!",
                title="simulation",
                text="kill",
                level=Qgis.Success,
            )
        else:
            nlog(
                "Can't send kill signal!",
                title="simulation",
                text="kill",
                current_state=ProcessState.get(self.state_code, "!Unknown"),
                ended=self.ended,
                level=Qgis.Warning,
            )

    def on_finished(self):
        self.ended = True
        self.log_stat("on_finished")
        self.log_file.close()
        ok = False
        if self.exit_code == QProcess.NormalExit:
            level = Qgis.Success
            msg = ""
            ok = True
        elif self.exit_code == QProcess.CrashExit:
            level = Qgis.Warning
            msg = f', error:{ProcessError.get(self.error_code, "!Unknown")}'
        else:
            level = Qgis.Critical
            msg = f", code:{self.exit_code}"
            msg += f', error:{ProcessError.get(self.error_code, "!Unknown")}'
        nlog(
            title="simulation",
            text="on_finished",
            level=level,
            exit_status=ExitStatus.get(self.exit_code, "!Unknown"),
            msg=msg,
            to_bar=True,
        )
        if ok and self.after:
            self.after()

    def read_standard_output(self):
        data = self.readAllStandardOutput()
        stdout = bytes(data).decode("utf8")
        if stdout != "":
            # self.log_file.write(stdout)
            self.append_message(stdout)

    def read_standard_error(self):
        data = self.readAllStandardError()
        stderr = bytes(data).decode("utf8")
        if stderr != "":
            # self.log_file.write(stderr)
            self.append_message(stderr, stderr=True)

    def on_state_changed(self, state):
        msg = ProcessState.get(state, "!Unknown")
        self.log_stat("on_state_changed")
        self.append_message(f"== process state changed : {msg}")
