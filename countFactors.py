import csv
import math
import scipy
import numpy

def countMoveDistance(xCoords, yCoords):
    distanceDetails = [None]*2
    distanceDetails[0] = 0
    distanceDetails[1] = 0
    firstElement = True

    prevX = 0
    prevY = 0
    for x, y in zip(xCoords, yCoords):
        if firstElement == True:
            firstElement = False
            prevX = x
            prevY = y
            continue

        distanceDetails[0] += math.sqrt((x - prevX) ** 2 + (y - prevY) ** 2)
        prevX = x;
        prevY = y;

    if len(xCoords) > 1:
        directLength = (math.sqrt((xCoords[-1] - xCoords[0]) ** 2 + (yCoords[-1] - yCoords[0]) ** 2))
        if directLength != 0:
            distanceDetails[1] = directLength/(distanceDetails[0])
        else:
            distanceDetails[1] = 0

    return distanceDetails

def pointSpeedAngleAcceleration(user, fileName, xCoords, yCoords, timeDatas, n):
    pointDatas = [None] * 23

    firstLine = secondLine = True

    acc = []
    angles = []
    veloX = []
    veloY = []
    velo = []
    jerk = []
    w = []
    # print(len(xCoords), " ", len(yCoords), " ", len(timeDatas))
    for x, y, t in zip(xCoords, yCoords, timeDatas):

        if firstLine == True:
            firstLine = False
            prevX = x
            prevY = y
            prevT = t
            continue

        tmpDistanceX = x - prevX
        tmpDistanceY = y - prevY
        tmpTime = t - prevT

        # calculating angle between two dots - comparing to max and min values and reinitialize if needed
        angles.append(math.degrees(math.atan2(prevY - y, prevX - x)))

        if tmpTime == 0:
            continue
        else:
            veloX.append(abs(tmpDistanceX/tmpTime))

            veloY.append(abs(tmpDistanceY/tmpTime))

            velo.append(math.sqrt(veloX[-1] ** 2 + veloY[-1] ** 2))

            w.append((angles[-1]/tmpTime))

        if firstLine == False and secondLine == True:
            secondLine = False
            prevVelo = 0
            if tmpTime != 0:
                prevVelo = velo[-1]
            continue

        if tmpTime != 0:
            acc.append((prevVelo - velo[-1])/tmpTime)
            jerk.append(acc[-1]/tmpTime)

        if secondLine == False:
            prevVelo = 0
            if tmpTime != 0:
                prevVelo = velo[-1]
        prevX = x
        prevY = y
        prevT = t




    if (len(angles) == 0):
        pointDatas[0] = 0
        pointDatas[1] = 0
        pointDatas[2] = 0
        pointDatas[21] = 0
    else:
        pointDatas[0] = numpy.std(angles)
        pointDatas[1] = max(angles)
        pointDatas[2] = numpy.mean(angles)
        pointDatas[21] = sum(angles)

    if (len(veloX) == 0):
        pointDatas[3] = 0
        pointDatas[4] = 0
        pointDatas[5] = 0
    else:
        pointDatas[3] = numpy.std(veloX)
        pointDatas[4] = max(veloX)
        pointDatas[5] = numpy.mean(veloX)

    if (len(veloY) == 0):
        pointDatas[6] = 0
        pointDatas[7] = 0
        pointDatas[8] = 0
    else:
        pointDatas[6] = numpy.std(veloY)
        pointDatas[7] = max(veloY)
        pointDatas[8] = numpy.mean(veloY)

    if (len(velo) == 0):
        pointDatas[9] = 0
        pointDatas[10] = 0
        pointDatas[11] = 0
    else:
        pointDatas[9] = numpy.std(velo)
        pointDatas[10] = max(velo)
        pointDatas[11] = numpy.mean(velo)
    if (len(acc) == 0):
        pointDatas[14] = 0
        pointDatas[12] = 0
        pointDatas[13] = 0
    else:
        pointDatas[12] = numpy.std(acc)
        pointDatas[13] = max(acc)
        pointDatas[14] = numpy.mean(acc)

    if (len(w) == 0):
        pointDatas[15] = 0
        pointDatas[16] = 0
        pointDatas[17] = 0
    else:
        pointDatas[15] = numpy.std(w)
        pointDatas[16] = max(w)
        pointDatas[17] = numpy.mean(w)

    if (len(jerk)) == 0:
        pointDatas[18] = 0
        pointDatas[19] = 0
        pointDatas[20] = 0
    else:
        pointDatas[18] = numpy.std(jerk)
        pointDatas[19] = max(jerk)
        pointDatas[20] = numpy.std(jerk)

    return pointDatas

def countSumDirection(xStart, yStart, xEnd, yEnd):
    y = yEnd - yStart
    x = xEnd - xStart
    angle = math.atan2(y, x)
    direction = 0

    if angle >= 0 and angle <= math.pi/4:
        direction = 1
    else:
        if angle > math.pi/4 and angle <= math.pi/2:
            direction = 2
        else:
            if angle > math.pi/2 and angle <= 3*math.pi/4:
                direction = 3
            else:
                if angle > 3*math.pi/4 and angle <= math.pi:
                    direction = 4
                else:
                    if angle >= -math.pi and angle <= -(3*math.pi/4):
                        direction = 5
                    else:
                        if angle > -(3*math.pi/4) and angle <= -math.pi/2:
                            direction = 6
                        else:
                            if angle > -math.pi/2 and angle <= -math.pi/4:
                                direction = 7
                            else:
                                if angle > -math.pi/4 and math.pi < 0:
                                    direction = 8

    return direction