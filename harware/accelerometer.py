import smbus
import time
import math

class FallDetector:
    def __init__(self, bus_number=1, device_address=0x68):
        self.bus = smbus.SMBus(bus_number)
        self.device_address = device_address
        self.setup_sensor()

    def setup_sensor(self):
        self.bus.write_byte_data(self.device_address, 0x6B, 0)
        print("Accelerometer Initialized.")

    def read_raw_data(self, addr):
        high = self.bus.read_byte_data(self.device_address, addr)
        low = self.bus.read_byte_data(self.device_address, addr + 1)
        value = ((high << 8) | low)
        if value > 32768:
            value -= 65536
        return value

    def get_acceleration(self):
        acc_x = self.read_raw_data(0x3B) / 16384.0
        acc_y = self.read_raw_data(0x3D) / 16384.0
        acc_z = self.read_raw_data(0x3F) / 16384.0
        return acc_x, acc_y, acc_z

    def detect_fall(self, threshold=2.5):
        acc_x, acc_y, acc_z = self.get_acceleration()
        magnitude = math.sqrt(acc_x**2 + acc_y**2 + acc_z**2)
        print(f"Acceleration Magnitude: {magnitude:.2f}g")
        if magnitude > threshold:
            return True
        return False

# Example usage
if __name__ == "__main__":
    detector = FallDetector()
    while True:
        if detector.detect_fall():
            print("Fall Detected!")
        time.sleep(0.5)