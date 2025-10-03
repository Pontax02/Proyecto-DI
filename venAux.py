import events
import globals
from dlgAbout import Ui_dlgAbout
from dlgCalendar import *
from datetime import datetime
from dlgAbout import *

from events import *


class Calendar(QtWidgets.QDialog):
    def __init__(self):
        super(Calendar, self).__init__()
        globals.vencal = Ui_dlgCalendar()   #instanciar ventana
        globals.vencal.setupUi(self)  #instanciar ventana
        day = datetime.now().day
        month = datetime.now().month
        year = datetime.now().year

        globals.vencal.Calendar.setSelectedDate(QtCore.QDate(year, month, day))
        globals.vencal.Calendar.clicked.connect(events.Events.loadData)


class dlgAbout(QtWidgets.QDialog):
    def __init__(self):
        super(dlgAbout, self).__init__()
        globals.about = Ui_dlgAbout()
        globals.about.setupUi(self)
        globals.ui.btnCloseabout.clicked.connect(events.Events.closeabout)