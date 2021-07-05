
from psychopy import visual, event, hardware, monitors, data, core
from psychopy.tools import monitorunittools
import numpy as np
import csv
import pickle as pkl
import copy
from time import localtime, strftime

# ==================== subject info ===================
subjID = "001"
runID = 1
timeStamp = strftime('%Y%m%d%H%M%S',localtime())
fileName = f'{timeStamp}_Multiple Alternatives Decision-Making_{subjID}_run{runID: 02d}'
# =================================================

mon = monitors.Monitor('mac')
mon.setSizePix([2560, 1600])
mon.setWidth(52.71) #cm
mon.setDistance(57)

win = visual.Window(
    size = [1200, 1000],
    units = "deg",
    monitor = mon,
    fullscr = False
)
event.globalKeys.clear()
event.globalKeys.add(key='q', func=core.quit)

# ================= experiment setting =================
nCond = 4
trialPerCond = 84
nTrial = nCond * trialPerCond # 336 trials in total

# dot properties
circle_colors = [(1, -1, -1), (-1, 1, -1), (-1, -1, 1)] # r/g/b
pos = [[(-3, 2), (0, 2), (3, 2)], [(-4, 2), (0, 2), (4, 2)], [(-3, 2), (-2, 2), (3, 2)], [(-3, 2), (2, 2), (3, 2)]] #pos for 4 configs
nDots = 375
dotSize = 0.2 # deg
dotStd = 2 # deg, std of dots distribution  

# box properties
box_pos = [(-3, -4), (0, -4), (3, -4)]

# confidence box properties
confidence_box_pos = [[(-4, -6)], [(-2, -6)], [(2, -6)], [(4, -6)]]
# =================================================

# instruction
instrText = \
    "- You will see three groups of exemplar dots represented a bird's eye view of three groups of people.\n \
    - The distribution of the three groups are circular and symmetrical and the centers of the three groups only varied horizontally.\n \
    - Each group wears a different color of shirt.\n \
    - The black dot represents a person from one of the three groups. \n\n \
    1) Please categorize this person to one of the three groups based on the position information you have.\n (Press '1', '2', or '3' to answer) \n \
    2) Report your confidence on a four-point Likert scale.\n (Press '1', '2', '3', or '4' to answer)\n\n \
    Please press 'space' to start the trials and 'q' to quit anytime."
text = visual.TextStim(
    win=win,
    text = instrText,
    font = "Arial",
    height = 0.5,
    units = "deg",
    color = [1, 1, 1]
)

text.draw()
win.flip()
event.waitKeys(keyList = "space")
win.flip()

#-------three groups of dots-------
dots_left = visual.ElementArrayStim( 
    win = win,
    units = "deg",
    nElements = nDots,
    fieldShape = "circle",
    fieldSize = (200, 200),
    sizes = dotSize
)
dots_center = copy.copy(dots_left)
dots_right = copy.copy(dots_left)

#-------target dot-------
target_dot = visual.Circle( 
    win = win,
    units = "deg",
    radius = 0.05,
    fillColor = [-1, -1, -1],
    lineColor = [-1, -1, -1],
    edges = 50
)

#-------colored response boxes-------
box_left = visual.Rect(
    win = win,
    units = "deg",
    size = (1, 0.5),
    lineColor = [-1, -1, -1],
    lineWidth = 15,
    pos = box_pos[0]
)

box_left_text = visual.TextStim(
    win = win,
    units = "deg",
    text = "(1)",
    font = "Arial",
    height = 0.4,
    color = [-1, -1, -1],
    pos = box_pos[0]
)
    
box_center = copy.copy(box_left)
box_center.pos = box_pos[1]
box_center_text = copy.copy(box_left_text)
box_center_text.pos = box_pos[1]
box_center_text.setText("(2)")

box_right = copy.copy(box_left)
box_right.pos = box_pos[2]
box_right_text = copy.copy(box_left_text)
box_right_text.pos = box_pos[2] 
box_right_text.setText("(3)")

q_text = "Which group does the black dot belong to?" # present the first question
q_text = visual.TextStim(
    win=win,
    text = q_text,
    font = "Arial",
    height = 0.5,
    color = [-1, -1, -1],
    pos = (0, -5)
)

#-------confidence level boxes-------
very_low_box = visual.Rect(
    win = win,
    units = "deg",
    pos = (-4.5, -6),
    size = (2, 1),
    fillColor = [0, 0, 0],
    lineColor = [-1, -1, -1],
    lineWidth = 15
)

very_low_text = "Very\nlow\n(1)"
print_very_low = visual.TextStim(
    win=win,
    text = very_low_text,
    font = "Arial",
    height = 0.3,
    units = "deg",
    color = [-1, -1, -1],
    pos = (-4.5, -6)
)

somewhat_low_box = copy.copy(very_low_box)
somewhat_low_box.pos = (-1.5, -6)
print_somewhat_low = copy.copy(print_very_low)
print_somewhat_low.setText("Somewhat\nlow\n(2)")
print_somewhat_low.pos = (-1.5, -6)

somewhat_high_box = copy.copy(very_low_box)
somewhat_high_box.pos = (1.5, -6)
print_somewhat_high = copy.copy(print_very_low)
print_somewhat_high.setText("Somewhat\nhigh\n(3)")
print_somewhat_high.pos = (1.5, -6)

very_high_box = copy.copy(very_low_box)
very_high_box.pos = (4.5, -6)
print_very_high = copy.copy(print_very_low)
print_very_high.setText("Very\nhigh\n(4)")
print_very_high.pos = (4.5, -6)

confidence_text = "How confident are you in your decision?" # present the second question
confidence_text = visual.TextStim(
    win=win,
    text = confidence_text,
    font = "Arial",
    height = 0.5,
    color = [-1, -1, -1],
    pos = (0, -7)
)

# ===========================================================
condition = np.arange(nTrial)
condition  = np.mod(condition, 4)
np.random.shuffle(condition) # shuffle the four configurations

all_colors = [] # save all colors
circles_mean = [] # save the means of the circles
target_dot_pos = [] # save target dot positions
responses = [] # save box and confidence choices
data = {} # store colors, means, target dot position, and two responses into data dict

# ======================== start the trials ========================
nTrial_1 = 3
for i in range(nTrial_1):
    # determine the condition
    pos_tmp = pos[condition[i]]
    circles_mean.append(pos_tmp) # save means of each trial in circle_mean

    # determine the colors
    circle_color = np.arange(3)
    np.random.shuffle(circle_color) # circles take on a random color
    all_colors.append(list(circle_color)) # save circle_color as a list in all_colors

    # left dots set pos & color and draw
    dots_left.setFieldPos(pos_tmp[0])
    dots_left_pos = np.random.multivariate_normal(pos_tmp[0], cov=[[dotStd**2, 0], [0, dotStd**2]], size=nDots)
    dots_left.setXYs(dots_left_pos)
    dots_left.colors = circle_colors[circle_color[0]] # circle_color contains a shuffled version of "0, 1, 2" and circle_colors contains the actual rbg code of the colors
    dots_left.draw()

    # center dots set pos & color and draw
    dots_center.setFieldPos(pos_tmp[1])
    dots_center_pos = np.random.multivariate_normal(pos_tmp[1], cov=[[dotStd**2, 0], [0, dotStd**2]], size=nDots)
    dots_center.setXYs(dots_center_pos)
    dots_center.colors = circle_colors[circle_color[1]] 
    dots_center.draw()

    # right dots set pos & color and draw
    dots_right.setFieldPos(pos_tmp[2])
    dots_right_pos = np.random.multivariate_normal(pos_tmp[2], cov=[[dotStd**2, 0], [0, dotStd**2]], size=nDots)
    dots_right.setXYs(dots_right_pos)
    dots_right.colors = circle_colors[circle_color[2]]
    dots_right.draw()

    # target dot set pos and draw
    tarRange = -pos_tmp[0][0]+pos_tmp[-1][0]+0.4
    tarPosX = np.random.rand() * tarRange - tarRange/2
    tarPosY = np.random.rand()*4-2
    target_dot.setPos([tarPosX, tarPosY])
    target_dot.draw()
    target_dot_pos.append(target_dot.pos) # save target dot position of each trial in target_dot_pos

    # answer boxes for the 1st question set colors and draw (box colors correspond with the dot colors)
    box_left.setColor(circle_colors[circle_color[0]])
    box_left.draw()
    box_left_text.draw()
    box_center.setColor(circle_colors[circle_color[1]])
    box_center.draw()
    box_center_text.draw()
    box_right.setColor(circle_colors[circle_color[2]])
    box_right.draw()
    box_right_text.draw()
    q_text.draw()

    # confidence level boxes draw
    very_low_box.draw()
    print_very_low.draw()
    somewhat_low_box.draw()
    print_somewhat_low.draw()
    somewhat_high_box.draw()
    print_somewhat_high.draw()
    very_high_box.draw()
    print_very_high.draw()
    confidence_text.draw()

    win.flip()

    # collect responses
    trialResp = [] # save 2 answers in trialResp first
    
    ans1 = event.waitKeys(keyList = ["1", "2", "3"])
    
    ans2 = event.waitKeys(keyList = ["1", "2", "3", '4'])
    trialResp = ans1 + ans2
    
    responses.append(trialResp) # append responses of each trial in a collective list 

# save data
data["Colors"] = all_colors
data["Means"] = circles_mean
data["Target dot pos"] = target_dot_pos
data["Responses"] = responses

# store data
with open(f'{fileName}.pkl', 'wb') as f:
    pkl.dump(data, f)

# load data 
#with open(f'{fileName}.pkl', 'rb') as f:
#    data = pkl.load(f)

win.close()