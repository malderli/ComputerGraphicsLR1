from PyQt5.QtWidgets import QWidget
from PyQt5.Qt import QGridLayout

from drawingarea import DrawingArea
from controls import Controls
import graphconv


class MainLogic:
    def __init__(self):
        self.waitedRotationPoint = False
        self.rotationPoint = None

        self.waitedPolygonPoints = False
        self.polygonPoints = []
        self.polygon = None
        self.polygonPointsNum = 3

        self.mainWindow = QWidget()
        self.lytMainWindow = QGridLayout()

        self.mainWindow.setWindowTitle('КГ ЛР1 | Лазарев Михайлин Тетерев')

        self.drawingArea = DrawingArea()
        self.drawingArea.signalDotAdded.connect(self.graphDotAdded)

        self.controls = Controls()
        self.controls.signalSetRPoint.connect(self.controlRotationPoint)
        self.controls.signalSetPolygonPoints.connect(self.controlPolygonPoints)
        self.controls.signalApplyRotation.connect(self.controlRotate)

        self.lytMainWindow.addWidget(self.drawingArea, 0, 0)
        self.lytMainWindow.addWidget(self.controls, 1, 0)

        self.mainWindow.setLayout(self.lytMainWindow)

        self.mainWindow.show()

        self.mainWindow.setFixedSize(self.mainWindow.size())

    def controlRotationPoint(self, state):
        if state:
            self.rotationPoint = None

            self.drawingArea.clearAll()

            if (self.polygonPoints != []) and (len(self.polygonPoints) == self.polygonPointsNum):
                # for dot in self.polygonPoints:
                #     self.drawingArea.addDot(dot['x'], dot['y'], dot['radius'], dot['color'])

                self.drawingArea.addPolygon(self.polygon, '#000000')

            self.drawingArea.repaint()

            self.drawingArea.addDotByClick(3, '#FF0000')

            self.waitedRotationPoint = True
        else:
            self.drawingArea.stopDotCatch()
            self.waitedRotationPoint = False

    def controlPolygonPoints(self, state, num):
        if state:
            self.polygonPoints = []
            self.polygon = None
            self.polygonPointsNum = num

            self.drawingArea.clearAll()

            if self.rotationPoint is not None:
                self.drawingArea.addDot(self.rotationPoint['x'], self.rotationPoint['y'],
                                        self.rotationPoint['radius'], self.rotationPoint['color'])

            self.drawingArea.repaint()

            self.drawingArea.addDotByClick(3, '#0000FF')

            self.waitedPolygonPoints = True
        else:
            self.drawingArea.stopDotCatch()
            self.waitedPolygonPoints = False

    def controlRotate(self, angle):
        self.polygon = graphconv.rotate(angle, (self.rotationPoint['x'], self.rotationPoint['y']), self.polygon)

        self.drawingArea.clearAll()

        if self.rotationPoint is not None:
            self.drawingArea.addDot(self.rotationPoint['x'], self.rotationPoint['y'],
                                    self.rotationPoint['radius'], self.rotationPoint['color'])

        self.drawingArea.addPolygon(self.polygon, '#000000')

        self.drawingArea.repaint()

    def graphDotAdded(self, data):
        if self.waitedRotationPoint:
            self.controls.switchRPointSetMode(False)
            self.waitedRotationPoint = False
            self.rotationPoint = data

        elif self.waitedPolygonPoints:
            self.polygonPoints.append(data)

            if len(self.polygonPoints) == self.polygonPointsNum:
                self.controls.switchPolygonSetMode(False)
                self.waitedPolygonPoints = False

                self.polygon = [(dot['x'], dot['y']) for dot in self.polygonPoints]

                self.drawingArea.clearAll()

                if self.rotationPoint is not None:
                    self.drawingArea.addDot(self.rotationPoint['x'], self.rotationPoint['y'],
                                            self.rotationPoint['radius'], self.rotationPoint['color'])

                self.drawingArea.addPolygon([(dot['x'], dot['y']) for dot in self.polygonPoints], '#000000')
            else:
                self.drawingArea.addDotByClick(3, '#0000FF')
