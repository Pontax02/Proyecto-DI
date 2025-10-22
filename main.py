from asyncio import Event
from enum import global_str

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
import styles

# Main (decalra el evento)---> Customers(Prepara la parte gráfica(Constriccion de la tabla)) -----> Conexion(oculto del sistema)(todas las acciones sobre la base de datos)    examen   primero creamos el evento y luego lo codificamos
class Main(QtWidgets.QMainWindow):
    def __init__(self):
        super(Main, self).__init__()
        globals.ui = Ui_MainWindow()
        globals.ui.setupUi(self)
        #instance
        globals.vencal = Calendar()
        globals.about = DlgAbout()
        self.setStyleSheet(styles.load_stylesheet())

        #conexion
        varcli = True
        Conexion.db_conexion(self)
        Customers.loadTablecli(varcli)
        Events.resizeTabCustomer(self)


        # Functions in menu bar
        globals.ui.actionExit.triggered.connect(Events.messageExit)
        globals.ui.actionAbout.triggered.connect(Events.messageAbout)


        #functions in line-edit
        globals.ui.txtDnicli.editingFinished.connect(Customers.checkDni)
        globals.ui.txtNomecli.editingFinished.connect(lambda:Customers.capitalizar(globals.ui.txtNomecli.text(),globals.ui.txtNomecli))
        globals.ui.txtApelcli.editingFinished.connect(lambda:Customers.capitalizar(globals.ui.txtApelcli.text(), globals.ui.txtApelcli))
        globals.ui.txtEmailcli.editingFinished.connect(lambda:Customers.checkMail(globals.ui.txtEmailcli.text()))
        globals.ui.txtMobilecli.editingFinished.connect(lambda:Customers.checkMobil(globals.ui.txtMobilecli.text()))

        #functions of chkhistoricocli
        globals.ui.chkHistoricocli.stateChanged.connect(Customers.Historicocli)


        #functions of buttons
        globals.ui.btnFechaltacli.clicked.connect(Events.openCalendar)
        globals.ui.btnDelcli.clicked.connect(Customers.delCliente)
        globals.ui.btnSavecli.clicked.connect(Customers.saveCli)
        globals.ui.btnCleancli.clicked.connect(Customers.cleanCli)
        globals.ui.btnModifcli.clicked.connect(Customers.modifcli)
        globals.ui.btnSearchcli.clicked.connect(Customers.searchCli)

        #Functions Combobox
        Events.loadProv(self)
        globals.ui.cmbProvcli.currentIndexChanged.connect(events.Events.loadMunicli)

        #functions of tables
        globals.ui.tableCustomerlist.clicked.connect(Customers.selectCustomer)



if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = Main()
    window.showMaximized()
    sys.exit(app.exec())