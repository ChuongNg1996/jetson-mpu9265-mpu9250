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
import math
import datetime
from bitstring import BitArray

# DEFINE THE ADDRESS(ES) OF THE DEVICE
MPU9265_ADDRESS = 0x68
MAG_ADDRESS = 0x0C

# Each device has (1) a set of register to store DATA, and (2) a set of register to CONFIG
# Check: https://invensense.tdk.com/wp-content/uploads/2015/02/RM-MPU-9250A-00-v1.6.pdf 

# DATA REGISTERS
# ACCEL
DEVICE_REGISTER_59 = 0x3B  # 59th Register of MPU9265 to access ACCEL_X_HIGH_BYTE
DEVICE_REGISTER_60 = 0x3C  # 60th Register of MPU9265 to access ACCEL_X_LOW_BYTE
DEVICE_REGISTER_61 = 0x3D  # 61th Register of MPU9265 to access ACCEL_Y_HIGH_BYTE
DEVICE_REGISTER_62 = 0x3E  # 62th Register of MPU9265 to access ACCEL_Y_LOW_BYTE
DEVICE_REGISTER_63 = 0x3F  # 63th Register of MPU9265 to access ACCEL_Z_HIGH_BYTE
DEVICE_REGISTER_64 = 0x40  # 64th Register of MPU9265 to access ACCEL_Z_LOW_BYTE

# GYRO
DEVICE_REGISTER_67 = 0x43
DEVICE_REGISTER_68 = 0x44
DEVICE_REGISTER_69 = 0x45
DEVICE_REGISTER_70 = 0x46
DEVICE_REGISTER_71 = 0x47
DEVICE_REGISTER_72 = 0x48


# CONFIG REGISTERS
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



# Class to config the device
class DeviceControl:  # pylint: disable-msg=too-few-public-methods
    def __init__(self, i2c):
        self.i2c_device = i2c  # self.i2c_device required by UnaryStruct class

    register59 = UnaryStruct(DEVICE_REGISTER_59, "<B")  # 8-bit number
    register60 = UnaryStruct(DEVICE_REGISTER_60, "<B")  # 8-bit number
    register61 = UnaryStruct(DEVICE_REGISTER_61, "<B")  # 8-bit number
    register62 = UnaryStruct(DEVICE_REGISTER_62, "<B")  # 8-bit number
    register63 = UnaryStruct(DEVICE_REGISTER_63, "<B")  # 8-bit number
    register64 = UnaryStruct(DEVICE_REGISTER_64, "<B")  # 8-bit number

    register67 = UnaryStruct(DEVICE_REGISTER_67, "<B")  # 8-bit number
    register68 = UnaryStruct(DEVICE_REGISTER_68, "<B")  # 8-bit number
    register69 = UnaryStruct(DEVICE_REGISTER_69, "<B")  # 8-bit number
    register70 = UnaryStruct(DEVICE_REGISTER_70, "<B")  # 8-bit number
    register71 = UnaryStruct(DEVICE_REGISTER_71, "<B")  # 8-bit number
    register72 = UnaryStruct(DEVICE_REGISTER_72, "<B")  # 8-bit number

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
registers.register27 = GYRO_FULL_SCALE_250_DPS
g_factor = 250

# Configure accelerometers range
registers.register28 = ACC_FULL_SCALE_2_G

# Set by pass mode for the magnetometers
registers.register55 = 0x02

# # Request continuous magnetometer measurements in 16 bits
# i2c_bus0.writeto(MAG_ADDRESS,0x0A,0x16) 

# Calibration
calibrate_num = 1000
AccErrorX = 0
AccErrorY = 0
AccErrorZ = 0
AccAngleErrorX = 0
AccAngleErrorY = 0
c = 0
while (c < calibrate_num):
    ax = format(registers.register59,'08b') + format(registers.register60,'08b')
    ax = -BitArray(bin=ax).int / 16384.0
    ay = format(registers.register61,'08b') + format(registers.register62,'08b')
    ay = -BitArray(bin=ay).int / 16384.0
    az = format(registers.register63,'08b') + format(registers.register64,'08b')
    az = BitArray(bin=az).int / 16384.0

    # Sum all readings
    AccErrorX = AccErrorX + ax
    AccErrorY = AccErrorY + ay
    AccErrorZ = AccErrorZ + az

    AccAngleErrorX = AccAngleErrorX + ((math.atan((ay) / math.sqrt(pow((ax), 2) + pow((az), 2))) * 180.0 / 3.14))
    AccAngleErrorY = AccAngleErrorY + ((math.atan(-1 * (ax) / math.sqrt(pow((ay), 2) + pow((az), 2))) * 180.0 / 3.14))
    c = c + 1

AccErrorX = AccErrorX/calibrate_num
AccErrorY = AccErrorY/calibrate_num
AccErrorZ = AccErrorZ/calibrate_num

AccAngleErrorX = AccAngleErrorX/calibrate_num
AccAngleErrorY = AccAngleErrorY/calibrate_num
c = 0

GyroErrorX = 0
GyroErrorY = 0
GyroErrorZ = 0

while (c < calibrate_num):
    gx = format(registers.register67,'08b') + format(registers.register68,'08b')
    gx = -BitArray(bin=gx).int / 131.0
    gy = format(registers.register69,'08b') + format(registers.register70,'08b')
    gy = -BitArray(bin=gy).int / 131.0
    gz = format(registers.register71,'08b') + format(registers.register72,'08b')
    gz = BitArray(bin=gz).int / 131.0

    # Sum all readings
    GyroErrorX = GyroErrorX + gx
    GyroErrorY = GyroErrorY + gy
    GyroErrorZ = GyroErrorZ + gz
    c = c + 1

GyroErrorX = GyroErrorX / calibrate_num
GyroErrorY = GyroErrorY / calibrate_num
GyroErrorZ = GyroErrorZ / calibrate_num

print("Sensor IMU Calibration Done.")
print(GyroErrorZ)

time_begin = datetime.datetime.now()

xChange = 0
yChange = 0
zChange = 0

xDot = 0
yDot = 0
zDot = 0

rollChange = 0
pitchChange = 0
yawChange = 0

while (1):
    
    # Each value is constructed by 8-bit LOW BYTE + HIGH BYTE
    # Cannot do [bit shift] then [OR] to combine them like C, has to combine string like below
    # Use BitArray to translate to SIGNED int. Beware of translating to UNSIGNED int, which is wrong

    ax = format(registers.register59,'08b') + format(registers.register60,'08b')
    ax = -BitArray(bin=ax).int / 16384.0 - AccErrorX
    ay = format(registers.register61,'08b') + format(registers.register62,'08b')
    ay = -BitArray(bin=ay).int / 16384.0 - AccErrorY
    az = format(registers.register63,'08b') + format(registers.register64,'08b')
    az = BitArray(bin=az).int / 16384.0 - AccErrorZ

    accAngleX = (math.atan(ay / math.sqrt(pow(ax, 2) + pow(az, 2))) * 180.0 / 3.14)
    accAngleY = (math.atan(-1 * (ax) / math.sqrt(pow(ay, 2) + pow(az, 2))) * 180.0 / 3.14) 

    gx = format(registers.register67,'08b') + format(registers.register68,'08b')
    gx = -BitArray(bin=gx).int / 131.0 - GyroErrorX
    gy = format(registers.register69,'08b') + format(registers.register70,'08b')
    gy = -BitArray(bin=gy).int / 131.0 - GyroErrorY
    gz = format(registers.register71,'08b') + format(registers.register72,'08b')
    gz = BitArray(bin=gz).int /131.0 - GyroErrorZ
  

    #print(float(ax),"\t", float(ay),"\t", float(az), "\t",float(gx), "\t",float(gy),"\t",float(gz))
    #print(int(ax),"\t", int(ay),"\t", int(az), "\t",int(gx), "\t",int(gy),"\t",int(gz))

    time_end = datetime.datetime.now()
    time_duration = time_end - time_begin
    #print(time_duration.total_seconds())
    time_duration = time_duration.total_seconds()

    
    xChange = xChange + xDot*time_duration + ax*time_duration*time_duration/2
    xDot = xDot + ax*time_duration

    yChange = yChange + yDot*time_duration + ay*time_duration*time_duration/2
    yDot = yDot + ay*time_duration

    zChange = zChange + zDot*time_duration + az*time_duration*time_duration/2
    zDot = zDot + az*time_duration 
    
    rollChange = rollChange + gx*time_duration
    #rollChange = 0.96*rollChange + 0.04*accAngleX
    pitchChange = pitchChange + gy*time_duration
    #pitchChange = 0.96*pitchChange + 0.04*accAngleY
    yawChange = yawChange + gz*time_duration

    print("x: ", float(xChange),"\t y: ", float(yChange),"\t z: ", float(zChange))
    print("Roll: ", float(rollChange),"\t Pitch: ", float(pitchChange),"\t Yaw: ", float(yawChange))
   
    time.sleep(0.1)
    time_begin = time_end