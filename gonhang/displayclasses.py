from PyQt5 import QtWidgets, QtCore, QtGui
from gonhang import core
from gonhang import api
import humanfriendly
from gonhang.core import Config
from gonhang.api import FileUtil
from gonhang.core import StorTemps
from gonhang.core import Partitions
import os
import gettext

localedir = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'locale')
translate = gettext.translation('gonhang', localedir, fallback=True)
_ = translate.gettext


class AboutBox(QtWidgets.QDialog):
    config = Config()

    def __init__(self, parent=None):
        super(AboutBox, self).__init__(parent)
        self.setFixedWidth(480)
        self.centerMe()
        self.setWindowTitle(_('GonhaNG - Next Generation') + f' - {self.config.getVersion()}')
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
        versionLabel = QtWidgets.QLabel(_('Version') + f' <strong>{self.config.getVersion()}</strong>')
        versionLabel.setTextFormat(QtCore.Qt.RichText)
        versionLabel.setAlignment(alignCenter)
        self.layout.addWidget(versionLabel)
        # contributors text
        contHeader = QtWidgets.QLabel(_('Contributors'))
        contHeader.setAlignment(QtCore.Qt.AlignHCenter)
        cont1 = QtWidgets.QLabel('<a href="https://github.com/fredcox">Fred Lins</a>')
        cont1.setAlignment(QtCore.Qt.AlignHCenter)
        cont2 = QtWidgets.QLabel('<a href="https://github.com/fagianijunior">Carlos Fagiani Junior</a>')
        cont2.setAlignment(QtCore.Qt.AlignHCenter)
        cont3 = QtWidgets.QLabel('<a href="https://t.me/@GeraldoSSK">Geraldo S. Simião Kutz</a>')
        cont3.setAlignment(QtCore.Qt.AlignHCenter)
        self.layout.addWidget(contHeader)
        self.layout.addWidget(cont1)
        self.layout.addWidget(cont2)
        self.layout.addWidget(cont3)

        # warrantyText
        textAboutLabel = QtWidgets.QLabel(_('This program comes with absolutely no warranty'))
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
    debugRed = 'background-color: rgb(255, 48, 79);'

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
        self.rgbColorYellow = QtGui.QColor(255, 153, 0)
        self.rgbColorGreen = QtGui.QColor(34, 255, 19)
        self.rgbColorRed = QtGui.QColor(255, 51, 0)

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
        if value < 40:
            pb.setStyleSheet(self.greenPBStyle)
        elif (value >= 40) and (value < 70):
            pb.setStyleSheet(self.yellowPBStyle)
        elif value >= 70:
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

    @staticmethod
    def displayRow(optionsList, value):
        rowCount = optionsList.count()
        for i in range(rowCount):
            rowText = optionsList.item(i).text()
            rowList = rowText.split('|')
            if str(value) == str(rowList[0]):
                optionsList.setCurrentRow(i)

    def makePartitionPB(self):
        Pb = QtWidgets.QProgressBar()
        Pb.setFixedHeight(20)
        Pb.setFont(self.fontDefault)
        Pb.setStyleSheet(self.greenPBStyle)
        Pb.setFixedWidth(260)
        Pb.setValue(100)
        return Pb


class DisplaySystem:
    commom = CommomAttributes()
    systemWidgets = dict()
    system = core.System()

    def initUi(self, vLayout):
        pbDefaultWidth = 200
        iconDefaultWidth = 48
        message = self.system.getMessage()
        systemGroupBox = self.commom.getDefaultGb(_('system'))

        localVLayout = QtWidgets.QVBoxLayout()
        localVLayout.setSpacing(0)

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

        localVLayout.addLayout(distroGridLayout)
        # ---------------------------------------------------------------------------
        # boot time label
        # verticalLayout.addLayout(distroGridLayout)

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

        daysLabel = QtWidgets.QLabel(_('days, '))
        self.commom.setLabel(daysLabel, self.commom.white, self.commom.fontDefault)
        btHLayout.addWidget(daysLabel)

        btHoursLabel = QtWidgets.QLabel(f"{message['btHours']} ")
        self.commom.setLabel(btHoursLabel, self.commom.green, self.commom.fontDefault)
        btHLayout.addWidget(btHoursLabel)
        self.systemWidgets['btHours'] = btHoursLabel

        hoursLabel = QtWidgets.QLabel(_('hours '))
        self.commom.setLabel(hoursLabel, self.commom.white, self.commom.fontDefault)
        btHLayout.addWidget(hoursLabel)

        btMinutesLabel = QtWidgets.QLabel(f"{message['btMinutes']} ")
        self.commom.setLabel(btMinutesLabel, self.commom.green, self.commom.fontDefault)
        btHLayout.addWidget(btMinutesLabel)
        self.systemWidgets['btMinutes'] = btMinutesLabel

        minutesLabel = QtWidgets.QLabel(_('minutes '))
        self.commom.setLabel(minutesLabel, self.commom.white, self.commom.fontDefault)
        btHLayout.addWidget(minutesLabel)

        btSecondsLabel = QtWidgets.QLabel(f"{message['btSeconds']} ")
        self.commom.setLabel(btSecondsLabel, self.commom.green, self.commom.fontDefault)
        btHLayout.addWidget(btSecondsLabel)
        self.systemWidgets['btSeconds'] = btSecondsLabel

        secondsLabel = QtWidgets.QLabel(_('seconds'))
        self.commom.setLabel(secondsLabel, self.commom.white, self.commom.fontDefault)
        btHLayout.addWidget(secondsLabel)

        bootAndCpuModelLayout.addLayout(btHLayout)

        localVLayout.addLayout(bootAndCpuModelLayout)
        # ---------------------------------------------------------------------------
        # CPU info
        cpuBrandLabel = QtWidgets.QLabel(self.system.getCpuModelName())
        self.commom.setLabel(cpuBrandLabel, self.commom.white, self.commom.fontDefault)
        cpuBrandLabel.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)

        bootAndCpuModelLayout.addWidget(cpuBrandLabel)

        # verticalLayout.addLayout(bootAndCpuModelLayout)
        # ---------------------------------------------------------------------------
        # Cpu load

        gridLayout = QtWidgets.QGridLayout()
        cpuIcon = QtWidgets.QLabel()
        cpuIcon.setPixmap(QtGui.QPixmap(f"{api.FileUtil.getResourcePath()}/images/cpu.png"))
        cpuIcon.setFixedWidth(iconDefaultWidth)

        gridLayout.addWidget(cpuIcon, 0, 0)

        # cpuProgressBar = QtWidgets.QProgressBar()
        cpuProgressBar = QtWidgets.QProgressBar()
        cpuProgressBar.setFixedHeight(self.commom.pbDefaultHeight)
        cpuProgressBar.setFixedWidth(pbDefaultWidth)
        # cpuProgressBar.setFont(self.commom.fontDefault)
        # cpuProgressBar.setStyleSheet(self.commom.greenPBStyle)
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

        # ramProgressBar = QtWidgets.QProgressBar()
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

        # verticalLayout.addLayout(gridLayout)

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
        tempProgressBar.setFormat('%p°C')
        tempProgressBar.setStyleSheet(self.commom.greenPBStyle)
        self.systemWidgets['cpuTempProgressBar'] = tempProgressBar
        tempProgressBar.setValue(30)

        gridLayout.addWidget(tempProgressBar, 3, 1)

        cpuCurrentTempLabel = QtWidgets.QLabel()
        self.commom.setLabel(cpuCurrentTempLabel, self.commom.white, self.commom.fontDefault)
        self.systemWidgets['cpuCurrentTempLabel'] = cpuCurrentTempLabel
        cpuCurrentTempLabel.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)

        gridLayout.addWidget(cpuCurrentTempLabel, 3, 2)

        cpuTempSeparatorLabel = QtWidgets.QLabel('/')
        self.commom.setLabel(cpuTempSeparatorLabel, self.commom.white, self.commom.fontDefault)
        cpuTempSeparatorLabel.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        self.systemWidgets['cpuTempSeparatorLabel'] = cpuTempSeparatorLabel

        gridLayout.addWidget(cpuTempSeparatorLabel, 3, 3)

        cpuTempLabel = QtWidgets.QLabel()
        self.commom.setLabel(cpuTempLabel, self.commom.green, self.commom.fontDefault)
        cpuTempLabel.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        self.systemWidgets['cpuTempLabel'] = cpuTempLabel

        gridLayout.addWidget(cpuTempLabel, 3, 4)

        # vLayout.addLayout(gridLayout)

        localVLayout.addLayout(gridLayout)

        systemGroupBox.setLayout(localVLayout)

        vLayout.addWidget(systemGroupBox)
        # --------------------------------------------------------------------------------------------------
        # systemGroupBox.setLayout(vLayout)
        self.hideWidgetByDefault()

        return systemGroupBox

    def hideWidgetByDefault(self):
        # --------------------------------------------------------------------------------------------------
        # Hide by default
        self.systemWidgets['cpuTempIcon'].hide()
        self.systemWidgets['cpuTempProgressBar'].hide()
        self.systemWidgets['cpuCurrentTempLabel'].hide()
        self.systemWidgets['cpuTempSeparatorLabel'].hide()
        self.systemWidgets['cpuTempLabel'].hide()

    def showWidgetByDefault(self):
        # --------------------------------------------------------------------------------------------------
        # Hide by default
        self.systemWidgets['cpuTempIcon'].show()
        self.systemWidgets['cpuTempProgressBar'].show()
        self.systemWidgets['cpuCurrentTempLabel'].show()
        self.systemWidgets['cpuTempSeparatorLabel'].show()
        self.systemWidgets['cpuTempLabel'].show()


class DisplayNvidia:
    common = CommomAttributes()
    nvidiaWidgets = dict()

    def initUi(self, verticalLayout):
        nvidiaGroupBox = self.common.getDefaultGb('nvidia')
        self.nvidiaWidgets['nvidiaGroupBox'] = nvidiaGroupBox
        gridLayout = QtWidgets.QGridLayout()
        gridLayout.setVerticalSpacing(1)
        gridLayout.setHorizontalSpacing(0)
        # ---------------------------------------------------
        # nvidia data

        nvidiaLogoLabel = QtWidgets.QLabel()
        nvidiaLogoLabel.setPixmap(QtGui.QPixmap(f"{FileUtil.getResourcePath()}/images/nvidia.png"))
        nvidiaLogoLabel.setFixedSize(64, 90)
        nvidiaLogoLabel.setAlignment(QtCore.Qt.AlignTop)

        gridLayout.addWidget(nvidiaLogoLabel, 0, 0, -1, 1)

        modelLabel = QtWidgets.QLabel(_('model:'))
        self.common.setLabel(modelLabel, self.common.orange, self.common.fontDefault)
        # noinspection PyTypeChecker
        modelLabel.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)

        gridLayout.addWidget(modelLabel, 0, 1)

        modelValueLabel = QtWidgets.QLabel()
        self.nvidiaWidgets['gpu_name'] = modelValueLabel
        modelValueLabel.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.common.setLabel(modelValueLabel, self.common.white, self.common.fontDefault)

        gridLayout.addWidget(modelValueLabel, 0, 2)

        loadIcon = QtWidgets.QLabel()
        loadIcon.setPixmap(QtGui.QPixmap(f'{FileUtil.getResourcePath()}/images/load.png'))
        loadIcon.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        loadIcon.setFixedSize(24, 24)

        gridLayout.addWidget(loadIcon, 0, 3)

        loadValueLabel = QtWidgets.QLabel()
        self.nvidiaWidgets['utilization_gpu'] = loadValueLabel
        loadValueLabel.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        loadValueLabel.setFixedWidth(80)
        self.common.setLabel(loadValueLabel, self.common.white, self.common.fontDefault)

        gridLayout.addWidget(loadValueLabel, 0, 4)

        memoryLabel = QtWidgets.QLabel(_('memory:'))
        memoryLabel.setFixedWidth(70)
        self.common.setLabel(memoryLabel, self.common.orange, self.common.fontDefault)
        memoryLabel.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)

        gridLayout.addWidget(memoryLabel, 1, 1)

        usedTotalMemLabel = QtWidgets.QLabel()
        self.nvidiaWidgets['usedTotalMemory'] = usedTotalMemLabel
        self.common.setLabel(usedTotalMemLabel, self.common.white, self.common.fontDefault)
        usedTotalMemLabel.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)

        gridLayout.addWidget(usedTotalMemLabel, 1, 2)

        tempIcon = QtWidgets.QLabel()
        tempIcon.setPixmap(QtGui.QPixmap(f'{FileUtil.getResourcePath()}/images/temp.png'))
        tempIcon.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        tempIcon.setFixedSize(24, 24)

        gridLayout.addWidget(tempIcon, 1, 3)

        tempLabel = QtWidgets.QLabel('')
        self.nvidiaWidgets['temperature_gpu'] = tempLabel
        tempLabel.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        self.common.setLabel(tempLabel, self.common.white, self.common.fontDefault)
        tempLabel.setFixedWidth(80)

        gridLayout.addWidget(tempLabel, 1, 4)

        # Driver Version

        driverLabel = QtWidgets.QLabel('driver:')
        self.common.setLabel(driverLabel, self.common.orange, self.common.fontDefault)
        driverLabel.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)

        gridLayout.addWidget(driverLabel, 2, 1)

        driverValueLabel = QtWidgets.QLabel()
        self.common.setLabel(driverValueLabel, self.common.white, self.common.fontDefault)
        driverValueLabel.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.nvidiaWidgets['driverValueLabel'] = driverValueLabel

        gridLayout.addWidget(driverValueLabel, 2, 2)

        fanIcon = QtWidgets.QLabel()
        fanIcon.setPixmap(QtGui.QPixmap(f'{FileUtil.getResourcePath()}/images/fan.png'))
        fanIcon.setAlignment(QtCore.Qt.AlignHCenter)
        fanIcon.setFixedSize(24, 24)

        gridLayout.addWidget(fanIcon, 2, 3)

        fanValueLabel = QtWidgets.QLabel()
        self.common.setLabel(fanValueLabel, self.common.white, self.common.fontDefault)
        fanValueLabel.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        fanValueLabel.setFixedWidth(80)

        self.nvidiaWidgets['fan_speed'] = fanValueLabel

        gridLayout.addWidget(fanValueLabel, 2, 4)

        # bios
        biosLabel = QtWidgets.QLabel('bios:')
        self.common.setLabel(biosLabel, self.common.orange, self.common.fontDefault)
        biosLabel.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)

        gridLayout.addWidget(biosLabel, 3, 1)

        biosValueLabel = QtWidgets.QLabel()
        self.common.setLabel(biosValueLabel, self.common.white, self.common.fontDefault)
        biosValueLabel.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.nvidiaWidgets['biosValueLabel'] = biosValueLabel

        gridLayout.addWidget(biosValueLabel, 3, 2)

        powerIcon = QtWidgets.QLabel()
        powerIcon.setPixmap(QtGui.QPixmap(f'{FileUtil.getResourcePath()}/images/power.png'))
        powerIcon.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        powerIcon.setFixedSize(24, 24)

        gridLayout.addWidget(powerIcon, 3, 3)

        powerDrawLabel = QtWidgets.QLabel()
        self.common.setLabel(powerDrawLabel, self.common.white, self.common.fontDefault)
        powerDrawLabel.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        powerDrawLabel.setFixedWidth(80)
        self.nvidiaWidgets['power_draw'] = powerDrawLabel

        gridLayout.addWidget(powerDrawLabel, 3, 4)

        nvidiaGroupBox.setLayout(gridLayout)
        nvidiaGroupBox.hide()
        self.nvidiaWidgets['nvidiaGroupBox'].setFixedHeight(130)

        verticalLayout.addWidget(nvidiaGroupBox)


class DisplayNet:
    common = CommomAttributes()
    netWidgets = dict()

    def initUi(self, vLayout):
        verticalLayout = QtWidgets.QVBoxLayout()
        netGroupBox = self.common.getDefaultGb(_('net'))
        self.netWidgets['netGroupBox'] = netGroupBox
        rateLabelWidth = 120
        # ---------------------------------------------------
        # Ip int Label
        ipLayout = QtWidgets.QGridLayout()
        intipLabel = QtWidgets.QLabel('int:')
        self.common.setLabel(intipLabel, self.common.orange, self.common.fontDefault)

        ipLayout.addWidget(intipLabel, 0, 0)

        # ip int value label
        intipValueLabel = QtWidgets.QLabel('')
        self.common.setLabel(intipValueLabel, self.common.white, self.common.fontDefault)
        self.netWidgets['intipLabel'] = intipValueLabel

        ipLayout.addWidget(intipValueLabel, 0, 1)

        # Ext Ip
        extipLabel = QtWidgets.QLabel('ext:')
        self.common.setLabel(extipLabel, self.common.orange, self.common.fontDefault)

        ipLayout.addWidget(extipLabel, 0, 2)

        extipValueLabel = QtWidgets.QLabel('')
        self.common.setLabel(extipValueLabel, self.common.white, self.common.fontDefault)
        self.netWidgets['extipLabel'] = extipValueLabel

        ipLayout.addWidget(extipValueLabel, 0, 3)

        verticalLayout.addLayout(ipLayout)

        # -------------------------------------------------

        netGridLayout = QtWidgets.QGridLayout()

        netCardIcon = QtWidgets.QLabel()
        netCardIcon.setPixmap(QtGui.QPixmap(f"{FileUtil.getResourcePath()}/images/netcard.png"))
        netCardIcon.setFixedSize(24, 24)

        netGridLayout.addWidget(netCardIcon, 0, 0)

        # -------------------------------------------------
        # interface ValueLabel
        ifaceValueLabel = QtWidgets.QLabel('')
        ifaceValueLabel.setTextFormat(QtCore.Qt.RichText)
        self.common.setLabel(ifaceValueLabel, self.common.white, self.common.fontDefault)
        self.netWidgets['ifaceValueLabel'] = ifaceValueLabel
        ifaceValueLabel.setFixedWidth(80)

        netGridLayout.addWidget(ifaceValueLabel, 0, 1)

        # -------------------------------------------------
        # Download Icon
        downloadIcon = QtWidgets.QLabel()
        downloadIcon.setPixmap(QtGui.QPixmap(f'{FileUtil.getResourcePath()}/images/download.png'))
        downloadIcon.setFixedSize(24, 24)

        netGridLayout.addWidget(downloadIcon, 0, 2)

        # ---------------------------------------------------
        # download rate label
        ifaceDownRateLabel = QtWidgets.QLabel('')
        self.common.setLabel(ifaceDownRateLabel, self.common.white, self.common.fontDefault)
        self.netWidgets['ifaceDownRateLabel'] = ifaceDownRateLabel
        ifaceDownRateLabel.setFixedWidth(rateLabelWidth)
        ifaceDownRateLabel.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)

        netGridLayout.addWidget(ifaceDownRateLabel, 0, 3)
        # ---------------------------------------------------

        # -------------------------------------------------
        # Upload Icon
        uploadIcon = QtWidgets.QLabel()
        uploadIcon.setPixmap(QtGui.QPixmap(f'{FileUtil.getResourcePath()}/images/upload.png'))
        uploadIcon.setFixedSize(24, 24)

        netGridLayout.addWidget(uploadIcon, 0, 4)
        # -------------------------------------------------

        # ---------------------------------------------------
        # upload rate label
        ifaceUpRateLabel = QtWidgets.QLabel('')
        self.common.setLabel(ifaceUpRateLabel, self.common.white, self.common.fontDefault)
        self.netWidgets['ifaceUpRateLabel'] = ifaceUpRateLabel
        ifaceUpRateLabel.setFixedWidth(rateLabelWidth)
        ifaceUpRateLabel.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)

        netGridLayout.addWidget(ifaceUpRateLabel, 0, 5)

        verticalLayout.addLayout(netGridLayout)

        # ---------------------------------------------------

        # Total in

        bytesLayout = QtWidgets.QGridLayout()

        bytesRcvLabel = QtWidgets.QLabel(_('total in:'))
        self.common.setLabel(bytesRcvLabel, self.common.orange, self.common.fontDefault)

        bytesLayout.addWidget(bytesRcvLabel, 0, 0)

        bytesRcvValueLabel = QtWidgets.QLabel('')
        bytesRcvValueLabel.setTextFormat(QtCore.Qt.RichText)
        self.common.setLabel(bytesRcvValueLabel, self.common.white, self.common.fontDefault)
        self.netWidgets['bytesRcvValueLabel'] = bytesRcvValueLabel

        bytesLayout.addWidget(bytesRcvValueLabel, 0, 1)

        # Total out
        bytesSentLabel = QtWidgets.QLabel(_('total out:'))
        self.common.setLabel(bytesSentLabel, self.common.orange, self.common.fontDefault)

        bytesLayout.addWidget(bytesSentLabel, 0, 2)

        bytesSentValueLabel = QtWidgets.QLabel('')
        bytesSentValueLabel.setTextFormat(QtCore.Qt.RichText)
        self.common.setLabel(bytesSentValueLabel, self.common.white, self.common.fontDefault)
        self.netWidgets['bytesSentValueLabel'] = bytesSentValueLabel

        bytesLayout.addWidget(bytesSentValueLabel, 0, 3)

        verticalLayout.addLayout(bytesLayout)

        netGroupBox.setFixedHeight(120)
        netGroupBox.setLayout(verticalLayout)
        netGroupBox.hide()

        vLayout.addWidget(netGroupBox)


class DisplayStorages(QtCore.QThread):
    storTemps = StorTemps()
    partitions = Partitions()
    config = Config()
    common = CommomAttributes()
    storTempsWidgets = list()
    partitionsWidgets = list()
    firstPass = False
    storageGroupBox = None
    configCacheStamp = 0
    signal = QtCore.pyqtSignal(bool, name='DisplayStorageFinish')
    groupBoxHeight = 0
    storTempsHeightStep = 40
    partitionsHeightStep = 30

    def __init__(self, parent=None):
        super(DisplayStorages, self).__init__(parent)
        self.finished.connect(self.myFinish)
        self.signal.connect(self.storTempsReceive)

    def myFinish(self):
        self.start()

    def storTempsReceive(self):
        self.hideStorTempsWidgets()
        self.hidePartTempsWidgets()
        self.groupBoxHeight = 0
        if self.storTemps.isToDisplay() or self.partitions.isToDisplay():
            self.storageGroupBox.show()
            if self.storTemps.isToDisplay():
                self.updateStorTempsUi()

            if self.partitions.isToDisplay():
                self.updatePartitionsUi()

            self.storageGroupBox.setFixedHeight(self.groupBoxHeight)
        else:
            self.storageGroupBox.hide()

    def initUi(self, vLayout):
        pbDefaultwith = 250
        localVLayout = QtWidgets.QVBoxLayout()
        self.storageGroupBox = self.common.getDefaultGb(_('disks'))
        gridLayout = QtWidgets.QGridLayout()
        for line in range(10):
            colList = list()
            ssdIcon = QtWidgets.QLabel()
            ssdIcon.setPixmap(QtGui.QPixmap(f'{FileUtil.getResourcePath()}/images/ssd.png'))
            ssdIcon.setFixedSize(24, 24)
            gridLayout.addWidget(ssdIcon, line, 0)
            colList.append(ssdIcon)

            device = QtWidgets.QLabel('/dev/teste')
            device.setFixedWidth(80)
            self.common.setLabel(device, self.common.white, self.common.fontDefault)
            gridLayout.addWidget(device, line, 1)
            colList.append(device)

            deviceLabel = QtWidgets.QLabel('label')
            self.common.setLabel(deviceLabel, self.common.white, self.common.fontDefault)
            gridLayout.addWidget(deviceLabel, line, 2)
            colList.append(deviceLabel)

            tempIcon = QtWidgets.QLabel()
            tempIcon.setPixmap(QtGui.QPixmap(f'{FileUtil.getResourcePath()}/images/temp.png'))
            tempIcon.setFixedHeight(24)
            tempIcon.setFixedWidth(24)
            gridLayout.addWidget(tempIcon, line, 3)
            colList.append(tempIcon)

            deviceTempLabel = QtWidgets.QLabel('temp oC')
            deviceTempLabel.setTextFormat(QtCore.Qt.RichText)
            self.common.setLabel(deviceTempLabel, self.common.white, self.common.fontDefault)
            deviceTempLabel.setAlignment(QtCore.Qt.AlignRight)
            gridLayout.addWidget(deviceTempLabel, line, 4)
            colList.append(deviceTempLabel)
            deviceTempLabel.setFixedWidth(70)

            self.storTempsWidgets.append(colList)

        # -------------------------------------------------------------------------
        # now, i will display partitions widgets
        partGridLayout = QtWidgets.QGridLayout()
        for i in range(0, 20, 3):
            partColList = list()

            fsTypeLabel = QtWidgets.QLabel('fsType')
            self.common.setLabel(fsTypeLabel, self.common.white, self.common.fontDefault)
            fsTypeLabel.setAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignLeft)
            fsTypeLabel.setFixedWidth(60)
            partGridLayout.addWidget(fsTypeLabel, i, 0)
            partColList.append(fsTypeLabel)

            mountpointValueLabel = QtWidgets.QLabel('mountpoint')
            mountpointValueLabel.setAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignHCenter)
            self.common.setLabel(mountpointValueLabel, self.common.white, self.common.fontDefault)
            mountpointValueLabel.setFixedWidth(pbDefaultwith)
            partGridLayout.addWidget(mountpointValueLabel, i, 1)
            partColList.append(mountpointValueLabel)

            totalValueLabel = QtWidgets.QLabel('total')
            self.common.setLabel(totalValueLabel, self.common.white, self.common.fontDefault)
            totalValueLabel.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
            partGridLayout.addWidget(totalValueLabel, i, 2)
            partColList.append(totalValueLabel)

            # ----------------------------------------------------------
            # used stats
            usedLabel = QtWidgets.QLabel(_('used:'))
            self.common.setLabel(usedLabel, self.common.red, self.common.fontDefault)
            usedLabel.setFixedWidth(60)
            partGridLayout.addWidget(usedLabel, i + 1, 0)
            partColList.append(usedLabel)

            # ProgressBar
            # usedPB = self.common.makePartitionPB()
            usedPB = QtWidgets.QProgressBar()
            usedPB.setStyleSheet(self.common.redPBStyle)
            usedPB.setFixedWidth(pbDefaultwith)
            usedPB.setFixedHeight(self.common.pbDefaultHeight)
            # usedPB.setStyleSheet(self.common.redPBStyle)
            partGridLayout.addWidget(usedPB, i + 1, 1)
            partColList.append(usedPB)

            usedValueLabel = QtWidgets.QLabel('used')
            self.common.setLabel(usedValueLabel, self.common.white, self.common.fontDefault)
            usedValueLabel.setStyleSheet(self.common.red)
            usedValueLabel.setAlignment(QtCore.Qt.AlignRight)
            partGridLayout.addWidget(usedValueLabel, i + 1, 2)
            partColList.append(usedValueLabel)

            # ----------------------------------------------------------
            # free stats
            freeLabel = QtWidgets.QLabel(_('free:'))
            self.common.setLabel(freeLabel, self.common.green, self.common.fontDefault)
            freeLabel.setFixedWidth(60)
            partGridLayout.addWidget(freeLabel, i + 2, 0)
            partColList.append(freeLabel)

            # freePB = self.common.makePartitionPB()
            freePB = QtWidgets.QProgressBar()
            freePB.setStyleSheet(self.common.greenPBStyle)
            freePB.setFixedHeight(self.common.pbDefaultHeight)
            freePB.setFixedWidth(pbDefaultwith)
            partGridLayout.addWidget(freePB, i + 2, 1)
            partColList.append(freePB)

            freeValueLabel = QtWidgets.QLabel('free')
            self.common.setLabel(freeValueLabel, self.common.green, self.common.fontDefault)
            freeValueLabel.setAlignment(QtCore.Qt.AlignRight)
            partGridLayout.addWidget(freeValueLabel, i + 2, 2)
            partColList.append(freeValueLabel)
            # ----------------------------------------------------------
            self.partitionsWidgets.append(partColList)

        localVLayout.addLayout(gridLayout)
        localVLayout.addLayout(partGridLayout)
        self.storageGroupBox.setLayout(localVLayout)
        vLayout.addWidget(self.storageGroupBox)
        # --------------------------------------------------------------------------
        self.hideStorTempsWidgets()
        self.hidePartTempsWidgets()

    def run(self):
        # -----------------------------------------------------------------------------
        # Detect if config file changed and mount StorTemps on the fly
        # -----------------------------------------------------------------------------
        cfgCacheStamp = os.stat(self.config.cfgFile).st_mtime
        if cfgCacheStamp != self.configCacheStamp:
            self.configCacheStamp = cfgCacheStamp
            print(_('Config File Changed. New Time Stamp:') + f' {self.configCacheStamp}')
        # -----------------------------------------------------------------------------
        self.msleep(500)
        self.signal.emit(True)

    def hideStorTempsWidgets(self):
        for line in range(10):
            for col in range(5):
                self.storTempsWidgets[line][col].hide()

    def updateStorTempsUi(self):
        for line, device in enumerate(self.storTemps.getMessage()):
            for col in range(5):
                self.storTempsWidgets[line][col].show()

            self.storTempsWidgets[line][1].setText(device[0]['device'])
            self.storTempsWidgets[line][2].setText(device[0]['label'])
            self.storTempsWidgets[line][4].setText("{:.1f} °C".format(float(device[0]['temperature'])))
            self.common.analizeTemp(self.storTempsWidgets[line][4], float(device[0]['temperature']), 50, 70)
            self.groupBoxHeight = self.groupBoxHeight + self.storTempsHeightStep

    def hidePartTempsWidgets(self):
        for line in range(len(self.partitionsWidgets)):
            for col in range(len(self.partitionsWidgets[line])):
                self.partitionsWidgets[line][col].hide()

    def updatePartitionsUi(self):
        for line, message in enumerate(self.partitions.getMessage()):
            # print(f'line: {line} message: {message}')
            # print(len(self.partitionsWidgets[line]))
            for col in range(9):
                self.partitionsWidgets[line][col].show()

            self.partitionsWidgets[line][1].setText(message['mountpoint'])
            self.partitionsWidgets[line][0].setText(message['fstype'])

            total = message['total']
            used = message['used']
            free = total - used
            pUsed = int((used * 100) / total)

            pFree = 100 - pUsed

            # print(f'{pUsed} {pFree}')

            # self.partitionsWidgets[line][2].setText(humanfriendly.format_size(message['total'], binary=True))
            self.partitionsWidgets[line][2].setText(humanfriendly.format_size(total, binary=True))
            # pUsed, pFree = self.getPercents(message['percent'])
            self.partitionsWidgets[line][4].setValue(pUsed)
            # self.partitionsWidgets[line][5].setText(humanfriendly.format_size(message['used'], binary=True))
            self.partitionsWidgets[line][5].setText(humanfriendly.format_size(used, binary=True))
            self.partitionsWidgets[line][7].setValue(pFree)
            # self.partitionsWidgets[line][8].setText(humanfriendly.format_size(message['free'], binary=True))
            self.partitionsWidgets[line][8].setText(humanfriendly.format_size(free, binary=True))
            self.groupBoxHeight = self.groupBoxHeight + (self.partitionsHeightStep * 3)

    @staticmethod
    def getPercents(percent):
        pUsed = int(percent)
        pFree = 100 - pUsed
        return [pUsed, pFree]

        # return [int(percentFree), int((100 - percent)))]


class DisplayWeather:
    common = CommomAttributes()
    weatherWidgets = dict()

    def initUi(self, verticalLayout):
        weatherGroupBox = self.common.getDefaultGb(_('weather'))
        vLayout = QtWidgets.QVBoxLayout()
        vLayout.addSpacing(10)
        self.weatherWidgets['weatherGroupBox'] = weatherGroupBox
        timeHeight = 50
        dateHeight = 25
        tempHeight = 60

        timeFont = QtGui.QFont('Fira Code', 45)
        dayFont = QtGui.QFont('Fira Code', 20)
        weekdayFont = QtGui.QFont('Fira Code', 15)
        yearFont = QtGui.QFont('Fira Code', 12)
        monthFont = QtGui.QFont('Fira Code', 12)

        gray = 'color: rgb(143, 143, 143);'

        mainHBLayout = QtWidgets.QHBoxLayout()
        mainHBLayout.setSpacing(0)
        mainHBLayout.setAlignment(QtCore.Qt.AlignHCenter)

        # Horizontal Layout for time
        timeHBLayout = QtWidgets.QHBoxLayout()
        timeHBLayout.setAlignment(QtCore.Qt.AlignHCenter)

        twoPointLabel = [QtWidgets.QLabel(':'), QtWidgets.QLabel(':')]
        for label in twoPointLabel:
            label.setFont(timeFont)
            label.setStyleSheet(gray)
            label.setFixedHeight(timeHeight)

        hourLabel = QtWidgets.QLabel('22')
        self.common.setLabel(hourLabel, self.common.white, timeFont)
        hourLabel.setFixedHeight(timeHeight)
        self.weatherWidgets['hour'] = hourLabel

        minLabel = QtWidgets.QLabel('24')
        self.common.setLabel(minLabel, self.common.white, timeFont)
        minLabel.setFixedHeight(timeHeight)
        self.weatherWidgets['min'] = minLabel

        timeHBLayout.addWidget(hourLabel)
        timeHBLayout.addWidget(twoPointLabel[0])
        timeHBLayout.addWidget(minLabel)

        self.weatherWidgets['hour'] = hourLabel
        self.weatherWidgets['min'] = minLabel

        mainHBLayout.addLayout(timeHBLayout)

        # date vertical layout
        dateVBLayout = QtWidgets.QVBoxLayout()
        # date horizontal layout
        dateHBLayout = QtWidgets.QHBoxLayout()
        dateHBLayout.setAlignment(QtCore.Qt.AlignLeft)

        dayLabel = QtWidgets.QLabel('05')
        self.common.setLabel(dayLabel, self.common.orange, dayFont)
        dayLabel.setFixedHeight(dateHeight)

        monthLabel = QtWidgets.QLabel('June')
        self.common.setLabel(monthLabel, self.common.orange, monthFont)
        monthLabel.setFixedHeight(dateHeight)
        monthLabel.setAlignment(QtCore.Qt.AlignBottom)

        yearLabel = QtWidgets.QLabel('2020')
        yearLabel.setFont(yearFont)
        yearLabel.setStyleSheet(self.common.white)
        self.common.setLabel(yearLabel, self.common.orange, yearFont)
        yearLabel.setFixedHeight(dateHeight)
        yearLabel.setAlignment(QtCore.Qt.AlignBottom)

        dateHBLayout.addWidget(dayLabel)
        dateHBLayout.addWidget(monthLabel)
        dateHBLayout.addWidget(yearLabel)
        self.weatherWidgets['day'] = dayLabel
        self.weatherWidgets['month'] = monthLabel
        self.weatherWidgets['year'] = yearLabel

        dateVBLayout.addLayout(dateHBLayout)

        weekdayHBLayout = QtWidgets.QHBoxLayout()

        weekdayLabel = QtWidgets.QLabel('Saturday')
        self.common.setLabel(weekdayLabel, self.common.orange, weekdayFont)
        weekdayLabel.setFixedHeight(20)

        weekdayHBLayout.addWidget(weekdayLabel)
        self.weatherWidgets['weekday'] = weekdayLabel

        # --------------------------------------------------------------------
        # Weather
        weatherHBLayout = QtWidgets.QHBoxLayout()

        weatherVBLayout = QtWidgets.QVBoxLayout()
        weatherVBLayout.setSpacing(0)
        weatherVBLayout.setAlignment(QtCore.Qt.AlignVCenter)

        tempLabel = QtWidgets.QLabel('27°C')
        self.common.setLabel(tempLabel, self.common.white, timeFont)
        tempLabel.setFixedHeight(tempHeight)
        self.weatherWidgets['temp'] = tempLabel

        weatherHBLayout.addWidget(tempLabel)

        # Cloud Icon
        cloudIconLabel = QtWidgets.QLabel()
        cloudIconLabel.setPixmap(QtGui.QPixmap(f'{FileUtil.getResourcePath()}/images/weather_icon.png'))
        cloudIconLabel.setFixedHeight(42)
        cloudIconLabel.setFixedHeight(tempHeight)
        self.weatherWidgets['cloudicon'] = cloudIconLabel

        weatherHBLayout.addWidget(cloudIconLabel)
        weatherHBLayout.setAlignment(QtCore.Qt.AlignHCenter)

        nameLabel = QtWidgets.QLabel('Recife')
        self.common.setLabel(nameLabel, self.common.orange, self.common.fontDefault)
        self.weatherWidgets['name'] = nameLabel

        countryLabel = QtWidgets.QLabel('BR')
        self.common.setLabel(countryLabel, self.common.white, self.common.fontDefault)
        self.weatherWidgets['country'] = countryLabel

        weatherVBLayout.addWidget(nameLabel)
        weatherVBLayout.addWidget(countryLabel)

        weatherHBLayout.addLayout(weatherVBLayout)
        # ---------------------------------------------------------------------
        # humidity, pressure, visibility,  wind,
        weatherGridLayout = QtWidgets.QGridLayout()
        weatherGridLayout.setSpacing(0)

        # humidityIcon
        humidityIcon = QtWidgets.QLabel()
        humidityIcon.setPixmap(QtGui.QPixmap(f'{FileUtil.getResourcePath()}/images/humidity.png'))
        humidityIcon.setFixedWidth(32)

        pressureIcon = QtWidgets.QLabel()
        pressureIcon.setPixmap(QtGui.QPixmap(f'{FileUtil.getResourcePath()}/images/pressure.png'))
        pressureIcon.setFixedWidth(32)

        visibilityIcon = QtWidgets.QLabel()
        visibilityIcon.setPixmap(QtGui.QPixmap(f'{FileUtil.getResourcePath()}/images/visibility.png'))
        visibilityIcon.setFixedWidth(32)

        windIcon = QtWidgets.QLabel()
        windIcon.setPixmap(QtGui.QPixmap(f'{FileUtil.getResourcePath()}/images/wind.png'))
        windIcon.setFixedWidth(32)

        weatherGridLayout.addWidget(humidityIcon, 0, 0, 1, 1, QtCore.Qt.AlignHCenter)
        weatherGridLayout.addWidget(pressureIcon, 0, 1, 1, 1, QtCore.Qt.AlignHCenter)
        weatherGridLayout.addWidget(visibilityIcon, 0, 2, 1, 1, QtCore.Qt.AlignHCenter)
        weatherGridLayout.addWidget(windIcon, 0, 3, 1, 1, QtCore.Qt.AlignHCenter)
        # ---------------------------------------------------------------------

        humidityLabel = QtWidgets.QLabel('65%')
        self.common.setLabel(humidityLabel, self.common.white, self.common.fontDefault)
        self.weatherWidgets['humidity'] = humidityLabel

        pressureLabel = QtWidgets.QLabel('1014hPa')
        self.common.setLabel(pressureLabel, self.common.white, self.common.fontDefault)
        self.weatherWidgets['pressure'] = pressureLabel

        visibilityLabel = QtWidgets.QLabel('10.0Km')
        self.common.setLabel(visibilityLabel, self.common.white, self.common.fontDefault)
        self.weatherWidgets['visibility'] = visibilityLabel

        windLabel = QtWidgets.QLabel('7.7m/s SE')
        self.common.setLabel(windLabel, self.common.white, self.common.fontDefault)
        self.weatherWidgets['wind'] = windLabel

        weatherGridLayout.addWidget(humidityLabel, 1, 0, 1, 1, QtCore.Qt.AlignHCenter)
        weatherGridLayout.addWidget(pressureLabel, 1, 1, 1, 1, QtCore.Qt.AlignHCenter)
        weatherGridLayout.addWidget(visibilityLabel, 1, 2, 1, 1, QtCore.Qt.AlignHCenter)
        weatherGridLayout.addWidget(windLabel, 1, 3, 1, 1, QtCore.Qt.AlignHCenter)

        # vLayout.addLayout(weatherGridLayout)
        dateVBLayout.addLayout(weekdayHBLayout)
        mainHBLayout.addLayout(dateVBLayout)
        vLayout.addLayout(mainHBLayout)

        weatherGroupBox.setLayout(vLayout)
        vLayout.addLayout(weatherHBLayout)
        vLayout.addLayout(weatherGridLayout)

        verticalLayout.addWidget(weatherGroupBox)
