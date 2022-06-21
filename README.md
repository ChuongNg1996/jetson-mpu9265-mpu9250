# Jetson MPU-92/65 (Building)
Read data from MPU92/65. 

## Project Description
There was not much example of using MPU92/65 (i can find only one for MPU9250 for Arduino), let alone on Jetson (Nano) board. So i tried to write one for my Jetson Nano using: 
* [board](https://learn.adafruit.com/arduino-to-circuitpython/the-board-module) & [busio](https://docs.circuitpython.org/en/latest/shared-bindings/busio/) modules from Adafruit with this [I2C example](https://learn.adafruit.com/circuitpython-basics-i2c-and-spi/i2c-devices) for initializing and reading **data** from a device (by its address) on the I2C bus.
* [Adafruit CircuitPython Register](https://docs.circuitpython.org/projects/register/en/latest/examples.html) to access specific registers of the MPU92/65   
* [Arduino example](https://bitbucket.org/cinqlair/mpu9250/src/master/) for configuring MPU92/65 and using its **data**.
* [The servo I2C example](https://github.com/JetsonHacksNano/ServoKit/blob/master/servoPlay.py) of JetsonHacks for some definitions. 

## Requirement
* Python >= 3.7

## Setup & Installation
* Firstly, let's check the pinouts of the board to see where we can use I2C. For [Jetson Nano](https://jetsonhacks.com/nvidia-jetson-nano-j41-header-pinout/), it is pin 3, 4 for SDA and SCL of I2C Bus 1 **AND** pin 27, 28 for SDA and SCL of I2C Bus 0. I choose I2C Bus 0. Make sure that pin 27, 28 is configured to I2C with `sudo /opt/nvidia/jetson-io/jetson-io.py`
* After connecting the wires, use `sudo i2cdetect -r -y 0` if I2C Bus 0 is used (or `sudo i2cdetect -r -y 1` if I2C Bus 1 is used) to check if the address of the device is available (`0x68` in this case).
* Install [board](https://learn.adafruit.com/arduino-to-circuitpython/the-board-module) & [busio](https://docs.circuitpython.org/en/latest/shared-bindings/busio/) modules
   ```sh
   pip3 install board
   pip3 install adafruit-blinka
   pip3 install adafruit-circuitpython-register
   ```
* Run `mpu9265_raw.py` to read raw values.

## Others
* Need Python >= 3.7. If there are multiple Python 3 and Python < 3.7 is set as default, change to higher version, for example Python 3.8 [by](https://askubuntu.com/questions/922853/update-python-3-5-to-3-6-via-terminal):
 ```sh
 sudo update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.8 1
 ```
* [From Adafruit](https://learn.adafruit.com/arduino-to-circuitpython/the-board-module): " CircuitPython knows what board it's running on, and it knows what the capabilities of that board are ... The board module in CircuitPython for a different board will have different constants specific to that board. The user does not have to tell CircuitPython what board it is running on, it knows."
