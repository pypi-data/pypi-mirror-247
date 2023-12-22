import sys
from PyQt5 import QtWidgets


def create_exceptions_hook(window):
    def exceptions_hook(exception_type, value, traceback):
        QtWidgets.QMessageBox.critical(
            window, "CRITICAL ERROR", str(value),
            QtWidgets.QMessageBox.Cancel
        )

        sys.__excepthook__(exception_type, value, traceback)
    return exceptions_hook
