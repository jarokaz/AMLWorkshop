# Azure ML Model Management

## Prepare workshop environment
### Create DL VM
Follow the instructor
After the VM has been provisioned connect to it using `ssh` client of your choice

### Configure Docker
```
sudo /opt/microsoft/azureml/initial_setup.sh
```

### Clone the workshop repo
```
cd ~/notebooks
git clone https://github.com/jarokaz/AMLWorkshop.git
```
### Download the model file to Lab04 workspace
```
cd AMLWorkshop/Labs/Lab04-ModelDeployment/
wget https://azaiworkshopst.blob.core.windows.net/wood/lumber1.h5
```

## Deploy model locally
Logon to Azure and set up the default subscription
```
az login
az account set -s <Subscription ID>
```

### Set up a local deployment environment
Register a few environment providers. This is a one time activity
```
az provider register -n Microsoft.MachineLearningCompute
az provider register -n Microsoft.ContainerRegistry
az provider register -n Microsoft.ContainerService
```
Create a resource group

```
az group create --name <Resource group name> --location eastus2
```

Create a local environment

```
az ml env setup -l  eastus2 -n [your environment name] -g [your resource group]
```
The local environment setup command creates the following resources in your subscription:

- A resource group (if not provided, or if the name provided does not exist)
- A storage account
- An Azure Container Registry (ACR)
- An Application insights account
- After setup completes successfully, set the environment to be used using the following command:








