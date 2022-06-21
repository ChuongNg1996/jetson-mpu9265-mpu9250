#!/usr/bin/python3

# On the Jetson Nano
# Bus 0 (pins 28,27) is board SCL_1, SDA_1 in the jetson board definition file
# Bus 1 (pins 5, 3) is board SCL, SDA in the jetson definition file

# IMPORT LIBRARY AND DEFINE THE I2C BUS (Bus 0 = SCL_1, SDA_1)
from board import SCL_1, SDA_1
from busio import I2C
import time
from adafruit_bus_device.i2c_device import I2CDevice
from adafruit_register.i2c_struct import UnaryStruct

# DEFINE THE ADDRESS(ES) OF THE DEVICE
MPU9265_ADDRESS = 0x68
MAG_ADDRESS = 0x0C

DEVICE_REGISTER_29 = 0x1D  # 29th Register of MPU9265 to access Accel Config 2
DEVICE_REGISTER_26 = 0x1A  # 26th Register of MPU9265 to access Config
DEVICE_REGISTER_27 = 0x1B  # 27th Register of MPU9265 to access Gyro Config 1
DEVICE_REGISTER_28 = 0x1C  # 28th Register of MPU9265 to access Accel Config 1
DEVICE_REGISTER_55 = 0x37  # 55th Register of MPU9265 to access Bypass Enable Config

# DEFINE VALUES FOR CONFIGURATION
GYRO_FULL_SCALE_250_DPS = 0x00  
GYRO_FULL_SCALE_500_DPS = 0x08
GYRO_FULL_SCALE_1000_DPS = 0x10
GYRO_FULL_SCALE_2000_DPS = 0x18

ACC_FULL_SCALE_2_G = 0x00  
ACC_FULL_SCALE_4_G = 0x08
ACC_FULL_SCALE_8_G = 0x10
ACC_FULL_SCALE_16_G = 0x18

# Each device has (1) a set of register to store data, and (2) a set of register to config
# Check: https://invensense.tdk.com/wp-content/uploads/2015/02/RM-MPU-9250A-00-v1.6.pdf 
# Buffer to write data into
result = bytearray(14) 

# Class to config the device
class DeviceControl:  # pylint: disable-msg=too-few-public-methods
    def __init__(self, i2c):
        self.i2c_device = i2c  # self.i2c_device required by UnaryStruct class

    register29 = UnaryStruct(DEVICE_REGISTER_29, "<B")  # 8-bit number
    register26 = UnaryStruct(DEVICE_REGISTER_26, "<B")  # 8-bit number
    register27 = UnaryStruct(DEVICE_REGISTER_27, "<B")  # 8-bit number
    register28 = UnaryStruct(DEVICE_REGISTER_28, "<B")  # 8-bit number
    register55 = UnaryStruct(DEVICE_REGISTER_55, "<B")  # 8-bit number

# Init the I2C bus to manipulate devices on I2C bus 0
i2c_bus0 = (I2C(SCL_1, SDA_1)) 
print(i2c_bus0.scan())
device = I2CDevice(i2c_bus0, MPU9265_ADDRESS)
registers = DeviceControl(device)


# Set accelerometers low pass filter at 5Hz
# Write 0x06 at 29th Register of MPU9265_ADDRESS
registers.register29 = 0x06

# Set gyroscope low pass filter at 5Hz
# Write 0x06 at 26th Register of MPU9265_ADDRESS
registers.register26 = 0x06

# Configure gyroscope range
registers.register27 = GYRO_FULL_SCALE_1000_DPS

# Configure accelerometers range
registers.register28 = ACC_FULL_SCALE_4_G

# Set by pass mode for the magnetometers
registers.register55 = 0x02

#print("register 1: {}; register 2: {}".format(registers.register1, registers.register2))


# # Request continuous magnetometer measurements in 16 bits
# i2c_bus0.writeto(MAG_ADDRESS,0x0A,0x16) 



while (1):
    i2c_bus0.readfrom_into(MPU9265_ADDRESS,result)

    ax = -(result[0] << 8 | result[1])
    ay = -(result[2] << 8 | result[3])
    az = result[4] << 8 | result[5]

    gx = -(result[8] << 8 | result[9])
    gy = -(result[10] << 8 | result[11])
    gz = result[12] << 8 | result[13]

    print(int(ax),"\t", int(ay),"\t", int(az), "\t",int(gx), "\t",int(gy),"\t",int(gz))
    time.sleep(1)