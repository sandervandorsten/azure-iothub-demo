import json
import logging
import os

import azure.functions as func
from azure.iot.hub import IoTHubRegistryManager
from azure.iot.hub.models import CloudToDeviceMethod, CloudToDeviceMethodResult


def main(msg: func.ServiceBusMessage):

    msg_json = json.loads(msg.get_body().decode("utf-8"))

    logging.info(f"Python ServiceBus queue trigger processed message: {msg_json}")
    device_id = msg_json["IoTHub"]["ConnectionDeviceId"]

    connectino_string_iothub = os.getenv("connectionStringIotHub")
    registry_manager = IoTHubRegistryManager(connectino_string_iothub)

    callback_method = "start_fan"
    callback_payload = {}
    # Call the direct method.
    device_method = CloudToDeviceMethod(
        method_name=callback_method, payload=callback_payload
    )
    response = registry_manager.invoke_device_method(device_id, device_method)

    print("")
    print("Device Method called")
    print("Device Method name       : {0}".format(callback_method))
    print("Device Method payload    : {0}".format(callback_payload))
    print("")
    print("Response status          : {0}".format(response.status))
    print("Response payload         : {0}".format(response.payload))

