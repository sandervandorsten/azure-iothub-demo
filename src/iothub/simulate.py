from device import SimulatedRaspberryPi

if __name__ == "__main__":
    print("IoT Hub Quickstart #2 - Simulated device")
    print("Press Ctrl-C to exit")

    device = SimulatedRaspberryPi()
    device()
