import pygame.time as time
from json import load
from src.configuraciones import alto_pantalla
from src.configuraciones import ancho_pantalla
from src.audio import audio


def cargar_dialogos(archivo_json):
    with open(archivo_json, "r", encoding="utf-8") as archivo:
        return load(archivo)


def renderizar_texto_simple(pantalla, texto, fuente):
    lineas = texto.splitlines()
    y_pos = alto_pantalla // 2 - (len(lineas) * fuente.get_height()) // 2
    
    for linea in lineas:
        if linea.strip():
            render = fuente.render(linea, True, (255, 255, 255))
            x_pos = ancho_pantalla // 2 - render.get_width() // 2
            pantalla.blit(render, (x_pos, y_pos))
        y_pos += fuente.get_height()


def resetear_estado_texto(letras_mostradas, texto_completo, ultimo_tiempo):
        letras_mostradas = 0
        texto_completo = False
        ultimo_tiempo = time.get_ticks()
        return letras_mostradas, texto_completo, ultimo_tiempo


def retroceder_dialogo(indice_dialogo, dialogos, archivo_json, texto_total,
                       letras_mostradas, texto_completo, ultimo_tiempo,
                       historial, hay_opciones, botones_opciones,
                       tiene_opciones_pendientes, dialogo_tiene_opciones,
                       musica_actual):
    if indice_dialogo > 0:
        indice_dialogo -= 1
        texto_total = dialogos[indice_dialogo]['texto']
        letras_mostradas, texto_completo, ultimo_tiempo = resetear_estado_texto(
            letras_mostradas, texto_completo, ultimo_tiempo)
        hay_opciones = False
        tiene_opciones_pendientes = False
        dialogo_tiene_opciones = False
        botones_opciones.clear()
        
        nueva_musica = dialogos[indice_dialogo].get("musica_fondo", None)
        if nueva_musica != musica_actual:
            musica_actual = nueva_musica
            if musica_actual:
                audio.reproducir_musica(musica_actual)
            else:
                audio.detener_musica()
        
        if historial and historial[-1]['archivo'] == archivo_json:
            historial.pop()
        return True, indice_dialogo, dialogos, archivo_json, texto_total, \
               letras_mostradas, texto_completo, ultimo_tiempo, historial, \
               hay_opciones, botones_opciones, tiene_opciones_pendientes, \
               dialogo_tiene_opciones, musica_actual

    elif historial:
        estado_anterior = historial.pop()
        archivo_json = estado_anterior['archivo']
        dialogos = cargar_dialogos(archivo_json)
        
        indice_dialogo = len(dialogos) - 1
        texto_total = dialogos[indice_dialogo]['texto']
        letras_mostradas, texto_completo, ultimo_tiempo = resetear_estado_texto(
            letras_mostradas, texto_completo, ultimo_tiempo)
        hay_opciones = False
        tiene_opciones_pendientes = False
        dialogo_tiene_opciones = False
        botones_opciones.clear()
        
        nueva_musica = dialogos[indice_dialogo].get("musica_fondo", None)
        if nueva_musica != musica_actual:
            musica_actual = nueva_musica
            if musica_actual:
                audio.reproducir_musica(musica_actual)
            else:
                audio.detener_musica()
        
        return True, indice_dialogo, dialogos, archivo_json, texto_total, \
               letras_mostradas, texto_completo, ultimo_tiempo, historial, \
               hay_opciones, botones_opciones, tiene_opciones_pendientes, \
               dialogo_tiene_opciones, musica_actual

    return False, indice_dialogo, dialogos, archivo_json, texto_total, \
           letras_mostradas, texto_completo, ultimo_tiempo, historial, \
           hay_opciones, botones_opciones, tiene_opciones_pendientes, \
           dialogo_tiene_opciones, musica_actual
