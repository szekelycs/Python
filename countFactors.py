import csv
import math
# import scipy

# TODO: pontonkenti sebesseg, pontonkenti szog: min, max, atlag
# TODO: download 2016/2017 microsoft office

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


def pointSpeedAngle(xCoords, yCoords, timeDatas):
    pointDatas = [None] * 10

    firstLine = True
    prevX = 0
    prevY = 0
    minAngle = 100000
    maxAngle = -100000
    minSpeed = 100000
    maxSpeed = -100000
    sumAngle = 0
    n = 0
    for x, y, t in zip(xCoords, yCoords, timeDatas):
        n+=1
        if firstLine == True:
            firstLine = False
            prevX = x
            prevY = y
            prevT = t
            continue

        # calculating angle between two dots - comparing to max and min values and reinitialize if needed
        angle = math.atan2(prevY - y, prevX - x)
        if angle < minAngle:
            minAngle = angle
        if angle > maxAngle:
            maxAngle = angle
        sumAngle += angle

        prevX = x
        prevY = y
        prevT = t

    pointDatas[0] = minAngle
    pointDatas[1] = maxAngle
    pointDatas[2] = sumAngle/n
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