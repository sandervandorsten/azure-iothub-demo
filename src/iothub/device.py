"""Contains interface objects to communicate with Raspberry Pi."""

from abc import abstractmethod
import datetime
import json
import random
import time
import threading
import os
import dotenv

# Using the Python Device SDK for IoT Hub:
#   https://github.com/Azure/azure-iot-sdk-python
from azure.iot.device import IoTHubDeviceClient, Message, MethodResponse


dotenv.load_dotenv(override=True)


class RaspberryPiInterface:
    def __init__(
        self,
        telemetry_interval: int = 3,
        fan_session_duration: int = 10,
        connection_string: str = os.getenv("CONNECTION_STRING_IOT_DEVICE"),
    ):
        """Abstract Raspberry Pi interface definition that is inherited by both simulated and real Raspberry Pi implementations.

        Args:
            telemetry_interval (int, optional): Interval in seconds at which the Raspberry pi should send telemetry to the cloud. Defaults to 3.
            fan_session_duration (int, optional): Time in seconds that the fan should turn on if the temperature is above a certain level. Defaults to 10.
            connection_string (str, optional): Connection string for the device to connect with Azure IoThub. Defaults to os.getenv("CONNECTION_STRING_IOT_DEVICE").
        """

        # Connection string for the device to connect with Azure IoThub.
        self.connection_string = connection_string
        # Interval in seconds at which the Raspberry pi should send telemetry to the cloud.
        self.telemetry_interval = telemetry_interval
        # Time in seconds that the fan should stay on if it is too warm.
        self.fan_session_duration = fan_session_duration
        # Inidicator for if the fan is currently turned on
        self.fan_active = False
        # Time that the fan should turn off again, if on.
        self.fan_stoptime = datetime.datetime(1970, 1, 1)

        # create a IoTHub client for the device to interact with.
        self.client = IoTHubDeviceClient.create_from_connection_string(
            self.connection_string
        )

    @abstractmethod
    def start_fan(self):
        pass

    @abstractmethod
    def stop_fan(self):
        pass

    @abstractmethod
    def get_temperature(self):
        pass

    def send_message(self):
        """Sends a message from the Raspberry Pi to the cloud with the sensor data."""

        # Build the message with telemetry values and local state.
        temperature = self.get_temperature()
        msg_txt_formatted = json.dumps(
            {"temperature": temperature, "fan_active": self.fan_active,}
        )
        message = Message(msg_txt_formatted)

        # You can add a custom application property to the message.
        # An IoT hub can filter on these properties without access to the message body.
        if temperature > 30:
            message.custom_properties["temperatureAlert"] = "true"
        else:
            message.custom_properties["temperatureAlert"] = "false"

        # Send the message.
        print("Sending message: {}".format(message))
        self.client.send_message(message)
        print("Message sent")

    def poll_fan(self):
        """Checks if the fan needs to be turned of."""
        if self.fan_active:
            if datetime.datetime.now() > self.fan_stoptime:
                self.stop_fan()
            else:
                print("The fan is currently active")

    def set_telemetry_interval(self, telemetry_interval: int, *args, **kwargs):
        """Set method for the telemetry interval that can be triggered from the cloud.

        Args:
            telemetry_interval (int): new value for the telemetry interval in seconds.

        Returns:
            tuple(int, dict): input for the methodResponse that will be returned after receiving a cloud-to-device method call.
        """
        try:
            self.telemetry_interval = int(telemetry_interval)
        except ValueError:
            response_payload = {
                "Response": f"Invalid value for telemetry interval. int required, got '{type(telemetry_interval)}': '{telemetry_interval}'"
            }
            response_status = 400
        else:
            response_payload = {
                "Response": f"Executed direct method 'set_telemetry_interval', and set the telemetry interval to {self.telemetry_interval} seconds'"
            }
            response_status = 200
        return response_status, response_payload

    def cloud_to_device_listener(self):
        """Listens in a seperate thread to incoming cloud-to-device requests. 
        
        Can fire methods on the Raspberry Pi locally, e.g. `self.start_fan` or `self.set_telemetry_interval`
        
        """
        while True:

            method_request = self.client.receive_method_request()
            print(
                f"\nMethod callback called with:\nmethodName = {method_request.name}\npayload = {method_request.payload}"
            )

            # Case switch for different methods that can be called from the cloud
            if method_request.name == "start_fan":
                response_status, response_payload = self.start_fan()
            elif method_request.name == "set_telemetry_interval":
                response_status, response_payload = self.set_telemetry_interval(
                    **method_request.payload
                )
            else:
                response_payload = {
                    "Response": "Direct method {} not defined".format(
                        method_request.name
                    )
                }
                response_status = 404
            method_response = MethodResponse(
                method_request.request_id, response_status, payload=response_payload
            )
            self.client.send_method_response(method_response)

    def __call__(self, *args, **kwargs):
        """Periodically send telemetry to the cloud, and start a thread to listen to cloud-to-device messages."""
        try:
            print("IoT Hub device sending periodic messages, press Ctrl-C to exit")

            # Start a thread to listen
            device_method_thread = threading.Thread(
                target=self.cloud_to_device_listener
            )
            device_method_thread.daemon = True
            device_method_thread.start()

            while True:
                self.send_message()
                self.poll_fan()
                time.sleep(self.telemetry_interval)

        except KeyboardInterrupt:
            print("IoTHubClient sample stopped")

    def run(self, *args, **kwargs):
        """Alias for the __call__ method."""
        return self.__call__(*args, **kwargs)


class SimulatedRaspberryPi(RaspberryPiInterface):
    def __init__(self, *args, **kwargs):
        """Instantiation of Simulated RaspberryPi that can run on any computer.

        You can use this class instance if you don't have a Raspberry Pi at hand,
        Or want to experiment with functionality without having to bother with 
        sensors, actuators and GPIO pins on the Raspberry Pi.

        """
        super().__init__(*args, **kwargs)
        self.simulated = True

    def start_fan(self):
        """Starts the fan on the Simulated Raspberry Pi."""

        fan_start_time = datetime.datetime.now()

        self.fan_active = True
        self.fan_stoptime = fan_start_time + datetime.timedelta(
            seconds=self.fan_session_duration
        )

        response_status = 200
        response_payload = {
            "Response": f"The fan has been (re)activated at {fan_start_time}"
        }
        print(response_payload["Response"])
        return response_status, response_payload

    def stop_fan(self):
        """Stop the fan."""
        self.fan_active = False
        print("Fan Stopped")

    def get_temperature(self):
        return 20 + (random.random() * 15)


class RaspberryPi(RaspberryPiInterface):
    def __init__(self, *args, **kwargs):
        """Interface for connecting a RaspberryPi with actual fan and temperature sensor"""
        super().__init__(*args, **kwargs)
        self.simulated = False

    def start_fan(self):
        raise NotImplementedError()

    def stop_fan(self):
        raise NotImplementedError()

    def get_temperature(self):
        raise NotImplementedError()
