import numpy as np
from tensorflow.python.keras.models import load_model

def init():
    global model
    model = load_model(model_path)
    
def run(rawdata):
    try:
        data = json.loads(rawdata)['image']
        data = numpy.array(data).reshape(1, data.shape)
        results = model.predict(data)
    except Exception as e:
        results = str(e)
    return json.dumps({"results":results})
    

