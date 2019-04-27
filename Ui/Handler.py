from Ui.Ui_MainWindow import Ui_MainWindow
from PyQt5 import QtWidgets, QtCore
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
        halls = []  # self.controller.getAllHalls()
        for i in range(1, 5):
            halls.append(str(i))
        for hall in halls:
            item = QtWidgets.QListWidgetItem(hall)
            item.setTextAlignment(QtCore.Qt.AlignCenter)
            self.listWidget.addItem(item)
            # self.verticalLayout_2.addWidget(button)

    def setSlots(self):
        self.chooseHallButton.clicked.connect(self.__hallChooseHandler)
        self.listWidget.itemClicked.connect(self.__hallItemClicked)
        self.createHallButton.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(1))
        self.createHallBackButton.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(0))
        self.finalCreateHallButton.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(2))

    def __hallChooseHandler(self):
        #if self.__currentHall is not None:
            self.stackedWidget.setCurrentIndex(2)

    def __hallItemClicked(self, item):
        #self.__currentHall = self.__hallMap[item.text()]
        pass
