import sys
import logging
from PyQt5 import QtWidgets, QtCore, QtGui
import subprocess
from gonhang.api import StringUtil
from gonhang.wizard import ChildWnd


class MainWindow(QtWidgets.QMainWindow):
    logger = logging.getLogger(__name__)
    wmctrlBin = subprocess.getoutput('which wmctrl')
    myCurrentId = ''
    # -------------------------------------------------------------
    # Window Flags
    flags = QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnBottomHint | QtCore.Qt.Tool

    # -------------------------------------------------------------

    def __init__(self):
        super(MainWindow, self).__init__()
        self.logger.info('Start MainWindow')
        self.setWindowTitle(StringUtil.getRandomString(30))
        self.setWindowFlags(self.flags)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

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

    def setWindowInEveryWorkspaces(self, windowId):
        # wmctrl -i -r 0x07a00006 -b add,sticky
        cmd = f'{self.wmctrlBin} -i -r {self.myCurrentId} -b add,sticky'
        output = subprocess.getoutput(cmd)

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
        wizard = ChildWnd()
        # wizard.show()



