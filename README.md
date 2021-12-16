# OpenCV Hand Gesture Detection and Control
Made by david-0609, for the FSFE YH4F Coding Competition 2021

## Dependencies
- Python 3.7, other versions of Python may not have the libraries
- Tensorflow, OpenCV, mediapipe (see requirements.txt)

## Installation and Running
	pip install -r requirements.txt
	python main.py

## Generalised Approach
<s> 1. The model will draw a covex hull around the hand after separating the hand from the background, using the convex hull, find fingertips and track for gestures</s>
### 2. Use preexisting mediapipe model to track hand (more feasible) and use in GUI/TUI application.
Algorithm to use: https://google.github.io/mediapipe/solutions/hands.html

The mediapipe module will grab the coordinates of the points on the hand, and these points will be used to determine if a finger is being held up or not. Motion tracking will be done with numpy and matplotlib by logging the coordinate changes of the fingertips inside a detection window that is triggered by counting the number of fingers up.
OOP will be used for extensiblity and ease of access with a front end TUI/GUI application.  

