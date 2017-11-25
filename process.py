import csv
import settings as st

#csvOutHeaders = ["method", "user", "session", "n_from", "n_to", "rowcnt", "type_of_action", "sumdist", "elpstime", "direction", "straight", "angle", "velo", "avg_velo"]

def processCsv(fileName, method, user):

    with open(fileName) as csvInFile:
        with open("ma_" + fileName, "w+", newline='') as csvOutFile:
            writer = csv.writer(csvOutFile, delimiter=',')
            writer.writerow(st.csvOutHeaders)
            reader = csv.reader(csvInFile)
            session = fileName[:-4]

            rowCnt = 0;                             # starts counting at the beginning of mouse action
            leftPressed = 0                         # 1 - if left click is pressed # 0 - if no action with left button
            rightPressed = 0                        # 1 - if right click is pressed # 0 - if no action with right button
            leftDrag = 0                            # 1 - if left mb is clicked before drag # 0 - if no action with left button drag
            rightDrag = 0                           # 1 - if right mb is clicked before drag # 0 - if no action with right button drag
            tmpStartTime = 0                        # first parameter of csv row - value = start time of mouse action
            firstLine = True                        # first line of csv contains headers
            allRows = 1                             # contains the processed row number
            move = 0
            xCoords = []
            yCoords = []

            for row in reader:
                if firstLine:                       # skipping first line
                    firstLine = False
                    continue
                allRows = allRows + 1
                rowCnt = rowCnt + 1
                if rowCnt == 1:                     # save starting time and starting line
                    move = 0
                    tmpStartTime = float(row[0])
                    tmpStartLine = allRows


                if row[3] == 'Move':                # if the mouse action type is movement we check whether the time limit is exceeded or not
                    limit = tmpStartTime + 10
                    move = 1
                    if limit < float(row[1]):
                        move = 0
                        writer.writerow([method, user, session, tmpStartLine, allRows, rowCnt, st.mouseMove])                       #mouse move
                        rowCnt = 0  # else nothing happens
                else:
                    if row[3] == 'Pressed':
                        if row[2] == 'Left':
                            leftPressed = 1
                        else:
                            rightPressed = 1
                    else:
                        if row[3] == 'Drag':
                            if leftPressed == 1:
                                if move == 1:
                                    writer.writerow([method, user, session, tmpStartLine, allRows - 2, rowCnt - 2, st.mouseMove])           #mouse move
                                    move = 0
                                    rowCnt = 2
                                    tmpStartLine = allRows - 1
                                    leftDrag = 1
                                    leftPressed = 0
                                else:
                                    leftDrag = 1
                                    leftPressed = 0
                            else:
                                if rightPressed == 1:
                                    if move == 1:
                                        writer.writerow([method, user, session, tmpStartLine, allRows - 2, rowCnt - 2, st.mouseMove])       #mouse move
                                        rowCnt = 2
                                        tmpStartLine = allRows - 1
                                        rightDrag = 1
                                        rightPressed = 0
                                    else:
                                        rightDrag = 1
                                        rightPressed = 0

                        else:
                            if row[3] == 'Released':
                                if rightPressed == 1:
                                    writer.writerow([method, user, session, tmpStartLine, allRows, rowCnt, st.rightClick])  # right click
                                    rightPressed = 0
                                    rowCnt = 0
                                else:
                                    if leftPressed == 1:
                                        writer.writerow([method, user, session, tmpStartLine, allRows, rowCnt, st.leftClick])       #left click
                                        leftPressed = 0
                                        rowCnt = 0
                                    else:
                                        if leftDrag == 1:
                                            writer.writerow([method, user, session, tmpStartLine, allRows, rowCnt, st.leftDrag])    #left click drag
                                            leftDrag = 0
                                            rowCnt = 0
                                        else:
                                            if rightDrag == 1:
                                                writer.writerow([method, user, session, tmpStartLine, allRows, rowCnt, st.rightDrag])#right click drag
                                                rightDrag = 0
                                                rowCnt = 0
                                            else:
                                                print("No Press or Drag before Release?, rowCnt: ", rowCnt, " ; n-from: ", tmpStartLine, " ; n-to", allRows)

    print("All: ", allRows)
    return

processCsv('session_2144641057.csv', 'train', 'user12')


    #import pandas as pd
    #actiondata = pd.read_csv(st.ACTION_FILENAME)
    #actiontype = actiondata['type_of_action']

    #dataset = pd.read_csv(feature_filename)
    # ends with class,session,n_from,n_to
    #numFeatures = int(dataset.shape[1]) - 3  ---- shape[0] sorok szama, shape[1] oszlopok szama
    #classes = dataset.groupby('class')

    #ket egymast koveto sor teljesen megegyezik - kiszurni