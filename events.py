import sys
import time
from window import *
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