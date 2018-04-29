import random
import struct
import time

from sensors.imu01b import (MAG_CONF_ADD_0, OUT_X_H_M, OUT_X_L_M, OUT_Y_H_M,
                            OUT_Y_L_M, OUT_Z_H_M, OUT_Z_L_M, TEMP_OUT_H_M,
                            TEMP_OUT_L_M, MAG_CONF_TEMP_ENABLED)


class MockI2C(object):

    def __init__(self, address):
        self.address = address
        self.actual_temp = 2000
        self.actual_x = 2000
        self.actual_y = 2000
        self.actual_z = 2000

        self.update_values_timeout = time.time()

    def update_values(self):
        self.actual_temp = self.get_random_value(self.actual_temp)
        self.actual_x = self.get_random_value(self.actual_x)
        self.actual_y = self.get_random_value(self.actual_y)
        self.actual_z = self.get_random_value(self.actual_z)

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
            rta = self.get_answer_from_value(self.actual_x, 0)
        elif args[1] == OUT_X_L_M:
            rta = self.get_answer_from_value(self.actual_x, 1)
        elif args[1] == OUT_Y_H_M:
            rta = self.get_answer_from_value(self.actual_y, 0)
        elif args[1] == OUT_Y_L_M:
            rta = self.get_answer_from_value(self.actual_y, 1)
        elif args[1] == OUT_Z_H_M:
            rta = self.get_answer_from_value(self.actual_z, 0)
        elif args[1] == OUT_Z_L_M:
            rta = self.get_answer_from_value(self.actual_z, 1)
        elif args[1] == MAG_CONF_ADD_0:
            return MAG_CONF_TEMP_ENABLED
        else:
            rta = None
        return rta
