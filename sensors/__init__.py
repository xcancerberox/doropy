

class BaseSensor(object):
    """
    Represent a sensor that return his value.
    This don't represent a meteorologic metric yet,
    is just a resource to be used to be parsed (in
    combination with onther sensors values) in order
    to obtain a meteorologic metric.

    params:
        :param interfaces: Dictionary with the avaliable interfaces
            to use giving a specific hardware (for now a Raspberry Pi)
        :interfaces type: dict
    """


    def __init__(self, interfaces):
        self.interfaces = interfaces
        self.sensor_read = {
            'sensor_id': type(self).__name__.lower(),
            'measurements': []
        }

    def get_value(self):
        """
        This should return a dict where the key are the
        sensor metric name and his value for each metric
        that the sensor could sense.
        """
        return self.sensor_read


