"""
A client Modbus RTU implementation.
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

# Reading discrete input
data['discrete0'] = instrument.read_discrete_input(0)
data['discrete1'] = instrument.read_discrete_input(1)
print((data['discrete0'], data['discrete1']))
assert data['discrete0'] == 0
assert data['discrete1'] == 1

# Reading coils
data['coil0'] = instrument.read_coil(0)
data['coil1'] = instrument.read_coil(1)
print((data['coil0'], data['coil1']))
assert data['coil0'] == 1
assert data['coil1'] == 0

# Reading input registers
data['input0'] = instrument.read_input_register(0)
data['input50'] = instrument.read_input_register(50)
print((data['input0'], data['input50']))
assert data['input0'] == 100
assert data['input50'] == 150

# Reading holding registers
data['holding0'] = instrument.read_holding_register(0)
data['holding5'] = instrument.read_holding_register(5)
print((data['holding0'], data['holding5']))
assert data['holding0'] == 500
assert data['holding5'] == 505


# Data base storing
conn = sqlite3.connect('local.db')

c = conn.cursor()

# Create table
c.execute('''
    CREATE TABLE IF NOT EXISTS log (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date DATETIME,
        variable VARCHAR(255),
        value DOUBLE
    )''')

# Insert a row of data
data = [(datetime.today(), key, value) for key, value in data.items()]
c.executemany('INSERT INTO log VALUES (NULL,?,?,?)', data)

# Save (commit) the changes
conn.commit()

for row in c.execute('SELECT * FROM log ORDER BY date'):
    print(row)

# We can also close the connection if we are done with it.
# Just be sure any changes have been committed or they will be lost.
conn.close()
