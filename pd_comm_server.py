## Server Dependencies

from dronekit import connect, Locations, Vehicle
from pymavlink import mavutil


## SITL

class ServerHandle():

    def __init__(self, target_udp_address : str):
        self.vehicle_handle = connect(target_udp_address, wait_ready=True)
        self.vh = self.vehicle_handle

    # View Model Connector #1
    def get_telemetry(self):
        return self.vh.attitude 
    
        #FIXME: copy-protect the values (either here, or in the View Model)
    
    # View Model Connetor #2 
    def set_tuning_parameters(self):
        
        
        return 





        

## HITL