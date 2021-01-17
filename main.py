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

appWindow = None            # Global MainWindow app
temperatureState = "Cool"   # Cool/HOT (ensures siren only triggers once per transition)

# Obtain temperatures and store in nice dictionary for use anywhere
def getTemperatures():
    if not hasattr(psutil, "sensors_temperatures"):
        sys.exit("platform not supported")

    if not hasattr(psutil, "sensors_fans"):
        sys.exit("platform not supported")

    temps = psutil.sensors_temperatures()
    fans  = psutil.sensors_fans()

    if not temps or not 'coretemp' in temps:
        sys.exit("Incompatible Hardware: Can't read any temperature")
    if not fans or not 'thinkpad' in fans:
        sys.exit("Incompatible Hardware: Can't read fan data")

    core0 = temps["coretemp"][0].current
    core1 = temps["coretemp"][1].current
    fan   = fans["thinkpad"][0].current

    core0_max = temps["coretemp"][0].high
    core1_max = temps["coretemp"][1].high

    return {
             "core0": core0,
             "core1": core1,
             "fan": fan,
             "max_core0": core0_max,
             "max_core1": core1_max,
           }

# Updates the dislpayed temperature values in the GUI Window
# and enables/disables the siren if necessary
def updateTemperatureVals():
    global appWindow
    global temperatureState

    dictValues = getTemperatures()
    appWindow.updateValues(dictValues)

    core0 = dictValues["core0"]
    core1 = dictValues["core1"]

    # Temperature threshold "state" is stored in GUI
    TEMP_THRESH_HI = appWindow.getTempThreshHi()
    TEMP_THRESH_LO = appWindow.getTempThreshLo()
    
    # Hi/Lo thresholds and temperatureState implement hysteresis
    if (max(core0, core1) > TEMP_THRESH_HI and temperatureState == "Cool"):
        temperatureState = "HOT"
        print("HIGH TEMP WARNING!!")
        Notify.Notification.new("HIGH TEMP WARNING!!").show()
        appWindow.playAlarm()

    elif (max(core0, core1) < TEMP_THRESH_LO and temperatureState == "HOT"):
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

    # Every two seconds, measure the CPU temperature and update the GUI
    timer = QTimer(appWindow)
    timer.setInterval(2000)
    timer.timeout.connect(updateTemperatureVals)
    timer.start()

    # Update the temperature values once before rendering the GUI
    updateTemperatureVals()
    appWindow.show()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
