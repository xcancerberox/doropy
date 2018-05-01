import time
from sensors.interfaces import GPIOs
from sensors.tachometer import Tachometer
from anemometer import AnemometerWithTachometer

GPIO_ADDRESS_A = 15


interfaces = {'gpios': GPIOs([GPIO_ADDRESS_A])}
tachometer = Tachometer(interfaces)
sensors = {'Tachometer': tachometer}

anemometer = AnemometerWithTachometer(sensors, 0.1)

while True:
    print(anemometer.get_value())
    #print(tachometer.get_value())
    time.sleep(1)

