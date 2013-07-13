import yaml
import time
import Adafruit_BBIO.GPIO as GPIO; 

config_file = open("/srv/robotice/config.yml", "r")

config = yaml.load(config_file)

if config.get("debug"):
	print GPIO
	
GPIO.setup("P8_16", GPIO.OUT)

while True:
	GPIO.output("P8_16", GPIO.HIGH)
	time.sleep(5)
	GPIO.output("P8_16", GPIO.HIGH)

GPIO.cleanup()