import unittest
from sensor_mock import SensorMock
from wind_vane import WindVaneWithIMU

class SensorMockTestCase(unittest.TestCase):

    def test_creation(self):

        sensor = SensorMock()

        self.assertEqual(None,None)

    def test_get_value(self):

        sensor = SensorMock()
        sensor_value = sensor.get_value()
        self.assertEqual(sensor_value,{'x_value': 0.1, 'y_value': 0.5, 'z_value': 1})

class WindVaneWithIMUTestCase(unittest.TestCase):

    def test_creation(self):
        sensor = SensorMock()
        IMU_wind_vane = WindVaneWithIMU(sensor)
        print(IMU_wind_vane.get_value()) 
        self.assertEqual(None,None)

    def test_get_value(self):
        sensor = SensorMock()
        IMU_wind_vane = WindVaneWithIMU(sensor)
        magnetometer_value = IMU_wind_vane.get_value()
        print(magnetometer_value)
        #self.assertEqual(magnetometer_value,{0.1, 0.5, 1])

if __name__ == "__main__":
    unittest.main()  
