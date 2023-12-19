import numpy as np

def saludar():
    print("Hola te saludo desde saludos.saludar()")

def prueba():
    print("Esto es una prueba")    

def generar_array(numeros):    
    return np.arange(numeros)

class Saludo:
    def __init__(self):
        print("Hola te saludo desde saludos __init__")


### __NAME == __MAIN__ SIRVE PARA PODER ESTABLECER QUE NO SE REPITA LA FUNCION 2 VECES 
if __name__ == '__main__':
    print(generar_array(5))