import math

# Constantes
JUGADOR_X = 'X'
JUGADOR_O = 'O'
VACIO = '-'

# Crear un tablero vacío 4x4
def crear_tablero():
    return [[VACIO for _ in range(4)] for _ in range(4)]

# Imprimir el tablero
def imprimir_tablero(tablero):
    for fila in tablero:
        print(' '.join(fila))
    print()

# Verificar si el tablero está lleno
def tablero_lleno(tablero):
    return all(celda != VACIO for fila in tablero for celda in fila)

# Función para verificar si un jugador ha ganado (4 en línea)
def verificar_ganador(tablero, jugador):
    # Verificar filas, columnas y diagonales
    for i in range(4):
        # Filas
        if all(tablero[i][j] == jugador for j in range(4)):
            return True
        # Columnas
        if all(tablero[j][i] == jugador for j in range(4)):
            return True

    # Diagonales
    if all(tablero[i][i] == jugador for i in range(4)):
        return True
    if all(tablero[i][3-i] == jugador for i in range(4)):
        return True
    
    return False


# Función heurística (cuenta líneas parciales)
def evaluar_tablero(tablero):
    if verificar_ganador(tablero, JUGADOR_X):
        return 100
    elif verificar_ganador(tablero, JUGADOR_O):
        return -100
    else:
        return 0  # Empate o estado no decisivo

# Minimax con poda alfa-beta
def minimax(tablero, profundidad, alfa, beta, es_maximizador):
    evaluacion = evaluar_tablero(tablero)
    
    # Caso terminal: victoria, derrota o empate
    if evaluacion == 100 or evaluacion == -100 or tablero_lleno(tablero):
        return evaluacion

    if profundidad == 0:  # Limitar la profundidad
        return evaluar_tablero(tablero)  # Evaluar el estado intermedio

    if es_maximizador:
        max_eval = -math.inf
        for i in range(4):
            for j in range(4):
                if tablero[i][j] == VACIO:
                    tablero[i][j] = JUGADOR_X
                    evaluacion = minimax(tablero, profundidad-1, alfa, beta, False)
                    tablero[i][j] = VACIO
                    max_eval = max(max_eval, evaluacion)
                    alfa = max(alfa, evaluacion)
                    if beta <= alfa:
                        break
        return max_eval
    else:
        min_eval = math.inf
        for i in range(4):
            for j in range(4):
                if tablero[i][j] == VACIO:
                    tablero[i][j] = JUGADOR_O
                    evaluacion = minimax(tablero, profundidad-1, alfa, beta, True)
                    tablero[i][j] = VACIO
                    min_eval = min(min_eval, evaluacion)
                    beta = min(beta, evaluacion)
                    if beta <= alfa:
                        break
        return min_eval

# Función para la IA (jugador O)
def mejor_movimiento(tablero, jugador):
    mejor_valor = -math.inf if jugador == JUGADOR_X else math.inf
    mejor_movimiento = None
    
    for i in range(4):
        for j in range(4):
            if tablero[i][j] == VACIO:
                tablero[i][j] = jugador
                valor_movimiento = minimax(tablero, 5, -math.inf, math.inf, jugador == JUGADOR_O)
                tablero[i][j] = VACIO
                if (jugador == JUGADOR_X and valor_movimiento > mejor_valor) or (jugador == JUGADOR_O and valor_movimiento < mejor_valor):
                    mejor_valor = valor_movimiento
                    mejor_movimiento = (i, j)
                    
    return mejor_movimiento

# Validar entrada del jugador
def obtener_coordenadas_validas(tablero):
    while True:
        try:
            fila, col = map(int, input("Introduce fila y columna (0-3): ").split())
            if fila < 0 or fila > 3 or col < 0 or col > 3:
                print("Coordenadas fuera de rango. Deben estar entre 0 y 3.")
            elif tablero[fila][col] != VACIO:
                print("Casilla ocupada. Elige otra coordenada.")
            else:
                return fila, col
        except ValueError:
            print("Entrada inválida. Introduce dos números separados por un espacio.")

# Modos de juego
def humano_vs_humano():
    tablero = crear_tablero()
    jugador_actual = JUGADOR_X
    while True:
        imprimir_tablero(tablero)
        print(f"Turno de {jugador_actual}")
        fila, col = obtener_coordenadas_validas(tablero)
        tablero[fila][col] = jugador_actual
        if verificar_ganador(tablero, jugador_actual):
            imprimir_tablero(tablero)
            print(f"Jugador {jugador_actual} gana!")
            break
        elif tablero_lleno(tablero):
            imprimir_tablero(tablero)
            print("Empate!")
            break
        jugador_actual = JUGADOR_O if jugador_actual == JUGADOR_X else JUGADOR_X

def humano_vs_ia():
    tablero = crear_tablero()
    jugador_actual = JUGADOR_X
    while True:
        imprimir_tablero(tablero)
        if jugador_actual == JUGADOR_X:
            print("Turno de Humano (X)")
            fila, col = obtener_coordenadas_validas(tablero)
            tablero[fila][col] = JUGADOR_X
            if verificar_ganador(tablero, JUGADOR_X):
                imprimir_tablero(tablero)
                print(f"Jugador {JUGADOR_X} gana!")
                break
            elif tablero_lleno(tablero):
                imprimir_tablero(tablero)
                print("Empate!")
                break
        else:
            print("Turno de IA (O)")
            mov = mejor_movimiento(tablero, JUGADOR_O)
            if mov:
                tablero[mov[0]][mov[1]] = JUGADOR_O
                if verificar_ganador(tablero, JUGADOR_O):
                    imprimir_tablero(tablero)
                    print("La IA gana!")
                    break
                elif tablero_lleno(tablero):
                    imprimir_tablero(tablero)
                    print("Empate!")
                    break
        jugador_actual = JUGADOR_O if jugador_actual == JUGADOR_X else JUGADOR_X

def ia_vs_ia():
    tablero = crear_tablero()
    jugador_actual = JUGADOR_X
    while True:
        imprimir_tablero(tablero)
        mov = mejor_movimiento(tablero, jugador_actual)
        if mov:
            tablero[mov[0]][mov[1]] = jugador_actual
            if verificar_ganador(tablero, jugador_actual):
                imprimir_tablero(tablero)
                print(f"Jugador {jugador_actual} (IA) gana!")
                break
            elif tablero_lleno(tablero):
                imprimir_tablero(tablero)
                print("Empate!")
                break
        jugador_actual = JUGADOR_O if jugador_actual == JUGADOR_X else JUGADOR_X

# Ejecutar el modo de juego deseado
ia_vs_ia()