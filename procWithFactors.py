import csv
import settings as st
import countFactors as cf
import os
import re

def processCsv(method):

    with open(st.outputTestFile, "w+", newline='') as csvOutFile:
        writer = csv.writer(csvOutFile, delimiter=',')
        writer.writerow(st.csvOutHeaders)

        for dirname, dirnames, filenames in os.walk(st.testDir):
            for fileName in filenames:
                user = os.path.basename(dirname)
                user = re.findall('\d+', user)[0]

                absoluteFilePath = os.path.join(dirname, fileName)
                # open csv reader and writer files
                with open(absoluteFilePath) as csvInFile:
                    reader = csv.reader(csvInFile)

                    fileName = re.findall(r'\d+', fileName)[0]


                    # starts counting at the beginning of mouse action
                    rowCnt = rowCntWithoutDuplicates = 0;
                    # 1 - if left click is pressed # 0 - if no action with left button
                    leftPressed = 0
                    # 1 - if right click is pressed # 0 - if no action with right button
                    rightPressed = 0
                    # 1 - if left mb is clicked before drag # 0 - if no action with left button drag
                    leftDrag = 0
                    # 1 - if right mb is clicked before drag # 0 - if no action with right button drag
                    rightDrag = 0
                    # first parameter of csv row - value = start time of mouse action
                    tmpStartTime = 0
                    # first line of csv contains headers
                    firstLine = True
                    # contains the processed row number
                    allRows = 1
                    # coordinates vectors for x and y coordinates
                    xCoords = []
                    yCoords = []
                    timeDatas = []
                    # vector for travelled distance and direction
                    distanceDetails = []

                    for row in reader:
                        # skipping first line
                        if firstLine:
                            firstLine = False
                            prevRow = row
                            continue


                        # incrementing total row value
                        allRows = allRows + 1

                        if row == prevRow:
                            continue
                        else:
                            rowCntWithoutDuplicates = rowCntWithoutDuplicates + 1

                        # incrementing the mouse move row value
                        rowCnt = rowCnt + 1

                        # save starting time and starting line
                        if rowCnt == 1:
                            # mouse move starting time
                            tmpStartTime = float(row[1])
                            # mouse move starting line
                            tmpStartLine = allRows

                        # "switch case" for categorizing the mouse actions
                        ################################## CASE MOVE ##################################
                        if row[3] == 'Move':
                            # check if lime limit is exceeded
                            limit = tmpStartTime + st.timeLimit
                            # if drag follows save finishing time for the mouse move action
                            tmpMoveFinishTime = float(row[1]);
                            # appending x and y coords to the vectors
                            if float(row[4]) < st.upLim or float(row[5]) < st.upLim:
                                xCoords.append(float(row[4]))
                                yCoords.append(float(row[5]))
                                timeDatas.append(float(row[1]))

                            # exceeded limit case
                            if limit < float(row[1]):
                                if rowCntWithoutDuplicates > 4 :
                                    # distance and straightness
                                    distanceDetails = cf.countMoveDistance(xCoords, yCoords)
                                    # time
                                    time = float(row[1]) - tmpStartTime;
                                    # direction
                                    angleInRad = cf.countSumDirection(xCoords[0], yCoords[0], xCoords[-1], yCoords[-1])
                                    angleVeloDetails = cf.pointSpeedAngleAcceleration(user, fileName, xCoords, yCoords, timeDatas, rowCntWithoutDuplicates)

                                    # append to csv file
                                    writer.writerow([user, method, fileName, tmpStartLine, allRows, rowCnt, st.mouseMove, distanceDetails[0], time, angleInRad, distanceDetails[1], angleVeloDetails[0], angleVeloDetails[1], angleVeloDetails[2], angleVeloDetails[3], angleVeloDetails[4], angleVeloDetails[5], angleVeloDetails[6], angleVeloDetails[7], angleVeloDetails[8], angleVeloDetails[9], angleVeloDetails[10], angleVeloDetails[11], angleVeloDetails[12], angleVeloDetails[13], angleVeloDetails[14], angleVeloDetails[15], angleVeloDetails[16], angleVeloDetails[17], angleVeloDetails[18], angleVeloDetails[19], angleVeloDetails[20], angleVeloDetails[21]])  # mouse move
                                    # empty the vectors with the x and y coordinates
                                del timeDatas[:]
                                del xCoords[:]
                                del yCoords[:]
                                # reinitialize rowCnt
                                rowCnt = 0
                                rowCntWithoutDuplicates = 0
                        else:
                            ################################## CASE PRESSED ##################################
                            if row[3] == 'Pressed':
                                # case left click
                                if row[2] == 'Left':
                                    # leftpressed ON
                                    leftPressed = 1
                                    # if drag follows we save the time
                                    tmpLeftDragStartTime = float(row[1])
                                    # if drag follows we save the x and y coordinates and we append x and y coordinates if left click happens
                                    if float(row[4]) < st.upLim or float(row[5]) < st.upLim:
                                        dragStartX = float(row[4])
                                        dragStartY = float(row[5])
                                        xCoords.append(float(row[4]))
                                        yCoords.append(float(row[5]))
                                        timeDatas.append(float(row[1]))
                                # case right click
                                else:
                                    # case right click
                                    rightPressed = 1
                                    # if right click drag follows we save the time
                                    tmpRightDragStartTime = float(row[1])
                                    # if drag follows we save the x and y coordinates and we append x and y coordinates if right click release
                                    if float(row[4]) < st.upLim or float(row[5]) < st.upLim:
                                        dragStartX = float(row[4])
                                        dragStartY = float(row[5])
                                        xCoords.append(float(row[4]))
                                        yCoords.append(float(row[5]))
                                        timeDatas.append(float(row[1]))
                            else:
                                ################################## CASE DRAG ##################################
                                if row[3] == 'Drag':
                                    # case left click before drag
                                    if leftPressed == 1:
                                        # if xy coords is not empty we pop the pressed line x and y coordinates (end of mouse move action)
                                        if xCoords and yCoords:
                                            xCoords.pop()
                                            yCoords.pop()

                                            # distance and straightness
                                            distanceDetails = cf.countMoveDistance(xCoords, yCoords)

                                            # time, direction, velocities(unit/s)
                                            if (rowCntWithoutDuplicates - 2) > 4:
                                                time = tmpMoveFinishTime - tmpStartTime;
                                                angleInRad = cf.countSumDirection(xCoords[0], yCoords[0], xCoords[-1], yCoords[-1])
                                                tmpMoveFinishTime = None
                                                # angle and speed datas (min, max, avg point by point)
                                                angleVeloDetails = cf.pointSpeedAngleAcceleration(user, fileName, xCoords, yCoords, timeDatas, rowCntWithoutDuplicates)
                                                # if (len(xCoords) != rowCntWithoutDuplicates):
                                                #     print(user, fileName, len(xCoords), len(yCoords), len(timeDatas), rowCntWithoutDuplicates, tmpStartLine, allRows)
                                                # append to csv file
                                                writer.writerow([user, method, fileName, tmpStartLine, allRows - 2, rowCnt - 2, st.mouseMove, distanceDetails[0], time, angleInRad, distanceDetails[1], angleVeloDetails[0], angleVeloDetails[1], angleVeloDetails[2], angleVeloDetails[3], angleVeloDetails[4], angleVeloDetails[5], angleVeloDetails[6], angleVeloDetails[7], angleVeloDetails[8], angleVeloDetails[9], angleVeloDetails[10], angleVeloDetails[11], angleVeloDetails[12], angleVeloDetails[13], angleVeloDetails[14], angleVeloDetails[15], angleVeloDetails[16], angleVeloDetails[17], angleVeloDetails[18], angleVeloDetails[19], angleVeloDetails[20], angleVeloDetails[21]])           #mouse move
                                            # empty vectors with x and y coordinates
                                            del timeDatas[:]
                                            del xCoords[:]
                                            del yCoords[:]
                                            # append drag start x and y coordinates (pressed coordiantes)
                                        xCoords.append(dragStartX)
                                        yCoords.append(dragStartY)
                                        timeDatas.append(tmpLeftDragStartTime)

                                        # append first drag type row coordinates
                                        xCoords.append(float(row[4]))
                                        yCoords.append(float(row[5]))
                                        timeDatas.append(float(row[1]))
                                        # reinitialize values
                                        tmpStartTime = tmpLeftDragStartTime
                                        rowCnt = 2
                                        rowCntWithoutDuplicates = 2
                                        tmpStartLine = allRows - 1
                                        leftDrag = 1
                                        leftPressed = 0
                                    else:
                                        # case left click drag
                                        if leftDrag == 1:
                                            if float(row[4]) < st.upLim or float(row[5]) < st.upLim:
                                                xCoords.append(float(row[4]))
                                                yCoords.append(float(row[5]))
                                                timeDatas.append(float(row[1]))
                                        else:
                                            # case right click before drag
                                            if rightPressed == 1:
                                                # if xy coords is not empty we pop the pressed line x and y coordinates (end of mouse move action)
                                                if xCoords and yCoords:
                                                    xCoords.pop()
                                                    yCoords.pop()

                                                    if (rowCntWithoutDuplicates - 2) > 4:
                                                        # distance and straightness
                                                        distanceDetails = cf.countMoveDistance(xCoords, yCoords)
                                                        # time, direction, velocity(unit/s)
                                                        time = tmpMoveFinishTime - tmpStartTime;
                                                        angleInRad = cf.countSumDirection(xCoords[0], yCoords[0], xCoords[-1], yCoords[-1])
                                                        tmpMoveFinishTime = None
                                                        # angle and speed datas (min, max, avg point by point)
                                                        # if (len(xCoords) != rowCntWithoutDuplicates):
                                                        #     print(user, fileName, len(xCoords), len(yCoords), len(timeDatas), rowCntWithoutDuplicates, tmpStartLine, allRows)
                                                        angleVeloDetails = cf.pointSpeedAngleAcceleration(user, fileName, xCoords, yCoords, timeDatas, rowCntWithoutDuplicates)
                                                        # append to csv file
                                                        writer.writerow([user, method, fileName, tmpStartLine, allRows - 2, rowCnt - 2, st.mouseMove, distanceDetails[0], time, angleInRad, distanceDetails[1], angleVeloDetails[0], angleVeloDetails[1], angleVeloDetails[2], angleVeloDetails[3], angleVeloDetails[4], angleVeloDetails[5], angleVeloDetails[6], angleVeloDetails[7], angleVeloDetails[8], angleVeloDetails[9], angleVeloDetails[10], angleVeloDetails[11], angleVeloDetails[12], angleVeloDetails[13], angleVeloDetails[14], angleVeloDetails[15], angleVeloDetails[16], angleVeloDetails[17], angleVeloDetails[18], angleVeloDetails[19], angleVeloDetails[20], angleVeloDetails[21]])  # mouse move
                                                    # empty vectors
                                                    del timeDatas[:]
                                                    del xCoords[:]
                                                    del yCoords[:]
                                                    # append drag start x and y coordinates (pressed coordinates)
                                                xCoords.append(dragStartX)
                                                yCoords.append(dragStartY)
                                                timeDatas.append(tmpRightDragStartTime)

                                                # append the first drag type x and y coordinates
                                                xCoords.append(float(row[4]))
                                                yCoords.append(float(row[5]))
                                                timeDatas.append(float(row[1]))
                                                # reinitalize starting time with current value
                                                tmpStartTime = tmpRightDragStartTime
                                                rowCnt = 2
                                                rowCntWithoutDuplicates = 2
                                                tmpStartLine = allRows - 1
                                                rightDrag = 1
                                                rightPressed = 0
                                            else:
                                                # case right click drag
                                                if rightDrag == 1:
                                                    if float(row[4]) < st.upLim or float(row[5]) < st.upLim:
                                                        xCoords.append(float(row[4]))
                                                        yCoords.append(float(row[5]))
                                                        timeDatas.append(float(row[1]))
                                else:
                                    ################################## CASE RELEASED ##################################
                                    if row[3] == 'Released':
                                        # case right click
                                        if rightPressed == 1:
                                            # release coordinates append
                                            if float(row[4]) < st.upLim or float(row[5]) < st.upLim:
                                                xCoords.append(float(row[4]))
                                                yCoords.append(float(row[5]))
                                                timeDatas.append(float(row[1]))

                                            if rowCntWithoutDuplicates > 4:
                                                # distance and straightness
                                                distanceDetails = cf.countMoveDistance(xCoords, yCoords)
                                                # time
                                                time = float(row[1]) - tmpStartTime
                                                # direction
                                                angleInRad = cf.countSumDirection(xCoords[0], yCoords[0], xCoords[-1], yCoords[-1])
                                                # angle and speed datas (min, max, avg point by point)
                                                # if (len(xCoords) != rowCntWithoutDuplicates):
                                                #     print(user, fileName, len(xCoords), len(yCoords), len(timeDatas), rowCntWithoutDuplicates, tmpStartLine, allRows)
                                                angleVeloDetails = cf.pointSpeedAngleAcceleration(user, fileName, xCoords, yCoords, timeDatas, rowCntWithoutDuplicates)
                                                # append to csv file
                                                writer.writerow([user, method, fileName, tmpStartLine, allRows, rowCnt, st.rightClick, distanceDetails[0], time, angleInRad, distanceDetails[1], angleVeloDetails[0], angleVeloDetails[1], angleVeloDetails[2], angleVeloDetails[3], angleVeloDetails[4], angleVeloDetails[5], angleVeloDetails[6], angleVeloDetails[7], angleVeloDetails[8], angleVeloDetails[9], angleVeloDetails[10], angleVeloDetails[11], angleVeloDetails[12], angleVeloDetails[13], angleVeloDetails[14], angleVeloDetails[15], angleVeloDetails[16], angleVeloDetails[17], angleVeloDetails[18], angleVeloDetails[19], angleVeloDetails[20], angleVeloDetails[21]])  # right click
                                            # empty x and y coordinates vectors
                                            del timeDatas[:]
                                            del xCoords[:]
                                            del yCoords[:]
                                            # reinitialize values
                                            rightPressed = 0
                                            rowCnt = 0
                                            rowCntWithoutDuplicates = 0
                                        else:
                                            # case left click
                                            if leftPressed == 1:
                                                # release coordinates append
                                                if float(row[4]) < st.upLim or float(row[5]) < st.upLim:
                                                    xCoords.append(float(row[4]))
                                                    yCoords.append(float(row[5]))
                                                    timeDatas.append(float(row[1]))

                                                if rowCntWithoutDuplicates > 4:
                                                    # distance and straightness
                                                    distanceDetails = cf.countMoveDistance(xCoords, yCoords)
                                                    # time
                                                    time = float(row[1]) - tmpStartTime
                                                    # direction
                                                    angleInRad = cf.countSumDirection(xCoords[0], yCoords[0], xCoords[-1], yCoords[-1])
                                                    # angle and speed datas (min, max, avg point by point)
                                                    angleVeloDetails = cf.pointSpeedAngleAcceleration(user, fileName, xCoords, yCoords, timeDatas, rowCntWithoutDuplicates)

                                                    # if(len(xCoords) != rowCntWithoutDuplicates):
                                                    #     print(user, fileName, len(xCoords), len(yCoords), len(timeDatas), rowCntWithoutDuplicates, tmpStartLine, allRows)

                                                    # append to csv file
                                                    writer.writerow([user, method, fileName, tmpStartLine, allRows, rowCnt, st.leftClick, distanceDetails[0], time, angleInRad, distanceDetails[1], angleVeloDetails[0], angleVeloDetails[1], angleVeloDetails[2], angleVeloDetails[3], angleVeloDetails[4], angleVeloDetails[5], angleVeloDetails[6], angleVeloDetails[7], angleVeloDetails[8], angleVeloDetails[9], angleVeloDetails[10], angleVeloDetails[11], angleVeloDetails[12], angleVeloDetails[13], angleVeloDetails[14], angleVeloDetails[15], angleVeloDetails[16], angleVeloDetails[17], angleVeloDetails[18], angleVeloDetails[19], angleVeloDetails[20], angleVeloDetails[21]])       #left click
                                                # empty x and y coordinates vectors
                                                del timeDatas[:]
                                                del xCoords[:]
                                                del yCoords[:]
                                                # reinitialize values
                                                leftPressed = 0
                                                rowCnt = 0
                                                rowCntWithoutDuplicates = 0
                                            else:
                                                # case left click drag
                                                if leftDrag == 1:
                                                    # release coordinates append
                                                    if float(row[4]) < st.upLim or float(row[5]) < st.upLim:
                                                        xCoords.append(float(row[4]))
                                                        yCoords.append(float(row[5]))
                                                        timeDatas.append(float(row[1]))

                                                    if rowCntWithoutDuplicates > 4:
                                                        # distance and straightness
                                                        distanceDetails = cf.countMoveDistance(xCoords, yCoords)
                                                        # time
                                                        time = float(row[1]) - tmpLeftDragStartTime
                                                        # direction
                                                        angleInRad = cf.countSumDirection(xCoords[0], yCoords[0], xCoords[-1], yCoords[-1])
                                                        # angle and speed datas (min, max, avg point by point)
                                                        # if (len(xCoords) != rowCntWithoutDuplicates):
                                                        #     print(user, fileName, len(xCoords), len(yCoords), len(timeDatas), rowCntWithoutDuplicates, tmpStartLine, allRows)

                                                        angleVeloDetails = cf.pointSpeedAngleAcceleration(user, fileName, xCoords, yCoords, timeDatas, rowCntWithoutDuplicates)
                                                        # append to csv file
                                                        writer.writerow([user, method, fileName, tmpStartLine, allRows, rowCnt, st.leftDrag, distanceDetails[0], time, angleInRad, distanceDetails[1], angleVeloDetails[0], angleVeloDetails[1], angleVeloDetails[2], angleVeloDetails[3], angleVeloDetails[4], angleVeloDetails[5], angleVeloDetails[6], angleVeloDetails[7], angleVeloDetails[8], angleVeloDetails[9], angleVeloDetails[10], angleVeloDetails[11], angleVeloDetails[12], angleVeloDetails[13], angleVeloDetails[14], angleVeloDetails[15], angleVeloDetails[16], angleVeloDetails[17], angleVeloDetails[18], angleVeloDetails[19], angleVeloDetails[20], angleVeloDetails[21]])    #left click drag
                                                    # empty x and y coordinates vectors
                                                    del timeDatas[:]
                                                    del xCoords[:]
                                                    del yCoords[:]
                                                    # reinitialize values
                                                    leftDrag = 0
                                                    rowCnt = 0
                                                    rowCntWithoutDuplicates = 0
                                                else:
                                                    # case right click drag
                                                    if rightDrag == 1:
                                                        # release coordinates append
                                                        if float(row[4]) < st.upLim or float(row[5]) < st.upLim:
                                                            xCoords.append(float(row[4]))
                                                            yCoords.append(float(row[5]))
                                                            timeDatas.append(float(row[1]))

                                                        if rowCntWithoutDuplicates > 4:
                                                            # distance and straightness
                                                            distanceDetails = cf.countMoveDistance(xCoords, yCoords)
                                                            # time
                                                            time = float(row[1]) - tmpRightDragStartTime
                                                            # direction
                                                            angleInRad = cf.countSumDirection(xCoords[0], yCoords[0], xCoords[-1], yCoords[-1])
                                                            # angle and speed datas (min, max, avg point by point)
                                                            angleVeloDetails = cf.pointSpeedAngleAcceleration(user, fileName, xCoords, yCoords, timeDatas, rowCntWithoutDuplicates)
                                                            # append to csv file
                                                            writer.writerow([user, method, fileName, tmpStartLine, allRows, rowCnt, st.rightDrag, distanceDetails[0], time, angleInRad, distanceDetails[1], angleVeloDetails[0], angleVeloDetails[1], angleVeloDetails[2], angleVeloDetails[3], angleVeloDetails[4], angleVeloDetails[5], angleVeloDetails[6], angleVeloDetails[7], angleVeloDetails[8], angleVeloDetails[9], angleVeloDetails[10], angleVeloDetails[11], angleVeloDetails[12], angleVeloDetails[13], angleVeloDetails[14], angleVeloDetails[15], angleVeloDetails[16], angleVeloDetails[17], angleVeloDetails[18], angleVeloDetails[19], angleVeloDetails[20], angleVeloDetails[21]]) #right click drag
                                                        # empty x and y coordinates vectors
                                                        del timeDatas[:]
                                                        del xCoords[:]
                                                        del yCoords[:]
                                                        # reinitialize values
                                                        rightDrag = 0
                                                        rowCnt = 0
                                                        rowCntWithoutDuplicates = 0
                                                    # case wrong value in state column ---> error?
                                                    else:
                                                        print(user, " ", fileName, " ", "--- no Press or Drag before Release?, rowCnt: ", rowCnt, " ; n-from: ", tmpStartLine, " ; n-to", allRows)
                                                        del timeDatas[:]
                                                        del xCoords[:]
                                                        del yCoords[:]

                                                        leftDrag = 0
                                                        leftPressed = 0
                                                        rightPressed = 0
                                                        rightDrag = 0
                                                        rowCnt = 0
                                                        rowCntWithoutDuplicates = 0
                                    if row[3] == 'Down' or row[3] == 'Up':
                                        rowCnt = rowCnt - 1
                                        rowCntWithoutDuplicates = rowCntWithoutDuplicates - 1


                        prevRow = row
    return

processCsv(st.method)

#method: 1 - train, 0 - test
