"""
A client Modbus RTU implementation for the MX2 variable-frequency drive.
"""
import time
import sqlite3

import serial

from mymodbus import MyInstrument
from database import save_coil, save_registers, print_db


PORT = '/dev/pts/4'
DB_NAME = 'local.db'
SLAVE_ADDR = 1
MAIN_SLEEP = 3
COILS = {
    'RUN': 1,
}
REGISTERS = {
    'REAL_FREQUENCY': (3, 2),
}
CLIENT_SERIAL = serial.Serial(
    port=PORT,
    baudrate=115200,
    bytesize=8,
    parity='N',
    stopbits=1,
    xonxoff=1,       # Software flow control
    #rtscts=False,    # Hardware flow control
    timeout=0.05
)


def main():
    instrument = MyInstrument(CLIENT_SERIAL, slaveaddress=SLAVE_ADDR)
    conn = sqlite3.connect(DB_NAME)
    for name, address in COILS.items():
        save_coil(conn, instrument, name, address)
    for name, address in REGISTERS.items():
        start_addr, n_registers = address
        save_registers(conn, instrument, name, start_addr, n_registers)
    print_db(conn, {'COILS': COILS, 'REGISTERS': REGISTERS})
    conn.close()


if __name__ == '__main__':
    for i in range(3):
        main()
        time.sleep(MAIN_SLEEP)
