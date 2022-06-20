#!/usr/bin/python3

import board 
import busio
import time

MPU9265_ADDRESS = 0x68

# On the Jetson Nano
# Bus 0 (pins 28,27) is board SCL_1, SDA_1 in the jetson board definition file
# Bus 1 (pins 5, 3) is board SCL, SDA in the jetson definition file
i2c_bus0=(busio.I2C(board.SCL_1, board.SDA_1))
print(i2c_bus0.scan())
result = bytearray(14)

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
