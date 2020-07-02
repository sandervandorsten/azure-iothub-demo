# Copyright (c) Microsoft. All rights reserved.
# Licensed under the MIT license. See LICENSE file in the project root for full license information.

import datetime
import random
import time
import threading
import os
import dotenv

# Using the Python Device SDK for IoT Hub:
#   https://github.com/Azure/azure-iot-sdk-python
# The sample connects to a device-specific MQTT endpoint on your IoT Hub.
from azure.iot.device import IoTHubDeviceClient, Message, MethodResponse

# The device connection string to authenticate the device with your IoT hub.
# Using the Azure CLI:
# az iot hub device-identity show-connection-string --hub-name {YourIoTHubName} --device-id MyNodeDevice --output table
dotenv.load_dotenv(override=True)
CONNECTION_STRING = os.getenv("CONNECTION_STRING_SIMULATED_DEVICE")
TELEMETRY_INTERVAL = 3

# Define the JSON message to send to IoT Hub.
TEMPERATURE = 20.0
HUMIDITY = 60
MSG_TXT = '{{"temperature": {temperature},"humidity": {humidity}}}'

# time in seconds that the fan should stay on if it is too warm.
FAN_SESSION_DURATION = 10
FAN_ACTIVE = False
FAN_STOPTIME = datetime.datetime(1970, 1, 1)


def iothub_client_init():
    # Create an IoT Hub client
    client = IoTHubDeviceClient.create_from_connection_string(CONNECTION_STRING)
    return client


def device_method_listener(device_client):
    global TELEMETRY_INTERVAL
    while True:

        poll_fan()  # checks status of the fan

        try:
            method_request = device_client.receive_method_request()
            print(
                f"\nMethod callback called with:\nmethodName = {method_request.name}\npayload = {method_request.payload}"
            )
            if method_request.name == "start_fan":
                response_status, response_payload = start_fan()
            elif method_request.name == "set_telemetry_interval":
                response_status, response_payload = set_telemetry_interval(
                    **method_request.payload
                )
            else:
                response_payload = {
                    "Response": "Direct method {} not defined".format(
                        method_request.name
                    )
                }
                response_status = 404
        # except Exception as e:
        #     response_status = 400
        #     response_payload = {
        #         "Response": f"An unexpected error has occured:\n {type(e)}: {e}"
        #     }

        finally:
            method_response = MethodResponse(
                method_request.request_id, response_status, payload=response_payload
            )
            device_client.send_method_response(method_response)


def start_fan():
    """Starts the fan on the Raspberry Pi."""
    global FAN_ACTIVE
    global FAN_STOPTIME
    global FAN_SESSION_DURATION

    fan_start_time = datetime.datetime.now()

    FAN_ACTIVE = True
    FAN_STOPTIME = fan_start_time + datetime.timedelta(seconds=FAN_SESSION_DURATION)

    response_status = 400
    response_payload = {
        "Response": f"The fan has been (re)activated at {fan_start_time}"
    }
    print(response_payload["Response"])
    return response_status, response_payload


def poll_fan():
    """Checks if the fan needs to be turned of."""
    global FAN_ACTIVE
    global FAN_STOPTIME
    if FAN_ACTIVE:
        if datetime.datetime.now() > FAN_STOPTIME:
            FAN_ACTIVE = False
            print("Fan Stopped")
        else:
            print("The fan is currently active")


def set_telemetry_interval(telemetry_interval: int):
    global TELEMETRY_INTERVAL

    print(telemetry_interval)
    try:
        TELEMETRY_INTERVAL = int(telemetry_interval)
    except ValueError:
        response_payload = {
            "Response": f"Invalid value for telemetry interval. int required, got '{type(telemetry_interval)}'"
        }
        response_status = 400
    else:
        response_payload = {
            "Response": f"Executed direct method 'set_telemetry_interval', and set the telemetry interval to {TELEMETRY_INTERVAL} seconds'"
        }
        response_status = 200
    return response_status, response_payload


def iothub_client_telemetry_sample_run():
    global TELEMETRY_INTERVAL
    try:
        client = iothub_client_init()
        print("IoT Hub device sending periodic messages, press Ctrl-C to exit")

        # Start a thread to listen
        device_method_thread = threading.Thread(
            target=device_method_listener, args=(client,)
        )
        device_method_thread.daemon = True
        device_method_thread.start()

        while True:
            send_message(client)
            poll_fan()
            time.sleep(TELEMETRY_INTERVAL)

    except KeyboardInterrupt:
        print("IoTHubClient sample stopped")


def send_message(client: IoTHubDeviceClient):
    # Build the message with simulated telemetry values.
    temperature = TEMPERATURE + (random.random() * 15)
    humidity = HUMIDITY + (random.random() * 20)
    msg_txt_formatted = MSG_TXT.format(temperature=temperature, humidity=humidity)
    message = Message(msg_txt_formatted)
    # Add a custom application property to the message.
    # An IoT hub can filter on these properties without access to the message body.
    if temperature > 30:
        message.custom_properties["temperatureAlert"] = "true"
    else:
        message.custom_properties["temperatureAlert"] = "false"

    # Send the message.
    print("Sending message: {}".format(message))
    client.send_message(message)
    print("Message sent")


if __name__ == "__main__":
    print("IoT Hub Quickstart #2 - Simulated device")
    print("Press Ctrl-C to exit")
    iothub_client_telemetry_sample_run()
