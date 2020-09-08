from PyQt5 import QtCore
from gonhang.core import System
from gonhang.core import Nvidia
from gonhang.displayclasses import DisplayNvidia
from gonhang.displayclasses import CommomAttributes


# ------------------------------------------------------------------------------------
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
    signal = QtCore.pyqtSignal(dict, name='ThreadNvidiaFinish')
    message = dict()

    def __init__(self, parent=None):
        super(ThreadNvidia, self).__init__(parent)
        self.finished.connect(self.updateNvidia)

    def updateNvidia(self):
        self.message = self.nvidia.getGPUsInfo()
        self.signal.emit(self.message)
        self.start()

    def run(self):
        self.msleep(500)  # sleep for 500ms


# ------------------------------------------------------------------------------------
# WatchDog
# One thread to manager another threads
class WatchDog(QtCore.QThread):
    nvidia = Nvidia()
    threadNvidia = ThreadNvidia()
    displayNvidia = DisplayNvidia()
    common = CommomAttributes()

    def __init__(self, parent=None):
        super(WatchDog, self).__init__(parent)
        self.finished.connect(self.threadFinished)
        self.threadNvidia.signal.connect(self.threadNvidiaReceive)

    def threadFinished(self):
        self.start()

    def threadNvidiaReceive(self, message):
        if self.nvidia.isToDisplayNvidia():
            self.displayNvidia.nvidiaWidgets['nvidiaGroupBox'].show()
            self.displayNvidia.nvidiaWidgets['gpu_name'].setText(message['gpu_name'])
            self.displayNvidia.nvidiaWidgets['utilization_gpu'].setText(f"{str(message['utilization_gpu'])}")
            self.displayNvidia.nvidiaWidgets['usedTotalMemory'].setText(f"{message['memory_used']}/{message['memory_total']}")
            self.displayNvidia.nvidiaWidgets['power_draw'].setText(f"{message['power_draw']}")
            self.displayNvidia.nvidiaWidgets['fan_speed'].setText(f"{message['fan_speed']}")
            self.displayNvidia.nvidiaWidgets['temperature_gpu'].setText(f"{int(message['temperature_gpu'])} °C")
            self.common.analizeTemp(
                self.displayNvidia.nvidiaWidgets['temperature_gpu'],
                message['temperature_gpu'],
                message['temperature_gpu_high'],
                message['temperature_gpu_critical']
            )
        else:
            self.displayNvidia.nvidiaWidgets['nvidiaGroupBox'].hide()

    def run(self):
        # ----------------------------------------------------------------------------
        # Verify for nvidia
        if self.nvidia.isToDisplayNvidia() and (not self.threadNvidia.isRunning()):
            self.threadNvidia.start()
        else:
            self.threadNvidia.quit()

        # ----------------------------------------------------------------------------
        self.msleep(1000)  # sleep for 500ms
