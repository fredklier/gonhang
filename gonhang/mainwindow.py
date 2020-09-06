import sys
import logging
from PyQt5 import QtWidgets, QtCore, QtGui
import subprocess
from gonhang.api import StringUtil
from gonhang.wizard import GonhaNgWizard
from gonhang.threads import ThreadSystem


class MainWindow(QtWidgets.QMainWindow):
    logger = logging.getLogger(__name__)
    wmctrlBin = subprocess.getoutput('which wmctrl')
    myWizard = None
    # -------------------------------------------------------------
    # Window Flags
    flags = QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnBottomHint | QtCore.Qt.Tool
    # -------------------------------------------------------------
    # Threads
    threadSystem = ThreadSystem()

    def __init__(self):
        super(MainWindow, self).__init__()
        self.logger.info('Start MainWindow')
        self.setWindowTitle(StringUtil.getRandomString(30))
        self.setWindowFlags(self.flags)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        # Global vertical Layout
        self.verticalLayout = QtWidgets.QVBoxLayout()
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
        # -------------------------------------------------------------
        self.verticalLayout.setAlignment(QtCore.Qt.AlignTop)
        # --------------------------------------------------------------

    def startAllThreads(self):
        # Connect thread signals and start
        self.threadSystem.signal.connect(self.threadSystemReceive)
        self.threadSystem.start()

    def getWindowCurrentId(self, windowTitle):
        self.logger.info(f'wmctrl binary found in : {self.wmctrlBin}')
        windowsList = subprocess.getoutput(f'{self.wmctrlBin} -l')
        windowsList = windowsList.split('\n')
        currentID = ''
        for window in windowsList:
            if windowTitle in window:
                wsplit = window.split()
                currentID = wsplit[0]

        return currentID

    def setWindowInEveryWorkspaces(self):
        # wmctrl -i -r 0x07a00006 -b add,sticky
        cmd = f'{self.wmctrlBin} -i -r {self.getWindowCurrentId(self.windowTitle())} -b add,sticky'
        subprocess.getoutput(cmd)

    def contextMenuEvent(self, event: QtGui.QContextMenuEvent):
        contextMenu = QtWidgets.QMenu(self)
        configAction = contextMenu.addAction('&Config')
        quitAction = contextMenu.addAction('&Quit')
        action = contextMenu.exec_(self.mapToGlobal(event.pos()))
        if action == quitAction:
            sys.exit()
        elif action == configAction:
            self.wizardAction()

    def wizardAction(self):
        self.logger.info('Enter in wizard...')
        self.myWizard = GonhaNgWizard(self)
        self.myWizard.show()

    def displaySystem(self):
        pbDefaultWidth = 180
        iconDefaultWidth = 80
        systemGroupBox = self.getDefaultGb('system')

        verticalLayout = QtWidgets.QVBoxLayout()
        verticalLayout.setSpacing(0)

        distroGridLayout = QtWidgets.QGridLayout()
        distroGridLayout.setAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignHCenter)
        distroGridLayout.setSpacing(0)
        # ---------------------------------------------------------------------------
        # distro Label
        # ---------------------------------------------------------------------------
        distroIcon = QtWidgets.QLabel()
        distroIcon.setPixmap(QtGui.QPixmap(self.distroUtil.getDistroIcon()))
        self.systemWidgets['distroIcon'] = distroIcon

        distroGridLayout.addWidget(distroIcon, 0, 0, -1, 1)

        # ---------------------------------------------------------------------------
        # Distro label
        distroLabel = QtWidgets.QLabel(self.distroUtil.getDistroStr())
        self.setLabel(distroLabel, self.white, self.fontDefault)
        self.systemWidgets['distroStr'] = distroLabel

        distroGridLayout.addWidget(distroLabel, 0, 1)

        # ---------------------------------------------------------------------------
        # kernel label
        kernelLabel = QtWidgets.QLabel(f"Kernel {self.platformUtil.getRelease()}")
        self.setLabel(kernelLabel, self.white, self.fontDefault)
        self.systemWidgets['release'] = kernelLabel

        distroGridLayout.addWidget(kernelLabel, 1, 1)
        # ---------------------------------------------------------------------------
        # Machine Label
        machineLabel = QtWidgets.QLabel(f"node {self.platformUtil.getNode()} arch {self.platformUtil.getMachine()}")
        self.setLabel(machineLabel, self.white, self.fontDefault)
        self.systemWidgets['nodeMachine'] = machineLabel

        distroGridLayout.addWidget(machineLabel, 2, 1)
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

        btDaysLabel = QtWidgets.QLabel('d')
        self.setLabel(btDaysLabel, self.green, self.fontDefault)
        btHLayout.addWidget(btDaysLabel)
        self.systemWidgets['btDays'] = btDaysLabel

        daysLabel = QtWidgets.QLabel('days, ')
        self.setLabel(daysLabel, self.white, self.fontDefault)
        btHLayout.addWidget(daysLabel)

        btHoursLabel = QtWidgets.QLabel('h')
        self.setLabel(btHoursLabel, self.green, self.fontDefault)
        btHLayout.addWidget(btHoursLabel)
        self.systemWidgets['btHours'] = btHoursLabel

        hoursLabel = QtWidgets.QLabel('hours ')
        self.setLabel(hoursLabel, self.white, self.fontDefault)
        btHLayout.addWidget(hoursLabel)

        btMinutesLabel = QtWidgets.QLabel('m')
        self.setLabel(btMinutesLabel, self.green, self.fontDefault)
        btHLayout.addWidget(btMinutesLabel)
        self.systemWidgets['btMinutes'] = btMinutesLabel

        minutesLabel = QtWidgets.QLabel('minutes ')
        self.setLabel(minutesLabel, self.white, self.fontDefault)
        btHLayout.addWidget(minutesLabel)

        btSecondsLabel = QtWidgets.QLabel('s')
        self.setLabel(btSecondsLabel, self.green, self.fontDefault)
        btHLayout.addWidget(btSecondsLabel)
        self.systemWidgets['btSeconds'] = btSecondsLabel

        secondsLabel = QtWidgets.QLabel('seconds')
        self.setLabel(secondsLabel, self.white, self.fontDefault)
        btHLayout.addWidget(secondsLabel)

        bootAndCpuModelLayout.addLayout(btHLayout)

        # ---------------------------------------------------------------------------
        cpuBrandLabel = QtWidgets.QLabel(self.config.getConfig('cpuinfo'))
        self.setLabel(cpuBrandLabel, self.white, self.fontDefault)
        cpuBrandLabel.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)

        bootAndCpuModelLayout.addWidget(cpuBrandLabel)

        verticalLayout.addLayout(bootAndCpuModelLayout)

        # Cpu load

        gridLayout = QtWidgets.QGridLayout()
        cpuIcon = QtWidgets.QLabel()
        cpuIcon.setPixmap(QtGui.QPixmap(f"{self.config.resource_path}/images/cpu.png"))
        cpuIcon.setFixedWidth(iconDefaultWidth)

        gridLayout.addWidget(cpuIcon, 0, 0)

        cpuProgressBar = QtWidgets.QProgressBar()
        cpuProgressBar.setFixedHeight(self.pbDefaultHeight)
        cpuProgressBar.setFont(self.fontDefault)
        cpuProgressBar.setStyleSheet(self.greenPBStyle)
        cpuProgressBar.setValue(12)
        self.systemWidgets['cpuProgressBar'] = cpuProgressBar

        gridLayout.addWidget(cpuProgressBar, 0, 1)

        cpuFreqCurrentLabel = QtWidgets.QLabel('')
        self.setLabel(cpuFreqCurrentLabel, self.white, self.fontDefault)
        self.systemWidgets['cpuFreqCurrent'] = cpuFreqCurrentLabel
        cpuFreqCurrentLabel.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)

        gridLayout.addWidget(cpuFreqCurrentLabel, 0, 2)

        cpuFreqSeparatorLabel = QtWidgets.QLabel('/')
        self.setLabel(cpuFreqSeparatorLabel, self.white, self.fontDefault)
        cpuFreqSeparatorLabel.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)

        gridLayout.addWidget(cpuFreqSeparatorLabel, 0, 3)

        cpuFreqMaxLabel = QtWidgets.QLabel('')
        self.setLabel(cpuFreqMaxLabel, self.green, self.fontDefault)
        cpuFreqMaxLabel.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        self.systemWidgets['cpuFreqMax'] = cpuFreqMaxLabel

        gridLayout.addWidget(cpuFreqMaxLabel, 0, 4)

        # ---------------------------------------------------------------------------
        # ram load

        ramIcon = QtWidgets.QLabel()
        ramIcon.setPixmap(QtGui.QPixmap(f"{self.config.resource_path}/images/ram.png"))

        gridLayout.addWidget(ramIcon, 1, 0)

        ramProgressBar = QtWidgets.QProgressBar()
        ramProgressBar.setFixedHeight(self.pbDefaultHeight)
        ramProgressBar.setFixedWidth(pbDefaultWidth)
        ramProgressBar.setFont(self.fontDefault)
        ramProgressBar.setStyleSheet(self.greenPBStyle)
        self.systemWidgets['ramProgressBar'] = ramProgressBar
        ramProgressBar.setValue(32)

        gridLayout.addWidget(ramProgressBar, 1, 1)

        ramUsedLabel = QtWidgets.QLabel('')
        self.setLabel(ramUsedLabel, self.white, self.fontDefault)
        self.systemWidgets['ramUsed'] = ramUsedLabel
        ramUsedLabel.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)

        gridLayout.addWidget(ramUsedLabel, 1, 2)

        ramSeparatorLabel = QtWidgets.QLabel('/')
        self.setLabel(ramSeparatorLabel, self.white, self.fontDefault)
        ramSeparatorLabel.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)

        gridLayout.addWidget(ramSeparatorLabel, 1, 3)

        ramTotalLabel = QtWidgets.QLabel('')
        self.setLabel(ramTotalLabel, self.green, self.fontDefault)
        self.systemWidgets['ramTotal'] = ramTotalLabel
        ramTotalLabel.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)

        gridLayout.addWidget(ramTotalLabel, 1, 4)

        # ---------------------------------------------------------------------------
        # swap load

        swapIcon = QtWidgets.QLabel()
        swapIcon.setPixmap(QtGui.QPixmap(f"{self.config.resource_path}/images/swap.png"))

        gridLayout.addWidget(swapIcon, 2, 0)

        swapProgressBar = QtWidgets.QProgressBar()
        swapProgressBar.setFixedHeight(self.pbDefaultHeight)
        swapProgressBar.setFixedWidth(pbDefaultWidth)
        swapProgressBar.setFont(self.fontDefault)
        swapProgressBar.setStyleSheet(self.greenPBStyle)
        self.systemWidgets['swapProgressBar'] = swapProgressBar
        swapProgressBar.setValue(52)

        gridLayout.addWidget(swapProgressBar, 2, 1)

        swapUsedLabel = QtWidgets.QLabel('')
        self.setLabel(swapUsedLabel, self.white, self.fontDefault)
        self.systemWidgets['swapUsed'] = swapUsedLabel
        swapUsedLabel.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)

        gridLayout.addWidget(swapUsedLabel, 2, 2)

        swapSeparatorLabel = QtWidgets.QLabel('/')
        self.setLabel(swapSeparatorLabel, self.white, self.fontDefault)
        swapSeparatorLabel.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)

        gridLayout.addWidget(swapSeparatorLabel, 2, 3)

        swapTotalLabel = QtWidgets.QLabel('')
        self.setLabel(swapTotalLabel, self.green, self.fontDefault)
        swapTotalLabel.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        self.systemWidgets['swapTotal'] = swapTotalLabel

        gridLayout.addWidget(swapTotalLabel, 2, 4)

        # ---------------------------------------------------------------------------
        # Temperature

        tempHLayout = QtWidgets.QHBoxLayout()
        tempHLayout.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)

        valueLabel = QtWidgets.QLabel('')
        self.systemWidgets['label'] = valueLabel
        self.setLabel(valueLabel, self.white, self.fontDefault)

        tempHLayout.addWidget(valueLabel)

        tempIcon = QtWidgets.QLabel()
        tempIcon.setPixmap(QtGui.QPixmap(f'{self.config.resource_path}/images/temp.png'))
        tempIcon.setFixedHeight(24)
        tempIcon.setFixedWidth(24)

        tempHLayout.addWidget(tempIcon)

        tempCurrentValueLabel = QtWidgets.QLabel('')
        self.setLabel(tempCurrentValueLabel, self.white, self.fontDefault)
        self.systemWidgets['current'] = tempCurrentValueLabel
        tempCurrentValueLabel.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)

        tempHLayout.addWidget(tempCurrentValueLabel)

        # ---------------------------------------------------------------------------
        verticalLayout.addLayout(gridLayout)
        verticalLayout.addLayout(tempHLayout)

        systemGroupBox.setLayout(verticalLayout)
        self.verticalLayout.addWidget(systemGroupBox)

    def threadSystemReceive(self, message):
        self.logger.info(f'Receive message => {message}')

    def getDefaultGb(self, title):
        defaultGb = QtWidgets.QGroupBox(title)
        defaultGb.setFont(self.fontGroupBox)
        defaultGb.setStyleSheet(self.groupBoxStyle)
        defaultGb.setFixedWidth(self.groupBoxDefaultWidth)
        return defaultGb
