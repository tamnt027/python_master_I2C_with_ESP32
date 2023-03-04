
from Adafruit_PureIO.smbus import SMBus
import time
# This is the address we gave in the ESP32 - see code
ESP_I2C_address = 0x30
# open I2C bus 1 = RPi3/4
bus = SMBus(1)

def read_from_arduino(i2caddress: hex, size: int):
    try:
        # get data sent by ESP32, in raw format.
        # read 25 bytes
        stream = bus.read_bytes(i2caddress, size)
        return stream
    except Exception as e:
        print("ERROR: {}".format(e))

# write data to ESP32
def write_to_arduino(i2caddress: hex, data: str):
    try:
        # send stream to slave
        bus.write_bytes(i2caddress, bytearray(data))
    except Exception as e:
        print("{}".format(e))