import pytest
from sensors import BaseSensor, imu01b


class TestBaseSensor(object):

    def test_init(self):
        interfaces = {'12c': None}
        sensor_instace = BaseSensor(interfaces)
        assert sensor_instace.interfaces is interfaces
        assert isinstance(sensor_instace.sensor_read, dict)

    def test_init_raises_type_error(self):
        with pytest.raises(TypeError):
            BaseSensor()


class TestIMU01b(object):


    def test_init(self, i2c_imu01b):
        imu_instance = imu01b.IMU01b(i2c_imu01b)

        sensors_types = [sensor['type'] for sensor in imu_instance.sensor_read['measurements']]
        assert sensors_types == ['magnetometer', 'thermometer', 'accelerometer']

    @pytest.mark.parametrize("readed_bytes,expected", [
        ([0x50, 0xc3], 15536),
        ([0x20, 0x4e], -20000),
        ([0xed, 0xf3], 3091),
    ])
    def test_get_acc_x(self, i2c_imu01b, readed_bytes, expected):
        i2c_imu01b['i2c'].read_values.extend(readed_bytes)
        imu_instance = imu01b.IMU01b(i2c_imu01b)
        x_value = imu_instance.get_acc_X()
        assert x_value == expected

    @pytest.mark.parametrize("readed_bytes,expected", [
        ([0x50, 0xc3], 15536),
        ([0x20, 0x4e], -20000),
        ([0xed, 0xf3], 3091),
    ])
    def test_get_acc_y(self, i2c_imu01b, readed_bytes, expected):
        i2c_imu01b['i2c'].read_values.extend(readed_bytes)
        imu_instance = imu01b.IMU01b(i2c_imu01b)
        y_value = imu_instance.get_acc_Y()
        assert y_value == expected

    @pytest.mark.parametrize("readed_bytes,expected", [
        ([0x50, 0xc3], 15536),
        ([0x20, 0x4e], -20000),
        ([0xed, 0xf3], 3091),
    ])
    def test_get_acc_z(self, i2c_imu01b, readed_bytes, expected):
        i2c_imu01b['i2c'].read_values.extend(readed_bytes)
        imu_instance = imu01b.IMU01b(i2c_imu01b)
        z_value = imu_instance.get_acc_Z()
        assert z_value == expected
    @pytest.mark.parametrize("readed_bytes,expected", [
        ([0x50, 0xc3], 15536),
        ([0x20, 0x4e], -20000),
        ([0xed, 0xf3], 3091),
    ])
    def test_get_mag_x(self, i2c_imu01b, readed_bytes, expected):
        i2c_imu01b['i2c'].read_values.extend(readed_bytes)
        imu_instance = imu01b.IMU01b(i2c_imu01b)
        x_value = imu_instance.get_mag_X()
        assert x_value == expected

    @pytest.mark.parametrize("readed_bytes,expected", [
        ([0x50, 0xc3], 15536),
        ([0x20, 0x4e], -20000),
        ([0xed, 0xf3], 3091),
    ])
    def test_get_mag_y(self, i2c_imu01b, readed_bytes, expected):
        i2c_imu01b['i2c'].read_values.extend(readed_bytes)
        imu_instance = imu01b.IMU01b(i2c_imu01b)
        y_value = imu_instance.get_mag_Y()
        assert y_value == expected

    @pytest.mark.parametrize("readed_bytes,expected", [
        ([0x50, 0xc3], 15536),
        ([0x20, 0x4e], -20000),
        ([0xed, 0xf3], 3091),
    ])
    def test_get_mag_z(self, i2c_imu01b, readed_bytes, expected):
        i2c_imu01b['i2c'].read_values.extend(readed_bytes)
        imu_instance = imu01b.IMU01b(i2c_imu01b)
        z_value = imu_instance.get_mag_Z()
        assert z_value == expected

    @pytest.mark.parametrize("readed_bytes,expected", [
        ([0x50, 0xc3], 50000),
        ([0x20, 0x4e], 20000),
        ([0xed, 0xf3], 62445),
    ])
    def test_get_temp(self, i2c_imu01b, readed_bytes, expected):
        i2c_imu01b['i2c'].read_values.extend(readed_bytes)
        imu_instance = imu01b.IMU01b(i2c_imu01b)
        temp_value = imu_instance.get_temp()
        assert temp_value == expected

    @pytest.mark.parametrize("readed_bytes,expected", [
        ([0x80, ], True),
        ([0x0f, ], False),
        ([0x5f, ], False),
        ([0xff, ], True)
    ])
    def test_temperature_sensor_is_on(self, i2c_imu01b, readed_bytes, expected):
        i2c_imu01b['i2c'].read_values.extend(readed_bytes)
        imu_instance = imu01b.IMU01b(i2c_imu01b)
        assert imu_instance.temperature_sensor_is_on() == expected

    @pytest.mark.parametrize("readed_bytes,expected", [
        ([0x80, ], True),
        ([0x0f, ], False),
        ([0x5f, ], False),
        ([0xff, ], True)
    ])
    def test_enable_temperature_sensor(self, i2c_imu01b, readed_bytes, expected):
        i2c_imu01b['i2c'].read_values.extend(readed_bytes)
        imu_instance = imu01b.IMU01b(i2c_imu01b)
        assert imu_instance.enable_temperature_sensor() == expected

    # def test_get_value(self, i2c_imu01b, readed_bytes, expected):
        # pass
