### Create compute target
```
az ml computetarget attach --name dockerdsvm --address jkdslxcpuvm.westus2.cloudapp.azure.com --type remotedocker --username demouser   remotedocker --password $password 
```
### Prepare compute target
```
az ml experiment prepare -c dockerdsvm
```
Remember to edit the framework in dockerdsvm.runconfig from PySpark to Python
"Framework": "Python"

### Submit experiment
```
az ml experiment submit -c dockerdsvm .\iris_sklearn.py
```
