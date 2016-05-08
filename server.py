"""
A server Modbus RTU implementation.
"""
import sys

import modbus_tk
import modbus_tk.defines as cst
from modbus_tk import modbus_rtu
import serial


PORT = '/dev/pts/5'


logger = modbus_tk.utils.create_logger(name='console',
                                       record_format='%(message)s')

server = modbus_rtu.RtuServer(
    serial.Serial(port=PORT,
                  baudrate=115200,
                  bytesize=8,
                  parity='N',
                  stopbits=1,
                  xonxoff=0,
                  rtscts=True,dsrdtr=True)
)

try:
    logger.info('Running...')
    logger.info('Enter \'quit\' for closing the server')

    server.start()

    slave_1 = server.add_slave(1)

    slave_1.add_block('discrete_inputs', cst.READ_DISCRETE_INPUTS, 0, 2)
    slave_1.set_values('discrete_inputs', 0, (0, 1))

    slave_1.add_block('coils', cst.COILS, 0, 2)
    slave_1.set_values('coils', 0, (1, 0))

    slave_1.add_block('input_regs', cst.READ_INPUT_REGISTERS, 0, 100)
    slave_1.set_values('input_regs', 0, [x + 100 for x in range(100)])

    slave_1.add_block('holding_regs', cst.HOLDING_REGISTERS, 0, 100)
    slave_1.set_values('holding_regs', 0, [x + 500 for x in range(100)])

    while True:
        cmd = sys.stdin.readline()
        args = cmd.split(' ')

        if cmd.find('quit') == 0:
            sys.stdout.write('bye-bye\n')
            break
        else:
            sys.stdout.write('Unknown command %s\n' % args[0])
finally:
    server.stop()
