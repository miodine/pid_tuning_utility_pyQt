from utils.pd_monit import StatusMonitor
from utils.pd_spinbox_constraint import *

from layout.pd_ui_ver_04_4 import Ui_MainWindow
from app.pd_comm_server import ServerHandle


from matplotlib.backends.backend_qt5agg import (
    FigureCanvas, NavigationToolbar2QT as NavigationToolbar)
from matplotlib.figure import Figure

# View Dependencies
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.Qt import Qt

# ViewModel Dependencies
import threading
import numpy as np
from collections import deque

# Server Dependencies
import time

#TARGET_IP = '192.168.4.2:14550'
TARGET_IP = 'udpin:localhost:14550'
BAUD_RATE = 57600

# Module Parameters
MODULE_NAME = 'VIEW_MODEL'

# State transition model flags
STM = {'NOT_CONNECTED': 0,
       'TRY_CONNECT': 1,
       'CONNECTED': 2,
       'TRY_DISCONNECT': 3}


# Monitoring Utilities
sm = StatusMonitor(MODULE_NAME)
csm = sm.cmd_status_monit


# TODO: Refactor method names
class ViewModel(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        # Setup Super Class
        QtWidgets.QMainWindow.__init__(self, parent=parent)

        # Setup the View Generalitise
        self.setupUi(self)

        sm.connect(self.var_monit)

        self.init_status = {"DATAFIELDS":       'NOT INIT', 
                            "DYNAMIC_PLOT":     'NOT_INIT',
                            "EVENT_CONNECTORS": 'NOT_INIT',
                            "SERVER_CONNECTOR": 'NOT_INIT'}

        self.__init_view_datafields()
        self.__init_dynamic_plot()
        self.__init_event_connectors()
        self.__init_server_connector()

        self._stm_handle(STM['NOT_CONNECTED'])



    def retranslateUi(self, MainWindow):
        super().retranslateUi(MainWindow)
        _translate = QtCore.QCoreApplication.translate

        self.checkbox_combine_pi_values.setEnabled(False)
        self.checkbox_combine_roll_pitch_axes.setEnabled(False)

    def __init_dynamic_plot(self):
        # Constants
        self.DYNAMIC_PLOT_BUFFER_SIZE = 51
        self._n = self.DYNAMIC_PLOT_BUFFER_SIZE

        self.DYNAMIC_PLOT_INTERVAL_LIMIT = 5
        self._T_max = self.DYNAMIC_PLOT_INTERVAL_LIMIT

        # Variables
        self.axis_to_plot = -1
        self.atp = self.axis_to_plot

        self.t = np.linspace(start=-self._T_max, stop=0, num=self._n)

        self.dp_attitude = np.zeros((3, self._n))
        self.dp_attitude_target = np.zeros((3, self._n))

        # TODO: If the tuning functionality was to be extended by adding
        #       the linear Z axis rate/stab tuning, then it would be better
        #       to store those signal trajectories in a separate array.

        dynamic_canvas = FigureCanvas(Figure(figsize=(3, 2)))
        self.dynamic_plot = self.layout_signal_viz
        self.dynamic_plot.addWidget(dynamic_canvas)
        self._dynamic_ax = dynamic_canvas.figure.subplots()

        self._timer = dynamic_canvas.new_timer(
            4, [(self._dynamic_plot_update, (), {})])
        self._timer.start()

        self.init_status["DYNAMIC_PLOT"] = "OK"

    def __init_view_datafields(self):
        self.CONNECTION_ADDRESSES = {'SITL_DEFAULT': 'udpin:localhost:14550',
                                     'HITL_DEFAULT': '192.168.4.2:14550'}
        self.CADDR = self.CONNECTION_ADDRESSES

        self.CONNECTION_BAUD_RATES = {'SITL_DEFAULT': 57600,
                                      'HITL_DEFAULT': 57600}

        self.CBAUD = self.CONNECTION_BAUD_RATES

        self.cbaud_flag = 'SITL_DEFAULT'

        self.AXES_ID = {"ROLL": 0, "PITCH": 1, "YAW": 2, "ALTITUDE": 3}
        self.AID = self.AXES_ID

        self.PARAMS_ID = {"P_RATE": 0, "I_RATE": 1, "D_RATE": 2}
        self.PaID = self.PARAMS_ID

        self.SPINBOX_CONSTRAINTS = UiSpinboxConstraints()
        self.SC = self.SPINBOX_CONSTRAINTS

        self.attitude_t = np.zeros((3, 1))
        self.attitude_target_t = np.zeros((3, 1))
        self.regulation_error = np.zeros((3, 1))

        # Current PID values
        self.pid_rate = np.zeros((3, 1))
        self.p_stab = 0.0

        # PI Lock Variables
        self.I_YAW_MULTIPLIER = 0.1
        self.I_ROLL_PITCH_MULTIPLIER = 1
        self.PI_lock_enabled = False   # ... szpachla...

        # ROLL-PITCH Lock Variables
        self.ROLL_PITCH_lock_enabled = False

        # Default PID values - taken directly from the flight controller board
        csm("Requesting default controller parameters...")

        self.pid_rate_def_roll = None
        self.p_stab_def_roll = None
        sm("Roll default OK")

        self.pid_rate_def_pitch = None
        self.p_stab_def_pitch = None
        csm("Pitch default OK")

        self.pid_rate_def_yaw = None
        self.p_stab_def_yaw = None

        csm("Yaw default OK")
        csm("All rotation axes OK. No altitude parameters.")

        self.init_status["DATAFIELDS"] = "OK"

    def __init_event_connectors(self):
        self.radio_pitch.toggled.connect(
            lambda: self._ui_select_axis(self.AID['PITCH']))
        self.radio_roll.toggled.connect(
            lambda: self._ui_select_axis(self.AID['ROLL']))
        self.radio_yaw.toggled.connect(
            lambda: self._ui_select_axis(self.AID['YAW']))
        self.radio_alt.toggled.connect(
            lambda: self._ui_select_axis(self.AID['ALTITUDE']))

        self.radio_sitl.toggled.connect(
            lambda: self._ui_connection_type('SITL_DEFAULT'))
        self.radio_hitl.toggled.connect(
            lambda: self._ui_connection_type('HITL_DEFAULT'))

        self.button_upload_tuning.clicked.connect(
            self._upload_defined_controller_values)
        self.button_download_tuning.clicked.connect(
            self._download_controller_values)
        self.button_upload_default_tuning.clicked.connect(
            self._upload_default_controller_values)

        self.button_target_ip_connect.clicked.connect(
            lambda: self._stm_handle(STM["TRY_CONNECT"]))
        self.button_target_ip_disconnect.clicked.connect(
            lambda: self._stm_handle(STM["TRY_DISCONNECT"]))

        self.checkbox_combine_pi_values.toggled.connect(self._PI_lock)
        self.checkbox_combine_roll_pitch_axes.toggled.connect(
            self._roll_pitch_lock)

        self.var_spinbox_rate_P.valueChanged.connect(
            lambda: self._evaluate_PI_lock(self.PaID["P_RATE"]))
        self.var_spinbox_rate_I.valueChanged.connect(
            lambda: self._evaluate_PI_lock(self.PaID["I_RATE"]))


        self.init_status["EVENT_CONNECTORS"] = "OK"


    def __init_server_connector(self):
        self.sh = None
        self.thread = None
        self.conn_target_ip = None
        self.conn_baud_rate = None

        self.init_status["SERVER_CONNECTOR"] = "OK"

    def _stm_handle(self, STM_FLAG: int):
        if STM_FLAG == 0:
            self.__stm_not_connected()
        elif STM_FLAG == 1:
            self.__stm_try_conect()
        elif STM_FLAG == 2:
            self.__stm_connected()
        elif STM_FLAG == 3:
            self.__stm_try_disconnect()
        else:
            csm("State Transition Model ERROR - State not Implemented!")
            csm("Resetting...")
            self.__stm_not_connected()
            csm("State Transition Model - State NOT_CONNECTED")

    def __stm_not_connected(self):
        self.button_target_ip_connect.setEnabled(True)
        self.button_target_ip_disconnect.setEnabled(False)
        self._ui_set_enabled_all(False)
        csm("Please enter the target platform's IP...")

    def __stm_try_conect(self):
        csm("Trying to connect...")
        self.conn_target_ip = self.var_lineedit_target_ip.text()

        # FIXME: make that work properly.
        self.conn_baud_rate = self.CBAUD[self.cbaud_flag]

        self._server_connect()
        

        # -> connected
        return 1

    def __stm_try_disconnect(self):
        self._server_disconnect()

        # -> no_connection
        return 1

    def __stm_connected(self):
        self.button_target_ip_connect.setEnabled(False)
        self.button_target_ip_disconnect.setEnabled(True)
        self._ui_set_enabled_all(True)
        csm("Connected! Select Axis to Tune...")
        return 1

    def _ui_select_axis(self, selected_axis):
        self.atp = selected_axis
        self._download_controller_values()
        self._ui_update_static_textfields()
        self._ui_update_spinbox_constraints()

        self._dynamic_plot_clear()

        if selected_axis not in range(0, 3):
            self._ui_set_enabled_spinboxes(False)

        else:
            self._ui_set_enabled_spinboxes(True)
            self.PI_lock_enabled = False  # entry point for the state machine
            self.ROLL_PITCH_lock_enabled = False

            if selected_axis == 2:
                self.checkbox_combine_pi_values.setEnabled(True)
                self.checkbox_combine_pi_values.setChecked(False)
                self.checkbox_combine_roll_pitch_axes.setEnabled(False)
                self.checkbox_combine_roll_pitch_axes.setChecked(False)

            elif selected_axis == 0 or selected_axis == 1:
                self.checkbox_combine_pi_values.setEnabled(True)
                self.checkbox_combine_pi_values.setChecked(False)
                self.checkbox_combine_roll_pitch_axes.setEnabled(True)
                self.checkbox_combine_roll_pitch_axes.setChecked(False)

            else:
                self.checkbox_combine_pi_values.setChecked(False)
                self.checkbox_combine_pi_values.setEnabled(False)
                self.checkbox_combine_roll_pitch_axes.setEnabled(False)
                self.checkbox_combine_roll_pitch_axes.setChecked(False)

    def _ui_set_enabled_spinboxes(self, enabled: bool):
        self.var_spinbox_rate_P.setEnabled(enabled)
        self.var_spinbox_rate_I.setEnabled(enabled)
        self.var_spinbox_rate_D.setEnabled(enabled)
        self.var_spinbox_stabilization_P.setEnabled(enabled)

        # no max accelleration at this time
        self.var_spinbox_stabilization_Accel.setEnabled(False)

    def _ui_set_enabled_interface(self, enabled: bool):

        #
        self.checkbox_combine_pi_values.setEnabled(enabled)
        self.checkbox_combine_roll_pitch_axes.setEnabled(enabled)

        #
        self.radio_yaw.setEnabled(enabled)
        self.radio_pitch.setEnabled(enabled)
        self.radio_roll.setEnabled(enabled)
        self.radio_alt.setEnabled(enabled)

        #
        self.button_upload_tuning.setEnabled(enabled)
        self.button_download_tuning.setEnabled(enabled)
        self.button_upload_default_tuning.setEnabled(enabled)

    def _ui_set_enabled_all(self, enabled: bool):
        self._ui_set_enabled_spinboxes(enabled)
        self._ui_set_enabled_interface(enabled)

    def _ui_update_static_textfields(self):
        self.var_spinbox_rate_P.setValue(self.pid_rate[0])
        self.var_spinbox_rate_I.setValue(self.pid_rate[1])
        self.var_spinbox_rate_D.setValue(self.pid_rate[2])
        self.var_spinbox_stabilization_P.setValue(self.p_stab)

    def _ui_update_dynamic_textfields(self):
        # FIXME: refactor:
        if self.atp not in range(0, 3):
            self.var_ref_value.setText("%.5f" % 0.0)
            self.var_act_value.setText("%.5f" % 0.0)
            self.var_reg_error.setText("%.5f" % 0.0)
            return

        self.var_ref_value.setText("%.5f" % self.attitude_target_t[self.atp])
        self.var_act_value.setText("%.5f" % self.attitude_t[self.atp])
        self.var_reg_error.setText("%.5f" % self.regulation_error[self.atp])

    def _ui_update_spinbox_constraints(self):
        if self.atp in range(0, 3):
            CONSTRAINTS = self.SC.get_constraint_list_by_axis(self.atp)

            # Rate:

            # P
            self.var_spinbox_rate_P.setMinimum(CONSTRAINTS[0].min)
            self.var_spinbox_rate_P.setMaximum(CONSTRAINTS[0].max)
            self.var_spinbox_rate_P.setSingleStep(CONSTRAINTS[0].step)

            # I
            self.var_spinbox_rate_I.setMinimum(CONSTRAINTS[1].min)
            self.var_spinbox_rate_I.setMaximum(CONSTRAINTS[1].max)
            self.var_spinbox_rate_I.setSingleStep(CONSTRAINTS[1].step)

            # D
            self.var_spinbox_rate_D.setMinimum(CONSTRAINTS[2].min)
            self.var_spinbox_rate_D.setMaximum(CONSTRAINTS[2].max)
            self.var_spinbox_rate_D.setSingleStep(CONSTRAINTS[2].step)

            # Stab:

            # These are the default ones, so we don't have to modify them.
            # Check the generated pd_ui_xxx file (layout folder) to make sure they're there.

    def _ui_connection_type(self, conn_type: str):
        self.var_lineedit_target_ip.setText(self.CADDR[conn_type])
        self.cbaud_flag = conn_type

    def _dynamic_plot_clear(self):

        self._dynamic_ax.clear()

        if(self.atp not in range(0, 3)):
            self.dp_attitude = np.zeros((3, self._n))
            self.dp_attitude_target = np.zeros((3, self._n))
            csm("Parameter Adjustment - Operation Not Supported!")
            return

        self.dp_attitude = self.dp_attitude[self.atp,
                                            self._n-1]*np.ones((3, self._n))
        self.dp_attitude_target = self.dp_attitude[self.atp,
                                                   self._n-1]*np.ones((3, self._n))
        csm("Parameter Adjustment - Visualising RPY Trajectories...")

    def _dynamic_plot_update(self):

        self._evaluate_regulation_error()
        self._ui_update_dynamic_textfields()

        if self.sh is None:
            return

        # Primary (plot-related) continuous events:
        self.attitude_t = self.sh.get_attitude_numpy()
        self.attitude_target_t = self.sh.get_attitude_target_numpy()

        self.dp_attitude = np.roll(self.dp_attitude, -1, axis=1)
        self.dp_attitude_target = np.roll(self.dp_attitude_target, -1, axis=1)

        self.dp_attitude[:, self._n-1] = self.attitude_t.ravel()
        self.dp_attitude_target[:, self._n-1] = self.attitude_target_t.ravel()

        if self.atp in range(0, 3):
            # Plot the trajectories
            self._dynamic_ax.clear()
            self._dynamic_ax.plot(
                self.t, self.dp_attitude[self.atp, :], label="Actual")
            self._dynamic_ax.plot(
                self.t, self.dp_attitude_target[self.atp, :], label="Target", marker='+')
            self._dynamic_ax.fill_between(
                self.t, self.dp_attitude[self.atp, :], self.dp_attitude_target[self.atp, :], color='#CFCFCF')
            self._dynamic_ax.legend()
            self._dynamic_ax.grid()

        self._dynamic_ax.figure.canvas.draw()

    def _server_disconnect(self):
        if self.thread is not None:
            self.thread.stop()
            self.thread = None
            self._stm_handle(STM["NOT_CONNECTED"])

    def _server_connect(self):
        # Server Connector

        self.thread = threading.Thread(target=self._server_connector_routine)
        self.thread.start()

        t = time.time()
        csm("Waiting for server handle... ")

        while self.sh is None:
            t_now = time.time()
            if (t_now - t) > 10:
                csm("Waiting for server handle... ")
                t = time.time()

        self._stm_handle(STM["CONNECTED"])

    def _server_connector_routine(self):
        self.server_handle = ServerHandle(
            self.conn_target_ip, self.conn_baud_rate)
        self.sh = self.server_handle

    def _evaluate_regulation_error(self):
        self.regulation_error = self.attitude_target_t - self.attitude_t

    def _download_controller_values(self):
        csm("Downloading controller parameter values from the flight controller...")
        
        try:
            if self.atp == 0:
                self.pid_rate = self.sh.get_RATE_ROLL_PID()
                self.p_stab = self.sh.get_STAB_ROLL_P()

            elif self.atp == 1:
                self.pid_rate = self.sh.get_RATE_PITCH_PID()
                self.p_stab = self.sh.get_STAB_PITCH_P()

            elif self.atp == 2:
                self.pid_rate = self.sh.get_RATE_YAW_PID()
                self.p_stab = self.sh.get_STAB_YAW_P()

            csm("Download complete.")
            self._ui_update_static_textfields()

        except Exception as e:
            print(e)


        csm("Download Failed (Check Logs)")
        


    def _upload_defined_controller_values(self):
        self.pid_rate[0] = self.var_spinbox_rate_P.value()
        self.pid_rate[1] = self.var_spinbox_rate_I.value()
        self.pid_rate[2] = self.var_spinbox_rate_D.value()
        self.p_stab = self.var_spinbox_stabilization_P.value()

        csm("Uploading the tuning...")

        if self.ROLL_PITCH_lock_enabled is True and (self.atp == 0 or self.atp == 1):
            self.sh.set_RATE_STAB_ROLL(self.pid_rate, self.p_stab)
            self.sh.set_RATE_STAB_PITCH(self.pid_rate, self.p_stab)
            csm("Upload successful. Pitch and roll transmitted together")
        else:
            if self.atp == 0:
                self.sh.set_RATE_STAB_ROLL(self.pid_rate, self.p_stab)
            elif self.atp == 1:
                self.sh.set_RATE_STAB_PITCH(self.pid_rate, self.p_stab)
            elif self.atp == 2:
                self.sh.set_RATE_STAB_YAW(self.pid_rate, self.p_stab)
            csm("Upload successful.")

    # FIXME: Boilerplate. Transmission error handling

    def _upload_default_controller_values(self):
        csm("Transmitting default controller parameters...")
        if self.atp == 0:
            self.pid_rate[0] = self.pid_rate_def_roll[0]
            self.pid_rate[1] = self.pid_rate_def_roll[1]
            self.pid_rate[2] = self.pid_rate_def_roll[2]
            self.p_stab = self.p_stab_def_roll
            self.sh.set_RATE_STAB_ROLL(self.pid_rate, self.p_stab)

        elif self.atp == 1:
            self.pid_rate[0] = self.pid_rate_def_pitch[0]
            self.pid_rate[1] = self.pid_rate_def_pitch[1]
            self.pid_rate[2] = self.pid_rate_def_pitch[2]
            self.p_stab = self.p_stab_def_pitch
            self.sh.set_RATE_STAB_PITCH(self.pid_rate, self.p_stab)

        elif self.atp == 2:
            self.pid_rate[0] = self.pid_rate_def_yaw[0]
            self.pid_rate[1] = self.pid_rate_def_yaw[1]
            self.pid_rate[2] = self.pid_rate_def_yaw[2]
            self.p_stab = self.p_stab_def_yaw
            self.sh.set_RATE_STAB_YAW(self.pid_rate, self.p_stab)

        csm("Default parameters sent. Transmission complete.")
        self._ui_update_static_textfields()

    def _PI_lock(self):
        # Toggle the state flag
        self.PI_lock_enabled = not self.PI_lock_enabled
        # self.var_spinbox_rate_I.setEnabled(self.PI_lock_disabled)
        if self.PI_lock_enabled is True:
            csm("PI lock enabled. YAW: Ki = {}*Kp, ROLL/PITCH: Ki = {}*Kp".format(
                self.I_YAW_MULTIPLIER, self.I_ROLL_PITCH_MULTIPLIER))
        else:
            csm("PI lock disabled.")

    def _evaluate_PI_lock(self, changed_param_id):

        coupling_value = 1
        inv_coupling_value = 1

        if self.atp == 0 or self.atp == 1:
            coupling_value = self.I_ROLL_PITCH_MULTIPLIER
        elif self.atp == 2:
            coupling_value = self.I_YAW_MULTIPLIER

        try:
            inv_coupling_value = 1.0/coupling_value
        except:
            csm("Multiplier value error. Make sure that the multiplier value is NOT zero.")

        if self.PI_lock_enabled is True:
            if changed_param_id == 0:
                curr_P_val = self.var_spinbox_rate_P.value()
                new_I_val = coupling_value*curr_P_val
                self.var_spinbox_rate_I.setValue(new_I_val)

            elif changed_param_id == 1:
                curr_I_val = self.var_spinbox_rate_I.value()

                new_P_val = inv_coupling_value*curr_I_val
                self.var_spinbox_rate_P.setValue(new_P_val)

    def _roll_pitch_lock(self):
        # Toggle the state flag
        self.ROLL_PITCH_lock_enabled = not self.ROLL_PITCH_lock_enabled

        if self.ROLL_PITCH_lock_enabled is True:
            csm("Roll and Pitch axes are now locked.")
        else:
            csm("Roll and Pitch axes are now unlocked.")
