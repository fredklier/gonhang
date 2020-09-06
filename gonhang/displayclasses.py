from PyQt5 import QtWidgets, QtCore, QtGui


class CommomAttributes:

    def __init__(self):
        # -------------------------------------------------------------
        # Styles
        self.groupBoxStyle = """
        QGroupBox {
            border: 1px solid white;
            border-radius: 5px;
            margin-top: 12px;
            padding-left: 2px;
        }
        QGroupBox:title {
            subcontrol-origin: margin;
            subcontrol-position: top left;
            color: rgb(252, 126, 0);
            left: 15px;
        }
        """
        self.yellowPBStyle = """
        QProgressBar {
            text-align: left;
            font-weight: bold;
            color: rgb(255, 255, 255);
            background-color : rgba(0, 0, 0, 0);
            border: 0px solid rgba(0, 0, 0, 0);
            border-radius: 3px;                                    
        }
        QProgressBar::chunk {
            background: rgb(255, 153, 0);
            border-radius: 3px;            
        }
        """

        self.redPBStyle = """
        QProgressBar {
            text-align: left;
            font-weight: bold;
            color: rgb(255, 255, 255);
            background-color : rgba(0, 0, 0, 0);
            border: 0px solid rgba(0, 0, 0, 0);
            border-radius: 3px;                                    
        }
        QProgressBar::chunk {
            background: rgb(255, 51, 0);
            border-radius: 3px;            
        }
        """
        self.greenPBStyle = """
        QProgressBar {
            text-align: left;
            font-weight: bold;
            color: rgb(255, 255, 255);
            background-color : rgba(0, 0, 0, 0);
            border: 0px solid rgba(0, 0, 0, 0);
            border-radius: 3px;           
        }
        QProgressBar::chunk {
            background: rgb(51, 153, 51);
            border-radius: 3px;            
        }
        """
        self.orange = 'color: rgb(252, 126, 0);'
        self.white = 'color: rgb(255, 255, 255);'
        self.green = 'color: rgb(34, 255, 19);'
        self.red = 'color: rgb(255, 51, 0);'
        self.yellow = 'color: rgb(255, 153, 0);'

        # ---------------------------------------------------------------------
        # Default font
        self.fontDefault = QtGui.QFont('Fira Code', 11)
        self.fontGroupBox = QtGui.QFont('Fira Code', 14)
        self.groupBoxDefaultWidth = 450

    def getDefaultGb(self, title):
        defaultGb = QtWidgets.QGroupBox(title)
        defaultGb.setFont(self.fontGroupBox)
        defaultGb.setStyleSheet(self.groupBoxStyle)
        defaultGb.setFixedWidth(self.groupBoxDefaultWidth)
        return defaultGb

    @staticmethod
    def setLabel(label, labelcolor, font):
        label.setFont(font)
        label.setStyleSheet(labelcolor)


class DisplaySystem:
    commom = CommomAttributes()
    systemWidgets = dict()

    def initUi(self):
        pbDefaultWidth = 180
        iconDefaultWidth = 80
        systemGroupBox = self.commom.getDefaultGb('system')

        verticalLayout = QtWidgets.QVBoxLayout()
        verticalLayout.setSpacing(0)

        distroGridLayout = QtWidgets.QGridLayout()
        distroGridLayout.setAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignHCenter)
        distroGridLayout.setSpacing(0)
        # ---------------------------------------------------------------------------
        # distro Icon
        # ---------------------------------------------------------------------------
        distroIcon = QtWidgets.QLabel()
        self.systemWidgets['distroIcon'] = distroIcon

        distroGridLayout.addWidget(distroIcon, 0, 0, -1, 1)

        # ---------------------------------------------------------------------------
        # Distro label
        distroLabel = QtWidgets.QLabel()
        self.commom.setLabel(distroLabel, self.commom.white, self.commom.fontDefault)
        self.systemWidgets['distroStr'] = distroLabel

        distroGridLayout.addWidget(distroLabel, 0, 1)

        # ---------------------------------------------------------------------------
        # kernel label
        kernelLabel = QtWidgets.QLabel()
        self.commom.setLabel(kernelLabel, self.commom.white, self.commom.fontDefault)
        self.systemWidgets['release'] = kernelLabel

        distroGridLayout.addWidget(kernelLabel, 1, 1)
        # ---------------------------------------------------------------------------
        # Machine Label
        machineLabel = QtWidgets.QLabel()
        self.commom.setLabel(machineLabel, self.commom.white, self.commom.fontDefault)
        self.systemWidgets['nodeMachine'] = machineLabel

        distroGridLayout.addWidget(machineLabel, 2, 1)
        # ---------------------------------------------------------------------------

        # # ---------------------------------------------------------------------------
        # # boot time label
        # verticalLayout.addLayout(distroGridLayout)
        #
        # bootAndCpuModelLayout = QtWidgets.QVBoxLayout()
        # bootAndCpuModelLayout.setSpacing(0)
        # btHLayout = QtWidgets.QHBoxLayout()
        # btHLayout.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        #
        # # --------------------------------------------------------------------
        # # days, hours, minutes and seconds labels
        #
        # btDaysLabel = QtWidgets.QLabel()
        # self.commom.setLabel(btDaysLabel, self.commom.green, self.commom.fontDefault)
        # btHLayout.addWidget(btDaysLabel)
        # self.systemWidgets['btDays'] = btDaysLabel
        #
        # daysLabel = QtWidgets.QLabel('days, ')
        # self.commom.setLabel(daysLabel, self.commom.white, self.commom.fontDefault)
        # btHLayout.addWidget(daysLabel)
        #
        # btHoursLabel = QtWidgets.QLabel()
        # self.commom.setLabel(btHoursLabel, self.commom.green, self.commom.fontDefault)
        # btHLayout.addWidget(btHoursLabel)
        # self.systemWidgets['btHours'] = btHoursLabel
        #
        # hoursLabel = QtWidgets.QLabel('hours ')
        # self.commom.setLabel(hoursLabel, self.commom.white, self.commom.fontDefault)
        # btHLayout.addWidget(hoursLabel)
        #
        # btMinutesLabel = QtWidgets.QLabel()
        # self.commom.setLabel(btMinutesLabel, self.commom.green, self.commom.fontDefault)
        # btHLayout.addWidget(btMinutesLabel)
        # self.systemWidgets['btMinutes'] = btMinutesLabel
        #
        # minutesLabel = QtWidgets.QLabel('minutes ')
        # self.commom.setLabel(minutesLabel, self.commom.white, self.commom.fontDefault)
        # btHLayout.addWidget(minutesLabel)
        #
        # btSecondsLabel = QtWidgets.QLabel()
        # self.commom.setLabel(btSecondsLabel, self.commom.green, self.commom.fontDefault)
        # btHLayout.addWidget(btSecondsLabel)
        # self.systemWidgets['btSeconds'] = btSecondsLabel
        #
        # secondsLabel = QtWidgets.QLabel('seconds')
        # self.commom.setLabel(secondsLabel, self.commom.white, self.commom.fontDefault)
        # btHLayout.addWidget(secondsLabel)
        #
        # bootAndCpuModelLayout.addLayout(btHLayout)

        systemGroupBox.setLayout(verticalLayout)

        return systemGroupBox
