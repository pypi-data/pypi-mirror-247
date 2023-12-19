### FROM SIRVE PARA TRAER UNA FUNCION O ALGO DE OTRO LADO , E IMPORT ES EL NOMBRE DE LA FUNCION 
import numpy as np
import unittest
from Mensajes.subpaquete.saludos import generar_array


class PruebasHola(unittest.TestCase):
    def test_generar_array(self):
        np.testing.assert_array_equal(
            np.array([0,1,2,3,4,5]),
            generar_array(6)
        )