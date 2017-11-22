### Create VM compute target
```
az ml computetarget attach --name dockerdsvm --address jkdslxcpuvm.westus2.cloudapp.azure.com --type remotedocker --username demouser   --password $password 
```
### Prepare VM compute target
```
az ml experiment prepare -c dockerdsvm
```
Remember to edit the framework in dockerdsvm.runconfig from PySpark to Python
"Framework": "Python"

### Submit experiment to VM
```
az ml experiment submit -c dockerdsvm .\iris_sklearn.py
```

### Create HDInsight compute target
```
az ml computetarget attach --name myhdi --address jkpaypal-ssh.azurehdinsight.net --username sshuser --type cluster --password <password> 
```

### Submit experiment to Spark
```
az ml experiment submit -c myhdi .\iris_spark.py
```

### Operationalize the model locally

Prepare operationalization environment
```
az ml env setup -n jkpaypaldemo --location westcentralus
```

Show operationalization environments
```
az ml env show -g jkpaypaldemorg -n jkpaypaldemo
```

Set operationalization environments
```
az ml env set -g jkpaypaldemorg -n jkpaypaldemo
```

Show the current operationalization environment
```
az ml env show
```
Set model management account
```
az ml account modelmanagement set  -g jkmlrg -n jkmlmodelmgmt
```

Create a real-time web service 

Register model
```
az ml model register --model model.pkl --name model.pkl
```
Create manifest
```
az ml manifest create --manifest-name <new manifest name> -f score_iris.py -r python -i <model ID> -s service_schema.json
```
Create image
```
az ml image create -n irisimage --manifest-id <manifest ID>
```

Create the service
```
az ml service create realtime --image-id <image ID> -n irisapp --collect-model-data true
```

Show the service
```
az ml service show realtime -i irisapp
```

Test the service
```
az ml service run realtime -i irisapp -d "{\"input_df\": [{\"petal width\": 0.25, \"sepal length\": 3.0, \"sepal width\": 3.6, \"petal length\": 1.3}]}"
```
