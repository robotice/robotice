"""
import Adafruit_BBIO.ADC as ADC
from time import sleep
 
sensor_pin = 'P8.10'
ADC.cleanup()
ADC.setup()
 
print('Reading\t\tVolts')
 
MAX = 0 
while True:
    reading = ADC.read(sensor_pin)
    if reading > MAX:
    	MAX = reading
    volts = reading * 1.800
    print('%f\tmax is: %f' % (reading, MAX))
    sleep(1)
"""
