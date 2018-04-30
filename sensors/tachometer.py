from sensors import BaseSensor

GPIO_A = 15
GPIO_B = 16


class Tachometer(BaseSensor):
    """
    Tachometer sensor implemented with an *BI EN11 HSM5A* encoder.

    Measure the average time to rotate 360º.
    """

    def __init__(self,
                 interfaces,
                 encoder_pulses=20):
        super().__init__(interfaces)
        self.sensor_read['measurements'] = [{
            'value': None,
            'unit': 'seconds',
            'type': 'average time per turn'
        }]
        self.encoder_pulses = encoder_pulses

    def get_records_list(self):
        """
        Gets the records list of the GPIO.
        The value is the same as the one returned by `GPIOs.get_records()` method.
        """
        a_values = self.interfaces['gpios'].get_records(GPIO_A)
        return a_values

    def get_value(self):
        """
        Calculates the average time per turn from
        the last stamples taken by the GPIOProcess.
        """
        records = self.get_records_list()
        cycles = len(records)
        total_time = records[-1].time - records[0].time
        cylce_time_avg = total_time / cycles
        self.sensor_read['measurements'][0]['value'] = cylce_time_avg
        return self.sensor_read
