# from wind_vane import WindVaneWithIMU
import json
import time
import zmq

from anemometer import AnemometerWithTachometer
from sensors.interfaces import GPIOs
from sensors.tachometer import Tachometer

COMMAND_SEPARATOR = '\n'
PREFIX_COMPLEX_SENSOR_LIST = 'sensors_list'
PREFIX_ANEMOMETER = 'anemometer'
PREFIX_METRIC = 'metric'
PREFIX_ERROR = 'error'

WIND_VANE_LABEL = 'wind_vane'
GPIO_ADDRESS_TACOMETER = 15
PALETA_LONG = 0.1
PUBLISH_TIME = 2

class WeatherStation(object):
    """
    """
    def __init__(self, publisher_port=5555):

        self.publisher_port = publisher_port

        # Inicio context para ZMQ
        self.context = None
        self.ser = None
        self.publisher_socket = None

        self._stop = False
        self.sensors = {}
        self.complex_sensors = {}

    def setup(self):
        self.setup_interfaces()
        self.setup_simple_sensor()
        self.setup_sensors()
        self.setup_sockets()

    def setup_sockets(self):
        self.context = zmq.Context()
        self.publisher_socket = self.context.socket(zmq.PUB)
        self.publisher_socket.bind("tcp://*:{0}".format(self.publisher_port))

    def setup_interfaces(self):
        self.interfaces = {
            'gpios': GPIOs([GPIO_ADDRESS_TACOMETER])
        }

    def setup_simple_sensor(self):
        self.sensors['Tachometer'] = Tachometer(self.interfaces)

    def setup_sensors(self):
        self.complex_sensors['anemometer'] = AnemometerWithTachometer(self.sensors, PALETA_LONG)

    def stop(self):
        """
        Stop the server. You shouldn't extend this function.
        """
        self._stop = True
        self.stop_sockets()

    def stop_sockets(self):
        """
        Stop the zmq sockets of your server.
        """
        self.publisher_socket.close()
        self.context.term()

    def run(self):
        self.setup()

        while not self._stop:
            try:
                sensor_list_msg = '{1}{0}{2}'.format(COMMAND_SEPARATOR,
                                                     PREFIX_COMPLEX_SENSOR_LIST,
                                                     json.dumps([PREFIX_ANEMOMETER]))  # TODO: After complex sensor label implementation change this
                self.publisher_socket.send_string(sensor_list_msg)

                for sensor in self.complex_sensors.values():
                    sensor_values = sensor.get_value()
                    sensor_msg = '{1}{0}{2}{0}{3}'.format(COMMAND_SEPARATOR,
                                                        PREFIX_METRIC,
                                                        PREFIX_ANEMOMETER,  # TODO: Add this as a wind vane class parametter.
                                                        json.dumps(sensor_values))
                    self.publisher_socket.send_string(sensor_msg)
            except Exception as error:
                error_msg = '{1}{0}{2}'.format(COMMAND_SEPARATOR,
                                               PREFIX_ERROR,
                                               error)
                self.publisher_socket.send_string(error_msg)
            finally:
                time.sleep(PUBLISH_TIME)

