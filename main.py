from asyncio import Event

import globals
from customers import Customers
from window import *
import sys
from events import *

class Main(QtWidgets.QMainWindow):
    def __init__(self):
        super(Main, self).__init__()
        globals.ui = Ui_MainWindow()
        globals.ui.setupUi(self)

        # Functions in menu bar
        globals.ui.actionExit.triggered.connect(Events.messageExit)


        #functions in line-edit
        globals.ui.txtDnicli.editingFinished.connect(Customers.checkDni)

        #functions of buttons
        globals.ui.btnFechaltacli.clicked.connect(Events.openCalendar)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = Main()
    window.showMaximized()
    sys.exit(app.exec())