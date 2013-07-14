import yaml
import Adafruit_BBIO.GPIO as GPIO
from time import sleep

config_file = open("/srv/robotice/config.yml", "r")

config = yaml.load(config_file)

if config.get("debug"):
	print GPIO

rele_port = "P8_10"
timeout = 2
#GPIO.setup("P8_41", GPIO.OUT)
GPIO.setup(rele_port, GPIO.OUT)
while True:
	GPIO.output(rele_port, GPIO.HIGH)
	#PIO.output("P8_41", GPIO.HIGH)
	print "on after %s s timeout" %timeout
	sleep(timeout)
	GPIO.cleanup()
	GPIO.setup(rele_port, GPIO.OUT)
	GPIO.output(rele_port, GPIO.LOW)
	print "off after %s s timeout" %timeout
	#GPIO.output("P8_41", GPIO.LOW)
	sleep(timeout)	
	GPIO.cleanup()
	GPIO.setup(rele_port, GPIO.OUT)


