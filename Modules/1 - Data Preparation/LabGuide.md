# Data Preparation


### Setup the compute target 

```
az ml computetarget attach --name dockervm --address jkdslxcpuvm.westus2.cloudapp.azure.com --username demouser --password $password --type remotedocker
```

This command creates two configuration files in teh aml_config folder of the project:
- dockervm.compute: This file contains the connection and configuration information for a remote execution target.
- dockervm.runconfig: This file is a set of run options used within the Workbench application.

Change the configuration in dockervm.runconfig to:

```
PrepareEnvironment: true 
CondaDependenciesFile: Config/conda_dependencies.yml 
SparkDependenciesFile: Config/dsvm_spark_dependencies.yml
```



