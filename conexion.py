import os

from events import *

from PyQt6 import QtSql, QtWidgets, QtCore, QtGui


class Conexion:
    def db_conexion(self = None):
        """
        Modulo para comprobar la conexión principal a la base de datos.
        :return: Boolean
        :rtype: Boolean
        """
        ruta_db = './data/bbdd.sqlite'

        if not os.path.isfile(ruta_db):
            QtWidgets.QMessageBox.critical(None, 'Error', 'The database file does not exist',
                                           QtWidgets.QMessageBox.StandardButton.Cancel)
            return False
        db = QtSql.QSqlDatabase.addDatabase('QSQLITE')
        db.setDatabaseName(ruta_db)

        if db.open():
            query = QtSql.QSqlQuery()
            query.exec("SELECT name FROM sqlite_master WHERE type='table';")

            if not query.next():  # Si no hay tablas
                QtWidgets.QMessageBox.critical(None, 'Error', 'Empty database or not valid',
                                               QtWidgets.QMessageBox.StandardButton.Cancel)
                return False
            else:
                QtWidgets.QMessageBox.information(None, 'Aviso', 'Database connected successfully',
                                                  QtWidgets.QMessageBox.StandardButton.Ok)
                return True
        else:
            QtWidgets.QMessageBox.critical(None, 'Error', 'Database could not be opened',
                                           QtWidgets.QMessageBox.StandardButton.Cancel)
            return False

    def listProv(self=None):
        """
        Modulo para obtener de la base de datos las provincias de España
        :return: devuelve una lista con las provincias
        :rtype: List
        """
        listProv = []
        query = QtSql.QSqlQuery()
        query.prepare("SELECT * FROM provincias;")
        if query.exec():
            while query.next():
                listProv.append(query.value(1))
        return listProv

    def listMuniProv(province):
        """
        Modulo para listar los municipios 
        :return: Devuelve la lista de municipios correspondiente a la provincia proporcionada
        :rtype: List
        """
        try:
            listmunicipios = []
            query = QtSql.QSqlQuery()
            query.prepare("SELECT * FROM municipios where idprov = (select idprov from provincias where provincia = :province)")
            query.bindValue(":province", province)
            if query.exec():
                while query.next():
                    listmunicipios.append(query.value(1))
            return listmunicipios
        except Exception as e:
            print("error en cargar MuniProv", e)


    @staticmethod
    def listTabCustomers(var):
        """
         Modulo para obtener de la base de datos los clientes
        :param var: Estado historico del cliente
        :type var: Boolean
        :return: Devuelve los clientes de la base datos
        :rtype: List
        """
        list = []
        if var:
            query = QtSql.QSqlQuery()
            query.prepare("SELECT * FROM customers  where historical = :true order by surname")
            query.bindValue(":true",str( True))
            if query.exec():
                while query.next():
                    row = [query.value(i) for i in range(query.record().count())]
                    list.append(row)
        else:
            query = QtSql.QSqlQuery()
            query.prepare("SELECT * FROM customers order by surname")
            if query.exec():
                while query.next():
                    row = [query.value(i) for i in range(query.record().count())]
                    list.append(row)
        return list

    @staticmethod
    def listTabProducts(self):
        """
        Modulo para obtener todos los productos de la base de datos
        :return: Devuelve la lista de productos
        :rtype: List
        """
        list = []

        query = QtSql.QSqlQuery()
        query.prepare("SELECT * FROM products order by code")

        if query.exec():
            while query.next():

                row = [query.value(i) for i in range(query.record().count())]
                list.append(row)

        return list
    @staticmethod
    def dataOneCustomer(dato):
        """

        Obtiene los datos de un cliente buscándolo por móvil o DNI/NIE.

        :param str dato: Móvil o DNI/NIE.
        :return: Lista con los datos del cliente.
        :rtype: list

        """

        try:
            list = []
            dato = str(dato).strip()
            query = QtSql.QSqlQuery()
            query.prepare("SELECT * FROM customers where mobile = :dato")
            query.bindValue(":dato", str(dato))
            if query.exec():
                while query.next():
                    for i in range (query.record().count()):
                        list.append(query.value(i))
            if len(list) == 0:
                query = QtSql.QSqlQuery()
                query.prepare("SELECT * FROM customers where dni_nie = :dato")
                query.bindValue(":dato", str(dato))
                if query.exec():
                    while query.next():
                        for i in range (query.record().count()):
                            list.append(query.value(i))
            return list
        except Exception as error:
            print("error dataOneCustomer", error)

    @staticmethod
    def dataOneProduct(dato):
        """

        :param dato: Id del producto
        :type dato: int
        :return: Devuelve los datos del producto
        :rtype: list
        """
        try:
            listpro = []
            dato = str(dato).strip()

            query = QtSql.QSqlQuery()
            query.prepare("SELECT * FROM products where code = :dato")
            query.bindValue(":dato", str(dato))

            if query.exec():
                while query.next():
                    for i in range(query.record().count()):
                        listpro.append(query.value(i))

            return listpro

        except Exception as e:
            print("error in load dataOneProduct", e)

    @staticmethod
    def deleteCli(dni):
        """

        :rtype: None
        """
        try:
            query = QtSql.QSqlQuery()
            query.prepare("UPDATE customers set historical = :value WHERE dni_nie = :dni")
            query.bindValue(":dni", str(dni))
            query.bindValue(":value",str(False))
            if query.exec():
                return True
            else:
                return False
        except Exception as e:
            print("error in delete", e)




    @staticmethod
    def addCli(newcli):
        """
        Modulo para añadir un cliente a la base de datos
        :param newcli: informacion del cliente
        :type newcli: lista
        :return: bool
        :rtype:
        :rtype: bool | None
        """
        try:

            query = QtSql.QSqlQuery()
            query.prepare("INSERT INTO customers(dni_nie, adddata,surname,name,mail,mobile,address,province,city, invoicetype, historical) VALUES(:dnicli, :adddata,:surname,:name,:mail,:mobile,:address,:province,:city,:invoicetype,:historical)")
            query.bindValue(":dnicli", str(newcli[0]))
            query.bindValue(":adddata", str(newcli[1]))
            query.bindValue(":surname", str(newcli[2]))
            query.bindValue(":name", str(newcli[3]))
            query.bindValue(":mail", str(newcli[4]))
            query.bindValue(":mobile", str(newcli[5]))
            query.bindValue(":address", str(newcli[6]))
            query.bindValue(":province", str(newcli[7]))
            query.bindValue(":city", str(newcli[8]))
            query.bindValue(":invoicetype", str(newcli[9]))
            query.bindValue(":historical", str(True))
            if query.exec():
                return True
            else:
                return False
        except:
            print("error in addCli")

    @staticmethod
    def addPro(newpro):
        try:

            query = QtSql.QSqlQuery()
            query.prepare("INSERT INTO products(name,stock,family,unitprice) VALUES(:name,:stock,:family,:unitprice)")
            query.bindValue(":name", str(newpro[0]))
            query.bindValue(":stock", str(newpro[1]))
            query.bindValue(":family", str(newpro[2]))
            query.bindValue(":unitprice", str(newpro[3]))

            if query.exec():
                return True
            else:
                return False
        except Exception as e:
            print("error in addPro", e)


    @staticmethod
    def modifyCli(dni,modifcli):
        try:

            if str(dni) == "":
                return False
            query = QtSql.QSqlQuery()
            query.prepare("UPDATE customers SET adddata = :data, surname = :surname, name = :name ,mail = :mail ,mobile = :mobile, address = :address,province = :province, city = :city, invoicetype = :invoicetype, historical = :historical  WHERE dni_nie = :dni")
            query.bindValue(":dni", str(dni))
            query.bindValue(":data", str(modifcli[0]))
            query.bindValue(":surname", str(modifcli[1]))
            query.bindValue(":name", str(modifcli[2]))
            query.bindValue(":mail", str(modifcli[3]))
            query.bindValue(":mobile", str(modifcli[4]))
            query.bindValue(":address", str(modifcli[5]))
            query.bindValue(":province", str(modifcli[6]))
            query.bindValue(":city", str(modifcli[7]))
            query.bindValue(":historical", str(modifcli[8]))
            query.bindValue(":invoicetype", str(modifcli[9]))
            if query.exec():

                return True
            else:
                return False
        except:
            print("error in modifyCli")

    def modifyPro(id, modpro):
        try:

            query = QtSql.QSqlQuery()
            query.prepare("UPDATE products SET name= :name, stock = :stock,family =:family, "
                          " unitprice =:unitprice where code = :id")
            query.bindValue(":id", str(id))
            query.bindValue(":name", str(modpro[0]))
            query.bindValue(":stock", int(modpro[2]))
            query.bindValue(":family", str(modpro[1]))
            price = modpro[3].replace("€", "")
            query.bindValue(":unitprice", str(price))

            if query.exec():
                return True
            else:
                return False
        except Exception as error:
            print("error modifyPro", error)

    def deletePro(id):
        try:
            query = QtSql.QSqlQuery()
            query.prepare("DELETE FROM products WHERE name = :id")
            query.bindValue(":id", str(id))
            if query.exec():
                return True
            else:
                return False
        except Exception as error:
            print("error deletePro in conexion", error)


    # Empiezo la facturacion


    
    @staticmethod
    def searchClient(dni):
        """

        Verifica si existe un cliente por DNI.

        :param str dni: DNI/NIE.
        :return: ``True`` si existe.
        :rtype: bool

        """

        try:
            dni = str(dni).upper()
            query = QtSql.QSqlQuery()
            query.prepare("SELECT * FROM customers WHERE dni_nie = :dni")
            query.bindValue(":dni", str(dni))
            if query.exec():
                if query.next():
                    return True
                else:
                    return False

        except Exception as error:
            print("error searchClient", error)

    @staticmethod
    def insertInvoice(dni,data):
        try:
            query = QtSql.QSqlQuery()
            query.prepare("INSERT INTO invoices(dninie,data) VALUES(:dni, :data)")
            query.bindValue(":dni", str(dni))
            query.bindValue(":data", str(data))
            if query.exec():
                return True
            else:
                return False
        except Exception as error:
            print("error insertInvoice in conexion", error)

    @staticmethod
    def deleteInvoice(numfac):
        try:
            query = QtSql.QSqlQuery()
            query.prepare("DELETE FROM invoices WHERE idfac= :numfac")
            query.bindValue(":numfac", int(numfac))
            if query.exec():
                return True
            else:
                return False
        except Exception as error:
            print("error insertInvoice in conexion", error)


    def allInvoices(self):
        try:
            records= []

            query = QtSql.QSqlQuery()
            query.prepare("SELECT * FROM invoices ORDER BY idfac DESC")
            if query.exec():
                while query.next():
                    row = [str(query.value(i)) for i in range(query.record().count())]
                    records.append(row)
            return records


        except Exception as error:
            print("error allInvoices in conexion", error)


    def selectProduct(item):
        try:
            query = QtSql.QSqlQuery()
            query.prepare("SELECT name, unitprice FROM products WHERE code = :code")
            query.bindValue(":code", str(item))
            if query.exec():
                if query.next():
                    row = [str(query.value(i)) for i in range(query.record().count())]
                else:
                    row = []

            return row
        except Exception as error:
            print("error selectProduct in conexion", error)

    @staticmethod
    def saveSales(data):
        """

        Inserta una línea de venta asociada a una factura.

        :param list data: Datos de la venta (idfac, idpro, product, unitprice, amount, total)
        :return: ``True`` si se insertó correctamente.
        :rtype: bool

        """

        try:
            print("Debug: Intentando guardar línea de venta con datos:", data)
            query = QtSql.QSqlQuery()
            query.prepare("INSERT INTO sales (idfac, idpro, product, unitprice, amount, total) "
                        " VALUES (:idfac, :idpro, :product, :unitprice, :amount, :total)")
            query.bindValue(":idfac", data[0])
            query.bindValue(":idpro", data[1])
            query.bindValue(":product", data[2])
            query.bindValue(":unitprice", data[3])
            query.bindValue(":amount", data[4])
            query.bindValue(":total", data[5])
            if query.exec():
                print("Debug: Línea de venta guardada correctamente.")
                return True
            else:
                print("Error: Falló la inserción en la tabla sales.")
                return False

        except Exception as error:
            print("Error en saveSales conexion:", error)


    def existFac(item):
        try:
            records = []
            query = QtSql.QSqlQuery()
            query.prepare("SELECT * FROM sales WHERE idfac = :item")
            query.bindValue(":item", int(item))
            if query.exec():
                while query.next():
                    row = [str(query.value(i)) for i in range(query.record().count())]
                    records.append(row)
            return records
        except Exception as error:
            print("error existFac in conexion", error)
    @staticmethod
    def existeFacturaSales(fact):
        """

               Devuelve True si en la tabla ventas existe el idfac, si no devuelve False
               :return: bool
               :rtype: bool

               """
        try:
            print("Debug: Verificando existencia de factura en ventas, idfac:", fact)
            if not fact or not str(fact).isdigit():
                print("Debug: idfac no válido")
                return False

            query = QtSql.QSqlQuery()
            query.prepare("SELECT * FROM sales WHERE idfac = :idfac")
            query.bindValue(":idfac", int(fact))
            if query.exec():
                if query.next():
                    print("Debug: Factura encontrada en ventas")
                    return True
                else:
                    print("Debug: Factura no encontrada en ventas")
                    return False

        except Exception as error:
            print("Error en existeFacturaSales:", error)

    @staticmethod
    def datosFac(id_factura):

        try:
            print("Debug: Ejecutando consulta para obtener datos de la factura con idfac:", id_factura)
            all_data_sales = []
            query = QtSql.QSqlQuery()
            query.prepare("SELECT * FROM sales where idfac = :idfac;")

            query.bindValue(":idfac", int(id_factura))

            if query.exec():
                print("Debug: Consulta ejecutada correctamente.")
                while query.next():
                    row = [query.value(i) for i in range(query.record().count())]
                    all_data_sales.append(row)
                print("Debug: Datos obtenidos:", all_data_sales)
            else:
                print("Error: La consulta para obtener datos de la factura falló.")

            return all_data_sales

        except Exception as error:
            print("Error en datosFac:", error)

    @staticmethod
    def dataOneSale(idfac):
        """
        Obtiene las líneas de venta de una factura.

        :param int idfac: ID de la factura.
        :return: Lista con líneas de venta.
        :rtype: list[list]
        """
        try:
            rows = []
            idfac = str(idfac).strip()
            query = QtSql.QSqlQuery()
            query.prepare("SELECT * FROM sales WHERE idfac = :idfac")
            query.bindValue(":idfac", idfac)

            if query.exec():
                while query.next():
                    codigo = query.value(2)
                    precio = query.value(4)
                    cantidad = query.value(5)
                    concepto = query.value(3)

                    # Calcular el total dinámicamente
                    total = round(float(precio) * float(cantidad), 2) if precio and cantidad else 0.0

                    rows.append([codigo, precio, cantidad, concepto, total])

            print(f"Debug: Ventas obtenidas para la factura {idfac}: {rows}")
            return rows

        except Exception as error:
            print(f"Error en dataOneSale: {error}")

    @staticmethod
    def dataOneInvoice(idfact):
        """

        Obtiene los datos de una factura por ID.

        :param int idfact: ID de la factura.
        :return: Lista con datos de la factura.
        :rtype: list

        """

        try:
            list = []
            idfact = str(idfact).strip()
            query = QtSql.QSqlQuery()
            query.prepare("SELECT * FROM invoices WHERE idfac = :idfac")
            query.bindValue(":idfac", idfact)
            if query.exec():
                while query.next():
                    for i in range(query.record().count()):
                        list.append(query.value(i))
            return list

        except Exception as error:
            print("error dataOneInvoice", error)

    @staticmethod
    def descontarStock(code, cantidad):
        """
        Descuenta el stock de un producto si hay suficiente cantidad disponible.

        :param code: Código del producto.
        :param cantidad: Cantidad a descontar.
        :return: True si el stock se descontó correctamente, False en caso contrario.
        """
        try:
            query = QtSql.QSqlQuery()

            # Verificar el stock actual del producto
            query.prepare("SELECT stock FROM products WHERE code = :code")
            query.bindValue(":code", code)

            if not query.exec() or not query.next():
                print(f"Error: No se pudo obtener el stock del producto con código {code}.")
                return False

            stock_actual = query.value(0)
            print(f"Debug: Stock actual del producto {code}: {stock_actual}")

            # Validar si hay suficiente stock
            if stock_actual < cantidad:
                print(f"Error: Stock insuficiente para el producto {code}. Disponible: {stock_actual}, solicitado: {cantidad}.")
                return False

            # Descontar el stock
            nuevo_stock = stock_actual - cantidad
            query.prepare("UPDATE products SET stock = :nuevo_stock WHERE code = :code")
            query.bindValue(":nuevo_stock", nuevo_stock)
            query.bindValue(":code", code)

            if query.exec():
                print(f"Debug: Stock actualizado para el producto {code}. Nuevo stock: {nuevo_stock}")
                return True
            else:
                print(f"Error: No se pudo actualizar el stock para el producto {code}.")
                return False

        except Exception as error:
            print("Error en descontarStock:", error)
            return False
        
    @staticmethod
    def listProducts():
        """

        Obtiene la lista completa de productos.

        :return: Lista de filas de productos.
        :rtype: list[list]

        """

        list = []
        query = QtSql.QSqlQuery()
        query.prepare("SELECT * FROM products")
        if query.exec():
            while query.next():
                row = [query.value(i) for i in range(query.record().count())]
                list.append(row)
        return list