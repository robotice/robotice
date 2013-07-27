#!/usr/bin/python
import argparse

p = argparse.ArgumentParser(description="Parse command arameters.")

p.add_argument("-p", "--port")
p.add_argument("-a", "--arch")

opts = p.parse_args()

def get_cds_data(sensor):
    if device = "rpi":
      import Adafruit_BBIO.ADC as ADC

	    ADC.setup()
	    reading = ADC.read(opts.port)

    if device = "beagle":
	    import RPi.GPIO as GPIO

	    GPIO.setmode(GPIO.BCM)

	    GPIO.setup(opts.port, GPIO.IN)
      reading = GPIO.input(opts.port)
	    GPIO.cleanup()
      
    return reading