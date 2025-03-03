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
                  112: (230, 299), 113: (300, 234), 114: (368, 295), 115: (303, 371)}  # llegadas

# Definir casillas seguras
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

#Diccionario camino de cada equipo
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

#Diccionario de carceles
carceles = {
    "rojo": [path_positions[i] for i in range(12, 16)],
    "verde": [path_positions[i] for i in range(4, 8)],
    "azul": [path_positions[i] for i in range(0, 4)],
    "amarillo": [path_positions[i] for i in range(8, 12)],
}

#Diccionario de salidas
salidas = {
    "rojo": path_positions[21],
    "verde": path_positions[38],
    "azul": path_positions[55],
    "amarillo": path_positions[72]
}

#Diccionario de salidas
llegadas = {
    "rojo": path_positions[115],
    "verde": path_positions[114],
    "azul": path_positions[113],
    "amarillo": path_positions[112]
}

#variables
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

def mostrar_texto(mensajes, espera=True):
    """
    Parámetros:
    mensajes: Lista de strings para mostrar en formato vertical.
    espera=True: Boleano, cuando es True la función pausa la ejecuación hasta que se presione la tecla espacio.
    
    La función muestra texto en el centro-derecha de la pantalla con fondo blanco y formato vertical.
    Si espera es True, pausa hasta que el usuario interactúe.
    """
    cuadro_x = scaled_width - 160
    cuadro_y = scaled_height // 2 - 50
    cuadro_ancho = 160
    cuadro_alto = len(mensajes) * 20 + 20
    pygame.draw.rect(screen, WHITE, (cuadro_x, cuadro_y, cuadro_ancho, cuadro_alto))
    for i, mensaje in enumerate(mensajes):
        fuente = pygame.font.Font(None, 15)
        texto_surface = fuente.render(mensaje, True, BLACK)
        screen.blit(texto_surface, (cuadro_x + 10, cuadro_y + 10 + i * 20))
    pygame.display.flip()
    if espera:
        esperando = True
        while esperando:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                    esperando = False
            pygame.time.wait(100)

#Salección del modo de juego
def menu_inicial():
    """
    Muestra el menú inicial y permite seleccionar el modo de juego.
    Retorna False para modo normal y True para modo desarrollador.
    """
    screen.blit(tablero_img, (0, 0))
    mostrar_texto(["Presiona 'N' para", "iniciar el juego"], espera=False)
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

#Seleción de los valores de los dados en modo desarrollador
def ingresar_valores_manuales():
    """
    Permite al usuario ingresar manualmente los valores de los dados en modo desarrollador.
    Retorna una tupla con los valores de los dos dados (entre 1 y 6).
    """
    screen.blit(tablero_img, (0, 0))
    dibujar_fichas()
    mostrar_texto(["Ingresa el valor", "del primer dado", "(1-6):"], espera=False)
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
    screen.blit(tablero_img, (0, 0))
    dibujar_fichas()
    mostrar_texto(["Ingresa el valor", "del segundo dado", "(1-6):"], espera=False)
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

#Se dibujan las fichas con un número sobre ellas 
def dibujar_fichas():
    """
    Dibuja las fichas en el tablero según sus posiciones actuales.
    Ajusta la posición visual si hay más de una ficha en la misma casilla.
    """
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
            offsets = [(-10, -10), (-10, 10), (10, -10), (10, 10)][:num_fichas]  # Permitir más de 2 en llegada
        for i, (color, ficha_index) in enumerate(fichas_en_casilla):
            radio = 18
            offset_x, offset_y = offsets[i % len(offsets)]
            pos_desplazada = (pos[0] + offset_x, pos[1] + offset_y)
            pygame.draw.circle(screen, colores_fichas[color], pos_desplazada, radio)
            font = pygame.font.Font(None, 28)
            text_surface = font.render(str(ficha_index + 1), True, BLACK)
            text_rect = text_surface.get_rect(center=pos_desplazada)
            screen.blit(text_surface, text_rect)

#Lanzamiento de dados
def lanzar_dados():
    """
    Genera valores aleatorios para los dos dados.
    Retorna una tupla con los valores de los dados (entre 1 y 6).
    """
    return random.randint(1, 6), random.randint(1, 6)

# Movimiento de la ficha
def mover_ficha(color, ficha_index, pasos, es_adicional=False):
    """
    Parámetros:
    color: Color del equipo que mueve la ficha.
    ficha_index: Índice de la ficha dentro de la lista de fichas.
    pasos: Número de posiciones que la ficha debe avanzar
    es_adicional=False: Indica si el movimiento es parte de movimientos adicionales (captura o llegada).
    
    Mueve una ficha del jugador según el número de pasos indicado.
    Retorna True si el movimiento se realizó, False si no fue posible.
    """
    global movimientos_adicionales, ultima_ficha_movida, running
    if ficha_index < len(fichas[color]):
        pos_actual = fichas[color][ficha_index]
        if pos_actual in carceles[color]:
            return False
        if pos_actual == salidas[color]:
            nueva_pos = caminos[color][0]
            fichas[color][ficha_index] = nueva_pos
            ultima_ficha_movida = (color, ficha_index)
            mostrar_texto([f"Ficha {ficha_index + 1}", f"de {color} salió", f"a {nueva_pos}"])
            return True
        else:
            if pos_actual in caminos[color]:
                indice_camino = caminos[color].index(pos_actual)
                nuevo_indice = indice_camino + pasos
                if nuevo_indice < len(caminos[color]):
                    if caminos[color][nuevo_indice] == llegadas[color]:
                        pasos_exactos = len(caminos[color]) - 1 - indice_camino
                        if pasos != pasos_exactos:
                            mensaje = [f"Esta ficha necesita", f"exactamente {pasos_exactos}", "para llegar a la meta.", "Seleccione otra ficha."]
                            mostrar_texto(mensaje)
                            print(" ".join(mensaje))
                            return False
                    bloqueo_indice = hay_bloqueo_en_camino(color, indice_camino, pasos)
                    if bloqueo_indice is not None:
                        mensaje = ["No puede mover", "esta ficha.", f"Bloqueo en", f"{caminos[color][bloqueo_indice + 1]}.", "Seleccione otra ficha."]
                        mostrar_texto(mensaje)
                        print(" ".join(mensaje))
                        return False
                    nueva_pos = caminos[color][nuevo_indice]
                    # No limitar a 2 fichas en la llegada
                    if nueva_pos != llegadas[color]:
                        fichas_en_casilla = sum(1 for equipo in fichas.values() for pos in equipo if pos == nueva_pos)
                        if fichas_en_casilla >= 2:
                            mensaje = ["No se puede mover", f"a {nueva_pos}.", "Ya hay 2 fichas.", "Seleccione otra ficha."]
                            mostrar_texto(mensaje)
                            print(" ".join(mensaje))
                            return False
                    fichas[color][ficha_index] = nueva_pos
                    bloqueo_o_captura = verificar_bloqueo_y_captura(color, nueva_pos)
                    if bloqueo_o_captura:
                        if "Capturaste" in bloqueo_o_captura:
                            mensajes = bloqueo_o_captura.split(". ")
                            mostrar_texto([m for m in mensajes if m])
                            print(bloqueo_o_captura)
                            ejecutar_movimientos_adicionales_inmediatos(color, 20)
                    if nueva_pos == caminos[color][-1]:  # Llegada a la meta otorga 10 movimientos
                        movimientos_adicionales += 10
                        mensaje = [f"¡Ficha {ficha_index + 1}", f"de {color} llegó", "a la meta!", "+10 movimientos."]
                        mostrar_texto(mensaje)
                        print(" ".join(mensaje))
                        ejecutar_movimientos_adicionales_inmediatos(color, 10)
                        # Verificar si el equipo ha ganado (4 fichas en la meta)
                        if sum(1 for pos in fichas[color] if pos == llegadas[color]) == 4:
                            mensaje = [f"¡{color.capitalize()} ha ganado!", "Todas las fichas", "están en la meta!"]
                            mostrar_texto(mensaje)
                            print(" ".join(mensaje))
                            running = False  # Terminar el juego
                    ultima_ficha_movida = (color, ficha_index)
                    return True
                else:
                    mensaje = [f"No puede mover", f"la ficha {ficha_index + 1}", f"de {color}. Excede", "el camino.", "Seleccione otra ficha."]
                    mostrar_texto(mensaje)
                    print(" ".join(mensaje))
                    return False
            else:
                print(f"La ficha {ficha_index + 1} de {color} no está en una posición válida.")
                return False
    return False

# Regla 1: Sacar ficha de la cárcel con un 5
def sacar_ficha_de_carcel(color):
    """
    Parámetros:
    color: Color del equipo que intenta sacar una ficha.
    
    Saca una ficha de la cárcel si hay menos de 2 en la salida.
    Retorna True si se sacó una ficha, False si no.
    """
    fichas_en_salida = sum(1 for pos in fichas[color] if pos == salidas[color])
    if fichas_en_salida >= 2:
        mensaje = ["No se puede sacar", "una ficha. Ya hay", f"dos en la salida", f"de {color}."]
        mostrar_texto(mensaje)
        print(" ".join(mensaje))
        return False
    for i, pos in enumerate(fichas[color]):
        if pos in carceles[color]:
            fichas[color][i] = salidas[color]
            mensaje = [f"¡Ficha {i + 1} de", f"{color} ha salido", "de la cárcel!"]
            mostrar_texto(mensaje)
            print(" ".join(mensaje))
            for equipo_enemigo, fichas_enemigas in fichas.items():
                if equipo_enemigo != color:
                    for ficha_index, pos_ficha in enumerate(fichas_enemigas):
                        if pos_ficha == salidas[color]:
                            fichas[equipo_enemigo][ficha_index] = carceles[equipo_enemigo][0]
                            mensaje = [f"¡Ficha {ficha_index + 1}", f"de {equipo_enemigo}", "capturada y enviada", "a la cárcel!"]
                            mostrar_texto(mensaje)
                            print(" ".join(mensaje))
                            ejecutar_movimientos_adicionales_inmediatos(color, 20)
                            break
            return True
    return False

#Regla 2: Capturar fichas en salida
def verificar_captura(color, ficha_index):
    """
    Parámetros:
    color: Color del equipo al que pertenece la ficha.
    ficha_index: Indice de la ficha dentro de la lista de fichas.
    
    Verifica si una ficha puede capturar a otra en una salida enemiga.
    Retorna True si hay captura posible, False si no.
    """
    pos_actual = fichas[color][ficha_index]
    if pos_actual in [salidas[color]] + carceles[color]:
        return False
    for equipo_enemigo, salida_enemiga in salidas.items():
        if equipo_enemigo != color and pos_actual == salida_enemiga:
            for ficha_enemiga_index, pos_ficha_enemiga in enumerate(fichas[equipo_enemigo]):
                if pos_ficha_enemiga == pos_actual:
                    return True
    return False

#Captura de fichas enemigas
def capturar_ficha(color, ficha_index):
    """
    Parámetros:
    color: Color del equipo al que pertenece la ficha.
    ficha_index: Indice de la ficha dentro de la lista de fichas.
    
    Captura una ficha enemiga y la envía a la cárcel.
    Actualiza los movimientos adicionales del equipo que captura.
    """
    global movimientos_adicionales
    fichas[color][ficha_index] = carceles[color][0]
    mensaje = [f"¡Ficha {ficha_index + 1}", f"de {color} capturada", "y devuelta a", "la cárcel!"]
    mostrar_texto(mensaje)
    print(" ".join(mensaje))
    movimientos_adicionales += 20
    mensaje = [f"¡{color} ha ganado", "20 movimientos", "adicionales!"]
    mostrar_texto(mensaje)
    print(" ".join(mensaje))

#Manejar capturas cuando una ficha sale de la carcel
def manejar_fichas_en_salida(color):
    """
    Parámetros:
    color: Color del equipo al que pertenece la ficha.
    
    Maneja el caso de dos fichas en la salida del equipo.
    Realiza captura si hay ficha enemiga o muestra mensaje de bloqueo.
    """
    fichas_en_salida = [(ficha_index, pos) for ficha_index, pos in enumerate(fichas[color]) if pos == salidas[color]]
    if len(fichas_en_salida) == 2:
        for equipo_enemigo, salida_enemiga in salidas.items():
            if equipo_enemigo != color:
                for ficha_enemiga_index, pos_ficha_enemiga in enumerate(fichas[equipo_enemigo]):
                    if pos_ficha_enemiga == salidas[color]:
                        capturar_ficha(equipo_enemigo, ficha_enemiga_index)
                        ejecutar_movimientos_adicionales_inmediatos(color, 20)
                        return
        mensaje = [f"¡Bloqueo en la", f"salida de {color}!", "No se pueden", "mover fichas."]
        mostrar_texto(mensaje)
        print(" ".join(mensaje))

# Regla 3: No se puede mover una ficha si hay un bloqueo en el camino del mismo equipo (a)
def verificar_bloqueo_y_captura(color, nueva_pos):
    """
    Parámetros:
    color: Color del equipo al que pertenece la ficha.
    nueva_pos: Nueva posición de la ficha en el tablero.
    
    Verifica si hay bloqueo o captura en una casilla.
    Retorna un mensaje describiendo el resultado (bloqueo o captura).
    """
    fichas_en_casilla = [(equipo, ficha_index) for equipo, fichas_equipo in fichas.items() for ficha_index, pos in enumerate(fichas_equipo) if pos == nueva_pos]
    if len(fichas_en_casilla) > 1:
        equipo1, ficha_index1 = fichas_en_casilla[0]
        equipo2, ficha_index2 = fichas_en_casilla[1]
        if nueva_pos == llegadas[color]:
            if equipo1 != color or equipo2 != color:
                equipo_capturado = equipo1 if equipo1 != color else equipo2
                ficha_capturada = ficha_index1 if equipo1 != color else ficha_index2
                fichas[equipo_capturado][ficha_capturada] = carceles[equipo_capturado][0]
                return f"Capturaste una ficha de {equipo_capturado} en la llegada y la enviaste a la cárcel."
            return ""  # No hay bloqueo en la llegada si son del mismo equipo
        if nueva_pos in seguros or nueva_pos in salidas.values():
            mensaje = [f"¡Bloqueo en", "casilla segura o", f"salida: {nueva_pos}!"]
            mostrar_texto(mensaje)
            print(" ".join(mensaje))
            return "Forma un bloqueo en una casilla especial."
        if equipo1 == equipo2:
            mensaje = [f"¡Fichas del equipo", f"{equipo1} forman", f"un bloqueo en", f"{nueva_pos}!"]
            mostrar_texto(mensaje)
            print(" ".join(mensaje))
            return "Forma un bloqueo con tus propias fichas."
        else:
            equipo_capturado = equipo1 if equipo1 != color else equipo2
            ficha_capturada = ficha_index1 if equipo1 != color else ficha_index2
            fichas[equipo_capturado][ficha_capturada] = carceles[equipo_capturado][0]
            mensaje = [f"¡Ficha de {color}", f"captura a la de", f"{equipo_capturado} en", f"{nueva_pos}!"]
            mostrar_texto(mensaje)
            print(" ".join(mensaje))
            return f"Capturaste una ficha de {equipo_capturado} y la enviaste a la cárcel."
    elif len(fichas_en_casilla) == 1:
        equipo, ficha_index = fichas_en_casilla[0]
        if nueva_pos not in seguros and nueva_pos not in salidas.values() and nueva_pos != llegadas[color] and equipo != color:
            fichas[equipo][ficha_index] = carceles[equipo][0]
            mensaje = [f"¡Ficha de {color}", f"captura a la de", f"{equipo} en", f"{nueva_pos}!"]
            mostrar_texto(mensaje)
            print(" ".join(mensaje))
            return f"Capturaste una ficha de {equipo} y la enviaste a la cárcel."
    return ""

#Verificación de captura o bloqueo (a-b)
def verificar_bloqueo_en_casilla(casilla):
    """
    Parámetros:
    casilla: posición en el tablero que se va verificar
    
    Verifica si una casilla tiene un bloqueo (2 o más fichas), excluyendo llegadas.
    Retorna True si hay bloqueo, False si no o si es una casilla de llegada.
    """
    if casilla in llegadas.values():
        return False
    return sum(1 for equipo in fichas.values() for pos in equipo if pos == casilla) >= 2

def hay_bloqueo_en_camino(color, indice_actual, pasos):
    """
    Parámetros:
    color: Color del equipo al que pertenece la ficha.
    indice_actual: indice actual de la ficha en el camino que corresponde.
    pasos: Número de las fichas que intenta avanzar.
    
    Verifica si hay un bloqueo en el camino de una ficha, excluyendo la meta.
    Retorna el índice justo antes del bloqueo si existe, o None si no hay bloqueo.
    """
    camino = caminos[color]
    for i in range(indice_actual + 1, min(indice_actual + pasos + 1, len(camino))):
        if verificar_bloqueo_en_casilla(camino[i]) and camino[i] != llegadas[color]:
            return i - 1
    return None

#Regla 5: Número exacto de movimientos para llegar a la meta
def verificar_movimiento_llegada(color, nuevo_indice, pasos):
    """
    Parámetros:
    color: Color del equipo al que pertenece la ficha.
    nuevo_indice: índice de la casilla a la que se intent mover la ficha.
    pasos: Número de posiciones que la ficha intenta avanzar.
    
    Verifica si el movimiento a la meta es exacto.
    Retorna True si el movimiento es válido, False si no.
    """
    llegada = llegadas[color]
    if caminos[color][nuevo_indice] == llegada:
        return pasos == (len(caminos[color]) - 1 - caminos[color].index(caminos[color][nuevo_indice - pasos]))
    return True

#Regla 6: Si no hay movimientos posibles el turno pasa
def convertir_tupla_a_indice(pos, color):
    """
    Parámetros:
    pos: Coordenadas de la posición a buscar.
    color: Color del equipo al que pertenece la ficha.
    
    Convierte una posición en coordenadas a un índice en el camino.
    Retorna el índice en el camino o -1 si no se encuentra.
    """
    for i, camino_pos in enumerate(caminos[color]):
        if camino_pos == pos:
            return i
    return -1

def hay_movimientos_posibles(color, dado1, dado2):
    """
    Parámetros:
    color: Color del equipo al que pertenece la ficha.
    dado1: Valor del primer dado.
    dado2: Valor del segundo dado.
    
    Verifica si hay movimientos posibles para un equipo con los dados actuales.
    Retorna True si hay movimientos posibles, False si no.
    """
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

# Regla 7: 20 movimientos adicionales al capturar una ficha
# Regla 8: 10 movimientos adicionales al llegar a la meta
def ejecutar_movimientos_adicionales_inmediatos(color, cantidad):
    """
    Parámetros:
    color: Color del equipo al que pertenece la ficha.
    cantidad: Cantidad de movimientos adicionales(10 o 20).
    
    Ejecuta movimientos adicionales de una vez para una ficha seleccionada.
    Usa la cantidad especificada de movimientos (10 o 20).
    """
    global movimientos_adicionales, running
    fichas_disponibles = mostrar_fichas_disponibles(color)
    if not fichas_disponibles:
        mensaje = ["No hay fichas", f"disponibles. Se", f"pierden los {cantidad}", "movimientos."]
        mostrar_texto(mensaje)
        print(" ".join(mensaje))
        return
    while True:
        ficha_seleccionada = seleccionar_ficha(color, fichas_disponibles)
        if ficha_seleccionada is None or not running:
            mensaje = ["Usted perdió los", f"{cantidad} movimientos.", "No seleccionó una", "ficha válida."]
            mostrar_texto(mensaje)
            print(" ".join(mensaje))
            return
        if mover_ficha(color, ficha_seleccionada, cantidad, es_adicional=True):
            break
        else:
            fichas_disponibles.remove(ficha_seleccionada)
            if not fichas_disponibles:
                mensaje = ["Usted perdió los", f"{cantidad} movimientos.", "Bloqueo o sin", "fichas disponibles."]
                mostrar_texto(mensaje)
                print(" ".join(mensaje))
                return

# Regla 9: Movimientos adicionales deben ser usados inmediatamente
def manejar_movimientos_adicionales(color):
    """
    Parámetros:
    color: color del equipo al que pertenece la ficha.
    
    Maneja los movimientos adicionales acumulados para un equipo.
    Retorna True si se usaron los movimientos, False si se perdieron.
    """
    global movimientos_adicionales
    if movimientos_adicionales > 0:
        mensaje = [f"Movimientos", f"adicionales:", f"{movimientos_adicionales}"]
        mostrar_texto(mensaje, espera=False)
        print(" ".join(mensaje))
        fichas_disponibles = mostrar_fichas_disponibles(color)
        if not fichas_disponibles:
            mensaje = ["Usted perdió los", f"{movimientos_adicionales}", "movimientos.", "Sin fichas", "disponibles."]
            mostrar_texto(mensaje)
            print(" ".join(mensaje))
            movimientos_adicionales = 0
            return False
        while True:
            ficha_seleccionada = seleccionar_ficha(color, fichas_disponibles)
            if ficha_seleccionada is None or not running:
                mensaje = ["Usted perdió los", f"{movimientos_adicionales}", "movimientos.", "No seleccionó una", "ficha válida."]
                mostrar_texto(mensaje)
                print(" ".join(mensaje))
                movimientos_adicionales = 0
                return False
            if mover_ficha(color, ficha_seleccionada, movimientos_adicionales, es_adicional=True):
                movimientos_adicionales = 0
                return True
            else:
                fichas_disponibles.remove(ficha_seleccionada)
                if not fichas_disponibles:
                    mensaje = ["Usted perdió los", f"{movimientos_adicionales}", "movimientos.", "Bloqueo o sin", "fichas disponibles."]
                    mostrar_texto(mensaje)
                    print(" ".join(mensaje))
                    movimientos_adicionales = 0
                    return False

# Regla 10: Dados iguales permiten repetir turno
def verificar_dados_iguales(dado1, dado2):
    """
    Parámetros:
    dado1: Valor del primer dado.
    dado2: Valor del segundo dado.
    
    Verifica si los valores de los dados son iguales.
    Retorna True si son iguales, False si no.
    """
    return dado1 == dado2

# Regla 11: Tres pares consecutivos devuelven la última ficha a la cárcel
def manejar_tres_pares_consecutivos(color):
    """
    Parámetros:
    color: Color del equipo al que pertenece la ficha.
    
    Maneja la regla de tres pares consecutivos.
    Envía la última ficha movida a la cárcel si aplica.
    """
    global pares_consecutivos, ultima_ficha_movida
    if pares_consecutivos == 3:
        mensaje = ["¡Tres pares", "consecutivos!", f"Última ficha de", f"{color} a la cárcel."]
        mostrar_texto(mensaje)
        print(" ".join(mensaje))
        if ultima_ficha_movida:
            color_ficha, ficha_index = ultima_ficha_movida
            fichas[color_ficha][ficha_index] = carceles[color_ficha][0]
        pares_consecutivos = 0

def mostrar_fichas_disponibles(color):
    """
    Parámetros:
    color: Color de del equipo al que pertenece la ficha.
    
    Muestra las fichas disponibles para mover de un equipo.
    Retorna una lista de índices de fichas fuera de la cárcel.
    """
    return [i for i, pos in enumerate(fichas[color]) if pos not in carceles[color]]

def seleccionar_ficha(color, fichas_disponibles):
    """
    Parámtros:
    Color: Color del equipo al que pertenece la ficha.
    fichas_disponibles: Lista de los indices de las fichas que se pueden mover.
    
    Permite al usuario seleccionar una ficha de las disponibles.
    Retorna el índice de la ficha seleccionada o None si no hay selección válida.
    """
    cuadro_x = scaled_width - 160
    cuadro_y = 10
    cuadro_ancho = 150
    cuadro_alto = 100 + len(fichas_disponibles) * 30
    screen.blit(tablero_img, (0, 0))
    dibujar_fichas()
    pygame.draw.rect(screen, WHITE, (cuadro_x, cuadro_y, cuadro_ancho, cuadro_alto))
    mostrar_texto([f"Turno de {color.capitalize()}"], espera=False)
    mostrar_texto([f"{color.capitalize()}: Seleccione", "ficha:"], espera=False)
    for i, ficha in enumerate(fichas_disponibles):
        fuente = pygame.font.Font(None, 25)
        texto_surface = fuente.render(f"{i + 1}: Ficha {ficha + 1}", True, BLACK)
        screen.blit(texto_surface, (cuadro_x + 10, cuadro_y + 70 + i * 30))
    pygame.display.flip()
    seleccion = None
    while seleccion is None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                global running
                running = False
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if pygame.K_1 <= event.key <= pygame.K_9 and (event.key - pygame.K_1) < len(fichas_disponibles):
                    seleccion = fichas_disponibles[event.key - pygame.K_1]
                    break
    return seleccion

def seleccionar_dado(dado1, dado2):
    """
    Parámetros:
    dado1: Valor del primer dado.
    dado2: Valor del segundo dado
    
    Permite al usuario seleccionar qué valor de dado usar.
    Retorna el valor seleccionado (dado1, dado2 o suma).
    """
    global color
    cuadro_x = scaled_width - 160
    cuadro_y = 470
    cuadro_ancho = 150
    cuadro_alto = 140
    screen.blit(tablero_img, (0, 0))
    dibujar_fichas()
    pygame.draw.rect(screen, WHITE, (cuadro_x, cuadro_y, cuadro_ancho, cuadro_alto))
    mostrar_texto([f"{color.capitalize()}: Seleccione", "dado:"], espera=False)
    fuente = pygame.font.Font(None, 25)
    screen.blit(fuente.render(f"1: Dado 1 ({dado1})", True, BLACK), (cuadro_x + 10, cuadro_y + 40))
    screen.blit(fuente.render(f"2: Dado 2 ({dado2})", True, BLACK), (cuadro_x + 10, cuadro_y + 70))
    screen.blit(fuente.render(f"3: Suma ({dado1 + dado2})", True, BLACK), (cuadro_x + 10, cuadro_y + 100))
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

def mover_automaticamente(color, dado1, dado2):
    """
    Parámetros:
    color: Color del equipo al que pertenece la ficha
    dado1: Valor del primer dado.
    dado2: Valor del segundo dado.
    
    Mueve automáticamente una ficha si solo hay una opción posible.
    Retorna True si se realizó un movimiento automático, False si no.
    """
    fichas_disponibles = mostrar_fichas_disponibles(color)
    if len(fichas_disponibles) == 1:
        ficha_index = fichas_disponibles[0]
        pos_actual = fichas[color][ficha_index]
        opciones_validas = []
        for pasos in [dado1, dado2, dado1 + dado2]:
            if pos_actual in carceles[color] and pasos == 5:
                opciones_validas.append((ficha_index, 5))
            elif pos_actual not in carceles[color]:
                indice_camino = caminos[color].index(pos_actual) if isinstance(pos_actual, tuple) else pos_actual
                nuevo_indice = indice_camino + pasos
                if nuevo_indice < len(caminos[color]):
                    bloqueo_indice = hay_bloqueo_en_camino(color, indice_camino, pasos)
                    if bloqueo_indice is None and verificar_movimiento_llegada(color, nuevo_indice, pasos):
                        opciones_validas.append((ficha_index, pasos))
        if len(opciones_validas) == 1:
            ficha_index, pasos = opciones_validas[0]
            if pasos == 5 and fichas[color][ficha_index] in carceles[color]:
                sacar_ficha_de_carcel(color)
            else:
                mover_ficha(color, ficha_index, pasos)
            return True
    return False

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
            if movimientos_adicionales > 0:
                manejar_movimientos_adicionales(color)
            else:
                if modo_desarrollador:
                    screen.blit(tablero_img, (0, 0))
                    dibujar_fichas()
                    mostrar_texto(["Presione L para", "lanzar al azar", "Presione M para", "ingresar manualmente"], espera=True)
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

                if mover_automaticamente(color, dado1, dado2):
                    if verificar_dados_iguales(dado1, dado2):
                        mensaje = [f"¡Dados iguales!", f"El equipo {color}", "repite turno."]
                        mostrar_texto(mensaje)
                        print(" ".join(mensaje))
                        pares_consecutivos += 1
                    else:
                        pares_consecutivos = 0
                        turno = (turno + 1) % len(jugadores)
                        color = jugadores[turno]
                    manejar_tres_pares_consecutivos(color)
                    if not hay_movimientos_posibles(color, dado1, dado2):
                        mensaje = ["No hay movimientos", f"posibles para {color}.", "Turno pasa al", "siguiente."]
                        mostrar_texto(mensaje)
                        print(" ".join(mensaje))
                        turno = (turno + 1) % len(jugadores)
                        color = jugadores[turno]
                    continue

                if dado1 == 5 or dado2 == 5 or suma_dados == 5:
                    fichas_en_salida = [pos for pos in fichas[color] if pos == salidas[color]]
                    if len(fichas_en_salida) < 2:
                        ficha_sacada = sacar_ficha_de_carcel(color)
                        if ficha_sacada:
                            print(f"¡Se sacó una ficha de la cárcel con un 5!")
                            fichas_disponibles = mostrar_fichas_disponibles(color)
                            if fichas_disponibles:
                                while True:
                                    ficha_seleccionada = seleccionar_ficha(color, fichas_disponibles)
                                    if ficha_seleccionada is None or not running:
                                        mensaje = ["No seleccionó una", "ficha válida.", "Turno perdido."]
                                        mostrar_texto(mensaje)
                                        print(" ".join(mensaje))
                                        break
                                    pasos = seleccionar_dado(dado1, dado2)
                                    if mover_ficha(color, ficha_seleccionada, pasos):
                                        if pasos in [dado1, dado2] and pasos != suma_dados:
                                            fichas_disponibles = mostrar_fichas_disponibles(color)
                                            if fichas_disponibles:
                                                while True:
                                                    ficha_seleccionada = seleccionar_ficha(color, fichas_disponibles)
                                                    if ficha_seleccionada is None or not running:
                                                        mensaje = ["No seleccionó una", "ficha válida.", "Segundo movimiento", "perdido."]
                                                        mostrar_texto(mensaje)
                                                        print(" ".join(mensaje))
                                                        break
                                                    pasos_restantes = dado2 if pasos == dado1 else dado1
                                                    if mover_ficha(color, ficha_seleccionada, pasos_restantes):
                                                        break
                                                    else:
                                                        fichas_disponibles.remove(ficha_seleccionada)
                                                        if not fichas_disponibles:
                                                            mensaje = ["No hay más", "fichas disponibles.", "Segundo movimiento", "perdido."]
                                                            mostrar_texto(mensaje)
                                                            print(" ".join(mensaje))
                                                            break
                                        break
                                    else:
                                        fichas_disponibles.remove(ficha_seleccionada)
                                        if not fichas_disponibles:
                                            mensaje = ["No hay más", "fichas disponibles.", "Turno perdido."]
                                            mostrar_texto(mensaje)
                                            print(" ".join(mensaje))
                                            break
                        else:
                            fichas_disponibles = mostrar_fichas_disponibles(color)
                            if fichas_disponibles:
                                while True:
                                    ficha_seleccionada = seleccionar_ficha(color, fichas_disponibles)
                                    if ficha_seleccionada is None or not running:
                                        mensaje = ["No seleccionó una", "ficha válida.", "Turno perdido."]
                                        mostrar_texto(mensaje)
                                        print(" ".join(mensaje))
                                        break
                                    pasos = seleccionar_dado(dado1, dado2)
                                    if mover_ficha(color, ficha_seleccionada, pasos):
                                        if pasos in [dado1, dado2] and pasos != suma_dados:
                                            fichas_disponibles = mostrar_fichas_disponibles(color)
                                            if fichas_disponibles:
                                                while True:
                                                    ficha_seleccionada = seleccionar_ficha(color, fichas_disponibles)
                                                    if ficha_seleccionada is None or not running:
                                                        mensaje = ["No seleccionó una", "ficha válida.", "Segundo movimiento", "perdido."]
                                                        mostrar_texto(mensaje)
                                                        print(" ".join(mensaje))
                                                        break
                                                    pasos_restantes = dado2 if pasos == dado1 else dado1
                                                    if mover_ficha(color, ficha_seleccionada, pasos_restantes):
                                                        break
                                                    else:
                                                        fichas_disponibles.remove(ficha_seleccionada)
                                                        if not fichas_disponibles:
                                                            mensaje = ["No hay más", "fichas disponibles.", "Segundo movimiento", "perdido."]
                                                            mostrar_texto(mensaje)
                                                            print(" ".join(mensaje))
                                                            break
                                        break
                                    else:
                                        fichas_disponibles.remove(ficha_seleccionada)
                                        if not fichas_disponibles:
                                            mensaje = ["No hay más", "fichas disponibles.", "Turno perdido."]
                                            mostrar_texto(mensaje)
                                            print(" ".join(mensaje))
                                            break
                    else:
                        mensaje = [f"¡Hay dos fichas", f"en la salida de", f"{color}! No se", "puede sacar otra."]
                        mostrar_texto(mensaje)
                        print(" ".join(mensaje))
                        fichas_disponibles = mostrar_fichas_disponibles(color)
                        if fichas_disponibles:
                            while True:
                                ficha_seleccionada = seleccionar_ficha(color, fichas_disponibles)
                                if ficha_seleccionada is None or not running:
                                    mensaje = ["No seleccionó una", "ficha válida.", "Turno perdido."]
                                    mostrar_texto(mensaje)
                                    print(" ".join(mensaje))
                                    break
                                pasos = seleccionar_dado(dado1, dado2)
                                if mover_ficha(color, ficha_seleccionada, pasos):
                                    if pasos in [dado1, dado2] and pasos != suma_dados:
                                        fichas_disponibles = mostrar_fichas_disponibles(color)
                                        if fichas_disponibles:
                                            while True:
                                                ficha_seleccionada = seleccionar_ficha(color, fichas_disponibles)
                                                if ficha_seleccionada is None or not running:
                                                    mensaje = ["No seleccionó una", "ficha válida.", "Segundo movimiento", "perdido."]
                                                    mostrar_texto(mensaje)
                                                    print(" ".join(mensaje))
                                                    break
                                                pasos_restantes = dado2 if pasos == dado1 else dado1
                                                if mover_ficha(color, ficha_seleccionada, pasos_restantes):
                                                    break
                                                else:
                                                    fichas_disponibles.remove(ficha_seleccionada)
                                                    if not fichas_disponibles:
                                                        mensaje = ["No hay más", "fichas disponibles.", "Segundo movimiento", "perdido."]
                                                        mostrar_texto(mensaje)
                                                        print(" ".join(mensaje))
                                                        break
                                    break
                                else:
                                    fichas_disponibles.remove(ficha_seleccionada)
                                    if not fichas_disponibles:
                                        mensaje = ["No hay más", "fichas disponibles.", "Turno perdido."]
                                        mostrar_texto(mensaje)
                                        print(" ".join(mensaje))
                                        break
                else:
                    fichas_disponibles = mostrar_fichas_disponibles(color)
                    if fichas_disponibles:
                        while True:
                            ficha_seleccionada = seleccionar_ficha(color, fichas_disponibles)
                            if ficha_seleccionada is None or not running:
                                mensaje = ["No seleccionó una", "ficha válida.", "Turno perdido."]
                                mostrar_texto(mensaje)
                                print(" ".join(mensaje))
                                break
                            pasos = seleccionar_dado(dado1, dado2)
                            if mover_ficha(color, ficha_seleccionada, pasos):
                                if pasos in [dado1, dado2] and pasos != suma_dados:
                                    fichas_disponibles = mostrar_fichas_disponibles(color)
                                    if fichas_disponibles:
                                        while True:
                                            ficha_seleccionada = seleccionar_ficha(color, fichas_disponibles)
                                            if ficha_seleccionada is None or not running:
                                                mensaje = ["No seleccionó una", "ficha válida.", "Segundo movimiento", "perdido."]
                                                mostrar_texto(mensaje)
                                                print(" ".join(mensaje))
                                                break
                                            pasos_restantes = dado2 if pasos == dado1 else dado1
                                            if mover_ficha(color, ficha_seleccionada, pasos_restantes):
                                                break
                                            else:
                                                fichas_disponibles.remove(ficha_seleccionada)
                                                if not fichas_disponibles:
                                                    mensaje = ["No hay más", "fichas disponibles.", "Segundo movimiento", "perdido."]
                                                    mostrar_texto(mensaje)
                                                    print(" ".join(mensaje))
                                                    break
                                break
                            else:
                                fichas_disponibles.remove(ficha_seleccionada)
                                if not fichas_disponibles:
                                    mensaje = ["No hay más", "fichas disponibles.", "Turno perdido."]
                                    mostrar_texto(mensaje)
                                    print(" ".join(mensaje))
                                    break

                if verificar_dados_iguales(dado1, dado2):
                    mensaje = [f"¡Dados iguales!", f"El equipo {color}", "repite turno."]
                    mostrar_texto(mensaje)
                    print(" ".join(mensaje))
                    pares_consecutivos += 1
                else:
                    pares_consecutivos = 0
                    turno = (turno + 1) % len(jugadores)
                    color = jugadores[turno]

                manejar_tres_pares_consecutivos(color)

                if not hay_movimientos_posibles(color, dado1, dado2):
                    mensaje = ["No hay movimientos", f"posibles para {color}.", "Turno pasa al", "siguiente."]
                    mostrar_texto(mensaje)
                    print(" ".join(mensaje))
                    turno = (turno + 1) % len(jugadores)
                    color = jugadores[turno]

    pygame.draw.rect(screen, WHITE, (scaled_width - 153, 141, 145, 145))
    pygame.draw.rect(screen, WHITE, (scaled_width - 153, 317.5, 145, 145))
    if mostrar_dados:
        text1 = font.render(str(dado1), True, BLACK)
        text2 = font.render(str(dado2), True, BLACK)
        screen.blit(text1, (scaled_width - 115, 141))
        screen.blit(text2, (scaled_width - 115, 317.5))

    if movimientos_adicionales > 0:
        fuente = pygame.font.Font(None, 30)
        texto_surface = fuente.render(f"Movimientos adicionales: {movimientos_adicionales}", True, BLACK)
        screen.blit(texto_surface, (10, 10))

    pygame.display.flip()
    clock.tick(30)

pygame.quit()
