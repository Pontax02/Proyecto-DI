import csv
import os
import shutil
import sys
import time
from fileinput import filename
from logging import exception

import events
from window import *
import zipfile
from venAux import *
import conexion
import globals
from PyQt6 import QtWidgets, QtCore, QtGui

class Events:
    @staticmethod
    def messageExit(self = None):
        try:
            mbox = QtWidgets.QMessageBox()
            mbox.setIcon(QtWidgets.QMessageBox.Icon.Question)
            mbox.setWindowIcon(QtGui.QIcon("img/omega.ico"))
            mbox.setWindowTitle("Exit")
            mbox.setText("Are you sure you want to exit?")
            mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No)
            mbox.setDefaultButton(QtWidgets.QMessageBox.StandardButton.No)
            #mbox.button(QtWidgets.QMessageBox.StandardButton.Yes)
            #mbox.button(QtWidgets.QMessageBox.StandardButton.No)
            mbox.resize(600,800)
            if mbox.exec() == QtWidgets.QMessageBox.StandardButton.Yes:
                sys.exit()
            else:
                mbox.hide()
        except Exception as e:
            print("error",e)


    def openCalendar (self = None) :
        try:
            globals.vencal.show()


        except Exception as e:
            print("error calendar",e)


    def loadData(qDate):
        try:
            data = ('{:02d}/{:02d}/{:4d}'.format(qDate.day(), qDate.month(), qDate.year()))
            if globals.ui.PanMain.currentIndex() == 0:
                globals.ui.txtAltacli.setText(data)
            time.sleep(0.3)
            globals.vencal.hide()

        except Exception as e:
            print("error loading Data", e)


    def loadProv(self):
        try:
            globals.ui.cmbProvcli.clear()
            list = conexion.Conexion.listProv(self)
            #listado = conexionserver.ConexionServer.listaProv(self)
            globals.ui.cmbProvcli.addItems(list)
        except Exception as e:
            print("error loading Prov", e)


    def loadMunicli(self):
        try:
            province = globals.ui.cmbProvcli.currentText()
            list = conexion.Conexion.listMuniProv(province)
            globals.ui.cmbMunicli.clear()
            globals.ui.cmbMunicli.addItems(list)
        except Exception as e:
            print("error loading MuniProv", e)



    def resizeTabCustomer(self):
        try:
            header = globals.ui.tableCustomerlist.horizontalHeader()
            for i in range(header.count()):
                if i == 3:
                    header.setSectionResizeMode(i, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
                else:
                    header.setSectionResizeMode(i, QtWidgets.QHeaderView.ResizeMode.Stretch)
                header_items = globals.ui.tableCustomerlist.horizontalHeaderItem(i)
                #negrita cabecera
                font = header_items.font()
                font.setBold(True)
                header_items.setFont(font)

        except Exception as e:
            print("error resizing table cients: ", e)


    def resizeTabProducts(self):
        try:
            header = globals.ui.tblProducts.horizontalHeader()
            for i in range(header.count()):
                if i == 3:
                    header.setSectionResizeMode(i, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
                else:
                    header.setSectionResizeMode(i, QtWidgets.QHeaderView.ResizeMode.Stretch)
                header_items = globals.ui.tblProducts.horizontalHeaderItem(i)
                #negrita cabecera
                font = header_items.font()
                font.setBold(True)
                header_items.setFont(font)

        except Exception as e:
            print("error resizing table products: ", e)

    def resizeTabSales(self):
        try:
            header = globals.ui.tabsales.horizontalHeader()
            for i in range(header.count()):
                if i == 0:
                    header.setSectionResizeMode(i, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
                else:
                    header.setSectionResizeMode(i, QtWidgets.QHeaderView.ResizeMode.Stretch)
                header_items = globals.ui.tabsales.horizontalHeaderItem(i)
                #negrita cabecera
                font = header_items.font()
                font.setBold(True)
                header_items.setFont(font)


        except Exception as e:
            print("error resizing table products: ", e)

    def messageAbout(self):
        try:
            globals.about.show()
        except Exception as e:
            print("error in open about", e)

    def closeabout(self):
        try:
            globals.about.hide()
        except Exception as e:
            print("error in close about", e)


    def saveBackup(self):
        try:
            data = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
            filename = str(data) + "_backup.zip"
            directory, file = globals.dlgopen.getSaveFileName(None, "Save Backup file", filename, "zip")

            if globals.dlgopen.accept and file:
                print(directory)
                filezip = zipfile.ZipFile(file, "w")
                filezip.write("./data/bbdd.sqlite", os.path.basename("bbdd.sqlite") ,zipfile.ZIP_DEFLATED)
                filezip.close()
                shutil.move(file, directory)
                mbox = QtWidgets.QMessageBox()
                mbox.setIcon(QtWidgets.QMessageBox.Icon.Information)
                mbox.setWindowIcon(QtGui.QIcon("img/omega.ico"))
                mbox.setWindowTitle("Save Backup")
                mbox.setText("Save Backup Done")
                mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
                mbox.exec()

        except Exception as e:
            print("error in save backup", e)



    def restoreBackup(self):
        try:
            filename = globals.dlgopen.getOpenFileName(None, "Restore Backup file", "","*.zip;;All Files(*)")
            file = filename[0]
            if file:
                with zipfile.ZipFile(file, "r") as bbdd:
                    bbdd.extractall(path = "./data",pwd= None)
                bbdd.close()
                mbox = QtWidgets.QMessageBox()
                mbox.setIcon(QtWidgets.QMessageBox.Icon.Information)
                mbox.setWindowIcon(QtGui.QIcon("img/omega.ico"))
                mbox.setWindowTitle("Restore Backup")
                mbox.setText("Restore Backup Done")
                mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
                mbox.exec()
                conexion.Conexion.db_conexion(self)
                events.Events.loadProv(self)
                customers.Customers.loadTablecli(self)



        except Exception as e:
            print("error in restore backup", e)


    def exportXlsCustomers(self):
        try:
            data = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
            filenam = str(data) + "_customers.csv"
            directory, file = globals.dlgopen.getSaveFileName(None, "Save Customers", filenam, ".csv")
            globals = False
            if file:
                records = conexion.Conexion.listTabCustomers(globals)
                with open(filenam, "w", newline="", encoding="utf-8") as csvfile:
                    writer = csv.writer(csvfile)
                    writer.writerow(["DNI_NIE", "AddData","Surname","Name","eMail","Mobile","Address","Province","City","InvoiceType","Active"])
                    for record in records:
                        writer.writerow(record)
                shutil.move(filenam, directory)

                mbox = QtWidgets.QMessageBox()
                mbox.setIcon(QtWidgets.QMessageBox.Icon.Information)
                mbox.setWindowIcon(QtGui.QIcon("img/omega.ico"))
                mbox.setWindowTitle("Export Customers")
                mbox.setText("Export Customers Done")
                mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
                mbox.exec()

            else:
                mbox = QtWidgets.QMessageBox()
                mbox.setIcon(QtWidgets.QMessageBox.Icon.Warning)
                mbox.setWindowIcon(QtGui.QIcon("img/omega.ico"))
                mbox.setWindowTitle("Export Customers")
                mbox.setText("Export Customers Error")
                mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
                mbox.exec()
        except Exception as e:
            print("error in exportXlsCustomers" ,e )
    def loadStatusbar(self):
        try:
            data = datetime.now().strftime("%d/%m/%Y")
            self.labelStatus = QtWidgets.QLabel(self)
            self.labelStatus.setText("Date: " + data + " - " + "Version 0.0.1")
            self.labelStatus.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            self.labelStatus.setStyleSheet("color: white; font-weight: bold; font-size: 15px;")
            globals.ui.statusbar.addPermanentWidget(self.labelStatus,1)

        except Exception as e:
            print("error in loadStatusbar", e)

    """
    def nextCli(self):
        '''

        :return: None
        :rtype: None
        Permite navegar entre la tabla de datos Clientes de 5 en 5


        '''
        
        try:
            if globals.ui.panPrincipal.currentIndex() == 0:
                if (globals.paginacli + 1) * globals.clientesxpagina < globals.longcli:
                    globals.paginacli += 1
                    customers.Customers.cargaTablaClientes(self)
                    if (globals.paginacli + 1) * globals.clientesxpagina >= globals.longcli:
                        globals.ui.btnNextCli.setStyleSheet("background-color: #A9C0D6;")
                        globals.ui.btnPrevCli.setStyleSheet("background-color:  #4682B4;")
                    else:
                        globals.ui.btnNextCli.setStyleSheet("background-color: #4682B4;;")
                        globals.ui.btnPrevCli.setStyleSheet("background-color: #4682B4;")
            if globals.ui.panPrincipal.currentIndex() == 1:
                if (globals.paginaprop + 1) * globals.propiedadesxpagina < globals.longprop:
                    # globals.ui.btnNextCli.setEnable(True)
                    globals.paginaprop += 1
                    propiedades.Propiedades.cargaTablaPropiedades(self)
                    if (globals.paginaprop + 1) * globals.propiedadesxpagina >= globals.longprop:
                        globals.ui.btnNextCli.setStyleSheet("background-color: #A9C0D6;")
                        globals.ui.btnPrevCli.setStyleSheet("background-color:  #4682B4;")
                    else:
                        globals.ui.btnNextCli.setStyleSheet("background-color: #4682B4;;")
                        globals.ui.btnPrevCli.setStyleSheet("background-color: #4682B4;")
        except Exception as e:
            print("error next boton", e)
            """
"""
    def prevCli(self):
        '''

        :return:None
        :rtype: None
        Permite retroceder de 5 en 5 el listado de clientes

        '''
        try:
            if globals.ui.panPrincipal.currentIndex() == 0:
                if globals.paginacli > 0:
                    globals.paginacli -= 1
                    clientes.Clientes.cargaTablaClientes(self)
                    # globals.ui.btnPrevCli.setEnabled(True)
                    if globals.paginacli <= 0:
                        globals.ui.btnPrevCli.setStyleSheet("background-color: #A9C0D6;")
                        globals.ui.btnNextCli.setStyleSheet("background-color: #4682B4;")
                    else:
                        globals.ui.btnNextCli.setStyleSheet("background-color:  #4682B4;")
                        globals.ui.btnPrevCli.setStyleSheet("background-color:  #4682B4;")
            if globals.ui.panPrincipal.currentIndex() == 1:
                if globals.paginaprop > 0:
                    # globals.ui.btnPrevCli.setDisable(False)
                    globals.paginaprop -= 1
                    propiedades.Propiedades.cargaTablaPropiedades(self)
                    if globals.paginaprop <= 0:
                        globals.ui.btnPrevCli.setStyleSheet("background-color: #A9C0D6;")
                        globals.ui.btnNextCli.setStyleSheet("background-color: #4682B4;")
                    else:
                        globals.ui.btnNextCli.setStyleSheet("background-color:  #4682B4;")
                        globals.ui.btnPrevCli.setStyleSheet("background-color:  #4682B4;")
        except Exception as e:
            print("error prev boton", e)
"""