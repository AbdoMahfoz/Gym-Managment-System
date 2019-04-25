from Ui.Ui_MainWindow import Ui_MainWindow

class MainWindow(Ui_MainWindow):
    def initialize(self):
        self.pushButton.setText("Say Hello")
        self.pushButton.clicked.connect(self.sayHello)
    def sayHello(self):
        print("Hello :D")