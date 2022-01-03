# OpenCV Hand Gesture Detection and Control
Made by david-0609, for the FSFE YH4F Coding Competition 2021

## Dependencies
- Python 3.7, other versions of Python may not be compatible with the libraries
- Numpy, OpenCV, mediapipe etc (see requirements.txt)

## Installation
	pip install -r requirements.txt

## Generalised Approach
<s> 1. The model will draw a covex hull around the hand after separating the hand from the background, using the convex hull, find fingertips and track for gestures</s>
### 2. Use preexisting mediapipe model to track hand (more feasible) and use in GUI/TUI application.
Algorithm to use: https://google.github.io/mediapipe/solutions/hands.html

The mediapipe module will grab the coordinates of the points on the hand, and these points will be used to determine if a finger is being held up or not. Motion tracking will be done with numpy and matplotlib by logging the coordinate changes of the fingertips inside a detection window that is triggered by counting the number of fingers up.
OOP will be used for extensiblity and ease of access with a front end TUI/GUI application.  

A detection window will be started as soon as all 5 fingers are found on screen, the default value is 5 seconds. Frames in the future 5 seconds will be monitored and after the finger is out of the camera or the window is over, an action will be performed through keyboard shortcut based on the results of monitoring. The x and y coordinates will be monitored and determined similiarly to the finger_up function.

## Screenshots

## Usage Examples

### Acknowledgements

Many Thanks to:
- My parents, who supported me throughout this project
- [brokenbyte](https://gitlab.com/brokenbyte/), who gave me lots of tips on development
- Tristan, who helped me develop my idea
- My friends, who gave me ideas for extra features
- Of course, there is always StackOverflow
