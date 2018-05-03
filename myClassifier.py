import settings as st
import csv
import numpy
from random import randint

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
                        rowToAppend.extend(result[j][1:-1])
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
                            rowToAppend.extend(result[randomIndex][1:-1])
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
                    rowToAppend.extend(result[j][1:-1])
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
                        rowToAppend.extend(result[randomIndex][1:-1])
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
                        rowToAppend.extend(result[randomIndex][1:-1])
                        writer.writerow(rowToAppend)
                        nsc = nsc + 1
                    nsc = 0
                    k = k + 1
            i = i + 1

classify('train')

