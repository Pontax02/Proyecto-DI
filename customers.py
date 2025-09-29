import re

import globals



class Customers:

    @staticmethod
    def checkDni(self=None):
        try:
            dni = globals.ui.txtDnicli.text()
            dni = str(dni).upper()
            globals.ui.txtDnicli.setText(dni)
            tabla = "TRWAGMYFPDXBNJZSQVHLCKE"
            dig_ext = "XYZ"
            reemp_dig_ext = {'X': '0', 'Y': '1', 'Z': '2'}
            numeros = "1234567890"
            if len(dni) == 9:
                dig_control = dni[8]
                dni = dni[:8]
                if dni[0] in dig_ext:
                    dni = dni.replace(dni[0], reemp_dig_ext[dni[0]])
                if len(dni) == len([n for n in dni if n in numeros]) and tabla[int(dni) % 23] == dig_control:
                    globals.ui.txtDnicli.setStyleSheet('background-color: rgb(255, 255, 220);')
                else:
                    globals.ui.txtDnicli.setStyleSheet('background-color:#FFC0CB;')
                    globals.ui.txtDnicli.setText(None)
                    globals.ui.txtDnicli.setFocus()
            else:
                globals.ui.txtDnicli.setStyleSheet('background-color:#FFC0CB;')
                globals.ui.txtDnicli.setText(None)
                globals.ui.txtDnicli.setFocus()
        except Exception as error:
            print("error en validar dni ", error)


    def capitalizar(texto,widget):
        try:
            texto = texto.title()
            widget.setText(texto)
        except Exception as error:
            print("error en capitalizar texto ", error)


    def checkMail(email):

        patron = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        if re.match(patron, email):
            globals.ui.txtEmailcli.setStyleSheet('background-color: rgb(255, 255, 220);')
        else:
            globals.ui.txtEmailcli.setStyleSheet('background-color:#FFC0CB;')
            globals.ui.txtEmailcli.setText(None)
            globals.ui.txtEmailcli.setPlaceholderText('Invalid Email')
            globals.ui.txtEmailcli.setFocus()


    def checkMobil(numero):
        patron = r'^[67]\d{8}$'
        if re.match(patron, numero):
            globals.ui.txtMobilecli.setStyleSheet('background-color: rgb(255, 255, 220);')
        else:
            globals.ui.txtMobilecli.setStyleSheet('background-color: #FFC0CB;')
            globals.ui.txtMobilecli.setText(None)
            globals.ui.txtMobilecli.setPlaceholderText('Invalid Mobile')
            globals.ui.txtMobilecli.setFocus()