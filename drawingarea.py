from PyQt5.QtWidgets import QWidget
from PyQt5.Qt import QSizePolicy, QColor, QPainter, pyqtSignal


class DrawingArea(QWidget):
    signalDotAdded = pyqtSignal(dict)

    def __init__(self):
        super(DrawingArea, self).__init__()

        self.objectsToDraw = []

        self.waitedDot = None

        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setMinimumSize(400, 400)
        self.setMaximumSize(400, 400)

    # def mouseMoveEvent(self, event):
    #     super(DrawingArea, self).mouseMoveEvent(event)
    #     pass

    def mousePressEvent(self, event):
        if self.waitedDot is not None:
            if self.rect().contains(event.pos()):
                self.waitedDot['x'] = event.x()
                self.waitedDot['y'] = event.y()

                self.objectsToDraw.append(self.waitedDot)

                self.waitedDot = None

                self.signalDotAdded.emit(self.objectsToDraw[-1])

                self.repaint()

    def paintEvent(self, QPaintEvent):
        painter = QPainter(self)

        painter.setRenderHint(painter.Antialiasing)
        painter.save()

        painter.setBrush(QColor('#FFFFFF'))
        painter.setPen(QColor('#000000'))

        painter.drawRect(self.rect())

        # Draw objects
        for item in self.objectsToDraw:
            if item['object_type'] == 'dot':
                painter.setBrush(QColor(item['color']))
                painter.setPen(QColor(item['color']))
                painter.drawEllipse(item['x'], item['y'], item['radius'], item['radius'])

            elif item['object_type'] == 'line':
                painter.setBrush(QColor(item['color']))
                painter.setPen(QColor(item['color']))
                painter.drawLine(item['x1'], item['y1'], item['x2'], item['y2'])

        painter.restore()

    def addDotByClick(self, radius, color):
        self.waitedDot = {'object_type': 'dot', 'radius': radius, 'color': color, 'x': -1, 'y': -1}

    def stopDotCatch(self):
        self.waitedDot = None

    def addDot(self, x, y, radius, color):
        self.objectsToDraw.append({'object_type': 'dot', 'radius': radius, 'color': color, 'x': x, 'y': y})

    def addLine(self, x1, y1, x2, y2, color):
        pass

    def addPolygon(self, points, color):
        for i in range(len(points) - 1):
            self.objectsToDraw.append({'object_type': 'line', 'color': color,
                                       'x1': points[i][0], 'y1': points[i][1],
                                       'x2': points[i + 1][0], 'y2': points[i + 1][1]})

        self.objectsToDraw.append({'object_type': 'line', 'color': color,
                                   'x1': points[0][0], 'y1': points[0][1],
                                   'x2': points[-1][0], 'y2': points[-1][1]})

    def clearAll(self):
        self.objectsToDraw = []

        self.repaint()
