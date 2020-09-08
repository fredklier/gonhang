from PyQt5 import QtWidgets, QtCore, QtGui
import subprocess
from gonhang.api import StringUtil
from gonhang.wizard import GonhaNgWizard
from gonhang.threads import ThreadSystem
from gonhang.threads import WatchDog
from gonhang.displayclasses import DisplaySystem
from gonhang.displayclasses import DisplayNvidia
from gonhang.displayclasses import CommomAttributes
from gonhang.core import Config
from gonhang.systemtray import SystemTrayIcon
from gonhang.api import FileUtil
from gonhang.core import System
from gonhang.core import Nvidia
from gonhang.core import KeysSkeleton
from gonhang.displayclasses import AboutBox
import sys
import time


class MainWindow(QtWidgets.QMainWindow):
    config = Config()
    system = System()
    nvidia = Nvidia()
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
    # threadNvidia = ThreadNvidia()
    watchDog = WatchDog()
    # --------------------------------------------------------------
    # itens hide by default
    nvidiaGroupBox = QtWidgets.QGroupBox()

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
        # start WatchDog
        print('Starting WatchDog....')
        self.watchDog.start()

    def showAboutBox(self):
        # self.aboutBox.exec_()
        self.aboutBox.show()

    def showSections(self):
        self.loadGlobalParams()
        self.displaySystem.initUi(self.verticalLayout)

        if self.nvidia.getNumberGPUs() > 0:
            self.nvidiaGroupBox = self.displayNvidia.initUi(self.verticalLayout)
            self.nvidiaGroupBox.hide()

    def loadGlobalParams(self):
        position = self.config.getKey('positionOption')
        if position is None:
            self.refreshPosition(0)
        else:
            self.refreshPosition(position['index'])

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

