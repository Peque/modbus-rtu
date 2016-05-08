"""
A client Modbus RTU implementation.
"""
from mymodbus import MyInstrument


PORT = '/dev/pts/4'
instrument = MyInstrument(PORT, slaveaddress=1)

# Reading discrete input
discrete0 = instrument.read_discrete_input(0)
discrete1 = instrument.read_discrete_input(1)
print((discrete0, discrete1))
assert discrete0 == 0
assert discrete1 == 1

# Reading coils
coil0 = instrument.read_coil(0)
coil1 = instrument.read_coil(1)
print((coil0, coil1))
assert coil0 == 1
assert coil1 == 0

# Reading input registers
input0 = instrument.read_input_register(0)
input50 = instrument.read_input_register(50)
print((input0, input50))
assert input0 == 100
assert input50 == 150

# Reading holding registers
holding0 = instrument.read_holding_register(0)
holding5 = instrument.read_holding_register(5)
print((holding0, holding5))
assert holding0 == 500
assert holding5 == 505
