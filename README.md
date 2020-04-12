# AIMLAV devkit
This project is based on many other subprojects and uses a project shell/structure based off the [nuScenes](https://github.com/nutonomy/nuscenes-devkit) project.

## Overview
- [Changelog](#changelog)
- [Project Description](#project-description)
- [Project Setup From Scratch](#project-setup-from_scratch)
- [Cloning The Project](#cloning-the_project)
- [Running Project From Pre-configured VM](#running-project-from-pre-configured-vm)
- [Getting Started](#getting-started)
- [Download dataset](#dataset-download)


## Changelog
- April. 11, 2018: Devkit initial setup.


## Project Description
- This project was actually to use the nuscenes dataset to train an object recognition model on point clouds and experiment with how adversarial attacks on point clouds can affect the quality of autonomous vehicles if not handled accordingly.

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

- When you configure this project I advise that you set it up on an Ubuntu 16.04 / 18.04 machine as I have tested the project on this platform. I have also tried to configure this project on a Jetson Xavier with Ubuntu 18.04 device however it was a hassle to get some of the packages to work, and some packages just never got to work at all namely tensorflow which is a requirement for Pointnet subproject. The Jetson Javier has been known to have a different CPU architecture and therefore works differently in many ways. 


## Project Setup from Scratch


Project Directory structure

python-sdk/
	/aml
		/Adversarial-point-pertubations-on-3D-objects
		/pointnet
	/data
		/sets/nuscenes
	/second.pytorch
	/nuscenes

The data/ directory houses everything to do with the dataset for the project, however take note some of the subprojects here might have thier own datasets.


### Nuscenes-devkit setup

Nuscenes works with python 3.7 and 3.6, but I advise you use 3.7 since I have experience in using this version as well.
Create project environment

`$ conda create -n nuscenes python=3.7`

`$ pip install -r python-sdk/requirements.txt`

To setup nuscenes refer to the well documented [nuscenes-devkit github repository](https://github.com/nutonomy/nuscenes-devkit)


### SECOND setup

Make use of the already existing environment nuscenes (we created this above) 

$ conda activate nuscenes

- Install dependencies

$ conda install scikit-image scipy numba pillow matplotlib

- Install required packages from the requirements.txt file:

`$ pip install -r requirements`

- Clone and install the spconv repository (https://github.com/traveller59/spconv)

`$ git clone https://github.com/traveller59/spconv.git --recursive`
`$ sudo apt-get install libboost-all-dev`

- Download and install cmake click [HERE](https://drive.google.com/open?id=1aYg3TvMIkIZsvbXWUkqAqc0hjOvS-PXfNaX0W__Ffsg) for steps on how to do this

Create a <something>.whl file to install this package

`$ python setup.py bdist_wheel`

Install the generated <something>.whl file

`$ cd ./dist`
`$ pip install <something>.whl`

### Adversarial point perturbations on 3D objects setup

- When running scripts or notebooks that execute code from this project please use python 2.7, there you should create a new python2.7 environment for this project and install it’s packages from the requirements.txt file.

`$ conda create -n app3d python=2.7`
`$ conda activate app3d`
`$ pip install -r requirements.txt`


### Pointnet setup

- Create a separate environment for this project it makes use of python 2.7

`$ conda create -n pnet python=2.7`

`$ conda activate pnet`

`$ pip install requirements.txt`

`$ sudo apt-get install libhdf5-dev`

Follow the the elegant usage instructions from the [github pointnet repository](https://github.com/TangeniThePyGuru/pointnet)


## Cloning the project

- Clone the project make sure to add the --recursive flag to include all the required subprojects

`$ git clone https://github.com/samtout/AIMLAV.git --recursive`

- Install Anaconda

`$ mkdir ~/temp && cd ~/temp`

`$ wget https://repo.anaconda.com/archive/Anaconda3-2020.02-Linux-x86_64.sh`

`$ ./Anaconda3-2020.02-Linux-x86_64.sh`

- Create virtual environment

`$ conda create -n p37 python=3.7`

- Activate Environment
`$ conda activate p37`

- Install requirements
`$ pip install -r requirements.txt`

## Running Project From Pre-configured VM 

***(For security purposes this instructions never go public when this repo goes public)***

***Assuming that you have VPN access to the subnet where the VM is located***

1. Start the Jupyter Server if it has not started already (**take note of any open terminals with services running**)

Open the actual Ubuntu VM make sure that you start the Jupyter server in the right directory using the command below:

`$ cd /media/research/AV_DATA/Nuscenes/nuscenes-devkit/python-sdk`

***This is were all the project development is taking place most of the time***

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


## Dataset download
To download nuScenes you need to go to the [Download page](https://www.nuscenes.org/download), 
create an account and agree to the nuScenes [Terms of Use](https://www.nuscenes.org/terms-of-use).
After logging in you will see multiple archives. 
For the devkit to work you will need to download *all* archives.
Please unpack the archives to the `data/sets/nuscenes` folder \*without\* overwriting folders that occur in multiple archives.
Eventually you should have the following folder structure:
```
/data/sets/nuscenes
    gt_database
    samples	-	Sensor data for keyframes.
    sweeps	-	Sensor data for intermediate frames.
    maps	-	Folder for all map files: rasterized .png images and vectorized .json files.
    v1.0-*	-	JSON tables that include all the meta data and annotations. Each split (trainval, test, mini) is provided in a separate folder.
```
If you want to use another folder, specify the `dataroot` parameter of the NuScenes class (see tutorial).

## TODO


