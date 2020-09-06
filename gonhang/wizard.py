from PyQt5 import QtWidgets


class SecondWindow(QtWidgets.QDialog):
    def __init__(self, *args, **kwargs):
        super(SecondWindow, self).__init__(*args, **kwargs)

        self.main_layout = QtWidgets.QVBoxLayout(self)

        self.hello_label = QtWidgets.QLabel('Hello I am the second window.', self)

        self.main_layout.addWidget(self.hello_label)
