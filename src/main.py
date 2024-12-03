import RPi.GPIO as GPIO

from System import *

def main():
    try:
        GPIO.setmode(GPIO.BCM)
        system = System()
        system.run()
    finally:
        GPIO.cleanup()

if __name__ == "__main__":
    main()