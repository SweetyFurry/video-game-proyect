# Documentación Técnica del Proyecto Video Game

## 1. Análisis de Clases y Módulos

### 1.1 Clase Boton (src/botones.py)
**Propósito:** Implementa un sistema de botones interactivos con efectos visuales y sonoros.

#### Atributos:
- `rect` (Rect): Rectángulo que define el área del botón
- `texto` (str): Texto a mostrar en el botón
- `color_normal` (tuple): Color RGBA del botón en estado normal
- `color_hover` (tuple): Color RGBA del botón al pasar el mouse
- `color_actual` (tuple): Color RGBA actual del botón
- `fuente` (Font): Fuente para el texto del botón
- `mouse_en_boton` (bool): Estado de hover del mouse
- `degradado_borde` (int): Tamaño del degradado en los bordes
- `accion` (function): Función a ejecutar al hacer clic
- `tiempo_ultimo_clic` (int): Control de tiempo entre clics
- `escala` (float): Factor de escala del botón
- `sonido_clic` (str): Ruta al archivo de sonido del clic

#### Métodos:
1. `__init__(self, posicion_x, posicion_y, ancho, alto, texto, color_normal, color_hover, tamano_texto)`
   - Constructor que inicializa un nuevo botón
   - **Parámetros:**
     * `posicion_x, posicion_y`: Coordenadas de posición
     * `ancho, alto`: Dimensiones del botón
     * `texto`: Texto a mostrar
     * `color_normal`: Color base (RGBA)
     * `color_hover`: Color al pasar mouse (RGBA)
     * `tamano_texto`: Tamaño de la fuente

2. `dibujar(self, superficie)`
   - Renderiza el botón en la superficie especificada
   - Implementa efectos de transparencia y degradado
   - Centra el texto en el botón
   - **Maneja dos modos de renderizado:**
     * Modo transparente (alpha = 0)
     * Modo con degradado y color

3. `manejar_evento(self, evento)`
   - Procesa eventos del mouse
   - **Maneja:**
     * `MOUSEMOTION`: Actualiza estado hover
     * `MOUSEBUTTONDOWN`: Ejecuta acción si corresponde
   - Retorna `True` si se procesó un clic válido

4. `asignar_accion(self, funcion)`
   - Asigna la función a ejecutar al hacer clic
   - **Parámetro:**
     * `funcion`: Función callback a ejecutar

## 2. Sistema de Audio (src/audio.py)
**Propósito:** Gestiona la reproducción de audio del juego.

### Componentes:
- Control de volumen para música y efectos
- Sistema de reproducción de efectos de sonido
- Gestión de música de fondo

## 3. Sistema de Escenas (src/escenas.py)
**Propósito:** Maneja las diferentes escenas y estados del juego.

### Características:
- Sistema de transición entre escenas
- Gestión de diálogos
- Control de estados del juego

## 4. Sistema de Guardado (src/sistema_guardado.py)
**Propósito:** Implementa la persistencia de datos del juego.

### Funcionalidades:
- Guardado de progreso
- Carga de partidas
- Almacenamiento en JSON

## 5. Configuraciones (src/configuraciones.py)
**Propósito:** Centraliza las configuraciones del juego.

### Variables:
- `ancho_pantalla`: Ancho de la ventana del juego
- `alto_pantalla`: Alto de la ventana del juego
- `fuente_letras`: Ruta a la fuente del juego

## 6. Patrones de Diseño Implementados

### 6.1 Patrón Observer
- Implementado en el sistema de eventos de botones
- Permite desacoplamiento entre UI y lógica

### 6.2 Patrón Singleton
- Utilizado en el sistema de audio
- Asegura una única instancia de control de audio

### 6.3 Patrón State
- Implementado en el sistema de escenas
- Maneja diferentes estados del juego

## 7. Consideraciones de Implementación

### 7.1 Optimización de Rendimiento
- Uso de superficies transparentes para efectos visuales
- Cálculo eficiente de degradados
- Gestión de memoria en renderizado

### 7.2 Manejo de Eventos
- Sistema de eventos de Pygame
- Procesamiento eficiente de input
- Control de estados de UI

### 7.3 Gestión de Recursos
- Carga dinámica de recursos
- Sistema de caché para optimización
- Manejo de memoria para recursos gráficos

## 8. Variables y Constantes Importantes

### 8.1 Configuración de Pantalla
- `ancho_pantalla`: Define el ancho de la ventana
- `alto_pantalla`: Define el alto de la ventana

### 8.2 Configuración de Audio
- `volumen_musica`: Control de volumen de música
- `volumen_efectos`: Control de volumen de efectos

### 8.3 Configuración de UI
- `tamano_texto`: Tamaño base de texto
- `color_normal`: Color base de botones
- `color_hover`: Color de hover de botones

## 9. Flujo de Ejecución

### 9.1 Inicialización
1. Carga de configuraciones
2. Inicialización de Pygame
3. Configuración de ventana
4. Carga de recursos

### 9.2 Bucle Principal
1. Procesamiento de eventos
2. Actualización de estado
3. Renderizado
4. Control de FPS

## 10. Dependencias Externas

### 10.1 Pygame
- **Versión:** Última estable
- **Módulos utilizados:**
  * `pygame.display`
  * `pygame.event`
  * `pygame.font`
  * `pygame.surface`
  * `pygame.rect`

### 10.2 Sistema de Archivos
- **Requisitos:**
  * Permisos de lectura/escritura
  * Estructura de directorios específica

---
