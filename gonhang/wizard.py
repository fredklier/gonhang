from PyQt5 import QtWidgets, QtGui, QtCore
from gonhang.api import FileUtil
from gonhang.core import Config
from gonhang.core import KeysSkeleton
from gonhang.core import Nvidia
from gonhang.displayclasses import CommomAttributes
import psutil


class GonhaNgWizard(QtWidgets.QWizard):
    nvidia = Nvidia()

    def __init__(self, parent=None):
        super(GonhaNgWizard, self).__init__(parent)
        self.addPage(CpuTempPage(self))
        self.addPage(NetPage(self))
        if self.nvidia.getNumberGPUs() > 0:
            self.addPage(NvidiaPage(self))
        self.setWindowTitle('GonhaNG Wizard Welcome')
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
        self.setTitle('CPU Temperature')
        self.vLayout = QtWidgets.QVBoxLayout()
        self.hint = 'GonhaNG measures the <strong>average</strong> temperature of <strong>all cpu cores</strong> installed in your system.\nIn general this value corresponds to <strong>Tdie</strong>'
        self.hintLabel = QtWidgets.QLabel(self.hint)
        self.hintLabel.setTextFormat(QtCore.Qt.RichText)
        self.vLayout.addWidget(self.hintLabel)

        self.groupBoxEnabled = QtWidgets.QGroupBox('Enable or Disable CPU Temperature? ')
        self.gbLayout = QtWidgets.QVBoxLayout()

        self.rbEnable = QtWidgets.QRadioButton('Enabled')
        self.rbEnable.clicked.connect(self.groupBoxClicked)
        self.gbLayout.addWidget(self.rbEnable)

        self.rbDisable = QtWidgets.QRadioButton('Disabled')
        self.rbDisable.clicked.connect(self.groupBoxClicked)
        self.rbDisable.setChecked(True)
        self.gbLayout.addWidget(self.rbDisable)

        self.groupBoxEnabled.setLayout(self.gbLayout)

        self.vLayout.addWidget(self.groupBoxEnabled)

        self.questionLabel = QtWidgets.QLabel('What is the temperature label of your CPU?')
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
                    '{}|{}| label: [{}] - current temp. {} °C'.format(index, subIndex, shwtemp.label, shwtemp.current)
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
        self.groupBoxEnabled = QtWidgets.QGroupBox('Enable or Disable Nvidia GPU Monitor? ')
        self.gbLayout = QtWidgets.QVBoxLayout()
        self.rbEnable = QtWidgets.QRadioButton('Enabled')
        self.rbEnable.clicked.connect(self.groupBoxClicked)
        self.gbLayout.addWidget(self.rbEnable)
        self.rbDisable = QtWidgets.QRadioButton('Disabled')
        self.rbDisable.clicked.connect(self.groupBoxClicked)
        self.rbDisable.setChecked(True)
        self.gbLayout.addWidget(self.rbDisable)

        self.groupBoxEnabled.setLayout(self.gbLayout)

        self.vLayout.addWidget(self.groupBoxEnabled)

        self.questionLabel = QtWidgets.QLabel('Please select the nvidia gpu you want to monitor.')
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
        self.setTitle('Network Interface')
        self.vLayout = QtWidgets.QVBoxLayout()
        self.groupBoxEnabled = QtWidgets.QGroupBox('Enable or Disable Network Interface Monitor? ')
        self.gbLayout = QtWidgets.QVBoxLayout()
        self.rbEnable = QtWidgets.QRadioButton('Enabled')
        self.rbEnable.clicked.connect(self.groupBoxClicked)
        self.gbLayout.addWidget(self.rbEnable)
        self.rbDisable = QtWidgets.QRadioButton('Disabled')
        self.rbDisable.clicked.connect(self.groupBoxClicked)
        self.rbDisable.setChecked(True)
        self.gbLayout.addWidget(self.rbDisable)

        self.groupBoxEnabled.setLayout(self.gbLayout)

        self.vLayout.addWidget(self.groupBoxEnabled)

        self.questionLabel = QtWidgets.QLabel('Please select the network interface you want to monitor.')
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
                self.optionsList.addItem('{}|\tIP Address: [{}]'.format(interface, network[interface][0].address))

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
