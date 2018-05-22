# Workshop environment set up

## Install Anaconda for Python 3
To install Anaconda for Python 3 follow the instructions at:

https://conda.io/docs/user-guide/install/index.html

## Install Azure CLI Azure ML CLI
You will need to install Azure CLI on your workstation. We are going to install all workshop dependencies in an isolated environment

### Create and activate a conda environment
```
conda create -n <env name> python=3.5 anaconda
source activate <env name>
```

### Install Azure CLI
```
pip install azure-cli
```

### Install Azure ML Model Management CLI
```
pip install -r https://aka.ms/az-ml-o16n-cli-requirements-file
```

### Logon to Azure
```
az login
```

### Set the default subscriptions
```
az account set -s <subscription id>
```


### Register providers
Before using Azure ML CLI you need to register Azure ML resource providers. This is a one time activity

```
az provider register -n Microsoft.MachineLearningCompute
az provider register -n Microsoft.ContainerRegistry
az provider register -n Microsoft.ContainerService
```

## Clone the workshop's repository

Clone the workshop's repository in your preferred location

```
git clone https://github.com/jarokaz/AMLWorkshop.git
```





