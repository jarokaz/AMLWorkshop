import tensorflow as tf
from tensorflow.python.keras.datasets import mnist, cifar10
from tensorflow.python.keras import Model, Input
from tensorflow.python.keras.layers import Dense, Dropout, Flatten, Conv2D, MaxPooling2D
from tensorflow.python.keras.optimizers import Adadelta, Adam
from tensorflow.python.keras.callbacks import TensorBoard

from tensorflow.python.keras.applications.vgg16 import VGG16
from tensorflow.python.keras import models
from tensorflow.python.keras import layers


import numpy as np
from time import time

from time import strftime, time 
from os.path import join
import os



def load_tfrecords(file):
    record_iterator = tf.python_io.tf_record_iterator(path=file)
    
    i=0
    images = []
    labels = []
    for string_record in record_iterator:
        example = tf.train.Example()
        example.ParseFromString(string_record)
        
        image_feature = example.features.feature['image'].bytes_list.value[0]
        label_feature = example.features.feature['label'].int64_list.value[0]
        
        image = np.fromstring(image_feature, dtype=np.uint8)
           
        assert IMAGE_SHAPE[0]*IMAGE_SHAPE[1]*IMAGE_SHAPE[2] == image.shape[0]
        
        image = np.reshape(image, IMAGE_SHAPE)
        label = label_feature
        
        images.append(image)
        labels.append(label)
       
    images = np.asarray(images)
    labels = np.asarray(labels)
    
    return  images, labels
    

def load_data_from_tfrecords(training_file, validation_file):
    
    x_train, y_train = load_tfrecords(training_file)
    x_test, y_test = load_tfrecords(validation_file)
    
    return x_train, y_train, x_test, y_test



def VGG16base():
  
    input = Input(shape=IMAGE_SHAPE, name=INPUT_NAME)
    conv_base = VGG16(weights='imagenet',
                   include_top=False,
                   input_tensor=input)
    
    for layer in conv_base.layers:
        layer.trainable = False

    a = Flatten()(conv_base.output)
    a = Dense(256, activation='relu')(a)
    y = Dense(NUM_CLASSES, activation='softmax')(a)
    
    model = Model(inputs=input, outputs=y)
    
    model.compile(loss='categorical_crossentropy',
                  optimizer=Adadelta(),
                  metrics=['acc'])
    
    return model


IMAGE_SHAPE = (112, 112, 3)
NUM_CLASSES = 7
INPUT_NAME = 'images'

    
def train_evaluate():
    

    x_train, y_train, x_test, y_test = load_data_from_tfrecords(FLAGS.training_file, FLAGS.validation_file)
   
    y_train = tf.keras.utils.to_categorical(y_train, NUM_CLASSES)
    x_train = x_train/255

    y_test = tf.keras.utils.to_categorical(y_test, NUM_CLASSES)
    x_test = x_test/255 
    

    model = VGG16base()
    

    tensorboard = TensorBoard(log_dir=FLAGS.log_dir)

    model.fit(x_train, y_train, 
                  validation_data = (x_test, y_test),
                  shuffle = True,
                  batch_size=FLAGS.batch_size,
                  epochs=FLAGS.epochs,
                  verbose=1, 
                  callbacks=[tensorboard])


    model.save(FLAGS.save_model_path)

    
FLAGS = tf.app.flags.FLAGS

# Default global parameters
tf.app.flags.DEFINE_integer('batch_size', 32, "Number of images per batch")
tf.app.flags.DEFINE_integer('epochs', 20, "Number of epochs to train")
tf.app.flags.DEFINE_string('log_dir', '../../../logdir/lumber1', "Checkpoints")
tf.app.flags.DEFINE_string('training_file', '../../../data/wood/tfrecords/training.tfrecords', "Training file")
tf.app.flags.DEFINE_string('validation_file', '../../../data/wood/tfrecords/validation.tfrecords', "Validation file")
tf.app.flags.DEFINE_string('save_model_path', '../../../SaveModel/lumber1.h5', 'Filename to save model to')
tf.app.flags.DEFINE_string('verbosity', 'INFO', "Control logging level")



def main(argv=None):
 
  if tf.gfile.Exists(FLAGS.log_dir):
    tf.gfile.DeleteRecursively(FLAGS.log_dir)
  tf.gfile.MakeDirs(FLAGS.log_dir)
  
  train_evaluate()
  

if __name__ == '__main__':
  tf.app.run()
