import numpy as np
from tensorflow.python.keras.models import load_model

def init():
    global model
    model = load_model(model_path)
    
def run(rawdata):
    try:
        image_list = json.loads(rawdata)['image']
        images = np.asarray(image_list)
        images = images/255
        results = model.predict(data)
    except Exception as e:
        results = str(e)
    return json.dumps({"results":results})
    

