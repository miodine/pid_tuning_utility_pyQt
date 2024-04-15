from PyQt5 import QtCore, QtGui, QtWidgets
import qdarkstyle

import sys
sys.path.append("./")

from layout.pd_ui_ver_04_1 import Ui_MainWindow

import sys

# module test
if __name__ == "__main__":
    

    app = QtWidgets.QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())

    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()

    sys.exit(app.exec_())
