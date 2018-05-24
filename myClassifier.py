import settings as st
import csv
import numpy
import pandas as pd
from random import randint

from pandas.plotting import scatter_matrix
import matplotlib.pyplot as plt
from sklearn import model_selection
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier

from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.naive_bayes import GaussianNB

def createBinaryClassifier(featureFileName):
    dataset = pd.read_csv(featureFileName)
    NUM_TREES = 500
    numFeatures = int(dataset.shape[1])
    array = dataset.values
    X = array[:, 4 : numFeatures - 1]
    Y = array[:, numFeatures - 1]
    # X = array[:, 0 : numFeatures - 1]
    # Y = array[:, numFeatures - 1]

    print(dataset.shape)
    validation_size = 0.20
    seed = 7
    X_train, X_validation, Y_train, Y_validation = model_selection.train_test_split(X, Y, test_size=validation_size, random_state=seed)

    rf = RandomForestClassifier(n_estimators=NUM_TREES)
    rf.fit(X_train, Y_train)
    predictions = rf.predict(X_validation)
    userAccuracy = accuracy_score(Y_validation, predictions)

    print(userAccuracy)

# def loopThroughUsers(userCount):
#     for i in userCount:
#         createBinaryClassifier()

def classify(method):
    if method == 'train':
        result = numpy.array(list(csv.reader(open(st.outputFile))))
        result = numpy.delete(result, (0), axis=0)

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

        firstRow = True
        i = 0
        nsc = 0


        while i < positionArrayLength - 1:
            j = positionArray[i]
            if firstRow == True:
                firstRow = False
                outputFileName = st.classOutputFile + result[positionArray[i]][0] + '.csv'
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

            outputFileName = st.classOutputFile + result[positionArray[i]][0] + '.csv'
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
classify('train')
# createBinaryClassifier('userClassification7.csv')
