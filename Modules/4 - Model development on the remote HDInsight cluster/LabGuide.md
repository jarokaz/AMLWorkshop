### Attache HDInsight computer target
```
az ml computetarget attach --name myhdi --address $jkpaypal-ssh.azurehdinsight.net --type cluster --username sshuser --password $password 
```

### Modify runconfig
```
PrepareEnvironment: true 
CondaDependenciesFile: Config/conda_dependencies.yml 
SparkDependenciesFile: Config/hdi_spark_dependencies.yml
```
### Submit the etl job
```
az ml experiment submit -a -t myhdi -c myhdi ./Code/train.py Config/storageconfig.json

```
