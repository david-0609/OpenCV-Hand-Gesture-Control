# OpenCV Hand Gesture Detection and Control
Made by david-0609, for the FSFE YH4F Coding Competition 2021

## Dependencies
- Python 3.7
- Tensorflow, OpenCV, mediapipe


## Generalised Approach
### 1. The model will draw a covex hull around the hand after separating the hand from the background, using the convex hull, find fingertips and track for gestures.
### 2. Use preexisting mediapipe model to track hand (more feasible) and use in GUI/TUI application.
https://google.github.io/mediapipe/solutions/hands.html
