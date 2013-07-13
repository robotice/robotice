import Adafruit_BBIO.PWM as PWM; 
import time
import yaml

config_file = open("/srv/robotice/config.yml", "r")

config = yaml.load(config_file)

if config.get("debug"):
	print PWM

PWM.cleanup()

while True:
	PWM.start("P8_45", 100)
	print "a"
	time.sleep(5)
	print "B"
	PWM.stop("P8_45")
