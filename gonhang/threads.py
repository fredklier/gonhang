from PyQt5 import QtCore
from gonhang.core import System
from gonhang.core import Nvidia
from gonhang.displayclasses import DisplaySystem
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
    common = CommomAttributes()
    # -----------------------------------------------------------------
    # System
    system = System()
    displaySystem = DisplaySystem()
    threadSystem = ThreadSystem()
    # -----------------------------------------------------------------
    # nvidia
    nvidia = Nvidia()
    displayNvidia = DisplayNvidia()
    threadNvidia = ThreadNvidia()

    def __init__(self, vLayout, parent=None):
        super(WatchDog, self).__init__(parent)
        self.finished.connect(self.threadFinished)
        self.threadNvidia.signal.connect(self.threadNvidiaReceive)

        self.threadSystem.signal.connect(self.threadSystemReceive)
        self.verticalLayout = vLayout

        # display system (default section)
        self.displaySystem.initUi(self.verticalLayout)
        # display nvidia if have nvidia gpu
        if self.nvidia.getNumberGPUs()>0:
            self.displayNvidia.initUi(self.verticalLayout)

    def threadFinished(self):
        self.start()

    def threadSystemReceive(self, message):
        # -----------------------------------------------------------------------------------------------------
        # System, release and node machine
        self.displaySystem.systemWidgets['distroStr'].setText(message['distroStr'])
        self.displaySystem.systemWidgets['release'].setText(f"Kernel {message['release']}")
        self.displaySystem.systemWidgets['nodeMachine'].setText(f"node {message['node']} arch {message['machine']}")
        # -----------------------------------------------------------------------------------------------------
        # boot time
        self.displaySystem.systemWidgets['btDays'].setText(f"{message['btDays']} ")
        self.displaySystem.systemWidgets['btHours'].setText(f"{message['btHours']} ")
        self.displaySystem.systemWidgets['btMinutes'].setText(f"{message['btMinutes']} ")
        self.displaySystem.systemWidgets['btSeconds'].setText(f"{message['btSeconds']} ")
        # -----------------------------------------------------------------------------------------------------
        # Cpu Load workout
        self.displaySystem.systemWidgets['cpuProgressBar'].setValue(message['cpuProgressBar'])
        self.common.analizeProgressBar(self.displaySystem.systemWidgets['cpuProgressBar'], message['cpuProgressBar'])
        self.displaySystem.systemWidgets['cpuFreqCurrent'].setText(f"{message['cpuFreqCurrent']} MHz")
        self.common.analizeValue(self.displaySystem.systemWidgets['cpuFreqCurrent'], message['cpuFreqCurrent'],
                                 message['cpuFreqMax'])
        # -----------------------------------------------------------------------------------------------------
        # Ram Load workout
        self.updateWorkOut(
            self.displaySystem.systemWidgets['ramProgressBar'],
            message['ramProgressBar'],
            self.displaySystem.systemWidgets['ramUsed'],
            message['ramUsed'],
            message['ramTotal']
        )
        # -----------------------------------------------------------------------------------------------------
        # swap Load workout
        self.updateWorkOut(
            self.displaySystem.systemWidgets['swapProgressBar'],
            message['swapProgressBar'],
            self.displaySystem.systemWidgets['swapUsed'],
            f"{message['swapUsed']}",
            message['swapTotal']
        )

        # ------------------------------------------------------------------------------------------------------
        # Verify if can display cpuTemp
        if self.system.isToDisplayCpuTemp():
            self.displaySystem.showWidgetByDefault()
            self.displaySystem.systemWidgets['cpuTempProgressBar'].setValue(message['cpuTempProgressBar'])
            self.common.analizeProgressBar(self.displaySystem.systemWidgets['cpuTempProgressBar'],
                                           message['cpuTempProgressBar'])
            self.displaySystem.systemWidgets['cpuCurrentTempLabel'].setText(f"{message['cpuCurrentTempLabel']} °C")
            self.common.analizeTemp(
                self.displaySystem.systemWidgets['cpuCurrentTempLabel'],
                float(message['cpuCurrentTempLabel']),
                75.0,
                85.0
            )
        else:
            self.displaySystem.hideWidgetByDefault()
        # ------------------------------------------------------------------------------------------------------

    def updateWorkOut(self, pb, pbValue, labelUsed, labelUsedValue, labelTotal):
        pb.setValue(pbValue)
        self.common.analizeProgressBar(pb, pbValue)
        labelUsed.setText(labelUsedValue)
        self.common.analizeValue(labelUsed, labelUsedValue, labelTotal)

    def threadNvidiaReceive(self, message):
        if self.nvidia.isToDisplayNvidia():
            self.displayNvidia.nvidiaWidgets['nvidiaGroupBox'].show()
            self.displayNvidia.nvidiaWidgets['gpu_name'].setText(message['gpu_name'])
            self.displayNvidia.nvidiaWidgets['utilization_gpu'].setText(f"{str(message['utilization_gpu'])}")
            self.displayNvidia.nvidiaWidgets['usedTotalMemory'].setText(
                f"{message['memory_used']}/{message['memory_total']}")
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

        if not self.threadSystem.isRunning():
            self.threadSystem.start()
        # ----------------------------------------------------------------------------
        # Verify for nvidia
        if self.nvidia.isToDisplayNvidia() or (not self.threadNvidia.isRunning()):
            self.threadNvidia.start()
        else:
            self.threadNvidia.quit()

        # ----------------------------------------------------------------------------
        self.msleep(1000)  # sleep for 500ms
