import unittest

import conexion
from conexion import Conexion

import globals
from PyQt6 import QtCore, QtGui, QtWidgets



class MyTest(unittest.TestCase):
    def test_connection(self):

        value = Conexion.db_conexion()
        msg = "Conexion no valida"
        self.assertEqual(value,msg)

    def test_pro(self):
        newpro = ["uvass","Food",10,1.99]
        result = conexion.Conexion.addPro(newpro)
        self.assertTrue(result)

if __name__ == '__main__':
    unittest.main()
