
# 
class StatusMonitor:
    def __init__(self, subsystem_ID: str):
        self._subsystem_id = subsystem_ID
    
    def cmd_status_monit(self, message : str):
        print(self._subsystem_id,': ', message, '\n\r')
