import sys

from PyQt6 import QtWidgets, QtCore, QtGui

class Events:
    @staticmethod
    def messageExit(self = None):
        mbox = QtWidgets.QMessageBox()
        mbox.setIcon(QtWidgets.QMessageBox.Icon.Question)
        mbox.setWindowIcon(QtGui.QIcon("./img/omega.png"))
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