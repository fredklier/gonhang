import sys
from PyQt5 import QtWidgets, QtCore, QtGui
import subprocess
from gonhang.api import StringUtil
from gonhang.wizard import GonhaNgWizard
from gonhang.wizard import PositionPage
from gonhang.threads import ThreadSystem
from gonhang.displayclasses import DisplaySystem
from gonhang.displayclasses import CommomAttributes
from gonhang.core import Config


class MainWindow(QtWidgets.QMainWindow):
    config = Config()
    wmctrlBin = subprocess.getoutput('which wmctrl')
    myWizard = None
    # -------------------------------------------------------------
    # Display classes
    common = CommomAttributes()
    displaySystem = DisplaySystem()
    # -------------------------------------------------------------
    # Threads
    threadSystem = ThreadSystem()

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
        centralWidGet = QtWidgets.QWidget(self)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setAlignment(QtCore.Qt.AlignTop)
        centralWidGet.setLayout(self.verticalLayout)
        self.setCentralWidget(centralWidGet)

    def showSections(self):
        self.loadGlobalParams()
        self.verticalLayout.addWidget(self.displaySystem.initUi())

    def loadGlobalParams(self):
        position = self.config.getKey('Position')
        if position is None:
            self.refreshPosition(0)
        else:
            self.refreshPosition(position['index'])

    def startAllThreads(self):
        # Connect thread signals and start
        self.threadSystem.signal.connect(self.threadSystemReceive)
        self.threadSystem.start()

    def getWindowCurrentId(self, windowTitle):
        print(f'wmctrl binary found in : {self.wmctrlBin}')
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

    def contextMenuEvent(self, event: QtGui.QContextMenuEvent):
        # -------------------------------------------------------------
        # Main Menu
        contextMenu = QtWidgets.QMenu(self)
        positionMenu = contextMenu.addMenu('Position')
        positionLeftAction = positionMenu.addAction('Left')
        positionCenterAction = positionMenu.addAction('Center')
        positionRightAction = positionMenu.addAction('Right')
        configAction = contextMenu.addAction('Config')
        quitAction = contextMenu.addAction('Quit')
        action = contextMenu.exec_(self.mapToGlobal(event.pos()))
        if action == quitAction:
            sys.exit()
        elif action == configAction:
            self.wizardAction()
        elif action == positionLeftAction:
            self.refreshPosition(0)
        elif action == positionCenterAction:
            self.refreshPosition(1)
        elif action == positionRightAction:
            self.refreshPosition(2)

    @staticmethod
    def getScreenGeometry():
        return QtWidgets.QApplication.desktop().screenGeometry()

    def refreshPosition(self, index):
        x = 0
        if index == 1:
            x = (self.getScreenGeometry().width() - self.geometry().width()) / 2
        elif index == 2:
            x = (self.getScreenGeometry().width() - self.geometry().width())

        self.move(x, 0)
        # write to config
        self.config.updateConfig({'Position': {'index': index, 'value': PositionPage.positions[index]}})

    def wizardAction(self):
        print('Enter in wizard...')
        self.myWizard = GonhaNgWizard(self)
        self.myWizard.show()

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
        self.updateWorkOut(
            self.displaySystem.systemWidgets['cpuProgressBar'],
            message['cpuProgressBar'],
            self.displaySystem.systemWidgets['cpuFreqCurrent'],
            message['cpuFreqCurrent'],
            message['cpuFreqMax']
        )
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

    def updateWorkOut(self, pb, pbValue, labelUsed, labelUsedValue, labelTotal):
        pb.setValue(pbValue)
        self.common.analizeProgressBar(pb, pbValue)
        labelUsed.setText(labelUsedValue)
        self.common.analizeValue(labelUsed, labelUsedValue, labelTotal)
