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
az ml env setup -n jkpaypaldemo --location westus2
```
