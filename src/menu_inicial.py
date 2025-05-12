# Importaciones:
from pygame import font
from pygame import mouse
from pygame import event
from pygame import QUIT
from pygame import quit
from pygame import MOUSEBUTTONDOWN
from pygame import display
from sys import exit
from src.configuraciones import ancho_pantalla
from src.configuraciones import alto_pantalla
from src.configuraciones import fuente_letras
from src.botones import Boton
from src.carga_imagenes import cargar_imagen

# Configuracion del menu inicial
def mostrar_menu_inicial(pantalla):
    """Muestra el menú inicial del juego y maneja la interacción del usuario."""
    
    fuente_titulo = font.Font(fuente_letras, 50)

    boton_nueva_partida = Boton(
        posicion_x = ancho_pantalla // 2 - 255, posicion_y = alto_pantalla // 2 - 100,
        ancho = 500, alto = 50,
        texto = "Iniciar nueva partida",
        color_normal = (80, 80, 80, 200),
        color_hover = (120, 120, 120, 200)
        )

    boton_cargar_partida = Boton(
        posicion_x = ancho_pantalla // 2 - 255, posicion_y = alto_pantalla //2,
        ancho = 500, alto = 50,
        texto = "Cargar partida",
        color_normal = (80, 80, 80, 200),
        color_hover = (120, 120, 120, 200)
        )

    while True:
        imagen_fondo = cargar_imagen("assets/fondos/fondo_cuarto_2.jpg", (ancho_pantalla, alto_pantalla))
        pantalla.blit(imagen_fondo, (0, 0))
        titulo = fuente_titulo.render("Te estan viendo, bro", True, (255, 255, 255))
        pantalla.blit(titulo, (ancho_pantalla//2 - titulo.get_width()//2, 100))
        posicion_mouse = mouse.get_pos()
        """Verifica si el mouse esta encima de algun boton y si si, lo hace true"""
        boton_nueva_partida.hover = boton_nueva_partida.rect.collidepoint(posicion_mouse)
        boton_cargar_partida.hover = boton_cargar_partida.rect.collidepoint(posicion_mouse)
        if boton_nueva_partida.hover:
            boton_nueva_partida.color_actual = boton_nueva_partida.color_hover
        else:
            boton_nueva_partida.color_actual = boton_nueva_partida.color_normal

        if boton_cargar_partida.hover:
            boton_cargar_partida.color_actual = boton_cargar_partida.color_hover
        else:
            boton_cargar_partida.color_actual = boton_cargar_partida.color_normal
        boton_nueva_partida.dibujar(pantalla)
        boton_cargar_partida.dibujar(pantalla)
        for evento in event.get():
            if evento.type == QUIT:
                quit()
                exit()
            if evento.type == MOUSEBUTTONDOWN and evento.button == 1:
                if boton_nueva_partida.hover:
                    return "nueva_partida"
                elif boton_cargar_partida.hover:
                    return "cargar_partida"
        
        display.flip()