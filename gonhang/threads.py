from PyQt5 import QtCore
import logging
from gonhang.core import System


# thread fast
class ThreadSystem(QtCore.QThread):
    logger = logging.getLogger(__name__)
    signal = QtCore.pyqtSignal(dict, name='ThreadFastFinish')
    system = System()

    def __init__(self, parent=None):
        super(ThreadSystem, self).__init__(parent)
        self.finished.connect(self.threadFinished)

    def threadFinished(self):
        self.start()

    def run(self):
        self.signal.emit(self.system.getMessage())
        self.msleep(500)  # sleep for 500ms

