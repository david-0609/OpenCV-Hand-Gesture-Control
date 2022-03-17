# Documentation & Explanations

## How I got the idea

The idea came to me from reading a ebook on my laptop, the pages were short and therefore I had to always press the next or page down button on my keyboard whenever I turn a page. This really disrupted my flow of reading, so I thought, a hand gesture would be a good way to do this in an elegant way that simulate the actual action when reading a paper book. Then, I decided to expand on this for this to have more functions, such as a swipe down gesture opening a drop down terminal and etc. 

## Design of the Program

The design pattern used for this project is Facade. I used this to abstract the interface of this program to a single object, which is `Run()` from `run.py`. As the only thing the user should do to interact with the program is to open the webcam, a facade stashes away the algorithm and makes the code simpler.The program is spilt modularly and the modules import certain data from `run.py`. Some functions dealing with basic operations such as sorting a list in a certain way, checking elements etc are put into `Tools.py` and imported when needed



## Key Libraries Used

- mediapipe 
  
  -    Licenced under Apache 2.0, provides live ML analysis of video imput

- OpenCV
  
  - Licenced under Apache 2.0, captures webcam input

- Multiprocessing
  
  - Built in Python package, allows the creation of seperate processes, in this case, one process runs in the background for hand detection, and another runs to control the process
  
- pickle

  - Built in Python library, used for caching configs such as the ids for fingers etc.
