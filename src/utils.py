# Importaciones:
import pygame.time as time
from json import load
from src.configuraciones import alto_pantalla
from src.configuraciones import ancho_pantalla
from src.audio import audio

# Funcion para cargar los dialogos desde un archivo JSON
def cargar_dialogos(archivo_json):
    """ Carga los dialogos desde un archivo JSON."""

    with open(archivo_json, "r", encoding="utf-8") as archivo:
        return load(archivo)

# Funcion para textos:
def renderizar_texto_simple(pantalla, texto, fuente):
    """Configuracion de los textos tanto animacion como el posicionamiento"""

    lineas = texto.splitlines()
    y_pos = alto_pantalla // 2 - (len(lineas) * fuente.get_height()) // 2
    
    for linea in lineas:
        if linea.strip():
            render = fuente.render(linea, True, (255, 255, 255))
            x_pos = ancho_pantalla // 2 - render.get_width() // 2
            pantalla.blit(render, (x_pos, y_pos))
        y_pos += fuente.get_height()

# Reiniciar estado de variables:
def resetear_estado_texto(letras_mostradas, texto_completo, ultimo_tiempo):
        """Reinicia el estado de las variables para la animacion del texto"""

        letras_mostradas = 0
        texto_completo = False
        ultimo_tiempo = time.get_ticks()
        return letras_mostradas, texto_completo, ultimo_tiempo
