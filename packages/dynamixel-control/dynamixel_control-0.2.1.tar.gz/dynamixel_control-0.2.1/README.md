# Dynamixel Control

## Use
Use this library to communicate with Dynamixel motors. Currently, this is set up for position control and feedback for Dynamixel XL-320 and XL-330 motors, although more can be added with ease.

## Instalation and Dependencies
Clone this package into your project or add as a submodule:
```bash
git clone https://github.com/OSUrobotics/dynamixel_control.git
or
git submodule add https://github.com/OSUrobotics/dynamixel_control.git
```

This library requires the following dependencies:
- Numpy
```bash
python3 -m pip install numpy
```
- Dynamixel-SDK
```bash
python3 -m pip install dynamixel-sdk
```

There are two modules - [dynamixel.py](dynamixel.py) and [dxl.py](dxl.py). [dynamixel.py](dynamixel.py) contains all of the functions needed to control and read dynamixels. Examples are provided at the bottom of the file. For every Dynamixel motor attached, [dynamixel.py](dynamixel.py) creates a Dxl object from [dxl.py](dxl.py). That object contains all the neccessary parameters and stores the Dynamixel's cablibration, current position, etc.


From directory, build package:
python3 -m build
Upload Package:
python3 -m twine upload dist/*
