import csv
import os
import shutil
import sys
import time
from fileinput import filename
from logging import exception
import customers
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
            print("error calendario",e)


    def loadData(qDate):
        try:
            data = ('{:02d}/{:02d}/{:4d}'.format(qDate.day(), qDate.month(), qDate.year()))
            if globals.ui.PanMain.currentIndex() == 0:
                globals.ui.txtAltacli.setText(data)
            time.sleep(0.3)
            globals.vencal.hide()

        except Exception as e:
            print("error en cargar Data", e)


    def loadProv(self):
        try:
            globals.ui.cmbProvcli.clear()
            list = conexion.Conexion.listProv(self)
            #listado = conexionserver.ConexionServer.listaProv(self)
            globals.ui.cmbProvcli.addItems(list)
        except Exception as e:
            print("error en cargar Prov", e)


    def loadMunicli(self):
        try:
            province = globals.ui.cmbProvcli.currentText()
            list = conexion.Conexion.listMuniProv(province)
            globals.ui.cmbMunicli.clear()
            globals.ui.cmbMunicli.addItems(list)
        except Exception as e:
            print("error en cargar MuniProv", e)



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
            print("error en resize tabla lcients: ", e)

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
            var = False
            if file:
                records = conexion.Conexion.listTabCustomers(var)
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
