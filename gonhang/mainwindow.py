from PyQt5 import QtWidgets, QtCore, QtGui
import subprocess
from gonhang.api import StringUtil
from gonhang.wizard import GonhaNgWizard
from gonhang.threads import ThreadSystem
from gonhang.threads import ThreadNvidia
from gonhang.displayclasses import DisplaySystem
from gonhang.displayclasses import DisplayNvidia
from gonhang.displayclasses import CommomAttributes
from gonhang.core import Config
from gonhang.systemtray import SystemTrayIcon
from gonhang.api import FileUtil
from gonhang.core import System
from gonhang.core import KeysSkeleton
from gonhang.displayclasses import AboutBox
import sys
import time


class MainWindow(QtWidgets.QMainWindow):
    config = Config()
    system = System()
    wmctrlBin = subprocess.getoutput('which wmctrl')
    myWizard = None
    app = QtWidgets.QApplication(sys.argv)
    keySkeleton = KeysSkeleton()
    # -------------------------------------------------------------
    # Display classes
    common = CommomAttributes()
    displaySystem = DisplaySystem()
    displayNvidia = DisplayNvidia()
    # -------------------------------------------------------------
    # Threads
    threadSystem = ThreadSystem()
    threadNvidia = ThreadNvidia()

    def __init__(self):
        super(MainWindow, self).__init__()
        print('Start MainWindow')
        self.setWindowTitle(StringUtil.getRandomString(30))
        # -------------------------------------------------------------
        # Window Flags
        self.windowFlags = QtCore.Qt.FramelessWindowHint
        self.windowFlags |= QtCore.Qt.WindowStaysOnBottomHint
        self.windowFlags |= QtCore.Qt.Tool
        self.setWindowFlags(self.windowFlags)
        # -------------------------------------------------------------
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        # Central Widget and Global vertical Layout
        centralWidget = QtWidgets.QWidget(self)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setAlignment(QtCore.Qt.AlignTop)
        centralWidget.setLayout(self.verticalLayout)
        self.setCentralWidget(centralWidget)
        # -----------------------------------------------------------------------------
        # Show Sections and initialize services
        self.showSections()
        self.show()
        time.sleep(1 / 50)
        self.setWindowInEveryWorkspaces()
        # -----------------------------------------------------------------------------

        self.systemTrayMenu = SystemTrayIcon(QtGui.QIcon(f'{FileUtil.getResourcePath()}/images/icon.png'), self)
        self.systemTrayMenu.show()
        self.aboutBox = AboutBox(self)

        # ----------------------------------------------------------------------------
        # start the threads
        print('Initializing Threads...')
        self.startAllThreads()

    def showAboutBox(self):
        # self.aboutBox.exec_()
        self.aboutBox.show()

    def showSections(self):
        self.loadGlobalParams()
        # self.verticalLayout.addWidget(self.displaySystem.initUi())
        self.displaySystem.initUi(self.verticalLayout)
        self.displayNvidia.initUi(self.verticalLayout)

    def loadGlobalParams(self):
        position = self.config.getKey('positionOption')
        if position is None:
            self.refreshPosition(0)
        else:
            self.refreshPosition(position['index'])

    def startAllThreads(self):
        # --------------------------------------------------------------------------------------
        # Connect thread signals and start
        self.threadSystem.signal.connect(self.threadSystemReceive)
        self.threadSystem.start()

        self.threadNvidia.signal.connect(self.threadNvidiaReceive)
        self.threadNvidia.start()
        # --------------------------------------------------------------------------------------

    def getWindowCurrentId(self, windowTitle):
        windowsList = subprocess.getoutput(f'{self.wmctrlBin} -l')
        windowsList = windowsList.split('\n')
        currentID = ''
        for window in windowsList:
            if windowTitle in window:
                wsplit = window.split()
                currentID = wsplit[0]

        return currentID

    def setWindowInEveryWorkspaces(self):
        cmd = f'{self.wmctrlBin} -i -r {self.getWindowCurrentId(self.windowTitle())} -b add,sticky'
        subprocess.getoutput(cmd)

    @staticmethod
    def getScreenGeometry():
        return QtWidgets.QApplication.desktop().screenGeometry()

    def refreshPosition(self, index):
        positions = [
            'Left',
            'Center',
            'Right'
        ]
        x = 0
        if index == 1:
            x = (self.getScreenGeometry().width() - self.geometry().width()) / 2
        elif index == 2:
            x = (self.getScreenGeometry().width() - self.geometry().width())

        self.move(x, 0)
        # --------------------------------------------------------------------------------------------
        # write to config
        self.keySkeleton.positionOption['positionOption']['index'] = index
        self.keySkeleton.positionOption['positionOption']['value'] = positions[index]
        self.config.updateConfig(self.keySkeleton.positionOption)
        # --------------------------------------------------------------------------------------------

    def wizardAction(self):
        print('Enter in wizard...')
        self.myWizard = GonhaNgWizard(self)
        self.myWizard.show()

    def threadNvidiaReceive(self, message):
        for i, msg in enumerate(message):
            self.displayNvidia.nvidiaWidgets[i]['gpu_name'].setText(msg['gpu_name'])
            self.displayNvidia.nvidiaWidgets[i]['utilization_gpu'].setText(f"{str(msg['utilization_gpu'])}")
            self.displayNvidia.nvidiaWidgets[i]['usedTotalMemory'].setText(f"{msg['memory_used']}/{msg['memory_total']}")
            self.displayNvidia.nvidiaWidgets[i]['power_draw'].setText(f"{msg['power_draw']}")
            self.displayNvidia.nvidiaWidgets[i]['fan_speed'].setText(f"{msg['fan_speed']}")
            self.displayNvidia.nvidiaWidgets[i]['temperature_gpu'].setText(
                f"{int(msg['temperature_gpu'])} °C")
            self.common.analizeTemp(self.displayNvidia.nvidiaWidgets[i]['temperature_gpu'], msg['temperature_gpu'],
                             msg['temperature_gpu_high'],
                             msg['temperature_gpu_critical'])

    def threadSystemReceive(self, message):
        # -----------------------------------------------------------------------------------------------------
        # System, release and node machine
        self.displaySystem.systemWidgets['distroStr'].setText(message['distroStr'])
        self.displaySystem.systemWidgets['release'].setText(f"Kernel {message['release']}")
        self.displaySystem.systemWidgets['nodeMachine'].setText(f"node {message['node']} arch {message['machine']}")
        # -----------------------------------------------------------------------------------------------------
        # boot time
        self.displaySystem.systemWidgets['btDays'].setText(f"{message['btDays']} ")
        self.displaySystem.systemWidgets['btHours'].setText(f"{message['btHours']} ")
        self.displaySystem.systemWidgets['btMinutes'].setText(f"{message['btMinutes']} ")
        self.displaySystem.systemWidgets['btSeconds'].setText(f"{message['btSeconds']} ")
        # -----------------------------------------------------------------------------------------------------
        # Cpu Load workout
        self.displaySystem.systemWidgets['cpuProgressBar'].setValue(message['cpuProgressBar'])
        self.common.analizeProgressBar(self.displaySystem.systemWidgets['cpuProgressBar'], message['cpuProgressBar'])
        self.displaySystem.systemWidgets['cpuFreqCurrent'].setText(f"{message['cpuFreqCurrent']} MHz")
        self.common.analizeValue(self.displaySystem.systemWidgets['cpuFreqCurrent'], message['cpuFreqCurrent'], message['cpuFreqMax'])
        # -----------------------------------------------------------------------------------------------------
        # Ram Load workout
        self.updateWorkOut(
            self.displaySystem.systemWidgets['ramProgressBar'],
            message['ramProgressBar'],
            self.displaySystem.systemWidgets['ramUsed'],
            message['ramUsed'],
            message['ramTotal']
        )
        # -----------------------------------------------------------------------------------------------------
        # swap Load workout
        self.updateWorkOut(
            self.displaySystem.systemWidgets['swapProgressBar'],
            message['swapProgressBar'],
            self.displaySystem.systemWidgets['swapUsed'],
            f"{message['swapUsed']}",
            message['swapTotal']
        )

        # ------------------------------------------------------------------------------------------------------
        # Verify if can display cpuTemp
        if self.system.isToDisplayCpuTemp():
            self.displaySystem.showWidgetByDefault()
            self.displaySystem.systemWidgets['cpuTempProgressBar'].setValue(message['cpuTempProgressBar'])
            self.common.analizeProgressBar(self.displaySystem.systemWidgets['cpuTempProgressBar'], message['cpuTempProgressBar'])
            self.displaySystem.systemWidgets['cpuCurrentTempLabel'].setText(f"{message['cpuCurrentTempLabel']} °C")
            self.common.analizeTemp(
                self.displaySystem.systemWidgets['cpuCurrentTempLabel'],
                float(message['cpuCurrentTempLabel']),
                75.0,
                85.0
            )
        else:
            self.displaySystem.hideWidgetByDefault()
        # ------------------------------------------------------------------------------------------------------

    def updateWorkOut(self, pb, pbValue, labelUsed, labelUsedValue, labelTotal):
        pb.setValue(pbValue)
        self.common.analizeProgressBar(pb, pbValue)
        labelUsed.setText(labelUsedValue)
        self.common.analizeValue(labelUsed, labelUsedValue, labelTotal)

