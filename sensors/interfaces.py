from threading import Thread
from queue import Queue
import time
from collections import namedtuple

try:
    import RPi.GPIO as GPIO
except ImportError:
    from sensors.mocks import MockGPIO
    GPIO = MockGPIO.instance()

Q_SIZE = 10000
SAMPLE_TIME = 0


class GPIORecord1(object):
    """Dummy container for a GPIO record readed in a specific time"""

    def __init__(self, value):
        self.value = value
        self.time = time.time()

GPIORecord = namedtuple('GPIORecord', 'value time')



class GPIOProcess(Thread):
    """
    This class define a GPIO process that keep reading the GPIO port in
    a `SAMPLE_TIME` period and store it in a queue.

    params:
        :param address: The GPIO addres using GPIO.BOARD system.
    """
    def __init__(self, address, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.address = address
        self.queue = Queue()
        self.last_record = GPIORecord(None, time.time())
        GPIO.setup(address, GPIO.IN)

    def check_for_new_value(self):
        """
        Check if the value in the GPIO is different than the last one.
        If it is, return a `GPIORecord`
        """
        new_value = GPIO.input(self.address)
        if new_value != self.last_record.value:
            new_record = GPIORecord(new_value, time.time())
            self.last_record = new_record
            return self.last_record
        return

    def run(self):
        """
        Start the sample process.
            * Check for new values.
            * If there is a new value, save it in the queue.
            * Wait `SAMPLE_TIME` seconds.
        """
        while True:
            new_record = self.check_for_new_value()
            if new_record:
                self.queue.put(new_record)
            time.sleep(SAMPLE_TIME)

    def exit(self):
        """
        Set the `_stop` flag to ``True`` and join the process
        """
        pass


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
                try:
                    records.append(gpio_process.queue.get())
                    gpio_process.queue.task_done()
                except Queue.Empty as e:
                    print("No hubo datos")
        return records

