"""Azure function that will send a cloud-to-device message via IoTHub to a device"""

import json
import logging
import os

import azure.functions as func
from azure.iot.hub import IoTHubRegistryManager
from azure.iot.hub.models import CloudToDeviceMethod, CloudToDeviceMethodResult


def main(msg: func.ServiceBusMessage):
    """When a message arrives on the servicebus, send a trigger to IoT Hub to start the fan for that device.

    Args:
        msg (func.ServiceBusMessage): Message from the connected Queue in a Azure ServiceBus
    """

    # Extract the method into a dictionary
    msg_dict = json.loads(msg.get_body().decode("utf-8"))

    logging.info(f"Python ServiceBus queue trigger processed message: {msg_dict}")

    # Enable a connectino with the IoT Hub. The connectionstring for the IoT Hub
    # is preloaded in the Azure Functions configurations.
    connectino_string_iothub = os.getenv("connectionStringIotHub")
    registry_manager = IoTHubRegistryManager(connectino_string_iothub)

    # Settings for the method that the IoT Device should run upon receiving the message.
    callback_method = "start_fan"
    callback_payload = {}
    device_method = CloudToDeviceMethod(
        method_name=callback_method, payload=callback_payload
    )

    # Sending the actual cloud-to-device message and invoke a function on the IoT device.
    device_id = msg_dict["IoTHub"]["ConnectionDeviceId"]
    response = registry_manager.invoke_device_method(device_id, device_method)

    print("")
    print("Device Method called")
    print("Device Method name       : {0}".format(callback_method))
    print("Device Method payload    : {0}".format(callback_payload))
    print("")
    print("Response status          : {0}".format(response.status))
    print("Response payload         : {0}".format(response.payload))

