import yaml
import time
import Adafruit_BBIO.GPIO as GPIO

config_file = open("/srv/robotice/config.yml", "r")

config = yaml.load(config_file)

if config.get("debug"):
	print GPIO

RELE_PORT = "P8_10"

#GPIO.setup("P8_41", GPIO.OUT)
GPIO.setup(RELE_PORT, GPIO.OUT)
while True:
	GPIO.output(RELE_PORT, GPIO.HIGH)
	#PIO.output("P8_41", GPIO.HIGH)
	time.sleep(2)
	GPIO.cleanup()
	GPIO.setup(RELE_PORT, GPIO.OUT)
	GPIO.output(RELE_PORT, GPIO.LOW)
	#GPIO.output("P8_41", GPIO.LOW)
	time.sleep(2)
	GPIO.cleanup()
	GPIO.setup(RELE_PORT, GPIO.OUT)


