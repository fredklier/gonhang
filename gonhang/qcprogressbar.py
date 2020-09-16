from PyQt5 import QtWidgets, QtCore, QtGui


class QCProgressBar(QtWidgets.QWidget):
    _value = 0

    def __init__(self):
        super(QCProgressBar, self).__init__()
        self.setSizePolicy(
           QtWidgets.QSizePolicy.MinimumExpanding,
           QtWidgets.QSizePolicy.MinimumExpanding
        )

    def paintEvent(self, e):
        painter = QtGui.QPainter(self)
        brush = QtGui.QBrush()
        brush.setStyle(QtCore.Qt.SolidPattern)
        rect = QtCore.QRect(0, 0, painter.device().width(), painter.device().height())
        painter.fillRect(rect, brush)

        # -----------------------------------------------------------
        # Draw the bars.
        brush.setStyle(QtCore.Qt.SolidPattern)
        if self.value() ==0:
            divisions = 1
        else:
            divisions = int(self.width() / self.value())

        for i in range(0, self.value(), 2):
            brush.setColor(QtGui.QColor(34, 255, 19))
            if (i >= 35) and (i < 65):
                brush.setColor(QtGui.QColor(250, 246, 145))
            elif i >= 65:
                brush.setColor(QtGui.QColor(255, 51, 0))

            redRect = QtCore.QRect(i * divisions, 0, divisions, self.height())
            painter.fillRect(redRect, brush)

        painter.end()

    def value(self):
        return self._value

    def setValue(self, value):
        self._value = int(value)
        self.update()

    def _trigger_refresh(self):
        self.update()
