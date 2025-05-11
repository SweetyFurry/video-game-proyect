# Importaciones:
from pygame import mixer
from pygame import time
from pygame import USEREVENT
from pygame import event
from collections import defaultdict

# Clase SistemaAudio:
class SistemaAudio:
    """Clase para manejar la reproducción de música y efectos de sonido en Pygame."""

    # Inicializa el sistema de audio y establece la configuración predeterminada.
    def __init__(self):
        """Inicializa el sistema de audio y establece la configuración predeterminada."""

        # 44100: calidad estándar de audio, -16: audio de buena calidad,
        # 2: estéreo, 512: tamaño del búfer, menor da menos latencia
        mixer.init(frequency = 44100, size = -16,
                    channels = 2, buffer = 512)
        self.musica_actual = None
        self.volumen_musica_defecto = 0.3
        self.volumen_efectos_defecto = 0.5
        self.sonidos_cargados = {}
        self.efectos_en_curso = defaultdict(int)
        self.ultimo_efecto_por_tipo = {}

    # Carga un sonido y lo almacena en caché
    def cargar_sonido(self, ruta, tipo="efecto"):
        # Si la ruta esta ya cargada se salta el if, si no
        if ruta not in self.sonidos_cargados:
            # Se guarda el sonido en una variable
            sound = mixer.Sound(ruta)
            # Se guarda el sonido en un diccionario
            self.sonidos_cargados[ruta] = sound
            return sound
        return self.sonidos_cargados[ruta]

    # reproduce musica y crea un bucle infinito hasta que ya no exista el archivo
    def reproducir_musica(self, ruta, loops=-1):
        """ Reproduce música en un bucle infinito hasta que se detenga o cambie la pista."""

        # Si la musica es diferente a la ruta dada
        if self.musica_actual != ruta:
            # Se detiene la musica y carga esa nueva musica en los sonidos
            self.detener_musica()
            musica = self.cargar_sonido(ruta, tipo="musica")
            if musica:
                # Usamos la musica actual
                self.musica_actual = ruta
                musica.set_volume(self.volumen_musica_defecto)
                musica.play(loops=loops)

    # Reproduce un efecto de sonido solo si no está ya reproduciéndose
    def reproducir_efecto(self, ruta, tipo=None):
        """Reproduce un efecto de sonido solo si no está ya reproduciéndose."""

        # Si el efecto ya fue reproducido
        if tipo and tipo in self.ultimo_efecto_por_tipo:
            tiempo_actual = time.get_ticks()
            tiempo_transcurrido = tiempo_actual - self.ultimo_efecto_por_tipo[tipo]
            # Si no ha pasado medio segundo, entonces el sonido no se reproduce
            if tiempo_transcurrido <= 500:
                return False
        # carga y guarda el sonido en efecto
        efecto = self.cargar_sonido(ruta)
        if efecto:
            # Verificar si ya se está reproduciendo este efecto y si lo esta ignora el sonido
            if self.efectos_en_curso[ruta] > 0:
                return False
            self.efectos_en_curso[ruta] += 1
            # Si el tipo de efecto es igual, entonces se guarda el tiempo en el que se intento reproducir
            if tipo:
                self.ultimo_efecto_por_tipo[tipo] = time.get_ticks()
            
            # Limpia el efecto en curso para que se pueda volver a reproducir el sonido
            def limpiar():
                """Limpia el efecto en curso para que se pueda volver a reproducir el sonido."""

                self.efectos_en_curso[ruta] -= 1


            efecto.set_volume(self.volumen_efectos_defecto)
            canal = efecto.play()
            if canal:
                # detectan cuando un sonido ha terminado de reproducirse para realizar alguna accion
                canal.set_endevent(USEREVENT + len(self.efectos_en_curso))
                event.set_allowed(USEREVENT + len(self.efectos_en_curso))
                return True
        return False


    def detener_musica(self):
        """Detiene la música actual y la establece en None."""

        if self.musica_actual:
            mixer.stop()
            self.musica_actual = None


    def set_volumen_musica(self, volumen):
        """limita el valor de volumen entre 0.0 y 1.0 y guarda el volumen en defectos"""

        self.volumen_musica_defecto = max(0.0, min(1.0, volumen))
        # Si existe algun tipo de musica entonces baja el audio o lo deja igual
        if self.musica_actual:
            self.sonidos_cargados[self.musica_actual].set_volume(self.volumen_musica_defecto)


    def set_volumen_efectos(self, volumen):
        """limita el valor de volumen entre 0.0 y 1.0 y guarda el volumen en defectos"""

        self.volumen_efectos_defecto = max(0.0, min(1.0, volumen))

    # Maneja eventos de finalización de sonidos
    def actualizar(self, eventos):
        """Maneja eventos de finalización de sonidos y actualiza el estado de los efectos en curso."""
        
        for evento in eventos:
            if evento.type >= USEREVENT and evento.type < USEREVENT + 100:
                """Si ruta esta en efectos en curso..."""
                for ruta in self.efectos_en_curso:
                    """Y si el efecto ya fue reproducido"""
                    if self.efectos_en_curso[ruta] > 0:
                        self.efectos_en_curso[ruta] -= 1
                        break

#Sirve para llamar a toda la clase desde audio
audio = SistemaAudio()