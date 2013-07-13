import yaml
import Adafruit_BBIO.PWM as PWM; 
import time

config_file = open("/srv/robotice/config.yml", "r")

config = yaml.load(config_file)

if config.get("debug"):
	print PWM

while True:
	PWM.start("P8_45", 100)
	time.sleep(5)
	PWM.stop("P8_45")

PWM.cleanup()	