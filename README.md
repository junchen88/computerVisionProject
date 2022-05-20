https://github.com/junchen88/computerVisionProject
# Installations needed:

Python version: 3.8.10 (tested)

**Python packages**:

- from PyQt5 import QtCore, QtGui, QtWidgets

- import numpy as np

- from scipy.stats import norm

- import scipy.ndimage

- import skimage

- from scipy.optimize import linear_sum_assignment

**packages**: numpy, scipy, skimage, PyQt5


## Steps to run
1. install python and its packages (using pip to install the packages)
2. download mot folder (containing the images) into the project folder
3. run main.py using python in the same folder with mot
4. assign value to STDs using slider or enter value into box (choose the best one by trying different values)
5. enter image name - the folder number eg. 001, 002, …. 020…
6. enter object type - the object that is going to be tracked, eg car
7. enter frame range – the frame range needed, can leave empty if user want all frames for that image name
8. click start to track
9. if file is not found, program will quit and error message is displayed on terminal
10. status is shown on terminal when the program is running
11. click the red cross on gui to close the program
