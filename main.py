# View Utilities
from PyQt5 import QtCore, QtGui, QtWidgets
import qdarkstyle

from app.pd_view_model import ViewModel

# General Dependencies
import sys

# Application Entry Point
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())

    ui = ViewModel()
    ui.show()

    sys.exit(app.exec_())
