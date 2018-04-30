import unittest
import numpy as np
from wind_vane import WindVaneWithIMU
from sensor_mock import SensorMock


class WindVaneWithIMUTestCase(unittest.TestCase):

    def test_creation(self):
        sensors = dict()
        sensors['IMU'] = SensorMock()
        IMU_wind_vane = WindVaneWithIMU(sensors)
        print(IMU_wind_vane.imu_sensor.sensor_read) 
        self.assertEqual(None,None)

    def test_get_value(self):
        sensors = dict() 
        sensors['IMU'] = SensorMock()
        IMU_wind_vane = WindVaneWithIMU(sensors)
        wind_angle_from_north = IMU_wind_vane.get_value()
        print(wind_angle_from_north)
        self.assertAlmostEqual(
            np.pi/4, 
            wind_angle_from_north['angle_from_north'])

if __name__ == "__main__":
    unittest.main()  
