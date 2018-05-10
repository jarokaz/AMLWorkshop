import tensorflow as tf

import numpy as np
import argparse
from time import strftime, time 
from os.path import join, split
import os

from trainer.model import display_model_summary, model_fn

 
def scale_image(image):

    """Scales image pixesl between -1 and 1"""
    image = image / 127.5
    image = image - 1.
    return image


 

def _parse(example_proto, augment):

    features = {"image": tf.FixedLenFeature((), tf.string, default_value=""),
                "label": tf.FixedLenFeature((), tf.int64, default_value=0)}

    parsed_features = tf.parse_single_example(example_proto, features)
    image = tf.decode_raw(parsed_features['image'], tf.uint8)
    image = tf.cast(image, tf.float32)
    image = scale_image(image)
    image = tf.reshape(image, IMAGE_SHAPE)
    
    if augment:
      image = tf.image.random_flip_left_right(image)
      image = tf.image.random_hue(image, max_delta=0.1)
        
    label = parsed_features['label']
    label = tf.one_hot(label, NUM_CLASSES)

    return  image, label

  
def input_fn(file, train, batch_size, buffer_size=4000):
   
    if train:
        rep = None 
        augment = True
    else:
        rep = 1
        augment = False

    dataset = tf.data.TFRecordDataset(file)
    parse = lambda x: _parse(x, augment)
    dataset = dataset.map(parse)
    
    if train:
        dataset = dataset.shuffle(buffer_size)
        
    dataset = dataset.batch(batch_size)
    dataset = dataset.repeat(rep)

    iterator = dataset.make_one_shot_iterator()
    features, labels = iterator.get_next()
    
    return {"image": features}, labels

def serving_input_fn():
    input_image = tf.placeholder(shape=INPUT_SHAPE, dtype=tf.uint8)
    image = tf.cast(input_image, tf.float32)
    scaled_image = scale_image(image)
    
    return tf.estimator.export.ServingInputReceiver({'image': scaled_image}, {'image': input_image})

    
IMAGE_SHAPE = (112, 112, 3,)
NUM_CLASSES = 7
INPUT_NAME = 'image'
INPUT_SHAPE = (None, 112, 112, 3)


def vgg16base1(image_shape, input_name, hidden_units):
    
    x = Input(shape=image_shape, name=input_name)
    base_model = VGG16(weights='imagenet',
                   include_top=False,
                   input_tensor=x)
    
    for layer in base_model.layers:
        layer.trainable =  False
    
    conv_base = base_model.output
  
    a = Flatten()(conv_base)
    a = Dense(hidden_units, activation='relu')(a)
    a = Dropout(0.5)(a)
    y = Dense(NUM_CLASSES, activation='softmax')(a)
    
    model = Model(inputs=x, outputs=y)
    
    return model
  

def model_fn(hidden_units, ckpt_folder):
    
    model_fn =  vgg16base1(IMAGE_SHAPE, INPUT_NAME, hidden_units) 
    
    optimizer = Adadelta()

    metrics = ['categorical_accuracy']
    loss = 'categorical_crossentropy'

    model_fn.compile(loss=loss, optimizer=optimizer, metrics=metrics)
    
    estimator = model_to_estimator(keras_model = model_fn, model_dir=ckpt_folder)
    
    return estimator



def train_evaluate():
    
    estimator = model_fn(FLAGS.hidden_units, FLAGS.job_dir)
    
    train_input_fn = lambda: input_fn(file=train_file, batch_size=batch_size, train=True)
    valid_input_fn = lambda: input_fn(file=valid_file, batch_size=batch_size, train=False)

    train_spec = tf.estimator.TrainSpec(input_fn=train_input_fn, max_steps=max_steps)
    
    export_latest = tf.estimator.FinalExporter("bclassifier", serving_input_fn)
    eval_spec = tf.estimator.EvalSpec(input_fn=valid_input_fn, 
                                      steps=eval_steps,
                                      exporters=export_latest)

    tf.estimator.train_and_evaluate(estimator, train_spec, eval_spec)


    
FLAGS = tf.app.flags.FLAGS

# Default global parameters
tf.app.flags.DEFINE_integer('batch_size', 32, "Number of images per batch")
tf.app.flags.DEFINE_integer('max_steps', 100000, "Number of steps to train")
tf.app.flags.DEFINE_string('job_dir', '../../../jobdir/run1', "Checkpoints")
tf.app.flags.DEFINE_string('data_dir', '../../../data/wood', "Data")
tf.app.flags.DEFINE_float('lr', 0.0005, 'Learning rate')
tf.app.flags.DEFINE_string('verbosity', 'INFO', "Control logging level")
tf.app.flags.DEFINE_integer('num_parallel_calls', 12, 'Input parallelization')
tf.app.flags.DEFINE_integer('throttle_secs', 300, "Evaluate every n seconds")
tf.app.flags.DEFINE_integer('hidden_units', 512, "Hidden units in the FCNN layer")


def main(argv=None):
 
  if tf.gfile.Exists(FLAGS.job_dir):
    tf.gfile.DeleteRecursively(FLAGS.job_dir)
  tf.gfile.MakeDirs(FLAGS.job_dir)
  
  train_evaluate()
  

if __name__ == '__main__':
  tf.app.run()