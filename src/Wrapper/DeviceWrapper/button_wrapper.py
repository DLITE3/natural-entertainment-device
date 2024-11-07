import RPi.GPIO as GPIO

class ButtonWrapper:
    def __init__(self, pins):
        self.pins = pins
        GPIO.setmode(GPIO.BCM)
        # Set up each pin
        for pin in self.pins:
            GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    def read_button_state(self, pin) -> int:
        return GPIO.input(pin)

    def read_multiple_buttons(self) -> dict:
        states = {}
        for pin in self.pins:
            states[pin] = self.read_button_state(pin)
        return states

    def stop(self) -> None:
         GPIO.cleanup()

