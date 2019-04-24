from Ui.Ui_MainWindow import Ui_MainWindow

class MainWindow(Ui_MainWindow):
    def setUpSlots(self):
        self.pushButton.clicked.connect(self.clickHandler)
    def clickHandler(self):
        print("Test")