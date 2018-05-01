from sensors.interfaces import GPIOs, GPIOProcess
import time
GPIO_ADDRESS_A = 15
gpios = GPIOs([GPIO_ADDRESS_A])
while 1:
    records = gpios.get_records(GPIO_ADDRESS_A)
    time.sleep(.5)
    print(len(records))

