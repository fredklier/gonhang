from PyQt5 import QtCore
from gonhang.core import Config
from gonhang.core import System
from gonhang.core import Nvidia
from gonhang.core import StorTemps
from gonhang.core import Net
from gonhang.displayclasses import DisplaySystem
from gonhang.displayclasses import DisplayNvidia
from gonhang.displayclasses import DisplayNet
from gonhang.displayclasses import CommomAttributes
import psutil
import subprocess
import humanfriendly


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


class ThreadStorTemps(QtCore.QThread):
    storTemps = StorTemps()
    signal = QtCore.pyqtSignal(dict, name='ThreadStorTempsFinish')
    message = dict()

    def __init__(self, parent=None):
        super(ThreadStorTemps, self).__init__(parent)
        self.finished.connect(self.updateStorTemps)

    def updateStorTemps(self):
        self.message = self.storTemps.getMessage()
        self.signal.emit(self.message)
        self.start()

    def run(self):
        self.msleep(1000)  # sleep for 500ms


class ThreadNet(QtCore.QThread):
    config = Config()
    net = Net()
    signal = QtCore.pyqtSignal(dict, name='ThreadNetFinish')
    message = dict()
    netOptionConfig = dict()
    myExtIp = subprocess.getoutput('curl -s ifconfig.me')
    countersRcv = [0, 0]
    countersSent = [0, 0]

    def __init__(self, parent=None):
        super(ThreadNet, self).__init__(parent)
        self.finished.connect(self.updateNet)

    def loadConfig(self):
        self.netOptionConfig = self.config.getKey('netOption')

    def updateNet(self):
        if self.net.isToDisplayNet():
            self.loadConfig()
            self.message.clear()
            interface = self.netOptionConfig['interface']
            counter = psutil.net_io_counters(pernic=True)[interface]
            self.countersRcv[1] = counter.bytes_recv
            self.countersSent[1] = counter.bytes_sent
            downSpeed = self.countersRcv[1] - self.countersRcv[0]
            upSpeed = self.countersSent[1] - self.countersSent[0]
            # get io statistics since boot
            net_io = psutil.net_io_counters(pernic=True)
            network = psutil.net_if_addrs()
            self.message['intipLabel'] = network[interface][0].address
            self.message['extipLabel'] = self.myExtIp
            self.message['ifaceValueLabel'] = interface
            self.message['ifaceDownRateLabel'] = downSpeed
            self.message['ifaceUpRateLabel'] = upSpeed
            self.message['bytesRcvValueLabel'] = net_io[interface].bytes_sent
            self.message['bytesSentValueLabel'] = net_io[interface].bytes_recv

        self.signal.emit(self.message)
        self.start()

    def run(self):
        if self.net.isToDisplayNet():
            self.loadConfig()
            counter = psutil.net_io_counters(pernic=True)[self.netOptionConfig['interface']]
            self.countersRcv[0] = counter.bytes_recv
            self.countersSent[0] = counter.bytes_sent

        self.msleep(1000)  # sleep for 500ms


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

    # -----------------------------------------------------------------
    # net
    net = Net()
    displayNet = DisplayNet()
    threadNet = ThreadNet()

    # -----------------------------------------------------------------
    # storTemps
    storTemps = StorTemps()
    # displayNet = DisplayNet()
    threadStorTemps = ThreadStorTemps()

    def __init__(self, vLayout, parent=None):
        super(WatchDog, self).__init__(parent)
        self.finished.connect(self.threadFinished)
        # ------------------------------------------------------------------
        # Connecting signals
        self.threadNvidia.signal.connect(self.threadNvidiaReceive)
        self.threadSystem.signal.connect(self.threadSystemReceive)
        self.threadNet.signal.connect(self.threadNetReceive)
        self.threadStorTemps.signal.connect(self.threadStorTempsReceive)
        # ------------------------------------------------------------------
        # show displayClasses
        self.verticalLayout = vLayout
        # ------------------------------------------------------------------
        # display system (default section)
        self.displaySystem.initUi(self.verticalLayout)
        # ------------------------------------------------------------------
        # display nvidia if have nvidia gpu
        self.displayNvidia.initUi(self.verticalLayout)
        # ------------------------------------------------------------------
        # display net
        self.displayNet.initUi(self.verticalLayout)
        # -------------------------------------------------------------------------------------------
        # Start another threads
        print(f'Starting threadSystem')
        self.threadSystem.start()
        print(f'Starting threadNvidia')
        self.threadNvidia.start()
        print(f'Starting threadNet')
        self.threadNet.start()
        # self.threadStorTempsId = self.threadStorTemps.currentThreadId()
        # print(f'Starting threadStorTemps ID: [{self.threadStorTemps.currentThreadId()}] = [{self.threadStorTempsId}]')

    def threadFinished(self):
        self.start()

    def threadStorTempsReceive(self, message):
        print(message)

    def threadNetReceive(self, message):
        if self.net.isToDisplayNet():
            self.displayNet.netWidgets['netGroupBox'].show()
            self.displayNet.netWidgets['intipLabel'].setText(message['intipLabel'])
            self.displayNet.netWidgets['extipLabel'].setText(message['extipLabel'])
            self.displayNet.netWidgets['ifaceValueLabel'].setText(message['ifaceValueLabel'])
            self.displayNet.netWidgets['ifaceDownRateLabel'].setText(
                '{}/s'.format(humanfriendly.format_size(message['ifaceDownRateLabel'], binary=True)))
            self.displayNet.netWidgets['ifaceUpRateLabel'].setText(
                '{}/s'.format(humanfriendly.format_size(message['ifaceUpRateLabel'], binary=True)))
            self.displayNet.netWidgets['bytesRcvValueLabel'].setText(
                humanfriendly.format_size(message['bytesRcvValueLabel'], binary=True))
            self.displayNet.netWidgets['bytesSentValueLabel'].setText(
                humanfriendly.format_size(message['bytesSentValueLabel'], binary=True))
        else:
            self.displayNet.netWidgets['netGroupBox'].hide()

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
            self.displayNvidia.nvidiaWidgets['driverValueLabel'].setText(message['driver_version'])
            self.displayNvidia.nvidiaWidgets['biosValueLabel'].setText(message['vbios_version'])
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
        # print('running....')
        self.sleep(1)
