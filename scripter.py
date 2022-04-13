import os
import keyboard
import mouse
import time
import threading
import pickle
import os
import shutil
from tkinter import *
#create necessary folder for saving macros
savedscriptsFolder=os.getcwd()+'/savedscripts'
if os.path.isdir(savedscriptsFolder)==False:
    os.mkdir(savedscriptsFolder)
#some defaults
recordKeybind='f'
playKeybind='g'
global currentMacroName
currentMacroName='unnamed'
currentPath=os.getcwd()
mouseEvents=[]
keyboardEvents=[]
savedMacros=os.listdir(currentPath+'/savedscripts')
hours=0
minutes=0
seconds=0
finishedPlaying=True
isPlayingWithTimer=False
#---USEFUL FUNCTIONS---
#---START COPYING FROM codegrepper.com
def convert(seconds):
    seconds = seconds % (24 * 3600)
    hour = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60      
    return hour, minutes, seconds
#---FINISH COPYING FROM codegrepper.com            
#---PLAY AND RECORD FUNCTIONS---
#move event=first is a int
#button event=first is a string
#wheel event=first is a float

def playMouse(mouseEvents):
    global start
    _start=time.time()
    i=0
    while True:
        if i==len(mouseEvents):
           # print(len(mouseEvents))
           # print(i)
            break
        mouseEvent=mouseEvents[i]
        _time=time.time()-_start
        #if event is mouse move
        if isinstance(mouseEvent[0], int)and isinstance(mouseEvent[1], int):
            #move mouse
            timeOfEvent=mouseEvent[2]
            if(_time>timeOfEvent-start):
               # print(str(i)+"move"+"time: "+str(_time)+" event time: "+ str(timeOfEvent-start)+str(mouseEvent))
                i=i+1
                mouse.move(mouseEvent[0], mouseEvent[1])
        if isinstance(mouseEvent[0], str):
            #click mouse
            timeOfEvent=mouseEvent[2]
            #[0]='event_type' --down,up
            #[0]=--left,right
            if(_time>timeOfEvent-start):
               # print(str(i)+"click"+"time: "+str(_time)+" event time: "+ str(timeOfEvent-start)+str(mouseEvent))
                #print(mouseEvent[1])
                i=i+1
                if(mouseEvent[0]=='down'):
                    mouse.press(mouseEvent[1])
                elif(mouseEvent[0]=="up"):
                    mouse.release(mouseEvent[1])
                elif(mouseEvent[0]=="double"): mouse.double_click(mouseEvent[1])
        if isinstance(mouseEvent[0], float):
            #scroll wheel
            timeOfEvent=mouseEvent[1]
            if(_time>timeOfEvent-start):
                #print("wheel"+"time: "+str(_time)+" event time: "+ str(timeOfEvent-start)+str(mouseEvent))
                mouse.wheel(mouseEvent[0])
                i=i+1


    
#time.sleep(1)
#print("press the keybind for recording/stopping the script")
#recordKeybind = keyboard.read_key()
#print("keybind setted successfully")
#time.sleep(1)
#print("press the keybind for playing the script")
#playKeybind = keyboard.read_key()
#print("keybind setted successfully")
#time.sleep(1)
def _record():
    #status PORCODDIO DICO CHE SON QUA
    print('recording...')
    #global var
    global start
    global keyboardEvents
    global mouseEvents
    start=time.time()

    mouse.hook(mouseEvents.append)
    keyboard.start_recording()       #Starting the recording

    keyboard.wait(recordKeybind)

    mouse.unhook(mouseEvents.append)
    keyboardEvents = keyboard.stop_recording()  #Stopping the recording. Returns list of events

    #print("recorded. press "+str(playKeybind)+" to play the recorded script")
    print("finished recording script succesfully!")
    updateWindow()

def _play():
    #global var
    global currentMacroName
    global isPlayingWithTimer
    global finishedPlaying
    global start
    global keyboardEvents
    global mouseEvents
    #status PORCODDIO DICO CHE SON QUA
    print(mouseEvents, keyboardEvents)
    print('playing'+currentMacroName)
    print(keyboardEvents)
    print(mouseEvents)
    #Keyboard threadings:

    k_thread = threading.Thread(target = lambda :keyboard.play(keyboardEvents))
    k_thread.start()

    #Mouse threadings:

    m_thread = threading.Thread(target = lambda :playMouse(mouseEvents))
    m_thread.start()

    #waiting for both threadings to be completed

    k_thread.join() 
    m_thread.join()
    finishedPlaying=True
    print('finished playing script succesfully!')
    if isPlayingWithTimer==False:
        updateWindow()
    




    
#---END TIMER FUNCTION
#--READ, SAVE, DELETE MACRO FUNCTIONS---
def readMacro(macroName):
    global start
    global keyboardEvents
    global mouseEvents
    macroName=macroName.strip()
    #check if macro exists
    isAMacro=False
    for i in range(len(savedMacros)):
        if macroName==savedMacros[i]:
            isAMacro=True
    if isAMacro==True:
        #get keyboard and mouse files
        file1=currentPath+"/savedscripts/"+macroName+'/keyboardevents.pk1'
        file2=currentPath+"/savedscripts/"+macroName+'/mouseevents.pk1'
        file3=currentPath+"/savedscripts/"+macroName+'/timerstart.txt'
        #get the arrays of objects
        with open(file1, 'rb') as inp:
            keyboardEvents = pickle.load(inp)
        with open(file2, 'rb') as inp:
            mouseEvents = pickle.load(inp)
        #get timer start of macro
        timerstartfile = open(file3,"r")
        start=timerstartfile.read()
        start=float(start)
        timerstartfile.close()
        return start, mouseEvents, keyboardEvents

def saveMacro(macroName):
    global start
    global keyboardEvents
    global mouseEvents
    macroName=macroName.strip()
    #check if macro with same name already exists
    alreadyExists=False
    for i in range(len(savedMacros)):
        if macroName==savedMacros[i]:
            alreadyExists=True
    if(alreadyExists==False):
        #create folder
        path=os.path.join(currentPath+'/savedscripts',macroName)
        os.mkdir(path)
        #create files
        file1 = str(path)+'/keyboardevents.pk1'
        open(file1, 'a').close()
        file2 =str(path)+'/mouseevents.pk1'
        open(file2, 'a').close()
        file3 =str(path)+'/timerstart.txt'
        open(file3, 'a').close()
        #write keyboard events and mouse events
        with open(file1, 'wb') as outp:
            pickle.dump(keyboardEvents, outp, pickle.HIGHEST_PROTOCOL)
        with open(file2, 'wb') as outp:
            pickle.dump(mouseEvents, outp, pickle.HIGHEST_PROTOCOL)
        #save the start time of mouse recordings
        timerstartfile = open(file3,"a")
        timerstartfile.write(str(start))
        timerstartfile.close()
def deleteMacro(macroName):
    macroName=macroName.strip()
    #check if macro exists
    for i in range(len(savedMacros)):
        print(savedMacros[i])
        isAMAcro=False
        print('macroname: '+macroName+'filename: '+savedMacros[i])
        if macroName==savedMacros[i]:
            isAMAcro=True
            break
    print(isAMAcro)
    if isAMAcro==True:
        shutil.rmtree(currentPath+'/savedscripts/'+macroName)

#useful function for tkinter GUI setup
def setRecordKey():
    global recordKeyButton
    global recordKeybind
    recordKeybind=keyboard.read_key()
    recordKeyButton.configure(text=recordKeybind)
def setPlayKey():
    global playKeyButton
    global playKeybind
    playKeybind=keyboard.read_key()
    playKeyButton.configure(text=playKeybind)
def setCurrentMacro(macroName):
    macroName=macroName.strip()
    global currentMacroLbl1
    #check if macro exists
    isAMacro=False
    for i in range(len(savedMacros)):
        if macroName==savedMacros[i]:
            isAMacro=True
    if isAMacro==True:
        global currentMacroName
        currentMacroName=macroName
        currentMacroLbl1.configure(text=macroName)
    readMacro(currentMacroName)

def _start():
    while True:
        readKey=keyboard.read_key()
        if readKey==recordKeybind:
            _record()
        if readKey==playKeybind:
            _play()
        window.update_idletasks()
        window.update()
    

#tkinter setup

window = Tk()

window.title("Scripter main window")

#keybinds buttons
recordKeyLbl = Label(window, text='record key')
recordKeyLbl.grid(column=0, row=0)
playKeyLbl=Label(window, text='play key')
playKeyLbl.grid(column=2, row=0)
recordKeyButton = Button(window, text=recordKeybind, command=setRecordKey)
recordKeyButton.grid(column=1, row=0)
playKeyButton = Button(window, text=playKeybind, command=setPlayKey)
playKeyButton.grid(column=3, row=0)
#start waiting for recording or play key (TODO: better way to do this)
startButton = Button(window, text='start', command=_start)
startButton.grid(column=4, row=1)
#current macro
currentMacroLbl1=Label(window, text='current macro name: '+currentMacroName)
currentMacroLbl1.grid(column=4, row=0)
#all saved macros
savedMacroLbl=Label(window, text='---SAVED MACROS---')
savedMacroLbl.grid(column=0, row=1)
for i in range(len(savedMacros)):
    label=Label(window, text=savedMacros[i])
    label.grid(row=2+i, column=0)
#macro name import text widget
macroNameText = Text(window,height=2, width=18)
macroNameText.insert(INSERT, "macroname")
macroNameText.grid(column=3, row=2)
#macro select
selectMacroButton = Button(window, text='select', command=lambda : setCurrentMacro(macroNameText.get('1.0','end')))
selectMacroButton.grid(column=3, row=4)
#macro delete
deleteMacroButton = Button(window, text='delete', command=lambda :deleteMacro(macroNameText.get('1.0','end')))
deleteMacroButton.grid(column=4, row=4)
#macro save
saveMacroButton = Button(window, text='save', command=lambda :saveMacro(macroNameText.get('1.0','end')))
saveMacroButton.grid(column=5, row=4)
#---TIMER TEXTS---
#timer hours text
timerHoursText = Text(window,height=1, width=10)
timerHoursText.insert(INSERT, "0")
timerHoursText.grid(column=3, row=6)
#timer minute text
timerMinuteText = Text(window,height=1, width=10)
timerMinuteText.insert(INSERT, "0")
timerMinuteText.grid(column=4, row=6)
#timer seconds text
timerSecondsText = Text(window,height=1, width=10)
timerSecondsText.insert(INSERT, "0")
timerSecondsText.grid(column=5, row=6)
#set timer button
setTimerButton = Button(window, text='play with timer', command=lambda :_playWithTimer(timerHoursText.get('1.0','end'), timerMinuteText.get('1.0','end'), timerSecondsText.get('1.0','end')))
setTimerButton.grid(column=4, row=7)
#timer hours remaining label
timerHoursLabel=Label(window, text='0')
timerHoursLabel.grid(column=3, row=8)
#timer hours remaining label
timerMinutesLabel=Label(window, text='0')
timerMinutesLabel.grid(column=4, row=8)
#timer hours remaining label
timerSecondsLabel=Label(window, text='0')
timerSecondsLabel.grid(column=5, row=8)
#---TIMER TEXTS END---
#---START TIMER FUNCTION
def _playWithTimer(_hours, _minutes, _seconds):
    global isPlayingWithTimer
    isPlayingWithTimer=True
    global finishedPlaying
    (_hours, _minutes, _seconds)=int(_hours), int(_minutes), int(_seconds)
    allInSeconds=_hours*3600+_minutes*60+_seconds
    start=time.time()
    while True:
        #if timer ended
        #set how many time remaining 
        _time=time.time()-start
        
        HoursMinutesSeconds=convert(allInSeconds-_time)
        timerHoursLabel.configure(text=HoursMinutesSeconds[0])
        timerMinutesLabel.configure(text=HoursMinutesSeconds[1])
        timerSecondsLabel.configure(text=HoursMinutesSeconds[2])
        window.update()
        window.update_idletasks()
        if _time>allInSeconds and finishedPlaying==True:
            #set bool to help with timer
            finishedPlaying=False
            _play()
        if _time>allInSeconds:
            start=time.time()
        #jus fo making you understand: now there would be isPlayingWithTimer=False IF IT WERENT FUCKING INFINITE!
#main

def updateWindow():
    while True:
        window.update()
        window.update_idletasks()


updateWindow()


    

 





