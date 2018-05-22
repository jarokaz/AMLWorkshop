# Azure ML Model Management

### Download the model file to Lab02 workspace
```
cd AMLWorkshop/Labs/Lab02-Deployment/
wget https://azureailabs.blob.core.windows.net/models/lumber.h5
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
To create local only deployment environment skip the `--cluster` option

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

You can switch between a local and cluster mode using
```
az ml env cluster
az ml env local
```



