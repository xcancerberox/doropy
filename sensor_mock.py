import numpy as np

class SensorMock:
    
    def __init__(self, sensor_type):
      
        if sensor_type == 'IMU':
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

        if sensor_type == 'Tachometer':
            value = 0.1 
            self.sensor_read = {'measurements': 
                                 [
                                  {'value': value  
                                  }
                                 ]
                                }

    def get_value(self):
        return self.sensor_read
