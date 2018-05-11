# Deploy a Machine Learning Model as a web service

## Create a schema.json file
While schema generation is optional, it is highly recommended to define the request and input variable format for better handling.

Create a schema to automatically validate the input and output of your web service. The CLIs also use the schema to generate a Swagger document for your web service.

To create the schema, import the following libraries:
```
from azureml.api.schema.dataTypes import DataTypes
from azureml.api.schema.sampleDefinition import SampleDefinition
from azureml.api.realtime.services import generate_schema
```
Define the input variables. For example to define Numpy array:
```
inputs = {"input_array": SampleDefinition(DataTypes.NUMPY, yourinputarray)}
generate_schema(run_func=run, inputs=inputs, filepath='./outputs/service_schema.json')
```

## Create a scoring driver

You provide a score.py file, which loads your model and returns the prediction result(s) using the model.
The file must include two functions: init and run.

Instructor will review the score file for the lab


## Register a model
```
az ml model register --model <path to model file> --name <model name>
```

## Create a manifest
```
az ml manifest create --manifest-name <your new manifest name> -f <path to score file> -r <runtime for the image, e.g. spark-py>
```

## Create an image
```
az ml image create -n <image name> --manifest-id <the manifest name>
```

## Create and deploy the web service
```
az ml service create realtime --image-id <image id> -n <service name>
```

## Test the service
### Get information about the service
```
az ml service usage realtime -i <service id>
```
### Call the service
```
az ml service run realtime -i <service id> -d "{\"input_df\": [INPUT DATA]}"
```


## To customize the docker image
Create a `dependencies.yml` file
```
az ml image create -n <my Image Name> --manifest-id <my Manifest ID> -c dependencies.yml
```


