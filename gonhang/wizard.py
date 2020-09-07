from PyQt5 import QtWidgets, QtGui
from gonhang.api import FileUtil
from gonhang.core import Config
import psutil


class GonhaNgWizard(QtWidgets.QWizard):

    def __init__(self, parent=None):
        super(GonhaNgWizard, self).__init__(parent)
        self.addPage(CpuTempPage(self))
        self.addPage(Page2(self))
        self.setWindowTitle('GonhaNG Wizard Welcome')
        self.resize(640, 480)
        self.setWizardStyle(QtWidgets.QWizard.MacStyle)
        self.setPixmap(QtWidgets.QWizard.BackgroundPixmap,
                       QtGui.QPixmap(f'{FileUtil.getResourcePath()}/images/logo.png'))
        self.centerMe()

    def centerMe(self):
        screenGeo = QtWidgets.QApplication.desktop().screenGeometry()
        x = (screenGeo.width() - self.width()) / 2
        y = (screenGeo.height() - self.height()) / 2
        self.move(x, 100)


class CpuTempPage(QtWidgets.QWizardPage):
    config = Config()
    cpuTempOption = dict(
        {
            'cpuTempOption': {
                'index': 0,
                'subIndex': 0,
                'enabled': False
            }
        }
    )

    def __init__(self, parent=None):
        super(CpuTempPage, self).__init__(parent)
        self.setTitle('CPU Temperature')
        self.setSubTitle('What is the temperature label of your CPU?')
        self.vLayout = QtWidgets.QVBoxLayout()
        self.hint = 'GonhaNG measures the average temperature of all the cpu cores installed in your system.\nIn general this value corresponds to Tdie'
        self.hintLabel = QtWidgets.QLabel(self.hint)
        self.vLayout.addWidget(self.hintLabel)

        # self.groupBoxEnabled = QtWidgets.QGroupBox('Enable or Disable? ')
        # self.gbLayout = QtWidgets.QVBoxLayout()
        # self.rbEnable = QtWidgets.QRadioButton('Enable')
        # self.gbLayout.addWidget(self.rbEnabled)

        # self.groupBoxEnabled.setLayout(self.gbLayout)

        # layout.addWidget(self.groupBoxEnabled)

        self.optionsList = QtWidgets.QListWidget()
        self.displayAvailableTemps()
        self.optionsList.clicked.connect(self.optionsClick)
        self.vLayout.addWidget(self.optionsList)
        self.setLayout(self.vLayout)

    def optionsClick(self):
        rowList = self.optionsList.currentItem().text().split('|')
        self.updateCpuTempOption(rowList[0], int(rowList[1]), enabled=False)
        # print(self.cpuTempOption)

    def updateCpuTempOption(self, index, subIndex, enabled):
        self.cpuTempOption.clear()
        self.cpuTempOption.update(
            {
                'cpuTempOption': {
                    'index': index,
                    'subIndex': subIndex,
                    'enabled': enabled
                }
            }
        )
        self.config.updateConfig(self.cpuTempOption)
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
        # print(f'cpuTempOptionConfig: {cpuTempOptionConfig}')
        if cpuTempOptionConfig is None:
            self.updateCpuTempOption(0, 0, False)
        else:
            self.updateCpuTempOption(
                cpuTempOptionConfig['index'],
                cpuTempOptionConfig['subIndex'],
                cpuTempOptionConfig['enabled']
            )

        self.displayCorrectRow()

    def displayCorrectRow(self):
        rowCount = self.optionsList.count()
        currentIndex = self.cpuTempOption['cpuTempOption']['index']
        currentSubIndex = self.cpuTempOption['cpuTempOption']['subIndex']
        for i in range(rowCount):
            rowText = self.optionsList.item(i).text()
            rowList = rowText.split('|')
            if str(currentIndex) == str(rowList[0]) and str(currentSubIndex) == str(rowList[1]):
                self.optionsList.setCurrentRow(i)


class Page2(QtWidgets.QWizardPage):
    def __init__(self, parent=None):
        super(Page2, self).__init__(parent)
        self.label1 = QtWidgets.QLabel()
        self.label2 = QtWidgets.QLabel()
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.label1)
        layout.addWidget(self.label2)
        self.setLayout(layout)

    def initializePage(self):
        self.label1.setText("Example text")
        self.label2.setText("Example text")
