# AIMLAV devkit
This project is based on many other subprojects and uses a project shell/structure based off the [nuScenes](https://github.com/nutonomy/nuscenes-devkit) project.

## Overview
- [Changelog](#changelog)
- [Project Description](#project-description)
- [Project Configuration](#project-configuration)
- [Running Project From Pre-configured VM](#running-project-from-pre-configured-vm)
- [Getting Started](#getting-started)


## Changelog
- April. 11, 2018: Devkit initial setup.


## Project Description
- This project was actually to use the nuscenes dataset to train an ***object recognition model on point clouds*** and experiment with how adversarial attacks on point clouds can affect the quality of autonomous vehicles if not handled accordingly.

- This project consists of 4 subprojects:

> Nuscenes Devkit 
    - The nuscenes dev kit provides us with an autonomous dataset that contains images and point clouds of scenes captured that we can use to train object recognition models 
    - Read more [HERE](https://github.com/nutonomy/nuscenes-devkit) 

> SECOND 
    - SECOND provides us with a preconfigured platform to allow us to train object detection models by using the the nuscenes dataset 
    - Read more [HERE](https://github.com/traveller59/second.pytorch)

> Adversarial point perturbations on 3D objects 
    - This repository provides functionalities to run untargeted adversarial attacks on objects for running untargeted adversarial attacks on 3D point cloud objects
    - Read more [HERE](https://github.com/Daniel-Liu-c0deb0t/Adversarial-point-perturbations-on-3D-objects)

> Pointnet 
    - Pointnet is an algorithm for deep learning specifically on Point Sets for 3D Classification and Segmentation
    - Read more [HERE](https://github.com/charlesq34/pointnet)

> *When you configure this project I advise that you set it up on an **Ubuntu 16.04 / 18.04 machine** as I have tested the project on this platform. I have also tried to configure this project on a **Jetson Xavier** with Ubuntu 18.04 device however it was a hassle to get some of the packages to work, and some packages just never got to work at all namely tensorflow which is a requirement for the Pointnet subproject. The Jetson Javier has been known to have a different CPU architecture and therefore works differently in many ways.*


## Project Setup from Scratch


Project Directory structure
```
nuscenes-devkit/python-sdk/
	/aml
		/Adversarial-point-pertubations-on-3D-objects
		/pointnet
	/data
		/sets/nuscenes
	/second.pytorch
	/nuscenes
```

The **data/** directory contains everything to do with the dataset for the project, however take note some of the subprojects here might have thier own datasets.

- Clone the project make sure to add the --recursive flag to include all the required subprojects

`$ mkdir /media/$USER/AV_DATA && cd /media/$USER/AV_DATA && git clone https://github.com/samtout/AIMLAV.git --recursive`

- cd into the ***python-sdk*** directory

`$ cd AIMLAV/python-sdk`

### Nuscenes-devkit setup

Nuscenes works with python 3.7 and 3.6, but I advise you use 3.7 since I have experienced using this version as well.
Create project environment

#### Install Anaconda

`$ mkdir ~/temp && cd ~/temp`

- If you did not install Anaconda already go ahead and install it, else [continue here](#create-virtual-environment).

`$ mkdir ~/temp && cd ~/temp`

- The two commands below do the same thing which is to download Anaconda, you can use whichever works for you.

`$ wget https://repo.anaconda.com/archive/Anaconda3-2020.02-Linux-x86_64.sh`

`$ curl -O https://repo.anaconda.com/archive/Anaconda3-2020.02-Linux-x86_64.sh`

- Give the current user execution permissions to the executable file

`$ chmod u+x Anaconda3-2020.02-Linux-x86_64.sh`

- Execute downloaded Anaconda script (follow instructions), when prompted **Do you wish the installer to initialize Anaconda3?** say yes.

`$ ./Anaconda3-2020.02-Linux-x86_64.sh`

- Close your current terminal and reopen again, if anaconda has no been added to *path* please add it by adding the following line to you **~/.bashrc** file.

`export PATH=~/anaconda3/bin:$PATH`

- Persist the changes you made to the **~/.bashrc** file

`$ source ~/.bashrc`

##### Create virtual environment

`$ conda create -n nuscenes python=3.7`

- Activate Environment

`$ conda activate nuscnes`

- Install requirements

`$ pip install -r requirements.txt`

- if you have issues installing opencv with the script above you can remove it from the requirements.txt file and install it via the conda package manager.

`$ conda install opencv-python`

#### Install project dependencies

- Paste the following two scripts to the ***~/.bashrc*** file 

```
export NUSCENES="data/sets/nuscenes"
export PYTHONPATH="${PYTHONPATH}:/media/$USER/AV_DATA/AIMLAV/nuscenes-devkit/python-sdk"
```
> The first line creates a ***nucenes environement variable*** which us used to access the dataset.
> The second line allows you to access python packages withing the ***python-sdk/*** directory, please take note of the path. This is where my project has been installed under the ***/media/$USER*** directory, so you should take note of where you install you project and change this accordingly.

- Open the file with nano and paste the code above

`$ sudo nano ~/.bashrc`

#### Download dataset

To download nuScenes you need to go to the [Download page](https://www.nuscenes.org/download), 
create an account and agree to the nuScenes [Terms of Use](https://www.nuscenes.org/terms-of-use).
After logging in you will see multiple archives. 
For the devkit to work you will need to download *all* archives. but for this project you can download the **mini dataset** to work with
Please unpack/unzip the archives to the `data/sets/nuscenes` folder \*without\* overwriting folders that occur in multiple archives.
Eventually you should have the following folder structure:

```
data/sets/nuscenes
    gt_database	-	ground_truth data (raw data for annotations)
    samples	-	Sensor data for keyframes.
    sweeps	-	Sensor data for intermediate frames.
    maps	-	Folder for all map files: rasterized .png images and vectorized .json files.
    v1.0-*	-	JSON tables that include all the meta data and annotations. Each split (trainval, test, mini) is provided in a separate folder.
```
If you want to use another folder, specify the `dataroot` parameter of the NuScenes class (see tutorial).


#### Test Nuscenes Project

- Run test under the ***python-sdk/*** directory to confirm that there is not missing information.

`$ python -m unittest`

### SECOND setup

**Make use of the already existing environment *nuscenes* (we created this above)**

- Activates a conda environment named *nuscenes*

`$ conda activate nuscenes`

- Install dependencies into this environment

`$ conda install scikit-image scipy numba pillow matplotlib`

- Install required packages from the second.pytorch/requirements.txt file:

`$ pip install -r second.pytorch/requirements.txt`

- Install CUDA from [HERE](https://docs.google.com/document/d/1s8pM0cNSrmc2Lvdy2eSEtBP2czZjJxrKkPF8773z_Xo/edit?usp=sharing)

**You need to add following environment variable for numba.cuda to *~/.bashrc***

```
export NUMBA_CUDA_DRIVER=/usr/lib/x86_64-linux-gnu/libcuda.so
export NUMBA_NVVM=/usr/local/cuda/nvvm/lib64/libnvvm.so
export NUMBA_LIBDEVICE=/usr/local/cuda/nvvm/libdevice
```

`$ sudo apt-get install libboost-all-dev`

- Download and install cmake click [HERE](https://drive.google.com/open?id=1aYg3TvMIkIZsvbXWUkqAqc0hjOvS-PXfNaX0W__Ffsg) for steps on how to do this.

- Clone and install the [spconv](https://github.com/traveller59/spconv) dependency 

`$ mkdir ~/temp && cd ~/temp`

`$ git clone https://github.com/traveller59/spconv.git --recursive`

- Create a <something>.whl file to install this package

`$ python setup.py bdist_wheel`

- Install the generated <something>.whl file

`$ cd ./dist`

`$ pip install <something>.whl`

- Add the following script to the bottom of ***~/.bashrc*** file, it allows SECOND to reference our ***nuscenes dataset***.
***Take note of the path below, make sure to use your own full path where you have installed the project, mine is under /media/$USER/***

`export NUSCENES_TRAINVAL_DATASET_ROOT="/media/$USER/AV_DATA/AIMLAV/nuscenes-devkit/python-sdk/data/sets/nuscenes"`

`$ sudo nano ~/.bashrc`


### Adversarial point perturbations on 3D objects setup

***When running scripts or notebooks that execute code from this project please use python 2.7, there you should create a new python2.7 environment for this project and install it’s packages from the requirements.txt file.***

- Create a new python2.7 environment for this subproject and install dependencies

`$ conda create -n app3d python=2.7`

`$ conda activate app3d`

`$ pip install -r aml/Adversarial-point-perturbations-on-3D-objects/requirements.txt`


### Pointnet setup

- Create a separate environment for this project, it makes use of python 2.7 and install dependencies. This project has different versions of the same dependencies in other virtual environments that's we need to create a new environment for it. 

`$ conda create -n pnet python=2.7`

`$ conda activate pnet`

- Install required dependencies

`$ pip install aml/pointnet/requirements.txt`

`$ sudo apt-get install libhdf5-dev`

You can follow the the elegant usage instructions from the [github pointnet repository](https://github.com/TangeniThePyGuru/pointnet)

***After setting up the project, you should skip the next section and head over to the [Getting Started](getting-started) section***

## Running Project From Pre-configured VM 

***THIS SECTION IS INDEPENDENT OF THE PREVIOUS SECTIONS***

***(For security purposes this instructions never go public when this repo goes public)***

***Assuming that you have VPN access to the subnet where the VM is located***

1. Start the Jupyter Server if it has not started already (**take note of any open terminals with services running**)

Open the actual Ubuntu VM make sure that you start the Jupyter server in the right directory using the command below:

`$ cd /media/research/AV_DATA/Nuscenes/nuscenes-devkit/python-sdk`

***This is were all the project development is taking place***

`$ conda activate`

- Start the Jupyter Server

`$ jupyter notebook --no-browser`

** *‘--no-browser’ flag simply means we don’t want a browser page to open up after starting the server* **

2. SSH tunnel into the Jupyter Server from your Computer

- You need to connect to a jupyter server running on the VM via SSH tunnelling, open up a terminal on your local machine and run the following command (take note the IP address below can change, let's assume it has not changed for now).

`$ ssh -N -f -L 8889:localhost:8888 research@10.5.128.17`

- As for MAC OSX, use the following command to SSH tunnel to prevent the common error “broken pipe”, the article [here](http://www.yellow-bricks.com/2018/11/26/ssh-broken-pipe-osx/) explains it very well if you’d like to read more about it.
 
`$ ssh -o -IPQoS=throughput -N -f -L 8889:localhost:8888 research@10.5.128.17`

- After the command above you should be able to connect to a *Jupyter Server/Environment* from your browser by simply typing the following link:

*http://localhost:8889*

- When prompted for a password use the password below:

*Way$ToGo2022*
	
**Take note you do not need to make any configurations unless introducing something new**

- The Jupyter Environment gives you the ability to open instances to your local terminal from the browser in case you need to execute any script from a terminal. 

- Otherwise if you are not comfortable with the Jupyter Environment you can always log into the actual machine by connecting to the VM directly via VMWare Workstation. Click [HERE](https://docs.google.com/document/d/13-j_JXBM0jagUzOZhlwAgfshlbX8O65PXvIZHe99ohQ/edit?usp=sharing) for steps on how to do the above.

## Getting started


### Nuscenes Data Analysis
- Carried out data analysis on the nuscenes dataset using the nuscenes devkit, you will find the notebook I had used for this experiment in the this notebook Replica_v1.5.ipynb


### Trained a car object recognition model using the Nuscenes Dataset 
- Using the SECOND devkit I trained an object recognition model using the Nuscenes dataset 

- The scripts to this experiments are found and can be executed in this directory second.pytorch/second

`$ python ./pytorch/train.py train --config_path=./configs/nuscenes/pedestrian-test.fhd.config --model_dir=model_pedestrian --measure_time=True`

- This command takes the parameters model configuration file as config_path and an output directory as model_dir. These configuration files can be found in the second.pytorch/second/configs. 

- You can create/customise your own config files and link them to the scripts/command above.

### Performed inferences on this car object recognition model
- Using the model trained above I then I run inferences on this models, experiments on this can be found in this notebook *second.pytorch/second/inference_v1.0.ipynb*
  
Trained a pointnet object recognition model using the pointnet subproject located *aml/pointnet*, I trained a point cloud object prediction model 
Pointnet used a modelnet40 dataset located in the *aml/pointnet/data* directory to train the object recognition model we have.

### Adversarial Attacks
- Ran adversarial attacks on modelnet40 point cloud dataset using the [**Adversarial-point-perturbations-on-3D-objects**](https://github.com/TangeniThePyGuru/Adversarial-point-perturbations-on-3D-objects) subproject. This project provides us with scripts to run adversarial attacks on point cloud objects, it is located here *aml/Adversarial-point-perturbations-on-3D-objects*, the scripts are located in the *src/* directory

- The *src/* folder contains all the scripts that we need to run adversarial attacks and visualise the results of these attacks.  
	
	- This folder also provides us with scripts to visualize perturbed objects but I     
           gave created a notebook *AML_notebook.ipynb* to help us visualise these
           perturbed  objects. See examples in the notebook.


## TODO


