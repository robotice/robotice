"""
import Adafruit_BBIO.GPIO as GPIO
from time import sleep

logger = logging.getLogger("robotice")
logger.setLevel(logging.DEBUG)

PORT = "P8_10"
timeout = 2
GPIO.setup(PORT, GPIO.OUT)

while True:
	GPIO.output(PORT, GPIO.HIGH)
	logger.debug("on after %s s timeout" %timeout)
	sleep(timeout)
	GPIO.cleanup()
	GPIO.setup(PORT, GPIO.OUT)
	GPIO.output(PORT, GPIO.LOW)
	logger.debug("off after %s s timeout" %timeout)
	sleep(timeout)	
	GPIO.cleanup()
	GPIO.setup(PORT, GPIO.OUT)
"""


