from PyQt5 import QtCore
from gonhang.core import System
from gonhang.core import Nvidia


# thread fast
class ThreadSystem(QtCore.QThread):
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


class ThreadNvidia(QtCore.QThread):
    nvidia = Nvidia()
    signal = QtCore.pyqtSignal(list, name='ThreadNvidiaFinish')
    message = []

    def __init__(self, parent=None):
        super(ThreadNvidia, self).__init__(parent)
        self.finished.connect(self.updateNvidia)

    def updateNvidia(self):
        self.message = self.nvidia.getGPUsInfo()
        self.signal.emit(self.message)
        self.start()

    def run(self):
        self.msleep(500)  # sleep for 500ms
