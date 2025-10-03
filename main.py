from asyncio import Event

import customers
import events
import globals
from conexion import Conexion
from customers import *
from dlgAbout import *
from venAux import *
from window import *
from dlgCalendar import *
import sys
from events import *

class Main(QtWidgets.QMainWindow):
    def __init__(self):
        super(Main, self).__init__()
        globals.ui = Ui_MainWindow()
        globals.ui.setupUi(self)
        #instance
        globals.vencal = Calendar()
        globals.about = dlgAbout()

        #conexion
        Conexion.db_conexion(self)
        Customers.loadTablecli(self)
        Events.resizeTabCustomer(self)


        # Functions in menu bar
        globals.ui.actionExit.triggered.connect(Events.messageExit)
        globals.ui.actionAbout.triggered.connect(Events.messageAbout)


        #functions in line-edit
        globals.ui.txtDnicli.editingFinished.connect(Customers.checkDni)
        globals.ui.txtNomecli.editingFinished.connect(lambda:Customers.capitalizar(globals.ui.txtNomecli.text(),globals.ui.txtNomecli))
        globals.ui.txtApelcli.editingFinished.connect(lambda:Customers.capitalizar(globals.ui.txtApelcli.text(), globals.ui.txtApelcli))
        globals.ui.txtEmailcli.editingFinished.connect(lambda: Customers.checkMail(globals.ui.txtEmailcli.text()))
        globals.ui.txtMobilecli.editingFinished.connect(lambda: Customers.checkMobil(globals.ui.txtMobilecli.text()))

        #functions of buttons
        globals.ui.btnFechaltacli.clicked.connect(Events.openCalendar)

        #Functions Combobox
        Events.loadProv(self)
        globals.ui.cmbProvcli.currentIndexChanged.connect(events.Events.loadMunicli)





if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = Main()
    window.showMaximized()
    sys.exit(app.exec())