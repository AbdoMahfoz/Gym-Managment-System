from PyQt5 import QtWidgets
from Ui.Handler import MainWindow
import sys

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    Window = QtWidgets.QMainWindow()
    ui = MainWindow()
    ui.setupUi(Window)
    ui.initialize(Window)
    Window.show()
    app.exec_()
    ui.onExit()