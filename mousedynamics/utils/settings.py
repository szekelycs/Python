# outputFile = 'balabit_features_training_SZCS.csv'
outputFile = 'mouse_action_summary.csv'
outputTestFile = 'test_mouse_action_summary.csv'
outputLegalTestFile = 'legal_test_mouse_action_summary.csv'
outputIllegalTestFile = 'illegal_test_mouse_action_summary.csv'

publicLabels = 'public_labels.csv'
classOutputFile = 'userClassification'
classOutputTestFile = 'userClassificationTest'

classOutputLegalTestFile = 'userClassificationLegalTest'
classOutputIllegalTestFile = 'userClassificationIllegalTest'
thresholdFile = 'thresholds.csv'
scoreFile = 'userScores.csv'

userCount = 10

#parameters for mouse move plots
leftClickOnly = 1
rightClickOnly = 1
dragOnly = 1
moveOnly = 1
timeLimit = 10
###################

#output csv headers
csvOutHeaders = ["user", "method", "session", "n_from", "n_to", "row_cnt", "type_of_action", "sum_dist", "elps_time", "direction", "straightness", "sd_ang", "max_ang", "mean_ang", "sd_velx", "max_velx", "mean_velx", "sd_vely", "max_vely", "mean_vely", "sd_vel", "max_vel", "mean_vel", "sd_acc", "max_acc", "mean_acc", "w_sd", "w_max", "w_mean", 'jerk_std', 'jerk_max', 'jerk_mean', 'sum_angles', 'pos_acc_time', 'pos_acc_time_part']
scoreFileHeaders = ["label", "score"]
method = 1
testMethod = 0

legalTestMethod = 2
illegalTestMethod = 3
# 1 - train, 0 - test
###################

#mouse action colors for plotting
colorMM = 'red'
colorLC = 'blue'
colorRC = 'green'
colorDD = 'black'


#mouse action codenames
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
classificationTestDir = 'D:\\Uni\\Allamvizsga\\Python\\classification_test_files\\'

classificationLegalTestDir = 'D:\\Uni\\Allamvizsga\\Python\\classification_legal_test_files\\'
classificationIllegalTestDir = 'D:\\Uni\\Allamvizsga\\Python\\classification_illegal_test_files\\'

legalTestSessionCopy = 'D:\\Uni\\Allamvizsga\\Python\\legal_test_files\\'
illegalTestSessionCopy = 'D:\\Uni\\Allamvizsga\\Python\\illegal_test_files\\'

legalOpDir = 'D:\\Uni\\Allamvizsga\\Python\\legalSessionsFeatures\\'
illegalOpDir = 'D:\\Uni\\Allamvizsga\\Python\\illegalSessionsFeatures\\'
modelDir = 'D:\\Uni\\Allamvizsga\\Python\\RFModels\\'

testPlotsDir = 'D:\\Uni\\Allamvizsga\\Python\\TestPlots\\'

positive = 'D:\\Uni\\Allamvizsga\\Python\\results\\positive.png'
negative = 'D:\\Uni\\Allamvizsga\\Python\\results\\negative.png'
empty = 'D:\\Uni\\Allamvizsga\\Python\\results\\empty.png'

workDir = 'D:\\Uni\\Allamvizsga\\Python\\'

# scoreDir = 'D:\\Uni\\Allamvizsga\\Python\\scoreFiles\\'

###################
# upper limit for xCoord and yCoord
upLim = 2500
