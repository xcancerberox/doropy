import random

class SensorMock:
    
    def __init__(self):
        
        self.sensor_value = {'x_value': 0.1, 'y_value': 0.5, 'z_value': 1}

    def get_value(self):
        return self.sensor_value
