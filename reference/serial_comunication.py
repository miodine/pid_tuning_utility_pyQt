import serial

import struct

COM_FLAG = 68


class MSL_UART_handler():
    def __init__(self):
        self._port_name = ''
        print('MS Lab. project - UART communication initialization...')
        self._port_name = input(
            'Port name to which NUCLEO is connected (eg. "COM4" - no spaces!): ')
        self.ser = serial.Serial(self._port_name, baudrate=115200,
                                 timeout=0.01, parity=serial.PARITY_NONE)  # open serial port
        print('Port ' + self.ser.name + ' has been opened...')
        print(
            "Make sure that baudrate == 115200, parity == none and comunicatiom flag == 68")

        self.transmitting_ = False

    def read_data(self, RPM_actual, RPM_reference, status_code, file_in, file_out, log_flag):

        received_RPM_reference = 0

        if self.ser.is_open == True and self.transmitting_ == False:
            s = self.ser.read(1)
            if s != b'':  # todo: zmien na wykrywanie flagi
                s = self.ser.read(4)
                RPM_actual = int.from_bytes(s, 'little')
                print(RPM_actual)

                s = self.ser.read(4)
                received_RPM_reference = int.from_bytes(s, 'little')
                print(received_RPM_reference)

                s = self.ser.read(1)
                status_code = int.from_bytes(s, 'little')
                print(status_code)
                print("-------------")

                if log_flag == True:
                    file_in.write("%d\n" % status_code)
                    file_out.write("%d\n" % RPM_actual)

                if received_RPM_reference != RPM_reference:
                    return RPM_actual, received_RPM_reference, status_code, True

        return RPM_actual, RPM_reference, status_code, False

    def send_data(self, Kp, Ki, Kd, RPM_set):
        #self.ser.write(struct.pack("B", COM_FLAG))
        self.transmitting_ = True
        print("transmitting...")
        self.ser.write(struct.pack("I", Kp))
        self.ser.write(struct.pack("I", Ki))
        self.ser.write(struct.pack("I", Kd))
        self.ser.write(struct.pack("I", RPM_set))
        self.transmitting_ = False
