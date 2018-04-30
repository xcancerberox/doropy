import time

import numpy as np

from sensors import BaseSensor

GPIO_A = 15
GPIO_B = 16


class Encoder(BaseSensor):

    def __init__(self,
                 interfaces,
                 sample_time=2,
                 encoder_pulses=20):
        super().__init__(interfaces)
        self.sensor_read['measurements'] = [{
            'value': None,
            'unit': 'seconds',
            'type': 'encoder'
        }]
        self.sample_time = sample_time
        self.encoder_pulses = encoder_pulses

    def get_a_value(self):
        a_value = self.interfaces['gpios'].get_value(GPIO_A)
        return a_value

    def get_b_value(self):
        b_value = self.interfaces['gpios'].get_value(GPIO_B)
        return b_value

    def get_value(self):
        start = time.time()
        a_value = self.get_a_value()
        pulses = 0
        timeout = time.time() + self.sample_time
        time_cycle = []

        while time.time() < timeout:
            new_a = self.get_a_value()
            if a_value != new_a:
                pulses += 1
                a_value = new_a

            if pulses == self.encoder_pulses * 2:
                pulses = 0
                now = time.time()
                time_cycle.append(now - start)
                start = now
        self.sensor_read['measurements'][0]['value'] = np.mean(time_cycle)
        return self.sensor_read
