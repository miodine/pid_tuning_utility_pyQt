## Server Dependencies

from dronekit import connect, Locations, Vehicle
from pymavlink import mavutil


## Misc. Dependencies
from utils.pd_math import to_quaternion
import math 

## SITL

class ServerHandle():

    def __init__(self, target_udp_address : str):
        self.vehicle_handle = connect(target_udp_address, wait_ready=True)
        self.vh = self.vehicle_handle
        print("Server Handle Initialized...")

        self.TEST_YAW = 200


    # View Model Connector #1
    def get_telemetry(self):
        return self.vh.attitude 

        #FIXME: copy-protect the values (either here, or in the View Model)
    
    # View Model Connetor #2 
    def set_tuning_parameters(self):
        
        return 
    
    # View Model Connector #3 
    # def send_desired_yaw(self,use_yaw_rate = True):
    #     msg = self.vh.message_factory.set_attitude_target_encode(
    #     0, # time_boot_ms
    #     1, # Target system
    #     0, # Target component
    #     0b00000000 if use_yaw_rate else 0b00000100,
    #     to_quaternion(0.0, 0.0, self.TEST_YAW), # Quaternion
    #     0, # Body roll rate in radian
    #     0, # Body pitch rate in radian
    #     math.radians(0.10), # Body yaw rate in radian/second
    #     0.50  # Thrust
    # )
    #     print(self.TEST_YAW)
    #     self.vh.send_mavlink(msg)
    #     #self.vh.flush()
    #     print(self.vh.attitude)

    #def get_position(self):
        #self.vh.location.

        
## HITL