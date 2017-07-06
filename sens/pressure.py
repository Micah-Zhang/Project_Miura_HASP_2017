from smbus import SMBus
import time


def read_pres():
	deg = u'\N{DEGREE SIGN}'
	ADDR = 0x60
	Ctrl_REG1 = 0x26
	PT_DATA_CFG = 0x13
	bus = SMBus(1)

	whoAmI = bus.read_byte_data(ADDR, 0x0C)
	print( hex(whoAmI))
	if whoAmI != 0xc4:
		print( "Device Not Active")
		exit(1)
	setting = bus.read_byte_data(ADDR, CTRL_REG1)
	newSetting = setting | 0x38
	bus.write_byte_data(ADDR, CTRL_REG1, newSetting)

	bus.write_byte_data(ADDR, PT_DATA_CFG, 0x07)

	setting = bus.read_byte_data(ADDR, CTRL_REG1)
	if (setting & 0x02) == 0:
		bus.write_byte_data(ADDR, CTRL_REG1, (setting | 0x02))

	print( "Waiting for data")
	status = bus.read_bytes_data(ADDR,0x00)
	time.sleep(0.5)

	print( "Reading data")
	p_data = bus.read_i2c_block_data(ADDR,0x01,3)
	t_data = bus.read_i2c_block_data(ADDR,0x04,2)
	status = bus.read_byte_data(ADDR,0x00)
	print("status:" +bin(status))

	p_msb = p_data[0]
	p_csb = p_data[1]
	p_lsb = p_data[2]
	t_msb = t_data[0]
	t_lsb = t_data[1]

	pressure = (p_msb << 10) | (p_csb << 2) | (p_lsb >> 6)
	p_decimal = ((p_lsb & 0x30) >>4) / 4.0

	print("Pressure and Temperature at "+time.strftime('%m/%d/%Y %H:%M:%S%z'))
	print( str(pressure + p_decimal))


read_pres()
