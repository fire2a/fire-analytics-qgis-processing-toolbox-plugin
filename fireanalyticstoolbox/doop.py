#!python3
"""
decision optimization helpers
"""


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
