import os
from datetime import datetime
import globals
from reportlab.pdfgen import canvas
from conexion import *
from PIL import Image

class Reports:

    @staticmethod
    def footer(titulo):
        try:
            globals.report.line(35, 60,525, 60)
            globals.report.line(35, 60, 525, 60)
            day = datetime.today().strftime("%d/%m/%Y %H:%M:%S")
            globals.report.setFont('Helvetica', size = 7)
            globals.report.drawString(70, 50, day)
            globals.report.drawString(250, 50, titulo)
            globals.report.drawString(480, 50, str('Página: ' + str(globals.report.getPageNumber())))
            globals.report.setFont('Helvetica', size=7)
            globals.report.drawString(70, 50, day)
            globals.report.drawString(250, 50, titulo)
            globals.report.drawString(480, 50, str('Página: ' + str(globals.report.getPageNumber())))
        except Exception as error:
            print(error)

    @staticmethod
    def topReport(titulo):
        try:
            path_logo = ".\\img\\omega.ico"
            logo = Image.open(path_logo)
            if isinstance(logo, Image.Image):
                globals.report.line(35, 60,525, 60)
                globals.report.setFont('Helvetica-Bold', size = 10)
                globals.report.drawString(55, 785, "EMPRESA TEIS" )
                globals.report.drawCentredString(290, 675, titulo)
                globals.report.line(35, 665,525, 665)
                globals.report.line(35, 60, 525, 60)
                globals.report.setFont('Helvetica-Bold', size=10)
                globals.report.drawString(55, 785, "EMPRESA TEIS")
                globals.report.drawCentredString(290, 675, titulo)
                globals.report.line(35, 665, 525, 665)
                #dibuja la imagen
                globals.report.drawImage(path_logo,490, 765, width=40, height=40)
                globals.report.drawImage(path_logo, 490, 765, width=40, height=40)
                # datos de la empresa
                globals.report.setFont('Helvetica', size = 8)
                globals.report.drawString(55, 760, "CIF: A12345678" )
                globals.report.drawString(55, 745, 'Avda. de Galicia, 101')
                globals.report.drawString(55, 730, "Vigo - 36215 - España")
                globals.report.drawString(55, 715, "Tlfo: 986 123 456")
                globals.report.drawString(55, 700, "email: teis@mail.com")
                globals.report.line(50, 800, 160, 800 )
                globals.report.line(50, 695, 160, 695 )
                globals.report.line(50, 800, 50, 695 )
                globals.report.line(160, 800, 160, 695 )
            else:
                print("no puedo cargar el imagen")

        except Exception as error:
            print(error)

    def reportCustomers(self):
        try:
            rootPath = ".\\reports"
            if not os.path.exists(rootPath):
                os.makedirs(rootPath)
            data = datetime.today().strftime("%Y_%m_%d_%H_%M_%S")
            namereportcli = data + "_reportcustomers.pdf"
            pdf_path = os.path.join(rootPath , namereportcli)
            globals.report = canvas.Canvas(pdf_path)
            titulo = "Listado Clientes"
            Reports.footer(titulo)
            Reports.topReport(titulo)
            var = False
            records = Conexion.listTabCustomers(var)

            if not records:
                print("No Customers")
                return

            items =  ["DNI_NIE", "SURNAME", "NAME", "MOBILE", "CITY", "INVOICE TYPE", "STATE"]
            globals.report.setFont("Helvetica-Bold", 10)
            globals.report.drawString(45, 650, str(items[0]))
            globals.report.drawString(105, 650, str(items[1]))
            globals.report.drawString(185, 650, str(items[2]))
            globals.report.drawString(245, 650, str(items[3]))
            globals.report.drawString(330, 650, str(items[4]))
            globals.report.drawString(390, 650, str(items[5]))
            globals.report.drawString(480, 650, str(items[6]))
            globals.report.line(35, 645, 525, 645)
            x = 55
            y = 630

            for record in records:
                if y <= 90:  # crea una nueva página
                    globals.report.setFont("Helvetica-Oblique", 8)
                    globals.report.drawString(450, 75, "Página siguiente...")
                    globals.report.showPage()  #crea una nueva página
                    self.footer(titulo)
                    self.topReport(titulo)
                    items = ["DNI_NIE", "SURNAME", "NAME", "MOBILE", "CITY", "INVOICE TYPE", "STATE"]
                    globals.report.setFont("Helvetica-Bold", 10)
                    globals.report.drawString(45, 650, str(items[0]))
                    globals.report.drawString(105, 650, str(items[1]))
                    globals.report.drawString(185, 650, str(items[2]))
                    globals.report.drawString(245, 650, str(items[3]))
                    globals.report.drawString(330, 650, str(items[4]))
                    globals.report.drawString(390, 650, str(items[5]))
                    globals.report.drawString(480, 650, str(items[6]))
                    globals.report.line(35, 645, 525, 645)
                    x = 55
                    y = 630

                globals.report.setFont("Helvetica", 8)
                dni = '***' + str(record[0][4:7] + '***')
                globals.report.drawCentredString(x +10, y, dni)
                globals.report.drawString(x + 50, y, str(record[2]))
                globals.report.drawString(x + 130, y, str(record[3]))
                globals.report.drawCentredString(x + 210, y, str(record[5]))
                globals.report.drawString(x + 270, y, str(record[8]))
                globals.report.drawString(x + 350, y, str(record[9]))
                if str(record[10]) == 'True':
                    globals.report.drawString(x + 430, y, "Activo")
                else:
                    globals.report.drawString(x + 430, y, "Baja")
                y = y - 25

            globals.report.save()
            # otra forma de abrir sin necesidade comprobar el nombre porque ya existe
            try:
                os.startfile(pdf_path)
            except Exception as e:
                print("No se pudo abrir el PDF:", e)

        except Exception as error:
            print("error en reportCustomers", error)

    def reportProducts(self):
        try:
            rootPath = ".\\reports"
            if not os.path.exists(rootPath):
                os.makedirs(rootPath)
            data = datetime.today().strftime("%Y_%m_%d_%H_%M_%S")
            namereportpro = data + "_reportproducts.pdf"
            pdf_path = os.path.join(rootPath, namereportpro)
            globals.report = canvas.Canvas(pdf_path)
            titulo = "Product List"
            Reports.footer(titulo)
            Reports.topReport(titulo)
            records = Conexion.listProducts()
            if not records:
                print("No Productos")
                return
            items = ["ID", "NAME", "FAMILY", "STOCK", "PRICE"]
            globals.report.setFont("Helvetica-Bold", 10)
            globals.report.drawString(60, 650, str(items[0]))
            globals.report.drawString(165, 650, str(items[1]))
            globals.report.drawString(310, 650, str(items[2]))
            globals.report.drawString(390, 650, str(items[3]))
            globals.report.drawString(480, 650, str(items[4]))
            globals.report.line(35, 645, 525, 645)
            x = 55
            y = 630
            for record in records:
                if y <= 90:  # crea una nueva página
                    globals.report.setFont("Helvetica-Oblique", 8)
                    globals.report.drawString(450, 75, "Página siguiente...")
                    globals.report.showPage()  # crea una nueva página
                    Reports.footer(titulo)
                    Reports.topReport(titulo)
                    items = ["DNI_NIE", "SURNAME", "NAME", "MOBILE", "CITY", "INVOICE TYPE", "STATE"]
                    globals.report.setFont("Helvetica-Bold", 10)
                    globals.report.drawString(60, 650, str(items[0]))
                    globals.report.drawString(165, 650, str(items[1]))
                    globals.report.drawString(310, 650, str(items[2]))
                    globals.report.drawString(390, 650, str(items[3]))
                    globals.report.drawString(480, 650, str(items[4]))
                    globals.report.line(35, 645, 525, 645)
                    x = 55
                    y = 630
                globals.report.setFont("Helvetica-Bold", 8)
                globals.report.drawCentredString(x+10, y, str(record[0]))
                globals.report.drawString(x + 110, y, str(record[1]))
                globals.report.drawString(x + 255, y, str(record[2]))
                globals.report.drawString(x + 350, y, str(record[3]))
                globals.report.drawRightString(x + 450, y, str(record[4]))
                y = y - 25
            globals.report.save()
            # otra forma de abrir sin necesidade comprobar el nombre porque ya existe
            try:
                os.startfile(pdf_path)
            except Exception as e:
                print("No se pudo abrir el PDF:", e)

        except Exception as error:
                print("error en report productos", error)

    @staticmethod
    def ticket(self = None):
        try:
            rootPath = ".\\reports"
            if not os.path.exists(rootPath):
                os.makedirs(rootPath)
            data = datetime.today().strftime("%Y_%m_%d_%H_%M_%S")
            ticket_name = data + "_ticket.pdf"
            pdf_path = os.path.abspath(os.path.join(rootPath, ticket_name))

            globals.report = canvas.Canvas(pdf_path)
            dni = globals.ui.lblDniFactura.text()
            titulo = "FACTURA SIMPLIFICADA" if dni == "00000000T" else "FACTURA"

            records = Conexion.dataOneCustomer(dni)

            y = 785
            globals.report.setFont("Helvetica-Bold", 10)
            globals.report.drawString(220, y, "DNI: " + str(records[0]))
            globals.report.drawString(220, y - 15, "APELLIDOS: " + str(records[2]))
            globals.report.drawString(220, y - 30, "NOMBRE: " + str(records[3]))
            globals.report.drawString(220, y - 45, "DIRECCIÓN:  " + str(records[6]))
            globals.report.drawString(220, y - 60, "LOCALIDAD: " + str(records[8]) + "  PROVINCIA: " + str(records[7]))

            numfact = globals.ui.lblnumfac.text()
            globals.report.setFont("Helvetica-Bold", 10)
            if titulo == "FACTURA":
                globals.report.drawString(320, 675, "Nº " + str(numfact))
            else:
                globals.report.drawString(360, 675, "Nº " + str(numfact))

            dataFact = Conexion.datosFac(numfact)
            print(dataFact)
            items = ["Code", "Product", "Unit Price", "Amount", "Total"]
            globals.report.drawString(60, 650, str(items[0]))
            globals.report.drawString(150, 650, str(items[1]))
            globals.report.drawString(310, 650, str(items[2]))
            globals.report.drawString(400, 650, str(items[3]))
            globals.report.drawString(480, 650, str(items[4]))
            globals.report.line(35, 640, 525, 640)

            x = 60
            y = 625
            for data in dataFact:
                globals.report.setFont("Helvetica", 8)
                globals.report.drawString(x, y, str(data[2]))
                globals.report.drawString(x + 90, y, str(data[4]))
                globals.report.drawString(x + 250, y, str(data[5]))
                globals.report.drawString(x + 360, y, str(data[3]))
                globals.report.drawString(x + 420, y, str(data[6]))
                y = y - 25

            Reports.topReport(titulo)
            Reports.footer(titulo)
            globals.report.save()

            try:
                os.startfile(pdf_path)
            except Exception as e:
                print("No se pudo abrir el PDF:", e)

        except Exception as error:
            print("error ticket", error)