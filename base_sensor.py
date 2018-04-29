import struct

import smbus

SMBUS_ADDRESS = 1
MAG_SUB_ADDRESS = 0x1e
OUT_X_H_M = 0x03
OUT_X_L_M = 0x04
OUT_Z_H_M = 0x05
OUT_Z_L_M = 0x06
OUT_Y_H_M = 0x07
OUT_Y_L_M = 0x08
MAG_CONF_ADD_0 = 0x00
MAG_CONF_TEMP_ENABLED = 0x90
TEMP_OUT_H_M = 0x31
TEMP_OUT_L_M = 0x32


def two_complement_2_decimal(value, n_bits):
    """Converts a two's component binary integer into a decimal integer."""
    for current_bit in range(n_bits):
        bit = (value >> current_bit) & 1
        if bit == 1:
            left_part = value >> (current_bit + 1)
            left_mask = 2**(n_bits - (current_bit + 1)) - 1
            right_mask = 2**(current_bit + 1)-1
            right_part = value & right_mask
            out = ((~left_part & left_mask) << (current_bit + 1)) + right_part
            if out >> (n_bits - 1):
                out = -value
            return out
    return 0


class BaseSensor(object):
    """
    Represent a sensor that return his value.
    This don't represent a meteorologic metric yet,
    is just a resource to be used to be parsed (in
    combination with onther sensors values) in order
    to obtain a meteorologic metric.

    The use of this class should be hardware agnostic.    """

    def __init__(self):

        self.sensor_read = dict()

    def get_value(self):
        """
        This should return a dict where the key are the
        sensor metric name and his value for each metric
        that the sensor could sense.
        """
        return self.sensor_read


class IMU01b(BaseSensor):
    """
    This class represent the IMU01b sensor and handle the interactions with it.

    Should be I2C and SMBUS agnostic for the user.

    For further explanation about whats happening here please refer to `IMU01b documentation <https://www.pololu.com/product/1268>`_

    """

    def __init__(self):

        super().__init__()
        self._bus = None
        self.setup()

    def setup(self):
        """
        Initalize the bus for i2C interactions and check
        if the temperature sensor is on.
        """
        self._bus = smbus.SMBus(1)
        if not self.temperature_sensor_is_on():
            now_it_is = self.enable_temperature_sensor()  # TODO: if it isn't should anyway return the only mangetometer value?
            if not now_it_is:
                raise Exception

    def get_value(self):
        """
        Read the temperature and magnetometer value and return it according with the BaseSensor specifications.
        """
        self.sensor_read['magnetometer'] = (self.get_X(), self.get_Y(), self.get_Z())
        self.sensor_read['temperature'] = None

        return self.sensor_read

    def get_X(self):
        """Read the X value from the magnetometer sensor"""
        low_byte = self._bus.read_byte_data(MAG_SUB_ADDRESS, OUT_X_L_M)
        high_byte = self._bus.read_byte_data(MAG_SUB_ADDRESS, OUT_X_H_M)
        int_value = struct.unpack('H', bytes([low_byte]) + bytes([high_byte]))[0]
        x_value = two_complement_2_decimal(int_value, 16)
        return x_value

    def get_Y(self):
        """Read the Y value from the magnetometer sensor"""
        low_byte = self._bus.read_byte_data(MAG_SUB_ADDRESS, OUT_Y_L_M)
        high_byte = self._bus.read_byte_data(MAG_SUB_ADDRESS, OUT_Y_H_M)
        int_value = struct.unpack('H', bytes([low_byte]) + bytes([high_byte]))[0]
        y_value = two_complement_2_decimal(int_value, 16)
        return y_value


    def get_Z(self):
        """Read the Z value from the magnetometer sensor"""
        low_byte = self._bus.read_byte_data(MAG_SUB_ADDRESS, OUT_Z_L_M)
        high_byte = self._bus.read_byte_data(MAG_SUB_ADDRESS, OUT_Z_H_M)
        int_value = struct.unpack('H', bytes([low_byte]) + bytes([high_byte]))[0]
        z_value = two_complement_2_decimal(int_value, 16)
        return z_value

    def get_temp(self):
        """Read the temperature value from the magnetometer temperature sensor"""
        low_byte = self._bus.read_byte_data(MAG_SUB_ADDRESS, TEMP_OUT_L_M)
        high_byte = self._bus.read_byte_data(MAG_SUB_ADDRESS, TEMP_OUT_H_M)
        temp_value = struct.unpack('H', bytes([low_byte]) + bytes([high_byte]))[0]
        return temp_value

    def temperature_sensor_is_on(self):
        """
        Check if the temperature sensor is ON. Indicated by the higher bit in the
        `MAG_CONF_ADD_0` record.
        """
        byte_conf = self._bus.read_byte_data(MAG_SUB_ADDRESS, MAG_CONF_ADD_0)
        temperature_on = (byte_conf & 0b10000000) / 128
        return bool(temperature_on)

    def enable_temperature_sensor(self):
        """
        Enable the temperature sensor, seting to 1 the higher bit in the `MAG_CONF_ADD_0` record.

        returns a bool that indicate if the temperature sensor is ON
        """
        self._bus.write_byte_data(MAG_SUB_ADDRESS, MAG_CONF_ADD_0, MAG_CONF_TEMP_ENABLED)
        return self.temperature_sensor_is_on()

