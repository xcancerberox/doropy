import unittest
import numpy as np
from anemometer import AnemometerWithTachometer
from sensor_mock import SensorMock


class AnemometerWithTachometerTestCase(unittest.TestCase):

    def test_creation(self):
        sensors = dict()
        sensors['Tachometer'] = SensorMock('Tachometer')
        arm_length_meters = 0.1
        anemometer = AnemometerWithTachometer(sensors, arm_length_meters)
        print(anemometer.sensor.sensor_read) 
        self.assertEqual(None,None)

    def test_get_value(self):
        sensors = dict() 
        sensors['Tachometer'] = SensorMock('Tachometer')
        arm_length_meters = 0.1
        anemometer = AnemometerWithTachometer(sensors, arm_length_meters)
        wind_speed = anemometer.get_value() 
        print(wind_speed)
        self.assertAlmostEqual(
            22.61946710584651, 
            wind_speed['wind_speed'])

if __name__ == "__main__":
    unittest.main()  
