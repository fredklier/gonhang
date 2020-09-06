from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import QApplication, QMenu, QSystemTrayIcon, QAction
from gonhang.api import FileUtil


class RightClickMenu(QMenu):

    def __init__(self, parent=None):
        QMenu.__init__(self, 'Gonha NG', parent)
        icon = QtGui.QIcon(f'{FileUtil.getResourcePath()}/images/icon.png')
        offAction = QAction(icon, "&Off", self)
        # offAction.triggered.connect(lambda: sendudp("s53905\n"))
        self.addAction(offAction)


class SystemTrayIcon(QSystemTrayIcon):
    def __init__(self, parent=None):
        QSystemTrayIcon.__init__(self, parent)
        self.setIcon(QtGui.QIcon("gnomeradio.xpm"))

        self.right_menu = RightClickMenu()
        self.setContextMenu(self.right_menu)

        self.activated.connect(self.onTrayIconActivated)

        class SystrayWheelEventObject(QtCore.QObject):
            def eventFilter(self, object, event):
                if type(event) == QtGui.QWheelEvent:
                    if event.delta() > 0:
                        print('event delta')
                    else:
                        print('NO event delta')
                    event.accept()
                    return True
                return False

        self.eventObj = SystrayWheelEventObject()
        self.installEventFilter(self.eventObj)

    @staticmethod
    def onTrayIconActivated(reason):
        if reason == QSystemTrayIcon.DoubleClick:
            print('double click')

    def welcome(self):
        self.showMessage("Hello", "I should be aware of both buttons")

    def show(self):
        QSystemTrayIcon.show(self)
