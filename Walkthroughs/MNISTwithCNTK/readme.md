# Classifying MNIST dataset using CNTK

This walkthrough demonstrates how to train a Fully Connected Neural Network using CNTK's graph API..

The code in this sample is adapted from the following CNTK tutorials:
1. https://github.com/Microsoft/CNTK/blob/v2.0/Tutorials/CNTK_103A_MNIST_DataLoader.ipynb
2. https://github.com/Microsoft/CNTK/blob/v2.0/Tutorials/CNTK_103C_MNIST_MultiLayerPerceptron.ipynb


## Running a training job locally

Before running the script for the first time you need to install the right version of CNTK into the local Python environment.

For example to install CNTK v2.2 for CPU run the following command in your CLI command prompt 
```
# You only need to do this once. This whl file is for Windows operating system.
$ pip install https://cntk.ai/PythonWheel/CPU-Only/cntk-2.2-cp35-cp35m-win_amd64.whl
```
Once you install CNTK, you can now run your script using the following command: 
```
# submit the experiment to local execution environment
$ az ml experiment submit -c local cntk_mnist.py
```
You can also start the job from the AML Workbench's GUI.

## Running it on a VM with GPU
With computationally expensive tasks like training a neural network, you can get a huge performance boost by running it on a GPU-equipped machine.

>Note, if your local machine already has NVidia GPU chips, and you have installed the CUDA libraries and toolkits, you can directly run the script using local compute target. Just be sure to pip-install the CNTK Python package for GPU for your OS. The below instructions are specifically for running script in a remote VM equipped with GPU.

### Step 1. Provision a GPU Linux VM 
Create an Ubuntu-based Deepl Learning Virtual Machine(DSVM) in Azure portal using one of the NC-series VM templates. NC-series VMs are the VMs equipped with NVidia Tesla K80 GPUs.
The Deep Learning Virtual Machine template includes all the necessary NVidia drivers and a number of Deep Learning toolkits including CNTK. 

### Step 2. Attach the compute context
Run following command to add the GPU VM as a compute target in your current project:
```
$ az ml computetarget attach --name mygpuvm --address <ip address or FQDN> --username <username> --password <pwd> remotedocker
```
The above command creates a `mygpuvm.compute` and `mygpuvm.runconfig` files under the `aml_config` folder.

### Step 3. Modify the configuration files under _aml_config_ folder
- You need the CNTK library built for GPU:
    
    In `conda_dependencies.yml` file, replace the CNTK library URL with the GPU version:

     - `https://cntk.ai/PythonWheel/GPU/cntk-2.2-cp35-cp35m-linux_x86_64.whl`

    Or you can use the 1-bit SGD version:

    - `https://cntk.ai/PythonWheel/GPU-1bit-SGD/cntk-2.2-cp35-cp35m-linux_x86_64.whl`

    You can find the latest CNTK Python library for Linux at the [CNTK documentation site](https://docs.microsoft.com/en-us/cognitive-toolkit/Setup-Linux-Python?tabs=cntkpy22).

- You need a different base Docker image with CUDA libraries preinstalled:

    In `mygpuvm.compute` file, replace the value of `baseImage` from `microsoft/mmlspark:plus-0.7.91` to  `microsoft/mmlspark:plus-gpu-0.7.91`

- You need to use _nvidiaDocker_ command to start the Docker container as opposed to the regular _docker_ command.

    In `mygpuvm.compute` file, add a line: `nvidiaDocker: true`

- Optionally, you can to specify the run time framework as _Python_ as opposed to _PySpark_ to gain a little more efficiency:

    In `mygpuvm.runconfig` file,  change the value of `Framework` from `PySpark` to `Python`.

### Step 4. Run the script.
```shell
# prepare your Docker image on the GPU VM.
$ az ml experiment prepare -c mygpuvm

# run the MNIST classification script
$ az ml experiment submit -c mygpuvm cntk_mnist.py
```
