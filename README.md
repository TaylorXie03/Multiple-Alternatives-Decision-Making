# Multiple Alternatives Decision-Making
A multiple alternatives decision-making task for confidence report 

Reference: Li, HH., Ma, W.J. Confidence reports in decision-making with multiple alternatives violate the Bayesian confidence hypothesis. Nat Commun 11, 2004 (2020). https://doi.org/10.1038/s41467-020-15581-6

**Developer**
Yuan (Taylor) Xie - yx2031@nyu.edu

**History**
20210702 Yuan (Taylor) Xie created it

**Task details**
- window size: 1200x1000 pixels
- Experiment contains 3 groups of dots of different colors (red, green, blue). 
- Three groups of dots have 4 configurations. Each configuration appears 84 times. Four configurations show up randomly, so 336 trials in total.
    - Means of the four configurations: 
        [(-3, 2), (0, 2), (3, 2)], [(-4, 2), (0, 2), (4, 2)], [(-3, 2), (-2, 2), (3, 2)], [(-3, 2), (2, 2), (3, 2)]
- Dot properties:
    - Each group has 375 dots.
    - Dot size is 0.2 degree.
    - Dot standard deviation is 2 degrees. 
    - The distribution of dots is a Gaussian distribution, using numpy.random.multivariate_normal
- Target dot properties:
    - Radius: 0.05
    - Black
    - Position is sampled uniformly from the mean of the leftmost group + 0.2 degree to the mean of the rightmost group + 0.2 degree
        tarRange = -pos_tmp[0][0]+pos_tmp[-1][0]+0.4
        x = np.random.rand() * tarRange - tarRange/2
        y = np.random.rand()*4-2
- Continues to the next trial after the subject finishes answering the two questions.
- Results: 
    - The results are saved as pkl files, named as "time_experiment title_subject ID_number run." (e.g. 20210702152334_Multiple Alternatives Decision-Making_001_run 1.pkl)
    - Result of each trial contains 4 elements: order of the colors of the groups, circle means, target dot position, subject's responses to two answers. 
    - Each element is a list. 
        - Color list contains the numbers corresponding to the three colors ("0" for red, "1" for green, "2" for blue). Within each list, the number at index position 0 indicates the color of the leftmost group, the number at position 1 indicates the color of the center group, ... (e.g. [[2, 1, 0], [0, 2, 1]])
        - Circle mean list contains the means of the three groups. (e.g. [[(-4, 2), (0, 2), (4, 2)], [(-3, 2), (0, 2), (3, 2)]])
        - Target dot position list contains arrays of the x,y positions of the target dot. (e.g. [array([-3.47171958,  1.52076317]), array([-2.59934763,  1.42143844])])
        - Responses list contains a list with the two chosen options. (e.g. [['1', '3'], ['3', '4']])

**Instruction for experimenter**
    - This program only contains one file.
    - Subject ID and number run can be changed.
    - The means of the groups can be adjusted at the "experiment setting" section in the program.

**Instruction for subjects**
    - Subjects press the number keys (1, 2, 3 for Q1 and 1, 2, 3, 4 for Q2) to answer the questions. 
    - The two questions appear on the screen at the same time with the stimuli so continue to answer the second question after finishing the first one. 
    - There won't be any notice after answering the first question but the second set of stimuli would appear after successfully completing both questions. 
    - Instructions shown before starting the trials: 
        "- You will see three groups of exemplar dots represented a bird's eye view of three groups of people.
        - The distribution of the three groups are circular and symmetrical and the centers of the three groups only varied horizontally.
        - Each group wears a different color of shirt.
        - The black dot represents a person from one of the three groups.
        1) Please categorize this person to one of the three groups based on the position information you have. (Press '1', '2', or '3' to answer)
        2) Report your confidence on a four-point Likert scale. (Press '1', '2', '3', or '4' to answer)
        Please press 'space' to start the trials and 'q' to quit anytime."
    
