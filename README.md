# Jetson MPU-92/65 (Building)
Read data from MPU92/65. 

## Project Description
There was not much example of using MPU92/65 (i can find only one for Arduino), let alone on Jetson (Nano) board. So i tried to write one for my Jetson Nano using: 
* [board](https://learn.adafruit.com/arduino-to-circuitpython/the-board-module) & [busio](https://docs.circuitpython.org/en/latest/shared-bindings/busio/) modules from Adafruit with this [I2C example](https://learn.adafruit.com/circuitpython-basics-i2c-and-spi/i2c-devices) for initializing and reading data in HEX from the I2C bus.
* [Arduino example](https://bitbucket.org/cinqlair/mpu9250/src/master/) for using the data.
* [The servo I2C example](https://github.com/JetsonHacksNano/ServoKit/blob/master/servoPlay.py) of JetsonHacks for some definitions. 

## Requirement
* Python >= 3.7

## Setup & Installation
* Firstly, let's check the pinouts of the board to see where we can use I2C. For [Jetson Nano](https://jetsonhacks.com/nvidia-jetson-nano-j41-header-pinout/), it is pin 3, 4 for SDA and SCL of I2C Bus 1 **AND** pin 27, 28 for SDA and SCL of I2C Bus 0. I choose I2C Bus 0. Make sure that pin 27, 28 is configured to I2C 
  
*
   ```sh
   pip3 install board
   pip3 install adafruit-blinka

   ```
## Others
* Need Python >= 3.7. If there are multiple Python 3 and Python < 3.7 is set as default, change to higher version, for example Python 3.8 [by](https://askubuntu.com/questions/922853/update-python-3-5-to-3-6-via-terminal):
 ```sh
 sudo update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.8 1
 ```
