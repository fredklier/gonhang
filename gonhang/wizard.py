from PyQt5 import QtWidgets, QtGui, QtCore
from gonhang.api import FileUtil
from gonhang.core import Config
from gonhang.core import KeysSkeleton
from gonhang.core import Nvidia
from gonhang.core import Net
from gonhang.core import StorTemps
from gonhang.displayclasses import CommomAttributes
from gonhang.threads import ThreadValidateWeather
import psutil
from telnetlib import Telnet
import gettext
import os

localedir = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'locale')
translate = gettext.translation('gonhang', localedir, fallback=True)
_ = translate.gettext


class GonhaNgWizard(QtWidgets.QWizard):
    nvidia = Nvidia()
    storTemps = StorTemps()

    def __init__(self, parent=None):
        super(GonhaNgWizard, self).__init__(parent)
        self.addPage(WeatherPage(self))
        self.addPage(CpuTempPage(self))
        self.addPage(NetPage(self))
        if self.nvidia.getNumberGPUs() > 0:
            self.addPage(NvidiaPage(self))

        if self.storTemps.hddtempIsOk():
            self.addPage(StorTempsPage(self))

        self.addPage(PartitionsPage(self))

        self.setWindowTitle(_('GonhaNG Wizard Welcome'))
        self.resize(640, 480)
        self.setWizardStyle(QtWidgets.QWizard.MacStyle)
        self.setPixmap(QtWidgets.QWizard.BackgroundPixmap,
                       QtGui.QPixmap(f'{FileUtil.getResourcePath()}/images/logo.png'))
        self.centerMe()

    def centerMe(self):
        screenGeo = QtWidgets.QApplication.desktop().screenGeometry()
        x = (screenGeo.width() - self.width()) / 2
        # y = (screenGeo.height() - self.height()) / 2
        self.move(x, 100)


class CpuTempPage(QtWidgets.QWizardPage):
    config = Config()
    keysSkeleton = KeysSkeleton()

    def __init__(self, parent=None):
        super(CpuTempPage, self).__init__(parent)
        self.setTitle(_('CPU Temperature'))
        self.vLayout = QtWidgets.QVBoxLayout()
        self.hint = _(
            'GonhaNG measures the average temperature of all cpu cores installed in your system. In general this value corresponds to Tdie')
        self.hintLabel = QtWidgets.QLabel(self.hint)
        self.hintLabel.setTextFormat(QtCore.Qt.RichText)
        self.vLayout.addWidget(self.hintLabel)

        self.groupBoxEnabled = QtWidgets.QGroupBox(_('Enable or Disable CPU Temperature? '))
        self.gbLayout = QtWidgets.QVBoxLayout()

        self.rbEnable = QtWidgets.QRadioButton(_('Enabled'))
        self.rbEnable.clicked.connect(self.groupBoxClicked)
        self.gbLayout.addWidget(self.rbEnable)

        self.rbDisable = QtWidgets.QRadioButton(_('Disabled'))
        self.rbDisable.clicked.connect(self.groupBoxClicked)
        self.rbDisable.setChecked(True)
        self.gbLayout.addWidget(self.rbDisable)

        self.groupBoxEnabled.setLayout(self.gbLayout)

        self.vLayout.addWidget(self.groupBoxEnabled)

        self.questionLabel = QtWidgets.QLabel(_('What is the temperature label of your CPU?'))
        self.vLayout.addWidget(self.questionLabel)

        self.optionsList = QtWidgets.QListWidget()
        self.displayAvailableTemps()
        self.optionsList.clicked.connect(self.optionsClick)
        self.vLayout.addWidget(self.optionsList)
        self.setLayout(self.vLayout)

    def groupBoxClicked(self):
        index = self.keysSkeleton.cpuTempOption['cpuTempOption']['index']
        subIndex = self.keysSkeleton.cpuTempOption['cpuTempOption']['subIndex']
        enabled = False
        if self.rbEnable.isChecked():
            self.optionsList.setEnabled(True)
            self.keysSkeleton.cpuTempOption['cpuTempOption']['enabled'] = True
            enabled = True
        else:
            self.optionsList.setDisabled(True)
            self.keysSkeleton.cpuTempOption['cpuTempOption']['enabled'] = False

        self.updateCpuTempOption(index, subIndex, enabled)

        # print(self.cpuTempOption)

    def optionsClick(self):
        rowList = self.optionsList.currentItem().text().split('|')
        self.updateCpuTempOption(rowList[0], int(rowList[1]),
                                 self.keysSkeleton.cpuTempOption['cpuTempOption']['enabled'])

    def updateCpuTempOption(self, index, subIndex, enabled):
        self.keysSkeleton.cpuTempOption.clear()
        self.keysSkeleton.cpuTempOption.update(
            {
                'cpuTempOption': {
                    'index': index,
                    'subIndex': subIndex,
                    'enabled': enabled
                }
            }
        )
        self.config.updateConfig(self.keysSkeleton.cpuTempOption)
        # print(self.cpuTempOption)

    def displayAvailableTemps(self):
        cpuSensors = psutil.sensors_temperatures()
        for index, sensor in enumerate(cpuSensors):
            for subIndex, shwtemp in enumerate(cpuSensors[sensor]):
                self.optionsList.insertItem(
                    subIndex,
                    '{}|{}| label: [{}] - temp. {} °C'.format(index, subIndex, shwtemp.label, shwtemp.current)
                )

        # Verify if exists key in config
        cpuTempOptionConfig = self.config.getKey('cpuTempOption')
        if cpuTempOptionConfig is None:
            self.updateCpuTempOption(0, 0, False)
        else:
            self.updateCpuTempOption(
                cpuTempOptionConfig['index'],
                cpuTempOptionConfig['subIndex'],
                cpuTempOptionConfig['enabled']
            )

        if not self.keysSkeleton.cpuTempOption['cpuTempOption']['enabled']:
            self.optionsList.setDisabled(True)
        else:
            self.optionsList.setEnabled(True)
            self.rbEnable.setChecked(True)

        self.displayCorrectRow()

    def displayCorrectRow(self):
        rowCount = self.optionsList.count()
        currentIndex = self.keysSkeleton.cpuTempOption['cpuTempOption']['index']
        currentSubIndex = self.keysSkeleton.cpuTempOption['cpuTempOption']['subIndex']
        # enable = self.rbEnable.q
        for i in range(rowCount):
            rowText = self.optionsList.item(i).text()
            rowList = rowText.split('|')
            if str(currentIndex) == str(rowList[0]) and str(currentSubIndex) == str(rowList[1]):
                self.optionsList.setCurrentRow(i)


class NvidiaPage(QtWidgets.QWizardPage):
    nvidia = Nvidia()
    keysSkeleton = KeysSkeleton()
    config = Config()
    common = CommomAttributes()

    def __init__(self, parent=None):
        super(NvidiaPage, self).__init__(parent)
        self.setTitle('Nvidia GPU')
        self.vLayout = QtWidgets.QVBoxLayout()
        self.groupBoxEnabled = QtWidgets.QGroupBox(_('Enable or Disable Nvidia GPU Monitor? '))
        self.gbLayout = QtWidgets.QVBoxLayout()
        self.rbEnable = QtWidgets.QRadioButton(_('Enabled'))
        self.rbEnable.clicked.connect(self.groupBoxClicked)
        self.gbLayout.addWidget(self.rbEnable)
        self.rbDisable = QtWidgets.QRadioButton(_('Disabled'))
        self.rbDisable.clicked.connect(self.groupBoxClicked)
        self.rbDisable.setChecked(True)
        self.gbLayout.addWidget(self.rbDisable)

        self.groupBoxEnabled.setLayout(self.gbLayout)

        self.vLayout.addWidget(self.groupBoxEnabled)

        self.questionLabel = QtWidgets.QLabel(_('Please select the nvidia gpu you want to monitor.'))
        self.vLayout.addWidget(self.questionLabel)

        self.optionsList = QtWidgets.QListWidget()
        self.optionsList.clicked.connect(self.optionsClick)
        self.vLayout.addWidget(self.optionsList)
        self.setLayout(self.vLayout)
        self.displayAvailablesGpus()

    def updateNvidiaOption(self, GpuId, enabled):
        self.keysSkeleton.nvidiaOption.clear()
        self.keysSkeleton.nvidiaOption.update(
            {
                'nvidiaOption': {
                    'GpuId': GpuId,
                    'enabled': enabled
                }
            }
        )
        self.config.updateConfig(self.keysSkeleton.nvidiaOption)
        # print(self.keysSkeleton.nvidiaOption)

    def displayAvailablesGpus(self):
        gpu = self.nvidia.getGPUsInfo()
        self.optionsList.addItem(f"{gpu['gpu_uuid']}| - {gpu['gpu_name']}")

        # Verify if exists key in config
        nvidiaOptionConfig = self.config.getKey('nvidiaOption')
        if nvidiaOptionConfig is None:
            self.updateNvidiaOption('', False)
        else:
            self.updateNvidiaOption(
                nvidiaOptionConfig['GpuId'],
                nvidiaOptionConfig['enabled']
            )

        if not self.keysSkeleton.nvidiaOption['nvidiaOption']['enabled']:
            self.optionsList.setDisabled(True)
        else:
            self.optionsList.setEnabled(True)
            self.rbEnable.setChecked(True)
        # print(gpuInfo)

        self.common.displayRow(self.optionsList, self.keysSkeleton.nvidiaOption['nvidiaOption']['GpuId'])

    def groupBoxClicked(self):
        enabled = False
        if self.rbEnable.isChecked():
            self.optionsList.setEnabled(True)
            self.keysSkeleton.nvidiaOption['nvidiaOption']['enabled'] = True
            enabled = True
        else:
            self.optionsList.setDisabled(True)
            self.keysSkeleton.nvidiaOption['nvidiaOption']['enabled'] = False

        self.updateNvidiaOption(self.keysSkeleton.nvidiaOption['nvidiaOption']['GpuId'], enabled)

    def optionsClick(self):
        rowList = self.optionsList.currentItem().text().split('|')
        self.updateNvidiaOption(rowList[0], self.keysSkeleton.nvidiaOption['nvidiaOption']['enabled'])


class NetPage(QtWidgets.QWizardPage):
    nvidia = Nvidia()
    keysSkeleton = KeysSkeleton()
    config = Config()
    common = CommomAttributes()

    def __init__(self, parent=None):
        super(NetPage, self).__init__(parent)
        self.setTitle(_('Network Interface'))
        self.vLayout = QtWidgets.QVBoxLayout()
        self.groupBoxEnabled = QtWidgets.QGroupBox(_('Enable or Disable Network Interface Monitor? '))
        self.gbLayout = QtWidgets.QVBoxLayout()
        self.rbEnable = QtWidgets.QRadioButton(_('Enabled'))
        self.rbEnable.clicked.connect(self.groupBoxClicked)
        self.gbLayout.addWidget(self.rbEnable)
        self.rbDisable = QtWidgets.QRadioButton(_('Disabled'))
        self.rbDisable.clicked.connect(self.groupBoxClicked)
        self.rbDisable.setChecked(True)
        self.gbLayout.addWidget(self.rbDisable)

        self.groupBoxEnabled.setLayout(self.gbLayout)

        self.vLayout.addWidget(self.groupBoxEnabled)

        self.questionLabel = QtWidgets.QLabel(_('Please select the network interface you want to monitor.'))
        self.vLayout.addWidget(self.questionLabel)

        self.optionsList = QtWidgets.QListWidget()
        self.optionsList.clicked.connect(self.optionsClick)
        self.vLayout.addWidget(self.optionsList)
        self.setLayout(self.vLayout)
        self.displayAvailablesInterfaces()

    def updateNetOption(self, interface, enabled):
        self.keysSkeleton.netOption.clear()
        self.keysSkeleton.netOption.update(
            {
                'netOption': {
                    'interface': interface,
                    'enabled': enabled
                }
            }
        )
        self.config.updateConfig(self.keysSkeleton.netOption)
        # print(self.keysSkeleton.netOption)

    def displayAvailablesInterfaces(self):
        network = psutil.net_if_addrs()
        # print(network['enp6s0'][0].address)
        # print(f"{type(network['enp6s0'][0])}")
        for interface in psutil.net_if_addrs():
            if interface != 'lo':
                self.optionsList.addItem('{}|\t[{}]'.format(interface, network[interface][0].address))

        # Verify if exists key in config
        netOptionConfig = self.config.getKey('netOption')
        if netOptionConfig is None:
            self.updateNetOption('', False)
        else:
            self.updateNetOption(
                netOptionConfig['interface'],
                netOptionConfig['enabled']
            )

        if not self.keysSkeleton.netOption['netOption']['enabled']:
            self.optionsList.setDisabled(True)
        else:
            self.optionsList.setEnabled(True)
            self.rbEnable.setChecked(True)

        self.common.displayRow(self.optionsList, self.keysSkeleton.netOption['netOption']['interface'])

    def groupBoxClicked(self):
        enabled = False
        if self.rbEnable.isChecked():
            self.optionsList.setEnabled(True)
            enabled = True
        else:
            self.optionsList.setDisabled(True)

        self.keysSkeleton.netOption['netOption']['enabled'] = enabled
        self.updateNetOption(self.keysSkeleton.netOption['netOption']['interface'], enabled)

    def optionsClick(self):
        rowList = self.optionsList.currentItem().text().split('|')
        self.updateNetOption(rowList[0], self.keysSkeleton.netOption['netOption']['enabled'])


class StorTempsPage(QtWidgets.QWizardPage):
    storTemps = StorTemps()
    keysSkeleton = KeysSkeleton()
    config = Config()
    common = CommomAttributes()

    def __init__(self, parent=None):
        super(StorTempsPage, self).__init__(parent)
        self.setTitle(_('Storages Temperatures'))
        subTitleComplement = ''
        if not self.storTemps.hddtempIsOk():
            subTitleComplement = _('Warning: [Your computer is not running hddtemp as daemon! ]')

        self.setSubTitle(
            _(
                'Remember, to monitor SSD/HDD Sata temperatures you need hddtemp running as daemon.') + f' {subTitleComplement}')
        self.vLayout = QtWidgets.QVBoxLayout()
        self.groupBoxEnabled = QtWidgets.QGroupBox('Enable or Disable Storages Temperature Monitor? ')
        self.gbLayout = QtWidgets.QVBoxLayout()
        self.rbEnable = QtWidgets.QRadioButton(_('Enabled'))
        self.rbEnable.clicked.connect(self.groupBoxClicked)
        self.gbLayout.addWidget(self.rbEnable)
        self.rbDisable = QtWidgets.QRadioButton(_('Disabled'))
        self.rbDisable.clicked.connect(self.groupBoxClicked)
        self.rbDisable.setChecked(True)
        self.gbLayout.addWidget(self.rbDisable)

        self.groupBoxEnabled.setLayout(self.gbLayout)

        self.vLayout.addWidget(self.groupBoxEnabled)

        self.questionLabel = QtWidgets.QLabel(
            _(
                'Please select the Storage Temperature you want to monitor. Press <shift> or <ctrl> to multiples selections.'))
        self.vLayout.addWidget(self.questionLabel)

        self.optionsList = QtWidgets.QListWidget()
        self.optionsList.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.optionsList.clicked.connect(self.optionsClick)
        self.vLayout.addWidget(self.optionsList)
        self.setLayout(self.vLayout)
        self.displayStorTemps()

    def updateStorTempsOption(self, devices, enabled):
        self.keysSkeleton.storTempsOption.clear()
        self.keysSkeleton.storTempsOption.update(
            {
                'storTempsOption': {
                    'devices': devices,
                    'enabled': enabled
                }
            }
        )
        self.config.updateConfig(self.keysSkeleton.storTempsOption)
        # print(self.keysSkeleton.storTempsOption)

    def displayStorTemps(self):
        sensors = psutil.sensors_temperatures()
        # print(sensors)
        # Show nvmes
        for sensor in sensors:
            if 'nvme' in sensor:
                for nvme in sensors[sensor]:
                    self.optionsList.addItem(f'{sensor}|{nvme.label}| temp. {nvme.current} °C')

        # hddtemp section
        if self.storTemps.hddtempIsOk():
            with Telnet('127.0.0.1', 7634) as tn:
                lines = tn.read_all().decode('utf-8')

            if lines != '':
                data = lines
                # remove first char
                data = data[1:]
                # remove the last char
                data = ''.join([data[i] for i in range(len(data)) if i != len(data) - 1])
                # replace double || by one |
                data = data.replace('||', '|')
                # convert to array
                data = data.split('|')
                dataLen = len(data)
                forLenght = int(dataLen / 4)

                newarray = self.storTemps.chunkIt(data, forLenght)

                for na in newarray:
                    self.optionsList.addItem(f'{na[0]}|{na[1]}| temp. {na[2]} °C')

        # Verify if exists key in config
        storTempsConfig = self.config.getKey('storTempsOption')
        if storTempsConfig is None:
            self.updateStorTempsOption(list(), False)
        else:
            self.updateStorTempsOption(
                storTempsConfig['devices'],
                storTempsConfig['enabled']
            )

        if not self.keysSkeleton.storTempsOption['storTempsOption']['enabled']:
            self.optionsList.setDisabled(True)
        else:
            self.optionsList.setEnabled(True)
            self.rbEnable.setChecked(True)

        self.displayCorrectRows()

    def groupBoxClicked(self):
        enabled = False
        if self.rbEnable.isChecked():
            self.optionsList.setEnabled(True)
            enabled = True
        else:
            self.optionsList.setDisabled(True)

        self.keysSkeleton.storTempsOption['storTempsOption']['enabled'] = enabled
        self.updateStorTempsOption(self.keysSkeleton.storTempsOption['storTempsOption']['devices'], enabled)

    def optionsClick(self):
        items = self.optionsList.selectedItems()
        tempList = list()
        for i in range(len(items)):
            # print(self.optionsList.selectedItems()[i].text())
            cols = self.optionsList.selectedItems()[i].text().split('|')
            tempList.append(
                {
                    'device': cols[0],
                    'label': cols[1]
                }
            )

        self.updateStorTempsOption(tempList, self.keysSkeleton.storTempsOption['storTempsOption']['enabled'])

    def displayCorrectRows(self):
        for i, device in enumerate(self.keysSkeleton.storTempsOption['storTempsOption']['devices']):
            line = self.optionsList.item(i).text()
            cols = line.split('|')
            # print(cols)
            # print(device)
            if (device['device'] == cols[0]) and (device['label'] == cols[1]):
                self.optionsList.item(i).setSelected(True)


class PartitionsPage(QtWidgets.QWizardPage):
    storTemps = StorTemps()
    keysSkeleton = KeysSkeleton()
    config = Config()
    common = CommomAttributes()

    def __init__(self, parent=None):
        super(PartitionsPage, self).__init__(parent)
        self.setTitle(_('Partitions'))
        self.vLayout = QtWidgets.QVBoxLayout()
        self.groupBoxEnabled = QtWidgets.QGroupBox(_('Enable or Disable Partitions Space Monitor? '))
        self.gbLayout = QtWidgets.QVBoxLayout()
        self.rbEnable = QtWidgets.QRadioButton(_('Enabled'))
        self.rbEnable.clicked.connect(self.groupBoxClicked)
        self.gbLayout.addWidget(self.rbEnable)
        self.rbDisable = QtWidgets.QRadioButton(_('Disabled'))
        self.rbDisable.clicked.connect(self.groupBoxClicked)
        self.rbDisable.setChecked(True)
        self.gbLayout.addWidget(self.rbDisable)

        self.groupBoxEnabled.setLayout(self.gbLayout)

        self.vLayout.addWidget(self.groupBoxEnabled)

        self.questionLabel = QtWidgets.QLabel(
            _('Please select the partitions you want to monitor. Press <shift> or <ctrl> to multiples selections.'))
        self.vLayout.addWidget(self.questionLabel)

        self.optionsList = QtWidgets.QListWidget()
        self.optionsList.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.optionsList.clicked.connect(self.optionsClick)
        self.vLayout.addWidget(self.optionsList)
        self.setLayout(self.vLayout)
        self.displayPartitionsOption()

    def updatePartitionsOption(self, devices, enabled):
        self.keysSkeleton.partitionsOption.clear()
        self.keysSkeleton.partitionsOption.update(
            {
                'partitionsOption': {
                    'partitions': devices,
                    'enabled': enabled
                }
            }
        )
        self.config.updateConfig(self.keysSkeleton.partitionsOption)

    def displayPartitionsOption(self):
        for partition in psutil.disk_partitions():
            # print(partition)
            self.optionsList.addItem(
                f'{partition.device}|' + _('mountpoint:') + f'|{partition.mountpoint}|{partition.fstype}')

        # Verify if exists key in config
        partitionOptionConfig = self.config.getKey('partitionsOption')
        # print(f'partitionOptionConfig: {partitionOptionConfig}')
        if partitionOptionConfig is None:
            self.updatePartitionsOption(list(), False)
        else:
            self.updatePartitionsOption(
                partitionOptionConfig['partitions'],
                partitionOptionConfig['enabled']
            )

        if not self.keysSkeleton.partitionsOption['partitionsOption']['enabled']:
            self.optionsList.setDisabled(True)
        else:
            self.optionsList.setEnabled(True)
            self.rbEnable.setChecked(True)

        self.displayCorrectRows()

    def groupBoxClicked(self):
        enabled = False
        if self.rbEnable.isChecked():
            self.optionsList.setEnabled(True)
            enabled = True
        else:
            self.optionsList.setDisabled(True)

        self.keysSkeleton.partitionsOption['partitionsOption']['enabled'] = enabled
        self.updatePartitionsOption(self.keysSkeleton.partitionsOption['partitionsOption']['partitions'], enabled)

    def optionsClick(self):
        items = self.optionsList.selectedItems()
        tempList = list()
        for i in range(len(items)):
            # print(self.optionsList.selectedItems()[i].text())
            cols = self.optionsList.selectedItems()[i].text().split('|')
            # print(cols)
            tempList.append(
                {
                    'partition': cols[0],
                    'mountpoint': cols[2],
                    'fstype': cols[3]
                }
            )
        #
        self.updatePartitionsOption(tempList, self.keysSkeleton.partitionsOption['partitionsOption']['enabled'])

    def displayCorrectRows(self):
        for i in range(self.optionsList.count()):
            # print(self.optionsList.item(i).text())
            line = self.optionsList.item(i).text()
            cols = line.split('|')
            for partConfig in self.keysSkeleton.partitionsOption['partitionsOption']['partitions']:
                if (partConfig['partition'] == cols[0]) and (partConfig['mountpoint'] == cols[2]):
                    self.optionsList.item(i).setSelected(True)


class WeatherPage(QtWidgets.QWizardPage):
    storTemps = StorTemps()
    keysSkeleton = KeysSkeleton()
    config = Config()
    common = CommomAttributes()
    threadValidateWeather = ThreadValidateWeather()
    net = Net()

    def __init__(self, parent=None):
        super(WeatherPage, self).__init__(parent)
        self.setTitle(_('Weather'))
        self.vLayout = QtWidgets.QVBoxLayout()
        messageLabel = QtWidgets.QLabel(
            _('To view weather information you need an account at <a href="https://openweathermap.org/">https://openweathermap.org/</a> and place your api key.'))
        self.vLayout.addWidget(messageLabel)
        messageLabel.setTextFormat(QtCore.Qt.RichText)
        # self.sub
        self.groupBoxEnabled = QtWidgets.QGroupBox(_('Do you want to enable date, time and weather conditions? '))
        self.gbLayout = QtWidgets.QVBoxLayout()
        self.rbEnable = QtWidgets.QRadioButton(_('Enabled'))
        self.rbEnable.clicked.connect(self.groupBoxClicked)
        self.gbLayout.addWidget(self.rbEnable)
        self.rbDisable = QtWidgets.QRadioButton(_('Disabled'))
        self.rbDisable.clicked.connect(self.groupBoxClicked)
        self.rbDisable.setChecked(True)
        self.gbLayout.addWidget(self.rbDisable)

        self.groupBoxEnabled.setLayout(self.gbLayout)

        self.vLayout.addWidget(self.groupBoxEnabled)

        self.questionLabel = QtWidgets.QLabel(
            _('Please fill in the fields below correctly and click on the validate button.'))
        self.vLayout.addWidget(self.questionLabel)

        # -----------------------------------------------------------------
        gridLayout = QtWidgets.QGridLayout()
        latitudeLabel = QtWidgets.QLabel('Latitude:')
        latitudeLabel.setFixedWidth(100)
        gridLayout.addWidget(latitudeLabel, 0, 0)

        self.latitudeEdit = QtWidgets.QLineEdit()
        self.latitudeEdit.setFixedWidth(200)
        gridLayout.addWidget(self.latitudeEdit, 0, 1)

        longitudeLabel = QtWidgets.QLabel('Longitude:')
        longitudeLabel.setFixedWidth(100)
        gridLayout.addWidget(longitudeLabel, 1, 0)

        self.longitudeEdit = QtWidgets.QLineEdit()
        self.longitudeEdit.setFixedWidth(200)
        gridLayout.addWidget(self.longitudeEdit, 1, 1)

        updateTimeLabel = QtWidgets.QLabel(_('Update time:'))
        updateTimeLabel.setFixedWidth(100)
        gridLayout.addWidget(updateTimeLabel, 2, 0)

        updateTimeLayout = QtWidgets.QHBoxLayout()
        self.updateTimeSpinner = QtWidgets.QSlider()
        self.updateTimeSpinner.setOrientation(QtCore.Qt.Horizontal)
        self.updateTimeSpinner.setMinimum(10)
        self.updateTimeSpinner.setMaximum(60)
        self.updateTimeSpinner.setValue(30)
        self.updateTimeSpinner.valueChanged.connect(self.updateTimeChanged)
        updateTimeLayout.addWidget(self.updateTimeSpinner)

        self.updateTimeValue = QtWidgets.QLabel('30 ' + _('minutes'))
        updateTimeLayout.addWidget(self.updateTimeValue)

        gridLayout.addLayout(updateTimeLayout, 2, 1)

        apiKeyLabel = QtWidgets.QLabel(_('Api Key:'))
        gridLayout.addWidget(apiKeyLabel, 3, 0)

        self.apiKeyEdit = QtWidgets.QLineEdit()
        gridLayout.addWidget(self.apiKeyEdit, 3, 1)

        self.validateButton = QtWidgets.QPushButton(_('Validate'))
        self.validateButton.setFixedWidth(100)
        gridLayout.addWidget(self.validateButton, 4, 1)
        self.validateButton.clicked.connect(self.validateButtonClicked)
        self.threadValidateWeather.signal.connect(self.threadValidaWeatherFinish)

        statusLabel = QtWidgets.QLabel(_('Status: '))
        gridLayout.addWidget(statusLabel, 5, 0)

        hLayout = QtWidgets.QHBoxLayout()

        self.statusIcon = QtWidgets.QLabel()
        self.statusIcon.setFixedWidth(24)
        self.statusIcon.setFixedHeight(24)
        hLayout.addWidget(self.statusIcon)

        self.statusValueLabel = QtWidgets.QLabel()
        hLayout.addWidget(self.statusValueLabel)

        gridLayout.addLayout(hLayout, 5, 1)

        self.vLayout.addLayout(gridLayout)
        self.setLayout(self.vLayout)
        self.displayUi()

    def updateTimeChanged(self):
        self.updateTimeValue.setText('{} {}'.format(self.updateTimeSpinner.value(), _('minutes')))
        self.updateWeatherOption(
            self.latitudeEdit.text(),
            self.longitudeEdit.text(),
            self.updateTimeSpinner.value(),
            self.apiKeyEdit.text(),
            self.keysSkeleton.weatherOption['weatherOption']['validated'],
            self.rbEnable.isChecked()
        )

    def displayUi(self):
        weatherOptionConfig = self.config.getKey('weatherOption')
        lat = self.latitudeEdit.text()
        lon = self.longitudeEdit.text()
        apiKey = self.apiKeyEdit.text()
        enabled = False
        validated = False
        updateTime = 30
        self.rbEnable.setChecked(False)
        if not (weatherOptionConfig is None):
            lat = weatherOptionConfig['lat']
            self.latitudeEdit.setText(lat)
            lon = weatherOptionConfig['lon']
            self.longitudeEdit.setText(lon)
            updateTime = weatherOptionConfig['updateTime']
            self.updateTimeSpinner.setValue(updateTime)
            apiKey = weatherOptionConfig['apiKey']
            self.apiKeyEdit.setText(apiKey)
            enabled = weatherOptionConfig['enabled']
            validated = weatherOptionConfig['validated']
            if validated:
                self.statusIcon.setPixmap(QtGui.QPixmap(f'{FileUtil.getResourcePath()}/images/validated.png'))
                self.statusValueLabel.setText(_('Validated!'))

        self.updateAll(enabled)
        self.rbEnable.setChecked(enabled)
        self.updateWeatherOption(
            lat,
            lon,
            updateTime,
            apiKey,
            validated,
            enabled
        )

    def threadValidaWeatherFinish(self, message):
        self.validateButton.setEnabled(True)
        self.statusValueLabel.setText(message['statusText'])
        if message['statusCode'] == 200:
            validated = False
            if message['validated']:
                self.statusIcon.setPixmap(QtGui.QPixmap(f'{FileUtil.getResourcePath()}/images/validated.png'))
                validated = True
            else:
                self.statusIcon.setPixmap(QtGui.QPixmap(f'{FileUtil.getResourcePath()}/images/unvalidated.png'))

            self.updateWeatherOption(
                self.latitudeEdit.text(),
                self.longitudeEdit.text(),
                self.updateTimeSpinner.value(),
                self.apiKeyEdit.text(),
                validated,
                self.keysSkeleton.weatherOption['weatherOption']['enabled']
            )
        else:
            self.statusIcon.setPixmap(QtGui.QPixmap(f'{FileUtil.getResourcePath()}/images/unvalidated.png'))

    def validateButtonClicked(self):
        if self.net.isOnline():
            self.validateButton.setEnabled(False)
            lat = self.latitudeEdit.text()
            lat = lat.strip()
            lon = self.longitudeEdit.text()
            lon = lon.strip()
            updateTime = self.updateTimeSpinner.value()
            validated = self.keysSkeleton.weatherOption['weatherOption']['validated']
            enabled = self.rbEnable.isChecked()
            apiKey = self.apiKeyEdit.text()
            apiKey.strip()
            self.updateWeatherOption(lat, lon, updateTime, apiKey, validated, enabled)

            self.threadValidateWeather.updateAndStart(
                self.latitudeEdit.text(),
                self.longitudeEdit.text(),
                self.apiKeyEdit.text()
            )

    def updateWeatherOption(self, lat, lon, updateTime, apiKey, validated, enabled):
        self.keysSkeleton.weatherOption.clear()
        self.keysSkeleton.weatherOption.update(
            {
                'weatherOption': {
                    'lat': lat,
                    'lon': lon,
                    'updateTime': updateTime,
                    'apiKey': apiKey,
                    'validated': validated,
                    'enabled': enabled

                }
            }
        )
        self.config.updateConfig(self.keysSkeleton.weatherOption)

    def updateAll(self, enabled):
        self.latitudeEdit.setEnabled(enabled)
        self.longitudeEdit.setEnabled(enabled)
        self.updateTimeSpinner.setEnabled(enabled)
        self.updateTimeValue.setEnabled(enabled)
        self.apiKeyEdit.setEnabled(enabled)
        self.validateButton.setEnabled(enabled)

    def groupBoxClicked(self):
        enabled = False
        if self.rbEnable.isChecked():
            enabled = True
            self.updateAll(enabled)
        else:
            self.updateAll(enabled)

        self.keysSkeleton.weatherOption['weatherOption']['enabled'] = enabled
        self.updateWeatherOption(
            self.latitudeEdit.text(),
            self.longitudeEdit.text(),
            self.updateTimeSpinner.value(),
            self.apiKeyEdit.text(),
            self.keysSkeleton.weatherOption['weatherOption']['validated'],
            enabled
        )
