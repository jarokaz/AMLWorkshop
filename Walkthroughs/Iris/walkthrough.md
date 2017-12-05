## Prepare remote HDInsight environment
### Create a compute target on the remote HDInsight
```
az ml computetarget attach cluster --name myhdi --address jkhdi-ssh.azurehdinsight.net --username sshuser --password <password> 
```


## Deploy a model
### Download the model pickle file
Download the model pickle file from the `outputs` directory of the latest run
### Generate the JSON schema file
Run `score_iris.py` to generate the schema file. The file will be put into the `outputs` folder of the run.
### Verify that Azure resource provider Microsoft.ContainerRegistry is registered in you subscription
```
az provider list --query "[].{Provider:namespace, Status:registrationState}" --out table
```
If it is not registered register it with the following command
```
az provider register --namespace Microsoft.ContainerRegistry
```
### Create a cluster operationalization environment
```
az ml env setup -n jkmlenv --location westcentralus -c
```

### Set the model management account
```
az ml account modelmanagement set -n jkmlmodelmgmt -g jkmlrg
```

### Set the operationalization environment
```
az ml env set -n jkmlenv -g jkmlrg
```

### Create a real-time web service in one command
```
az ml service create realtime -f score_iris.py --model-file model.pkl -s service_schema.json -n irisapp -r python --collect-model-data true
```

### Run the real-time web service
```
az ml service run realtime -i irisapp -d "{\"input_df\": [{\"petal width\": 0.25, \"sepal length\": 3.0, \"sepal width\": 3.6, \"petal length\": 1.3}]}"
```
