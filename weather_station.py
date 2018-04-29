import struct
import time
import multiprocessing as mp
from threading import Lock, Thread

import zmq

from ClaptonBase.containers import MemoInstance, Node, Package
from ClaptonBase.exceptions import (ChecksumException, InvalidPackage,
                                    NodeNotExists, NoMasterException,
                                    ReadException, TokenExeption,
                                    WriteException)
from ClaptonBase.serial_interface import SerialInterface
from ClaptonBase.utils import get_logger

from .cfg import (CHECK_NODE_PERIOD, COMMAND_SEPARATOR, DEFAULT_BAUDRATE,
                  DEFAULT_LOG_LVL, DEFAULT_PUB_PORT,
                  DEFAULT_SERIAL_CONNECTION_PREFIX, DEFAULT_SERIAL_PORT,
                  DEFAULT_SERIAL_TIMEOUT, DEFAULT_SYSTEM_CONNECTION_PREFIX,
                  LOG_TKLSERIAL, MEMO_READ_NAMES, PUBLISHER_ERROR_PREFIX)



class BaseServer(mp.Process):
    """
    This class provides the main functions of the server architecture, wich are:
        * Initialize the SerialInterface
        * Initialize the publisher socket to report msgs of whatever you want, depending of the server behavior
            In advance always will report the serial port connection system connection
        * Initialize the reporter thread that will report the messages that you want.

    """
    def __init__(self,
                 serial_port=DEFAULT_SERIAL_PORT,
                 baudrate=DEFAULT_BAUDRATE,
                 serial_timeout=DEFAULT_SERIAL_TIMEOUT,
                 publisher_port=DEFAULT_PUB_PORT,
                 command_separator=COMMAND_SEPARATOR,
                 serial_connection_prefix=DEFAULT_SERIAL_CONNECTION_PREFIX,
                 system_connection_prefix=DEFAULT_SYSTEM_CONNECTION_PREFIX,
                 publisher_error_prefix=PUBLISHER_ERROR_PREFIX):

        super().__init__()

        # msgs prefixes and zmq stufs
        self.serial_connection_prefix = serial_connection_prefix
        self.system_connection_prefix = system_connection_prefix
        self.publisher_error_prefix = publisher_error_prefix
        self.command_separator = command_separator
        self.publisher_port = publisher_port

        # serial connection
        self.serial_port = serial_port
        self.baudrate = baudrate
        self.serial_timeout = serial_timeout

        # Inicio context para ZMQ
        self.context = None
        self.ser = None
        self.publisher_socket = None

        # Bandera de parada para los Threads
        self.stop = False

    def setup(self):
        self.setup_context()
        self.setup_sockets()
        self.setup_processes()

    def setup_context(self):
        self.ser = SerialInterface(serial_port=self.serial_port,
                                   baudrate=self.baudrate,
                                   timeout=self.serial_timeout)
        self.context = zmq.Context()

    def setup_sockets(self):
        self.publisher_socket = self.context.socket(zmq.PUB)
        self.publisher_socket.bind("tcp://*:{0}".format(self.publisher_port))

    def setup_processes(self):
        """
        Start the threads of your server.
        If you want to run aditional threads you should extend this function
        to start them::

            class YourCustomServer(BaseServer):

                def start_threads(self):
                    super().start_threads()
                    self.your_custom_thread.start()

                def stop_threads(self):
                    super().stop_threads()
                    self.your_custom_thread.join()

        Be aware to also stop your custom threads in :func:`stop_threads`
        """
        pass

    def join(self, *args, **kwargs):
        """
        Stop the server. You shouldn't extend this function.
        """
        self.stop = True
        self.stop_processes()
        self.stop_sockets()
        self.ser.stop()
        super().join(*args, **kwargs)

    def stop_processes(self):
        """
        Stop the threads of your server.
        If you want to run aditional threads and you alredy registered to be started :func:`start_threads`
        you should extend this function to stop them::

            class YourCustomServer(BaseServer):

                ...

                def start_threads(self):
                    super().start_threads()
                    self.your_custom_thread.start()

                def stop_threads(self):
                    super().stop_threads()
                    self.your_custom_thread.join()

        """
        pass

    def stop_sockets(self):
        """
        Stop the zmq sockets of your server.
        If you want to run aditional sockets you should extend this function to start them.
        Be aware that you should do it *before* the function base execution::

            class YourCustomServer(BaseServer):

                ...

                def stop_sockets(self):
                    self.your_custom_socket.close()
                    super().stop_sockets()

        """
        self.publisher_socket.close()
        self.context.term()

    def run_when_master(self):
        """
        Run the function that `reporter_thread` runs when you are master.
        In the BaseServer this function do nothing, so you can replace it if you want to run aditional functions::

            class YourCustomServer(BaseServer):

                ...

                def run_when_master(self):
                    self.do_something_as_master()

        """
        pass

    def run_when_slave(self):
        """
        Run the function that `reporter_thread` runs when you are slave.
        In the BaseServer this function do nothing, so you can replace it if you want to run aditional functions::

            class YourCustomServer(BaseServer):

                ...

                def run_when_slave(self):
                    self.do_something_as_slave()

        """
        pass

    def run_always(self):
        """
        Run the function that `reporter_thread` runs *always*. Doesn't matter if you are master or slave.
        In the BaseServer this function make the system and serial connections report.
        If you want to run aditional functions you should extend this function::

            class YourCustomServer(BaseServer):

                ...

                def run_always(self):
                    self.do_something_always()
                    super().run_always()
        """
        self.report_serial_connection()
        self.report_system_connection()

    def report_serial_connection(self):
        msg = '{1}{0}{2}'.format(self.command_separator,
                                 self.serial_connection_prefix,
                                 int(self.ser._ser.isOpen()))
        self.publisher_socket.send_string(msg)


    def report_system_connection(self):
        pass

    def run(self):
        self.setup()

        while not self.stop:
            try:
                if self.ser.im_master:
                    self.run_when_master()
                else:
                    self.run_when_slave()
                self.run_always()
            except Exception as error:
                error_msg = '{1}{0}{2}'.format(self.command_separator,
                                               self.publisher_error_prefix,
                                               error)
                self.publisher_socket.send_string(error_msg)

