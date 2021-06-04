import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BOARD)
GPIO.setup(31, GPIO.IN)


while True:
	print(GPIO.input(31))
	time.sleep(0.5)




