

from PIL import Image
from reportlab.pdfgen import canvas
import os, datetime

import conexion
import globals
import globals
from conexion import Conexion

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


    def footer(self,title):


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
    def topreport(self,title):
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


            globals.report.save()
            for file in os.listdir(self.rootPath):
                if file.endswith(self.namereportcli):
                    os.startfile(self.pdf_path)


        except Exception as e:
            print(e)

    def ticket(self):
        try:
            dni = globals.ui.txtDniFac.text()

            if dni == "00000000T":
                titulo = "FACTURA SIMPLIFICADA"
            else:
                titulo = "FACTURA"

            records = conexion.Conexion.dataOneCustomer(dni)
            globals.report.setFont("Helvetica-Bold", 10)
            globals.report.drawString(220, 700, "DNI: " + str(records[0]))
            globals.report.drawString(220, 685, "Apellidos: " + str(records[1]))
            globals.report.drawString(220, 670, "NOMBRE: " + str(records[3]))
            globals.report.drawString(220, 655, "DIRECCION: " + str(records[6]))
            globals.report.drawString(220, 640, "LOCALIDAD" + str(records[8]) + "PROVINCIA: " + str(records[7]))



            self.footer(titulo)
            self.topreport(titulo)
            globals.report.save()
            for file in os.listdir(self.rootPath):
                if file.endswith(self.ticket_path):
                    os.startfile(self.pdf_path)

        except Exception as e:
            print("error in ticket", e)