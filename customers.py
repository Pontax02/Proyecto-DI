import re


from PyQt6.QtWidgets import QMessageBox

import globals
from events import *
from conexion import *
from PyQt6 import QtWidgets, QtCore, QtGui

class Customers:

    @staticmethod
    def checkDni(self=None):
        try:
            #Evita el problema de ejecutar varios finished
            globals.ui.txtDnicli.editingFinished.disconnect(Customers.checkDni)
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
        finally:
            globals.ui.txtDnicli.editingFinished.connect(Customers.checkDni)

    def capitalizar(texto,widget):
        try:
            texto = texto.title()
            widget.setText(texto)
        except Exception as error:
            print("error en capitalizar texto ", error)


    def checkMail(email):
        try:

            patron = r'^[\w\.-]+@[\w\.-]+\.\w+$'
            if re.match(patron, email):
                globals.ui.txtEmailcli.setStyleSheet('background-color: rgb(255, 255, 220);')
            else:
                globals.ui.txtEmailcli.setStyleSheet('background-color:#FFC0CB;')
                globals.ui.txtEmailcli.setText(None)
                globals.ui.txtEmailcli.setPlaceholderText('Invalid Email')
                globals.ui.txtEmailcli.setFocus()
        except Exception as error:
            print("error en validar email ", error)


    def checkMobil(numero):
        patron = r'^[67]\d{8}$'
        if re.match(patron, numero):
            globals.ui.txtMobilecli.setStyleSheet('background-color: rgb(255, 255, 220);')
        else:
            globals.ui.txtMobilecli.setStyleSheet('background-color: #FFC0CB;')
            globals.ui.txtMobilecli.setText(None)
            globals.ui.txtMobilecli.setPlaceholderText('Invalid Mobile')
            globals.ui.txtMobilecli.setFocus()

    def cleanCli(self):
        try:
            formcli = [globals.ui.txtDnicli, globals.ui.txtAltacli, globals.ui.txtApelcli,
                       globals.ui.txtNomecli, globals.ui.txtEmailcli, globals.ui.txtMobilecli,
                       globals.ui.txtDircli]
            for i,dato in enumerate(formcli):
                formcli[i] = dato.setText("")

            Events.loadProv(self)
            globals.ui.cmbMunicli.clear()
            globals.ui.rbtFacemail.setChecked(True)

        except Exception as error:
            print("error in clean ", error)

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
                if str(record[10]) == "True":
                    globals.ui.tableCustomerlist.setItem(index, 6, QtWidgets.QTableWidgetItem(str("Alta")))
                else:
                    globals.ui.tableCustomerlist.setItem(index, 6, QtWidgets.QTableWidgetItem(str("Baja")))
                globals.ui.tableCustomerlist.item(index, 0).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignLeft.AlignVCenter)
                globals.ui.tableCustomerlist.item(index, 1).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignLeft.AlignVCenter)
                globals.ui.tableCustomerlist.item(index, 2).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter.AlignCenter)
                globals.ui.tableCustomerlist.item(index, 3).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter.AlignCenter)
                globals.ui.tableCustomerlist.item(index, 4).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter.AlignCenter)
                globals.ui.tableCustomerlist.item(index, 5).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter.AlignCenter)
                globals.ui.tableCustomerlist.item(index, 6).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter.AlignCenter)
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
            globals.estado = str(record[10]) #Estado del cliente
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

            newcli = [globals.ui.txtDnicli.text(),globals.ui.txtAltacli.text(),globals.ui.txtApelcli.text(),globals.ui.txtNomecli.text(),globals.ui.txtEmailcli.text(),globals.ui.txtMobilecli.text(),globals.ui.txtDircli.text(),globals.ui.cmbProvcli.currentText(),globals.ui.cmbMunicli.currentText()]
            if globals.ui.rbtFacpapel.isChecked():
                fact = "paper"

            elif globals.ui.rbtFacemail.isChecked():
                fact = "electronic"
            newcli.append(fact)
            if Conexion.addCli(newcli) and len(newcli) > 0:
                mbox = QtWidgets.QMessageBox()
                mbox.setWindowTitle("Information")
                mbox.setIcon(QtWidgets.QMessageBox.Icon.Information)
                mbox.setText("Client added")
                mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Yes)

                if mbox.exec():
                    mbox.hide()
            else:
                mbox = QtWidgets.QMessageBox()
                mbox.setWindowTitle("Warning")
                mbox.setIcon(QtWidgets.QMessageBox.Icon.Warning)
                mbox.setText("Warning, no Client added")
                mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Yes)

                if mbox.exec():
                    mbox.hide()
            varcli = True
            Customers.loadTablecli(varcli)
        except Exception as error:
            print("Error  saving customer ", error)


    def modifcli(self):
        try:
            varcli = "True"
            print(globals.estado)
            if globals.estado == str("False"):
                mbox = QtWidgets.QMessageBox()
                mbox.setWindowTitle("Information")
                mbox.setIcon(QtWidgets.QMessageBox.Icon.Information)
                mbox.setText("Client non activated. DO you want activated?")
                mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No)
                if mbox.exec():
                    globals.estado = str("True")

            mbox = QtWidgets.QMessageBox()
            mbox.setWindowTitle("Modify")
            mbox.setIcon(QtWidgets.QMessageBox.Icon.Question)
            mbox.setText("Modify Client?")
            mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No)
            mbox.setDefaultButton(QtWidgets.QMessageBox.StandardButton.No)
            if mbox.exec():
                dni = globals.ui.txtDnicli.text()
                modifcli = [globals.ui.txtAltacli.text(), globals.ui.txtApelcli.text(),
                          globals.ui.txtNomecli.text(), globals.ui.txtEmailcli.text(), globals.ui.txtMobilecli.text(),
                          globals.ui.txtDircli.text(), globals.ui.cmbProvcli.currentText(),
                          globals.ui.cmbMunicli.currentText(),globals.estado]
                if globals.ui.rbtFacpapel.isChecked():
                    fact = "paper"
                elif globals.ui.rbtFacemail.isChecked():
                    fact = "electronic"
                modifcli.append(fact)
                if Conexion.modifyCli(dni, modifcli):
                    mbox = QtWidgets.QMessageBox()
                    mbox.setWindowTitle("Information")
                    mbox.setIcon(QtWidgets.QMessageBox.Icon.Information)
                    mbox.setText("Client modified")
                    mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
                    if mbox.exec():
                        mbox.hide()
                else:
                    mbox = QtWidgets.QMessageBox()
                    mbox.setWindowTitle("Warning")
                    mbox.setIcon(QtWidgets.QMessageBox.Icon.Warning)
                    mbox.setText("Warning, no Client modified")
                    if mbox.exec():
                        mbox.hide()




            else:
                mbox.hide()

            Customers.loadTablecli(varcli)
        except Exception as error:
            print("error en modifing customer ", error)


    def searchCli(self):
        try:
            record = []
            dni = globals.ui.txtDnicli.text()
            if record == Conexion.dataOneCustomer(str(dni)):
                if not record:
                    mbox = QtWidgets.QMessageBox()
                    mbox.setWindowTitle("Information")
                    mbox.setIcon(QtWidgets.QMessageBox.Icon.Information)
                    mbox.setText("Client not exists")
                    mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
                    if mbox.exec():
                        mbox.hide()
                else:
                    box = [globals.ui.txtDnicli,globals.ui.txtAltacli,globals.ui.txtApelcli,globals.ui.txtNomecli,globals.ui.txtEmailcli,globals.ui.txtMobilecli,globals.ui.txtDircli]
                    for i in range(len(box)):
                        box[i].setText(record[i])

                    globals.ui.cmbProvcli.setCurrentText(str(record[7]))
                    globals.ui.cmbMunicli.setCurrentText(str(record[8]))
                    if str(record[9]) == 'paper':
                        globals.ui.rbtFacpapel.setChecked(True)
                    else:
                        globals.ui.rbtFacemail.setChecked(True)

        except:
            print("error en searching customer ", globals.estado)
