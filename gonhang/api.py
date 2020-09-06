from PyQt5 import QtWidgets
import string
import random
import os
import re


class FileUtil:

    # Return the contents of filename
    @staticmethod
    def getContents(fileName):
        file = open(fileName, mode='r')
        content = file.read()
        file.close()
        return content

    @staticmethod
    def getResourcePath():
        return os.path.dirname(__file__)


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


class StringUtil:

    @staticmethod
    def removeString(regPattern, stringToUpdate):
        regex = re.compile(regPattern)
        return regex.sub('', stringToUpdate)

    @staticmethod
    def getRandomString(stringLenght):
        letters = string.ascii_lowercase
        result_str = ''.join(random.choice(letters) for i in range(stringLenght))
        return result_str
