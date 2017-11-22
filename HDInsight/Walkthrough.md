### Create HDInsight computer target
```
az ml computetarget attach --name jkhdi --address jkspark-ssh.azurehdinsight.net --type cluster --username demouser --password $password 
```
### Modify jkhdi.runconfig
```
PrepareEnvironment: true 
CondaDependenciesFile: Config/conda_dependencies.yml 
SparkDependenciesFile: Config/hdi_spark_dependencies.yml
```

### Prepare the project environment on the cluster
```
az ml experiment prepare -c jkhdi
```


