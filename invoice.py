from operator import index
from time import sleep
from datetime import datetime

from PyQt6 import QtWidgets, QtCore
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QTabWidget

from conexion import Conexion
import globals
from globals import linesales
from reports import Reports

class Invoice:

    @staticmethod
    def searchInvoice():
        """
        Busca un cliente a partir del DNI introducido en la interfaz
        y carga sus datos en el formulario de factura.

        Si el cliente no existe, muestra un mensaje de advertencia.
        """
        try:
            dni = globals.ui.txtDniFac.text().upper().strip()

            # Si el DNI está vacío se asigna uno por defecto
            if dni == "" or Conexion.searchClient(dni):
                if dni == "":
                    dni = "00000000T"
                    globals.ui.txtDniFac.setText(dni)

                record = Conexion.dataOneCustomer(dni)

                # Carga de datos del cliente en la UI
                globals.ui.lblNamefac.setText(record[2] + " " + record[3])
                globals.ui.lblTipofac.setText(record[9])
                globals.ui.lblnumfac_3.setText(
                    record[6] + "   " + record[8] + "   " + record[7]
                )
                globals.ui.lblnumfac_4.setText(str(record[5]))

                # Estado del cliente
                if record[10] == "True":
                    globals.ui.lblStatusfac.setText("Activo")
                else:
                    globals.ui.lblStatusfac.setText("Inactivo")
            else:
                globals.ui.txtDniFac.setText("")
                mbox = QtWidgets.QMessageBox()
                mbox.setIcon(QtWidgets.QMessageBox.Icon.Warning)
                mbox.setWindowTitle("Warning")
                mbox.setText("Client not exists")
                mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
                if mbox.exec() == QtWidgets.QMessageBox.StandardButton.Ok:
                    mbox.hide()

        except Exception as error:
            print("error en searchInvoice", error)


    @staticmethod
    def reloadInvoice():
        """
        Limpia todos los campos del formulario de facturación
        y reinicia la tabla de ventas.
        """
        try:
            formfact = [
                globals.ui.lblNamefac,
                globals.ui.lblnumfac_3,
                globals.ui.lblStatusfac,
                globals.ui.lblTipofac,
                globals.ui.lblnumfac_4,
                globals.ui.lblFechafac,
                globals.ui.lblnumfac,
                globals.ui.txtDniFac,
            ]

            # Vaciar campos
            for dato in formfact:
                dato.setText("")

            # Vaciar tabla de ventas
            globals.ui.tabsales.setRowCount(0)

        except Exception as error:
            print("error en reloadInvoice", error)

    @staticmethod
    def saveInvoice():
        """
        Guarda una nueva factura en la base de datos utilizando
        el DNI del cliente y la fecha actual.

        Si la factura se crea correctamente, se habilita la tabla
        de ventas para introducir líneas.
        """
        try:
            dni = globals.ui.txtDniFac.text()
            data = datetime.now().strftime("%d/%m/%Y")

            if dni != "" and data != "":
                if Conexion.insertInvoice(dni, data):
                    Invoice.loadTableInvoice()

                    mbox = QtWidgets.QMessageBox()
                    mbox.setIcon(QtWidgets.QMessageBox.Icon.Information)
                    mbox.setWindowTitle("Invoice")
                    mbox.setText("Invoice created successfully")
                    if mbox.exec():
                        mbox.hide()

                    Invoice.activeSales()
            else:
                mbox = QtWidgets.QMessageBox()
                mbox.setIcon(QtWidgets.QMessageBox.Icon.Warning)
                mbox.setWindowTitle("Warning")
                mbox.setText("Missing Fields or Data")
                mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
                if mbox.exec() == QtWidgets.QMessageBox.StandardButton.Ok:
                    mbox.hide()

        except Exception as error:
            print("error en saveInvoice", error)

    @staticmethod
    def loadTableInvoice(self=None):
        """
        Carga todas las facturas existentes en la tabla de facturas
        de la interfaz gráfica.

        :param self: Parámetro opcional para compatibilidad con señales
        """
        try:
            records = Conexion.allInvoices(self)
            index = 0

            header = globals.ui.tablefacv.horizontalHeader()
            header.setSectionResizeMode(3, QtWidgets.QHeaderView.ResizeMode.Fixed)
            globals.ui.tablefacv.setColumnWidth(3, 36)
            globals.ui.tablefacv.setColumnWidth(0, 55)

            for record in records:
                globals.ui.tablefacv.setColumnWidth(3, 34)
                globals.ui.tablefacv.setRowCount(index + 1)
                globals.ui.tablefacv.setItem(index, 0, QtWidgets.QTableWidgetItem(record[0]))
                globals.ui.tablefacv.setItem(index, 1, QtWidgets.QTableWidgetItem(record[1]))
                globals.ui.tablefacv.setItem(index, 2, QtWidgets.QTableWidgetItem(record[2]))
                # aquí se crea un botón en cada fila
                btn_del = QtWidgets.QPushButton()
                btn_del.setIcon(QIcon("./img/basura.png"))
                btn_del.setIconSize(QtCore.QSize(26, 26))
                btn_del.setFixedSize(32, 32)
                btn_del.setStyleSheet("border: none; background-color: transparent")
                btn_del.clicked.connect(Invoice.deleteInvoice)
                globals.ui.tablefacv.setCellWidget(index, 3, btn_del)
                globals.ui.tablefacv.item(index, 0).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                globals.ui.tablefacv.item(index, 1).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                globals.ui.tablefacv.item(index, 2).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

                index = index + 1
            datos = records[0]
            globals.ui.lblnumfac.setText(str(datos[0]))
            globals.ui.txtDniFac.setText(str(datos[1]))
            globals.ui.lblFechafac.setText(str(datos[2]))
        except Exception as error:
            print("error load tablafac", error)

    @staticmethod
    def loadInvoiceirst():
        """
        Inicializa la carga de la primera factura por defecto
        con un DNI genérico.
        """
        try:
            globals.ui.txtDniFac.setText("00000000T")
            globals.ui.lblnumfac.setText("")
            globals.ui.lblFechafac.setText("")
            Invoice.searchInvoice()
            header = globals.ui.tabsales.horizontalHeader()
            header.setSectionResizeMode(5, QtWidgets.QHeaderView.ResizeMode.Fixed)
            globals.ui.tabsales.setColumnWidth(5, 36)

        except Exception as error:
            print("error en loadInvoiceirst", error)

    @staticmethod
    def selectInvoice():
        """
        Carga la factura seleccionada en la tabla de facturas
        y muestra sus líneas de venta asociadas.
        """
        try:
            row = globals.ui.tablefacv.currentRow()
            if row == -1:
                print("Debug: No row selected in tablefacv")  # Debug statement
                return

            # Obtener el ID de la factura seleccionada
            id_factura = globals.ui.tablefacv.item(row, 0).text()
            print(f"Debug: Selected invoice ID: {id_factura}")  # Debug statement

            # Obtener los datos de la factura seleccionada
            recordinvoice = Conexion.dataOneInvoice(id_factura)
            if not recordinvoice:
                QtWidgets.QMessageBox.warning(
                    None,
                    "Error",
                    f"No se encontraron datos para la factura con ID {id_factura}.",
                )
                return

            # Cargar los datos de la factura en los campos correspondientes
            globals.ui.lblnumfac.setText(str(recordinvoice[0]))
            globals.ui.txtDniFac.setText(str(recordinvoice[1]))
            globals.ui.lblFechafac.setText(str(recordinvoice[2]))

            # Obtener los datos del cliente asociado al DNI
            recordcustomer = Conexion.dataOneCustomer(recordinvoice[1])
            if recordcustomer:
                globals.ui.lblNamefac.setText(recordcustomer[2] + " " + recordcustomer[3])
                globals.ui.lblTipofac.setText(recordcustomer[9])
                globals.ui.lblnumfac_3.setText(
                    recordcustomer[6] + "   " + recordcustomer[8] + "   " + recordcustomer[7]
                )
                globals.ui.lblnumfac_4.setText(str(recordcustomer[5]))

                # Estado del cliente
                if recordcustomer[10] == "True":
                    globals.ui.lblStatusfac.setText("Activo")
                else:
                    globals.ui.lblStatusfac.setText("Inactivo")

            # Load sales data
            Invoice.cargarVentas(id_factura)

        except Exception as error:
            print("Error en selectInvoice:", error)

    @staticmethod
    def activeSales(row=None):
        """
        Activa una fila editable en la tabla de ventas para
        introducir una nueva línea de venta.

        :param row: Índice de la fila a activar
        """
        try:
            fact = globals.ui.lblnumfac.text()

            if Conexion.existeFacturaSales(fact):
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
                if not Conexion.existeFacturaSales(fact):
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
    def saveSales(self=None):
        """
        Guarda las líneas de venta asociadas a la factura actual.

        - Si la factura ya tiene ventas, genera directamente el ticket
        - Si no, guarda cada línea en la base de datos
        - Bloquea la tabla tras guardar correctamente

        :param self: Parámetro opcional para compatibilidad con señales
        """
        from products import Products
        try:
            fact = globals.ui.lblnumfac.text()

            if Conexion.existeFacturaSales(fact):
                Reports.ticket(self)
            else:
                correct = False
                for data in globals.linesales:
                    correct = Conexion.saveSales(data)
                    if correct:
                        Conexion.descontarStock(data[1], data[4]) # Code , Sales

                if globals.linesales[-1] and correct:
                    mbox = QtWidgets.QMessageBox()
                    mbox.setIcon(QtWidgets.QMessageBox.Icon.Information)
                    mbox.setWindowTitle("Sales Saved")
                    mbox.setText(
                        "Sales saved. Printing Invoice..."
                    )
                    mbox.setStandardButtons(
                        QtWidgets.QMessageBox.StandardButton.Ok
                    )

                    if mbox.exec() == QtWidgets.QMessageBox.StandardButton.Ok:
                        Invoice.bloquearTablaSales()
                        globals.linesales.clear()
                        globals.ui.tabsales.setRowCount(0)
                        mbox.hide()

                        Products.loadTableProducts()

        except Exception as error:
            print("Error in saveSales:", error)

    @staticmethod
    def cargarVentas(idfac):
        """
        Carga las líneas de venta de una factura existente
        y las muestra en la tabla de ventas.

        :param idfac: Identificador de la factura
        :type idfac: str
        """
        try:
            data = Conexion.dataOneSale(idfac)
            table = globals.ui.tabsales

            # Ensure the table is cleared before loading new data
            table.setRowCount(0)  # Clear all rows

            if not data:
                print(f"Debug: No sales data found for invoice {idfac}")  # Debug statement
                Invoice.activeSales()
            else:
                table.setRowCount(len(data))

                for row_index, sale_row in enumerate(data):
                    for col_index, cell_value in enumerate(sale_row):
                        table_item = QtWidgets.QTableWidgetItem(str(cell_value))
                        table.setItem(row_index, col_index, table_item)

                    # Add delete button in the last column
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
    def bloquearTablaSales():
        """
        Bloquea la edición de todas las celdas de la tabla de ventas,
        impidiendo modificaciones una vez guardada la factura.
        """
        try:
            table = globals.ui.tabsales
            for row in range(table.rowCount()):
                for col in range(table.columnCount()):
                    item = table.item(row, col)
                    if item:
                        item.setFlags(
                            item.flags() &
                            ~QtCore.Qt.ItemFlag.ItemIsEditable
                        )

        except Exception as error:
            print("Error en bloquearTablaSales:", error)

    @staticmethod
    def deleteInvoice():
        try:
            fact = globals.ui.lblnumfac.text()

            if Conexion.existeFacturaSales(fact):
                mbox = QtWidgets.QMessageBox()
                mbox.setIcon(QtWidgets.QMessageBox.Icon.Information)
                mbox.setWindowTitle("Can't delete Invoice")
                mbox.setText("This invoice have sales it can't be deleted.")
                mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
                if mbox.exec() == QtWidgets.QMessageBox.StandardButton.Ok:
                    mbox.hide()
            else:
                Conexion.deleteInvoice(fact)
                mbox = QtWidgets.QMessageBox()
                mbox.setIcon(QtWidgets.QMessageBox.Icon.Information)
                mbox.setWindowTitle("Deleted invoice")
                mbox.setText("Invoice Nº" + str(fact) + " has been successfully deleted.")
                mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
                if mbox.exec() == QtWidgets.QMessageBox.StandardButton.Ok:
                    mbox.hide()
                Invoice.loadTableInvoice()
        except Exception as error:
            print("Error en deleteInvoice:", error)

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

            if Conexion.existeFacturaSales(fact):
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