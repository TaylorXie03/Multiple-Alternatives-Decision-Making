
import random

import psychopy.visual
import psychopy.event
import psychopy.hardware
from psychopy.tools import monitorunittools
import numpy as np
import csv
import pickle as pkl

win = psychopy.visual.Window(
    size = [1200, 1000],
    units = "pix",
    fullscr = False,
    color = [1, 1, 1]
)

#center_1, center_2, center_3, response = [], [], [], []

eccentricity = 8

#instruction
instrText = """You will see three groups of exemplar dots represented a bird's eye view of three groups of people.\n 
    The distribution of the three groups are circular and symmetrical and the centers of the three groups only varied horizontally.\n
    Each group wears a different color of shirt. The black dot represents a person from one of the three groups. \n\n
    1) Please categorize this person to one of the three groups based on the position information you have. \n
    2) Report your confidence on a four-point Likert scale.\n
    Please press "space" to start the trials."""
text = psychopy.visual.TextStim(
    win=win,
    text = instrText,
    font = "Arial",
    color = [-1, -1, -1]
)

text.draw()
win.flip()
psychopy.event.waitKeys(keyList = "space")
win.flip()

#circle on the left
dots_left = psychopy.visual.DotStim( 
    win = win,
    units = "pix",
    nDots = 375,
    fieldShape = "circle",
    dotSize = 3,
    fieldPos = (-90, 50),
    fieldSize = (300, 300)
)

#determine color for the circle on the left
color_left = random.randint(1, 3)
if color_left == 1:
    dots_left.color = [-1, -1, 1] #green
elif color_left == 2:
    dots_left.color = [1, -1, -1] #red
else:
    dots_left.color = [-1, 1, -1] #blue

#center
dots_center = psychopy.visual.DotStim( 
    win = win,
    units = "pix",
    nDots = 375,
    fieldShape = "circle",
    dotSize = 3,
    fieldPos = (0, 50), #set y=50 to give the response boxes more room
    fieldSize = (300, 300)
)

#determine color
keep_going = True

while keep_going:
    color_center= random.randint(1, 3)
    if color_center != color_left:
        keep_going = False

if color_center == 1:
    dots_center.color = [-1, -1, 1] #green
elif color_center == 2:
    dots_center.color = [1, -1, -1] #red
else:
    dots_center.color = [-1, 1, -1] #blue

#right
dots_right = psychopy.visual.DotStim( 
    win = win,
    units = "pix",
    nDots = 375,
    fieldShape = "circle",
    dotSize = 3,
    fieldPos = (90, 50),
    fieldSize = (300, 300)
)

#determine color
keep_going = True

while keep_going:
    color_right= random.randint(1, 3)
    if color_right != color_left and color_right != color_center:
        keep_going = False

if color_right == 1:
    dots_right.color = [-1, -1, 1] #green
elif color_right == 2:
    dots_right.color = [1, -1, -1] #red
else:
    dots_right.color = [-1, 1, -1] #blue

#target dot
target_dot = psychopy.visual.Circle( 
    win = win,
    units = "pix",
    radius = 2.5,
    fillColor = [-1, -1, -1],
    lineColor = [-1, -1, -1],
    edges = 150,
    pos = [random.randint(-200, 200), random.randint(-100, 100)]
)

#create colored response box
red_box = psychopy.visual.ButtonStim(
    win = win,
    units = "pix",
    text = "",
    pos = (-90, -150),
    size = (30, 50),
    fillColor = [1, -1, -1],
    borderColor = [-1, -1, -1],
    borderWidth = 15
)

blue_box = psychopy.visual.ButtonStim(
    win = win,
    units = "pix",
    text = "",
    pos = (0, -150),
    size = (30, 50),
    fillColor = [-1, 1, -1],
    borderColor = [-1, -1, -1],
    borderWidth = 15
)

green_box = psychopy.visual.ButtonStim(
    win = win,
    units = "pix",
    text = "",
    pos = (90, -150),
    size = (30, 50),
    fillColor = [-1, -1, 1],
    borderColor = [-1, -1, -1],
    borderWidth = 15
)

# --------------- start the trials --------------- 
#nTrial_1 = 84
#for i in range(nTrial_1):
dots_left.draw()
dots_center.draw()
dots_right.draw()
target_dot.draw()

red_box.draw()
blue_box.draw()
green_box.draw()

win.flip()
    
    

psychopy.event.waitKeys(keyList = "1")

#core.wait(6) #wait for 600ms before the next trial

win.close()
