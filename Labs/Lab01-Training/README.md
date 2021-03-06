# Running a training job on a single GPU

The goal of this lab is to develop basic understanding of Azure Batch AI service and prepare Azure Batch AI environment for the labs focused on more advanced topics of distributed and parallel training.

**Follow the instructor**. The instructor will explain each step and deep dive into the algorithm used in the lab.


## Create the workshop's resource group and storage
All Azure resources created during the workshop will be hosted in the same resource group. It will simplify navigation and clean-up. This streamlined approach will work well for the workshop but does not represent the best practice for more complex production deployments. Refer to you organization's Azure guidance when setting up production grade environments.

### Activate the conda environment
```
source activate azure-cli
```

### Login to your Azure subscription
```
az login
```
If you have multiple subscriptions set the right one with
```
az account set -s <Subscription ID>
```

### Register Batch AI resource providers
Make sure that Batch AI resource providers are registered for you subscription. This is a one-time configuration.
```
az provider register -n Microsoft.BatchAI
az provider register -n Microsoft.Batch

```
### Create a resource group

```
az group create --name <Resource group name> --location eastus2
az configure --defaults group=<Resource group Name>
az configure --defaults location=eastus2
```

### Create a storage account
We will use an Azure file share backed up by  Azure storage to store training data, training scripts, training logs, checkpoints, and the final model.
```
az storage account create --name <Storage Account Name> --sku Standard_LRS
```

### Set environmnent variables
To simplify further commands we can set up environmental variables with the storage account name and the access key
```
az storage account keys list \
    -n <Storage account name> \
    -o table
export AZURE_STORAGE_ACCOUNT=<Storage account name>
export AZURE_STORAGE_ACCESS_KEY=<Storage account access key>
```

### Prepare Azure file share
This lab will utilize Azure File Shares as shared storage. As noted by the instructor other shared storage options (e.g. NFS and distributed file systems) may perform better for really large data sets.


#### Create a file share
```
az storage share create \
    --account-name <Storage account Name> 
    --name <File share name>
```

#### Create data and scripts directories in the share
```
az storage directory create \
    --share-name  <File share name>
    --name data
    
az storage directory create \
    --share-name  <File share name>
    --name scripts
```

#### Copy training data
The training data in the TFRecords format have been uploaded to a public container in Azure storage. Use the following command to copy the files to your file share. The `--dryrun` option allows you to verify the configuration before starting the asynchronous copy operation.

The instructor will provide you with <Storage account access key>
    

```
az storage file copy start-batch \
  --destination-path data \
  --destination-share <File share name> \
  --source-account-name azureailabs \
  --source-account-key k0sEc3OL07/c5Gy5L4LS4bPrvczX8Smktn2GGpISa9iQ4CGdPRvPQXZ71ZbAg5K3YCXpBJnk1kV/+ZahmO2KCA== \
  --source-container woodtfrecords \
  --pattern '*' \
  --dryrun
```


#### Copy the training scripts
```
cd <Repo root>/AMLWorkshop/Labs/Lab01-Training
az storage file upload --share-name <File share name> --source train_evaluate.py --path scripts
```

#### Verify that files are in the right folders
```
az storage file list --share-name <File share name> --path scripts -o table
az storage file list --share-name <File share name> --path data -o table
```

## Prepare a single node GPU cluster

```
az batchai cluster create \
  --name  <Cluster name> \
  --vm-size STANDARD_NC6 \
  --image UbuntuLTS \
  --min 1 \
  --max 1 \
  --storage-account-name <Storage account name> \
  --afs-name <File share name> \
  --afs-mount-path external \
  --user-name <User name> \
  --password <Password>
```

It is recommended, although not required, to use ssh keys instead of passwords

```
az batchai cluster create \
  --name  <Cluster name> \
  --vm-size STANDARD_NC6 \
  --image UbuntuLTS \
  --min 1 \
  --max 1 \
  --storage-account-name <Storage account name> \
  --afs-name <File share name> \
  --afs-mount-path external \
  --ssh-key ~/.ssh/id_rsa.pub \
  --user-name $USER 
  
```
To generate `ssh` keys you can use an app of your choice including ssh-keygen:
```
ssh-keygen -t rsa
```

Or you can generate ssh keys automatically during cluster creation
```
az batchai cluster create \
  --name  <Cluster name> \
  --vm-size STANDARD_NC6 \
  --image UbuntuLTS \
  --min 1 \
  --max 1 \
  --storage-account-name <Storage account name> \
  --afs-name <File share name> \
  --afs-mount-path external \
  --generate-ssh-keys \
  --user-name $USER 
```

### Get cluster status
```
az batchai cluster list -o table
```

### List ssh connection info for the nodes in a cluster
```
az batchai cluster list-nodes -n <Cluster name> -o table
```

### Explore the cluster's node
```
ssh <IP address> -p <port>
cd /mnt/batch/tasks/shared/LS_root/mounts
```


## Create a training job

Walkthrough the job's python files and JSON template file for the job configuration `job.json'`

### Create job
```
az batchai job create \
  --name <Job name> \
  --cluster-name <Cluster name> \
  --config job.json
```
## Monitor the job
### List the jobs
```
az batchai job list -o table
```
### Show the job's status
```
az batchai job show -n <Job name>
```

### List stdout and stderr output
```
az batchai job file list \
  --name <Job nme> \
  --output-directory-id stdouterr
```

### Stream files from output directories
```
az batchai job file stream \
  -n <Job name> \
  -d stdouterr \
  -f <File to stream>
```
### Use Azure portal
You can also use Azure portal to monitor the job. 



### Terminate/Delete the job
If you want to terminate or delet the job you can use the following commands
```
az batchai job terminate --name <Job name>
az batchai job delete --name <Job name>
```

## Delete the  cluster
```
az batchai cluster delete --name <Cluster name>
```

