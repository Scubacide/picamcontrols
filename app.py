import picamera
import time
import datetime as dt
from time import sleep
from datetime import datetime
from guizero import App, Text, Picture, Box, PushButton, Window, TextBox, ListBox
import tkinter
from tkinter.constants import CENTER, LEFT, TOP, W
import os
from os import system, path
import asyncio
dir = "/home/pi/PiCam"
a = 0
def fileSetup():
    if os.path.exists(dir):
        pass
    else:
        os.mkdir(dir)
        os.mkdir(dir + "/Pictures")
        os.mkdir(dir + "/Timelapses")
        os.mkdir(dir + "/Timelapses/TimelapsePics")
        os.mkdir(dir + "/Videos")
#pic
def takePic(): #working
    print('test')
    with picamera.PiCamera() as camera:
        now = dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        camera.resolution = (1920, 1080)
        camera.framerate = 30
        camera.start_preview()
        time.sleep(2)
        camera.annotate_background = picamera.Color('gray')
        camera.annotate_text = dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        camera.capture("/home/pi/PiCam/Pictures/" + str(now) + ".jpg")
        camera.stop_preview()
        now = None
        print('test')
#ps vid
def takeVideoPS(): #working
    statusChange1()
    time.sleep(1)
    try:
        recordTime = ((int(inputBoxH.value) * 3600) + (int(inputBoxM.value) * 60) + (int(inputBoxS.value)))
        with picamera.PiCamera() as camera:
            now = dt.datetime.now().strftime('%Y-%m-%d %H:%M')
            camera.resolution = (1920, 1080)
            camera.framerate = 30
            camera.brightness = 55
            camera.start_preview()
            camera.annotate_background = picamera.Color('gray')
            camera.start_recording("/home/pi/PiCam/Videos/" + str(now) + '.h264')
            start = dt.datetime.now()
            while (dt.datetime.now() - start).seconds < recordTime:
                camera.annotate_text = dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                camera.wait_recording(0.1)
            camera.stop_recording()
            camera.stop_preview()
            statusTxt.value = "Done."
            print(recordTime)
    except:
        statusTxt.value = "Time error."

Recording = True
#video non preset
def takeVideo(): #broken
    with picamera.PiCamera() as camera:
        now = dt.datetime.now().strftime('%Y-%m-%d %H:%M')
        camera.resolution = (1280, 768)
        camera.framerate = 30
        camera.brightness = 55
        camera.start_preview()
        camera.annotate_background = picamera.Color('gray')
        camera.start_recording("/home/pi/PiCam/Videos/" + str(now) + '.h264')
        camera.annotate_text = dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
def startVid(): #broken
    print('hi')
    app.repeat(1000, takeVideo)
def stopVid(): #broken
    print('stopped')
    app.cancel(takeVideo)
    Recording: False

#timelapse preset, non preset, clear tl pics, and compile video
def timeLapsePS(): #working (mostly)
    statusChange2()
    recordTime = ((int(inputBoxH.value) * 3600) + (int(inputBoxM.value) * 60) + (int(inputBoxS.value)))
    now = dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    picInterval = int(inputBoxTLI.value)
    fps = 30
    picsToTake = int((recordTime)/picInterval)
    print(now)
    print("Taking " + str(picsToTake) + " over the course of " + str(recordTime) + " seconds.")

    with picamera.PiCamera() as camera:
        for i in range(picsToTake):
            camera.capture('/home/pi/PiCam/Timelapses/TimelapsePics/image{0:06d}.jpg'.format(i))
            sleep(picInterval)
    statusTxt.value = "Done."
def makeTimelapse(): #working
    statusChange3()
    fps = 30
    now = dt.datetime.now().strftime('%Y-%m-%d_%H:%M')
    recordTime = ((int(inputBoxH.value) * 3600) + (int(inputBoxM.value) * 60) + (int(inputBoxS.value)))
    print("Please standby as your timelapse video is created.")
    system('ffmpeg -r {} -f image2 -s 1280x768 -nostats -loglevel 0 -pattern_type glob -i "/home/pi/PiCam/Timelapses/TimelapsePics/*.jpg" -vcodec libx264 -crf 25  -pix_fmt yuv420p /home/pi/PiCam/Timelapses/{}.mp4'.format(fps, now))
    print(now)
def startTimelapse(): #working
    statusChange2()
    app.repeat((int(inputBoxTLI.value)*1000), timelapse)
    print(int(inputBoxTLI.value)*1000)
def timelapse(): #working
    global a
    with picamera.PiCamera() as camera:
        camera.capture('/home/pi/PiCam/Timelapses/TimelapsePics/image{0:06d}.jpg'.format(a))  
        print("Capped pic # {}".format(a))   
    a+=1
def stopTimelapse(): #working
    statusChange5()
    print('Stopped')
    app.cancel(timelapse)
def clearTLP(): #working
    statusChange4()
    system('rm /home/pi/PiCam/Timelapses/TimelapsePics/*.jpg')

def startStream():
    app.repeat(10000, stream)
def stream():
    system('python3 /home/pi/Desktop/stream.py')
def stopStream():
    print('exiting.')
    system('exit')
    app.cancel(stream)
#statuses
def statusChange1(): #recording
    statusTxt.value = "Recording..."
def statusChange2(): #timelapsing
    statusTxt.value = "Timelapsing..."
def statusChange3(): #compiling tl
    statusTxt.value = "Compiling TL..."
def statusChange4(): #timelapse cleared
    statusTxt.value = "Timelapse Cleared."
def statusChange5(): #timelapse stopped
    statusTxt.value = "Timelapse Stopped."

#folder openings
def openFolderP(): 
    path = "/home/pi/PiCam/Pictures"
    path = os.path.realpath(path)
    os.system('xdg-open "%s"' % path)
def openFolderV():
    path = "/home/pi/PiCam/Videos"
    path = os.path.realpath(path)
    os.system('xdg-open "%s"' % path)
def openFolderTV():
    path = "/home/pi/PiCam/Timelapses"
    path = os.path.realpath(path)
    os.system('xdg-open "%s"' % path)


#GUI--------------------------------------------------------------------------------
app = App(title="Pi Camera Controls", width=440, height=450, layout="grid")
#row1
pictureButton = PushButton(app, text="Take Picture", grid=[0,0], width=15, height=2, command=takePic)
videoButtonPS = PushButton(app, text="Record Video PS", grid=[1,0], width=15, height=2, command=takeVideoPS)
timelapseButtonPS = PushButton(app, text="Take Timelapse PS", grid=[2,0], width=15, height=2, command=timeLapsePS)
#row2
startVidButton = PushButton(app, text="Start Recording", grid=[0,1], width=15, height=2, command=startVid)
byJoshTxt = Text(app, text="by Josh M", grid=[1,1], width=9, height=1)
stopVidButton = PushButton(app, text="Stop Recording", grid=[2,1], width=15, height=2, command=stopVid)
#row3
startTLButton = PushButton(app, text="Start Timelapse", grid=[0,2], width=15, height=2, command=startTimelapse)
makeTLButton = PushButton(app, text="Make Timelapse", grid=[1,3], width=15, height=2, command=makeTimelapse)
stopTLButton = PushButton(app, text="Stop Timelapse", grid=[2,2], width=15, height=2, command=stopTimelapse)
#row4
startStreamButton = PushButton(app, text="Start Streaming", grid=[0,3], width=15, height=2, command=stream)
stopStreamButton = PushButton(app, text="Stop Streaming", grid=[2,3], width=15, height=2, command=stopStream)
#row5
picFolderButton = PushButton(app, text="View Pics", grid=[0,8], width=15, height=2, command=openFolderP)
vidFolderButton = PushButton(app, text="View Videos", grid=[1,8], width=15, height=2, command=openFolderV)
TLFolder = PushButton(app, text="View Timelapses", grid=[2,8], width=15, height=2, command=openFolderTV)
#inputs
vidTimeH = Text(app, grid=[0,4], text="Record Hours: ", align="left")
inputBoxH = TextBox(app, grid=[1,4], text="0", align="left")
vidTimeM = Text(app, grid=[0,5], text="Record Mins: ", align="left")
inputBoxM = TextBox(app, grid=[1,5], text="0", align="left")
vidTimeS = Text(app, grid=[0,6], text="Record Seconds: ", align="left")
inputBoxS = TextBox(app, grid=[1,6], text="0", align="left")
timelapseInt = Text(app, grid=[0,7], text="Capture Interval: ", align="left")
inputBoxTLI = TextBox(app, grid=[1,7], text="1", align="left")

clearButton = PushButton(app, grid=[2,5,2,6], text="Clear TL Pics", height=1, width=10, align="top", command=clearTLP)

statusTxt = Text(app, grid=[1,2], text="status")
fileSetup()
startVidButton.disable()
stopVidButton.disable()
app.show()
app.display()
#GUI--------------------------------------------------------------------------------
