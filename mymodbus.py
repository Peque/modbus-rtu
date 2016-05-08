"""
A Modbus RTU client based on minimalmodbus.
"""
import serial
import minimalmodbus


class MyInstrument(minimalmodbus.Instrument):
    def __init__(self, port, slaveaddress, mode='rtu'):
        # TODO: remove when pyserial 3.1 is out
        minimalmodbus._SERIALPORTS[port] = serial.Serial(
            port=port,
            baudrate=115200,
            bytesize=8,
            parity='N',
            stopbits=1,
            xonxoff=0,
            timeout=0.05,
            rtscts=True,
            dsrdtr=True
        )
        super().__init__(port, slaveaddress, mode=mode)

    def read_input_registers(self, address, number=1):
        return self._genericCommand(functioncode=4,
                                    registeraddress=address,
                                    numberOfRegisters=number,
                                    payloadformat='registers')

    def read_input_register(self, address):
        return self.read_input_registers(address)[0]

    def read_holding_registers(self, address, number=1):
        return self._genericCommand(functioncode=3,
                                    registeraddress=address,
                                    numberOfRegisters=number,
                                    payloadformat='registers')

    def read_holding_register(self, address):
        return self.read_holding_registers(address)[0]

    def read_coil(self, address):
        return self._genericCommand(functioncode=1,
                                    registeraddress=address)

    def read_discrete_input(self, address):
        return self._genericCommand(functioncode=2,
                                    registeraddress=address)
