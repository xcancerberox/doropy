import time
import pytest
from sensors.interfaces import GPIOProcess, GPIORecord, GPIOs
from sensors.mocks import MockGPIO
import multiprocessing as mp

DUMMY_GPIO_ADDRESS = 1  # Just a dummy gpio address

class TestGPIORecord(object):

    def test_init_ok(self):
        record = GPIORecord(1)
        assert record.value == 1
        assert isinstance(record.time, float)


class TestGPIOProcess(object):

    def test_init_ok(self):
        gpio_queue = mp.Queue(10)
        gpio_process = GPIOProcess(DUMMY_GPIO_ADDRESS, gpio_queue)
        assert isinstance(gpio_process, GPIOProcess)
        assert gpio_process.address == DUMMY_GPIO_ADDRESS
        assert isinstance(gpio_process.last_record, GPIORecord)

    def test_check_new_value_return_gpio_record(self, gpio_instance):
        gpio_queue = mp.Queue(10)
        gpio_process = GPIOProcess(DUMMY_GPIO_ADDRESS, gpio_queue)
        gpio_queue.put(1)
        time.sleep(1)
        print(gpio_queue.empty())
        gpio_record = gpio_process.check_for_new_value()
        assert isinstance(gpio_record, GPIORecord)
        assert gpio_record.value == 1
        gpio_queue.put(0)
        time.sleep(1)
        new_gpio_record = gpio_process.check_for_new_value()
        assert new_gpio_record.value == 0

    def test_check_new_value_return_none(self):
        gpio_queue = mp.Queue(10)
        gpio_process = GPIOProcess(DUMMY_GPIO_ADDRESS, gpio_queue)
        gpio_record = gpio_process.check_for_new_value()
        gpio_record_shoud_be_none = gpio_process.check_for_new_value()
        assert not gpio_record_shoud_be_none

    def test_queue_store_noting_if_gpio_not_change(self):
        print("INIT TEST")
        gpio_queue = mp.Queue(10)
        gpio_process = GPIOProcess(DUMMY_GPIO_ADDRESS, gpio_queue)
        gpio_queue.put(1)
        gpio_process.start()
        queued_record_1 = gpio_process.queue.get()
        assert isinstance(queued_record_1, GPIORecord)
        assert queued_record_1.value == 1
        gpio_queue.put(0)
        queued_record_0 = gpio_process.queue.get()
        assert isinstance(queued_record_0, GPIORecord)
        assert queued_record_0.value == 0
        assert gpio_process.queue.empty()
        gpio_queue.put(-1)
        gpio_queue.cancel_join_thread()
        gpio_queue.close()
        gpio_process.exit()

    def test_queue_store_value_if_gpio_change(self):
        pass

    def test_join_process(self):
        pass


class TestGPIOs(object):

    def test_init_ok(self):
        pass

    def test_init_gpios(self):
        pass

    def test_get_last_record(self):
        pass

    def test_get_records(self):
        pass
