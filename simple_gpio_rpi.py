import yaml
import RPi.GPIO as GPIO
import time

config_file = open("/srv/robotice/config.yml", "r")

config = yaml.load(config_file)

if config.get("debug"):
	print GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.OUT)

while True:
	GPIO.output(18, False)
	time.sleep(5)
	GPIO.output(18, True)