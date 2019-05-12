from Ui.Ui_MainWindow import Ui_MainWindow
from PyQt5 import QtWidgets, QtCore, QtGui
from Controller import Controller


class MainWindow(Ui_MainWindow):
    def __init__(self):
        self.__controller = Controller()
        self.__custDict = {}
        self.__hallDict = {}
        self.__chosenHall = None
        self.__chosenCustomer = None
        for customer in self.__controller.getAllCustomers():
            self.__custDict[f"{str(customer.getId())} - {customer.getName()}"] = customer
        for hall in self.__controller.getAllHalls():
            self.__hallDict[f"{str(hall.getId())} - {hall.getName()}"] = hall

    def onExit(self):
        pass

    def initialize(self, MainWindow):
        self.window = MainWindow
        self.setSlots()
        self.stackedWidget.setCurrentIndex(0)
        for cust in self.__custDict.keys():
            self.gymHallGrid.addItem(cust)
        for hall in self.__hallDict.keys():
            self.customerGrid.addItem(hall)

    def setSlots(self):
        self.gymHallGrid.itemClicked.connect(self.__hallChosen)
        self.customerGrid.itemClicked.connect(self.__customerChosen)

    def __hallChosen(self, item):
        self.__chosenHall = self.__hallDict[item.text()]

    def __customerChosen(self, item):
        self.__chosenCustomer = self.__custDict[item.text()]
