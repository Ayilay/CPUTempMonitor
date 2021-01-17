#!/usr/bin/env python3

import gi.repository
gi.require_version('Notify', '0.7')
from gi.repository import Notify

import psutil
import sys
import signal

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from mainWindow import Window

appWindow = None
temperatureState = "Cool"

def getTemperatures():
    if not hasattr(psutil, "sensors_temperatures"):
        sys.exit("platform not supported")

    if not hasattr(psutil, "sensors_fans"):
        sys.exit("platform not supported")

    temps = psutil.sensors_temperatures()
    fans  = psutil.sensors_fans()

    if not temps:
        sys.exit("Can't read any temperature")
    if not fans or not 'thinkpad' in fans:
        sys.exit("Can't read fan data")

    core0 = temps["coretemp"][0].current
    core1 = temps["coretemp"][1].current
    gpu   = 0 if not "nouveau" in temps else temps["nouveau"][0].current
    fan   = fans["thinkpad"][0].current

    core0_max = temps["coretemp"][0].high
    core1_max = temps["coretemp"][1].high
    gpu_max   = 0 if not "nouveau" in temps else temps["nouveau"][0].high

    return {
             "core0": core0,
             "core1": core1,
             "gpu": gpu,
             "fan": fan,
             "max_core0": core0_max,
             "max_core1": core1_max,
             "max_gpu": gpu_max
           }

def updateTemperatureVals():
    global appWindow
    global temperatureState

    dictValues = getTemperatures()
    #print(dictValues)
    appWindow.updateValues(dictValues)

    core0 = dictValues["core0"]
    core1 = dictValues["core1"]
    gpu   = dictValues["gpu"]

    TEMP_THRESH_HI = appWindow.getTempThreshHi()
    TEMP_THRESH_LO = appWindow.getTempThreshLo()
    #TEMP_THRESH_HI = 65
    #TEMP_THRESH_LO = 60
    
    if (max(core0, core1, gpu) > TEMP_THRESH_HI and temperatureState == "Cool"):
        temperatureState = "HOT"
        print("HIGH TEMP WARNING!!")
        Notify.Notification.new("HIGH TEMP WARNING!!").show()
        appWindow.playAlarm()

    elif (max(core0, core1, gpu) < TEMP_THRESH_LO and temperatureState == "HOT"):
        temperatureState = "Cool"
        print("Cooled down :D")
        Notify.Notification.new("CPU Cooled Down").show()
        appWindow.stopAlarm()

    

def main():
    global appWindow

    # Exit app on Ctrl+C
    signal.signal(signal.SIGINT, signal.SIG_DFL)

    # Sends DBus notifications to Desktop, quite nifty
    Notify.init("CPU Temperature Monitor")

    # The app GUI (View only, Controller is this file)
    app = QApplication(sys.argv)
    appWindow = Window()

    # Initialize the periodic timer that grabs the temperatures
    timer = QTimer(appWindow)
    timer.setInterval(2000)
    timer.timeout.connect(updateTemperatureVals)
    timer.start()

    # Update the temperature values before rendering the GUI
    updateTemperatureVals()
    appWindow.show()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
