import RPi.GPIO as GPIO


class PIR:
    def __int__(self, pin, name, motion_detected):
        self.pin = pin
        self.name = name
        GPIO.setup(self.pin, GPIO.IN)
        GPIO.add_event_detect(self.pin, GPIO.RISING, callback=lambda channel: motion_detected(self.name))

def run_loop(pir, callback, stop_event, publish_event, settings):
    pir.detect_motion()
    while True:
        if stop_event.is_set():
            GPIO.remove_event_detect(pir.pin)
            GPIO.cleanup()
            break