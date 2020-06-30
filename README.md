https://docs.microsoft.com/en-us/azure/iot-hub/quickstart-send-telemetry-python?source=docs

```bash
export IoTHubName="svd-iot-01"
export deviceName="HpLaptopLinux"
```

1. Download the az iot hub extension
```bash
az extension add --name azure-iot
```


2. Create a IoT Device Identity within an IoT hub
```bash
az iot hub device-identity create --hub-name $IoTHubName --device-id $deviceName
```

3. Run the following command in Azure Cloud Shell to get the device connection string for the device you registered:
```bash
az iot hub device-identity show-connection-string --hub-name $IoTHubName --device-id $deviceName --output table
```

4. You also need the Event Hubs-compatible endpoint, Event Hubs-compatible path, and service primary key from your IoT hub to enable the back-end application to connect to your IoT hub and retrieve the messages. The following commands retrieve these values for your IoT hub:
```bash
az iot hub show \
    --query properties.eventHubEndpoints.events.endpoint \
    --name $IoTHubName
az iot hub show \
    --query properties.eventHubEndpoints.events.path \
    --name $IoTHubName
az iot hub policy show \
    --name service \
    --query primaryKey \
    --hub-name $IoTHubName

