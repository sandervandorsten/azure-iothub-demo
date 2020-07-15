# Deploying Infrastructure
<img src="https://raw.githubusercontent.com/sandervandorsten/azure-iothub-demo/master/images/azure-iothub-demo.png" alt="Infrastructure Overview" border="1">

## Prerequisites

- Azure account with a subscription you are allowed to create resources in (Free Trial Subscription should do)
- Make sure you have [installed the Azure CLI](https://docs.microsoft.com/en-us/cli/azure/install-azure-cli?view=azure-cli-latest) on your computer
- basic knowledge of git + python virtual environments
- access to a bash-like terminal

## Deploying Infrastructure
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

<img src="https://raw.githubusercontent.com/sandervandorsten/azure-iothub-demo/master/images/deploy-infra01.png" alt="Infrastructure Deployment" border="1">

## Next Steps
Now you have deployed your infrastructure, we can [start and configure the different services](Installation/iot-hub.md) that we're going to need to run our application.