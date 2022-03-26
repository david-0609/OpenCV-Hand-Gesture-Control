# OpenCV Hand Gesture Detection and Control

Made by david-0609, for the FSFE YH4F Coding Competition 2021

## Note:
#### *YH4F Judges: Please see branch YH4F_Submit for the final submission of this project.*

[![Stand With Ukraine](https://raw.githubusercontent.com/vshymanskyy/StandWithUkraine/main/banner2-direct.svg)](https://vshymanskyy.github.io/StandWithUkraine)

## Description

This program reads in coordinates of finger landmarks (see landmarks.png) and uses the data to find fingters that are up and by tracking the movements of the fingertips, detects a gesture and executes a keyboard shortcut linked to it. A premade module for hand detection is used and OpenCV is used to record dta from the webcam. The program is designed modularly and uses a facade design pattern, with the module Run being the facade object. The library being used to execure keystrokes is pyautogui, which can only be used under a GUI environment. Configparser is used to read in the config file, see https://docs.python.org/3/library/configparser.html for detailed explanation of the format. The algorithm used to detect the direcion of travel of the finger is quite simple and can be improved to use a more sophisticated method for a better result, for the purpose of this project, the accuracy is sufficient. 

## Dependencies

- Python 3.7, other versions of Python may not be compatible with the libraries
- X11 GUI (Needed for pynput module) 
- Numpy, OpenCV, mediapipe etc (see requirements.txt)

## Installation

    pip install -r requirements.txt

It is recommended to create a virtual environment to install the python packages. 

## Generalised Approach

<s> 1. The model will draw a covex hull around the hand after separating the hand from the background, using the convex hull, find fingertips and track for gestures (See experiement1.py) </s> As this approach gave highly inconsistant results, this method is scrapped. 

### 2. Use preexisting mediapipe model to track hand (more feasible) and use in GUI/TUI application.

Algorithm to use: https://google.github.io/mediapipe/solutions/hands.html

The mediapipe module will grab the coordinates of the points on the hand, and these points will be used to determine if a finger is being held up or not. Motion tracking will be done with numpy and matplotlib by logging the coordinate changes of the fingertips inside a detection window that is triggered by counting the number of fingers up.
OOP will be used for extendiblity in the future and ease of access with a front end TUI/GUI application.  

A detection window will be started as soon as all 5 fingers are found on screen, the default value is 5 seconds. Frames in the future 5 seconds will be monitored and after the finger is out of the camera or the window is over, an action will be performed through keyboard shortcut based on the results of monitoring. The x and y coordinates will be monitored and determined similiarly to the finger_up function.

## Screenshots

## Usage Example

Running without specifying config file (defaults to `config` in home directory)

`python run.py --debug --camera-dir="/dev/video0"`

Running with specific config file

`python run.py --debug --camera-dir="/dev/video0" --config-path="/path/to/config"`

### Acknowledgements

Many Thanks to:

- My parents, who supported me throughout this project
- [brokenbyte](https://gitlab.com/brokenbyte/), who gave me lots of tips on development
- Tristan, who helped me develop my idea
- My friends, who gave me ideas for extra features
- Of course, there is always StackOverflow
