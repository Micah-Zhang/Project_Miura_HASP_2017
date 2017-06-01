import smbus
import time

# Get I2C bus
bus = smbus.SMBus(1)

# ADXL345 addres, 0x53(82)
# Select bandwidth rate register, 0x2C(44)
#		0x0A(10)	Normal mode, Output data rate = 100 Hz
bus.write_byte_data(0x53, 0x2C, 0x0A)
# ADXL345 address, 0x53(83)
# Select power control register, 0x2D(45)
# 		0x08(08)	Auto Sleep disable
bus.write_byte_data(0x53, 0x2D, 0x08)

