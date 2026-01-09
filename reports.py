

from PIL import Image
from reportlab.pdfgen import canvas
import os, datetime

import conexion
import globals
import globals
from conexion import Conexion
from globals import subtotal


class Reports:
    def __init__(self):
        rootPath= ".\\reports"
        data = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
        self.namereportcli = data + "_reportcustomers.pdf"
        self.ticket = data + "_ticket.pdf"
        self.pdf_path = os.path.join(rootPath, self.namereportcli)
        self.ticket_path = os.path.join(rootPath, self.ticket)
        globals.report = canvas.Canvas(self.pdf_path)
        globals.report = canvas.Canvas(self.ticket_path)
        self.rootPath = rootPath

    @staticmethod
    def footer(title):


        try:

            globals.report.line(35,60,525,60)
            globals.report.line(35,60,525,60)
            day = datetime.datetime.today()
            day = day.strftime("%d/%m/%Y %H:%M:%S")
            globals.report.setFont("Helvetica", 7)
            globals.report.drawString(70,50,day)
            globals.report.drawString(250,50,title)
            globals.report.drawString(500,50,str("Page: " +  str(globals.report.getPageNumber())))
            globals.report.setFont("Helvetica", 7)
            globals.report.drawString(70,50,day)
            globals.report.drawString(250,50,title)
            globals.report.drawString(500,50,str("Page: " +  str(globals.report.getPageNumber())))

        except Exception as error:
            print(error)
    @staticmethod
    def topreport(title):
        try:
            path_logo= ".\\img\\omega.ico"
            logo = Image.open(path_logo)
            if isinstance(logo,Image.Image):

                globals.report.setFont("Helvetica", 10)
                globals.report.drawString(55,785,"EMPRESA TEIS")
                globals.report.drawCentredString(300,675,title)
                globals.report.line(35,665,525,665)
                globals.report.drawImage(path_logo,480,745,40,40)
                globals.report.setFont("Helvetica", 10)
                globals.report.drawString(55,785,"EMPRESA TEIS")
                globals.report.drawCentredString(300,675,title)
                globals.report.line(35,665,525,665)
                globals.report.drawImage(path_logo,480,745,40,40)
                #data company
                globals.report.setFont("Helvetica", 8)
                globals.report.drawString(55,760,"CIF: A65327894")
                globals.report.drawString(55,745,"Avda de Galicia 101")
                globals.report.drawString(55,730,"Vigo - 36215 - España")
                globals.report.drawString(55,715,"Tlfo: 986 123 456")
                globals.report.drawString(55,700,"email:teis@mail.com")
                globals.report.line(50,800,160,800)
                globals.report.line(50,695,160,695)
                globals.report.line(50,800,50,695)
                globals.report.line(160,800,160,695)
 #data company
                globals.report.setFont("Helvetica", 8)
                globals.report.drawString(55,760,"CIF: A65327894")
                globals.report.drawString(55,745,"Avda de Galicia 101")
                globals.report.drawString(55,730,"Vigo - 36215 - España")
                globals.report.drawString(55,715,"Tlfo: 986 123 456")
                globals.report.drawString(55,700,"email:teis@mail.com")
                globals.report.line(50,800,160,800)
                globals.report.line(50,695,160,695)
                globals.report.line(50,800,50,695)
                globals.report.line(160,800,160,695)



            else:
                print("Cannot load image")
        except Exception as e:
            print(e)


    def reportCustomers(self):
        try:

            title = "List Client"
            self.footer(title)
            self.topreport(title)
            var = False
            records = Conexion.listTabCustomers(var)
            if not records:
                print("No Customers found")
                return
            items = ["DNI_NIE","SURNAME","NAME","MOBILE","CITY","INVOICE TYPE", "STATE"]
            globals.report.setFont("Helvetica-Bold",10)
            globals.report.drawString(45, 650, str(items[0]))
            globals.report.drawString(100, 650, str(items[1]))
            globals.report.drawString(185, 650, str(items[2]))
            globals.report.drawString(245, 650, str(items[3]))
            globals.report.drawString(330, 650, str(items[4]))
            globals.report.drawString(390, 650, str(items[5]))
            globals.report.drawString(480, 650, str(items[6]))
            globals.report.line(35, 645, 525, 645)
            x = 55
            y = 630
            for record in records:
                if y <=90:

                    globals.report.setFont("Helvetica-Bold",8)
                    globals.report.drawString(450,75,"Next Page...")
                    globals.report.showPage()#Crea una nueva imagen
                    self.footer(title)
                    self.topreport(title)
                    items = ["DNI_NIE", "SURNAME", "NAME", "MOBILE", "CITY", "INVOICE TYPE", "STATE"]
                    globals.report.setFont("Helvetica-Bold", 12)
                    globals.report.drawString(45, 650, str(items[0]))
                    globals.report.drawString(100, 650, str(items[1]))
                    globals.report.drawString(185, 650, str(items[2]))
                    globals.report.drawString(245, 650, str(items[3]))
                    globals.report.drawString(330, 650, str(items[4]))
                    globals.report.drawString(390, 650, str(items[5]))
                    globals.report.drawString(480, 650, str(items[6]))
                    globals.report.line(45, 645, 525, 645)
                    x = 55
                    y = 630
                globals.report.setFont("Helvetica", 8)
                dni = "****" + str(record[0][4:7] + "***")
                globals.report.drawCentredString(x + 10, y, dni)
                globals.report.drawString(x + 50, y, str(record[2]))
                globals.report.drawString(x + 130, y, str(record[3]))
                globals.report.drawCentredString(x + 210, y, str(record[5]))
                globals.report.drawString(x + 270, y, str(record[8]))
                globals.report.drawString(x + 350, y, str(record[9]))
                if str(record[10]) == "True":
                    globals.report.drawString(x+430,y,"Active")
                else:
                    globals.report.drawString(x+430,y,"Inactive")

                y = y - 25



            for file in os.listdir(self.rootPath):
                if file.endswith(self.namereportcli):
                    os.startfile(self.pdf_path)


        except Exception as e:
            print(e)

    @staticmethod
    def ticket(self=None):
        try:
            subtotal = 0.00
            iva = 0.00
            total = 0.00
            rootPath = ".\\reports"
            if not os.path.exists(rootPath):
                os.makedirs(rootPath)
            data = datetime.datetime.today().strftime("%Y_%m_%d_%H_%M_%S")
            ticket_name = data + "_ticket.pdf"
            pdf_path = os.path.abspath(os.path.join(rootPath, ticket_name))

            globals.report = canvas.Canvas(pdf_path)
            dni = globals.ui.txtDniFac.text()
            titulo = "FACTURA SIMPLIFICADA" if dni == "00000000T" else "FACTURA"

            records = Conexion.dataOneCustomer(dni)
            if records[0] != "00000000T":
                globals.report.setFont("Helvetica-Bold", 10)
                globals.report.drawString(280, 780, "Customer")
                globals.report.setFont("Helvetica", 9)
                globals.report.drawString(280, 765, "DNI: " + str(records[0]))
                globals.report.drawString(280, 750, "SURNAME: " + str(records[2]))
                globals.report.drawString(280, 735, "NAME: " + str(records[3]))
                globals.report.drawString(280, 720, "ADDRESS:  " + str(records[6]))
                globals.report.drawString(280, 705, "CITY: " + str(records[8]) + "  PROVINCE: " + str(records[7]))
            numfac = globals.ui.lblnumfac.text()
            globals.report.setFont("Helvetica-Bold", 10)
            globals.report.drawRightString(500, 675, "Nº  " + str(numfac))
            datafac = Conexion.datosFac(numfac)
            items = ["Cod", "Product", "Unit Price", "Amount", "Total"]
            globals.report.setFont("Helvetica-Bold", 10)
            globals.report.drawString(60, 650, str(items[0]))
            globals.report.drawString(145, 650, str(items[1]))
            globals.report.drawString(310, 650, str(items[2]))
            globals.report.drawString(390, 650, str(items[3]))
            globals.report.drawString(480, 650, str(items[4]))
            globals.report.line(35, 640, 525, 640)
            x = 55
            y = 630
            for record in datafac:
                globals.report.setFont("Helvetica", 8)
                globals.report.drawCentredString(x + 15, y, str(record[2]))
                globals.report.drawString(x + 90, y, str(record[3]))
                globals.report.drawCentredString(x + 280, y, str(record[4]))
                globals.report.drawCentredString(x + 355, y, str(record[5]))
                globals.report.drawRightString(x + 450, y, str(record[6]) + ' €')
                y = y - 15
                subtotal = round(float(record[6]) + subtotal, 2)
            globals.report.line(x + 200, y, x + 470, y)
            iva = round(subtotal * 0.21, 2)
            total = round(subtotal + iva, 2)
            y = y - 20
            globals.report.setFont("Helvetica-Bold", 8)
            globals.report.drawRightString(x + 450, y, "Subtotal: " + str(subtotal) + " €")
            globals.report.drawRightString(x + 450, y - 15, "IVA: " + str(iva) + " €")
            globals.report.drawRightString(x + 450, y - 35, "Total Payment: " + str(total) + " €")
            Reports.topreport(titulo)
            Reports.footer(titulo)
            globals.report.save()

            # otra forma de abrir sin necesidade comprobar
            try:
                os.startfile(pdf_path)
            except Exception as e:
                print("No se pudo abrir el PDF:", e)

        except Exception as error:
            print("error ticket", error)


