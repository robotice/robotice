import Adafruit_BBIO.ADC as ADC
import time
 
sensor_pin = 'P9_40'
 
ADC.setup()
 
print('Reading\t\tVolts')
 
MAX = 0 
while True:
    reading = ADC.read(sensor_pin)
    if reading > MAX:
    	MAX = reading
    volts = reading * 1.800
    print('%f\tmax is: %f' % (reading, MAX))
    time.sleep(1)