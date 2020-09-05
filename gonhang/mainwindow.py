import coloredlogs
import logging
from PyQt5 import QtWidgets


class MainWindow(QtWidgets.QMainWindow):
    logger = logging.getLogger(__name__)

    def __init__(self):
        super(MainWindow, self).__init__()
        coloredlogs.install()
        self.logger.info('Start MainWindow')
        self.setFixedWidth(450)
        self.setFixedHeight(200)

