from PyQt5 import QtCore, QtWidgets, QtGui
from gonhang.api import FileUtil
from gonhang.displayclasses import AboutBox


class SystemTrayIcon(QtWidgets.QSystemTrayIcon):

    def __init__(self, icon, parent=None):
        QtWidgets.QSystemTrayIcon.__init__(self, icon, parent)
        menu = QtWidgets.QMenu(parent)
        self.setContextMenu(menu)
        positionMenu = menu.addMenu('Position')
        positionLeftAction = positionMenu.addAction('Left')
        positionLeftAction.triggered.connect(self.moveMeToLeft)
        positionCenterAction = positionMenu.addAction('Center')
        positionCenterAction.triggered.connect(self.moveMeToCenter)
        positionRightAction = positionMenu.addAction('Right')
        positionRightAction.triggered.connect(self.moveMeToRight)
        configAction = menu.addAction(QtGui.QIcon(f'{FileUtil.getResourcePath()}/images/gear.png'), 'Config')
        configAction.triggered.connect(self.wizardAction)
        aboutAction = menu.addAction(QtGui.QIcon(f'{FileUtil.getResourcePath()}/images/about.png'), 'About')
        aboutAction.triggered.connect(self.aboutAction)
        exitAction = menu.addAction(QtGui.QIcon(f'{FileUtil.getResourcePath()}/images/exit.png'), 'Exit')
        exitAction.triggered.connect(self.exit)

    def aboutAction(self):
        self.parent().showAboutBox()

    def moveMeToLeft(self):
        self.parent().refreshPosition(0)

    def moveMeToCenter(self):
        self.parent().refreshPosition(1)

    def moveMeToRight(self):
        self.parent().refreshPosition(2)

    def wizardAction(self):
        print('Enter in wizard...')
        self.parent().wizardAction()

    @staticmethod
    def exit():
        QtCore.QCoreApplication.exit()
