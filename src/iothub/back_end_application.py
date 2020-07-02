# Copyright (c) Microsoft. All rights reserved.
# Licensed under the MIT license. See LICENSE file in the project root for full license information.

# Using the Python Device SDK for IoT Hub:
#   https://github.com/Azure/azure-iot-sdk-python
# The sample connects to a device-specific HTTP endpoint on your IoT Hub.
import sys
import os
import dotenv
import fire
from typing import Any

# pylint: disable=E0611

from azure.iot.hub import IoTHubRegistryManager
from azure.iot.hub.models import CloudToDeviceMethod, CloudToDeviceMethodResult

from builtins import input

# The service connection string to authenticate with your IoT hub.
# Using the Azure CLI:
# az iot hub show-connection-string --hub-name {your iot hub name} --policy-name service
dotenv.load_dotenv()
CONNECTION_STRING = os.getenv("CONNECTION_STRING_IOT_HUB")
DEVICE_ID = os.getenv("DEVICE_ID")

# Details of the direct method to call.


def iothub_devicemethod_sample_run(
    callback_method: str = "set_telemetry_interval",
    callback_payload: dict = {"telemetry_interval": 10},
):
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

    # except Exception as ex:
    #     print("")
    #     print("Unexpected error {0}".format(ex))
    #     return
    except KeyboardInterrupt:
        print("")
        print("IoTHubDeviceMethod sample stopped")


if __name__ == "__main__":
    print("IoT Hub Python quickstart #2...")
    print("    Connection string = {0}".format(CONNECTION_STRING))
    print("    Device ID         = {0}".format(DEVICE_ID))

    fire.Fire(iothub_devicemethod_sample_run)
