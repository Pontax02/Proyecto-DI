
from PIL import Image
from reportlab.pdfgen import canvas
import os, datetime
from conexion import Conexion

class Reportproducts:
    def __init__(self):
        rootPath= ".\\reports"
        data = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
        self.namereportcli = data + "_reportproducts.pdf"
        self.pdf_path = os.path.join(rootPath, self.namereportcli)
        self.c = canvas.Canvas(self.pdf_path)
        self.rootPath = rootPath


    def footer(self,title):


        try:

            self.c.line(35,60,525,60)
            day = datetime.datetime.today()
            day = day.strftime("%d/%m/%Y %H:%M:%S")
            self.c.setFont("Helvetica", 7)
            self.c.drawString(70,50,day)
            self.c.drawString(250,50,title)
            self.c.drawString(500,50,str("Page: " +  str(self.c.getPageNumber())))

        except Exception as error:
            print(error)
    def topreport(self,title):
        try:
            path_logo= ".\\img\\omega.ico"
            logo = Image.open(path_logo)
            if isinstance(logo,Image.Image):

                self.c.setFont("Helvetica", 10)
                self.c.drawString(55,785,"EMPRESA TEIS")
                self.c.drawCentredString(300,675,title)
                self.c.line(35,665,525,665)
                self.c.drawImage(path_logo,480,745,40,40)
                #data company
                self.c.setFont("Helvetica", 8)
                self.c.drawString(55,760,"CIF: A65327894")
                self.c.drawString(55,745,"Avda de Galicia 101")
                self.c.drawString(55,730,"Vigo - 36215 - España")
                self.c.drawString(55,715,"Tlfo: 986 123 456")
                self.c.drawString(55,700,"email:teis@mail.com")
                self.c.line(50,800,160,800)
                self.c.line(50,695,160,695)
                self.c.line(50,800,50,695)
                self.c.line(160,800,160,695)



            else:
                print("Cannot load image")
        except Exception as e:
            print(e)


    def reportCustomers(self):
        try:

            title = "List Products"
            self.footer(title)
            self.topreport(title)

            records = Conexion.listTabProducts()
            if not records:
                print("No Products found")
                return
            items = ["DNI_NIE","SURNAME","NAME","MOBILE","CITY","INVOICE TYPE", "STATE"]
            self.c.setFont("Helvetica-Bold",10)
            self.c.drawString(45, 650, str(items[0]))
            self.c.drawString(100, 650, str(items[1]))
            self.c.drawString(185, 650, str(items[2]))
            self.c.drawString(245, 650, str(items[3]))
            self.c.drawString(330, 650, str(items[4]))
            self.c.drawString(390, 650, str(items[5]))
            self.c.drawString(480, 650, str(items[6]))
            self.c.line(35, 645, 525, 645)
            x = 55
            y = 630
            for record in records:
                if y <=90:

                    self.c.setFont("Helvetica-Bold",8)
                    self.c.drawString(450,75,"Next Page...")
                    self.c.showPage()#Crea una nueva imagen
                    self.footer(title)
                    self.topreport(title)
                    items = ["DNI_NIE", "SURNAME", "NAME", "MOBILE", "CITY", "INVOICE TYPE", "STATE"]
                    self.c.setFont("Helvetica-Bold", 12)
                    self.c.drawString(45, 650, str(items[0]))
                    self.c.drawString(100, 650, str(items[1]))
                    self.c.drawString(185, 650, str(items[2]))
                    self.c.drawString(245, 650, str(items[3]))
                    self.c.drawString(330, 650, str(items[4]))
                    self.c.drawString(390, 650, str(items[5]))
                    self.c.drawString(480, 650, str(items[6]))
                    self.c.line(45, 645, 525, 645)
                    x = 55
                    y = 630
                self.c.setFont("Helvetica", 8)
                dni = "****" + str(record[0][4:7] + "***")
                self.c.drawCentredString(x + 10, y, dni)
                self.c.drawString(x + 50, y, str(record[2]))
                self.c.drawString(x + 130, y, str(record[3]))
                self.c.drawCentredString(x + 210, y, str(record[5]))
                self.c.drawString(x + 270, y, str(record[8]))
                self.c.drawString(x + 350, y, str(record[9]))
                if str(record[10]) == "True":
                    self.c.drawString(x+430,y,"Active")
                else:
                    self.c.drawString(x+430,y,"Inactive")

                y = y - 25


            self.c.save()
            for file in os.listdir(self.rootPath):
                if file.endswith(self.namereportcli):
                    os.startfile(self.pdf_path)


        except Exception as e:
            print(e)
