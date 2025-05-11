# Importaciones:
from pygame import Rect
from pygame import font
from pygame import Surface
from pygame import SRCALPHA
from pygame import draw
from pygame import MOUSEMOTION
from pygame import MOUSEBUTTONDOWN
from src.configuraciones import fuente_letras
from src.audio import audio

class Boton:

    # Se declara el constructor para crear un boton
    def __init__(self, posicion_x, posicion_y, ancho,
                alto, texto,
                color_normal = (80, 80, 80, 200),
                color_hover = (120, 120, 120, 200),
                tamano_texto = 25):
        """ Constructor de la clase Boton."""

        # Se crea un rectangulo con la posicion, ancho y alto que le damos"""
        self.rect = Rect(posicion_x, posicion_y, ancho, alto)
        self.texto = texto
        self.color_normal = color_normal
        self.color_hover = color_hover
        self.color_actual = color_normal
        self.fuente = font.Font(fuente_letras, tamano_texto)
        self.mouse_en_boton = False
        # se calcula el degradado de los bordes para que se vean proporcionales
        self.degradado_borde = int(ancho * 0.3)
        self.accion = None
        self.tiempo_ultimo_clic = 0
        self.escala = 1.0
        self.sonido_clic = "assets/sonidos/efectos_sonidos/click.wav"


    def dibujar(self, superficie):
        """ Dibuja el botón en la superficie dada. """

        # Si el boton es completamente transparente
        if self.color_actual[3] == 0:
            # Se renderiza el texto con la fuente y color blanco
            texto_render = self.fuente.render(self.texto, True, (255, 255, 255))
            # genera un rectangulo del tamaño del texto y lo centra
            tamanio_rectangulo = texto_render.get_rect(center = self.rect.center)
            # Pinta el texto en la superficie de la posicion del rectangulo invisible"""
            superficie.blit(texto_render, tamanio_rectangulo)
        else:
            # Se crea una superficie transparente del tamaño del boton
            superficie_transparente = Surface((self.rect.width, self.rect.height), SRCALPHA)
            # Se recorre el ancho del boton desde 0 px hasta x px
            for i in range(self.rect.width):
                # se guarda la transparencia del color
                color_alfa = self.color_actual[3]
                if i < self.degradado_borde:
                    # se calcula el degradado del borde izquierdo para que se vean proporcionales de izquierda a derecha
                    color_alfa = int(color_alfa * (i / self.degradado_borde))
                elif i > self.rect.width - self.degradado_borde:
                    # Hace lo mismo que el codigo de arriba, pero en sentido contrario
                    color_alfa = int(color_alfa * ((self.rect.width - i) / self.degradado_borde))
                # Se dibuja una linea vertical en la superficie transparente con el color y la transparencia calculada
                draw.line(superficie_transparente, (*self.color_actual[:3], color_alfa), (i, 0), (i, self.rect.height))
            # Pinta el texto en la superficie de la posicion del rectangulo
            texto_render = self.fuente.render(self.texto, True, (255, 255, 255))
            # Pinta el texto en el centro del rectangulo
            tamanio_rectangulo = texto_render.get_rect(center = (self.rect.width // 2, self.rect.height // 2))
            # Pinta el texto en la superficie de la posicion del rectangulo y centrado
            superficie_transparente.blit(texto_render, tamanio_rectangulo)
            # Pinta la superficie con el cuadro transparente y con el tamanio de x y y, para pegar todo ya
            superficie.blit(superficie_transparente, self.rect.topleft)

    # Controla el evento del mouse
    def manejar_evento(self, evento):
        """ Maneja los eventos del mouse para el botón. """

        # Detecta el movimiento del mouse
        if evento.type == MOUSEMOTION:
            # Verifica si el mouse esta encima del boton y si si, es true"""
            self.mouse_en_boton = self.rect.collidepoint(evento.pos)
            if self.mouse_en_boton:
                self.color_actual = self.color_hover
            else:
                self.color_actual = self.color_normal
        # Detecta el movimiento del mouse y si dio click izquierdo
        if evento.type == MOUSEBUTTONDOWN and evento.button == 1:
            # Si el mouse esta sobre el raton y hay una accion
            if self.mouse_en_boton and self.accion:
                # Reproduce el sonido de clic
                audio.reproducir_efecto(self.sonido_clic)
                # Realiza la accion
                self.accion()
                return True
        return False

    # Asigna una funcion a la accion del boton
    def asignar_accion(self, funcion):
        self.accion = funcion