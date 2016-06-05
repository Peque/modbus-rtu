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
MAIN_SLEEP = 60
COILS = {
    'OPERATION_STATE': 0x000F,
    'READY': 0x0011,
    'RUN': 0x0013,
    'FA1': 0x0014,
    'FA2': 0x0015,
    'AL': 0x0018,
    'FA3': 0x0019,
    'UV': 0x001c,
    'FA4': 0x002b,
    'FA5': 0x002c,
    'LOC': 0x003e,
    'FWR': 0x0046,
    'MJA': 0x0048,
}
REGISTERS = {
    'VFDA_STATE': (0x0003, 1),
    'TRIGGER_COUNT': (0x0011, 1),
    'TRIGGER_1': (0x0012, 10),
    'TRIGGER_2': (0x001c, 10),
    'TRIGGER_3': (0x0026, 10),
    'TRIGGER_4': (0x0030, 10),
    'TRIGGER_5': (0x003a, 10),
    'TRIGGER_6': (0x0044, 10),
    'OUTPUT_FREQUENCY': (0x1001, 2),
    'OUTPUT_CURRENT': (0x1003, 1),
    'REAL_FREQUENCY': (0x100B, 2),
    'OUTPUT_VOLTAGE': (0x1011, 1),
    'POWER': (0x1012, 1),
    'WATTS_HOUR': (0x1013, 2),
    'TIME_RUNNING': (0x1015, 2),
    'TIME_POWERED': (0x1017, 2),
    'HEATSINK_TEMP': (0x1019, 1),
    'DC_VOLTAGE': (0x1026, 1),
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
    conn.close()


if __name__ == '__main__':
    while True:
        main()
        time.sleep(MAIN_SLEEP)
