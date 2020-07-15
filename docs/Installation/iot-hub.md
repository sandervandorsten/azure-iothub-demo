<h1> <img src="https://raw.githubusercontent.com/sandervandorsten/azure-iothub-demo/master/images/iot-hub-logo.png" alt="IoT Hub Logo" align="left" style="height:40px;padding:5px"> IoT Hub: Registering a Device</h1>

<img src="https://raw.githubusercontent.com/sandervandorsten/azure-iothub-demo/master/images/azure-iothub-demo.png" alt="Infrastructure Overview" border="1">

## What is Azure IoT Hub
The Azure IoT Hub is a managed service, hosted in the cloud, that acts as a central message hub for bi-directional communication between your IoT application and the devices it manages. You can use Azure IoT Hub to build IoT solutions with reliable and secure communications between millions of IoT devices and a cloud-hosted solution backend. You can connect virtually any device to IoT Hub. 

## Installation
Today we're going to connect only one device. To register a device on IoT Hub:

1. Go to your IoT Hub resource and select the menu blade **IoT Devices** (see screenshot below)
2. Register a New device by clicking **+ New**
3. In the "Create a Device" tab, **write down a Device ID**, for example `MyRaspberryPi`. This should be a identifier unique within the IoT Hub.
4. Leave everything else to it's default values and press **Save**. 

<img src="https://raw.githubusercontent.com/sandervandorsten/azure-iothub-demo/master/images/iothub-register01.png" alt="Resources">

## Recap
**You have succesfully registered a device on IoT Hub**! You may come back to this screen later to **copy the (Primary) Connection String to your local configuration file (your `.env` file)** to allow your device to connect to IoT Hub. We will do this later though, once we're doing installing all the different Azure services. 

## Next Steps
Now you've configured everything for IoT Hub, you'll continue by setting up your [Stream Analytics Job](stream-analytics.md)