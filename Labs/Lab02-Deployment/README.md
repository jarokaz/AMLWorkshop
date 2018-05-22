# Azure ML Model Management

## Switch to Azure ML CLI environment
```
source activate azure-ml
```

## Download the model file to Lab02 workspace
```
cd AMLWorkshop/Labs/Lab02-Deployment/
wget https://azureailabs.blob.core.windows.net/models/lumber.h5
```

## Set up Model Management
Logon to Azure and set up the default subscription
```
az login
```

Make sure that you are using a right subscription
```
az account list -o table
```


### Register providers
Register a few environment providers. This is a one time activity
```
az provider register -n Microsoft.MachineLearningCompute
az provider register -n Microsoft.ContainerRegistry
az provider register -n Microsoft.ContainerService
```

### Create a Model Management Account
Use the same resource group as for the first lab

```
az ml account modelmanagement create -l eastus2 -n <account name> -g <resource group name> --sku-instances 1 --sku-name S1
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

The environment setup command creates the following resources in your subscription:

- A resource group (if not provided, or if the name provided does not exist)
- A storage account
- An Azure Container Registry (ACR)
- An Application insights account

After the command completes, set the created environment as a default environment
```
az ml env set -n <environment name> -g <resource group name>
```

You can switch between a local and cluster mode using
```
az ml env cluster
az ml env local
```



