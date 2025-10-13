import re

from PyQt6.QtWidgets import QMessageBox

import globals

from conexion import *
from PyQt6 import QtWidgets, QtCore, QtGui

class Customers:

    @staticmethod
    def checkDni(self=None):
        try:
            dni = globals.ui.txtDnicli.text()
            dni = str(dni).upper()
            globals.ui.txtDnicli.setText(dni)
            tabla = "TRWAGMYFPDXBNJZSQVHLCKE"
            dig_ext = "XYZ"
            reemp_dig_ext = {'X': '0', 'Y': '1', 'Z': '2'}
            numeros = "1234567890"
            if len(dni) == 9:
                dig_control = dni[8]
                dni = dni[:8]
                if dni[0] in dig_ext:
                    dni = dni.replace(dni[0], reemp_dig_ext[dni[0]])
                if len(dni) == len([n for n in dni if n in numeros]) and tabla[int(dni) % 23] == dig_control:
                    globals.ui.txtDnicli.setStyleSheet('background-color: rgb(255, 255, 220);')
                else:
                    globals.ui.txtDnicli.setStyleSheet('background-color:#FFC0CB;')
                    globals.ui.txtDnicli.setText(None)
                    globals.ui.txtDnicli.setFocus()
            else:
                globals.ui.txtDnicli.setStyleSheet('background-color:#FFC0CB;')
                globals.ui.txtDnicli.setText(None)
                globals.ui.txtDnicli.setFocus()
        except Exception as error:
            print("error en validar dni ", error)


    def capitalizar(texto,widget):
        try:
            texto = texto.title()
            widget.setText(texto)
        except Exception as error:
            print("error en capitalizar texto ", error)


    def checkMail(email):

        patron = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        if re.match(patron, email):
            globals.ui.txtEmailcli.setStyleSheet('background-color: rgb(255, 255, 220);')
        else:
            globals.ui.txtEmailcli.setStyleSheet('background-color:#FFC0CB;')
            globals.ui.txtEmailcli.setText(None)
            globals.ui.txtEmailcli.setPlaceholderText('Invalid Email')
            globals.ui.txtEmailcli.setFocus()


    def checkMobil(numero):
        patron = r'^[67]\d{8}$'
        if re.match(patron, numero):
            globals.ui.txtMobilecli.setStyleSheet('background-color: rgb(255, 255, 220);')
        else:
            globals.ui.txtMobilecli.setStyleSheet('background-color: #FFC0CB;')
            globals.ui.txtMobilecli.setText(None)
            globals.ui.txtMobilecli.setPlaceholderText('Invalid Mobile')
            globals.ui.txtMobilecli.setFocus()
    @staticmethod
    def loadTablecli(varcli):
        try:
            listTabCustomers = Conexion.listTabCustomers(varcli)
            index = 0
            for record in listTabCustomers:
                globals.ui.tableCustomerlist.setRowCount(index + 1)
                globals.ui.tableCustomerlist.setItem(index, 0, QtWidgets.QTableWidgetItem(str(record[2])))
                globals.ui.tableCustomerlist.setItem(index, 1, QtWidgets.QTableWidgetItem(str(record[3])))
                globals.ui.tableCustomerlist.setItem(index, 2, QtWidgets.QTableWidgetItem(str("  " + str(record[5]) + "  ")))
                globals.ui.tableCustomerlist.setItem(index, 3, QtWidgets.QTableWidgetItem(str(record[7])))
                globals.ui.tableCustomerlist.setItem(index, 4, QtWidgets.QTableWidgetItem(str(record[8])))
                globals.ui.tableCustomerlist.setItem(index, 5, QtWidgets.QTableWidgetItem(str(record[9])))
                globals.ui.tableCustomerlist.item(index, 0).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignLeft.AlignVCenter)
                globals.ui.tableCustomerlist.item(index, 1).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignLeft.AlignVCenter)
                globals.ui.tableCustomerlist.item(index, 2).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter.AlignCenter)
                globals.ui.tableCustomerlist.item(index, 3).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter.AlignCenter)
                globals.ui.tableCustomerlist.item(index, 4).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter.AlignCenter)
                globals.ui.tableCustomerlist.item(index, 5).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter.AlignCenter)
                index += 1
        except Exception as error:
            print("error en loadTablecli ", error)
    @staticmethod
    def Historicocli(self):
        try:
            if globals.ui.chkHistoricocli.isChecked():
                varcli = False
            else:
                varcli = True
            Customers.loadTablecli(varcli)
        except Exception as error:
            print("error en historicocli ", error)

    def selectCustomer(self):
        try:
            row = globals.ui.tableCustomerlist.selectedItems()
            data = [dato.text() for dato in row]
            record = Conexion.dataOneCustomer(str(data[2]))
            boxes = [globals.ui.txtDnicli,globals.ui.txtAltacli,globals.ui.txtApelcli,globals.ui.txtNomecli,globals.ui.txtEmailcli,globals.ui.txtMobilecli,globals.ui.txtDircli]
            for i in range(len(boxes)):
                boxes[i].setText(record[i])

            globals.ui.cmbProvcli.setCurrentText(str(record[7]))
            globals.ui.cmbMunicli.setCurrentText(str(record[8]))
            if str(record[9]) == 'paper':
                globals.ui.rbtFacpapel.setChecked(True)
            else:
                globals.ui.rbtFacemail.setChecked(True)
        except Exception as error:
            print("error en selecting customer ", error)


    def delCliente(self):
        try:
            mbox = QtWidgets.QMessageBox()
            mbox.setWindowTitle("WARNING")
            mbox.setIcon(QtWidgets.QMessageBox.Icon.Warning)
            mbox.setText("Delete Client?")
            mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No)
            mbox.setDefaultButton(QtWidgets.QMessageBox.StandardButton.No)
            if mbox.exec():

                dni = globals.ui.txtDnicli.text()
                if Conexion.deleteCli(dni):

                    mbox = QtWidgets.QMessageBox()
                    mbox.setWindowTitle("Information")
                    mbox.setIcon(QtWidgets.QMessageBox.Icon.Information)
                    mbox.setText("Delete Client?")
                    mbox.standardButton(QtWidgets.QMessageBox.StandardButton.Yes)

                else:
                    print("Something went wrong")
                Customers.loadTablecli(self)
            else:
                print("mensaje con msbox")

        except Exception as error:
            print("error en deleting customer ", error)
            
    def saveCli(self):
        try:

            newcli = [globals.ui.txtDnicli,globals.ui.txtAltacli,globals.ui.txtApelcli,globals.ui.txtNomecli,globals.ui.txtEmailcli,globals.ui.txtMobilecli,globals.ui.txtDircli,globals.ui.cmbProvcli.currentText(),globals.ui.cmbMunicli.currentText(),globals.ui.rbtFacpapel.isChecked()]
            if globals.ui.rbtFacpapel.isChecked():
                fact = "paper"

            elif globals.ui.rbtFacemail.isChecked():
                fact = "electronic"
            newcli.append(fact)
            if Conexion.addCli(newcli):
                mbox = QtWidgets.QMessageBox()
                mbox.setWindowTitle("Information")
                mbox.setIcon(QtWidgets.QMessageBox.Icon.Information)
                mbox.setText("Client added")
                mbox.standardButton(QtWidgets.QMessageBox.StandardButton.Yes)

            else:
                mbox = QtWidgets.QMessageBox()
                mbox.setWindowTitle("Warning")
                mbox.setIcon(QtWidgets.QMessageBox.Icon.Warning)
                mbox.setText("Warning, no Client added")
                mbox.standardButton(QtWidgets.QMessageBox.StandardButton.Yes)

            varcli = True
            Customers.loadTablecli(varcli)
        except Exception as error:
            print("Error  saving customer ", error)
