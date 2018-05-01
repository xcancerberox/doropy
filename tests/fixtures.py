import pytest
from sensors.mocks import MockGPIO

class MockI2C(object):

    def __init__(self, address):
        self.address = address
        self.read_values = {}

    def read(self, *args):
        return self.read_values.pop(0)

    def write(self, *args):
        pass


@pytest.fixture
def i2c_imu01b():

    interfaces = {
        'i2c': MockI2C(1)
    }
    interfaces['i2c'].read_values = [0x80]
    return interfaces

@pytest.fixture
def gpio_instance():
    print("Init gpio_instance")
    gpio_instance = MockGPIO.instance()
    gpio_instance.reset_cache()
    return gpio_instance
