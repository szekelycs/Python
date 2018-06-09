from mousedynamics.utils import settings as st
import csv
import numpy
import os
import pandas as pd
import re
from random import randint

from sklearn import model_selection
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score
from sklearn.ensemble import RandomForestClassifier



def testForUI(user, session, legality):
    featureTrainFile = st.classificationDir + st.classOutputFile + user + '.csv';
    trainDataset = pd.read_csv(featureTrainFile)
    NUM_TREES = 500
    numFeaturesTrain = int(trainDataset.shape[1])
    trainArray = trainDataset.values
    X_train = trainArray[:, 5: numFeaturesTrain]
    Y_train = trainArray[:, 0]

    if legality == 1:
        walkDir = st.legalOpDir
    else:
        walkDir = st.illegalOpDir

    featureTestFile = walkDir + user + '\\' + session[2:]


    testDataset = pd.read_csv(featureTestFile)
    numFeaturesTest = int(testDataset.shape[1])
    testArray = testDataset.values
    X_validation = testArray[:, 5: numFeaturesTest]
    Y_validation = []

    XValLength = len(X_validation)
    if(legality == 1):
        for i in range(0, XValLength):
            Y_validation.append(1)
    else:
        for i in range(0, XValLength):
            Y_validation.append(0)

    rf = RandomForestClassifier(n_estimators=NUM_TREES)
    rf.fit(X_train, Y_train)

    predictions = rf.predict_proba(X_validation)
    return predictions

##########################################################
##########################################################
##########################################################
##########################################################
# Test for each sessions file by file

def testSessionForUser(rf, user, featureTestFile, legality):
    # trainDataset = pd.read_csv(featureTrainFile)
    # NUM_TREES = 500
    # numFeaturesTrain = int(trainDataset.shape[1])
    # trainArray = trainDataset.values
    # X_train = trainArray[:, 5: numFeaturesTrain]
    # Y_train = trainArray[:, 0]

    testDataset = pd.read_csv(featureTestFile)
    numFeaturesTest = int(testDataset.shape[1])
    testArray = testDataset.values
    X_validation = testArray[:, 5: numFeaturesTest]
    Y_validation = []

    XValLength = len(X_validation)
    if(legality == 1):
        print("LEGAL SCORES")
        p = 'legal'
        for i in range(0, XValLength):
            Y_validation.append(1)
    else:
        print("ILLEGAL SCORES")
        p = 'illegal'
        for i in range(0, XValLength):
            Y_validation.append(0)

    # rf = RandomForestClassifier(n_estimators=NUM_TREES)
    # rf.fit(X_train, Y_train)
    predictions = rf.predict(X_validation)
    userAccuracy = accuracy_score(Y_validation, predictions)  # Y_predict



    print("Accuracy score")
    print("User " + re.findall('\d+', user)[0], userAccuracy, p)
    # print("Precision score")
    # print(precision_score(Y_validation, predictions))
    # print("Recall score")
    # print(recall_score(Y_validation, predictions))
    # print("Confusion matrix")
    # print(confusion_matrix(Y_validation, predictions))
    # print("Classification report")
    # print(classification_report(Y_validation, predictions))

    # return userAccuracy
# testSessionForUser(st.classificationDir + 'userClassification7.csv', st.legalOpDir + '7\\session_1244242475', 1)

def loopThroughLegalIllegal(legality):
    accuracy = []
    if legality == 1:
        walkDir = st.legalOpDir
    else:
        walkDir = st.illegalOpDir
    for dirname, dirnames, filenames in os.walk(st.classificationDir):
        for fileName in filenames:
            user = re.findall('\d+', fileName)[0]
            trainDataset = pd.read_csv(st.classificationDir + fileName)
            NUM_TREES = 500
            numFeaturesTrain = int(trainDataset.shape[1])
            trainArray = trainDataset.values
            X_train = trainArray[:, 5: numFeaturesTrain]
            Y_train = trainArray[:, 0]

            rf = RandomForestClassifier(n_estimators=NUM_TREES)
            rf.fit(X_train, Y_train)

            for dirnameTest, dirnamesTest, filenamesTest in os.walk(walkDir):
                for testDirName in dirnamesTest:
                    if testDirName == user:
                        for d1, d2, testFileNamesInTmpDir in os.walk(walkDir + testDirName):
                            for testFileNameInTmpDir in testFileNamesInTmpDir:
                                # print(walkDir, testDirName, testFileNameInTmpDir)
                                testSessionForUser(rf, user, walkDir + user + "\\" + testFileNameInTmpDir, legality)




# loopThroughLegalIllegal(0)

####################################################################################
####################################################################################
####################################################################################
####################################################################################
# TEST TEST TEST #

def createBinaryClassifierTestFiles(featureTrainFile, featureTestFile, method):
    trainDataset = pd.read_csv(featureTrainFile)
    NUM_TREES = 500
    numFeaturesTrain = int(trainDataset.shape[1])
    trainArray = trainDataset.values
    X_train = trainArray[:, 5: numFeaturesTrain]
    Y_train = trainArray[:, 0]

    testDataset = pd.read_csv(featureTestFile)
    numFeaturesTest = int(testDataset.shape[1])
    testArray = testDataset.values
    X_validation = testArray[:, 5: numFeaturesTest]
    Y_validation = testArray[:, 0]

    rf = RandomForestClassifier(n_estimators=NUM_TREES)
    rf.fit(X_train, Y_train)
    predictions = rf.predict(X_validation)
    userAccuracy = accuracy_score(Y_validation, predictions) #Y_predict

    if method == 1:
        print("SCORES")
    else:
        print("SCORES")

    print("Accuracy score")
    print("User " + re.findall('\d+', featureTrainFile)[0], userAccuracy)
    print("Precision score")
    print(precision_score(Y_validation, predictions))
    print("Recall score")
    print(recall_score(Y_validation, predictions))
    print("Confusion matrix")
    print(confusion_matrix(Y_validation, predictions))
    print("Classification report")
    print(classification_report(Y_validation, predictions))

    return userAccuracy


def loopThroughUsersTest():
    accuracy = []
    for dirname, dirnames, filenames in os.walk(st.classificationDir):
        for fileName in filenames:
            user = re.findall('\d+', fileName)[0]
            # print(user, " ", fileName)
            score1 = createBinaryClassifierTestFiles(st.classificationDir + fileName, st.classificationLegalTestDir + st.classOutputLegalTestFile + user + '.csv', 1)
            score2 = createBinaryClassifierTestFiles(st.classificationDir + fileName, st.classificationIllegalTestDir + st.classOutputIllegalTestFile + user + '.csv', 0)
            accuracy.append(score1)
            accuracy.append(score2)
            # input("Press Enter to continue...")
            # print(user, " legal: ", score1, " illegal: ", score2)


####################################################################################
####################################################################################
####################################################################################
####################################################################################
#  TRAIN TRAIN TRAIN #


def createBinaryClassifier(featureFileName):
    dataset = pd.read_csv(st.classificationDir + featureFileName)
    NUM_TREES = 500
    numFeatures = int(dataset.shape[1])
    array = dataset.values
    X = array[:, 5 : numFeatures]
    Y = array[:, 0]

    # print(dataset.shape)
    validation_size = 0.20
    seed = 7
    X_train, X_validation, Y_train, Y_validation = model_selection.train_test_split(X, Y, test_size=validation_size, random_state=seed)

    rf = RandomForestClassifier(n_estimators=NUM_TREES)
    rf.fit(X_train, Y_train)
    predictions = rf.predict(X_validation)
    userAccuracy = accuracy_score(Y_validation, predictions)


    print("Accuracy score")
    print("User " + re.findall('\d+', featureFileName)[0], userAccuracy)
    print("Precision score")
    print(precision_score(Y_validation, predictions))
    print("Recall score")
    print(recall_score(Y_validation, predictions))
    print("Confusion matrix")
    print(confusion_matrix(Y_validation, predictions))
    print("Classification report")
    print(classification_report(Y_validation, predictions))

    return userAccuracy

def loopThroughUsersTrainFilesOnly():
    accuracy = []
    for dirname, dirnames, filenames in os.walk(st.classificationDir):
        for fileName in filenames:
            # user = os.path.basename(fileName)
            user = re.findall('\d+', fileName)[0]
            # print(user, " ", fileName)
            score = createBinaryClassifier(fileName)
            accuracy.append(score)
            input("Press enter to continue...")

####################################################################################
####################################################################################
####################################################################################
####################################################################################
# BINARY CLASSIFIER CREATOR #


def classify(method):
    if method == 1:
        ipfi = st.outputFile
        opd = st.classificationDir
        opf = st.classOutputFile
    else:
        if method == 0:
            ipfi = st.outputTestFile
            opd = st.classificationTestDir
            opf = st.classOutputTestFile
        else:
            if method == 2:
                ipfi = st.outputLegalTestFile
                opd = st.classificationLegalTestDir
                opf = st.classOutputLegalTestFile
            else:
                if method == 3:
                    ipfi = st.outputIllegalTestFile
                    opd = st.classificationIllegalTestDir
                    opf = st.classOutputIllegalTestFile
                else:
                    print('Method error')
                    return


    result = numpy.array(list(csv.reader(open(ipfi))))
    result = numpy.delete(result, (0), axis=0)

    if not os.path.exists(opd):
        os.makedirs(opd)

    positionArray = []
    resultLength = len(result)
    firstRow = True

    for i in range(resultLength):
        if (firstRow == True):
            prevClassifier = result[i][0]
            positionArray.append(i)
            firstRow = False

        currentClassifier = result[i][0]

        if (prevClassifier == currentClassifier):
            prevClassifier = currentClassifier
        else:
            positionArray.append(i)
            prevClassifier = currentClassifier


    positionArray.append(resultLength - 1)
    positionArrayLength = len(positionArray)
    # print(positionArray)

    firstRow = True
    i = 0
    nsc = 0


    while i < positionArrayLength - 1:
        j = positionArray[i]
        if firstRow == True:
            firstRow = False
            outputFileName = opd + opf + result[positionArray[i]][0] + '.csv'
            with open(outputFileName, "w+", newline='') as outCSVClassifierFile:
                writer = csv.writer(outCSVClassifierFile, delimiter=',')
                writer.writerow(st.csvOutHeaders)

                positiveSampleCount = 0
                while j < positionArray[i + 1]:
                    positiveSampleCount = positiveSampleCount + 1
                    rowToAppend = []
                    rowToAppend.append('1')
                    rowToAppend.extend(result[j][1:])
                    writer.writerow(rowToAppend)
                    j = j + 1

                negativeSampleCount = positiveSampleCount / (positionArrayLength - 2)
                k = i
                while k < positionArrayLength - 1:
                    startIndex = positionArray[k]
                    endIndex = positionArray[k + 1]
                    while nsc < negativeSampleCount:
                        randomIndex = randint(startIndex, endIndex)
                        rowToAppend = []
                        rowToAppend.append('0')
                        rowToAppend.extend(result[randomIndex][1:])
                        writer.writerow(rowToAppend)
                        nsc = nsc + 1
                    nsc = 0
                    k = k + 1
            i = i + 1
            continue

        outputFileName = opd + opf + result[positionArray[i]][0] + '.csv'
        with open(outputFileName, "w+", newline='') as outCSVClassifierFile:
            writer = csv.writer(outCSVClassifierFile, delimiter=',')
            writer.writerow(st.csvOutHeaders)

            positiveSampleCount = 0
            while j < positionArray[i + 1]:
                rowToAppend = []
                rowToAppend.append('1')
                rowToAppend.extend(result[j][1:])
                writer.writerow(rowToAppend)
                j = j + 1
                positiveSampleCount = positiveSampleCount + 1


            negativeSampleCount = positiveSampleCount / (positionArrayLength - 2)
            k = 0
            while k < i:
                startIndex = positionArray[k]
                endIndex = positionArray[k + 1]

                while nsc < negativeSampleCount:
                    randomIndex = randint(startIndex, endIndex)
                    rowToAppend = []
                    rowToAppend.append('0')
                    rowToAppend.extend(result[randomIndex][1:])
                    writer.writerow(rowToAppend)
                    nsc = nsc + 1
                nsc = 0
                k = k + 1

            k = i + 1
            while k < positionArrayLength - 1:
                startIndex = positionArray[k]
                endIndex = positionArray[k + 1]

                while nsc < negativeSampleCount:
                    randomIndex = randint(startIndex, endIndex)
                    rowToAppend = []
                    rowToAppend.append('0')
                    rowToAppend.extend(result[randomIndex][1:])
                    writer.writerow(rowToAppend)
                    nsc = nsc + 1
                nsc = 0
                k = k + 1
        i = i + 1

####################################################################################
####################################################################################
####################################################################################
####################################################################################

# CALL SOME METHODS #


# classify(2)
# classify(3)
# classify(1)
# # 1 - train, 0 - test
# print('TRAIN')
# loopThroughUsersTrainFilesOnly()
# print('TEST')
# loopThroughUsersTest()
