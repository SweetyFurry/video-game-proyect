# Importaciones
from pygame import event
from pygame import display
from pygame import font
from pygame import Surface
from pygame import draw
from pygame import time
from pygame import QUIT
from pygame import KEYDOWN
from pygame import K_SPACE
from pygame import SRCALPHA
from pygame import MOUSEBUTTONDOWN
from pygame import MOUSEMOTION
from json import load
from src.configuraciones import fuente_letras
from src.configuraciones import alto_pantalla
from src.configuraciones import ancho_pantalla
from src.carga_imagenes import cargar_imagen
from src.botones import Boton
from src.audio import audio
from src.sistema_guardado import guardar_partida
from src.utils import cargar_dialogos
from src.utils import renderizar_texto_simple
from src.utils import resetear_estado_texto

# Funcion principal del bucle de dialogo:
def bucle_dialogo(pantalla, archivo_json="jsons/parte_1.json", estado_guardado=None):
    """Bucle principal del diálogo que organiza los json, contiene configuracion de los botones
    y mantiene la logica de las escenas"""

    if estado_guardado:
        dialogos = cargar_dialogos(estado_guardado['archivo_actual'])
        indice_dialogo = estado_guardado['dialogo_actual']
        texto_completo = estado_guardado['texto_completo']
        letras_mostradas = estado_guardado.get('letras_mostradas', 0)
        texto_total = estado_guardado.get('texto_total', "")
        ultimo_tiempo = estado_guardado.get('ultimo_tiempo', time.get_ticks())
        historial = estado_guardado.get('historial', [])
        musica_actual = estado_guardado.get('musica_actual', None)
    else:
        dialogos = cargar_dialogos(archivo_json)
        indice_dialogo = 0
        texto_completo = False
        letras_mostradas = 0
        texto_total = ""
        ultimo_tiempo = time.get_ticks()
        historial = []
        musica_actual = None
    
    fuente_dialogo = font.Font(fuente_letras, 20)
    fuente_narrador = font.Font(fuente_letras, 24)
    fuente_nombre = font.Font(fuente_letras, 33)
    fondo_actual = None
    fondo_img = None
    reloj = time.Clock()
    corriendo = True
    botones_opciones = []
    hay_opciones = False
    tiene_opciones_pendientes = False
    dialogo_tiene_opciones = False

    if musica_actual:
        audio.reproducir_musica(musica_actual)

    # Creacion de botones:
    boton_guardar = Boton(ancho_pantalla - 105, 5, 100, 30, "Guardar",
                        (0, 0, 0, 0), (0, 204, 35, 30), 20)

    boton_salir = Boton(5, 5, 70, 30, "Salir",
                        (0, 0, 0, 0), (200, 50, 50, 50), 20)

    boton_anterior = Boton(ancho_pantalla // 2 - 150, 5,
                            100, 30, "Anterior", (0, 0, 0, 0),
                            (0, 0, 0, 0), 20)

    boton_siguiente = Boton(ancho_pantalla // 2 + 50, 5,
                            100, 30, "Siguiente", (0, 0, 0, 0),
                            (0, 0, 0, 0), 20)

    # Reiniciar el estado de las variables para la animacion del texto
    letras_mostradas, texto_completo, ultimo_tiempo = resetear_estado_texto(
        letras_mostradas, texto_completo, ultimo_tiempo
    )

    # Funcion para guardar el progreso actual:
    def guardar_progreso():
        """Guarda el progreso actual en un archivo JSON"""

        estado = {
            'archivo_actual': archivo_json,
            'dialogo_actual': indice_dialogo,
            'texto_completo': texto_completo,
            'letras_mostradas': letras_mostradas,
            'texto_total': texto_total,
            'ultimo_tiempo': ultimo_tiempo,
            'historial': historial,
            'musica_actual': musica_actual
        }
        guardar_partida(estado)

    # Funcion para retroceder en el dialogo:
    def retroceder_dialogo():
        """Retrocede al dialogo anterior, si existe"""

        nonlocal indice_dialogo, dialogos, archivo_json, texto_total,\
                letras_mostradas, texto_completo, ultimo_tiempo,\
                historial, hay_opciones, botones_opciones,\
                tiene_opciones_pendientes, dialogo_tiene_opciones,\
                musica_actual
        
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
            return True
        
        # Si no hay dialogo anterior, retroceder al anterior estado guardado
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
            
            return True
        
        return False

    # Funcion para avanzar en el dialogo:
    def avanzar_dialogo(nuevo_archivo=None):
        """Avanza al siguiente dialogo, si existe"""

        nonlocal indice_dialogo, texto_completo, letras_mostradas,\
                ultimo_tiempo, dialogos, archivo_json, corriendo,\
                hay_opciones, botones_opciones, historial,\
                tiene_opciones_pendientes, dialogo_tiene_opciones,\
                musica_actual
        
        # Si hay opciones pendientes, no se puede avanzar
        historial.append({
            'archivo': archivo_json,
            'indice': indice_dialogo,
            'texto': texto_total,
            'tiene_opciones': dialogo_tiene_opciones,
            'musica_fondo': musica_actual
        })
            
        if nuevo_archivo:
            try:
                dialogos = cargar_dialogos(nuevo_archivo)
                archivo_json = nuevo_archivo
                indice_dialogo = 0
                hay_opciones = False
                tiene_opciones_pendientes = False
                dialogo_tiene_opciones = False
                botones_opciones.clear()
            except FileNotFoundError:
                corriendo = False
        else:
            indice_dialogo += 1
        
        letras_mostradas, texto_completo, ultimo_tiempo = resetear_estado_texto(
        letras_mostradas, texto_completo, ultimo_tiempo)
        
        if indice_dialogo >= len(dialogos):
            corriendo = False

    # Asignar acciones a los botones:
    boton_guardar.asignar_accion(guardar_progreso)
    boton_salir.asignar_accion(lambda: None)
    boton_anterior.asignar_accion(retroceder_dialogo)
    boton_siguiente.asignar_accion(lambda: avanzar_dialogo())

    # Bucle principal del dialogo:
    while corriendo:
        eventos = event.get()
        
        for e in eventos:
            if e.type == QUIT:
                corriendo = False
                
            if e.type == KEYDOWN and e.key == K_SPACE:
                if dialogo_tiene_opciones:
                    if not texto_completo:
                        letras_mostradas = len(texto_total)
                        texto_completo = True
                else:
                    if not texto_completo:
                        letras_mostradas = len(texto_total)
                        texto_completo = True
                    else:
                        avanzar_dialogo()
                continue
                
            if e.type == MOUSEBUTTONDOWN and e.button == 1:
                if boton_salir.rect.collidepoint(e.pos):
                    corriendo = False
                    
                if boton_anterior.rect.collidepoint(e.pos):
                    boton_anterior.accion()
                    
                if boton_siguiente.rect.collidepoint(e.pos):
                    if not dialogo_tiene_opciones or (texto_completo and not tiene_opciones_pendientes):
                        avanzar_dialogo()
                    
                if boton_guardar.rect.collidepoint(e.pos):
                    boton_guardar.accion()
                
                for boton in botones_opciones:
                    if boton.rect.collidepoint(e.pos):
                        boton.accion()
                        break
            
            # Cambiar el color del boton al pasar el mouse por encima
            if e.type == MOUSEMOTION:
                boton_anterior.hover = boton_anterior.rect.collidepoint(e.pos)
                if boton_anterior.hover:
                    boton_anterior.color_actual = boton_anterior.color_hover
                else: 
                    boton_anterior.color_actual = boton_anterior.color_normal
                
                puede_avanzar = not dialogo_tiene_opciones or (texto_completo and not tiene_opciones_pendientes)
                boton_siguiente.hover = boton_siguiente.rect.collidepoint(e.pos) and puede_avanzar
                if (boton_siguiente.hover and puede_avanzar):
                    boton_siguiente.color_actual = boton_siguiente.color_hover
                elif (dialogo_tiene_opciones and not texto_completo): 
                    boton_siguiente.color_actual = (100, 100, 100, 100) 
                else: 
                    boton_siguiente.color_actual = boton_siguiente.color_normal
                
                boton_guardar.hover = boton_guardar.rect.collidepoint(e.pos)
                if boton_guardar.hover:
                    boton_guardar.color_actual = boton_guardar.color_hover
                else:
                    boton_guardar.color_actual = boton_guardar.color_normal
                
                boton_salir.hover = boton_salir.rect.collidepoint(e.pos)
                if boton_salir.hover:
                    boton_salir.color_actual = boton_salir.color_hover
                else:
                    boton_salir.color_actual = boton_salir.color_normal
                
                for boton in botones_opciones:
                    boton.hover = boton.rect.collidepoint(e.pos)
                    if boton.hover:
                        boton.color_actual = boton.color_hover
                    else:
                        boton.color_actual = boton.color_normal

        pantalla.fill((0, 0, 0))
        
        # Si hay un fondo de pantalla, dibujarlo
        if indice_dialogo < len(dialogos):
            entrada = dialogos[indice_dialogo]
            texto_total = entrada["texto"]
            
            nueva_musica = entrada.get("musica_fondo", None)
            if nueva_musica != musica_actual:
                musica_actual = nueva_musica
                if musica_actual:
                    audio.reproducir_musica(musica_actual)
                else:
                    audio.detener_musica()
            
            # Si hay un efecto de sonido, reproducirlo
            efecto_sonido = entrada.get("efecto_sonido", None)
            tipo_efecto = entrada.get("tipo_efecto", efecto_sonido)
            if efecto_sonido and letras_mostradas == 0:
                audio.reproducir_efecto(efecto_sonido, tipo=tipo_efecto)
            
            dialogo_tiene_opciones = "opciones" in entrada
            
            # Si hay un fondo de pantalla, cargarlo
            nuevo_fondo = entrada.get("fondo", "")
            if nuevo_fondo and (fondo_actual != nuevo_fondo or fondo_img is None):
                try:
                    fondo_img = cargar_imagen(nuevo_fondo, (ancho_pantalla, alto_pantalla))
                    fondo_actual = nuevo_fondo
                except Exception as e:
                    fondo_img = None
            
            if fondo_img:
                pantalla.blit(fondo_img, (0, 0))

            if entrada.get("narrador", False):
                if not texto_completo:
                    tiempo_actual = time.get_ticks()
                    if tiempo_actual - ultimo_tiempo >= 30:
                        letras_mostradas += 1
                        ultimo_tiempo = tiempo_actual
                    if letras_mostradas >= len(texto_total):
                        texto_completo = True
                
                renderizar_texto_simple(pantalla, texto_total[:letras_mostradas], fuente_narrador)
                
                # Si el texto se ha completado y hay opciones, mostrarlas
                if texto_completo and dialogo_tiene_opciones and not botones_opciones:
                    tiene_opciones_pendientes = True
                    hay_opciones = True
                    y_pos = 200
                    for opcion in entrada["opciones"]:
                        nuevo_boton = Boton(135, y_pos,
                                            1000, 40, opcion["texto"],
                                            (0, 0, 0, 180),
                                            (156, 156, 156, 220))
                        nuevo_boton.asignar_accion(lambda arch=opcion["archivo"]: avanzar_dialogo(arch))
                        botones_opciones.append(nuevo_boton)
                        y_pos += 70
            else:
                if "imagen_personaje" in entrada and entrada["imagen_personaje"]:
                    lado = entrada.get("lado_personaje")
                    if lado == "izquierda":
                        pos_x = 10 
                    else:
                        pos_x = 550
                    pantalla.blit(cargar_imagen(entrada["imagen_personaje"]), (pos_x, 0))

                caja_texto = Surface((1000, 110), SRCALPHA)
                draw.rect(caja_texto, (255, 255, 255), (0, 0, 1000, 110), border_radius=7)
                draw.rect(caja_texto, (0, 0, 0, 160), (2, 2, 996, 106), border_radius=5)

                # Animar el texto
                if not texto_completo:
                    tiempo_actual = time.get_ticks()
                    if tiempo_actual - ultimo_tiempo >= 30:
                        letras_mostradas += 1
                        ultimo_tiempo = tiempo_actual
                    if letras_mostradas >= len(texto_total):
                        texto_completo = True

                texto_parcial = texto_total[:letras_mostradas]
                lineas = texto_parcial.splitlines()
                y_texto = 20
                for linea in lineas:
                    render = fuente_dialogo.render(linea, True, (255, 255, 255))
                    caja_texto.blit(render, (30, y_texto))
                    y_texto += 28
                pantalla.blit(caja_texto, (135, 600))

                if "personaje" in entrada and entrada["personaje"]:
                    nombre = fuente_nombre.render(entrada["personaje"], True, (255, 255, 255))
                    if entrada.get("lado_personaje", "izquierda") == "izquierda":
                        lado_nombre = 1022
                    else: 
                        lado_nombre = 150
                    pantalla.blit(nombre, (lado_nombre, 560))

                if texto_completo and dialogo_tiene_opciones and not botones_opciones:
                    tiene_opciones_pendientes = True
                    hay_opciones = True
                    y_pos = 200
                    for opcion in entrada["opciones"]:
                        nuevo_boton = Boton(135, y_pos,
                                            1000, 40, opcion["texto"],
                                            (0, 0, 0, 180),
                                            (156, 156, 156, 220))
                        nuevo_boton.asignar_accion(lambda arch=opcion["archivo"]: avanzar_dialogo(arch))
                        botones_opciones.append(nuevo_boton)
                        y_pos += 70

        # Si no hay opciones, limpiar la lista de botones
        boton_guardar.dibujar(pantalla)
        boton_salir.dibujar(pantalla)
        boton_anterior.dibujar(pantalla)
        
        puede_avanzar = not dialogo_tiene_opciones or (texto_completo and not tiene_opciones_pendientes)
        color_original_normal = boton_siguiente.color_normal
        color_original_hover = boton_siguiente.color_hover
        
        if not puede_avanzar:
            boton_siguiente.color_normal = (100, 100, 100, 100)
            boton_siguiente.color_hover = (100, 100, 100, 100)
        
        # Dibujar el boton de siguiente
        boton_siguiente.dibujar(pantalla)
        boton_siguiente.color_normal = color_original_normal
        boton_siguiente.color_hover = color_original_hover
        
        for boton in botones_opciones:
            boton.dibujar(pantalla)
        
        if entrada.get("pregunta"):
            display.set_caption(entrada.get("pregunta"))
        else:
            display.set_caption("Te estan viendo, bro")

        display.flip()
        reloj.tick(30)
    
    audio.detener_musica()