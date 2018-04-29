import numpy as np
from complex_sensor import ComplexSensor


class WindVaneWithIMU(ComplexSensor):
    """This class represents a IMU-based wind vane,
    which gets inferes wind direction from magnetometer readings."""

    def __init__(self, imu_sensor):
        super().__init__()
        self.sensor = imu_sensor

    def normalize_magnetometer_value(self):
        """Returns the normalized magnetometer vector as a list."""
        magnetometer_dict = self.sensor.get_value()
        magnetometer_components = sorted(magnetometer_dict.values())
        magnetometer_value_norm =  np.sqrt(sum(component**2 for component in magnetometer_components))
        normalized_magnetometer_value = magnetometer_components / magnetometer_value_norm
        return normalized_magnetometer_value
          
    def get_value(self):
        return self.normalize_magnetometer_value()
        

