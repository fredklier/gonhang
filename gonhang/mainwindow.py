import coloredlogs
import logging
from PyQt5 import QtWidgets, QtCore
import subprocess
from gonhang.api import StringUtil
import time


class MainWindow(QtWidgets.QMainWindow):
    logger = logging.getLogger(__name__)
    wmctrlBin = subprocess.getoutput('which wmctrl')
    myCurrentId = ''

    def __init__(self):
        super(MainWindow, self).__init__()
        # coloredlogs.install()
        self.logger.info('Start MainWindow')
        self.setWindowTitle(StringUtil.getRandomString(30))

        # time.sleep(5)
        # self.myCurrentId = self.getWindowCurrentId(self.windowTitle())
        # self.logger.info(f'My Current Id: [{self.myCurrentId}]')

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
        self.logger.info(f'Output from command [{cmd}] is: {output}')
