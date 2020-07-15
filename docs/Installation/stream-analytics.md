<h1> <img src="https://raw.githubusercontent.com/sandervandorsten/azure-iothub-demo/master/images/stream-analytics-logo.png" alt="Stream Analytics Logo" alt="IoT Hub Logo" align="left" style="height:40px;padding:5px"> Stream Analytics: Starting the Analysis Job</h1>

<img src="https://raw.githubusercontent.com/sandervandorsten/azure-iothub-demo/master/images/azure-iothub-demo.png" alt="Infrastructure Overview" border="1">

## What is Stream Analytics
Azure Stream Analytics is a real-time analytics and complex event-processing engine that is designed to analyze and process high volumes of fast streaming data from multiple sources simultaneously. Patterns can be identified from a number of input sources including devices, sensors and applications. These patterns can be used to trigger actions and initiate workflows such as creating alerts, feeding information to a reporting tool, or storing transformed data for later use. 

## Usage
We will use Stream Analytics to ingest data from IoT Hub and move it to both Blob Storage and a Service Bus Queue for more complex actions. This is already configured for you when the infrastructure was deployed, the only thing we need to do is **Start the Streaming Job**.

## Installation
1. **Navigate to your Stream Analytics resource** and you will see the the **Overview page**. 
2. On the bottom right you will see the **Query** that is already pre-defined. This query does 2 things. (it shown below as well for convenience)
    1. it moves all data from the **input called** `iothub` **to the output called `blobstorage`**
    2. it moves all data where `temperature > 29` from the **input called** `iothub` **to the output called** `servicebus`
    ```SQL  hl_lines="14 15"
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
3. If you want to learn how this input and outputs are actually coupled to the IoT Hub and Service Bus in our infrastructure, you can navigate to the menu blades on the left of your screen called **inputs** and **outputs** (under **Job Topology**). At deployment time, the bindings to these services were already done for you so you don't have to worry about them.

    ??? tip "Creating input and output bindings"
        If you want to learn how to create these yourself, **I recommend [This video](https://www.youtube.com/watch?v=NbGmyjgY0pU) by Adam Marczak** on Azure Stream Analytics. I fact, I recommend all his Azure tutorials, which helped me a great deal in developing this project.
        
4. Now you know roughly what happens in Stream Analytics, we can **start this Stream Analytics Job** to start processing incoming requests. Remember that we're not sending any data from a device yet to our application, but we're just preconfiguring the infrastrature. Press the **> Start** button **at the top of the Overview** menu to start the job. It takes about a minute or two to activate, you can see the status straight below it. (see screenshot below)

<p align="center">
  <img src="https://raw.githubusercontent.com/sandervandorsten/azure-iothub-demo/master/images/streaming.png" alt="Stream Analytics" border="2" height="100%">
</p>

## Recap
You have sucessfully started your Steam Analytics job! In a bit, our Raspberry Pi Data will flow through this job to the connected services. Now it's not doing anything yet though, So lets quickly finish up our infrastructure setup to start sending data. 

???+ warning "Cost Saving Tip"
    Pause your stream Analytics job once your done developing. **You don't pay per request, but per hour.**

## Next Steps
The last service we need to get up and running is [Azure Function](function.md)