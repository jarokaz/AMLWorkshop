
# Import the relevant modules to be used later
from __future__ import print_function
import gzip
import numpy as np
import os
import shutil
import struct
import sys
import time
import pandas 

import cntk as C
from azureml.logging import get_azureml_logger

# Read a CTF formatted text (as mentioned above) using the CTF deserializer from a file
def create_reader(path, is_training, input_dim, num_label_classes):
    return C.io.MinibatchSource(C.io.CTFDeserializer(path, C.io.StreamDefs(
        labels = C.io.StreamDef(field='labels', shape=num_label_classes, is_sparse=False),
        features   = C.io.StreamDef(field='features', shape=input_dim, is_sparse=False)
    )), randomize = is_training, max_sweeps = C.io.INFINITELY_REPEAT if is_training else 1)

# Defines a utility that prints the training progress
def print_training_progress(trainer, mb, frequency, verbose=1):
    training_loss = "NA"
    eval_error = "NA"

    if mb%frequency == 0:
        training_loss = trainer.previous_minibatch_loss_average
        eval_error = trainer.previous_minibatch_evaluation_average
        if verbose: 
            print ("Minibatch: {0}, Loss: {1:.4f}, Error: {2:.2f}%".format(mb, training_loss, eval_error*100))
        
    return mb, training_loss, eval_error

# Create the network architecture
def create_model(features):
    with C.layers.default_options(init = C.layers.glorot_uniform(), activation = C.ops.relu):
            h = features
            for _ in range(num_hidden_layers):
                h = C.layers.Dense(hidden_layers_dim)(h)
            r = C.layers.Dense(num_output_classes, activation = None)(h)
            return r


if __name__ == '__main__':
    run_logger = get_azureml_logger() 

    #Define network architecture hyperparameters
    learning_rate = 0.2
    hidden_layers_dim = 10 
    num_hidden_layers = 1

    # Define the data dimensions
    input_dim = 784
    num_output_classes = 10

    # load hyperparameters from command line arguments
    if len(sys.argv) > 1:
        hidden_layers_dim = int(sys.argv[1])
        
    if len(sys.argv) > 2:
        num_hidden_layers = int(sys.argv[2])

    if len(sys.argv) > 3:
        learning_rate = float(sys.argv[3])


    # log hyperparameters for this run
    run_logger.log("Learning rate", learning_rate) 
    run_logger.log("Hidden layers dimmension", hidden_layers_dim)
    run_logger.log("No of hidden layers", num_hidden_layers)

    print("Hidden layers dimension: {0}".format(hidden_layers_dim))
    print("No of hidden layers: {0}".format(num_hidden_layers))
    print("Learning rate: {0}".format(learning_rate))



    # Ensure we always get the same amount of randomness
    np.random.seed(0)

    datapath = os.environ['AZUREML_NATIVE_SHARE_DIRECTORY']
    train_file = datapath + "MNIST_train.txt"
    test_file = datapath + "MNIST_validate.txt"

    print("Using training file:  {0}".format(train_file))
    print("Using testing file:  {0}".format(test_file))

    input = C.input_variable(input_dim)
    label = C.input_variable(num_output_classes)

    # Scale the input to 0-1 range by dividing each pixel by 255.
    z = create_model(input/255.0)

    loss = C.cross_entropy_with_softmax(z, label)
    label_error = C.classification_error(z, label)

    # Instantiate the trainer object to drive the model training
    lr_schedule = C.learning_rate_schedule(learning_rate, C.UnitType.minibatch)
    learner = C.sgd(z.parameters, lr_schedule)
    trainer = C.Trainer(z, (loss, label_error), [learner])


    # Initialize the parameters for the trainer
    minibatch_size = 64
    num_samples_per_sweep = 60000
    num_sweeps_to_train_with = 10
    num_minibatches_to_train = (num_samples_per_sweep * num_sweeps_to_train_with) / minibatch_size

    # Create the reader to training data set
    reader_train = create_reader(train_file, True, input_dim, num_output_classes)

    # Map the data streams to the input and labels.
    input_map = {
        label  : reader_train.streams.labels,
        input  : reader_train.streams.features
    } 

    # Run the trainer on and perform model training
    training_progress_output_freq = 500
    
    errors = []
    losses = []
    for i in range(0, int(num_minibatches_to_train)):        
        # Read a mini batch from the training data file
        data = reader_train.next_minibatch(minibatch_size, input_map = input_map)
        
        trainer.train_minibatch(data)
        batchsize, loss, error = print_training_progress(trainer, i, training_progress_output_freq, verbose=1)
        if (error != 'NA') and (loss != 'NA'):
            errors.append(float(error))
            losses.append(float(loss))
    
    # Log the training error and loss
    run_logger.log("Training Losses", losses)
    run_logger.log("Training Errors",errors)
    

    # Read the validation data
    reader_test = create_reader(test_file, False, input_dim, num_output_classes)

    test_input_map = {
        label  : reader_test.streams.labels,
        input  : reader_test.streams.features,
    }

    # Test data for trained model
    test_minibatch_size = 512
    num_samples = 10000
    num_minibatches_to_test = num_samples // test_minibatch_size
    test_result = 0.0

    
    for i in range(num_minibatches_to_test):    
        # We are loading test data in batches specified by test_minibatch_size
        # Each data point in the minibatch is a MNIST digit image of 784 dimensions 
        # with one pixel per dimension that we will encode / decode with the 
        # trained model.
        data = reader_test.next_minibatch(test_minibatch_size,
                                        input_map = test_input_map)

        eval_error = trainer.test_minibatch(data)
        test_result = test_result + eval_error
    
    accuracy = 100 - (test_result * 100) / num_minibatches_to_test
    # Average accuracy across all test minibatches
    print("Accuracy: {0:.2f}%".format(accuracy))
 
    # Log validation accuracy 
    run_logger.log("Accuracy", accuracy)
   
    # save model to outputs folder
    z.save('outputs/cntk.model')
