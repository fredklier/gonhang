from PyQt5 import QtCore
import logging


# thread fast
class ThreadSystem(QtCore.QThread):
    logger = logging.getLogger(__name__)
    signal = QtCore.pyqtSignal(dict, name='ThreadFastFinish')

    def __init__(self, parent=None):
        super(ThreadSystem, self).__init__(parent)
        self.finished.connect(self.threadFinished)

    def threadFinished(self):
        self.logger.info('Stop ThreadSystem')
        self.start()

    def run(self):
        # self.signal.emit(self.system.getMessage())
        self.logger.info('Running ThreadSystem')
        self.msleep(1500)  # sleep for 500ms


