import sys
import logging
from PyQt5 import QtWidgets, QtCore, QtGui
import subprocess
from gonhang.api import StringUtil
from gonhang.wizard import GonhaNgWizard
from gonhang.threads import ThreadSystem
from gonhang.displayclasses import DisplaySystem


class MainWindow(QtWidgets.QMainWindow):
    logger = logging.getLogger(__name__)
    wmctrlBin = subprocess.getoutput('which wmctrl')
    myWizard = None
    # -------------------------------------------------------------
    # Display classes
    displaySystem = DisplaySystem()
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
        # Central Widget and Global vertical Layout
        centralWidGet = QtWidgets.QWidget(self)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setAlignment(QtCore.Qt.AlignTop)
        centralWidGet.setLayout(self.verticalLayout)
        self.setCentralWidget(centralWidGet)
        # --------------------------------------------------------------

    def showSections(self):
        self.verticalLayout.addWidget(self.displaySystem.initUi())

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

    def threadSystemReceive(self, message):
        self.logger.info(f'Receive message => {message}')
