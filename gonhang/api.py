from PyQt5 import QtWidgets


class FileUtil:

    # Return the contents of filename
    @staticmethod
    def getContents(fileName):
        file = open(fileName, mode='r')
        content = file.read()
        file.close()
        return content


# Display an Alert
class Alert(QtWidgets.QDialog):

    def __init__(self, title, message):
        super(Alert, self).__init__()
        self.setWindowTitle(title)
        self.buttonBox = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.accepted.connect(self.accept)
        messageLabel = QtWidgets.QLabel(message)
        self.layout = QtWidgets.QVBoxLayout()
        self.layout.addWidget(messageLabel)
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)
