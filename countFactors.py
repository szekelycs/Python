import csv
import math
# import scipy

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
    w = []

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
        angles.append(math.atan2(prevY - y, prevX - x))

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

        if secondLine == False:
            prevVelo = 0
            if tmpTime != 0:
                prevVelo = velo[-1]
        prevX = x
        prevY = y
        prevT = t



    pointDatas[0] = min(angles)
    pointDatas[1] = max(angles)
    if (len(angles) == 0):
        pointDatas[2] = 0
    else:
        pointDatas[2] = sum(angles) / len(angles)


    pointDatas[3] = min(veloX)
    pointDatas[4] = max(veloX)
    if (len(veloX) == 0):
        pointDatas[5] = 0
    else:
        pointDatas[5] = sum(veloX) / len(veloX)


    pointDatas[6] = min(veloY)
    pointDatas[7] = max(veloY)
    if (len(veloY) == 0):
        pointDatas[8] = 0
    else:
        pointDatas[8] = sum(veloY) / len(veloY)

    pointDatas[9] = min(velo)
    pointDatas[10] = max(velo)
    if (len(velo) == 0):
        pointDatas[11] = 0
    else:
        pointDatas[11] = sum(velo) / len(velo)

    pointDatas[12] = min(acc)
    pointDatas[13] = max(acc)
    if (len(acc) == 0):
        pointDatas[14] = 0
    else:
        pointDatas[14] = sum(acc) / len(acc)

    pointDatas[15] = min(w)
    pointDatas[16] = max(w)
    if (len(w) == 0):
        pointDatas[17] = 0
    else:
        pointDatas[17] = sum(w) / len(w)

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