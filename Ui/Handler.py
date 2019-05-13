from Ui.Ui_MainWindow import Ui_MainWindow
from PyQt5 import QtWidgets, QtCore, QtGui
from Controller import Controller
from datetime import datetime


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
        self.homeCustomers.clicked.connect(self.__homeClick)
        self.homeEquipment.clicked.connect(self.__homeClick)
        self.homeExercisePlans.clicked.connect(self.__homeClick)
        self.homeGymHalls.clicked.connect(self.__homeClick)
        self.homeSubscribe.clicked.connect(self.__homeClick)
        self.homeTrainers.clicked.connect(self.__homeClick)
        self.customerBack.clicked.connect(self.__back)
        self.equipmentsBack.clicked.connect(self.__back)
        self.exercisePlanBack.clicked.connect(self.__back)
        self.gymHallBack.clicked.connect(self.__back)
        self.subscibeBack.clicked.connect(self.__back)
        self.trainersBack.clicked.connect(self.__back)
        self.customerGrid.itemClicked.connect(self.__customerItemClicked)
        self.deleteCustomerButton.clicked.connect(self.__deleteCustomer)
        self.cancelSubscriptionButton.clicked.connect(self.__cancelSubscribtion)
        self.createCustomerButton.clicked.connect(self.__createCustomer)
        self.updateCustomerButton.clicked.connect(self.__updateCustomer)
        self.subscribeGymHallComboBox.currentIndexChanged.connect(self.__subscribeGymSelectionChanged)
        self.subscribeTrainerComboBox.currentIndexChanged.connect(self.__subscribeTrainerSelectinoChanged)
        self.subcribeButton.clicked.connect(self.__subscribeButtonClicked)
        self.checkAvailabilityButton.clicked.connect(self.__subscribeCheckClicked)
        self.createHallButton.clicked.connect(self.__hallCreateClicked)
        self.updateGymHall.clicked.connect(self.__hallUpdateClicked)
        self.deleteGymHallButton.clicked.connect(self.__hallDeleteClicked)
        self.gymHallGrid.itemClicked.connect(self.__hallGridSelected)
        self.createEquipmentButton.clicked.connect(self.__createEquipment)
        self.updateEquipmentButton.clicked.connect(self.__updateEquipment)

    def __back(self):
        self.stackedWidget.setCurrentWidget(self.homePage)

    def __homeClick(self):
        btn = self.window.sender().text()
        if btn == "Customers":
            self.stackedWidget.setCurrentWidget(self.customerPage)
            self.__customerInitialize()
        elif btn == "Trainers":
            self.stackedWidget.setCurrentWidget(self.trainersPage)
        elif btn == "Gym Halls":
            self.stackedWidget.setCurrentWidget(self.gymHallPage)
            self.__initializeGymHall()
        elif btn == "Equipments":
            self.stackedWidget.setCurrentWidget(self.equipmentsPage)
            self.__initializeEquipments()
        elif btn == "Exercise Plans":
            self.stackedWidget.setCurrentWidget(self.exercisePlanPage)
        elif btn == "Subcribe a customer to a plan":
            self.stackedWidget.setCurrentWidget(self.subscribePage)
            self.__subscribeInitialize()
        else:
            raise Exception(f"{btn}")

    def __customerInitialize(self):
        self.customerGrid.addItems(self.__custDict.keys())

    def __customerItemClicked(self, item):
        customer = self.__custDict[item.text()]
        self.customerNameEdit.setText(customer.getName())
        self.customerEmailEdit.setText(customer.getEmail())
        self.subscriptionsGrid.clear()
        lst = []
        for i in customer.getSubscribtions():
            lst.append(f"{str(i.getId())} - {str(i.getReservationTime())}")
        self.subscriptionsGrid.addItems(lst)
    
    def __deleteCustomer(self):
        cust = self.__custDict[self.customerGrid.selectedItems()[0].text()]
        self.__controller.deleteCustomer(cust)
        self.customerGrid.takeItem(self.customerGrid.row(self.customerGrid.selectedItems()[0]))
        self.customerNameEdit.setText("")
        self.customerEmailEdit.setText("")
        self.subscriptionsGrid.clear()

    def __createCustomer(self):
        cust = self.__controller.createCustomer(self.customerNameEdit.text(), self.customerEmailEdit.text())
        self.__custDict[cust.getName()] = cust
        self.customerGrid.addItem(QtWidgets.QListWidgetItem(cust.getName()))
        self.customerNameEdit.setText("")
        self.customerEmailEdit.setText("")
    
    def __updateCustomer(self):
        cust = self.__custDict[self.customerGrid.selectedItems()[0].text()]
        self.__custDict.pop(cust.getName())
        cust.setName(self.customerNameEdit.text())
        cust.setEmail(self.customerEmailEdit.text())
        self.__custDict[cust.getName()] = cust
        self.customerGrid.selectedItems()[0].setText(cust.getName())

    def __cancelSubscribtion(self):
        cust = self.__custDict[self.customerGrid.selectedItems()[0].text()]
        subid = str()
        subid = self.subscriptionsGrid.selectedItems()[0].text()
        subid = subid[:subid.find("-")]
        for sub in cust.getSubscribtions():
            if sub.getId() == int(subid):
                self.__controller.cancelSubscribtion(cust, sub)
                break
        self.subscriptionsGrid.takeItem(self.subscriptionsGrid.row(self.subscriptionsGrid.selectedItems()[0]))

    def __subscribeInitialize(self):
        self.subscribeCustomerComboBox.clear()
        self.subscribeGymHallComboBox.clear()
        custs = []
        for i in self.__custDict.values():
            custs.append(i.getName())
        self.subscribeCustomerComboBox.addItems(custs)
        halls = []
        for i in self.__hallDict.values():
            halls.append(i.getName())
        self.subscribeGymHallComboBox.addItems(halls)

    def __subscribeGymSelectionChanged(self, something):
        self.subscribeTrainerComboBox.clear()
        hall = self.__hallDict[self.subscribeGymHallComboBox.currentText()]
        trainers = []
        for trainer in hall.getTrainers():
            trainers.append(trainer.getName())
        self.subscribeTrainerComboBox.addItems(trainers)

    def __subscribeTrainerSelectinoChanged(self, something):
        self.subscribeExercisePlanComboBox.clear()
        hall = self.__hallDict[self.subscribeGymHallComboBox.currentText()]
        plans = []
        for trainer in hall.getTrainers():
            if trainer.getName() == self.subscribeTrainerComboBox.currentText():
                for plan in trainer.getAllExcercisePlans():
                    plans.append(str(plan.getId()))
        self.subscribeExercisePlanComboBox.addItems(plans)

    def __subscribeButtonClicked(self):
        cust = self.__custDict[self.subscribeCustomerComboBox.currentText()]
        hall = self.__hallDict[self.subscribeGymHallComboBox.currentText()]
        for trainer in hall.getTrainers():
            if trainer.getName() == self.subscribeTrainerComboBox.currentText():
                for plan in trainer.getAllExcercisePlans():
                    if plan.getId() == int(self.subscribeExercisePlanComboBox.currentText()):
                        self.__controller.subscribeCustomer(cust, plan, str.lower(self.subscribeCustomerComboBox_2.currentText),
                            self.subscribeDailyStart.value(), self.subscribeDailyEnd.value(), datetime.now())

    def __subscribeCheckClicked(self):
        hall = self.__hallDict[self.subscribeGymHallComboBox.currentText()]
        for trainer in hall.getTrainers():
            if trainer.getName() == self.subscribeTrainerComboBox.currentText():
                for plan in trainer.getAllExcercisePlans():
                    if plan.getId() == int(self.subscribeExercisePlanComboBox.currentText()):
                        return self.__controller.checkAvailability(plan, self.subscribeDailyStart, self.subscribeDailyEnd)
        return False

    def __initializeGymHall(self):
        self.gymHallGrid.clear()
        for i in self.__controller.getAllHalls():
            self.gymHallGrid.addItem(i.getName())

    def __hallCreateClicked(self):
        self.__controller.createHall(self.nameGymHallEdit.text())
        self.gymHallGrid.addItem(self.nameGymHallEdit.text())
        self.nameGymHallEdit.setText("")

    def __hallUpdateClicked(self):
        for hall in self.__controller.getAllHalls():
            if hall.getName() == self.gymHallGrid.selectedItems()[0].text():
                hall.setName(self.nameGymHallEdit.text())
                self.gymHallGrid.selectedItems()[0].setText(hall.getName())
                break

    def __hallDeleteClicked(self):
        for hall in self.__controller.getAllHalls():
            if hall.getName() == self.gymHallGrid.selectedItems()[0].text():
                self.__controller.deleteHall(hall)
                self.gymHallGrid.takeItem(self.gymHallGrid.row(self.gymHallGrid.selectedItems()[0]))
                break

    def __hallGridSelected(self):
        self.nameGymHallEdit.setText(self.gymHallGrid.selectedItems()[0].text())

    def __initializeEquipments(self):
        self.equipmentsGymHallComboBox.clear()
        self.equipmentsGrid.clear()
        for i in self.__controller.getAllHalls():
            self.equipmentsGymHallComboBox.addItem(i.getName())
            for j in i.getAllEquipments():
                self.equipmentsGrid.addItem(j.getName())

    def __createEquipment(self):
        hall = self.__hallDict[self.equipmentsGymHallComboBox.currentText()]
        self.__controller.createEquipment(self.nameEquipmentsEdit.text(), hall)
        self.equipmentsGrid.addItem(self.nameEquipmentsEdit.text())
        self.nameGymHallEdit.setText("")

    def __updateEquipment(self):
        pass
        