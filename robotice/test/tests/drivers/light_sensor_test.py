"""
import Adafruit_BBIO.ADC as ADC
from time import sleep
 
sensor_pin = 'P9_38'
 
ADC.setup()
 
print('Reading\t\tVolts')
 
while True:
    reading = ADC.read(sensor_pin)
    volts = reading * 1.800
    print('%f\t%f' % (reading, volts))
    sleep(1)
"""