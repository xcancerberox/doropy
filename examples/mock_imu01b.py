from sensors.interfaces import MockI2C
from sensors.imu01b import IMU01b


interfaces = {
    'i2c': MockI2C(1)  # For mocking the address value is not important, but should be present
}

fancy_imu = IMU01b(interfaces)

fancy_imu.get_value()
