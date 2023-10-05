from pd_ui_ver_03_1 import Ui_MainWindow
from pd_comm_server import ServerHandle

from matplotlib.backends.backend_qt5agg import (
    FigureCanvas, NavigationToolbar2QT as NavigationToolbar)
from matplotlib.figure import Figure


# View Dependencies
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.Qt import Qt

# ViewModel Dependencies
import threading
import numpy as np

# Server Dependencies

import time 

class ViewModel(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self,parent = None):
        # Setup Super Class
        QtWidgets.QMainWindow.__init__(self, parent=parent)
        
        # Setup the View Generalitise
        self.setupUi(self)
        
        # Setup Signal Plot
        self.__init_dynamic_plot()
        self.__init_class_variables()
        self.__init_server_connector()



    def retranslateUi(self, MainWindow):
        super().retranslateUi(MainWindow)
        _translate = QtCore.QCoreApplication.translate

    def __init_dynamic_plot(self):
        dynamic_canvas = FigureCanvas(Figure(figsize=(1, 1)))
        self.dynamic_plot = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_4)
        self.dynamic_plot.addWidget(dynamic_canvas)
        self.dynamic_plot.setGeometry(QtCore.QRect(10, 10, 20, 10))
        self._dynamic_ax = dynamic_canvas.figure.subplots()
        self._dynamic_ax.xaxis.set_visible(False)

        self._timer = dynamic_canvas.new_timer(
            100, [(self._dynamic_plot_update, (), {})])
        self._timer.start()

    def __init_server_connector(self):
        # Server Connector
        self.thread = threading.Thread(target=self._server_connector_routine)
        self.thread.start()
    
    def __init_class_variables(self):
        self.first_ticks = 0
        self.plot_buffer = np.zeros(101)

    def __init_keyboard_handle(self):
        pass

    def _dynamic_plot_update(self):
        # FIXME: Redo, implement time dependency, use deque https://www.geeksforgeeks.org/dynamic-visualization-using-python/
        # Dummy code
        self._dynamic_ax.clear()
        t = np.linspace(0, 10, 101)
        # Shift the sinusoid as a function of time.
        self._dynamic_ax.plot(t, np.sin(t + time.time()))
        self._dynamic_ax.plot(t, np.cos(t+ time.time()))
        self._dynamic_ax.figure.canvas.draw()

        # old Code
        # if self.first_ticks_ < 100:
        #     self.first_ticks_ += 1
        #     self.plot_buffer[self.first_ticks_] = 1
        # else:
        #     self.plot_buffer[len(self.plot_buffer)-1] = 1
        #     for i in range(1, len(self.plot_buffer)):
        #         self.plot_buffer[i-1] = self.plot_buffer_[i]
    
    def _server_connector_routine(self):
        self.server_handle = ServerHandle('udpin:localhost:14551')

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Shift:
            print("XD")



