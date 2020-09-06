from PyQt5 import QtWidgets, QtGui
from gonhang.api import FileUtil


class GonhaNgWizard(QtWidgets.QWizard):

    def __init__(self, parent=None):
        super(GonhaNgWizard, self).__init__(parent)
        self.addPage(PositionPage(self))
        self.addPage(Page2(self))
        self.setWindowTitle('GonhaNG Wizard Welcome')
        self.resize(640, 480)
        self.setWizardStyle(QtWidgets.QWizard.MacStyle)
        print(f'Resource path: {FileUtil.getResourcePath()}')
        self.setPixmap(QtWidgets.QWizard.BackgroundPixmap,
                       QtGui.QPixmap(f'{FileUtil.getResourcePath()}/images/logo.png'))


class PositionPage(QtWidgets.QWizardPage):
    def __init__(self, parent=None):
        super(PositionPage, self).__init__(parent)
        self.setTitle('Position')
        self.setSubTitle('What position on the screen do you want?')
        layout = QtWidgets.QVBoxLayout()
        self.optionsList = QtWidgets.QListWidget()
        self.optionsList.insertItem(0, 'Left')
        self.optionsList.insertItem(1, 'Center')
        self.optionsList.insertItem(2, 'Right')
        self.optionsList.clicked.connect(self.positionClicked)
        layout.addWidget(self.optionsList)
        self.setLayout(layout)

    @staticmethod
    def positionClicked():
        print('clicou em position')


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
