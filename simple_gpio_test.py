import RPi.GPIO as GPIO
import time

while True:
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(18, GPIO.OUT)
	GPIO.output(18, False)
	time.sleep(5)
	GPIO.output(18, True)