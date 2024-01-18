import RPi.GPIO as GPIO


class RPIR2:
    def __int__(self, pin, name, motion_detected):
        self.pin = pin
        self.name = name
        GPIO.setup(self.pin, GPIO.IN)
        GPIO.add_event_detect(self.pin, GPIO.RISING, callback=lambda channel: motion_detected(self.name))

def run_loop(rpir2, callback, stop_event, publish_event, settings):
    rpir2.detect_motion()
    while True:
        if stop_event.is_set():
            GPIO.remove_event_detect(rpir2.pin)
            GPIO.cleanup()
            break