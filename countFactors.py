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
    prevX = 0
    prevY = 0
    minAngle = 100000
    maxAngle = -100000
    sumAngle = 0

    minAcc = 100000
    maxAcc = -100000
    sumAcc = 0

    minVelo = minVeloX = minVeloY = 100000
    maxVelo = maxVeloX = maxVeloY = -100000
    sumVelo = sumVeloX = sumVeloY = 0
    m = n
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
        if tmpTime == 0:
            m = m - 1
        else:
            tmpVeloX = abs(tmpDistanceX/tmpTime)
            if tmpVeloX < minVeloX:
                minVeloX = tmpVeloX
            if tmpVeloX > maxVeloX:
                maxVeloX = tmpVeloX
            sumVeloX += tmpVeloX

            tmpVeloY = abs(tmpDistanceY/tmpTime)
            if tmpVeloY < minVeloY:
                minVeloY = tmpVeloY
            if tmpVeloY > maxVeloY:
                maxVeloY = tmpVeloY
            sumVeloY += tmpVeloY

            tmpVelo = math.sqrt(tmpVeloX ** 2 + tmpVeloY ** 2)
            if tmpVelo < minVelo:
                minVelo = tmpVelo
            if tmpVelo > maxVelo:
                maxVelo = tmpVelo
            sumVelo += tmpVelo

        # calculating angle between two dots - comparing to max and min values and reinitialize if needed
        angle = math.atan2(prevY - y, prevX - x)
        if angle < minAngle:
            minAngle = angle
        if angle > maxAngle:
            maxAngle = angle
        sumAngle += angle

        if firstLine == False and secondLine == True:
            secondLine = False
            prevVelo = 0
            if tmpTime != 0:
                prevVelo = tmpVelo
            continue

        if tmpTime != 0:
            tmpAcc = (prevVelo - tmpVelo)/tmpTime;
            if tmpAcc < minAcc:
                minAcc = tmpAcc
            if tmpAcc > maxAcc:
                maxAcc = tmpAcc
            sumAcc += tmpAcc

        if secondLine == False:
            prevVelo = 0
            if tmpTime != 0:
                prevVelo = tmpVelo
        prevX = x
        prevY = y
        prevT = t

    if minAngle == 100000 or minVeloX == 100000 or minVeloY == 100000 or minAcc == 100000:
        print(user + " " + fileName + " ")
        print(xCoords)
        print(yCoords)

        print(timeDatas)
        print(pointDatas)

    pointDatas[0] = minAngle
    pointDatas[1] = maxAngle
    pointDatas[2] = sumAngle/n

    pointDatas[3] = minVeloX
    pointDatas[4] = maxVeloX
    if m == 0:
        pointDatas[5] = 0
    else:
        pointDatas[5] = sumVeloX / m


    pointDatas[6] = minVeloY
    pointDatas[7] = maxVeloY
    if m == 0:
        pointDatas[8] = 0
    else:
        pointDatas[9] = sumVeloY / m


    pointDatas[10] = minVelo
    pointDatas[11] = maxVelo
    if m == 0:
        pointDatas[12] = 0
    else:
        pointDatas[13] = sumVelo/m


    pointDatas[14] = minAcc
    pointDatas[15] = maxAcc
    if m == 0:
        pointDatas[16] = 0
    else:
        pointDatas[17] = sumAcc/m

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