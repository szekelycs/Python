import csv
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import settings as st
import countFactors as cf

# a hashmark-al elvalasztott reszek a kirajzolashoz szuksegesek - a 2500-nal nagyobb koordinatakat kiszurjuk
######################
######################
######################

def processCsv(fileName):

    with open(fileName) as csvfile:
        reader = csv.reader(csvfile)

        rowCnt = 0;                             # starts counting at the beginning of mouse action
        leftPressed = 0                         # 1 - if left click is pressed # 0 - if no action with left button
        rightPressed = 0                        # 1 - if right click is pressed # 0 - if no action with right button
        leftDrag = 0                            # 1 - if left mb is clicked before drag # 0 - if no action with left button drag
        rightDrag = 0                           # 1 - if right mb is clicked before drag # 0 - if no action with right button drag
        tmpStartTime = 0                        # first parameter of csv row - value = start time of mouse action
        firstLine = True                        # first line of csv contains headers
        allRows = 1                             # contains the processed row number

        xCoords = []                            # necessary at plotting - contains the x coords of the mouse position
        yCoords = []                            # necessary at plotting - contains the y coords of the mouse position

        mm = mpatches.Patch(color='red', label='Mouse Move - MM')
        rc = mpatches.Patch(color='black', label='Right Click - RC')
        lc = mpatches.Patch(color='yellow', label='Left Click - LC')
        ld = mpatches.Patch(color='green', label='Left Click Drag - LD')
        # rd = mpatches.Patch(color='magenta', label='Right Click Drag - RD')

        plt.legend(handles=[mm, rc, lc, ld])


        # handles = []
        # if st.leftClickOnly == 1:
        #     handles.append(lc)
        #
        # plt.legend(handles)

        for row in reader:
            if firstLine:                       # skipping first line
                firstLine = False
                continue
            allRows = allRows + 1
            rowCnt = rowCnt + 1
            if rowCnt == 1:                     # save starting time and starting line
                tmpStartTime = float(row[0])
                tmpStartLine = allRows

            if row[3] == 'Move':
                limit = tmpStartTime + 10

                if float(row[4]) < 2500 or float(row[5]) < 2500:
                    xCoords.append(float(row[4]))
                    yCoords.append(float(row[5]))

                if limit < float(row[1]):
                    #print("Action - MOVE, rowcount: ", rowCnt, " ; n-from: ", tmpStartLine, " ; n-to: ", allRows)
                    rowCnt = 0  # else nothing happens
                    if st.moveOnly == 1:
                        plt.plot(xCoords, yCoords, linestyle='-', color='red', markersize=0.8, linewidth=0.1, marker='.')
                    del xCoords[:]
                    del yCoords[:]
            else:
                if row[3] == 'Pressed':
                    if row[2] == 'Left':
                        leftPressed = 1
                        dragStartX = float(row[4])
                        dragStartY = float(row[5])
                        if st.leftClickOnly == 1:
                            if float(row[4]) < 2500 or float(row[5]) < 2500:
                                xCoords.append(float(row[4]))
                                yCoords.append(float(row[5]))
                    else:
                        if row[2] == 'Right':
                            rightPressed = 1
                            dragStartX = float(row[4])
                            dragStartY = float(row[5])
                            if st.rightClickOnly:
                                if float(row[4]) < 2500 or float(row[5]) < 2500:
                                    xCoords.append(float(row[4]))
                                    yCoords.append(float(row[5]))
                else:
                    if row[3] == 'Drag':
                        if leftPressed == 1:
                            #print("Action - MOVE, rowcount: ", rowCnt - 2, " ; n-from: ", tmpStartLine, " ; n-to", allRows - 2)
                            rowCnt = 2
                            tmpStartLine = allRows - 1
                            leftDrag = 1
                            leftPressed = 0

                            if st.moveOnly == 1:
                                plt.plot(xCoords, yCoords, linestyle='-', linewidth=0.1, markersize=0.8, color='red', marker='.')
                            del xCoords[:]
                            del yCoords[:]

                        if leftDrag == 1:
                            if st.dragOnly == 1:
                                if float(row[4]) < 2500 or float(row[5]) < 2500:
                                    if rowCnt == 2:
                                        xCoords.append(dragStartX)
                                        yCoords.append(dragStartY)
                                        dragStartX = 0
                                        dragStartY = 0
                                    xCoords.append(float(row[4]))
                                    yCoords.append(float(row[5]))
                        else:
                            if rightPressed == 1:
                                #print("Action - MOVE, rowcount: ", rowCnt - 2, " ; n-from: ", tmpStartLine, " ; n-to", allRows - 2)
                                rowCnt = 2
                                tmpStartLine = allRows - 1
                                rightDrag = 1
                                rightPressed = 0

                                if st.moveOnly == 1:
                                    plt.plot(xCoords, yCoords, linestyle='-', linewidth=0.1, markersize=0.8, color='red', marker='.')
                                del xCoords[:]
                                del yCoords[:]

                            if rightDrag == 1:
                                if st.dragOnly == 1:
                                    if float(row[4]) < 2500 or float(row[5]) < 2500:
                                        if rowCnt == 2:
                                            xCoords.append(dragStartX)
                                            yCoords.append(dragStartY)
                                            dragStartX = 0
                                            dragStartY = 0
                                        xCoords.append(float(row[4]))
                                        yCoords.append(float(row[5]))
                    else:
                        if row[3] == 'Released':
                            if rightPressed == 1:
                                rightPressed = 0
                                #print("Action - RIGHT CLICK, rowcount: ", rowCnt, " ; n-from: ", tmpStartLine, " ; n-to", allRows)
                                rowCnt = 0

                                if st.rightClickOnly == 1:
                                    plt.plot(xCoords, yCoords, linestyle='-', color='black', linewidth=0.1, markersize=0.8, marker='.')
                                del xCoords[:]
                                del yCoords[:]
                            else:
                                if leftPressed == 1:
                                    leftPressed = 0
                                    #print("Action - LEFT CLICK, rowcount: ", rowCnt, " ; n-from: ", tmpStartLine, " ; n-to", allRows)
                                    rowCnt = 0

                                    if st.leftClickOnly == 1:
                                        plt.plot(xCoords, yCoords, linestyle='-', color='yellow', linewidth=0.1, markersize=0.8, marker='.')
                                    del xCoords[:]
                                    del yCoords[:]
                                else:
                                    if leftDrag == 1:
                                        leftDrag = 0
                                        #print("Action - LEFT CLICK DRAG, rowcount: ", rowCnt, " ; n-from: ", tmpStartLine, " ; n-to", allRows)
                                        rowCnt = 0

                                        if st.dragOnly == 1:
                                            plt.plot(xCoords, yCoords, linestyle='-', color='green', linewidth=0.1, markersize=0.8, marker='.')
                                        del xCoords[:]
                                        del yCoords[:]
                                    else:
                                        if rightDrag == 1:
                                            rightDrag = 0
                                            #print("Action - RIGHT CLICK DRAG, rowcount: ", rowCnt, " ; n-from: ", tmpStartLine, " ; n-to", allRows)
                                            rowCnt = 0

                                            if st.dragOnly == 1:
                                                plt.plot(xCoords, yCoords, linestyle='-', color='magenta', linewidth=0.1, markersize=0.8, marker='.')
                                            del xCoords[:]
                                            del yCoords[:]
                                        else:
                                            print("No Press or Drag before Release?, rowCnt: ", rowCnt, " ; n-from: ", tmpStartLine, " ; n-to", allRows)
        print("All: ", allRows)
        plt.show()
        return

processCsv('session_2144641057.csv')


#import pandas as pd
#actiondata = pd.read_csv(st.ACTION_FILENAME)
#actiontype = actiondata['type_of_action']

#dataset = pd.read_csv(feature_filename)
# ends with class,session,n_from,n_to
#numFeatures = int(dataset.shape[1]) - 3  ---- shape[0] sorok szama, shape[1] oszlopok szama
#classes = dataset.groupby('class')

#ket egymast koveto sor teljesen megegyezik - kiszurni