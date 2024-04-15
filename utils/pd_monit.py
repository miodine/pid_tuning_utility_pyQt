from PyQt5 import QtWidgets as QW

class StatusMonitor:
    def __init__(self, subsystem_ID: str):
        self._subsystem_id = subsystem_ID
        self.qt_gui_monit = None

    def cmd_status_monit(self, message : str):
        monit = self._subsystem_id + ': ' + message + '\n\r'
        print(monit)
        if self.qt_gui_monit is not None:
            self.qt_gui_monit.setText(message)

        return monit
    
    def connect(self, gui_monit : QW.QLabel):
        self.qt_gui_monit = gui_monit