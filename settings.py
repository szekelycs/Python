# TODO: 25/05/2018 - classify metódus - 'continuous' típus probléma; tesztelés teszthalmazzal



# outputFile = 'balabit_features_training_SZCS.csv'
outputFile = 'mouse_action_summary.csv'
outputTestFile = 'test_mouse_action_summary.csv'
classOutputFile = 'userClassification'
#parameters for mouse move plots
leftClickOnly = 1
rightClickOnly = 1
dragOnly = 1
moveOnly = 1
timeLimit = 10
###################

#output csv headers
csvOutHeaders = ["user", "method", "session", "n_from", "n_to", "row_cnt", "type_of_action", "sum_dist", "elps_time", "direction", "straightness", "sd_ang", "max_ang", "mean_ang", "sd_velx", "max_velx", "mean_velx", "sd_vely", "max_vely", "mean_vely", "sd_vel", "max_vel", "mean_vel", "sd_acc", "max_acc", "mean_acc", "w_sd", "w_max", "w_mean", 'jerk_std', 'jerk_max', 'jerk_mean', 'sum_angles']
method = 0
# 1 - train, 0 - test
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
trainDir = 'D:\\Uni\\Allamvizsga\\Python\\csvFiles'
testDir = 'D:\\Uni\\Allamvizsga\\Python\\test_files'
classificationDir = 'D:\\Uni\\Allamvizsga\\Python\\classification_files\\'

###################
# upper limit for xCoord and yCoord
upLim = 2500
