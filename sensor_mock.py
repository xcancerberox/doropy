import numpy as np

class SensorMock:
    
    def __init__(self):
        x_value = 1.0
        y_value = 0.0
        z_value = 1.0
        self.sensor_read = {'measurements': 
                             [
                              {'value': 
                               (x_value, y_value, z_value)
                              }
                             ]
                            }

    def get_value(self):
        return self.sensor_read
