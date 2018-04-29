from complex_sensor import ComplexSensor

class Anemometer():
    def __init__(self, sensors):
        super().__init__()
        self.sensor = sensors['encoder']

    def get_wind_speed(self):
        wind_speed = self.sensor.get_value()
        return wind_speed

    def prepare_output(self):
        prepared_output = {'wind_speed': self.get_wind_speed()}
        return prepared_output

    def get_value(self):
        return self.prepare_output()
