# Workshop environment set up

## Install Anaconda for Python 3
To install Anaconda for Python 3 follow the instructions at:

https://conda.io/docs/user-guide/install/index.html

## Install Azure CLI 
We are going to install all workshop dependencies in an isolated conda environment

### Create and activate a conda environment
```
conda create -n azure-cli python=3.5 anaconda
source activate azure-cli
```

### Install Azure CLI
```
pip install azure-cli
```

### Deactivate the environment
```
source deactivate azure-cli
```

## Install Azure ML Model Management CLI
At this point Azure ML Model Management CLI is not based on the latest version of Azure CLI. As such we will install it in an isoloate conda environmet

### Create and activate a conda environment
```
conda create -n azure-ml python=3.5 anaconda
source activate azure-ml
```

### Install Azure ML Model Managment CLI

```
pip install -r https://aka.ms/az-ml-o16n-cli-requirements-file
```

### Deactivate the environment
```
source deactivate azure-ml
```




## Clone the workshop's repository

Clone the workshop's repository in your preferred location

```
git clone https://github.com/jarokaz/AMLWorkshop.git
```





