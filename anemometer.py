import numpy as np
from complex_sensor import ComplexSensor

class AnemometerWithTachometer(ComplexSensor):
    
    def __init__(self, sensors, arm_length_meters):
        super().__init__()
        self.sensor = sensors['Tachometer']
        self.arm_length_meters = arm_length_meters

    def get_wind_speed(self):
        rotation_period = self.sensor.get_value()['measurements'][0]['value']
        rotation_speed = 2*np.pi*(1/rotation_period) 
        wind_speed_m_s = rotation_speed * self.arm_length_meters
        wind_speed_km_h = 3.6 * wind_speed_m_s
        return wind_speed_km_h

    def prepare_output(self):
        prepared_output = {'wind_speed': self.get_wind_speed()}
        return prepared_output

    def get_value(self):
        return self.prepare_output()
