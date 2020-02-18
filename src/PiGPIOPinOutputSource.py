import pigpio

# The GPIO Pins. Use Broadcom numbers.
RED_PIN   = 17
GREEN_PIN = 27
BLUE_PIN  = 4

class PiGPIOPinOutputSource:

    def __init__(self):
        self.pi = pigpio.pi()

    def display(self, red, blue, green):
        self.pi.set_PWM_dutycycle(RED_PIN, int(red))
        self.pi.set_PWM_dutycycle(GREEN_PIN, int(green))
        self.pi.set_PWM_dutycycle(BLUE_PIN, int(blue))

    def shutdown():
        self.pi.set_PWM_dutycycle(RED_PIN, 0)
        self.pi.set_PWM_dutycycle(GREEN_PIN, 0)
        self.pi.set_PWM_dutycycle(BLUE_PIN, 0)