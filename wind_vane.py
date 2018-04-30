import numpy as np
from complex_sensor import ComplexSensor


class WindVaneWithIMU(ComplexSensor):
    """This class represents a IMU-based wind vane,
    which gets inferes wind direction from magnetometer readings."""

    def __init__(self, sensors):
        super().__init__()
        self.imu_sensor = sensors['IMU']
 
    def normalize_vector(self,vector_array):
        """Gets a vector as tuple. Returns the normalized vector as a list."""
        vector_norm =  np.sqrt(sum(component**2 for component in vector_array))
        normalized_vector = vector_array / vector_norm
        print(normalized_vector)
        return normalized_vector
    
    def get_wind_angle_from_north(self):
        wind_vector = np.array([1,0,0]) # Wind vane tip is -X, so wind comes from X. Already norm 1.
        north_list = list(self.imu_sensor.get_value()['measurements'][0]['value'])
        north = np.array(north_list)
        gravity = np.array([0,-1,0]) # Y points up, so gravity is -Y. Already norm 1.
        normalized_north = self.normalize_vector(north)
        horizontal_vec_1 = np.cross(gravity,normalized_north)
        horizontal_vec_2 = np.cross(gravity, horizontal_vec_1)
        proj_north_2_gravity = np.dot(normalized_north,gravity)
        proj_north_2_horizontal = normalized_north - proj_north_2_gravity
        wind_cosine_from_north = np.dot(normalized_north,wind_vector) 
        wind_angle_from_north = np.arccos(np.clip(wind_cosine_from_north,-1,1))
        return wind_angle_from_north

    def prepare_output(self):
        prepared_output = {'angle_from_north': self.get_wind_angle_from_north()}
        return prepared_output

    def get_value(self):
        return self.prepare_output()

