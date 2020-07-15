<h1> <img src="https://raw.githubusercontent.com/sandervandorsten/azure-iothub-demo/master/images/rpi.svg" alt="Raspberry Pi Logo" align="left" style="height:40px;padding:5px"> Using A Simulated Raspberry Pi</h1>

<img src="https://raw.githubusercontent.com/sandervandorsten/azure-iothub-demo/master/images/azure-iothub-demo.png" alt="Infrastructure Overview" border="1">


## Starting the simulated Raspberry Pi
Now the configuration is finished, **you can start the RaspberryPi simulation**. The simulated Raspberry Pi will:

  - send a random temperature value every 3 seconds to the IoT Hub.
  - listen to its IoT Hub for messages. Our function app will send messages to the device through the IoT Hub to start the fan if `temperature > 29` (as configured in our Stream Analytics Job). The fan will then be turned on for 10 seconds, and deactivated afterwards. Hence, if the temperature will stay above 29 degrees, the fan will stay on because the RaspberryPi will keep receiving messages to turn on the fan.

open a terminal in the `azure-iothub-demo` folder and activate your virtual environment
```bash
source venv/bin/activate
```

Navigate to the `src/iothub` folder and run the Raspberry Pi simulation
```bash
cd src/iothub
python main.py --RPi SimulatedRaspberryPi
# IoT Hub device sending periodic messages, press Ctrl-C to exit
# Sending message: {"temperature": 33.794175910136936, "fan_active": false}
# Message sent
# Sending message: {"temperature": 22.667180109040924, "fan_active": false}
# Message sent
# ...
```

Once the Raspberry Pi sends a message with a `temperature > 29`, this message will be forwarded by the Stream Analytics Job to the Service Bus Queue. Once this message arrives on the Service Bus Queue, it will trigger the Function app (that is running in the cloud), which sends a message through the IoTHub to the device that the fan should be activated.

You can monitor the activity of the individual services in the Azure Portal.
