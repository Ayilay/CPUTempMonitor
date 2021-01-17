from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtMultimedia import QSound

class Window(QMainWindow):

    def __init__(self):
        super().__init__()

        self.alarmTone = QSound("resources/alarm.wav")
        self.setWindowIcon(QIcon("resources/cpu-temp_2.png"))

        self.setWindowTitle("System Temperature Monitor")
        self.resize(300, 250)

        # Threshold for alerting user
        # Alarm starts when temp rises above HI thresh
        # Alarm stops  when temp falls below LO thresh
        self.tempThreshHi = 100
        self.tempThreshLo = 85

        # Font Family for all text
        fontFam = QFont("Droid Sans Mono", 16)

        # Threshold Setting options
        
        threshGroup = self.initThreshSettingsGroup()

        # Add the Temperature Status text
        self.overalStatus = QLabel()
        self.overalStatus.setText("Temperature Nominal")
        self.overalStatus.setFont(fontFam)
        self.overalStatus.setStyleSheet("color: black")
        self.overalStatus.setAlignment(Qt.AlignCenter)

        statusGroup = self.initTempDisplayGroup(fontFam)

        # Finally, place all sub-layouts and widgets to the main layout
        mainLayout = QVBoxLayout()
        mainLayout.addSpacing(10)
        mainLayout.addWidget(statusGroup)
        mainLayout.addWidget(threshGroup)
        mainLayout.addSpacing(20)
        mainLayout.addWidget(self.overalStatus)
        mainLayout.addStretch(1)

        # Set the layout on the application's window
        self.centralWidget = QWidget()
        self.centralWidget.setLayout(mainLayout)
        zz = 20
        self.centralWidget.setContentsMargins(zz, 5, zz, 5)
        self.setCentralWidget(self.centralWidget)

        # DEBUG STUFF, REMOVE WHEN DONE
        #fontdb = QFontDatabase()
        #for fontEntry in (fontdb.families()):
        #    print( fontEntry)

        # Create the Menu Bar
        #self.createMenuBar()
        #self.statusbar = self.statusBar()

    ############################################################
    #   GUI Init Helper Functions
    ############################################################

    def initTempDisplayGroup(self, fontFam):
        statusGroupLayout = QGridLayout()

        cpu0_txt         = QLabel();
        cpu1_txt         = QLabel();
        gpu0_txt         = QLabel();
        rpm0_txt         = QLabel();
        self.cpu0_val    = QLabel();
        self.cpu1_val    = QLabel();
        self.gpu0_val    = QLabel();
        self.rpm0_val    = QLabel();

        cpu0_txt.setText("Core0: ");
        cpu1_txt.setText("Core1: ");
        rpm0_txt.setText("Fan RPM: ");

        self.cpu0_val.setText("60 °C");
        self.cpu1_val.setText("60 °C");
        self.rpm0_val.setText("4000 RPM");

        cpu0_txt.setFont(fontFam);
        cpu1_txt.setFont(fontFam);
        rpm0_txt.setFont(fontFam);

        cpu0_txt.setAlignment(Qt.AlignRight);
        cpu1_txt.setAlignment(Qt.AlignRight);
        rpm0_txt.setAlignment(Qt.AlignRight);

        self.cpu0_val.setFont(fontFam);
        self.cpu1_val.setFont(fontFam);
        self.rpm0_val.setFont(fontFam);

        # Position the labels and widgets
        y = 0
        x = -1
        statusGroupLayout.setColumnStretch((x := x+1), 0)
        statusGroupLayout.addWidget(cpu0_txt, y, (x := x+1))
        statusGroupLayout.setColumnMinimumWidth((x := x+1), 10)
        statusGroupLayout.addWidget(self.cpu0_val, y, (x := x+1))
        statusGroupLayout.setColumnStretch((x := x+1), 0)

        y = y + 1
        x = -1
        statusGroupLayout.setColumnStretch((x := x+1), 1)
        statusGroupLayout.addWidget(cpu1_txt, y, (x := x+1))
        statusGroupLayout.setColumnMinimumWidth((x := x+1), 10)
        statusGroupLayout.addWidget(self.cpu1_val, y, (x := x+1))
        statusGroupLayout.setColumnStretch((x := x+1), 1)

        y = y + 1
        x = -1
        statusGroupLayout.setColumnStretch((x := x+1), 1)
        statusGroupLayout.addWidget(rpm0_txt, y, (x := x+1))
        statusGroupLayout.setColumnMinimumWidth((x := x+1), 10)
        statusGroupLayout.addWidget(self.rpm0_val, y, (x := x+1))
        statusGroupLayout.setColumnStretch((x := x+1), 1)

        # Add all statusGroup widgets to a GroupBox
        statusGroupBox = QGroupBox("Temperature Stats")
        statusGroupBox.setLayout(statusGroupLayout)

        return statusGroupBox

    # Initialize the temperature threshold sliders
    # Each slider has 3 elements; The "name" of the slider,
    #   the slider itself, and a QLineEdit box that displays
    #   the current value of the slider
    def initThreshSettingsGroup(self):
        self.threshHiSlider = QSlider(Qt.Horizontal)
        self.threshLoSlider = QSlider(Qt.Horizontal)

        # The High Threshold Slider
        hiSliderLayout = QHBoxLayout()
        self.threshHiSlider.setMinimum(40)
        self.threshHiSlider.setMaximum(110)
        self.threshHiSlider.setValue(self.tempThreshHi)
        self.threshHiSlider.setTickPosition(QSlider.TicksAbove)
        self.threshHiSlider.setMinimumWidth(200)
        self.threshHiSlider.valueChanged.connect(self.sliderHiChanged)

        # Identifies High Threshold Slider
        hiLabel = QLabel("Hi")

        # A text box for manually setting the value
        self.hiThreshVal = QLineEdit("{}".format(self.tempThreshHi))
        self.hiThreshVal.setMaximumWidth(50)
        self.hiThreshVal.setMaxLength(3)
        self.hiThreshVal.returnPressed.connect(self.sliderBoxHiChanged)

        # The Low Threshold Slider
        loSliderLayout = QHBoxLayout()
        self.threshLoSlider.setMinimum(40)
        self.threshLoSlider.setMaximum(110)
        self.threshLoSlider.setValue(self.tempThreshLo)
        self.threshLoSlider.setMinimumWidth(200)
        self.threshLoSlider.setTickPosition(QSlider.TicksAbove)
        self.threshLoSlider.valueChanged.connect(self.sliderLoChanged)

        # Identifies Low Threshold Slider
        loLabel = QLabel("Lo")

        # A text box for manually setting the value
        self.loThreshVal = QLineEdit("{}".format(self.tempThreshLo))
        self.loThreshVal.setMaximumWidth(50)
        self.loThreshVal.setMaxLength(3)
        self.loThreshVal.returnPressed.connect(self.sliderBoxLoChanged)

        # Add "Slider Widget" Elements to their layouts (name, slider, value)
        hiSliderLayout.addWidget(hiLabel)
        hiSliderLayout.addWidget(self.threshHiSlider)
        hiSliderLayout.addWidget(self.hiThreshVal)
        loSliderLayout.addWidget(loLabel)
        loSliderLayout.addWidget(self.threshLoSlider)
        loSliderLayout.addWidget(self.loThreshVal)

        # Add the sliders to their final vertical layout
        threshLayout = QVBoxLayout()
        threshLayout.addLayout(hiSliderLayout)
        threshLayout.addLayout(loSliderLayout)

        threshGroup = QGroupBox("Temperature Thresholds")
        threshGroup.setLayout(threshLayout)

        return threshGroup

    def updateValues(self, dictValues):
        gpuVal = 0
        if (dictValues["gpu"] == 0):
            gpuVal = "N/A"
        else:
            gpuVal = dictValues["gpu"] 

        self.cpu0_val.setText("{} °C".format(dictValues["core0"]));
        self.cpu1_val.setText("{} °C".format(dictValues["core1"]));
        self.gpu0_val.setText("{} °C".format(gpuVal));
        self.rpm0_val.setText("{} RPM".format(dictValues["fan"]));

    def playAlarm(self):
        self.alarmTone.play()
        self.overalStatus.setText("CPU OVERHEAT!")
        self.overalStatus.setStyleSheet("color: red")

    def stopAlarm(self):
        self.alarmTone.stop()
        self.overalStatus.setText("Temperature Nominal")
        self.overalStatus.setStyleSheet("color: black")

    ############################################################
    #   Temperature Threshold Signals
    ############################################################
    def sliderLoChanged(self, newVal):
        self.setTempThreshLo(newVal)

    def sliderHiChanged(self, newVal):
        self.setTempThreshHi(newVal)

    def sliderBoxLoChanged(self):
        self.setTempThreshLo(int(self.loThreshVal.text()))

    def sliderBoxHiChanged(self):
        self.setTempThreshHi(int(self.hiThreshVal.text()))

    ############################################################
    #   Setters/Getters
    ############################################################

    def getTempThreshHi(self):
        return self.tempThreshHi

    def getTempThreshLo(self):
        return self.tempThreshLo

    def setTempThreshHi(self, newVal):
        self.tempThreshHi = newVal
        self.hiThreshVal.setText("{}".format(newVal))
        self.threshHiSlider.setValue(newVal)

    def setTempThreshLo(self, newVal):
        self.tempThreshLo = newVal
        self.loThreshVal.setText("{}".format(newVal))
        self.threshLoSlider.setValue(newVal)
