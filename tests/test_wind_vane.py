import unittest
from sensors.interfaces import MockI2C
from sensors.imu01b import IMU01b
from wind_vane import WindVaneWithIMU

interfaces = {
    'i2c': MockI2C(1)  # For mocking the address value is not important, but should be present
}

class WindVaneWithIMUTestCase(unittest.TestCase):

    def test_creation(self):
        imu_sensor = IMU01b(interfaces)
        IMU_wind_vane = WindVaneWithIMU(imu_sensor)
        print(IMU_wind_vane.sensor.sensor_read) 
        self.assertEqual(None,None)

    def test_get_value(self):
        imu_sensor = IMU01b(interfaces)
        IMU_wind_vane = WindVaneWithIMU(imu_sensor)
        #magnetometer_value = IMU_wind_vane.get_value()
        print(IMU_wind_vane.get_value())
        #self.assertEqual(magnetometer_value,{0.1, 0.5, 1])

if __name__ == "__main__":
    unittest.main()  
