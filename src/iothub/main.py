"""CLI utility to start a (simulated) Raspberry Pi."""

from device import SimulatedRaspberryPi, RaspberryPi, RaspberryPiInterface

from fire import Fire


def main(RPi: RaspberryPiInterface = "SimulatedRaspberryPi", *args, **kwargs):
    Device = eval(RPi)
    print(f"Starting IoT device: '{Device.__name__}' and connecting it to IoT Hub.")

    device = Device(*args, **kwargs)
    device.run()


if __name__ == "__main__":
    Fire(main)
