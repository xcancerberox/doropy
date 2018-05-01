import random
import struct
import time

import multiprocessing as mp

from sensors.imu01b import (MAG_CONF_ADD_0, MAG_CONF_TEMP_ENABLED, OUT_X_H_A,
                            OUT_X_H_M, OUT_X_L_A, OUT_X_L_M, OUT_Y_H_A,
                            OUT_Y_H_M, OUT_Y_L_A, OUT_Y_L_M, OUT_Z_H_A,
                            OUT_Z_H_M, OUT_Z_L_A, OUT_Z_L_M, TEMP_OUT_H_M,
                            TEMP_OUT_L_M)

import RPi.GPIO as GPIO


Q_SIZE = 10000
SAMPLE_TIME = 0


class GPIORecord(object):
    """Dummy container for a GPIO record readed in a specific time"""

    def __init__(self, value):
        self.value = value
        self.time = time.time()


class GPIOProcess(mp.Process):
    """
    This class define a GPIO process that keep reading the GPIO port in
    a `SAMPLE_TIME` period and store it in a queue.

    params:
        :param address: The GPIO addres using GPIO.BOARD system.
    """
    def __init__(self, address, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.address = address
        self.queue = mp.Queue(Q_SIZE)
        self.last_record = GPIORecord(None)
        self._stop = False
        GPIO.setup(address, GPIO.IN)

    def run(self):
        """
        Start the sample process:
            * Read the GPIO value giving the address.
            * If the new value is different than the last value, save it in the queue.
            * Wait `SAMPLE_TIME` seconds.
        """
        while not self._stop:
            new_value = GPIO.input(self.address)
            #print(new_value)
            if new_value != self.last_record.value:
                new_record = GPIORecord(new_value)
                self.last_record = new_record
                self.queue.put(new_record)
            time.sleep(SAMPLE_TIME)

    def join(self):
        """
        Set the `_stop` flag to ``True`` and join the process
        """
        self._stop = True
        super().join()


class GPIOs(object):
    """
    This class handle the GPIOs Processes and serve the methods
    to access the values.

    params:
        :param address: List of `GPIO.BOARD` addresses to read.

    """

    def __init__(self, addresses):
        self.addresses = addresses
        self.gpios = dict()
        self.setup()

    def setup(self):
        """
        Set the GPIO to use BOARD addresses and run `_init_gpios`
        """
        GPIO.setmode(GPIO.BOARD)
        self._init_gpios()

    def _init_gpios(self):
        """
        For each GPIO address Initialize the `GPIOProcess` and save it.
        """
        for address in self.addresses:
            gpio_process = GPIOProcess(address)
            gpio_process.start()
            self.gpios[address] = gpio_process

    def stop(self):
        for gpio_process in self.gpios:
            gpio_process.join()

    def get_last_record(self, address):
        """
        Get the last record of a gpio with the given address
        """
        return self.gpios[address].last_record

    def get_records(self, address, n_records=200):
        """
        Get `n_records` of the `GPIOProcess` queue. As default return the max size of the queue.
        It could return less values in case that ``gpio_process.queue.qsize() < n_records``.

        Return a list of `GPIORecord` instances.
        """
        gpio_process = self.gpios[address]
        records = []
        for i in range(n_records):
            if not gpio_process.queue.empty():
                records.append(gpio_process.queue.get())
        return records


class MockI2C(object):

    def __init__(self, address):
        self.address = address
        self.actual_temp = 2000
        self.actual_mag_x = 2000
        self.actual_mag_y = 2000
        self.actual_mag_z = 2000
        self.actual_acc_x = 2000
        self.actual_acc_y = 2000
        self.actual_acc_z = 2000

        self.update_values_timeout = time.time()

    def update_values(self):
        self.actual_temp = self.get_random_value(self.actual_temp)
        self.actual_mag_x = self.get_random_value(self.actual_mag_x)
        self.actual_mag_y = self.get_random_value(self.actual_mag_y)
        self.actual_mag_z = self.get_random_value(self.actual_mag_z)
        self.actual_acc_x = self.get_random_value(self.actual_acc_x)
        self.actual_acc_y = self.get_random_value(self.actual_acc_y)
        self.actual_acc_z = self.get_random_value(self.actual_acc_z)

    def get_random_value(self, previous):
        return int(previous + random.random()*2.5 * random.choice([1, -1]))

    def get_answer_from_value(self, value, index):
        return struct.pack('h', value)[index]

    def write(self, *args):
        pass

    def read(self, *args):
        if time.time() > self.update_values_timeout:
            self.update_values()
            self.update_values_timeout = time.time() + 1

        if args[1] == TEMP_OUT_H_M:
            rta = self.get_answer_from_value(self.actual_temp, 0)
        elif args[1] == TEMP_OUT_L_M:
            rta = self.get_answer_from_value(self.actual_temp, 1)
        elif args[1] == OUT_X_H_M:
            rta = self.get_answer_from_value(self.actual_mag_x, 0)
        elif args[1] == OUT_X_L_M:
            rta = self.get_answer_from_value(self.actual_mag_x, 1)
        elif args[1] == OUT_Y_H_M:
            rta = self.get_answer_from_value(self.actual_mag_y, 0)
        elif args[1] == OUT_Y_L_M:
            rta = self.get_answer_from_value(self.actual_mag_y, 1)
        elif args[1] == OUT_Z_H_M:
            rta = self.get_answer_from_value(self.actual_mag_z, 0)
        elif args[1] == OUT_Z_L_M:
            rta = self.get_answer_from_value(self.actual_mag_z, 1)
        elif args[1] == OUT_X_H_A:
            rta = self.get_answer_from_value(self.actual_acc_x, 0)
        elif args[1] == OUT_X_L_A:
            rta = self.get_answer_from_value(self.actual_acc_x, 1)
        elif args[1] == OUT_Y_H_A:
            rta = self.get_answer_from_value(self.actual_acc_y, 0)
        elif args[1] == OUT_Y_L_A:
            rta = self.get_answer_from_value(self.actual_acc_y, 1)
        elif args[1] == OUT_Z_H_A:
            rta = self.get_answer_from_value(self.actual_acc_z, 0)
        elif args[1] == OUT_Z_L_A:
            rta = self.get_answer_from_value(self.actual_acc_z, 1)
        elif args[1] == MAG_CONF_ADD_0:
            return MAG_CONF_TEMP_ENABLED
        else:
            rta = None
        return rta
