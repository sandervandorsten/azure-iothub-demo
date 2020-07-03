"""Simulate a cloud-to-device message to an Azure Iothub device."""

# Using the Python Device SDK for IoT Hub:
#   https://github.com/Azure/azure-iot-sdk-python
import sys
import os
import dotenv
import fire

from azure.iot.hub import IoTHubRegistryManager
from azure.iot.hub.models import CloudToDeviceMethod, CloudToDeviceMethodResult

# The service connection string to authenticate with your IoT hub.
# You can specify them in an .env file, and obtain them using the Azure CLI:
# az iot hub show-connection-string --hub-name {your iot hub name} --policy-name service
dotenv.load_dotenv(override=True)
CONNECTION_STRING = os.getenv("CONNECTION_STRING_IOT_HUB")
DEVICE_ID = os.getenv("DEVICE_ID")


def iothub_devicemethod_sample_run(
    callback_method: str = "start_fan", callback_payload: dict = {},
):
    """Simulate a cloud-to-device message to an IoT device to run a method.

    Args:
        callback_method (str, optional): Function that will be called on the IoT Device. Defaults to `start_fan`.
        callback_payload (dict, optional): additional data that can be processed by the IoT Device. Defaults to `{}`.
    """
    try:
        # Create IoTHubRegistryManager
        registry_manager = IoTHubRegistryManager(CONNECTION_STRING)

        # Call the direct method.
        deviceMethod = CloudToDeviceMethod(
            method_name=callback_method, payload=callback_payload
        )
        response = registry_manager.invoke_device_method(DEVICE_ID, deviceMethod)

        print("")
        print("Device Method called")
        print("Device Method name       : {0}".format(callback_method))
        print("Device Method payload    : {0}".format(callback_payload))
        print("")
        print("Response status          : {0}".format(response.status))
        print("Response payload         : {0}".format(response.payload))

        input("Press Enter to continue...\n")

    except KeyboardInterrupt:
        print("")
        print("IoTHubDeviceMethod sample stopped")


if __name__ == "__main__":
    print("Demoing cloud-to-device messaging through IoT Hub...")
    print("    Connection string = {0}".format(CONNECTION_STRING))
    print("    Device ID         = {0}".format(DEVICE_ID))

    fire.Fire(iothub_devicemethod_sample_run)
