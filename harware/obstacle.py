import RPi.GPIO as gpio
import time

class Ultrasonic:
    def __init__(self):
        gpio.setmode(gpio.BCM)
        gpio.setmode(gpio.BOARD)
        gpio.setwarnings(0)

        self.echo = 18
        self.trigger = 16
        gpio.setup(self.trigger, gpio.OUT)        
        gpio.setup(self.echo, gpio.IN)

    def dist(self):
        gpio.output(self.trigger, True)
        time.sleep(0.001)
        gpio.output(self.trigger, False)

        p_s = 0
        p_e = 0
        while gpio.input(self.echo) == 0:
            p_s = time.time()
        while gpio.input(self.echo) == 1:
            p_e = time.time()

        duration = p_e - p_s
        distance = ((duration * 34300) / 2)
        return round(distance, 2)

    def cleanup(self):
        gpio.cleanup()


if __name__=="__main__":
        sensor = Ultrasonic()
        try:
            while True:
                actual_dist = sensor.dist()
                print("Distance", actual_dist)
                if actual_dist < 30:
                    print("\n Obsstacle detected")
                time.sleep(0.01)
        except KeyboardInterrupt:
            print("Stopped by user")
        finally:
            sensor.cleanup()
