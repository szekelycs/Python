outputFile = 'mouse_action_summary.csv'

#parameters for mouse move plots
leftClickOnly = 1
rightClickOnly = 1
dragOnly = 1
moveOnly = 1
timeLimit = 10
###################

#output csv headers
#TODO: angle - speed for every point? sum?
csvOutHeaders = ["user", "method", "session", "n_from", "n_to", "rowcnt", "type_of_action", "sumdist", "elpstime", "direction", "straight", "avg_velo"]
###################

#mouse move codenames
'mm'
mouseMove = 0
'lc'
leftClick = 1
'rc'
rightClick = 2
'ld'
leftDrag = 3
'rD'
rightDrag = 4
###################
trainDir = "E:\Egyetem\Allamvizsga\Python\csvFiles2"

