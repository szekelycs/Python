from tkinter import *
from PIL import ImageTk, Image
import pandas as pd
import os
import mousedynamics.utils.settings as st
import mousedynamics.classification.myClassifier as test
import numpy
import pickle
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

def getSessionPlot(event):
    session = sessionList.get(sessionList.curselection()[0])
    tmp = Image.open(st.testPlotsDir + session[2:] + '.png')
    img = tmp.resize((400, 300), Image.ANTIALIAS)
    phImg = ImageTk.PhotoImage(img)
    panel.configure(image=phImg)
    panel.image = phImg

def predict():
    user = userList.get('active')
    uNum = re.findall('\d+', user)[0]


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
                tmp = Image.open(st.positive)
                bgImg = tmp.resize((150, 50), Image.ANTIALIAS)
                phIm = ImageTk.PhotoImage(bgImg)
                belongImg.configure(image=phIm)
                belongImg.image = phIm
            else:
                tmp = Image.open(st.negative)
                bgImg = tmp.resize((150, 50), Image.ANTIALIAS)
                phIm = ImageTk.PhotoImage(bgImg)
                belongImg.configure(image=phIm)
                belongImg.image = phIm
            break

    return



def scale():
    global userList
    global sessionList

    global bgImg
    global phIm
    global belongImg


    global img
    global phImg
    global panel
    global thescale

    thescale=Tk()
    userScroll=Scrollbar(thescale)
    userScroll.pack(side='left', fill='y')

    sessionScroll = Scrollbar(thescale)
    sessionScroll.pack(side='left', fill='y')


    userList = Listbox(thescale, yscrollcommand = userScroll.set, exportselection = 0)
    sessionList = Listbox(thescale, yscrollcommand = sessionScroll.set, exportselection = 0)

    # T = Text(thescale, height=2, width=30)
    # T.pack(side='bottom')
    # T.insert(END, "Belongs to user?")

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



    tmp2 = Image.open(st.empty)
    bgImg = tmp2.resize((150, 50), Image.ANTIALIAS)
    phIm = ImageTk.PhotoImage(bgImg)
    belongImg = Label(thescale, image=phIm)
    belongImg.pack()

    calculateButton = Button(thescale, text="Calculate predictions", command=predict)
    calculateButton.pack(side='bottom', fill = X)

    tmp = Image.open(st.testPlotsDir + sessionList.get('active')[2:] + '.png')
    img = tmp.resize((400, 300), Image.ANTIALIAS)
    phImg = ImageTk.PhotoImage(img)
    panel = Label(thescale, image=phImg)
    panel.pack(side="right", fill="both", expand="no")



    userList.bind("<<ListboxSelect>>", getSessions)
    sessionList.bind("<<ListboxSelect>>", getSessionPlot)

    userList.pack(side='left', fill='both')
    userScroll.config(command=userList.yview)

    sessionList.pack(side='left', fill='both')
    sessionScroll.config(command=sessionList.xview)

    thescale.mainloop()

scale()