'''
    ____  ____  ____      ____________________   __  _________  ______  ___ 
   / __ \/ __ \/ __ \    / / ____/ ____/_  __/  /  |/  /  _/ / / / __ \/   |
  / /_/ / /_/ / / / /_  / / __/ / /     / /    / /|_/ // // / / / /_/ / /| |
 / ____/ _, _/ /_/ / /_/ / /___/ /___  / /    / /  / // // /_/ / _, _/ ___ |
/_/   /_/ |_|\____/\____/_____/\____/ /_/    /_/  /_/___/\____/_/ |_/_/  |_|
    __  _____   _____ ____     ___   ____ ________ 
   / / / /   | / ___// __ \   |__ \ / __ <  /__  /
  / /_/ / /| | \__ \/ /_/ /   __/ // / / / /  / /
 / __  / ___ |___/ / ____/   / __// /_/ / /  / /
/_/ /_/_/  |_/____/_/       /____/\____/_/  /_/
'''

import threading
import quick2wire.i2c
import smbus


class I2Cbus:
    def __init__(self):
        self.lock = threading.Lock()
        self.smbus = smbus.SMBus(1)

    def read(self, addr, n):
        with self.lock:
            with quick2wire.i2c.I2CMaster() as bus:
                d = bus.transaction(quick2wire.i2c.reading(addr, n))[0]
        return d

    def write(self, addr, cmd):
        with self.lock:
            with quick2wire.i2c.I2CMaster() as bus:
                bus.transaction(quick2wire.i2c.writing_bytes(addr, cmd))

    def sm_read(self, addr, reg):
        with self.lock:
            return self.smbus.read_byte_data(addr, reg)

    def sm_read_word(self, addr, reg):
        high = self.smbus.read_byte_data(addr, reg)
        low = self.smbus.read_byte_data(addr, reg + 1)
        val = (high << 8) + low
        return val

    def sm_read_word_2c(self, addr, reg):
        val = self.sm_read_word(addr, reg)
        if val >= 0x8000:
            return -((65535 - val) + 1)
        else:
            return val

    def sm_write(self, addr, reg, cmd):
        with self.lock:
            self.smbus.write_byte_data(addr, reg, cmd)
