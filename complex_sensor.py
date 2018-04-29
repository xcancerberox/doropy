class ComplexSensor():
    """Parent class for every complex sensor.
    Complex sensors share the get_value method in order to standarize their output.
    """
    
    def __init__(self):
        """sensor_value is the attribute that each child 
        should fill with the information it publishes.
        """
        self.sensor_value = dict()

    def get_value(self):
        """Returns a dict with the value measured by the sensor and its unit."""
        return self.sensor_value
