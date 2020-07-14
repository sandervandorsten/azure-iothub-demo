<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->

<!-- [![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url] -->
[![Issues][issues-shield]][issues-url]
[![Updates][pyup-shield]][pyup-url]
[![MIT License][license-shield]][license-url]
[![Code Style][code-style-shield]][code-style-url]
[![LinkedIn][linkedin-shield]][linkedin-url]



<!-- PROJECT LOGO -->
<br />
<p align="center">
  <a href="https://github.com/sandervandorsten/azure-iothub-demo">
    <img src="images/rpi.svg" alt="Logo" width="120">
  </a>

  <h3 align="center">Azure IoT Hub Demo</h3>

  <p align="center">
    IoT application on Azure to connect a <b>RaspberryPi</b> to <b>IoT Hub</b>. <br>Sends device-to-cloud telemetry and allows cloud-to-device callbacks to be sent to the Raspberry Pi.
    <br />
    <br>
    <a href="https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fsandervandorsten%2Fazure-iothub-demo%2Fmaster%2Finfra%2Fdeployment.json" target="_blank">
        <img src="https://aka.ms/deploytoazurebutton"/>
    </a>
    <br>
    <br />
    <a href="https://github.com/sandervandorsten/azure-iothub-demo/issues">Report Bug</a>
    ·
    <a href="https://github.com/sandervandorsten/azure-iothub-demo/issues">Request Feature</a>
  </p>
</p>

Do you want to have a fresh breeze in you home office, but are you to lazy to turn on the fan yourself? With this project you'll have your office cooled down in notime!

<img src="images/azure-iothub-demo.png" alt="Infrastructure Overview" border="1">

<!-- TABLE OF CONTENTS -->
## Table of Contents

* [About the Project](#about-the-project)
  * [Background](#background)
  * [Infrastructure](#infrastructure)
  * [Control Flow](#control-flow)
* [Getting Started](#getting-started)
  * [Prerequisites](#prerequisites)
  * [Deploying Infrastructure](#deploying-infrastructure)
  * [Starting Services](#starting-services)
    * [Registering a device on IoT Hub](#registering-a-device-on-iot-hub)
    * [Starting the analysis job on Stream Analytics](starting-the-analysis-job-on-stream-analytics)
    * [Deploying a function to Azure Functions](#deploying-a-function-to-azure-functions)
* [Usage](#usage)
* [License](#license)
* [Contact](#contact)
* [Resources used for project development](#Resources-used-for-project-development)


<!-- ABOUT THE PROJECT -->
## About The Project
This project helps you setup a relatively simple Azure Infrastructure for connecting your own Raspberry Pi to the cloud. You can use this as a starting point to develop small IoT applications. It contains:
- The possibility to simulate a Raspberry Pi from your computer to speed up development
- Simple data storage in a container for 'cold' analysis
- data flowing through Stream Analytics to perform live analysis and send this along to other Azure Services
- Infrastructure as code using ARM templates so you can deploy your own easily
  - Estimated costs: **< 10EUR / Month** (if you set IoT Hub to use a free account, limited to 1 per subscription)
- An easily extendable infrastructure, for example if:
  - You want to create a dashboard with PowerBI, you can [add PowerBI as an output to Stream Analytics](https://docs.microsoft.com/en-us/azure/stream-analytics/stream-analytics-power-bi-dashboard). 
  - You want to [register more IoT devices to IoT Hub](https://docs.microsoft.com/en-us/azure/iot-hub/iot-hub-get-started-physical) 

### Background
<img src="images/thermometer.svg" alt="Getting Hot it Here" width="100" height="100" align="right">I started this project whilst working from home on different coding projects on Azure in the summer during the COVID-19 outbreak. Whilst working from home certainly has it's advantages, I did miss the AC that we have at the office at times. 

<br>

<img src="images/fan.svg" alt="Attaching a fan" width="100" height="100" align="left">
Whilst the temperature in my home-office sky-rocketed in June, I bought a ventilator to keep me cool. This was great, however having it turned on at all times is a bit of an overkill as it is certainly not hot all day-everyday here in the Netherlands. My ventilator however did not support temperature-based-control, hence I wanted to build this myself.

<br>

<img src="images/rpi.svg" alt="Raspberry Pi" width="100" height="100" align="right">
I had a Raspberry Pi lying around so wanted to use this as an interface for measuring temperature and controlling the ventilator. As I was working on a number of projects in Azure, I wondered if I could use their cloud services to connect this raspberry Pi to the cloud. Hence I asked myself:

<br>
<br>

<p align="center" style="font-size: 30px ; padding 0px 50px">
    <b>Can I connect a Raspberry Pi to IoT Hub to  <br> 1) send device-to-cloud telemetry data and <br> 2) trigger the ventilator on my desk with a cloud-to-device message?</b>
<p>

In my mind, the application should contain a few components:
- Raspberry Pi: 
    - stream temperature data from device to the cloud. 
    - listen to signal that triggers fan activation from the cloud. 
- 'arbitrary-cloud-services':
    - data should be stored somewhere
    - Once a certain temperature threshold has been exceded, a message should be returned to the Raspberry Pi to trigger the fan.


### Infrastructure
I ended up using the following Infrastructure:
- **Raspberry Pi** to connect sensor and fan to. This project also includes a simulated Raspberry Pi device that you can run on your computer to speed up development. 
- **Azure IoT Hub**. Allows you to securely connect IoT devices to Azure cloud, from which you can further route messages to different services.
- **Stream Analytics**. Performs streaming data analysis on your IoT input data and forwards the data to specified services. 
- **Blob Storage**. Cold storage for the data.
- **Service Bus Queue**. Queue used as input/trigger for Azure Functions. 
- **Functions**. Serverless function that is triggered by the aforementioned Service Bus Queue, and sends a message via IoT Hub to the Connected Raspberry Pi device. 

<img src="images/azure-iothub-demo.png" alt="Infrastructure Overview" border="1">

### Control Flow

1. A Raspberry Pi collects data from a connected temperature sensor. It sends this so-called telemetry data to it's designated IoT Hub. 
2. The IoT Hub processess incoming and outgoing requests from/to connected IoT devices. It has a `Messaging` Endpoint, from which Stream Analytics ingests the Raspberry Pi temperature telemetry for further processing.
3. Stream Analytics writes all telemetry temperature data to a blob storage, and writes a subset of the temperatures to a Queue on the Service Bus. In this example, we send only the telemetry data `temperature > 29` to the Queue. 
4. When a new message is stored on the Queue, a Azure Function is triggered. 
5. The function app sends a message to the IoT hub that the fan of the connected Raspberry Pi should turn on. Effectively in our example this means that the fan will turn on for a while if, and only if `temperature > 29`. 
6. The IoT Hub securely forwards the message to the Raspberry Pi to start the connected ventilator.


<!-- GETTING STARTED -->
## Getting Started

In this step-by-step guide we'll help you set up everything to get your own application up and running. The setup is going to cover the following parts: 
 1. [Deploying your own copy infrastructure to Azure using ARM templates](#deploying-infrastructure)
 2. [Starting and configuring the individual services](#starting-services), specifically:
    1. [Registering a (simulated) Raspberry Pi device on IoT Hub](#registering-a-device-on-iot-hub)
    2. [Starting our analysis job on Stream Analytics](#starting-the-analysis-job-on-stream-analytics)
    3. [Deploying a function to Azure Functions](#deploying-a-function-to-azure-functions)
 3. TBA

### Prerequisites

- Azure account with a subscription you are allowed to create resources in (Free Trial Subscription should do)
- Make sure you have [installed the Azure CLI](https://docs.microsoft.com/en-us/cli/azure/install-azure-cli?view=azure-cli-latest) on your computer
- basic knowledge of git + python virtual environments
- access to a bash-like terminal

### Deploying Infrastructure
I've [defined the infrastructure in an ARM template](https://azure.microsoft.com/en-us/resources/templates/). This allows you to press the button below and deploy the infrastructure to your own Azure account with the click of a button. 

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fsandervandorsten%2Fazure-iothub-demo%2Fmaster%2Finfra%2Fdeployment.json)

1. Press the 'Deploy to Azure' button above to create a custom deployment in Azure
2. Login to your Azure Account where you want to create the application (if not logged in yet)
3. You should then see the Custom Deployment screen as in the screenshot below. Here you can specify some settings for the Deployment.
    1. Select a subscription in which you want to create the resources in
    2. Create a new resourcegroup in which you want to deploy these resources
    3. Keep all the other settings as default, unless you know what you're doing and want to change something
    4. Scroll down, accept the terms and conditions and click Purchase.
    5. **IMPORTANT** Remember that this deployment and the running of it will cost you money. For me, I didn't pay more that a few euros and I let it run for a month or so. Please remember to remove your resources if you're not using them anymore! 
4. After a couple of minutes (+- 5 minutes I guess) your infrastructure deployment should be completed. Navigate to the resource group you've created to see the different services you've deployed. 

<img src="images/deploy-infra01.png" alt="Infrastructure Deployment" border="1">

### Starting Services
You should now have the individual components deployed within your Resource Group. Navigate to your resource group overview, and you'll see something like this.

<img src="images/resourcegroup-overview.png" alt="Resources" border="1">

To use our end-to-end application, we must activate and configure some of our individual services. We're going to do that now.  

#### Registering a device on IoT Hub
<img src="images/iot-hub-logo.png" alt="IoT Hub Logo" height="100px" align="right">
The Azure IoT Hub is a managed service, hosted in the cloud, that acts as a central message hub for bi-directional communication between your IoT application and the devices it manages. You can use Azure IoT Hub to build IoT solutions with reliable and secure communications between millions of IoT devices and a cloud-hosted solution backend. You can connect virtually any device to IoT Hub. 

<br><br>

Today we're going to connect only one device. To register a device on IoT Hub:
1. Go to your IoT Hub resource and select the menu blade **IoT Devices** (see screenshot below)
2. Register a New device by clicking **+ New**
3. In the "Create a Device" tab, **write down a Device ID**, for example `MyRaspberryPi`. This should be a identifier unique within the IoT Hub.
4. Leave everything else to it's default values and press **Save**. 
5. **You have succesfully registered a device on IoT Hub**! You will come back to this screen later to **copy the (Primary) Connection String to your local configuration file (your `.env` file)** to allow your device to connect to IoT Hub. We will do this later though, once we're doing configuring the infrastructure.

<img src="images/iothub-register01.png" alt="Resources" border="1">

#### Starting the analysis job on Stream Analytics
<img src="images/stream-analytics-logo.png" alt="Stream Analytics Logo" height="100px" align="right">
Azure Stream Analytics is a real-time analytics and complex event-processing engine that is designed to analyze and process high volumes of fast streaming data from multiple sources simultaneously. Patterns can be identified from a number of input sources including devices, sensors and applications. These patterns can be used to trigger actions and initiate workflows such as creating alerts, feeding information to a reporting tool, or storing transformed data for later use. 

<br><br>

We will use Stream Analytics to ingest data from IoT Hub and move it to both Blob Storage and a Service Bus Queue for more complex actions. This is already configured for you when the infrastructure was deployed, the only thing we need to do is **Start the Streaming Job**.

1. **Navigate to your Stream Analytics resource** and you will see the the **Overview page**. 
2. On the bottom right you will see the **Query** that is already pre-defined. This query does 2 things. (it shown below as well for convenience)
    1. it moves all data from the **input called** `iothub` **to the output called `blobstorage`**
    2. it moves all data where `temperature > 29` from the **input called** `iothub` **to the output called** `servicebus`
    ```SQL 
    SELECT
        *
    INTO
        blobstorage
    FROM
        iothub

    SELECT
        *
    INTO
        servicebus
    FROM
        iothub
    WHERE
        temperature > 29
    ```
3. If you want to learn how this input and outputs are actually coupled to the IoT Hub and Service Bus in our infrastructure, you can navigate to the menu blades on the left of your screen called **inputs** and **outputs** (under **Job Topology**). At deployment time, the bindings to these services were already done for you so you don't have to worry about them. If you want to learn how to create these yourself, **I recommend [This video](https://www.youtube.com/watch?v=NbGmyjgY0pU) by Adam Marczak** on Azure Stream Analytics. I fact, I recommend all his Azure tutorials, which helped me a great deal in developing this project.
4. Now you know roughly what happens in Stream Analytics, we can **start this Stream Analytics Job** to start processing incoming requests. Remember that we're not sending any data from a device yet to our application, but we're just preconfiguring the infrastrature. Press the **> Start** button **at the top of the Overview** menu to start the job. It takes about a minute or two to activate, you can see the status straight below it. (see screenshot below)
5. You have sucessfully started your Steam Analytics job! In a bit, our Raspberry Pi Data will flow through this job to the connected services. Now it's not doing anything yet though, So lets quickly finish up our infrastructure setup to start sending data. 
6. **Cost saving Tip:** Pause your stream Analytics job once your done developing. You don't pay per request, but per hour. 


<p align="center">
  <img src="images/streaming.png" alt="Stream Analytics" border="2" height="100%">
</p>

#### Deploying a function to Azure Functions
<img src="images/azure-functions-logo.png" alt="Azure Functions Logo" height="100px" align="right">
Azure Functions is a serverless compute service that lets you run event-triggered code without having to explicitly provision or manage infrastructure. A function is "triggered" by a specific type of event. Supported triggers include responding to changes in data, responding to messages, running on a schedule, or as the result of an HTTP request.

<br><br>

In our application, we're going to start a function when we receive a message on our Service Bus Queue. A function can be deployed within Azure Functions, and can be developed locally on your computer. We're going to deploy a function that I already prepared for this demo.

Make sure you have [installed the Azure CLI](https://docs.microsoft.com/en-us/cli/azure/install-azure-cli?view=azure-cli-latest) on your computer. you can test this by running `az --version` in your terminal. 

##### 1/4: Downloading the repository

```bash
# 1. Clone this repository to your computer.
git clone https://github.com/sandervandorsten/azure-iothub-demo.git
# Cloning into 'azure-iothub-demo'...
# ...
# Resolving deltas: 100% ..., done.

# 2. navigate into the git repository
cd azure-iothub-demo

# 3. Create a virtual environment with python 3.7 and install the requirements
virtualenv -p $(which python3.7) venv
source venv/bin/activate
pip install -r requirements.txt
```


##### 2/4: Running our functions application locally
Now we have our code and python environment locally, we can test our function app locally before we deploy it to our cloud project. 

The code that will be run in the function can be found in `src/azure_functions/ServiceBusQueueTriggerTemperature/__init__.py` in this repository, you can check it out if you like. 

To start our function app locally:
```bash
# 1. Navigate to the folder containing the source code for Azure Functions
cd src/azure_functions

# 2. Download the application settings from the cloud. 
# These are the environment variables that will be used to connect Azure Functions 
# to different services, such as storage and the IoT Hub.
# it will store the configuration files automatically in `src/azure_functions/local.settings.json`.
# Note that you should replace the functionapp name with your own!!
func azure functionapp fetch-app-settings functionapp-pndvv72m6ihab
# App Settings:
# Loading FUNCTIONS_WORKER_RUNTIME = *****
# Loading FUNCTIONS_EXTENSION_VERSION = *****
# Loading AzureWebJobsStorage = *****
# Loading connectionStringListenServiceBus = *****
# Loading connectionStringIotHub = *****

# 3. Start the function app locally. This will start a local webserver on port 7071. 
# Our function should then run locally on your computer, 
# but listens to the Service Bus Queue in the cloud. 
func start
# Found Python version 3.7.5 (python3).

#                   %%%%%%
#                  %%%%%%
#             @   %%%%%%    @
#           @@   %%%%%%      @@
#        @@@    %%%%%%%%%%%    @@@
#      @@      %%%%%%%%%%        @@
#        @@         %%%%       @@
#          @@      %%%       @@
#            @@    %%      @@
#                 %%
#                 %
# ...
# Content root path: /.../azure-iothub-demo/src/azure_functions
# Now listening on: http://0.0.0.0:7071
# Application started. Press Ctrl+C to shut down.
```

##### 3/4: Simulating a RaspberryPi Locally
Running our function app was the last step of infrastructure that we should enable before we can start testing our whole setup. Now, we need to connect a IoT Device to the IoT Hub s.t. we can send device-to-cloud telemetry towards our cloud application, and receive cloud-to-device messages from our function app. I've created a Raspberry Pi Interface in `azure-iothub-demo/src/iothub/device.py` that we're going to use to **simulate a Raspberry Pi**. You can connect your own raspberry Pi to do the actual work, but this is (currently) beyond the scope of this tutorial. 

To start a Raspberry Pi simulation, open an extra terminal window (leaving the one running the function app open!) and running the following snippets:

```bash
# 0. Navigate to the azure-iothub-demo folder and activate the virtual environment in this terminal as well
source venv/bin/activate

# 1. Copy the sanmple.env file to .env file s.t. we can store essential credentials here later
cp sample.env .env

# 2. Download the azure IoT Hub Extension to interact with our cloud application
az extension add --name azure-iot

# 3. Save your unique IoT Hub name (see your own Azure Portal with the name of your Iot Hub resource Name) and DeviceId s.t. we can use them below
export IoTHubName="rpi-iothub-........."
export deviceId="MyRaspberryPi"

# 4. Access the connection string for the IoT Hub in your terminal
az iot hub show-connection-string \
  --name $IoTHubName \
  --output table
#HostName=rpi-iothub-pndvv72m6ihab.azure-devices.net;SharedAccessKeyName=iothubowner;SharedAccessKey=BhkccChKy2ii4SdlXw00/1NtD0p6nssS0MIHoWqZODI=

# 5. Access the Connection String for the DeviceId you've created in IoT Hub. 
az iot hub device-identity show-connection-string \
  --hub-name $IoTHubName \
  --device-id $deviceId \
  --output table
#HostName=rpi-iothub-pndvv72m6ihab.azure-devices.net;DeviceId=MyRaspberryPi;SharedAccessKey=bHnH82Pn21X0QPVkrFCban/XTEml5zAVR8YkiccgZPQ=
```

- Now, open the `.env` file with a text editor and replace the string values s.t. it looks like this
  ```bash
  DEVICE_ID="MyRaspberryPi"
  CONNECTION_STRING_IOT_DEVICE="HostName=rpi-iothub-pndvv72m6ihab.azure-devices.net;DeviceId=MyRaspberryPi;SharedAccessKey=bHnH82Pn21X0QPVkrFCban/XTEml5zAVR8YkiccgZPQ="
  CONNECTION_STRING_IOT_HUB="HostName=rpi-iothub-pndvv72m6ihab.azure-devices.net;SharedAccessKeyName=iothubowner;SharedAccessKey=BhkccChKy2ii4SdlXw00/1NtD0p6nssS0MIHoWqZODI="
  ```
- Save the .env file and close it. . **This file contains credentials and should not be shared, or stored publicly!** 
- Now the configuration is finished, you can start the RaspberryPi simulation. the Simulated Raspberry Pi will:
  - send a random temperature value every 3 seconds to the IoT Hub.
  - listen to it's IoT Hub for messages. Our function app will send messages to the device through the IoT Hub to start the fan if `temperature > 29` (as configured in our Stream Analytics Job). The fan will then be turned on for 10 seconds, and deactivated afterwards. Hence, if the temperature will stay above 29 degrees, the fan will stay on because the RaspberryPi will keep receiving messages to turn on the fan.
- To start the Raspberry Pi simulation, re-use the second terminal window and execute the following commands: 
  ```bash
  # 6. navigate to the iothub folder and run the Raspberry Pi simulation
  cd src/iothub
  python main.py --RPi SimulatedRaspberryPi
  # IoT Hub device sending periodic messages, press Ctrl-C to exit
  # Sending message: {"temperature": 33.794175910136936, "fan_active": false}
  # Message sent
  # Sending message: {"temperature": 22.667180109040924, "fan_active": false}
  # Message sent
  # ...
  ```
- Once the Raspberry Pi sends a message with a `temperature > 29`, this message will be forwarded by the Stream Analytics Job to the Service Bus Queue. Once this message arrives on the Service Bus Queue, it will trigger the Function app (that is running locally on your computer), which sends a message through the IoTHub to the device that the fan should be activated. The logs in your terminal of your function app should look something like this:
  ```log
  [7/14/2020 9:53:43 AM] Executing 'Functions.ServiceBusQueueTriggerTemperature' (Reason='New ServiceBus message detected on 'temperature'.', Id=161614bf-3d3a-40f7-8608-7e2c88d08ba0)
  [7/14/2020 9:53:43 AM] Trigger Details: MessageId: a5f9ddcd698142e495a1cec97f954071, DeliveryCount: 10, EnqueuedTime: 7/14/2020 9:53:42 AM, LockedUntil: 7/14/2020 9:58:43 AM, SessionId: 18725
  [7/14/2020 9:53:43 AM]  INFO: Received FunctionInvocationRequest, request ID: 2f46689a-8f66-4dab-88da-6381e553e3f2, function ID: 4065367e-45d4-45f3-bb6e-416b2fdeed51, invocation ID: 161614bf-3d3a-40f7-8608-7e2c88d08ba0
  [7/14/2020 9:53:43 AM] Python ServiceBus queue trigger processed message: {'temperature': 30.463195551136046, 'fan_active': 1, 'EventProcessedUtcTime': '2020-07-14T09:53:36.6114953Z', 'PartitionId': 1, 'EventEnqueuedUtcTime': '2020-07-14T09:53:36.5600000Z', 'IoTHub': {'MessageId': None, 'CorrelationId': None, 'ConnectionDeviceId': 'MyRaspberryPi', 'ConnectionDeviceGenerationId': '637298794990585953', 'EnqueuedTime': '2020-07-14T09:53:36.0000000', 'StreamId': None}}
  [7/14/2020 9:53:43 AM] Device Method called
  [7/14/2020 9:53:43 AM] Device Method name       : start_fan
  [7/14/2020 9:53:43 AM] Device Method payload    : {}
  [7/14/2020 9:53:43 AM] Response status          : 200
  [7/14/2020 9:53:43 AM] Response payload         : {'Response': 'The fan has been (re)activated at 2020-07-14 11:53:43.095383'}
  ```
- 


<!-- USAGE EXAMPLES -->
## Usage

Use this space to show useful examples of how a project can be used. Additional screenshots, code examples and demos work well in this space. You may also link to more resources.

_For more examples, please refer to the [Documentation](https://example.com)_



<!-- ROADMAP -->
<!-- ## Roadmap

See the [open issues](https://github.com/sandervandorsten/azure-iothub-demo/issues) for a list of proposed features (and known issues). -->



<!-- CONTACT -->
## Contact

Sander van Dorsten - [Github](https://github.com/sandervandorsten) - sandervandorsten [at] gmail [dot] com

Project Link: [https://github.com/sandervandorsten/azure-iothub-demo](https://github.com/sandervandorsten/azure-iothub-demo)


## Related resources

* [Introduction to building IoT Solutions with Microsoft Azure (YouTube)](https://www.youtube.com/watch?v=Pxj9fYgcwV0)
* [**Azure For Everyone** Tutorials by Adam Marczak (YouTube)](https://www.youtube.com/channel/UCdmEIMC3LBil4o0tjaTbj0w)




<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/sandervandorsten/azure-iothub-demo.svg?
[contributors-url]: https://github.com/sandervandorsten/azure-iothub-demo/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/sandervandorsten/azure-iothub-demo.svg?
[forks-url]: https://github.com/sandervandorsten/azure-iothub-demo/network/members
[stars-shield]: https://img.shields.io/github/stars/sandervandorsten/azure-iothub-demo.svg?
[stars-url]: https://github.com/sandervandorsten/azure-iothub-demo/stargazers
[issues-shield]: https://img.shields.io/github/issues/sandervandorsten/azure-iothub-demo.svg?
[issues-url]: https://github.com/sandervandorsten/azure-iothub-demo/issues
[license-shield]: https://img.shields.io/github/license/sandervandorsten/azure-iothub-demo.svg?
[license-url]: https://github.com/sandervandorsten/azure-iothub-demo/blob/master/LICENSE
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/sandervandorsten
[code-style-shield]: https://img.shields.io/badge/code%20style-black-000000.svg
[code-style-url]: https://github.com/psf/black
[pyup-shield]: https://pyup.io/repos/github/sandervandorsten/azure-iothub-demo/shield.svg
[pyup-url]: https://pyup.io/repos/github/sandervandorsten/azure-iothub-demo/


[image-overview]: images/azure-iothub-demo.png
[image-back-end-simulation]: images/back-end-simulation.png
[image-functions]: images/functions.png
[image-deployment01]: images/deploying_infrastructure01.png
[image-deployment02]: images/deploying_infrastructure02.png
