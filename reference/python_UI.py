# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'preliminary_layout.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets

from datetime import datetime


import sys
import qdarkstyle
import numpy as np

from serial_comunication import MSL_UART_handler

import threading

from matplotlib.backends.backend_qt5agg import (
    FigureCanvas, NavigationToolbar2QT as NavigationToolbar)
from matplotlib.figure import Figure


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        # UI - GENERATED LAYOUT
        self.serial_handler = MSL_UART_handler()

        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(571, 620)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(10, 340, 201, 101))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.reg_quality = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.reg_quality.setContentsMargins(0, 0, 0, 0)
        self.reg_quality.setObjectName("reg_quality")

        # LABELS SYSTEM INPUT, SYSTEM OUTPUT, REGULATION QUALITY
        self.label_sys_in = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_sys_in.setObjectName("label_sys_in")
        self.reg_quality.addWidget(self.label_sys_in, 2, 0, 1, 1)
        self.var_sysin = QtWidgets.QLabel(self.gridLayoutWidget)
        self.var_sysin.setObjectName("var_sysin")
        self.reg_quality.addWidget(self.var_sysin, 2, 1, 1, 1)
        self.label_sys_out = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_sys_out.setObjectName("label_sys_out")
        self.reg_quality.addWidget(self.label_sys_out, 3, 0, 1, 1)

        # VARIABLES SYSTEM INPUT, SYSTEM OUTPUT, REGULATION QUALITY
        self.var_sysout = QtWidgets.QLabel(self.gridLayoutWidget)
        self.var_sysout.setObjectName("var_sysout")
        self.reg_quality.addWidget(self.var_sysout, 3, 1, 1, 1)

        self.var_regerror = QtWidgets.QLabel(self.gridLayoutWidget)
        self.var_regerror.setObjectName("var_regerror")
        self.reg_quality.addWidget(self.var_regerror, 4, 1, 1, 1)
        self.label_reg_error = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_reg_error.setObjectName("label_reg_error")
        self.reg_quality.addWidget(self.label_reg_error, 4, 0, 1, 1)
        self.gridLayoutWidget_2 = QtWidgets.QWidget(self.centralwidget)
        self.gridLayoutWidget_2.setGeometry(QtCore.QRect(10, 460, 551, 41))
        self.gridLayoutWidget_2.setObjectName("gridLayoutWidget_2")
        self.tuning = QtWidgets.QGridLayout(self.gridLayoutWidget_2)
        self.tuning.setContentsMargins(0, 0, 0, 0)
        self.tuning.setObjectName("tuning")
        self.line_13 = QtWidgets.QFrame(self.gridLayoutWidget_2)
        self.line_13.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_13.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_13.setObjectName("line_13")
        self.tuning.addWidget(self.line_13, 0, 0, 1, 1)

        # PID ADJUSTMENT (TUNING): SPINBOXES
        self.var_spinbox_P = QtWidgets.QDoubleSpinBox(self.gridLayoutWidget_2)
        self.var_spinbox_P.setObjectName("var_spinbox_P")
        self.tuning.addWidget(self.var_spinbox_P, 0, 2, 1, 1)
        self.var_spinbox_I = QtWidgets.QDoubleSpinBox(self.gridLayoutWidget_2)
        self.var_spinbox_I.setObjectName("var_spinbox_I")

        self.tuning.addWidget(self.var_spinbox_I, 0, 6, 1, 1)
        self.line_10 = QtWidgets.QFrame(self.gridLayoutWidget_2)
        self.line_10.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_10.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_10.setObjectName("line_10")
        self.tuning.addWidget(self.line_10, 0, 3, 1, 1)
        self.label_D = QtWidgets.QLabel(self.gridLayoutWidget_2)
        self.label_D.setObjectName("label_D")
        self.tuning.addWidget(self.label_D, 0, 8, 1, 1)
        self.label_P = QtWidgets.QLabel(self.gridLayoutWidget_2)
        self.label_P.setObjectName("label_P")
        self.tuning.addWidget(self.label_P, 0, 1, 1, 1)
        self.label_I = QtWidgets.QLabel(self.gridLayoutWidget_2)
        self.label_I.setObjectName("label_I")
        self.tuning.addWidget(self.label_I, 0, 4, 1, 1)
        self.var_spinbox_D = QtWidgets.QDoubleSpinBox(self.gridLayoutWidget_2)
        self.var_spinbox_D.setObjectName("var_spinbox_D")
        self.tuning.addWidget(self.var_spinbox_D, 0, 9, 1, 1)

        # SEPARATING LINES
        self.line_12 = QtWidgets.QFrame(self.gridLayoutWidget_2)
        self.line_12.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_12.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_12.setObjectName("line_12")
        self.tuning.addWidget(self.line_12, 0, 7, 1, 1)
        self.line_11 = QtWidgets.QFrame(self.gridLayoutWidget_2)
        self.line_11.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_11.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_11.setObjectName("line_11")
        self.tuning.addWidget(self.line_11, 0, 5, 1, 1)
        self.line_14 = QtWidgets.QFrame(self.gridLayoutWidget_2)
        self.line_14.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_14.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_14.setObjectName("line_14")
        self.tuning.addWidget(self.line_14, 0, 10, 1, 1)

        # SEND PID DEFAULT
        self.button_send_default_tuning = QtWidgets.QPushButton(
            self.centralwidget)
        self.button_send_default_tuning.setGeometry(
            QtCore.QRect(10, 530, 551, 23))
        self.button_send_default_tuning.setObjectName(
            "button_send_default_tuning")
        self.button_send_default_tuning.setEnabled(False)

        # SEND PID USER
        self.button_send_custom_tuning = QtWidgets.QPushButton(
            self.centralwidget)
        self.button_send_custom_tuning.setGeometry(
            QtCore.QRect(10, 510, 551, 23))
        self.button_send_custom_tuning.setObjectName(
            "button_send_custom_tuning")
        self.button_send_custom_tuning.setEnabled(False)

        self.button_transmit_data = QtWidgets.QPushButton(self.centralwidget)
        self.button_transmit_data.setGeometry(QtCore.QRect(230, 410, 331, 31))
        self.button_transmit_data.setObjectName("button_transmit_data")

        self.line_2 = QtWidgets.QFrame(self.centralwidget)
        self.line_2.setGeometry(QtCore.QRect(10, 450, 551, 16))
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.line_5 = QtWidgets.QFrame(self.centralwidget)
        self.line_5.setGeometry(QtCore.QRect(210, 340, 20, 101))
        self.line_5.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_5.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_5.setObjectName("line_5")
        self.line_6 = QtWidgets.QFrame(self.centralwidget)
        self.line_6.setGeometry(QtCore.QRect(10, 330, 551, 16))
        self.line_6.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_6.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_6.setObjectName("line_6")

        self.line_9 = QtWidgets.QFrame(self.centralwidget)
        self.line_9.setGeometry(QtCore.QRect(10, 550, 551, 20))
        self.line_9.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_9.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_9.setObjectName("line_9")

        self.horizontalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.horizontalLayoutWidget.setGeometry(
            QtCore.QRect(230, 340, 331, 31))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.velocity_adjustment = QtWidgets.QHBoxLayout(
            self.horizontalLayoutWidget)

        self.velocity_adjustment.setContentsMargins(0, 0, 0, 0)
        self.velocity_adjustment.setObjectName("velocity_adjustment")
        self.label_velocity = QtWidgets.QLabel(self.horizontalLayoutWidget)
        self.label_velocity.setObjectName("label_velocity")
        self.velocity_adjustment.addWidget(self.label_velocity)
        self.var_velocity = QtWidgets.QLabel(self.horizontalLayoutWidget)
        self.var_velocity.setObjectName("var_velocity")
        self.velocity_adjustment.addWidget(self.var_velocity)
        self.button_velocity_plus = QtWidgets.QPushButton(
            self.horizontalLayoutWidget)

        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Ignored, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.button_velocity_plus.sizePolicy().hasHeightForWidth())

        self.button_velocity_plus.setSizePolicy(sizePolicy)
        self.button_velocity_plus.setObjectName("button_velocity_plus")
        self.velocity_adjustment.addWidget(self.button_velocity_plus)
        self.button_velocity_minus = QtWidgets.QPushButton(
            self.horizontalLayoutWidget)

        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Ignored, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.button_velocity_minus.sizePolicy().hasHeightForWidth())

        self.button_velocity_minus.setSizePolicy(sizePolicy)
        self.button_velocity_minus.setObjectName("button_velocity_minus")
        self.velocity_adjustment.addWidget(self.button_velocity_minus)

        self.horizontalLayoutWidget_2 = QtWidgets.QWidget(self.centralwidget)
        self.horizontalLayoutWidget_2.setGeometry(
            QtCore.QRect(230, 380, 331, 23))
        self.horizontalLayoutWidget_2.setObjectName("horizontalLayoutWidget_2")
        self.velocity_range_monit = QtWidgets.QHBoxLayout(
            self.horizontalLayoutWidget_2)
        self.velocity_range_monit.setContentsMargins(0, 0, 0, 0)
        self.velocity_range_monit.setObjectName("velocity_range_monit")
        self.label_percentage_bar = QtWidgets.QLabel(
            self.horizontalLayoutWidget_2)
        self.label_percentage_bar.setObjectName("label_percentage_bar")
        self.velocity_range_monit.addWidget(self.label_percentage_bar)

        self.var_progressbar = QtWidgets.QProgressBar(
            self.horizontalLayoutWidget_2)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.var_progressbar.sizePolicy().hasHeightForWidth())
        self.var_progressbar.setSizePolicy(sizePolicy)
        self.var_progressbar.setProperty("value", 0)
        self.var_progressbar.setAlignment(
            QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.var_progressbar.setTextVisible(True)
        self.var_progressbar.setObjectName("var_progressbar")
        self.velocity_range_monit.addWidget(self.var_progressbar)
        self.horizontalLayoutWidget_3 = QtWidgets.QWidget(self.centralwidget)
        self.horizontalLayoutWidget_3.setGeometry(
            QtCore.QRect(10, 300, 551, 21))
        self.horizontalLayoutWidget_3.setObjectName("horizontalLayoutWidget_3")
        self.operation_state = QtWidgets.QHBoxLayout(
            self.horizontalLayoutWidget_3)
        self.operation_state.setContentsMargins(0, 0, 0, 0)
        self.operation_state.setObjectName("operation_state")
        self.label_monit = QtWidgets.QLabel(self.horizontalLayoutWidget_3)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.label_monit.sizePolicy().hasHeightForWidth())
        self.label_monit.setSizePolicy(sizePolicy)
        self.label_monit.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_monit.setObjectName("label_monit")
        self.operation_state.addWidget(self.label_monit)
        self.var_monit = QtWidgets.QLabel(self.horizontalLayoutWidget_3)
        self.var_monit.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.var_monit.setObjectName("var_monit")
        self.operation_state.addWidget(self.var_monit)
        self.line_7 = QtWidgets.QFrame(self.centralwidget)
        self.line_7.setGeometry(QtCore.QRect(10, 290, 551, 16))
        self.line_7.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_7.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_7.setObjectName("line_7")

        self.horizontalLayoutWidget_4 = QtWidgets.QWidget(self.centralwidget)
        self.horizontalLayoutWidget_4.setGeometry(
            QtCore.QRect(20, 20, 521, 251))
        self.horizontalLayoutWidget_4.setObjectName("horizontalLayoutWidget_4")

        # VISUALISATION OF CHANGE IN THE VELOCITY ON GIVEN INTERVAL
        dynamic_canvas = FigureCanvas(Figure(figsize=(1, 1)))

        self.dynamic_plot = QtWidgets.QVBoxLayout(
            self.horizontalLayoutWidget_4)
        self.dynamic_plot.addWidget(dynamic_canvas)
        self.dynamic_plot.setGeometry(QtCore.QRect(10, 10, 20, 10))
        self._dynamic_ax = dynamic_canvas.figure.subplots()
        self._dynamic_ax.xaxis.set_visible(False)

        self._timer = dynamic_canvas.new_timer(
            100, [(self._update_readout, (), {})])
        self._timer.start()

        self.horizontalLayout = QtWidgets.QHBoxLayout(
            self.horizontalLayoutWidget_4)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        
        self.horizontalLayoutWidget_5 = QtWidgets.QWidget(self.centralwidget)
        self.horizontalLayoutWidget_5.setGeometry(
            QtCore.QRect(10, 560, 551, 31))
        self.horizontalLayoutWidget_5.setObjectName("horizontalLayoutWidget_5")

        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(
            self.horizontalLayoutWidget_5)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.button_start_logging = QtWidgets.QPushButton(
            self.horizontalLayoutWidget_5)
        self.button_start_logging.setObjectName("button_start_logging")
        self.horizontalLayout_2.addWidget(self.button_start_logging)
        self.button_stop_logging = QtWidgets.QPushButton(
            self.horizontalLayoutWidget_5)
        self.button_stop_logging.setObjectName("button_stop_logging")
        self.button_stop_logging.setEnabled(False)

        self.horizontalLayout_2.addWidget(self.button_stop_logging)

        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 571, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        # BIND EVENTS
        self.button_velocity_plus.clicked.connect(self.event_increase_velocity)
        self.button_velocity_minus.clicked.connect(
            self.event_decrease_velocity)
        self.button_send_custom_tuning.clicked.connect(
            self.event_updatePIDFromValues)
        self.button_send_default_tuning.clicked.connect(
            self.event_updatePIDDefault)
        self.button_transmit_data.clicked.connect(self.event_transmitData)
        self.button_start_logging.clicked.connect(self.event_start_logging)
        self.button_stop_logging.clicked.connect(self.event_stop_logging)

        # CLASS constants
        self.MAX_RPM = 7900
        self.MIN_RPM = 0

        self.INCREMENT_STEP_RPM = 100

        self.P_GAIN_DEFAULT = 1
        self.I_GAIN_DEFAULT = 1
        self.D_GAIN_DEFAULT = 1

        # CLASS variables
        self.plot_buffer_ = np.zeros(101)
        self.RPM_set = 0
        self.RPM_actual = 1
        self.RPM_difference = 0
        self.RPM_to_be_set = 0

        self.first_ticks_ = 0
        self.status = 0

        self.p_gain = 1
        self.i_gain = 1
        self.d_gain = 1

        self.monit = ""

        self.enc_used = False

        self.logging_started = False
        self.input_logger = open("RPM_SET_DATA_LOG.txt", "a")
        self.input_logger.close()

        self.output_logger = open("RPM_SET_DATA_LOG.txt", "a")
        self.output_logger.close()

# CLASS METHODS

    def reg_quality_update(self):
        self.RPM_actual, self.RPM_set, self.status, self.enc_used = self.serial_handler.read_data(
            self.RPM_actual, self.RPM_set, self.status, self.input_logger, self.output_logger, self.logging_started)
        self.var_sysout.setText(str(self.RPM_actual) + " RPM")
        self.var_regerror.setText(str(self.RPM_set - self.RPM_actual) + " RPM")

        if(self.status != 0):
            self._update_monit(
                "SERIAL DATA-BUFFER OVERFLOW OCCURED! PLEASE HOLD UNTIL SYSTEM OUTPUT SHOWS VALUE < 8000 AND > 0")
        if(self.enc_used == True):
            self._update_monit("Reference RPM set locally!")
            self.var_sysin.setText(str(self.RPM_set) + " RPM")

    def _update_readout(self):
        # get data
        thread = threading.Thread(target=self.reg_quality_update)
        thread.start()

        self._dynamic_ax.clear()
        t = np.linspace(0, 10, 101)
        self._update_output_RPM_visualisation()

        self._dynamic_ax.plot(t, self.plot_buffer_)
        self._dynamic_ax.figure.canvas.draw()

    def _update_output_RPM_visualisation(self):
        if self.first_ticks_ < 100:
            self.first_ticks_ += 1
            self.plot_buffer_[self.first_ticks_] = self.RPM_actual
        else:
            self.plot_buffer_[len(self.plot_buffer_)-1] = self.RPM_actual
            for i in range(1, len(self.plot_buffer_)):
                self.plot_buffer_[i-1] = self.plot_buffer_[i]

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate(
            "MainWindow", "MPS Lab - Motor control and control data visualisation app"))
        self.label_sys_in.setText(_translate("MainWindow", "System input:"))
        self.var_sysin.setText(_translate("MainWindow", "0 RPM"))
        self.label_sys_out.setText(_translate("MainWindow", "System output:"))
        self.var_sysout.setText(_translate("MainWindow", "__sys_output__"))
        self.var_regerror.setText(_translate("MainWindow", "__sys_regerror__"))
        self.label_reg_error.setText(
            _translate("MainWindow", "Regulation error:"))
        self.label_D.setText(_translate("MainWindow", "Derivative gain (D)"))
        self.label_P.setText(_translate("MainWindow", "Proportional gain (P)"))
        self.label_I.setText(_translate("MainWindow", "Integrator gain (I)"))
        # TRANSMIT BUTTONS
        self.button_send_default_tuning.setText(
            _translate("MainWindow", "Set default tuning values"))
        self.button_send_custom_tuning.setText(_translate(
            "MainWindow", "Set tuning values defined above"))
        self.button_transmit_data.setText(_translate(
            "MainWindow", "Update tunig and/or velocity"))
        self.label_velocity.setText(
            _translate("MainWindow", "New RPM value: "))
        self.var_velocity.setText(_translate("MainWindow", "0 RPM"))
        self.button_velocity_plus.setText(_translate("MainWindow", "+"))
        self.button_velocity_minus.setText(_translate("MainWindow", "-"))
        self.label_percentage_bar.setText(_translate(
            "MainWindow", "% of max. value allowed:"))
        self.label_monit.setText(_translate("MainWindow", "MONIT:"))
        self.var_monit.setText(_translate(
            "MainWindow", "Program started, and it is probably working properly."))

        self.button_start_logging.setText(
            _translate("MainWindow", "Start Logging"))
        self.button_stop_logging.setText(
            _translate("MainWindow", "Stop Logging "))

    def _update_monit(self, string):
        self.monit = string
        self.var_monit.setText(self.monit)


# EVENTS

    def event_increase_velocity(self):
        if self.RPM_to_be_set < self.MAX_RPM:
            self.RPM_to_be_set += self.INCREMENT_STEP_RPM
            self._update_monit("RPM to-be-set increased")
            self.var_progressbar.setProperty(
                "value", int(self.RPM_to_be_set/self.MAX_RPM * 100))
        else:
            self._update_monit("RPM to-be-set cannot be increased anymore!")
        self.var_velocity.setText(str(self.RPM_to_be_set) + " RPM")

    def event_decrease_velocity(self):
        if self.RPM_to_be_set > self.MIN_RPM:
            self.RPM_to_be_set -= self.INCREMENT_STEP_RPM
            self._update_monit("RPM to-be-set decreased")

            self.var_progressbar.setProperty(
                "value", int(self.RPM_to_be_set/self.MAX_RPM * 100))
        else:
            self._update_monit("RPM to-be-set cannot be decreased anymore!")
        self.var_velocity.setText(str(self.RPM_to_be_set) + " RPM")

    def event_updatePIDFromValues(self):
        self.p_gain = int(100*self.var_spinbox_P.value())
        self.i_gain = int(100*self.var_spinbox_I.value())
        self.d_gain = int(100*self.var_spinbox_D.value())
        self._update_monit(
            "PID control not available in demo version. Please pay 1,500,000 USD to obtain all the features.")

    def event_updatePIDDefault(self):
        self.p_gain = self.P_GAIN_DEFAULT
        self.i_gain = self.I_GAIN_DEFAULT
        self.d_gain = self.D_GAIN_DEFAULT
        self._update_monit(
            "PID control not available in demo version. Please pay 1,500,000 USD to obtain all the features.")

    def event_transmitData(self):
        self._update_monit("Sending an update...")
        self.RPM_set = self.RPM_to_be_set
        self.var_sysin.setText(str(self.RPM_set) + " RPM")
        self.serial_handler.send_data(
            self.p_gain, self.i_gain, self.d_gain, self.RPM_set)
        self._update_monit("Update sent.")

    def event_start_logging(self):
        self.input_logger = open("RPM_SET_DATA_LOG.txt", "a")
        self.output_logger = open("RPM_OUTPUT_DATA_LOG.txt", "a")
        self.logging_started = True

        self.input_logger.write("Log started at: " +
                                str(datetime.now()) + "\n")
        self.input_logger.write("Logs taken each 1s. \r\n")

        self.output_logger.write(
            "Log started at: " + str(datetime.now()) + "\n")
        self.output_logger.write("Logs taken each 1s. \r\n")

        self.button_start_logging.setEnabled(False)
        self.button_stop_logging.setEnabled(True)

        self._update_monit("Input and output data log started.")

    def event_stop_logging(self):

        self.input_logger.write("Log stopped at: " +
                                str(datetime.now()) + "\r\n")
        self.output_logger.write(
            "Log stopped at: " + str(datetime.now()) + "\r\n")

        self.input_logger.close()
        self.output_logger.close()
        self.logging_started = False

        self.button_start_logging.setEnabled(True)
        self.button_stop_logging.setEnabled(False)

        self._update_monit("Input and output data logging has been stopped. ")


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())

    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()

    sys.exit(app.exec_())
