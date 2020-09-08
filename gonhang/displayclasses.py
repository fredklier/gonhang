from PyQt5 import QtWidgets, QtCore, QtGui
from gonhang import core
from gonhang import api
import humanfriendly
from gonhang.core import Config
from gonhang.api import FileUtil


class AboutBox(QtWidgets.QDialog):
    config = Config()

    def __init__(self, parent=None):
        super(AboutBox, self).__init__(parent)
        self.setFixedWidth(480)
        self.centerMe()
        self.setWindowTitle(f'GonhaNG - Next Generation - {self.config.getVersion()}')
        alignCenter = QtCore.Qt.AlignHCenter
        self.okButton = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok)
        self.okButton.accepted.connect(self.hideMe)
        self.layout = QtWidgets.QVBoxLayout()
        # ------------------------------------------------------------------------------------------
        # Logo
        self.logoLabel = QtWidgets.QLabel()
        self.logoLabel.setPixmap(QtGui.QPixmap(f'{FileUtil.getResourcePath()}/images/logoaboutbox.png'))
        self.layout.addWidget(self.logoLabel)
        self.logoLabel.setAlignment(alignCenter)
        # ------------------------------------------------------------------------------------------
        # text about box
        gonhaNgLabel = QtWidgets.QLabel('<strong>GonhaNG - Next Generation</strong>')
        gonhaNgLabel.setTextFormat(QtCore.Qt.RichText)
        gonhaNgLabel.setAlignment(alignCenter)
        self.layout.addWidget(gonhaNgLabel)
        versionLabel = QtWidgets.QLabel(f'Version <strong>{self.config.getVersion()}</strong>')
        versionLabel.setTextFormat(QtCore.Qt.RichText)
        versionLabel.setAlignment(alignCenter)
        self.layout.addWidget(versionLabel)
        # warrantyText
        textAboutLabel = QtWidgets.QLabel('This program comes with absolutely <strong>no warranty</strong>')
        textAboutLabel.setTextFormat(QtCore.Qt.RichText)
        textAboutLabel.setAlignment(alignCenter)
        self.layout.addWidget(textAboutLabel)
        urlLink = '<a href=\"https://github.com/fredcox/gonhang/blob/master/LICENSE\">https://github.com/fredcox/gonhang/blob/master/LICENSE</a>'
        urlLabel = QtWidgets.QLabel(urlLink)
        urlLabel.setAlignment(alignCenter)
        urlLabel.setOpenExternalLinks(True)
        self.layout.addWidget(urlLabel)

        self.layout.addSpacing(30)

        self.layout.addWidget(self.okButton, alignment=QtCore.Qt.AlignHCenter)
        self.setLayout(self.layout)

    def centerMe(self):
        screenGeo = QtWidgets.QApplication.desktop().screenGeometry()
        x = (screenGeo.width() - self.width()) / 2
        # y = (screenGeo.height() - self.height()) / 2
        self.move(x, 100)

    def hideMe(self):
        self.hide()


class CommomAttributes:
    pbDefaultHeight = 20
    tempLabelWidth = 50

    def __init__(self):
        # -------------------------------------------------------------
        # Styles
        self.groupBoxStyle = """
        QGroupBox {
            border: 1px solid white;
            border-radius: 5px;
            margin-top: 12px;
            padding-left: 2px;
        }
        QGroupBox:title {
            subcontrol-origin: margin;
            subcontrol-position: top left;
            color: rgb(252, 126, 0);
            left: 15px;
        }
        """
        self.yellowPBStyle = """
        QProgressBar {
            text-align: left;
            font-weight: bold;
            color: rgb(255, 255, 255);
            background-color : rgba(0, 0, 0, 0);
            border: 0px solid rgba(0, 0, 0, 0);
            border-radius: 3px;                                    
        }
        QProgressBar::chunk {
            background: rgb(255, 153, 0);
            border-radius: 3px;            
        }
        """

        self.redPBStyle = """
        QProgressBar {
            text-align: left;
            font-weight: bold;
            color: rgb(255, 255, 255);
            background-color : rgba(0, 0, 0, 0);
            border: 0px solid rgba(0, 0, 0, 0);
            border-radius: 3px;                                    
        }
        QProgressBar::chunk {
            background: rgb(255, 51, 0);
            border-radius: 3px;            
        }
        """
        self.greenPBStyle = """
        QProgressBar {
            text-align: left;
            font-weight: bold;
            color: rgb(255, 255, 255);
            background-color : rgba(0, 0, 0, 0);
            border: 0px solid rgba(0, 0, 0, 0);
            border-radius: 3px;           
        }
        QProgressBar::chunk {
            background: rgb(51, 153, 51);
            border-radius: 3px;            
        }
        """
        self.orange = 'color: rgb(252, 126, 0);'
        self.white = 'color: rgb(255, 255, 255);'
        self.green = 'color: rgb(34, 255, 19);'
        self.red = 'color: rgb(255, 51, 0);'
        self.yellow = 'color: rgb(255, 153, 0);'

        # ---------------------------------------------------------------------
        # Default font
        self.fontDefault = QtGui.QFont('Fira Code', 11)
        self.fontGroupBox = QtGui.QFont('Fira Code', 14)
        self.groupBoxDefaultWidth = 450

    def getDefaultGb(self, title):
        defaultGb = QtWidgets.QGroupBox(title)
        defaultGb.setFont(self.fontGroupBox)
        defaultGb.setStyleSheet(self.groupBoxStyle)
        defaultGb.setFixedWidth(self.groupBoxDefaultWidth)
        return defaultGb

    @staticmethod
    def setLabel(label, labelcolor, font):
        label.setFont(font)
        label.setStyleSheet(labelcolor)

    def analizeProgressBar(self, pb, value):
        if value < 50:
            pb.setStyleSheet(self.greenPBStyle)
        elif (value >= 50) and (value < 80):
            pb.setStyleSheet(self.yellowPBStyle)
        elif value >= 80:
            pb.setStyleSheet(self.redPBStyle)

    def analizeFreq(self, lbl, current, maximun):
        currentValue = float(current)
        maxValue = float(maximun)
        highValue = maxValue - (maxValue * 0.4)

        if currentValue < highValue:
            lbl.setStyleSheet(self.green)
        elif (currentValue >= highValue) and (currentValue < maxValue):
            lbl.setStyleSheet(self.yellow)
        elif currentValue >= maxValue:
            lbl.setStyleSheet(self.red)

    def analizeValue(self, lbl, current, maximun):
        currentValue = humanfriendly.parse_size(current)
        maxValue = humanfriendly.parse_size(maximun)
        highValue = maxValue - (maxValue * 0.4)

        if currentValue < highValue:
            lbl.setStyleSheet(self.green)
        elif (currentValue >= highValue) and (currentValue < maxValue):
            lbl.setStyleSheet(self.yellow)
        elif currentValue >= maxValue:
            lbl.setStyleSheet(self.red)

    @staticmethod
    def analizeTemp(label, current, highValue, criticalValue):
        colorNormal = 'color: rgb(157, 255, 96);'
        colorWarning = 'color: rgb(255, 255, 153);'
        colorAlarm = 'color: rgb(255, 79, 79);'
        label.setStyleSheet(colorNormal)
        if current >= criticalValue:
            label.setStyleSheet(colorAlarm)
        elif (current < criticalValue) and (current >= highValue):
            label.setStyleSheet(colorWarning)


class DisplaySystem:
    commom = CommomAttributes()
    systemWidgets = dict()
    system = core.System()

    def initUi(self):
        pbDefaultWidth = 180
        iconDefaultWidth = 80
        message = self.system.getMessage()
        systemGroupBox = self.commom.getDefaultGb('system')

        verticalLayout = QtWidgets.QVBoxLayout()
        verticalLayout.setSpacing(0)

        distroGridLayout = QtWidgets.QGridLayout()
        distroGridLayout.setAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignHCenter)
        distroGridLayout.setSpacing(0)
        # ---------------------------------------------------------------------------
        # distro Icon
        # ---------------------------------------------------------------------------
        distroIcon = QtWidgets.QLabel()
        distroIcon.setPixmap(QtGui.QPixmap(message['distroIcon']))
        self.systemWidgets['distroIcon'] = distroIcon

        distroGridLayout.addWidget(distroIcon, 0, 0, -1, 1)

        # ---------------------------------------------------------------------------
        # Distro label
        distroLabel = QtWidgets.QLabel(message['distroStr'])
        self.commom.setLabel(distroLabel, self.commom.white, self.commom.fontDefault)
        self.systemWidgets['distroStr'] = distroLabel

        distroGridLayout.addWidget(distroLabel, 0, 1)

        # ---------------------------------------------------------------------------
        # kernel label
        kernelLabel = QtWidgets.QLabel(f"Kernel {message['release']}")
        self.commom.setLabel(kernelLabel, self.commom.white, self.commom.fontDefault)
        self.systemWidgets['release'] = kernelLabel

        distroGridLayout.addWidget(kernelLabel, 1, 1)
        # ---------------------------------------------------------------------------
        # Machine Label
        machineLabel = QtWidgets.QLabel(f"node {message['node']} arch {message['machine']}")
        self.commom.setLabel(machineLabel, self.commom.white, self.commom.fontDefault)
        self.systemWidgets['nodeMachine'] = machineLabel

        distroGridLayout.addWidget(machineLabel, 2, 1)
        # ---------------------------------------------------------------------------
        verticalLayout.addLayout(distroGridLayout)
        # ---------------------------------------------------------------------------
        # ---------------------------------------------------------------------------
        # boot time label
        verticalLayout.addLayout(distroGridLayout)

        bootAndCpuModelLayout = QtWidgets.QVBoxLayout()
        bootAndCpuModelLayout.setSpacing(0)
        btHLayout = QtWidgets.QHBoxLayout()
        btHLayout.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)

        # --------------------------------------------------------------------
        # days, hours, minutes and seconds labels
        btDaysLabel = QtWidgets.QLabel(f"{message['btDays']} ")
        self.commom.setLabel(btDaysLabel, self.commom.green, self.commom.fontDefault)
        btHLayout.addWidget(btDaysLabel)
        self.systemWidgets['btDays'] = btDaysLabel

        daysLabel = QtWidgets.QLabel('days, ')
        self.commom.setLabel(daysLabel, self.commom.white, self.commom.fontDefault)
        btHLayout.addWidget(daysLabel)

        btHoursLabel = QtWidgets.QLabel(f"{message['btHours']} ")
        self.commom.setLabel(btHoursLabel, self.commom.green, self.commom.fontDefault)
        btHLayout.addWidget(btHoursLabel)
        self.systemWidgets['btHours'] = btHoursLabel

        hoursLabel = QtWidgets.QLabel('hours ')
        self.commom.setLabel(hoursLabel, self.commom.white, self.commom.fontDefault)
        btHLayout.addWidget(hoursLabel)

        btMinutesLabel = QtWidgets.QLabel(f"{message['btMinutes']} ")
        self.commom.setLabel(btMinutesLabel, self.commom.green, self.commom.fontDefault)
        btHLayout.addWidget(btMinutesLabel)
        self.systemWidgets['btMinutes'] = btMinutesLabel

        minutesLabel = QtWidgets.QLabel('minutes ')
        self.commom.setLabel(minutesLabel, self.commom.white, self.commom.fontDefault)
        btHLayout.addWidget(minutesLabel)

        btSecondsLabel = QtWidgets.QLabel(f"{message['btSeconds']} ")
        self.commom.setLabel(btSecondsLabel, self.commom.green, self.commom.fontDefault)
        btHLayout.addWidget(btSecondsLabel)
        self.systemWidgets['btSeconds'] = btSecondsLabel

        secondsLabel = QtWidgets.QLabel('seconds')
        self.commom.setLabel(secondsLabel, self.commom.white, self.commom.fontDefault)
        btHLayout.addWidget(secondsLabel)

        bootAndCpuModelLayout.addLayout(btHLayout)

        verticalLayout.addLayout(bootAndCpuModelLayout)
        # ---------------------------------------------------------------------------
        # CPU info
        cpuBrandLabel = QtWidgets.QLabel(self.system.getCpuModelName())
        self.commom.setLabel(cpuBrandLabel, self.commom.white, self.commom.fontDefault)
        cpuBrandLabel.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)

        bootAndCpuModelLayout.addWidget(cpuBrandLabel)

        verticalLayout.addLayout(bootAndCpuModelLayout)
        # ---------------------------------------------------------------------------
        # Cpu load

        gridLayout = QtWidgets.QGridLayout()
        cpuIcon = QtWidgets.QLabel()
        cpuIcon.setPixmap(QtGui.QPixmap(f"{api.FileUtil.getResourcePath()}/images/cpu.png"))
        cpuIcon.setFixedWidth(iconDefaultWidth)

        gridLayout.addWidget(cpuIcon, 0, 0)

        cpuProgressBar = QtWidgets.QProgressBar()
        cpuProgressBar.setFixedHeight(self.commom.pbDefaultHeight)
        cpuProgressBar.setFont(self.commom.fontDefault)
        cpuProgressBar.setStyleSheet(self.commom.greenPBStyle)
        cpuProgressBar.setValue(message['cpuProgressBar'])
        self.systemWidgets['cpuProgressBar'] = cpuProgressBar

        gridLayout.addWidget(cpuProgressBar, 0, 1)

        cpuFreqCurrentLabel = QtWidgets.QLabel(f"{message['cpuFreqCurrent']} MHz")
        self.commom.setLabel(cpuFreqCurrentLabel, self.commom.white, self.commom.fontDefault)
        self.systemWidgets['cpuFreqCurrent'] = cpuFreqCurrentLabel
        cpuFreqCurrentLabel.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)

        gridLayout.addWidget(cpuFreqCurrentLabel, 0, 2)

        cpuFreqSeparatorLabel = QtWidgets.QLabel('/')
        self.commom.setLabel(cpuFreqSeparatorLabel, self.commom.white, self.commom.fontDefault)
        cpuFreqSeparatorLabel.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)

        gridLayout.addWidget(cpuFreqSeparatorLabel, 0, 3)

        cpuFreqMaxLabel = QtWidgets.QLabel(f"{message['cpuFreqMax']} MHz")
        self.commom.setLabel(cpuFreqMaxLabel, self.commom.green, self.commom.fontDefault)
        cpuFreqMaxLabel.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        self.systemWidgets['cpuFreqMax'] = cpuFreqMaxLabel

        gridLayout.addWidget(cpuFreqMaxLabel, 0, 4)

        # ---------------------------------------------------------------------------
        # ram load

        ramIcon = QtWidgets.QLabel()
        ramIcon.setPixmap(QtGui.QPixmap(f"{api.FileUtil.getResourcePath()}/images/ram.png"))

        gridLayout.addWidget(ramIcon, 1, 0)

        ramProgressBar = QtWidgets.QProgressBar()
        ramProgressBar.setFixedHeight(self.commom.pbDefaultHeight)
        ramProgressBar.setFixedWidth(pbDefaultWidth)
        ramProgressBar.setFont(self.commom.fontDefault)
        ramProgressBar.setStyleSheet(self.commom.greenPBStyle)
        self.systemWidgets['ramProgressBar'] = ramProgressBar
        ramProgressBar.setValue(message['ramProgressBar'])

        gridLayout.addWidget(ramProgressBar, 1, 1)

        ramUsedLabel = QtWidgets.QLabel(f"{message['ramUsed']}")
        self.commom.setLabel(ramUsedLabel, self.commom.white, self.commom.fontDefault)
        self.systemWidgets['ramUsed'] = ramUsedLabel
        ramUsedLabel.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)

        gridLayout.addWidget(ramUsedLabel, 1, 2)

        ramSeparatorLabel = QtWidgets.QLabel('/')
        self.commom.setLabel(ramSeparatorLabel, self.commom.white, self.commom.fontDefault)
        ramSeparatorLabel.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)

        gridLayout.addWidget(ramSeparatorLabel, 1, 3)

        ramTotalLabel = QtWidgets.QLabel(f"{message['ramTotal']}")
        self.commom.setLabel(ramTotalLabel, self.commom.green, self.commom.fontDefault)
        self.systemWidgets['ramTotal'] = ramTotalLabel
        ramTotalLabel.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)

        gridLayout.addWidget(ramTotalLabel, 1, 4)

        # ---------------------------------------------------------------------------
        # swap load

        swapIcon = QtWidgets.QLabel()
        swapIcon.setPixmap(QtGui.QPixmap(f"{api.FileUtil.getResourcePath()}/images/swap.png"))

        gridLayout.addWidget(swapIcon, 2, 0)

        swapProgressBar = QtWidgets.QProgressBar()
        swapProgressBar.setFixedHeight(self.commom.pbDefaultHeight)
        swapProgressBar.setFixedWidth(pbDefaultWidth)
        swapProgressBar.setFont(self.commom.fontDefault)
        swapProgressBar.setStyleSheet(self.commom.greenPBStyle)
        self.systemWidgets['swapProgressBar'] = swapProgressBar
        swapProgressBar.setValue(message['swapProgressBar'])

        gridLayout.addWidget(swapProgressBar, 2, 1)

        swapUsedLabel = QtWidgets.QLabel(f"{message['swapUsed']}")
        self.commom.setLabel(swapUsedLabel, self.commom.white, self.commom.fontDefault)
        self.systemWidgets['swapUsed'] = swapUsedLabel
        swapUsedLabel.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)

        gridLayout.addWidget(swapUsedLabel, 2, 2)

        swapSeparatorLabel = QtWidgets.QLabel('/')
        self.commom.setLabel(swapSeparatorLabel, self.commom.white, self.commom.fontDefault)
        swapSeparatorLabel.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)

        gridLayout.addWidget(swapSeparatorLabel, 2, 3)

        swapTotalLabel = QtWidgets.QLabel(f"{message['swapTotal']}")
        self.commom.setLabel(swapTotalLabel, self.commom.green, self.commom.fontDefault)
        swapTotalLabel.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        self.systemWidgets['swapTotal'] = swapTotalLabel

        gridLayout.addWidget(swapTotalLabel, 2, 4)

        verticalLayout.addLayout(gridLayout)

        # ---------------------------------------------------------------------------
        # cpu Temperature Load
        cpuTempIcon = QtWidgets.QLabel()
        cpuTempIcon.setPixmap(QtGui.QPixmap(f"{api.FileUtil.getResourcePath()}/images/temp.png"))
        self.systemWidgets['cpuTempIcon'] = cpuTempIcon

        gridLayout.addWidget(cpuTempIcon, 3, 0)

        tempProgressBar = QtWidgets.QProgressBar()
        tempProgressBar.setFixedHeight(self.commom.pbDefaultHeight)
        tempProgressBar.setFixedWidth(pbDefaultWidth)
        tempProgressBar.setFont(self.commom.fontDefault)
        tempProgressBar.setStyleSheet(self.commom.greenPBStyle)
        self.systemWidgets['cpuTempProgressBar'] = tempProgressBar
        tempProgressBar.setValue(30)

        gridLayout.addWidget(tempProgressBar, 3, 1)

        cpuCurrentTempLabel = QtWidgets.QLabel('30.0 °C')
        self.commom.setLabel(cpuCurrentTempLabel, self.commom.white, self.commom.fontDefault)
        self.systemWidgets['cpuCurrentTempLabel'] = cpuCurrentTempLabel
        cpuCurrentTempLabel.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)

        gridLayout.addWidget(cpuCurrentTempLabel, 3, 2)

        cpuTempSeparatorLabel = QtWidgets.QLabel('/')
        self.commom.setLabel(cpuTempSeparatorLabel, self.commom.white, self.commom.fontDefault)
        cpuTempSeparatorLabel.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        self.systemWidgets['cpuTempSeparatorLabel'] = cpuTempSeparatorLabel

        gridLayout.addWidget(cpuTempSeparatorLabel, 3, 3)

        cpuTempMaxLabel = QtWidgets.QLabel('100.0 °C')
        self.commom.setLabel(cpuTempMaxLabel, self.commom.red, self.commom.fontDefault)
        cpuTempMaxLabel.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        self.systemWidgets['cpuTempMaxLabel'] = cpuTempMaxLabel

        gridLayout.addWidget(cpuTempMaxLabel, 3, 4)

        verticalLayout.addLayout(gridLayout)

        # --------------------------------------------------------------------------------------------------
        systemGroupBox.setLayout(verticalLayout)
        self.hideWidgetByDefault()

        return systemGroupBox

    def hideWidgetByDefault(self):
        # --------------------------------------------------------------------------------------------------
        # Hide by default
        self.systemWidgets['cpuTempIcon'].hide()
        self.systemWidgets['cpuTempProgressBar'].hide()
        self.systemWidgets['cpuCurrentTempLabel'].hide()
        self.systemWidgets['cpuTempSeparatorLabel'].hide()
        self.systemWidgets['cpuTempMaxLabel'].hide()

    def showWidgetByDefault(self):
        # --------------------------------------------------------------------------------------------------
        # Hide by default
        self.systemWidgets['cpuTempIcon'].show()
        self.systemWidgets['cpuTempProgressBar'].show()
        self.systemWidgets['cpuCurrentTempLabel'].show()
        self.systemWidgets['cpuTempSeparatorLabel'].show()
        self.systemWidgets['cpuTempMaxLabel'].show()
