import matplotlib.pyplot as plt
import mousedynamics.utils.settings as st
import matplotlib.patches as mpatches
import csv

def plotmouseaction(rowStart, rowFinish, fileName, type):
    with open(fileName) as csvfile:

        xCoords = []
        yCoords = []
        Txt = []

        reader = csv.reader(csvfile)
        rows = [r for r in reader]
        mm = mpatches.Patch(color=st.colorMM, label='Mouse Move - MM')
        rc = mpatches.Patch(color=st.colorRC, label='Right Click - RC')
        lc = mpatches.Patch(color=st.colorLC, label='Left Click - LC')
        ld = mpatches.Patch(color=st.colorDD, label='Left Click Drag - LD')

        k = 1
        for i in range(rowStart-1, rowFinish):
            print(rows[i])
            xCoords.append(float(rows[i][4]))
            yCoords.append(float(rows[i][5]))
            Txt.append('P' + str(k))
            k = k + 1


        if type == 'mm':
            plt.plot(xCoords, yCoords, linestyle='-', linewidth=0.5, markersize=3, color= st.colorMM, marker='*')
            plt.axis([0, 2100, 0, 1200])

            for i, txt in enumerate(Txt):
                plt.annotate(txt, (xCoords[i], yCoords[i]))
        else:
            if type == 'lc':
                plt.plot(xCoords, yCoords, linestyle='-', linewidth=0.5, markersize=3, color=st.colorLC, marker='o')
                plt.axis([0, 2100, 0, 1200])
                for i, txt in enumerate(Txt):
                    plt.annotate(txt, (xCoords[i], yCoords[i]))
            else:
                if type == 'rc':
                    plt.plot(xCoords, yCoords, linestyle='-', linewidth=0.5, markersize=3, color=st.colorRC, marker='.')
                    plt.axis([0, 2100, 0, 1200])
                    for i, txt in enumerate(Txt):
                        plt.annotate(txt, (xCoords[i], yCoords[i]))
                else:
                    if type == 'ld':
                        plt.plot(xCoords, yCoords, linestyle='-', linewidth=0.5, markersize=3, color=st.colorDD, marker='^')
                        plt.axis([0, 2100, 0, 1200])
                        for i, txt in enumerate(Txt):
                            plt.annotate(txt, (xCoords[i], yCoords[i]))
        if type == 'mm':
            plt.legend(handles=[mm])
        else:
            if type == 'lc':
                plt.legend(handles=[lc])
            else:
                if type == 'rc':
                    plt.legend(handles=[rc])
                else:
                    if type == 'ld':
                        plt.legend(handles=[ld])
                    else:
                        print('Action type error')

        del xCoords[:]
        del yCoords[:]
        plt.show()


# plotmouseaction(2, 82, 'session_2144641057.csv', 'mm')
# plotmouseaction(29679, 29690, 'session_2144641057.csv', 'lc')
# plotmouseaction(9879, 9890, 'session_2144641057.csv', 'rc')
# plotmouseaction(955, 977, 'session_2144641057.csv', 'ld')



