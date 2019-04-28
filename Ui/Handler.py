from Ui.Ui_MainWindow import Ui_MainWindow
from PyQt5 import QtWidgets, QtCore, QtGui
from Controller import Controller


class MainWindow(Ui_MainWindow):
    def __init__(self):
        self.__controller = Controller()
        self.__controller.readFromFile("data.txt")
        self.__hallMap = {}
        self.__currentHall = None

    def onExit(self):
        self.__controller.writeToFile("data.txt")

    def initialize(self, MainWindow):
        self.window = MainWindow
        self.setSlots()
        self.stackedWidget.setCurrentIndex(0)
        for hall in self.__controller.getAllHalls():
            self.__hallMap[hall.getName()] = hall
            item = QtWidgets.QListWidgetItem(hall.getName())
            self.listWidget.addItem(item)

    def setSlots(self):
        self.chooseHallButton.clicked.connect(self.__hallChooseHandler)
        self.listWidget.itemClicked.connect(self.__hallItemClicked)
        self.createHallButton.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(1))
        self.createHallBackButton.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(0))
        self.finalCreateHallButton.clicked.connect(self.__createHallHandler)

    def __createHallHandler(self):
        self.__currentHall = self.__controller.createHall(self.createHallLineEdit.text())
        self.stackedWidget.setCurrentIndex(2)

    def __hallChooseHandler(self):
        if self.__currentHall is not None:
            self.stackedWidget.setCurrentIndex(2)
        else:
            QtWidgets.QMessageBox(QtWidgets.QMessageBox.Critical, "Error", "You must choose a hall", parent=self.window).show()

    def __hallItemClicked(self, item):
        self.__currentHall = self.__hallMap[item.text()]
