import datetime
from mailbox import mbox
from traceback import print_tb

from PyQt6 import QtWidgets, QtCore
from time import sleep
import conexion
import globals
import products
from conexion import Conexion
from globals import linesales, subtotal


class Invoice:

    @staticmethod
    def searchCli(self = None):
        try:

            dni = globals.ui.txtDniFac.text().upper().strip()

            if globals.ui.txtDniFac.text() == "":
                dni = "39512621R"
            globals.ui.txtDniFac.setText(dni)
            record = conexion.Conexion.dataOneCustomer(dni)

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
            globals.ui.lblnumfac.setText("")
            globals.ui.lblFechafac.setText("")
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
                if conexion.Conexion.insertInvoice(dni, data):
                    Invoice.loadTablefac()
                    mbox = QtWidgets.QMessageBox()
                    mbox.setIcon(QtWidgets.QMessageBox.Icon.Information)
                    mbox.setWindowTitle("Invoice")
                    mbox.setText("Invoice saved")
                    mbox.exec()
                    sleep(2)
                    mbox.hide()


            else:
                mbox = QtWidgets.QMessageBox()
                mbox.setIcon(QtWidgets.QMessageBox.Icon.Warning)
                mbox.setWindowTitle("Invoice")
                mbox.setText("Missing data")
                mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
                if mbox.exec() == QtWidgets.QMessageBox.StandardButton.Ok:
                    mbox.hide()

        except:
            print("error in saving invoice")


    def loadTablefac(self = None):
        try:
            records = conexion.Conexion.allInvoices(self = None)

            index = 0
            for record in records:
                globals.ui.tablefacv.setRowCount(index + 1)
                globals.ui.tablefacv.setItem(index, 0, QtWidgets.QTableWidgetItem(record[0]))
                globals.ui.tablefacv.setItem(index, 1, QtWidgets.QTableWidgetItem(record[1]))
                globals.ui.tablefacv.setItem(index, 2, QtWidgets.QTableWidgetItem(record[2]))
                globals.ui.tablefacv.item(index, 0).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                globals.ui.tablefacv.item(index, 1).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                globals.ui.tablefacv.item(index, 2).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                index = index + 1
            # el ultimo record debe cargar en los label
            datos = records[0]
            globals.ui.lblnumfac.setText(str(datos[0]))
            globals.ui.txtDniFac.setText(str(datos[1]))
            globals.ui.lblFechafac.setText(str(datos[2]))



        except Exception as error:
            print("error in loadTablefac", error)

    def loadFactFirs(self = None):
        try:
            globals.ui.txtDniFac.setText("39512621R")
            globals.ui.lblnumfac.setText("")
            globals.ui.lblFechafac.setText("")
            Invoice.searchCli(self = None)
        except Exception as error:
            print("error in loadFacFirs", error)


    def selectinvoice(self):
        try:
            row = globals.ui.tablefacv.selectedItems()
            data = [dato.text() for dato in row]
            globals.ui.lblnumfac.setText(str(data[0]))
            globals.ui.txtDniFac.setText(str(data[1]))
            globals.ui.lblFechafac.setText(str(data[2]))
            Invoice.searchCli(self)
            #Invoice.activeSales(self)
            #Si la factura existe carga los productos en la tabla ventas
            records = []
            records = conexion.Conexion.existFac(data[0])
            if len(records) > 0:
                globals.ui.tabsales.blockSignals(True)


                Invoice.loadTablesales(records)
                globals.ui.tabsales.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers)

                #Desactivar la tabla ventas

            else:
                globals.subtotal = 0.0
                globals.ui.lblSubtotal.setText("")
                globals.ui.lblIVA.setText("")
                globals.ui.lblTotal.setText("")
                globals.ui.tabsales.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.AllEditTriggers)
                globals.ui.tabsales.blockSignals(False)


                Invoice.activeSales(self)


        except Exception as error:
            print("error en selecting invoice ", error)





    @staticmethod
    def activeSales(self, row=None):
        try:
            # Si no se pasa fila, añadimos la primera fila
            if row is None:
                row = 0
                globals.ui.tabsales.setRowCount(1)
            else:
                # Si es fila nueva, aumentamos el rowCount
                if row >= globals.ui.tabsales.rowCount():
                    globals.ui.tabsales.setRowCount(row + 1)
            globals.ui.tabsales.setStyleSheet("""
                                   /* Fila seleccionada */
                                   QTableWidget::item:selected {
                                       background-color: rgb(255, 255, 202);  /* Color pálido amarillo */
                                       color: black;                          /* Color del texto al seleccionar */
                                   }
                                   """)

            # Columna 0 (código)
            globals.ui.tabsales.setItem(row, 0, QtWidgets.QTableWidgetItem(""))
            globals.ui.tabsales.item(row, 0).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

            # Columna 2 (price)
            globals.ui.tabsales.setItem(row, 2, QtWidgets.QTableWidgetItem(""))

            # Columna 3 (cantidad)
            globals.ui.tabsales.setItem(row, 3, QtWidgets.QTableWidgetItem(""))
            globals.ui.tabsales.item(row, 3).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

            # Columna 4 (total)
            globals.ui.tabsales.setItem(row, 4, QtWidgets.QTableWidgetItem(""))

        except Exception as error:
            print("error active sales", error)

    def cellChangedSales(self, item):
        try:
            iva = 0.21
            row = item.row()
            col = item.column()
            if col not in (0, 3):
                return

            value = item.text().strip()
            data = conexion.Conexion.selectProduct(value)
            if value == "":
                return

            globals.ui.tabsales.blockSignals(True)

            # Columna 0 entonces buscar producto y rellenar nombre y precio
            if col == 0:


                if len(data) == 0:
                    mbox = QtWidgets.QMessageBox()
                    mbox.setIcon(QtWidgets.QMessageBox.Icon.Critical)
                    mbox.setWindowTitle("Error")
                    mbox.setText("Product does not exist")
                    mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
                    if mbox.exec() == QtWidgets.QMessageBox.StandardButton.Ok:
                        mbox.hide()
                else:
                    globals.ui.tabsales.setItem(row, 1, QtWidgets.QTableWidgetItem(str(data[0])))
                    globals.ui.tabsales.setItem(row, 2, QtWidgets.QTableWidgetItem(str(data[1])))
                    globals.ui.tabsales.item(row, 2).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

            # Columna 3 → calcular total
            elif col == 3:
                cantidad = float(value)
                precio_item = globals.ui.tabsales.item(row, 2)
                if precio_item:
                    precio = float(precio_item.text())
                    tot = round(precio * cantidad, 2)
                    globals.ui.tabsales.setItem(row, 4, QtWidgets.QTableWidgetItem(str(tot)))
                    globals.ui.tabsales.item(row, 4).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignRight
                                                                        | QtCore.Qt.AlignmentFlag.AlignVCenter)

            globals.ui.tabsales.blockSignals(False)

            # Comprobar si la fila actual está completa y añadir nueva fila
            if all([
                globals.ui.tabsales.item(row, 0) and globals.ui.tabsales.item(row, 0).text().strip(),
                globals.ui.tabsales.item(row, 1) and globals.ui.tabsales.item(row, 1).text().strip(),
                globals.ui.tabsales.item(row, 2) and globals.ui.tabsales.item(row, 2).text().strip(),
                globals.ui.tabsales.item(row, 3) and globals.ui.tabsales.item(row, 3).text().strip(),
                globals.ui.tabsales.item(row, 4) and globals.ui.tabsales.item(row, 4).text().strip()
            ]):
                line = [globals.ui.lblnumfac.text(),globals.ui.tabsales.item(row, 0).text().strip(),
                        globals.ui.tabsales.item(row, 1).text().strip(),
                        globals.ui.tabsales.item(row, 2).text().strip(),
                        globals.ui.tabsales.item(row, 3).text().strip(),
                        globals.ui.tabsales.item(row, 4).text().strip()]
                next_row = globals.ui.tabsales.rowCount()
                Invoice.activeSales(self, row=next_row)
                globals.subtotal = round(globals.subtotal + tot,2)
                totaliva = round(globals.subtotal * iva, 2)
                total = round(globals.subtotal + iva, 2)
                globals.ui.lblSubtotal.setText(str(globals.subtotal))
                globals.ui.lblIVA.setText(str(totaliva))
                globals.ui.lblTotal.setText(str(total) +  " €")




                globals.linesales.append(line)
                print(globals.linesales)



        except Exception as error:
            print("Error en cellChangedSales:", error)
            globals.ui.tabsales.blockSignals(False)


    def saveSales(self):
        try:
            for i, data in enumerate(globals.linesales):
                correct = conexion.Conexion.saveSales(data)
                if i == len(globals.linesales) - 1 and correct:
                    mbox = QtWidgets.QMessageBox()
                    mbox.setIcon(QtWidgets.QMessageBox.Icon.Information)
                    mbox.setWindowTitle("Info")
                    mbox.setText("Sales saved printing invoice")
                    mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
                    if mbox.exec() == QtWidgets.QMessageBox.StandardButton.Ok:
                        print("dsfsdf")
                        globals.linesales.clear()
        except Exception as error:
            print("Error en cellChangedSales:", error)


    @staticmethod
    def loadTablesales(records):

        try:
            subtotal  = 0.00
            index = 0
            for record in records:
                globals.ui.tabsales.setRowCount(index + 1)
                globals.ui.tabsales.setItem(index, 0, QtWidgets.QTableWidgetItem(str(record[2])))
                globals.ui.tabsales.setItem(index, 1, QtWidgets.QTableWidgetItem(str(record[3])))
                globals.ui.tabsales.setItem(index, 2, QtWidgets.QTableWidgetItem(str(record[4])))
                globals.ui.tabsales.setItem(index, 3, QtWidgets.QTableWidgetItem(str(record[5])))
                globals.ui.tabsales.setItem(index, 4, QtWidgets.QTableWidgetItem(str(record[6])))
                subtotal = round(subtotal + float(record[6]), 2)
                index += 1
            globals.ui.lblSubtotal.setText(str(subtotal) + " €")
            iva = round(float(subtotal * 0.21),2)
            globals.ui.lblIVA.setText(str(iva) + " €")
            total = round(float(subtotal + iva), 2)
            globals.ui.lblTotal.setText(str(total) + " €")
        except Exception as error:
            print("error in loadTablesales ", error)