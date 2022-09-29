import sys
from PyQt5.Qt import QApplication

from mainlogic import MainLogic


if __name__ == '__main__':
    app = QApplication(sys.argv)

    logic = MainLogic()

    sys.exit(app.exec_())


