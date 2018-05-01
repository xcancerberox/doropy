import random
import struct
import time
from multiprocessing import Lock
from sensors.imu01b import (MAG_CONF_ADD_0, MAG_CONF_TEMP_ENABLED, OUT_X_H_A,
                            OUT_X_H_M, OUT_X_L_A, OUT_X_L_M, OUT_Y_H_A,
                            OUT_Y_H_M, OUT_Y_L_A, OUT_Y_L_M, OUT_Z_H_A,
                            OUT_Z_H_M, OUT_Z_L_A, OUT_Z_L_M, TEMP_OUT_H_M,
                            TEMP_OUT_L_M)


class MockGPIO(object):

    _instance = None

    def __init__(self):
        self.IN = 1
        self.OUT = 2
        # self.responses_cache = {1: 1}
        self._update_cache_lock = Lock()

    def setup(cls, address, mode):
        pass

    def reset_cache(self):
        with self._update_cache_lock:
            self.responses_cache = {1: 1}

    def update_response_value(self, address, value):
        # with self._update_cache_lock:
        # self.responses_cache[address] = value
        print("Updated to: {}".format(self.responses_cache[address]))
        print("Update GPIO.cache ID: {}".format(id(self.responses_cache)))

    def _get_response_value(self, address):
        # if address not in self.responses_cache.keys():
            # print("New address {}".format(address))
            # self.update_response_value(address, 1)
        # with self._update_cache_lock:
        print("Cache value: {}".format(self.responses_cache[address]))
        print("Update GPIO.cache ID: {}".format(id(self.responses_cache)))
        return self.responses_cache[address]

    def input(self, address):
        return self._get_response_value(address)

    def setmode(self, mode):
        pass

    @classmethod
    def instance(cls):
        if not cls._instance:
            cls._instance = cls()
        return cls._instance


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
