from sensors.interfaces import GPIOs
from sensors.encoder import Encoder

GPIO_ADDRESS_A = 15
GPIO_ADDRESS_B = 16

gpios = GPIOs([GPIO_ADDRESS_A, GPIO_ADDRESS_B])
interfaces = {
    'gpios': gpios,
}

encoder = Encoder(interfaces)
print(encoder.get_value())
