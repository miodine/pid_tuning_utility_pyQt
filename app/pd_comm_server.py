## Server Dependencies

from dronekit import connect, Locations, Vehicle
from pymavlink import mavutil


## Misc. Dependencies
from utils.pd_math import to_quaternion
from utils.pd_monit import StatusMonitor
import math 


## Module Parameters
MODULE_NAME = 'SERVER'

## Monitoring Utilities
sm = StatusMonitor(MODULE_NAME)
csm = sm.cmd_status_monit


## SITL

class ServerHandle():

    def __init__(self, target_udp_address : str):
        
        # Vehicle handle initialization
        self.vehicle_handle = connect(target_udp_address, wait_ready=True)
        self.vh = self.vehicle_handle   # abstraction

        # Message listeners
        self.vh.add_message_listener("ATTITUDE_TARGET", self._parse_attitude_target)

        # Class datafields
        self.attitude_target = None


        csm("Server Handle Initialized...")


    def _parse_attitude_target(self, vehicle, message_name, message):
        self.attitude_target

    # View Model Connector #1
    def get_attitude(self):
        return self.vh.attitude 

        #FIXME: copy-protect the values (either here, or in the View Model)
    
    def get_attitude_target(self):
        pass


    # View Model Connetor #2 
    def set_tuning_parameters(self):
        
        return 
    

        
## HITL