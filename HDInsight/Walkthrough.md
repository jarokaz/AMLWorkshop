### Create HDInsight computer target
```
az ml computetarget attach --name jkhdi --address $jkspark-ssh.azurehdinsight.net --type cluster --username demouser --password $password 
```
