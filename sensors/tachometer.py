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
            'unit': 'time in seconds to rotate 360º',
            'type': 'tachometer'
        }]
        self.encoder_pulses = encoder_pulses

    def get_records_list(self):
        """
        Get the records list of the GPIO.
        The value is the same that the returned by `GPIOs.get_records()` method.
        """
        a_values = self.interfaces['gpios'].get_records(GPIO_A)
        return a_values

    def get_value(self):
        """
        Calculate the time to rotate 360º of the last stamples taken for the GPIOProcess.
        """

        records = self.get_records_list()
        if records:
            cycles = len(records) / (self.encoder_pulses * 2)
            total_time = records[-1].time - records[0].time
            cycle_time_avg = total_time / cycles
        else:
            cycle_time_avg = 0
        self.sensor_read['measurements'][0]['value'] = cycle_time_avg
        return self.sensor_read
