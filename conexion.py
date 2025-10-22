import os

from events import *

from PyQt6 import QtSql, QtWidgets, QtCore, QtGui


class Conexion:
    def db_conexion(self = None):
        ruta_db = './data/bbdd.sqlite'

        if not os.path.isfile(ruta_db):
            QtWidgets.QMessageBox.critical(None, 'Error', 'El archivo de la base de datos no existe.',
                                           QtWidgets.QMessageBox.StandardButton.Cancel)
            return False
        db = QtSql.QSqlDatabase.addDatabase('QSQLITE')
        db.setDatabaseName(ruta_db)

        if db.open():
            query = QtSql.QSqlQuery()
            query.exec("SELECT name FROM sqlite_master WHERE type='table';")

            if not query.next():  # Si no hay tablas
                QtWidgets.QMessageBox.critical(None, 'Error', 'Base de datos vacía o no válida.',
                                               QtWidgets.QMessageBox.StandardButton.Cancel)
                return False
            else:
                QtWidgets.QMessageBox.information(None, 'Aviso', 'Conexión Base de Datos realizada',
                                                  QtWidgets.QMessageBox.StandardButton.Ok)
                return True
        else:
            QtWidgets.QMessageBox.critical(None, 'Error', 'No se pudo abrir la base de datos.',
                                           QtWidgets.QMessageBox.StandardButton.Cancel)
            return False

    def listProv(self=None):

        listProv = []
        query = QtSql.QSqlQuery()
        query.prepare("SELECT * FROM provincias;")
        if query.exec():
            while query.next():
                listProv.append(query.value(1))
        return listProv

    def listMuniProv(province):
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
    def dataOneCustomer(dato):
        try:
            list = []
            dato = str(dato).strip()
            #busca por el mobile
            query = QtSql.QSqlQuery()
            query.prepare("SELECT * FROM customers where mobile = :dato")
            query.bindValue(":dato", str(dato))
            if query.exec():
                while query.next():
                    for i in range(query.record().count()):
                        list.append(query.value(i))
            #si no hay por el movil busca por el dni
            if len(list) == 0:
                query = QtSql.QSqlQuery()
                query.prepare("SELECT * FROM customers where dni_nie = :dato")
                query.bindValue(":dato", str(dato))
                if query.exec():
                    while query.next():
                        for i in range(query.record().count()):
                            list.append(query.value(i))

            return list

        except Exception as e:
            print("error in load dataOneCustomer", e)

    @staticmethod
    def deleteCli(dni):
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
        try:
            query = QtSql.QSqlQuery()
            query.prepare("INSERT INTO customers(dni_nie, adddata,surname,name,mail,mobile,address,province,city, invoicetyp, historical) VALUES(:dnicli, :adddata,:surname,:name,:mail,:mobile,:address,:province,:city,:invoicetyp,:historical)")
            query.bindValue(":dnicli", str(newcli[0]))
            query.bindValue(":adddata", str(newcli[1]))
            query.bindValue(":surname", str(newcli[2]))
            query.bindValue(":name", str(newcli[3]))
            query.bindValue(":mail", str(newcli[4]))
            query.bindValue(":mobile", str(newcli[5]))
            query.bindValue(":address", str(newcli[6]))
            query.bindValue(":province", str(newcli[7]))
            query.bindValue(":city", str(newcli[8]))
            query.bindValue(":invoicetyp", str(newcli[9]))
            query.bindValue(":historical", str(True))
            if query.exec():
                return True
            else:
                return False
        except:
            print("error in addCli")


    @staticmethod
    def modifyCli(dni,modifcli):
        try:
            query = QtSql.QSqlQuery()
            query.prepare("UPDATE customers SET adddata= :data, surname = :surname, name = :name , mobile = :mobile, address = :address,province = :province, city = :city, invoicetyp = :invoicetyp, historical = :historical "
                          " "
                          "WHERE dni_nie = :dni")
            query.bindValue(":dni", str(dni))
            query.bindValue(":data", str(modifcli[0]))
            query.bindValue(":surname", str(modifcli[1]))
            query.bindValue(":name", str(modifcli[2]))
            query.bindValue(":mail", str(modifcli[3]))
            query.bindValue(":mobile", str(modifcli[4]))
            query.bindValue(":address", str(modifcli[5]))
            query.bindValue(":province", str(modifcli[6]))
            query.bindValue(":city", str(modifcli[7]))
            query.bindValue("historical", str(modifcli[8]))
            query.bindValue(":invoicetyp", str(modifcli[9]))
            if query.exec():
                return True
            else:
                return False
        except:
            print("error in modifyCli")
