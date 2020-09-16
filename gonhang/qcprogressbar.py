from PyQt5 import QtWidgets, QtCore, QtGui


class QCProgressBar(QtWidgets.QWidget):
    _value = 95
    _bgcolor = 'gray'
    _barcolor = 'red'

    def __init__(self):
        super(QCProgressBar, self).__init__()
        self.setSizePolicy(
            QtWidgets.QSizePolicy.MinimumExpanding,
            QtWidgets.QSizePolicy.MinimumExpanding
        )

    def paintEvent(self, e):
        painter = QtGui.QPainter(self)
        brush = QtGui.QBrush()
        # brush.setStyle(QtCore.Qt.SolidPattern)
        # brush.setColor(QtGui.QColor(self._bgcolor))
        rect = QtCore.QRect(0, 0, painter.device().width(), painter.device().height())
        painter.fillRect(rect, brush)

        # -----------------------------------------------------------
        # Draw the bars.
        brush.setStyle(QtCore.Qt.SolidPattern)
        brush.setColor(QtGui.QColor(self.barbcolor()))
        divisions = int(self.width() / 100)
        for i in range(0, self.value(), 2):
            redRect = QtCore.QRect(i * divisions, 0, divisions, self.height())
            painter.fillRect(redRect, brush)

        painter.end()

    def barbcolor(self):
        return self._barcolor

    def setBarColor(self, color):
        self._barcolor = color
        self.update()

    def value(self):
        return self._value

    def setValue(self, value):
        self._value = int(value)
        self.update()

    def _trigger_refresh(self):
        self.update()

    def bgcolor(self):
        return self._bgcolor

    def setBgcolor(self, bgcolor):
        self._bgcolor = bgcolor
        self.update()
