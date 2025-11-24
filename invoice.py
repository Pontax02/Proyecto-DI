import datetime

from PyQt6 import QtWidgets


import conexion
import globals
from conexion import Conexion


class Invoice:

    @staticmethod
    def searchCli(self = None):
        try:

            dni = globals.ui.txtDniFac.text().upper().strip()
            #widget.setText(dni)
            if globals.ui.txtDniFac.text() == "":
                dni = "39512621R"
            globals.ui.txtDniFac.setText(dni)
            record = conexion.Conexion.dataOneCustomer(dni)
            print(record)
            if len(record) != 0:
                globals.ui.lblNamefac.setText(record[2] + " " + record[3])
                globals.ui.lblTipofac.setText(record[9])
                globals.ui.lblnumfac_3.setText(record[6] + "   " + record[8] + "   " + record[7])
                globals.ui.lblnumfac_4.setText(record[5])
                if record[10] == "True":
                    globals.ui.lblStatusfac.setText("Active")
                else:
                    globals.ui.lblStatusfac.setText("Inactive")
            else:
                globals.ui.txtDniFac.setText("")
                mbox = QtWidgets.QMessageBox()
                mbox.setIcon(QtWidgets.QMessageBox.Icon.Warning)
                mbox.setWindowTitle("Invoice")
                mbox.setText("Client does not exist")
                mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
                if mbox.exec() == QtWidgets.QMessageBox.StandardButton.Ok:
                    mbox.hide()

                print("client does not exists")
        except Exception as error:
            print("error in altafac", error)


    @staticmethod
    def cleanFac(self = None):
        try:
            globals.ui.txtDniFac.setText("")
            globals.ui.lblNamefac.setText("")
            globals.ui.lblTipofac.setText("")
            globals.ui.lblnumfac_3.setText("")
            globals.ui.lblnumfac_4.setText("")
            globals.ui.lblStatusfac.setText("")
            globals.ui.lblNamefac.setText("")
            globals.ui.lblTipofac.setText("")
            globals.ui.lblnumfac_3.setText("")
            globals.ui.lblnumfac_4.setText("")


        except Exception as error:
            print("error in cleanfac", error)

    @staticmethod
    def saveInvoice(self = None):
        try:
            dni = globals.ui.txtDniFac.text()

            data = datetime.datetime.now().strftime("%d/%m/%Y")
            if dni != "" and data != "":


                print(dni,data)
                if conexion.Conexion.insertInvoice(dni, data):
                    print("invoice saved")
            else:
                mbox = QtWidgets.QMessageBox()
                mbox.setIcon(QtWidgets.QMessageBox.Icon.Warning)
                mbox.setWindowTitle("Invoice")
                mbox.setText("Missing data")

        except:
            print("error in saving invoice")
