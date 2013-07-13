import yaml
import time
import Adafruit_BBIO.GPIO as GPIO; 

config_file = open("/srv/robotice/config.yml", "r")

config = yaml.load(config_file)

if config.get("debug"):
	print GPIO
GPIO.cleanup()
GPIO.setup("P8_10", GPIO.OUT)

while True:
	GPIO.output("P8_10", GPIO.HIGH)
	time.sleep(0.4)
	GPIO.output("P8_10", GPIO.LOW)
	time.sleep(0.4)