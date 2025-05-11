# Importaciones:
from json import dump
from json import load
from os import path
from os import makedirs

# Funcion para guardar la partida:
def guardar_partida(datos, slot=1):
    """ Funcion para guardar la partida en un archivo JSON """

    #Si no existe una carpeta llamada partida guardada
    if not path.exists('partida_guardada'):
        # Entonces crea esa carpeta
        makedirs('partida_guardada')
    #Abre o crea el archivo guardado_1 escribe los datos dentro,
    #indent=2 da formato, ensure_ascii=False permite usar caracteres
    #como ñ, acentos, etc
    with open(f'partida_guardada/guardado_{slot}.json', 'w', encoding='utf-8') as f:
        dump(datos, f, indent=2, ensure_ascii=False)

# Funcion para cargar la partida:
def cargar_partida(slot=1):
    """ Funcion para cargar la partida desde un archivo JSON """
    ruta = f'partida_guardada/guardado_{slot}.json'
    if not path.exists(ruta):
        return None
    with open(ruta, 'r', encoding='utf-8') as f:
        return load(f)