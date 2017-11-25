import matplotlib.pyplot as plt
import csv

def plotmouseaction(rowStart, rowFinish, fileName, type):
    with open(fileName) as csvfile:
        xCoords = []
        yCoords = []
        reader = csv.reader(csvfile)
        rows = [r for r in reader]
        for i in range(rowStart-1, rowFinish):
            print(rows[i])
            xCoords.append(float(rows[i][4]))
            yCoords.append(float(rows[i][5]))

        if type == 'mm':
            plt.plot(xCoords, yCoords, linestyle='-', linewidth=0.5, markersize=3, color='red', marker='*')
            plt.axis([0, 2100, 0, 1200])
        else:
            if type == 'lc':
                plt.plot(xCoords, yCoords, linestyle='-', linewidth=0.5, markersize=3, color='blue', marker='o')
                plt.axis([0, 2100, 0, 1200])
            else:
                if type == 'rc':
                    plt.plot(xCoords, yCoords, linestyle='-', linewidth=0.5, markersize=3, color='green', marker='.')
                    plt.axis([0, 2100, 0, 1200])
                else:
                    if type == 'ld':
                        plt.plot(xCoords, yCoords, linestyle='-', linewidth=0.5, markersize=3, color='black', marker='^')
                        plt.axis([0, 2100, 0, 1200])
                    else:
                        if type == 'rd':
                            plt.plot(xCoords, yCoords, linestyle='-', linewidth=0.5, markersize=3, color='magenta', marker='8')
                            plt.axis([0, 2100, 0, 1200])
        del xCoords[:]
        del yCoords[:]
        plt.show()


plotmouseaction(2, 83, 'session_2144641057.csv', 'mm')
#plotmouseaction(29679, 29693, 'session_2144641057.csv', 'lc')
#plotmouseaction(9879, 9890, 'session_2144641057.csv', 'rc')
# plotmouseaction(119, 125, 'session_2144641057.csv', 'ld')



