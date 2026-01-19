import datetime
from mailbox import mbox
from traceback import print_tb

from PyQt6.QtGui import QIcon

import reports
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
                dni = "00000000T"
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
        """
        Modulo para guardar al cliente en la tabla de facturas
        :param self:None
        :type self:None
        """
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

    @staticmethod
    def loadTablefac(self=None):
        try:
            records = conexion.Conexion.allInvoices(self = None)
            index = 0

            # es para que el ancho de la celda se ajuste al botón
            header = globals.ui.tablefacv.horizontalHeader()
            header.setSectionResizeMode(3, QtWidgets.QHeaderView.ResizeMode.Fixed)
            globals.ui.tablefacv.setColumnWidth(3, 36)

            for record in records:
                globals.ui.tablefacv.setColumnWidth(3, 34)
                globals.ui.tablefacv.setRowCount(index + 1)
                globals.ui.tablefacv.setItem(index, 0, QtWidgets.QTableWidgetItem(record[0]))
                globals.ui.tablefacv.setItem(index, 1, QtWidgets.QTableWidgetItem(record[1]))
                globals.ui.tablefacv.setItem(index, 2, QtWidgets.QTableWidgetItem(record[2]))
                # aquí se crea un botón en cada fila
                btn_del = QtWidgets.QPushButton()
                btn_del.setIcon(QIcon("./img/basura.png"))
                btn_del.setIconSize(QtCore.QSize(30, 30))
                btn_del.setFixedSize(32, 32)
                btn_del.setStyleSheet("border: none; background-color: transparent")
                btn_del.setProperty("numfac",record[0])
                btn_del.clicked.connect(Invoice.del_Invoice)
                globals.ui.tablefacv.setCellWidget(index, 3, btn_del)
                globals.ui.tablefacv.item(index, 0).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                globals.ui.tablefacv.item(index, 1).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                globals.ui.tablefacv.item(index, 2).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

                index = index + 1
            ## el último record debe cargarse sus datos en los label
            datos = records[0]
            globals.ui.lblnumfac.setText(str(datos[0]))
            globals.ui.txtDniFac.setText(str(datos[1]))
            globals.ui.lblFechafac.setText(str(datos[2]))
        except Exception as error:
            print("error load tablafac", error)




        except Exception as error:
            print("error in loadTablefac", error)

    def loadFactFirs(self = None):
        try:
            globals.ui.txtDniFac.setText("00000000T")
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
            header = globals.ui.tabsales.horizontalHeader()
            header.setSectionResizeMode(5, QtWidgets.QHeaderView.ResizeMode.Fixed)
            globals.ui.tabsales.setColumnWidth(5, 32)
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

            #Columa 1

            globals.ui.tabsales.setItem(row, 1, QtWidgets.QTableWidgetItem(""))


            # Columna 2 (price)
            globals.ui.tabsales.setItem(row, 2, QtWidgets.QTableWidgetItem(""))

            # Columna 3 (cantidad)
            globals.ui.tabsales.setItem(row, 3, QtWidgets.QTableWidgetItem(""))
            globals.ui.tabsales.item(row, 3).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

            # Columna 4 (total)
            globals.ui.tabsales.setItem(row, 4, QtWidgets.QTableWidgetItem(""))

            #colima 5 crea el icono de basura
            btn_del_file = QtWidgets.QPushButton()
            btn_del_file.setIcon(QIcon("./img/basura.png"))
            btn_del_file.setIconSize(QtCore.QSize(32, 32))
            btn_del_file.setFixedSize(32,32)
            btn_del_file.setStyleSheet("border: none; background-color: transparent")
            btn_del_file.setProperty("idpro",globals.ui.tabsales.item(row, 0).text())
            btn_del_file.clicked.connect(Invoice.del_File)
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
                globals.linesales.append(line)
                cantidad = float(value)
                precio_item = globals.ui.tabsales.item(row, 2)
                precio = float(precio_item.text())
                tot = round(precio * cantidad, 2)
                next_row = globals.ui.tabsales.rowCount()
                Invoice.activeSales(self, row=next_row)
                globals.subtotal = round(globals.subtotal + tot,2)
                totaliva = round(globals.subtotal * iva, 2)
                total = round(globals.subtotal + totaliva, 2)
                globals.ui.lblSubtotal.setText(str(globals.subtotal))
                globals.ui.lblIVA.setText(str(totaliva))
                globals.ui.lblTotal.setText(str(total) +  " €")

        except Exception as error:
            print("Error en cellChangedSales:", error)
            globals.ui.tabsales.blockSignals(False)

    @staticmethod
    def saveSales(self = None):
        try:
            #empieza a recorrer la tabla e ir guardando en la bbdd de ventas
            table = globals.ui.tabsales
            rows = table.rowCount()
            cols = table.columnCount()
            fac = globals.ui.lblnumfac.text()
            if conexion.Conexion.existFacSales(fac):
                reports.Reports.ticket(self)

            else:
                for row in range(rows):
                    line = {}
                    for col in range(cols - 1):
                        item = table.item(row, col)
                        if item and item.text() != "":
                            line[col] = item.text()
                        correct = conexion.Conexion.saveSales(line)
                    if correct:
                        mbox = QtWidgets.QMessageBox()
                        mbox.setIcon(QtWidgets.QMessageBox.Icon.Information)
                        mbox.setWindowTitle("Info")
                        mbox.setText("Sales saved printing invoice")
                        mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
                        if mbox.exec() == QtWidgets.QMessageBox.StandardButton.Ok:
                            #aqui llamo al modulo reports y funcion ticket
                            globals.linesales.clear()
        except Exception as error:
            print("Error en cellChangedSales:", error)


    @staticmethod
    def loadTablesales(records):
        header = globals.ui.tabsales.horizontalHeader()
        header.setSectionResizeMode(5, QtWidgets.QHeaderView.ResizeMode.Fixed)
        globals.ui.tabsales.setColumnWidth(5, 32)

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



    @staticmethod
    def del_Invoice():
        try:
            boton = QtWidgets.QApplication.instance().sender()
            numfac = boton.property("numfac")
            if conexion.Conexion.existFacSales(numfac):
                mbox = QtWidgets.QMessageBox()
                mbox.setIcon(QtWidgets.QMessageBox.Icon.Warning)
                mbox.setWindowTitle("Warning")
                mbox.setText("Exist sales. Do not allow delete invoice")
                mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
                if mbox.exec() == QtWidgets.QMessageBox.StandardButton.Ok:
                    mbox.hide()
            else:
                if conexion.Conexion.deleteInvoice(numfac):
                    mbox = QtWidgets.QMessageBox()
                    mbox.setIcon(QtWidgets.QMessageBox.Icon.Information)
                    mbox.setWindowTitle("Information")
                    mbox.setText("Invoice deleted")
                    mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
                    Invoice.loadTablefac()
                    if mbox.exec() == QtWidgets.QMessageBox.StandardButton.Ok:
                        mbox.hide()
        except Exception as error:
            print("Error in del_invoice:", error)



    @staticmethod
    def del_sale():
        try:
            boton = QtWidgets.QApplication.instance().sender()
            numfac = boton.property("numfac")
        except Exception as error:
            print("error in del_sale ", error)


    @staticmethod
    def del_File():
        try:

            boton1 = QtWidgets.QApplication.instance().sender()
            idpro = boton1.property("idpro")


            table = globals.ui.tabsales
       #     for row in range(table.rowCount()):
        except Exception as error:
            print("error in del_File ", error)