## Server Dependencies

from dronekit import connect, Locations, Vehicle
from pymavlink import mavutil


## Misc. Dependencies
from utils.pd_math import to_quaternion
from utils.pd_monit import StatusMonitor
import math 
import numpy as np
from scipy.spatial.transform import Rotation as R

## Module Parameters
MODULE_NAME = 'SERVER'

## Monitoring Utilities
sm = StatusMonitor(MODULE_NAME)
csm = sm.cmd_status_monit


## SITL
class ServerHandle():

    def __init__(self, target_udp_address : str):
        
        # Vehicle handle initialization

        csm("Server Handle Initialization...")
        self.vehicle_handle = connect(target_udp_address, wait_ready=True)
        self.vh = self.vehicle_handle   # abstraction

        # Message listeners
        self.vh.add_message_listener("ATTITUDE_TARGET", self._parse_attitude_target)

        # Class datafields
        self.attitude_target = None
        csm("Server Handle Initialized...")


    def _parse_attitude_target(self, vehicle, message_name, message):
        self.attitude_target = message

    # View Model Connectors
    def get_attitude_raw(self):
        return self.vh.attitude 
        #FIXME: copy-protect the values (either here, or in the View Model)
    
    def get_attitude_target_raw(self):
        return self.attitude_target
    
    def get_attitude_numpy(self):
        r = self.vh.attitude.roll
        p = self.vh.attitude.pitch
        y = self.vh.attitude.yaw

        # Return Column Vector of current RPY values 
        try:
            return np.array([r,p,y]).T
        except Exception as e:
            csm("Attitude - No data received.")
            return np.zeros((3,1))

    def get_attitude_target_numpy(self):
        # rates
        # r_t = self.attitude_target.body_roll_rate
        # p_t = self.attitude_target.body_pitch_rate
        # y_t = self.attitude_target.body_yaw_rate
        try: 
            r = R.from_quat(np.array(self.attitude_target.q))
            r = r.as_euler('zyx', degrees=False).T
            r[2] += math.pi
            r[2] = -r[2]
            r[0] = -r[0]

            return r
            


        except Exception as e:
            csm("Attitude Target - No data received.")
            return np.zeros((3,1))
 
    # View Model Connetor #2 
    def set_tuning_parameters(self):
        return 
    
    def get_STAB_PITCH_P(self):
        return self.vh.parameters['Q_A_ANG_PIT_P']

    def get_STAB_ROLL_P(self):
        return self.vh.parameters['Q_A_ANG_RLL_P']

    def get_STAB_YAW_P(self):
        return self.vh.parameters['Q_A_ANG_YAW_P']
    

    #FIXME: Get rid of the boilerplate code

    def get_RATE_ROLL_PID(self) -> np.array:
        p = self.vh.parameters['Q_A_RAT_RLL_P']
        i = self.vh.parameters['Q_A_RAT_RLL_I']
        d = self.vh.parameters['Q_A_RAT_RLL_D']
        return np.array([p,i,d]).T
    
    def get_RATE_PITCH_PID(self) -> np.array:
        p = self.vh.parameters['Q_A_RAT_PIT_P']
        i = self.vh.parameters['Q_A_RAT_PIT_I']
        d = self.vh.parameters['Q_A_RAT_PIT_D']
        return np.array([p,i,d]).T
    
    def get_RATE_YAW_PID(self) -> np.array:
        p = self.vh.parameters['Q_A_RAT_YAW_P']
        i = self.vh.parameters['Q_A_RAT_YAW_I']
        d = self.vh.parameters['Q_A_RAT_YAW_D']
        return np.array([p,i,d]).T
    
    def set_RATE_STAB_ROLL(self, pid_rate: np.array, p_stab: np.array):
        self.vh.parameters['Q_A_RAT_RLL_P'] = pid_rate[0]
        self.vh.parameters['Q_A_RAT_RLL_I'] = pid_rate[1]
        self.vh.parameters['Q_A_RAT_RLL_D'] = pid_rate[2]
        self.vh.parameters['Q_A_ANG_RLL_P'] = p_stab

    def set_RATE_STAB_PITCH(self, pid_rate: np.array, p_stab: np.array):
        self.vh.parameters['Q_A_RAT_PIT_P'] = pid_rate[0]
        self.vh.parameters['Q_A_RAT_PIT_I'] = pid_rate[1]
        self.vh.parameters['Q_A_RAT_PIT_D'] = pid_rate[2]
        self.vh.parameters['Q_A_ANG_PIT_P'] = p_stab

    def set_RATE_STAB_YAW(self, pid_rate: np.array, p_stab: np.array):
        self.vh.parameters['Q_A_RAT_YAW_P'] = pid_rate[0]
        self.vh.parameters['Q_A_RAT_YAW_I'] = pid_rate[1]
        self.vh.parameters['Q_A_RAT_YAW_D'] = pid_rate[2]
        self.vh.parameters['Q_A_ANG_YAW_P'] = p_stab