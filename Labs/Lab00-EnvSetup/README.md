# Workshop environment set 

## Install Anaconda for Python 3
To install Anaconda for Python 3 follow the instructions at:

https://conda.io/docs/user-guide/install/index.html

## Install Azure CLI 
We are going to install all workshop dependencies in an isolated conda environment

### Create and activate a conda environment
```
conda create -n <Env name> python=3.5 anaconda
source activate <Env name>
```

### Install Azure CLI
```
pip install azure-cli
```


### Install Azure ML Model Managment CLI

```
pip install azure-cli-ml
```


## Clone the workshop's repository

Clone the workshop's repository in your preferred location

```
git clone https://github.com/jarokaz/AMLWorkshop.git
```





