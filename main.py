from pygame import init
from pygame import quit
from pygame import display
from sys import exit
from src.configuraciones import ancho_pantalla
from src.configuraciones import alto_pantalla
from src.audio import audio
from src.menu_inicial import mostrar_menu_inicial
from src.sistema_guardado import cargar_partida
from src.escenas import bucle_dialogo

def main():
    """Iniciamos los modulos de pygame"""
    init()
    """configuramos los pixeles de la pantalla"""
    tamano_pantalla = display.set_mode((ancho_pantalla, alto_pantalla))
    """Colocamos el titulo a la ventana"""
    display.set_caption("Te estan viendo, bro")
    """Configurar el volumen de la musica y de los efectos"""
    audio.set_volumen_musica(0.2 )
    audio.set_volumen_efectos(1)
    while True:
        display.set_caption("Te estan viendo, bro")
        menu = mostrar_menu_inicial(tamano_pantalla)
        """Si el menu no carga correctamente entonces cierra el juego"""
        if menu is None:
            break
        """Si el jugador selecciona cargar partida, entonces..."""
        if menu == "cargar_partida":
            estado = cargar_partida()
            if estado:
                bucle_dialogo(tamano_pantalla, estado_guardado=estado)
            else:
                bucle_dialogo(tamano_pantalla)
        else:
            bucle_dialogo(tamano_pantalla)
    
    quit()
    exit()

if __name__ == "__main__":
    main()