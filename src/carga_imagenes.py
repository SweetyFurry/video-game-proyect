# Importaciones:
from pygame import image
from pygame import transform

# Cargamos las imágenes una sola vez y las almacenamos en un diccionario
imagenes_cargadas = {}

# Las imagenes que se redimensionan son solo las que pasamos como argumento su ancho y alto (tamaño)
def cargar_imagen(ruta, tamaño=None):
    """Carga una imagen desde la ruta especificada y la redimensiona si se proporciona un tamaño."""
    clave = (ruta, tamaño)
    """Si la imagen no ha sido cargada..."""
    if clave not in imagenes_cargadas:
        """y si la imagen termina en .png, la cargamos con convert_alpha()"""
        if ruta.endswith('.png'):
            img = image.load(ruta).convert_alpha()
        else:
            """si no, la cargamos con convert()"""
            img = image.load(ruta).convert()
        if tamaño:
            """si se proporciona un tamaño, la redimensionamos"""
            img = transform.scale(img, tamaño)
        """Se almacena la imagen ya cargada"""
        imagenes_cargadas[clave] = img
    return imagenes_cargadas[clave]