import yaml
import time
import Adafruit_BBIO.GPIO as GPIO; 

config_file = open("/srv/robotice/config.yml", "r")

config = yaml.load(config_file)

if config.get("debug"):
	print GPIO
	
GPIO.setup("P8_10", GPIO.OUT)

while True:
	print "a"
	GPIO.output("P8_10", GPIO.HIGH)
	time.sleep(5)
	print "b"
	GPIO.output("P8_10", GPIO.LOW)

GPIO.cleanup()