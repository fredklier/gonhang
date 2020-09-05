import coloredlogs
import logging
from PyQt5 import QtWidgets, QtCore
import subprocess
from gonhang.api import StringUtil
import time


class MainWindow(QtWidgets.QMainWindow):
    logger = logging.getLogger(__name__)
    wmctrlBin = subprocess.getoutput('which wmctrl')

    def __init__(self):
        super(MainWindow, self).__init__()
        coloredlogs.install()
        self.logger.info('Start MainWindow')
        self.setWindowTitle(StringUtil.getRandomString(30))
        self.logger.info(f'Current title: {self.windowTitle()}')

        # self.myWindowId = self.getWindowCurrentId(self.windowTitle())
        # self.logger.info(f'Current window ID: [{self.myWindowId}]')
        # self.setWindowInEveryWorkspaces(self.myWindowId)
        # self.logger.info(f'Now, window Id: {self.myWindowId} is present in every workspaces...')

    def getWindowCurrentId(self, windowTitle):
        # wmctrl -i -r 0x07a00006 -b add,sticky
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
        subprocess.getoutput(f'{self.wmctrlBin} -i -r {self.myWindowId} -b add,sticky')
