outputFile = 'mouse_action_summary.csv'

#parameters for mouse move plots
leftClickOnly = 1
rightClickOnly = 1
dragOnly = 1
moveOnly = 1
timeLimit = 10
###################

#output csv headers
csvOutHeaders = ["user", "method", "session", "n_from", "n_to", "row_cnt", "type_of_action", "sum_dist", "elps_time", "direction", "straightness", "min_ang", "max_ang", "avg_ang", "sum_ang", "min_vel", "max_vel", "avg_vel", "sum_vel"]
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

