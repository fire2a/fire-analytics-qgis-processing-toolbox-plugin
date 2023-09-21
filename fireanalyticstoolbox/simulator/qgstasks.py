import random
from time import sleep

from qgis.core import (Qgis, QgsApplication, QgsMessageLog,
                       QgsProcessingException, QgsTask)

MESSAGE_CATEGORY = "Fire Analytics bkgdtsks"


class MyQgsTask(QgsTask):
    def __init__(self, description, context, feedback):
        super().__init__(description, QgsTask.CanCancel)
        self.exception = None
        self.context = context
        self.feedback = feedback

    def finished(self, result, funcok=None, funcfail=None):
        if result:
            self.feedback.pushInfo(f"Task: {self.description()} finished")
            if funcok:
                funcok()
        else:
            if self.exception is None:
                self.feedback.pushWarning(f"Task: {self.description()} not successful but without exception")
            else:
                self.feedback.reportError(f"Task: {self.description()} exception: {self.exception}")
                if funcfail:
                    funcfail()
                if self.exception != "canceled":
                    raise QgsProcessingException(self.tr(self.exception))

    def cancel(self):
        self.feedback.pushWarning(f"Task {self.description()} was canceled")
        super().cancel()


class StopMeTask(MyQgsTask):
    def __init__(self, *args, total=100):
        super().__init__(*args)
        self.total = total

    def run(self):
        for i in range(1, self.total + 1):
            self.setProgress(i)
            if self.isCanceled():
                self.exception = "canceled"
                return False
            sleep(0.5)
            arandominteger = random.randint(0, 500)
            if arandominteger == 42:
                self.exception = "bad value!"
                return False
            self.feedback.pushInfo(f"task: {self.description()}, i: {i}, rand: {arandominteger}")
        return True


class RandomIntegerSumTask(QgsTask):
    """This shows how to subclass QgsTask"""

    def __init__(self, description, duration):
        super().__init__(description, QgsTask.CanCancel)
        self.duration = duration
        self.total = 0
        self.iterations = 0
        self.exception = None

    def run(self):
        """Here you implement your heavy lifting.
        Should periodically test for isCanceled() to gracefully
        abort.
        This method MUST return True or False.
        Raising exceptions will crash QGIS, so we handle them
        internally and raise them in self.finished
        """
        QgsMessageLog.logMessage('Started task "{}"'.format(self.description()), MESSAGE_CATEGORY, Qgis.Info)
        wait_time = self.duration / 100
        for i in range(100):
            sleep(wait_time)
            # use setProgress to report progress
            self.setProgress(i)
            arandominteger = random.randint(0, 500)
            self.total += arandominteger
            self.iterations += 1
            # check isCanceled() to handle cancellation
            if self.isCanceled():
                return False
            # simulate exceptions to show how to abort task
            if arandominteger == 42:
                # DO NOT raise Exception('bad value!')
                # this would crash QGIS
                self.exception = Exception("bad value!")
                return False
        return True

    def finished(self, result):
        """
        This function is automatically called when the task has
        completed (successfully or not).
        You implement finished() to do whatever follow-up stuff
        should happen after the task is complete.
        finished is always called from the main thread, so it's safe
        to do GUI operations and raise Python exceptions here.
        result is the return value from self.run.
        """
        if result:
            QgsMessageLog.logMessage(
                'RandomTask "{name}" completed\nRandomTotal: {total} (with {iterations} iterations)'.format(
                    name=self.description(), total=self.total, iterations=self.iterations
                ),
                MESSAGE_CATEGORY,
                Qgis.Success,
            )
        else:
            if self.exception is None:
                QgsMessageLog.logMessage(
                    'RandomTask "{name}" not successful but without '
                    "exception (probably the task was manually "
                    "canceled by the user)".format(name=self.description()),
                    MESSAGE_CATEGORY,
                    Qgis.Warning,
                )
            else:
                QgsMessageLog.logMessage(
                    'RandomTask "{name}" Exception: {exception}'.format(
                        name=self.description(), exception=self.exception
                    ),
                    MESSAGE_CATEGORY,
                    Qgis.Critical,
                )
                raise self.exception

    def cancel(self):
        QgsMessageLog.logMessage(
            'RandomTask "{name}" was canceled'.format(name=self.description()), MESSAGE_CATEGORY, Qgis.Info
        )
        super().cancel()


if __name__ == "__main__":
    longtask = RandomIntegerSumTask("waste cpu long", 20)
    shorttask = RandomIntegerSumTask("waste cpu short", 10)
    minitask = RandomIntegerSumTask("waste cpu mini", 5)
    shortsubtask = RandomIntegerSumTask("waste cpu subtask short", 5)
    longsubtask = RandomIntegerSumTask("waste cpu subtask long", 10)
    shortestsubtask = RandomIntegerSumTask("waste cpu subtask shortest", 4)

    # Add a subtask (shortsubtask) to shorttask that must run after
    # minitask and longtask has finished
    shorttask.addSubTask(shortsubtask, [minitask, longtask])
    # Add a subtask (longsubtask) to longtask that must be run
    # before the parent task
    longtask.addSubTask(longsubtask, [], QgsTask.ParentDependsOnSubTask)
    # Add a subtask (shortestsubtask) to longtask
    longtask.addSubTask(shortestsubtask)

    QgsApplication.taskManager().addTask(longtask)
    QgsApplication.taskManager().addTask(shorttask)
    QgsApplication.taskManager().addTask(minitask)
