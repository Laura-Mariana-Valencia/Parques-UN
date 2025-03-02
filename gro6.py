from collections import defaultdict
import random
import pygame

# Inicializar Pygame
pygame.init()

# Cargar imagen del tablero
tablero_img = pygame.image.load("parques.png")
width, height = tablero_img.get_size()

# Establecer el tamaño deseado (70% del tamaño original)
scaled_width = int(width * 0.7)
scaled_height = int(height * 0.7)

# Escalar la imagen
tablero_img = pygame.transform.scale(tablero_img, (scaled_width, scaled_height))

# Configurar pantalla
screen = pygame.display.set_mode((scaled_width, scaled_height))
screen.blit(tablero_img, (0, 0))
pygame.display.flip()

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 182, 193)
BLUE = (173, 216, 230)
GREEN = (144, 238, 144)
YELLOW = (255, 255, 153)

# Fuente para los dados
pygame.font.init()
font = pygame.font.Font(None, 200)
clock = pygame.time.Clock()

# Posiciones de las casillas (simplificadas)
path_positions = {0: (24, 85), 1: (86, 23), 2: (98, 159), 3: (160, 99),  # cárcel azul
                  4: (446, 99), 5: (521, 23), 6: (582, 86), 7: (506, 157),  # cárcel verde
                  8: (100, 445), 9: (26, 519), 10: (86, 577), 11: (160, 507),  # cárcel amarillo
                  12: (444, 505), 13: (504, 445), 14: (519, 577), 15: (579, 519),  # cárcel rojo
                  16: (283, 590), 17: (363, 592), 18: (363, 568), 19: (363, 544), 20: (361, 517), 21: (359, 493),
                  22: (356, 467), 23: (366, 431), 24: (385, 403), 25: (408, 382), 26: (435, 371), 27: (465, 364),
                  28: (492, 363), 29: (519, 365), 30: (540, 366), 31: (567, 364), 32: (590, 364),  # Rojo 1 al 17
                  33: (593, 316), 34: (589, 245), 35: (567, 244), 36: (543, 245), 37: (518, 246), 38: (494, 241),
                  39: (467, 244), 40: (436, 236), 41: (409, 219), 42: (385, 196), 43: (371, 166), 44: (359, 138),
                  45: (367, 110), 46: (367, 88), 47: (367, 63), 48: (368, 38), 49: (363, 10),  # Verde 18 al 34
                  50: (302, 11), 51: (223, 10), 52: (223, 36), 53: (222, 65), 54: (214, 86), 55: (215, 112),
                  56: (226, 136), 57: (219, 162), 58: (203, 186), 59: (183, 199), 60: (160, 212), 61: (137, 217),
                  62: (113, 214), 63: (87, 214), 64: (61, 215), 65: (37, 215), 66: (10, 216),  # Azul 35 al 51
                  67: (13, 304), 68: (10, 378), 69: (37, 379), 70: (63, 380), 71: (87, 378), 72: (111, 376), 73: (135, 376),
                  74: (165, 383), 75: (188, 396), 76: (207, 418), 77: (224, 440), 78: (234, 467), 79: (225, 492), 80: (226, 515),
                  81: (222, 541), 82: (222, 568), 83: (221, 591),  # Amarillo 52 al 68
                  84: (296, 567), 85: (298, 545), 86: (299, 517), 87: (299, 493), 88: (301, 468), 89: (299, 443), 90: (300, 416),  # Camino llegada rojo
                  91: (568, 301), 92: (540, 301), 93: (517, 298), 94: (491, 297), 95: (467, 297), 96: (442, 297), 97: (417, 297),  # Camino llegada verde
                  98: (302, 37), 99: (301, 63), 100: (302, 86), 101: (303, 112), 102: (303, 137), 103: (304, 161), 104: (304, 187),  # Camino llegada azul
                  105: (37, 302), 106: (63, 301), 107: (89, 301), 108: (111, 301), 109: (137, 301), 110: (162, 300), 111: (188, 299),  # Camino llegada amarillo
                  112: (230, 299), 113: (300, 234), 114: (368, 295), 115: (303, 371),}  # llegadas

# Definir casillas seguras (ajusta según tu tablero)
seguros = [path_positions[i] for i in [24, 41, 58, 75]]

# Variables iniciales
dado1, dado2 = 1, 1
movimientos_adicionales = 0
ultima_ficha_movida = None

# Diccionario de fichas
fichas = {
    "rojo": [path_positions[i] for i in range(12, 16)],
    "verde": [path_positions[i] for i in range(4, 8)],
    "azul": [path_positions[i] for i in range(0, 4)],
    "amarillo": [path_positions[i] for i in range(8, 12)],
}

caminos = {"rojo": [21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41,
                    42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62,
                    63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83,
                    16, 84, 85, 86, 87, 88, 89, 90, 115],
           "verde": [38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58,
                     59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79,
                     80, 81, 82, 83, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32,
                     91, 92, 93, 94, 95, 96, 97, 114],
           "azul": [55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75,
                    76, 77, 78, 79, 80, 81, 82, 83, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28,
                    29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49,
                    50, 98, 99, 100, 101, 102, 103, 104, 113],
           "amarillo": [72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 16, 17, 18, 19, 20, 21, 22, 23, 24,
                        25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45,
                        46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66,
                        67, 105, 106, 107, 108, 109, 110, 111, 112]}

carceles = {
    "rojo": [path_positions[i] for i in range(12, 16)],
    "verde": [path_positions[i] for i in range(4, 8)],
    "azul": [path_positions[i] for i in range(0, 4)],
    "amarillo": [path_positions[i] for i in range(8, 12)],
}

salidas = {
    "rojo": path_positions[21],
    "verde": path_positions[38],
    "azul": path_positions[55],
    "amarillo": path_positions[72]
}

llegadas = {
    "rojo": path_positions[115],
    "verde": path_positions[114],
    "azul": path_positions[113],
    "amarillo": path_positions[112]
}

jugadores = ["rojo", "verde", "azul", "amarillo"]
turno = 0
color = jugadores[turno]
pares_consecutivos = 0

# Colores de las fichas
colores_fichas = {
    "rojo": RED,
    "verde": GREEN,
    "azul": BLUE,
    "amarillo": YELLOW
}

# Función para mostrar texto
def mostrar_texto(texto, x, y, tamaño=36, color=BLACK):
    fuente = pygame.font.Font(None, tamaño)
    texto_surface = fuente.render(texto, True, color)
    screen.blit(texto_surface, (x, y))

# Menú inicial
def menu_inicial():
    screen.fill(WHITE)
    mostrar_texto("Presiona 'N' para Modo Normal", 100, 200, tamaño=50, color=BLACK)
    mostrar_texto("Presiona 'D' para Modo Desarrollador", 100, 300, tamaño=50, color=BLACK)
    pygame.display.flip()
    esperando = True
    while esperando:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_n:
                    return False
                elif event.key == pygame.K_d:
                    return True

modo_desarrollador = menu_inicial()

# Ingresar valores manualmente (modo desarrollador)
def ingresar_valores_manuales():
    screen.fill(WHITE)
    mostrar_texto("Ingresa el valor del primer dado (1-6):", 100, 200, tamaño=40, color=BLACK)
    pygame.display.flip()
    dado1 = None
    while dado1 is None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.unicode.isdigit() and 1 <= int(event.unicode) <= 6:
                    dado1 = int(event.unicode)
                    break
    screen.fill(WHITE)
    mostrar_texto("Ingresa el valor del segundo dado (1-6):", 100, 200, tamaño=40, color=BLACK)
    pygame.display.flip()
    dado2 = None
    while dado2 is None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.unicode.isdigit() and 1 <= int(event.unicode) <= 6:
                    dado2 = int(event.unicode)
                    break
    return dado1, dado2

# Dibujar fichas
def dibujar_fichas():
    posiciones_ocupadas = {}
    for color, fichas_color in fichas.items():
        for ficha_index, pos_index in enumerate(fichas_color):
            if isinstance(pos_index, tuple):
                pos = pos_index
            elif isinstance(pos_index, int) and pos_index in path_positions:
                pos = path_positions[pos_index]
            else:
                continue
            if pos not in posiciones_ocupadas:
                posiciones_ocupadas[pos] = []
            posiciones_ocupadas[pos].append((color, ficha_index))
    for pos, fichas_en_casilla in posiciones_ocupadas.items():
        num_fichas = len(fichas_en_casilla)
        offsets = [(0, 0)]
        if num_fichas == 2:
            offsets = [(-10, 0), (10, 0)]
        elif num_fichas >= 3:
            num_fichas = 2
            offsets = [(-10, 0), (10, 0)]
        for i, (color, ficha_index) in enumerate(fichas_en_casilla[:num_fichas]):
            radio = 18
            offset_x, offset_y = offsets[i % len(offsets)]
            pos_desplazada = (pos[0] + offset_x, pos[1] + offset_y)
            pygame.draw.circle(screen, colores_fichas[color], pos_desplazada, radio)
            font = pygame.font.Font(None, 28)
            text_surface = font.render(str(ficha_index + 1), True, BLACK)
            text_rect = text_surface.get_rect(center=pos_desplazada)
            screen.blit(text_surface, text_rect)

# Lanzar dados
def lanzar_dados():
    return random.randint(1, 6), random.randint(1, 6)

# Verificar bloqueo en el camino
def hay_bloqueo_en_camino(color, indice_actual, pasos):
    camino = caminos[color]
    for i in range(indice_actual + 1, min(indice_actual + pasos + 1, len(camino))):
        if verificar_bloqueo_en_casilla(camino[i]):
            return i - 1  # Devuelve la posición justo antes del bloqueo
    return None  # No hay bloqueo en el camino

# Mover ficha
def mover_ficha(color, ficha_index, pasos):
    global movimientos_adicionales, ultima_ficha_movida
    if ficha_index < len(fichas[color]):
        pos_actual = fichas[color][ficha_index]
        if pos_actual in carceles[color]:
            return
        if pos_actual == salidas[color]:
            nueva_pos = caminos[color][0]
            fichas[color][ficha_index] = nueva_pos
        else:
            if pos_actual in caminos[color]:
                indice_camino = caminos[color].index(pos_actual)
                nuevo_indice = indice_camino + pasos
                if nuevo_indice < len(caminos[color]):
                    # Verificar bloqueo en el camino
                    bloqueo_indice = hay_bloqueo_en_camino(color, indice_camino, pasos)
                    if bloqueo_indice is not None:
                        print(f"¡Hay un bloqueo en {caminos[color][bloqueo_indice + 1]}! Movimiento detenido en {caminos[color][bloqueo_indice]}.")
                        nueva_pos = caminos[color][bloqueo_indice]
                    else:
                        nueva_pos = caminos[color][nuevo_indice]
                    fichas_en_casilla = sum(1 for equipo in fichas.values() for pos in equipo if pos == nueva_pos)
                    if fichas_en_casilla >= 2:
                        print(f"¡No se puede mover a {nueva_pos} porque ya hay 2 fichas!")
                        return
                    fichas[color][ficha_index] = nueva_pos
                    bloqueo_o_captura = verificar_bloqueo_y_captura(color, nueva_pos)
                    if bloqueo_o_captura:
                        print(bloqueo_o_captura)
                        if "Capturaste" in bloqueo_o_captura:
                            ejecutar_movimientos_adicionales_inmediatos(color, 20)  # Ejecutar 20 movimientos tras captura
                    if nueva_pos == caminos[color][-1]:  # Llegada a la meta (Regla 8)
                        movimientos_adicionales += 10
                        print(f"¡Ficha {ficha_index + 1} de {color} ha llegado a la meta! +10 movimientos adicionales.")
                        ejecutar_movimientos_adicionales_inmediatos(color, 10)  # Ejecutar 10 movimientos tras llegar a la meta
                    ultima_ficha_movida = (color, ficha_index)
                else:
                    print(f"No puedes mover la ficha {ficha_index + 1} de {color} porque excede el camino.")
            else:
                print(f"La ficha {ficha_index + 1} de {color} no está en una posición válida.")

# Ejecutar movimientos adicionales inmediatamente (de una vez)
def ejecutar_movimientos_adicionales_inmediatos(color, cantidad):
    global movimientos_adicionales
    fichas_disponibles = mostrar_fichas_disponibles(color)
    if not fichas_disponibles:
        print(f"No hay fichas disponibles para mover. Se pierden los {cantidad} movimientos adicionales.")
        return
    ficha_seleccionada = seleccionar_ficha(color, fichas_disponibles)
    if ficha_seleccionada is not None:
        pos_actual = fichas[color][ficha_seleccionada]
        if pos_actual in carceles[color]:
            print("No se puede mover una ficha en la cárcel.")
            return
        indice_camino = caminos[color].index(pos_actual)
        nuevo_indice = indice_camino + cantidad
        if nuevo_indice < len(caminos[color]):
            bloqueo_indice = hay_bloqueo_en_camino(color, indice_camino, cantidad)
            if bloqueo_indice is not None:
                print(f"¡Hay un bloqueo en el camino! Movimiento detenido en {caminos[color][bloqueo_indice]}.")
                nueva_pos = caminos[color][bloqueo_indice]
            else:
                nueva_pos = caminos[color][nuevo_indice]
            fichas_en_casilla = sum(1 for equipo in fichas.values() for pos in equipo if pos == nueva_pos)
            if fichas_en_casilla >= 2:
                print(f"¡No se puede mover a {nueva_pos} porque ya hay 2 fichas!")
                return
            fichas[color][ficha_seleccionada] = nueva_pos
            print(f"Ficha {ficha_seleccionada + 1} de {color} movida directamente {cantidad} pasos a {nueva_pos}.")
            bloqueo_o_captura = verificar_bloqueo_y_captura(color, nueva_pos)
            if bloqueo_o_captura:
                print(bloqueo_o_captura)
                if "Capturaste" in bloqueo_o_captura:
                    ejecutar_movimientos_adicionales_inmediatos(color, 20)  # Ejecutar 20 movimientos tras captura adicional
            if nueva_pos == caminos[color][-1]:
                movimientos_adicionales += 10
                print(f"¡Ficha {ficha_seleccionada + 1} de {color} ha llegado a la meta! +10 movimientos adicionales.")
                ejecutar_movimientos_adicionales_inmediatos(color, 10)  # Ejecutar 10 movimientos tras llegar a la meta
            ultima_ficha_movida = (color, ficha_seleccionada)
        else:
            print(f"No se puede mover {cantidad} pasos porque excede el camino.")
    else:
        print("No se seleccionó ninguna ficha. Movimientos adicionales perdidos.")

# Sacar ficha de la cárcel
def sacar_ficha_de_carcel(color):
    fichas_en_salida = sum(1 for pos in fichas[color] if pos == salidas[color])
    if fichas_en_salida >= 2:
        print(f"No se puede sacar una ficha de la cárcel porque ya hay dos en la salida de {color}.")
        return False
    for i, pos in enumerate(fichas[color]):
        if pos in carceles[color]:
            fichas[color][i] = salidas[color]
            print(f"¡Ficha {i + 1} de {color} ha salido de la cárcel!")
            for equipo_enemigo, fichas_enemigas in fichas.items():
                if equipo_enemigo != color:
                    for ficha_index, pos_ficha in enumerate(fichas_enemigas):
                        if pos_ficha == salidas[color]:
                            fichas[equipo_enemigo][ficha_index] = carceles[equipo_enemigo][0]
                            print(f"¡Ficha {ficha_index + 1} de {equipo_enemigo} capturada y enviada a la cárcel!")
                            ejecutar_movimientos_adicionales_inmediatos(color, 20)  # Ejecutar movimientos tras captura en salida
                            break
            return True
    return False

# Verificar captura
def verificar_captura(color, ficha_index):
    pos_actual = fichas[color][ficha_index]
    if pos_actual in [salidas[color]] + carceles[color]:
        return False
    for equipo_enemigo, salida_enemiga in salidas.items():
        if equipo_enemigo != color and pos_actual == salida_enemiga:
            for ficha_enemiga_index, pos_ficha_enemiga in enumerate(fichas[equipo_enemigo]):
                if pos_ficha_enemiga == pos_actual:
                    return True
    return False

def capturar_ficha(color, ficha_index):
    global movimientos_adicionales
    fichas[color][ficha_index] = carceles[color][0]
    print(f"¡Ficha {ficha_index + 1} de {color} capturada y devuelta a la cárcel!")
    movimientos_adicionales += 20  # Acumular movimientos (Regla 7)
    print(f"¡{color} ha ganado 20 movimientos adicionales!")

def manejar_fichas_en_salida(color):
    fichas_en_salida = [(ficha_index, pos) for ficha_index, pos in enumerate(fichas[color]) if pos == salidas[color]]
    if len(fichas_en_salida) == 2:
        for equipo_enemigo, salida_enemiga in salidas.items():
            if equipo_enemigo != color:
                for ficha_enemiga_index, pos_ficha_enemiga in enumerate(fichas[equipo_enemigo]):
                    if pos_ficha_enemiga == salidas[color]:
                        capturar_ficha(equipo_enemigo, ficha_enemiga_index)
                        ejecutar_movimientos_adicionales_inmediatos(color, 20)  # Ejecutar movimientos tras captura
                        return
        print(f"¡Bloqueo en la salida de {color}! No se pueden mover fichas hasta que una se mueva.")

# Verificar bloqueo y captura
def verificar_bloqueo_y_captura(color, nueva_pos):
    fichas_en_casilla = [(equipo, ficha_index) for equipo, fichas_equipo in fichas.items() for ficha_index, pos in enumerate(fichas_equipo) if pos == nueva_pos]
    if len(fichas_en_casilla) > 1:
        equipo1, ficha_index1 = fichas_en_casilla[0]
        equipo2, ficha_index2 = fichas_en_casilla[1]
        if equipo1 == equipo2:
            print(f"¡Fichas del equipo {equipo1} forman un bloqueo en {nueva_pos}!")
            return "Forma un bloqueo con tus propias fichas."
        if nueva_pos in seguros or nueva_pos in salidas.values():
            print(f"¡Fichas de {equipo1} y {equipo2} forman un bloqueo en una casilla segura o salida!")
            return "Forma un bloqueo en una casilla especial."
        equipo_capturado = equipo1 if equipo1 != color else equipo2
        ficha_capturada = ficha_index1 if equipo1 != color else ficha_index2
        print(f"¡Ficha de {color} captura a la ficha de {equipo_capturado} en {nueva_pos}!")
        capturar_ficha(equipo_capturado, ficha_capturada)
        return f"Capturaste una ficha de {equipo_capturado} y la enviaste a la cárcel."
    return ""

# Verificar bloqueo en casilla
def verificar_bloqueo_en_casilla(casilla):
    return sum(1 for equipo in fichas.values() for pos in equipo if pos == casilla) >= 2

# Verificar llegada exacta
def verificar_movimiento_llegada(color, nuevo_indice, pasos):
    llegada = llegadas[color]
    if caminos[color][nuevo_indice] == llegada:
        return pasos == (len(caminos[color]) - 1 - caminos[color].index(caminos[color][nuevo_indice - pasos]))
    return True

# Verificar movimientos posibles
def convertir_tupla_a_indice(pos, color):
    for i, camino_pos in enumerate(caminos[color]):
        if camino_pos == pos:
            return i
    return -1

def hay_movimientos_posibles(color, dado1, dado2):
    if dado1 == 5 or dado2 == 5 or dado1 + dado2 == 5:
        if any(pos in carceles[color] for pos in fichas[color]):
            return True
    for ficha_index, pos in enumerate(fichas[color]):
        if pos not in carceles[color]:
            pos_index = convertir_tupla_a_indice(pos, color) if isinstance(pos, tuple) else pos
            for pasos in [dado1, dado2, dado1 + dado2]:
                nueva_pos_index = pos_index + pasos
                if nueva_pos_index < len(caminos[color]):
                    bloqueo_indice = hay_bloqueo_en_camino(color, pos_index, pasos)
                    if bloqueo_indice is None and verificar_movimiento_llegada(color, nueva_pos_index, pasos):
                        return True
    return False

# Manejar movimientos adicionales (usado para movimientos acumulados no inmediatos)
def manejar_movimientos_adicionales(color):
    global movimientos_adicionales
    if movimientos_adicionales > 0:
        print(f"Movimientos adicionales restantes: {movimientos_adicionales}")
        fichas_disponibles = mostrar_fichas_disponibles(color)
        if fichas_disponibles:
            ficha_seleccionada = seleccionar_ficha(color, fichas_disponibles)
            if ficha_seleccionada is not None:
                mover_ficha(color, ficha_seleccionada, movimientos_adicionales)
                movimientos_adicionales = 0  # Usar todos los movimientos de una vez
                return True
        movimientos_adicionales = 0  # Si no se mueve, se pierden
    return False

# Verificar dados iguales
def verificar_dados_iguales(dado1, dado2):
    return dado1 == dado2

# Manejar tres pares consecutivos
def manejar_tres_pares_consecutivos(color):
    global pares_consecutivos, ultima_ficha_movida
    if pares_consecutivos == 3:
        print(f"¡Tres pares consecutivos! La última ficha movida de {color} regresa a la cárcel.")
        if ultima_ficha_movida:
            color_ficha, ficha_index = ultima_ficha_movida
            fichas[color_ficha][ficha_index] = carceles[color_ficha][0]
        pares_consecutivos = 0

# Mostrar fichas disponibles
def mostrar_fichas_disponibles(color):
    return [i for i, pos in enumerate(fichas[color]) if pos not in carceles[color]]

# Seleccionar ficha
def seleccionar_ficha(color, fichas_disponibles):
    cuadro_x = scaled_width - 160
    cuadro_y = 10
    cuadro_ancho = 150
    cuadro_alto = 100 + len(fichas_disponibles) * 30
    screen.blit(tablero_img, (0, 0))
    dibujar_fichas()
    pygame.draw.rect(screen, WHITE, (cuadro_x, cuadro_y, cuadro_ancho, cuadro_alto))
    mostrar_texto(f"Turno de {color}", cuadro_x + 10, cuadro_y + 10, tamaño=20, color=BLACK)
    mostrar_texto("Seleccione ficha:", cuadro_x + 10, cuadro_y + 40, tamaño=20, color=BLACK)
    for i, ficha in enumerate(fichas_disponibles):
        mostrar_texto(f"{i + 1}: Ficha {ficha + 1}", cuadro_x + 10, cuadro_y + 70 + i * 30, tamaño=20, color=BLACK)
    pygame.display.flip()
    seleccion = None
    while seleccion is None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if pygame.K_1 <= event.key <= pygame.K_9 and (event.key - pygame.K_1) < len(fichas_disponibles):
                    seleccion = fichas_disponibles[event.key - pygame.K_1]
                    break
    return seleccion

# Seleccionar dado
def seleccionar_dado(dado1, dado2):
    cuadro_x = scaled_width - 160
    cuadro_y = 470
    cuadro_ancho = 150
    cuadro_alto = 140
    screen.blit(tablero_img, (0, 0))
    dibujar_fichas()
    pygame.draw.rect(screen, WHITE, (cuadro_x, cuadro_y, cuadro_ancho, cuadro_alto))
    mostrar_texto("Seleccione dado:", cuadro_x + 10, cuadro_y + 10, tamaño=20, color=BLACK)
    mostrar_texto(f"1: Dado 1 ({dado1})", cuadro_x + 10, cuadro_y + 40, tamaño=20, color=BLACK)
    mostrar_texto(f"2: Dado 2 ({dado2})", cuadro_x + 10, cuadro_y + 70, tamaño=20, color=BLACK)
    mostrar_texto(f"3: Suma ({dado1 + dado2})", cuadro_x + 10, cuadro_y + 100, tamaño=20, color=BLACK)
    pygame.display.flip()
    seleccion = None
    while seleccion is None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    seleccion = dado1
                elif event.key == pygame.K_2:
                    seleccion = dado2
                elif event.key == pygame.K_3:
                    seleccion = dado1 + dado2
                break
    return seleccion

# Inicializar valores
dado1, dado2 = lanzar_dados()
mostrar_dados = True

# Bucle principal
running = True
while running:
    screen.blit(tablero_img, (0, 0))
    dibujar_fichas()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            if movimientos_adicionales > 0:  # Regla 9: Priorizar movimientos adicionales
                manejar_movimientos_adicionales(color)
            else:
                if modo_desarrollador:
                    screen.fill(WHITE)
                    mostrar_texto("Presiona 'L' para lanzar dados", 100, 200, tamaño=40, color=BLACK)
                    mostrar_texto("Presiona 'M' para ingresar manualmente", 100, 300, tamaño=40, color=BLACK)
                    pygame.display.flip()
                    esperando = True
                    while esperando:
                        for sub_event in pygame.event.get():
                            if sub_event.type == pygame.QUIT:
                                pygame.quit()
                                exit()
                            if sub_event.type == pygame.KEYDOWN:
                                if sub_event.key == pygame.K_l:
                                    dado1, dado2 = lanzar_dados()
                                    esperando = False
                                elif sub_event.key == pygame.K_m:
                                    dado1, dado2 = ingresar_valores_manuales()
                                    esperando = False
                else:
                    dado1, dado2 = lanzar_dados()

                suma_dados = dado1 + dado2

                if dado1 == 5 or dado2 == 5 or suma_dados == 5:
                    fichas_en_salida = [pos for pos in fichas[color] if pos == salidas[color]]
                    if len(fichas_en_salida) < 2:
                        ficha_sacada = sacar_ficha_de_carcel(color)
                        if ficha_sacada:
                            print(f"¡Se sacó una ficha de la cárcel con un 5!")
                            fichas_disponibles = mostrar_fichas_disponibles(color)
                            if fichas_disponibles:
                                ficha_seleccionada = seleccionar_ficha(color, fichas_disponibles)
                                if ficha_seleccionada is not None:
                                    pasos = seleccionar_dado(dado1, dado2)
                                    mover_ficha(color, ficha_seleccionada, pasos)
                                    ultima_ficha_movida = (color, ficha_seleccionada)
                                    if pasos in [dado1, dado2] and pasos != suma_dados:
                                        fichas_disponibles = mostrar_fichas_disponibles(color)
                                        if fichas_disponibles:
                                            ficha_seleccionada = seleccionar_ficha(color, fichas_disponibles)
                                            if ficha_seleccionada is not None:
                                                pasos_restantes = dado2 if pasos == dado1 else dado1
                                                mover_ficha(color, ficha_seleccionada, pasos_restantes)
                                                ultima_ficha_movida = (color, ficha_seleccionada)
                        else:
                            fichas_disponibles = mostrar_fichas_disponibles(color)
                            if fichas_disponibles:
                                ficha_seleccionada = seleccionar_ficha(color, fichas_disponibles)
                                if ficha_seleccionada is not None:
                                    pasos = seleccionar_dado(dado1, dado2)
                                    mover_ficha(color, ficha_seleccionada, pasos)
                                    ultima_ficha_movida = (color, ficha_seleccionada)
                                    if pasos in [dado1, dado2] and pasos != suma_dados:
                                        fichas_disponibles = mostrar_fichas_disponibles(color)
                                        if fichas_disponibles:
                                            ficha_seleccionada = seleccionar_ficha(color, fichas_disponibles)
                                            if ficha_seleccionada is not None:
                                                pasos_restantes = dado2 if pasos == dado1 else dado1
                                                mover_ficha(color, ficha_seleccionada, pasos_restantes)
                                                ultima_ficha_movida = (color, ficha_seleccionada)
                    else:
                        print(f"¡Hay dos fichas en la salida de {color}! No se puede sacar otra.")
                        fichas_disponibles = mostrar_fichas_disponibles(color)
                        if fichas_disponibles:
                            ficha_seleccionada = seleccionar_ficha(color, fichas_disponibles)
                            if ficha_seleccionada is not None:
                                pasos = seleccionar_dado(dado1, dado2)
                                mover_ficha(color, ficha_seleccionada, pasos)
                                ultima_ficha_movida = (color, ficha_seleccionada)
                                if pasos in [dado1, dado2] and pasos != suma_dados:
                                    fichas_disponibles = mostrar_fichas_disponibles(color)
                                    if fichas_disponibles:
                                        ficha_seleccionada = seleccionar_ficha(color, fichas_disponibles)
                                        if ficha_seleccionada is not None:
                                            pasos_restantes = dado2 if pasos == dado1 else dado1
                                            mover_ficha(color, ficha_seleccionada, pasos_restantes)
                                            ultima_ficha_movida = (color, ficha_seleccionada)
                else:
                    fichas_disponibles = mostrar_fichas_disponibles(color)
                    if fichas_disponibles:
                        ficha_seleccionada = seleccionar_ficha(color, fichas_disponibles)
                        if ficha_seleccionada is not None:
                            pasos = seleccionar_dado(dado1, dado2)
                            mover_ficha(color, ficha_seleccionada, pasos)
                            ultima_ficha_movida = (color, ficha_seleccionada)
                            if pasos in [dado1, dado2] and pasos != suma_dados:
                                fichas_disponibles = mostrar_fichas_disponibles(color)
                                if fichas_disponibles:
                                    ficha_seleccionada = seleccionar_ficha(color, fichas_disponibles)
                                    if ficha_seleccionada is not None:
                                        pasos_restantes = dado2 if pasos == dado1 else dado1
                                        mover_ficha(color, ficha_seleccionada, pasos_restantes)
                                        ultima_ficha_movida = (color, ficha_seleccionada)

                if verificar_dados_iguales(dado1, dado2):
                    print(f"¡Dados iguales! El equipo {color} repite turno.")
                    pares_consecutivos += 1
                else:
                    pares_consecutivos = 0
                    turno = (turno + 1) % len(jugadores)
                    color = jugadores[turno]

                manejar_tres_pares_consecutivos(color)

                if not hay_movimientos_posibles(color, dado1, dado2):
                    print(f"No hay movimientos posibles para {color}. Turno pasa al siguiente.")
                    turno = (turno + 1) % len(jugadores)
                    color = jugadores[turno]

    pygame.draw.rect(screen, WHITE, (scaled_width - 153, 141, 145, 145))
    pygame.draw.rect(screen, WHITE, (scaled_width - 153, 317.5, 145, 145))
    if mostrar_dados:
        text1 = font.render(str(dado1), True, BLACK)
        text2 = font.render(str(dado2), True, BLACK)
        screen.blit(text1, (scaled_width - 115, 141))
        screen.blit(text2, (scaled_width - 115, 317.5))

    # Mostrar movimientos adicionales en pantalla (Regla 9)
    if movimientos_adicionales > 0:
        mostrar_texto(f"Movimientos adicionales: {movimientos_adicionales}", 10, 10, tamaño=30, color=BLACK)

    pygame.display.flip()
    clock.tick(30)

pygame.quit()