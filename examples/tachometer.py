from sensors.interfaces import GPIOs
from sensors.tachometer import Tachometer

GPIO_ADDRESS_A = 15

gpios = GPIOs([GPIO_ADDRESS_A, ])
interfaces = {
    'gpios': gpios,
}

encoder = Tachometer(interfaces)
print(encoder.get_value())
