"""
A client Modbus RTU implementation for the MX2 variable-frequency drive.
"""
import serial
from datetime import datetime

import sqlite3
from mymodbus import MyInstrument


PORT = '/dev/pts/4'


client_serial = serial.Serial(
    port=PORT,
    baudrate=115200,
    bytesize=8,
    parity='N',
    stopbits=1,
    xonxoff=1,       # Software flow control
    #rtscts=False,    # Hardware flow control
    timeout=0.05
)

instrument = MyInstrument(client_serial, slaveaddress=1)

data = {}

# Reading VFD data
RUN = instrument.read_coil(int(0x13))
REAL_FREQUENCY = instrument.read_holding_registers(int(0x100B), 2)

# Data post-procesing
REAL_FREQUENCY_H, REAL_FREQUENCY_L = REAL_FREQUENCY

# Data base storing
conn = sqlite3.connect('local.db')

c = conn.cursor()

c.execute('''
    CREATE TABLE IF NOT EXISTS log (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date DATETIME,
        RUN BOOL,
        REAL_FREQUENCY_H DOUBLE,
        REAL_FREQUENCY_L DOUBLE
    )''')

values = (
    datetime.utcnow(),
    RUN,
    REAL_FREQUENCY_H,
    REAL_FREQUENCY_L
)
c.execute('INSERT INTO log VALUES (NULL,?,?,?,?)', values)

conn.commit()

for row in c.execute('SELECT * FROM log ORDER BY date'):
    print(row)

conn.close()
