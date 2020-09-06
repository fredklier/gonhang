from PyQt5 import QtWidgets, QtGui


class ChildWnd(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.resize(200, 100)
        self.show()
