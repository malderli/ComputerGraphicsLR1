from PyQt5.QtWidgets import QWidget, QGroupBox, QPushButton, QLineEdit, QSpinBox, QFrame
from PyQt5.Qt import QGridLayout, QHBoxLayout, QSizePolicy, pyqtSignal


class Controls(QGroupBox):
    signalSetPolygonPoints = pyqtSignal(bool, int)
    signalSetRPoint = pyqtSignal(bool)
    signalApplyRotation = pyqtSignal(int)

    def __init__(self):
        super(Controls, self).__init__()

        self.setTitle('Управление')

        self.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)

        self.lytMain = QGridLayout()

        self.sbPolygonPointsCounter = QSpinBox()
        self.sbPolygonPointsCounter.setMinimum(3)
        self.sbPolygonPointsCounter.setMaximum(10)

        self.btnSetPolygonPoints = QPushButton('Разместить многоугольник')
        self.btnSetPolygonPoints.setCheckable(True)
        self.btnSetPolygonPoints.clicked.connect(self.btnSetPolygonPointsClicked)

        self.sbRotationAngle = QSpinBox()
        self.sbRotationAngle.setMinimum(1)
        self.sbRotationAngle.setMaximum(360)

        self.btnSetRotationPoint = QPushButton('Разместить точку поворота')
        self.btnSetRotationPoint.setCheckable(True)
        self.btnSetRotationPoint.clicked.connect(self.btnSetRPointClicked)

        self.btnApplyRotation = QPushButton('Выполнить поворот')
        self.btnApplyRotation.clicked.connect(self.btnRotateClicked)

        self.lytMain.addWidget(self.sbPolygonPointsCounter, 0, 0)
        self.lytMain.addWidget(self.btnSetPolygonPoints, 0, 1, 1, 2)

        self.lytMain.addWidget(self.sbRotationAngle, 1, 0)
        self.lytMain.addWidget(self.btnApplyRotation, 1, 1)
        self.lytMain.addWidget(self.btnSetRotationPoint, 1, 2)

        self.setLayout(self.lytMain)

    def btnSetRPointClicked(self):
        self.btnSetPolygonPoints.setChecked(False)
        self.signalSetRPoint.emit(self.btnSetRotationPoint.isChecked())

    def btnSetPolygonPointsClicked(self):
        self.btnSetRotationPoint.setChecked(False)
        self.signalSetPolygonPoints.emit(self.btnSetPolygonPoints.isChecked(), self.sbPolygonPointsCounter.value())

    def btnRotateClicked(self):
        self.signalApplyRotation.emit(self.sbRotationAngle.value())

    def switchRPointSetMode(self, state):
        self.btnSetRotationPoint.setChecked(state)

    def switchPolygonSetMode(self, state):
        self.btnSetPolygonPoints.setChecked(state)
