# Azure Functions: Callback to IoT Hub

## Description
This module contains an Azure Functions 'function' called `ServiceBusQueueTriggerTemperature`, which fires when a message arrives on it's input queue `temperature`. It will:

1. Parse this message to extract the original IoTHub-device-name that sent the message. 
2. Connect to IoTHub
3. send a cloud-to-device message via IoTHub to the device mentioned above.

In this demo example it will try to fire the method `start_fan` of the IoT Device. 

# Usage
For usage examples, see the `README.md` document in the root of this project.