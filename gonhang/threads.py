from PyQt5 import QtCore, QtGui
from gonhang.core import Config
from gonhang.core import System
from gonhang.core import Nvidia
from gonhang.core import StorTemps
from gonhang.core import Net
from gonhang.core import Weather
from gonhang.displayclasses import DisplaySystem
from gonhang.displayclasses import DisplayNvidia
from gonhang.displayclasses import DisplayNet
from gonhang.displayclasses import DisplayStorages
from gonhang.displayclasses import DisplayWeather
from gonhang.displayclasses import CommomAttributes

import psutil
import subprocess
import humanfriendly
from datetime import datetime
import gettext
import os

localedir = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'locale')
translate = gettext.translation('gonhang', localedir, fallback=True)
_ = translate.gettext


class ThreadDateTime(QtCore.QThread):
    signal = QtCore.pyqtSignal(dict, name='ThreadDateTimeFinish')
    myTime = 30 * 60
    weather = Weather()
    message = dict()

    def __init__(self, parent=None):
        super(ThreadDateTime, self).__init__(parent)
        self.finished.connect(self.finishThreadTime)

    def finishThreadTime(self):
        self.message.clear()
        now = datetime.now()
        # ---------------------------------------------------------------------------------
        # Update Date and time
        # ---------------------------------------------------------------------------------
        self.message['hour'] = now.strftime('%H')
        self.message['min'] = now.strftime('%M')
        self.message['sec'] = now.strftime('%S')
        self.message['day'] = now.strftime("%d")
        self.message['weekday'] = now.strftime("%A")
        self.message['month'] = now.strftime("%B")
        self.message['year'] = now.strftime("%Y")

        self.signal.emit(self.message)
        self.start()

    def run(self):
        self.sleep(1)


class ThreadWeather(QtCore.QThread):
    signal = QtCore.pyqtSignal(dict, name='ThreadWeatherFinish')
    myTime = 30 * 60
    weather = Weather()

    def __init__(self, parent=None):
        super(ThreadWeather, self).__init__(parent)
        self.finished.connect(self.finishThreadWeather)

    def updateMyTime(self, myTime):
        self.myTime = (myTime * 60)

    def finishThreadWeather(self):
        self.start()

    def run(self):
        self.signal.emit(self.weather.getMessage())
        print(_('threadWeather sleep now for') + f' {self.myTime} ' + _('seconds...'))
        self.sleep(self.myTime)


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
            self.message['bytesRcvValueLabel'] = net_io[interface].bytes_recv
            self.message['bytesSentValueLabel'] = net_io[interface].bytes_sent

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
    configCacheStamp = 0
    config = Config()
    common = CommomAttributes()
    # -----------------------------------------------------------------
    # weather
    weather = Weather()
    displayWeather = DisplayWeather()
    threadWeather = ThreadWeather()
    threadDateTime = ThreadDateTime()
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
    displayStorages = DisplayStorages()

    def __init__(self, vLayout, parent=None):
        super(WatchDog, self).__init__(parent)
        # ------------------------------------------------------------------
        # Connecting signals
        self.threadNvidia.signal.connect(self.threadNvidiaReceive)
        self.threadSystem.signal.connect(self.threadSystemReceive)
        self.threadNet.signal.connect(self.threadNetReceive)
        self.threadWeather.signal.connect(self.threadWeatherReceive)
        self.threadDateTime.signal.connect(self.threadDateTimeReceive)
        # ------------------------------------------------------------------
        # show displayClasses
        self.verticalLayout = vLayout
        # ------------------------------------------------------------------
        # display weather
        weatherOptionConfig = self.config.getKey('weatherOption')
        myTime = 30
        if not (weatherOptionConfig is None):
            myTime = weatherOptionConfig['updateTime']

        self.threadWeather.updateMyTime(myTime)
        self.displayWeather.initUi(self.verticalLayout)

        # ------------------------------------------------------------------
        # display system (default section)
        self.systemGroupBox = self.displaySystem.initUi(self.verticalLayout)
        # ------------------------------------------------------------------
        # display nvidia if have nvidia gpu
        self.displayNvidia.initUi(self.verticalLayout)
        # ------------------------------------------------------------------
        # display net
        self.displayNet.initUi(self.verticalLayout)
        # ------------------------------------------------------------------
        # display Storages
        self.displayStorages.initUi(self.verticalLayout)
        # ------------------------------------------------------------------
        # Start another threads
        print(_('Starting threadWeather'))
        self.threadWeather.start()
        print(_('Starting threadDateTime'))
        self.threadDateTime.start()
        print(_('Starting threadSystem'))
        self.threadSystem.start()
        print(_('Starting threadNvidia'))
        self.threadNvidia.start()
        print(_('Starting threadNet'))
        self.threadNet.start()
        print(_('Starting Thread DisplayStorages'))
        self.displayStorages.start()

        self.start()

    def threadDateTimeReceive(self, message):
        if self.weather.isToDisplay():
            self.displayWeather.weatherWidgets['weatherGroupBox'].show()
            self.displayWeather.weatherWidgets['hour'].setText(message['hour'])
            self.displayWeather.weatherWidgets['min'].setText(message['min'])
            self.displayWeather.weatherWidgets['day'].setText(f"{message['day']},")
            self.displayWeather.weatherWidgets['month'].setText(f"{message['month']} ")
            self.displayWeather.weatherWidgets['year'].setText(message['year'])
            self.displayWeather.weatherWidgets['weekday'].setText(message['weekday'])
        else:
            self.displayWeather.weatherWidgets['weatherGroupBox'].hide()

    def threadWeatherReceive(self, message):
        if self.weather.isToDisplay():
            self.displayWeather.weatherWidgets['weatherGroupBox'].show()
            self.displayWeather.weatherWidgets['name'].setText(message['name'])
            self.displayWeather.weatherWidgets['country'].setText(message['country'])
            self.displayWeather.weatherWidgets['humidity'].setText(message['humidity'])
            self.displayWeather.weatherWidgets['pressure'].setText(message['pressure'])
            self.displayWeather.weatherWidgets['visibility'].setText(message['visibility'])
            self.displayWeather.weatherWidgets['wind'].setText(message['wind'])
            # print(message)
            pixmap = QtGui.QPixmap()
            pixmap.loadFromData(self.weather.getIcon(message['icon']))
            self.displayWeather.weatherWidgets['cloudicon'].setPixmap(pixmap)
        else:
            self.displayWeather.weatherWidgets['weatherGroupBox'].hide()

    def threadNetReceive(self, message):
        if self.net.isToDisplayNet():
            self.displayNet.netWidgets['netGroupBox'].show()
            self.displayNet.netWidgets['intipLabel'].setText(message['intipLabel'])
            self.displayNet.netWidgets['extipLabel'].setText(message['extipLabel'])
            self.displayNet.netWidgets['ifaceValueLabel'].setText(f"{message['ifaceValueLabel']}")
            self.displayNet.netWidgets['ifaceDownRateLabel'].setText(
                '{}/s'.format(humanfriendly.format_size(message['ifaceDownRateLabel'], binary=True)))
            self.displayNet.netWidgets['ifaceUpRateLabel'].setText(
                '{}/s'.format(humanfriendly.format_size(message['ifaceUpRateLabel'], binary=True)))
            self.displayNet.netWidgets['bytesRcvValueLabel'].setText(
                f"{humanfriendly.format_size(message['bytesRcvValueLabel'], binary=True)}")
            self.displayNet.netWidgets['bytesSentValueLabel'].setText(
                f"{humanfriendly.format_size(message['bytesSentValueLabel'], binary=True)}")
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
            self.displaySystem.systemWidgets['cpuTempLabel'].setText(message['cpuTempLabel'])
            self.systemGroupBox.setFixedHeight(230)
        else:
            self.displaySystem.hideWidgetByDefault()
            self.systemGroupBox.setFixedHeight(200)

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


class ThreadValidateWeather(QtCore.QThread):
    net = Net()
    signal = QtCore.pyqtSignal(dict, name='ThreadValidateWeatherFinish')
    weather = Weather()

    def __init__(self, parent=None):
        super(ThreadValidateWeather, self).__init__(parent)

    def updateAndStart(self, lat, lon, apiKey):
        self.weather.updateUrl(lat, lon, apiKey)
        self.start()

    def run(self):
        self.signal.emit(self.weather.getMessage())
