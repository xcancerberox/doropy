import struct

from sensors import BaseSensor

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


class IMU01b(BaseSensor):
    """
    This class represent the IMU01b sensor and handle the interactions with it.

    Should be I2C and SMBUS agnostic for the user.

    For further explanation about whats happening here please refer to `IMU01b documentation <https://www.pololu.com/product/1268>`_

    """

    def __init__(self, interfaces):

        super().__init__(interfaces)
        self.sensor_read['measurements'] = [
            {
                'value': None,
                'unit': 'Gauss',
                'type': 'magnetometer',
            }, {
                'value': None,
                'unit': 'ºC',
                'type': 'thermometer',
            }]

        self.setup()

    def setup(self):
        """
        Check if the temperature sensor is on and enable it if it isn't.
        """
        if not self.temperature_sensor_is_on():
            self.enable_temperature_sensor()

    def get_value(self):
        """
        Read the temperature and magnetometer value and return it according with the BaseSensor specifications.
        """
        self.sensor_read['measurements'][0]['value'] = (self.get_X(), self.get_Y(), self.get_Z())
        self.sensor_read['measurements'][1]['value'] = self.get_temp()
        return self.sensor_read

    def get_X(self):
        """Read the X value from the magnetometer sensor"""
        low_byte = self.interfaces['i2c'].read(MAG_SUB_ADDRESS, OUT_X_L_M)
        high_byte = self.interfaces['i2c'].read(MAG_SUB_ADDRESS, OUT_X_H_M)
        int_value = struct.unpack('H', bytes([low_byte]) + bytes([high_byte]))[0]
        x_value = two_complement_2_decimal(int_value, 16)
        return x_value

    def get_Y(self):
        """Read the Y value from the magnetometer sensor"""
        low_byte = self.interfaces['i2c'].read(MAG_SUB_ADDRESS, OUT_Y_L_M)
        high_byte = self.interfaces['i2c'].read(MAG_SUB_ADDRESS, OUT_Y_H_M)
        int_value = struct.unpack('H', bytes([low_byte]) + bytes([high_byte]))[0]
        y_value = two_complement_2_decimal(int_value, 16)
        return y_value


    def get_Z(self):
        """Read the Z value from the magnetometer sensor"""
        low_byte = self.interfaces['i2c'].read(MAG_SUB_ADDRESS, OUT_Z_L_M)
        high_byte = self.interfaces['i2c'].read(MAG_SUB_ADDRESS, OUT_Z_H_M)
        int_value = struct.unpack('H', bytes([low_byte]) + bytes([high_byte]))[0]
        z_value = two_complement_2_decimal(int_value, 16)
        return z_value

    def get_temp(self):
        """Read the temperature value from the magnetometer temperature sensor"""
        low_byte = self.interfaces['i2c'].read(MAG_SUB_ADDRESS, TEMP_OUT_L_M)
        high_byte = self.interfaces['i2c'].read(MAG_SUB_ADDRESS, TEMP_OUT_H_M)
        temp_value = struct.unpack('H', bytes([low_byte]) + bytes([high_byte]))[0]
        return temp_value

    def temperature_sensor_is_on(self):
        """
        Check if the temperature sensor is ON. Indicated by the higher bit in the
        `MAG_CONF_ADD_0` record.
        """
        byte_conf = self.interfaces['i2c'].read(MAG_SUB_ADDRESS, MAG_CONF_ADD_0)
        temperature_on = (byte_conf & 0b10000000) / 128
        return bool(temperature_on)

    def enable_temperature_sensor(self):
        """
        Enable the temperature sensor, seting to 1 the higher bit in the `MAG_CONF_ADD_0` record.

        returns a bool that indicate if the temperature sensor is ON
        """
        self.interfaces['i2c'].write(MAG_SUB_ADDRESS, MAG_CONF_ADD_0, MAG_CONF_TEMP_ENABLED)
        return self.temperature_sensor_is_on()

