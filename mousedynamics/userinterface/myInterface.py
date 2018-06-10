from tkinter import *
import pandas as pd
import os
import mousedynamics.utils.settings as st
import mousedynamics.classification.myClassifier as test
import numpy
# from tkinter import Tk, Listbox, Button, Scrollbar

def getSessions(event):
    sessionList.delete(0, END)
    user = userList.get(userList.curselection()[0])
    fUNumber = re.findall('\d+', user)[0]


    for dirname, dirnames, filenames in os.walk(st.legalOpDir):
        for dir in dirnames:
            if dir == fUNumber:
                for dirname2, dirnames2, filenames2 in os.walk(st.legalOpDir + fUNumber):
                    for file in filenames2:
                        sessionList.insert(END, "L " + file)

    for dirname, dirnames, filenames in os.walk(st.illegalOpDir):
        for dir in dirnames:
            if dir == fUNumber:
                for dirname2, dirnames2, filenames2 in os.walk(st.illegalOpDir + fUNumber):
                    for file in filenames2:
                        sessionList.insert(END, "I " + file)

def predict():
    user = userList.get('active')
    uNum = re.findall('\d+', user)[0]
    T.delete('1.0', END)

    session = sessionList.get('active')

    sessionFileName = session[2:]
    if session[0] == 'L':
        legality = 1
    else:
        legality = 0

    predictions = test.testForUI(uNum, session, legality)

    thDataset = pd.read_csv(st.workDir+st.thresholdFile)

    thresholds = thDataset.values

    for i in thresholds:
        if i[0] == int(uNum):
            if numpy.mean(predictions[:,1]) > i[1]:
                T.insert(END, 'YES')
            else:
                T.insert(END, 'NO')
            break

    return



def scale():
    global userList
    global sessionList
    global T

    thescale=Tk()
    userScroll=Scrollbar(thescale)
    userScroll.pack(side='left', fill='y')

    sessionScroll = Scrollbar(thescale)
    sessionScroll.pack(side='right', fill='y')


    userList = Listbox(thescale, yscrollcommand = userScroll.set, exportselection = 0)
    sessionList = Listbox(thescale, yscrollcommand = sessionScroll.set, exportselection = 0)


    T = Text(thescale, height=2, width=30)
    T.pack()
    T.insert(END, "Belongs to user?")

    for dirname, dirnames, filenames in os.walk(st.classificationDir):
         for fileName in filenames:
             user = re.findall('\d+', fileName)[0]
             userList.insert(END, "User " + user)

    user = userList.get('active')
    fUNumber = re.findall('\d+', user)[0]

    for dirname, dirnames, filenames in os.walk(st.legalOpDir):
        for dir in dirnames:
            if dir == fUNumber:
                for dirname2, dirnames2, filenames2 in os.walk(st.legalOpDir + fUNumber):
                    for file in filenames2:
                        sessionList.insert(END, "L " + file)

    for dirname, dirnames, filenames in os.walk(st.illegalOpDir):
        for dir in dirnames:
            if dir == fUNumber:
                for dirname2, dirnames2, filenames2 in os.walk(st.illegalOpDir + fUNumber):
                    for file in filenames2:
                        sessionList.insert(END, "I " + file)

    sessionList.pack(side='right', fill='both')
    sessionScroll.config(command=sessionList.xview)

    userList.bind("<<ListboxSelect>>", getSessions)

    userList.pack(side='left', fill='both')
    userScroll.config(command=userList.yview)

    # refreshButton=Button(thescale, text="Refresh sessions", command=getSessions)
    # refreshButton.pack()



    calculateButton = Button(thescale, text="Calculate predictions", command=predict)
    calculateButton.pack()


    thescale.mainloop()

scale()