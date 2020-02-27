# Build a Docker image with custom Python package pre-installed

This project demonstrates how to build your python application as a Docker image.

## Directory Structure
```
├── my_package/       <- Package directory for storing your python code
        ├── __init__.py
        └── e.g. main.py
├── requirements.txt  <- Use by pip to install the libraries required for running your Python code
├── setup.py          <- Use by Python setup tools to build the python distribution
├── Dockerfile        <- Dockerfile for buildling the Docker image
└── build.sh          <- Bash script to build your python app and the Docker image
```

#### 1. Put your python code into a package directory
The *my_package* directory contains the python modules you created.  
This directory must have a file named __init__.py to be recognised as a python package directory.

#### 2. Include required packages or minimum version required of packages in requirements.txt file
More information about the requirements can be found here - https://pip.pypa.io/en/stable/user_guide/#id12
The Python libraries listed in this file will be installed during the Docker build process.

#### 3. Fill in package information in setup.py
This is the build script for the Python build tool - setuptools.  
Update this file with the correction information about your package such as package name and author name.  
Refer to https://packaging.python.org/tutorials/packaging-projects/ for more information.

#### 4. Run build.sh to build the Python package and the Docker image
Run the build script to perform the following steps:
1. Build the Python package using setuptools
2. Build a Docker image based on the provided Dockerfile
3. Test the Docker container
