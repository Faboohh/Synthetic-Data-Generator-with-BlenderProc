# BlenderProc
## Synthetic Data Generation for Computer Vision
**Comprehensive Tutorial**  
*Date: 2025-08-18*
[![BlenderProc Version](https://img.shields.io/badge/BlenderProc-2.8.0-blue)](https://github.com/DLR-RM/BlenderProc)
[![Blender Version](https://img.shields.io/badge/Blender-4.2.1-lightblue)](https://www.blender.org/download/)
[![Platform](https://img.shields.io/badge/Platform-Linux-lightgrey)]()

---

## Table of Contents
1. [Introduction](#introduction)
    - [Pros](#pros)
    - [Cons](#cons)
2. [Installation and Setup](#installation-and-setup)
    - [Environment Setup](#environment-setup)
    - [BlenderProc Installation](#blenderproc-installation)
        - [Method 1: pip Installation](#method-1-pip-installation)
        - [Method 2: Git Installation](#method-2-git-installation)
    - [Quick Start](#quick-start)
    - [Viewing Results](#viewing-results)
3. [Dataset Downloads](#dataset-downloads)
    - [CC Textures Dataset](#cc-textures-dataset)
    - [Available Datasets](#available-datasets)
4. [Basic BlenderProc Script Structure](#basic-blenderproc-script-structure)
    - [Essential Components](#essential-components)
    - [Complete Basic Script](#complete-basic-script)
5. [Script Components Explained](#script-components-explained)
    - [Scene Setup](#scene-setup)
    - [Noise Addition](#noise-addition)
    - [Lighting](#lighting)
    - [Camera Alignment](#camera-alignment)
    - [Output Rendering](#output-rendering)

---

## Introduction

BlenderProc is a synthetic data generator, it helps the process of training a neural network by reducing the amount of manual data collection required. This tool allows for easy modifications of data such as noise creation (new objects and different backgrounds).

### Pros
- Reduces manual data collection requirements
- Enables easy data variation and modification
- Accelerates neural network training processes
- Provides controlled testing environments

### Cons
- Performance degradation due to sim2real gap
- Does not replicate the real world, might be faulty
- Requires time and attention, steep learning curve

---

## Installation and Setup

### Environment Setup
To avoid conflicts and damage, create a dedicated conda environment:

Click here to follow the official Anaconda installation [guide](https://www.anaconda.com/download)

```bash
# Create new environment with Python 3.10
$ conda create --name blenderproc python=3.10

# Activate the environment
$ conda activate blenderproc

# To exit the environment (when needed)
$ conda deactivate

# Go inside your blenderproc folder inside the environment
cd your/path/to/env

# BlenderProc Installation and Basic Usage

## Installation

### Method 1: pip
```bash
pip install blenderproc
```

### Method 2: Git
```bash
git clone https://github.com/DLR-RM/BlenderProc
cd BlenderProc
pip install -e .
```

### Quick Start
```bash
blenderproc quickstart
```

### Viewing Results
```bash
blenderproc vis hdf5 output/0.hdf5
```

---

## Dataset Downloads

- **CC Textures**: https://cc0textures.com/
- **BlenderKit**: Materials and models
- **Haven**: Textures and models from polyhaven.com
- **Pix3D**: IKEA dataset
- **SceneNet**: Scene datasets
- **Matterport**: 3D environment scans

---

## Basic BlenderProc Script

```python
import blenderproc as bproc
import numpy as np

# Initialize BlenderProc
bproc.init()

# Load an object
objs = bproc.loader.load_obj("path/to/model.obj")

# Randomize object pose
for obj in objs:
    obj.set_location(np.random.uniform(-1, 1, size=3))
    obj.set_rotation_euler(np.random.uniform(0, np.pi*2, size=3))

# Add lighting
light = bproc.types.Light()
light.set_location([2, -2, 2])
light.set_energy(np.random.uniform(100, 500))

# Define camera poses
cam_pose = bproc.math.build_transformation_mat(
    [0, -3, 1], [np.random.uniform(0.1, 0.5), 0, 0]
)
bproc.camera.add_camera_pose(cam_pose)

# Render output and write COCO annotations
data = bproc.renderer.render()
bproc.writer.write_coco_annotations("output/", data)
```
# Debugging

BlenderProc provides an excellent debugging feature to check the "Behind the scenes":

```bash
$ blenderproc debug yourfile.py
```

This allows real-time visualization of script execution and scene construction.

# How to create distractions for object detection

## Prerequisites
Download the code from the GitHub repository with this command:

```bash
$ git clone https://github.com/Faboohh/Synthetic-Data-Generator-with-BlenderProc.git
```
and leave it there for the moment, we are going to use it later on.

Prepare the following datasets:

## CC Textures Dataset

```bash
$ blenderproc download cc_textures path/to/folder/where/to/save/materials
```

**Warning:** This is a large dataset (~1900 folders) that may take 45+ minutes to download.

## IPD Dataset Setup

We are going to need an even larger dataset, which is the [IPD dataset](https://huggingface.co/datasets/bop-benchmark/ipd/tree/main). This will take a couple of hours to download, depending on the internet connection and speed. 

```bash
# Create dataset folder
$ mkdir bpd_datasets && cd bpd_datasets

# Create IPD folder
$ mkdir ipd && cd ipd

# Set environment variable in the CLI (if you restart the CLI without having downloaded the files redo this command)
$ export SRC=https:https://huggingface.co/datasets/bop-benchmark/ipd/tree/main

# Download required files
$ wget $SRC/ipd_base.zip
$ wget $SRC/ipd_models.zip
```

## File Organization

After downloading and extracting the ZIP files:

1. Extract both ZIP files  
2. Move folders from `ipd_models.zip` into the main `ipd` folder  
3. Take the ObjectDetection Script from the repository you cloned
4. Place it in `examples/dataset/bop_object_physics_positioning/`

## Running distraction generator script

```bash
$ blenderproc run examples/datasets/bop_object_physics_positioning/main_v2.py \
  /data/bpc_datasets ipd resources/cctextures output_main_v2
```

**Important:** Ensure all file paths are correct. The IPD parameter should target the folder; objects will be selected randomly.

After running the command, two images with different outputs will be generated. Inside them there will be images containing a background from CC Textures and random objects from the IPD dataset.
Each image will have it's own camera position, the camera position is customizable, by modifying the camera position file. 


# Parameters

In this section, some interesting parameters will be explained. Some of these are use inside the SceneCreation script.

Inside this GitHub repository there is a folder with all the necessary data.

Step 1 clone the repository, if you didnt do it before.

```bash
$ git clone https://github.com/Faboohh/Synthetic-Data-Generator-with-BlenderProc.git
```

Step 2 move the sceneCreation script inside your main blenderProc folder

to run this code you will need:
1. An Object(Blenderproc supports .obj files)
2. A camera position file with the camera poses(explained later in this guide)
3. ccTexture downloaded in your environment
4. an output dir for the final output


```bash
blenderproc run examples/datasets/bop_object_physics_positioning/blenderProcMain.py --camera examples/resources/camera_positionsCustom.txt --obj resources/personalObjects/home.obj --second_obj resources/personalObjects/table.obj  --texture_dir resources/cctextures/  --output_dir output_main_v2/
```



If we follow the official BlenderProc website, we can notice some interesting functionalities, such as adding a plane onto our scene.

### Camera Position
The camera Position can be passed as an argument, as did in the second script, and its fully customizable. 
Inside a file you will put 6 coordinates in total
X, Y, Z axis
X, Y, Z rotation in radiants so make sure to convert them.

each line is a different camera pose and 2 different images will be outputed.

Inside the Script/sceneCreation folder there is an example camera pose file, try to use that


**Warning: when adding a custom camera pose make sure there are no blank lines otherwise the program will fail**

### How to add primitive Objects

One of blenderproc's built-in function is the create_primitive(), it takes 2 parameters the first one is the primitive we are adding,
the second one is the size of that object. Then with the set_location function we set the location of that plane.

This is the list of all the available primitives
[“CUBE”, “CYLINDER”, “CONE”, “PLANE”, “SPHERE”, “MONKEY”]


Lets add a Plane to our scene for example and set the origin as it's location

```python
# Create floor
floor = bproc.object.create_primitive("PLANE", scale=[5, 5, 1])
floor.set_location([0, 0, 0])
```

As we can see we define the primitive as a Plane with the realitve sizes and then set the location as the origin (X, Y, Z).
# Troubleshooting

## Git Installation Error

If you encounter the error:

> The git executable must be specified in one of the following ways...

This indicates that Git is not installed or is not accessible globally. Install Git using:

```bash
$ sudo apt install git
```

## Common Issues and Solutions

- **Path Issues:** Always verify that file paths are correct and accessible  
- **Environment Conflicts:** Use the dedicated conda environment  
- **Memory Issues:** Large datasets may require significant RAM and storage  
- **Network Timeouts:** Dataset downloads may fail due to network issues; retry if necessary  

# Conclusion

BlenderProc provides a powerful framework for generating synthetic training data for computer vision applications. While the Sim2Real gap presents challenges, the tool's flexibility and extensive dataset support make it valuable for accelerating machine learning model development.

