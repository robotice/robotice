"""
import RPi.GPIO as GPIO
from time import sleep

logger = logging.getLogger("robotice")
logger.setLevel(logging.DEBUG)

PORT = 18
timeout = 2

#rpi extender or GPIO.BOARD 
GPIO.setmode(GPIO.BCM)
GPIO.setup(PORT, GPIO.OUT)

#GPIO.setup("P8_41", GPIO.OUT)
GPIO.setup(PORT, GPIO.OUT)
while True:
	GPIO.output(PORT, True)
	logger.debug("on after %s s timeout" %timeout)
	sleep(timeout)
	GPIO.output(PORT, False)
	logger.debug("off after %s s timeout" %timeout)
	sleep(timeout)	
"""