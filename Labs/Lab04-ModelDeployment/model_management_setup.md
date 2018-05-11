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

## Set up Model Management
Logon to Azure and set up the default subscription
```
az login
az account set -s <Subscription ID>
```

### Register providers
Register a few environment providers. This is a one time activity
```
az provider register -n Microsoft.MachineLearningCompute
az provider register -n Microsoft.ContainerRegistry
az provider register -n Microsoft.ContainerService
```

### Create a Model Management Account
```
az group create -l eastus2 -n <resource group name>
az ml account modelmanagement create -l eastus2 -n <account name> -g <resource group name> --sku-instances <number of instances> --sku-name <Pricing tier for example S1>
```

### Set a model management account
```
az ml account modelmanagement set -n <account name> -g <resource group>
```
### Create a deployment environment
```
az ml env setup --cluster -n <env name> -g <resource group> -l eastus2

```

Wait till the operation completes. You can monitor the status using:
```
az ml env show -g <resource group> -n <env name>
```

The local environment setup command creates the following resources in your subscription:

- A resource group (if not provided, or if the name provided does not exist)
- A storage account
- An Azure Container Registry (ACR)
- An Application insights account
- After setup completes successfully, set the environment to be used using the following command:

After the command completes, set the created environment as a default environment
```
az ml env set -n <environment name> -g <resource group name>
```

## Create a local deployment environment

```
az ml env setup -l  eastus2 -n <environment name> -g <resource group>
```

## Deploy a model as a web service



