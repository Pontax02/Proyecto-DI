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


                Invoice.activeSales()


        except Exception as error:
            print("error en selecting invoice ", error)

    @staticmethod
    def activeSales(row=None):
        """
        Activa una fila editable en la tabla de ventas para
        introducir una nueva línea de venta.

        :param row: Índice de la fila a activar
        """
        try:
            fact = globals.ui.lblnumfac.text()

            if Conexion.existFacSales(fact):
                return

            table = globals.ui.tabsales
            if row is None:
                row = table.rowCount()

            if row >= globals.ui.tabsales.rowCount():
                globals.ui.tabsales.setRowCount(row + 1)

            center_align = QtCore.Qt.AlignmentFlag.AlignCenter

            # Código de producto
            item_code = QtWidgets.QTableWidgetItem("")
            item_code.setTextAlignment(center_align)
            globals.ui.tabsales.setItem(row, 0, item_code)

            # Concepto
            globals.ui.tabsales.setItem(row, 1, QtWidgets.QTableWidgetItem(""))

            # Precio
            item_price = QtWidgets.QTableWidgetItem("")
            item_price.setTextAlignment(center_align)
            globals.ui.tabsales.setItem(row, 2, item_price)

            # Cantidad
            item_qty = QtWidgets.QTableWidgetItem("")
            item_qty.setTextAlignment(center_align)
            globals.ui.tabsales.setItem(row, 3, item_qty)

            # Total
            item_total = QtWidgets.QTableWidgetItem("")
            item_total.setTextAlignment(
                QtCore.Qt.AlignmentFlag.AlignRight |
                QtCore.Qt.AlignmentFlag.AlignVCenter
            )
            globals.ui.tabsales.setItem(row, 4, item_total)

            # Eliminar
            btn_del = QtWidgets.QPushButton()
            btn_del.setIcon(QIcon("./img/basura.png"))
            btn_del.setIconSize(QtCore.QSize(26, 26))
            btn_del.setFixedSize(32, 32)
            btn_del.setStyleSheet("border: none; background-color: transparent")
            btn_del.clicked.connect(Invoice.deleteSales)
            globals.ui.tabsales.setCellWidget(row, 5, btn_del)

        except Exception as error:
            print("error en activeSales", error)

    @staticmethod
    def cellChangedSales(item):
        """
        Gestiona los cambios realizados en las celdas de la tabla de ventas.

        - Detecta cambios en el código de producto y cantidad
        - Calcula automáticamente el total por línea
        - Actualiza subtotal, IVA y total de la factura
        - Añade una nueva fila cuando la actual está completa
        - Guarda la línea de venta en ``globals.linesales``

        :param item: Celda modificada en la tabla de ventas
        :type item: QTableWidgetItem
        """
        try:
            if item is None:
                return

            row = item.row()
            col = item.column()

            # Solo reaccionar a cambios en código o cantidad
            if col not in (0, 3):
                return

            # Evitar bucles infinitos al modificar celdas desde código
            globals.ui.tabsales.blockSignals(True)

            value = item.text().strip()

            # Cambio en código de producto
            if col == 0:
                if value == "":
                    globals.ui.tabsales.setItem(row, 1, QtWidgets.QTableWidgetItem(""))
                    globals.ui.tabsales.setItem(row, 2, QtWidgets.QTableWidgetItem(""))
                else:
                    data = Conexion.selectProduct(value)
                    if data:
                        globals.ui.tabsales.setItem(
                            row, 1, QtWidgets.QTableWidgetItem(str(data[0]))
                        )
                        globals.ui.tabsales.setItem(
                            row, 2, QtWidgets.QTableWidgetItem(str(data[1]))
                        )
                        globals.ui.tabsales.item(
                            row, 2
                        ).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                    else:
                        mbox = QtWidgets.QMessageBox()
                        mbox.setIcon(QtWidgets.QMessageBox.Icon.Warning)
                        mbox.setWindowTitle("Warning")
                        mbox.setText("Product not exists")
                        mbox.setStandardButtons(
                            QtWidgets.QMessageBox.StandardButton.Ok
                        )
                        if mbox.exec() == QtWidgets.QMessageBox.StandardButton.Ok:
                            mbox.hide()
                        globals.ui.tabsales.setItem(
                            row, 0, QtWidgets.QTableWidgetItem("")
                        )

            # Cálculo del total por línea
            if col in (0, 3):
                item_qty = globals.ui.tabsales.item(row, 3)
                item_price = globals.ui.tabsales.item(row, 2)

                if item_qty and item_price:
                    try:
                        cantidad = float(item_qty.text())
                        precio = float(item_price.text())
                        tot = round(precio * cantidad, 2)

                        globals.ui.tabsales.setItem(
                            row, 4, QtWidgets.QTableWidgetItem(str(tot))
                        )
                        globals.ui.tabsales.item(
                            row, 4
                        ).setTextAlignment(
                            QtCore.Qt.AlignmentFlag.AlignRight |
                            QtCore.Qt.AlignmentFlag.AlignVCenter
                        )
                    except ValueError:
                        globals.ui.tabsales.setItem(
                            row, 4, QtWidgets.QTableWidgetItem("0.00")
                        )

            # Cálculo del subtotal general
            grand_subtotal = 0.0
            for r in range(globals.ui.tabsales.rowCount()):
                item_total = globals.ui.tabsales.item(r, 4)
                if item_total and item_total.text():
                    try:
                        grand_subtotal += float(item_total.text())
                    except ValueError:
                        pass

            globals.subtotal = grand_subtotal

            # Cálculo de IVA y total final
            iva = 0.21
            totaliva = round(globals.subtotal * iva, 2)
            total = round(globals.subtotal + totaliva, 2)

            globals.ui.lblSubtotal.setText(f"{globals.subtotal:.2f} €")
            globals.ui.lblIVA.setText(f"{totaliva:.2f} €")
            globals.ui.lblTotal.setText(f"{total:.2f} €")

            # Comprobar si la fila está completa
            row_items = [globals.ui.tabsales.item(row, i) for i in range(5)]
            is_row_complete = all(it and it.text().strip() for it in row_items)

            fact = globals.ui.lblnumfac.text().strip()

            if not fact.isdigit():
                return

            if is_row_complete:
                if not Conexion.existFacSales(fact):
                    if row == globals.ui.tabsales.rowCount() - 1:
                        next_row = globals.ui.tabsales.rowCount()
                        QtCore.QTimer.singleShot(
                            0, lambda: Invoice.activeSales(next_row)
                        )

                    # Guardar línea de venta
                    sale = [
                        int(globals.ui.lblnumfac.text()),
                        int(row_items[0].text()),
                        row_items[1].text(),
                        float(row_items[2].text()),
                        int(row_items[3].text()),
                        float(row_items[4].text()),
                    ]
                    globals.linesales.append(sale)

        except Exception as error:
            print("Error in cellChangedSales:", error)

        finally:
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
    def loadTableSales(idfac):
        """
        Carga las líneas de venta de una factura existente
        y las muestra en la tabla de ventas.

        :param idfac: Identificador de la factura
        :type idfac: str
        """
        try:
            data = Conexion.dataOneSale(idfac)
            table = globals.ui.tblSales
            table.setRowCount(0)

            if not data:
                Invoice.activeSales()
            else:
                table.setRowCount(len(data))

                for row_index, sale_row in enumerate(data):
                    for col_index, cell_value in enumerate(sale_row):
                        table_item = QtWidgets.QTableWidgetItem(
                            str(cell_value)
                        )
                        table.setItem(
                            row_index, col_index, table_item
                        )

                        btn_del = QtWidgets.QPushButton()
                        btn_del.setIcon(QIcon("./img/basura.png"))
                        btn_del.setIconSize(QtCore.QSize(26, 26))
                        btn_del.setFixedSize(32, 32)
                        btn_del.setStyleSheet("border: none; background-color: transparent")
                        btn_del.clicked.connect(Invoice.deleteSales)

                        table.setCellWidget(row_index, 5, btn_del)

                Invoice.bloquearTablaSales()

        except Exception as error:
            print("Error en cargarVentas:", error)



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
    def deleteSales():
        try:
            btn = globals.ui.tabsales.sender()

            if not btn:
                return

            table = globals.ui.tabsales

            # localizar la fila del botón pulsado
            for row in range(table.rowCount()):
                if table.cellWidget(row, 5) == btn:
                    break
            else:
                return

            # comprobar si la factura ya tiene ventas guardadas
            fact = globals.ui.lblnumfac.text()

            if Conexion.existFacSales(fact):
                mbox = QtWidgets.QMessageBox()
                mbox.setIcon(QtWidgets.QMessageBox.Icon.Warning)
                mbox.setWindowTitle("No permitido")
                mbox.setText("Esta factura ya está guardada y no se pueden borrar líneas.")
                mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
                mbox.exec()
                return

            # eliminar fila
            table.removeRow(row)

            # eliminar de linesales si existe
            if row < len(globals.linesales):
                globals.linesales.pop(row)

            # recalcular totales
            subtotal = 0.0
            for r in range(table.rowCount()):
                item_total = table.item(r, 4)
                if item_total and item_total.text():
                    subtotal += float(item_total.text())

            globals.subtotal = subtotal
            iva = round(subtotal * 0.21, 2)
            total = round(subtotal + iva, 2)

            globals.ui.lblSubtotal.setText(f"{subtotal:.2f} €")
            globals.ui.lblIVA.setText(f"{iva:.2f} €")
            globals.ui.lblTotal.setText(f"{total:.2f} €")

        except Exception as error:
            print("Error en deleteSales:", error)