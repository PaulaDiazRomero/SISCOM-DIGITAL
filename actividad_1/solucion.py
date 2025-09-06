# Actividad 1: Fuentes discretas

from random import choices     # Para muestreo aleatorio ponderado


""" Una rutina de simulación de fuente discreta sin memoria (Discrete Memoryless Source, DMS)
a partir de su tabla de frecuencias de símbolos. """

def fuente(tabla):     # Crea una fuente discreta sin memoria a partir de {símbolo: frecuencia}

    simbolos = list(tabla.keys())     # Lista de símbolos
    frecs    = list(tabla.values())   # Lista de frecuencias

    def f(cantidad):     # Genera "cantidad" símbolos según la distribución dada
        secuencia = choices(simbolos, weights=frecs, k=cantidad)  # Muestreo con reemplazo
        return "".join(map(str, secuencia))  # Concatena símbolos como string

    return f   # Se devuelve la función generadora


""" Una rutina de análisis de frecuencias que estime en base a la salida de una fuente su tabla de frecuencias. """

def contar_frecuencias(secuencia):     # Cuenta cuántas veces aparece cada símbolo en una secuencia
    
    # Parámetro: secuencia : str o lista
    # Devuelve: frecs : diccionario {símbolo: cantidad de apariciones}
    
    frecs = {}  # Crea un diccionario vacío para acumular los conteos

    for s in secuencia:        # Recorre cada símbolo de la secuencia
        if s in frecs:              
            frecs[s] += 1      # Sumamos 1 a su contador si ya lo vimos antes
        else:                       
            frecs[s] = 1       # Inicializamos su contador en 1 si aparece una vez

    return frecs  # Devuelve el diccionario con los conteos


""" Una rutina que genere, en base a la tabla de frecuencias de una DMS un arbol de Huffman óptimo para dicha fuente. """

def huffman(frecs):     # Genera un árbol de Huffman a partir de la tabla de frecuencias
    
    # Parámetro: frecs : diccionario {símbolo: frecuencia}
    # Devuelve: arbol : lista anidada
    
    # Crea una lista de nodos como [[simbolo], frecuencia]
    nodos = [[[sim], freq] for sim, freq in frecs.items()]  # Cada nodo es una decisión

    # Iteramos hasta que quede un solo árbol
    while len(nodos) > 1:
        nodos = sorted(nodos, key=lambda x: x[1])    # Ordenamos los nodos por frecuencia ascendente para ver cuáles son los de menor frecuencia

        # Tomamos los dos nodos con menor frecuencia
        a = nodos.pop(0)
        b = nodos.pop(0)
        
        nuevo = [ [a[0], b[0]], a[1] + b[1] ]    # Combinamos en un nuevo nodo 
        nodos.append(nuevo)                      # Volvemos a agregarlo a la lista de nodos

    return nodos[0][0]    # Devuelve la parte de los símbolos (del nodo final que contiene la estructura del árbol )


""" Una rutina que, dado un arbol de decisión genere una tabla de códigos """

def tabla_codigo(arbol, prefijo=""):     # Genera un diccionario de códigos binarios (tabla) a partir del árbol de Huffman
    
    # Parámetro: arbol : lista anidada
    # Devuelve: tabla : diccionario {símbolo: código binario}
    
    n = len(arbol)   # Cantidad de elementos en el nodo actual
    
    match n:
        case 2:  
            # Nodo interno/subárbol: tiene hijo izquierdo y derecho
            izquierda = tabla_codigo(arbol[0], prefijo + "0")  # Recorre izquierda, concatenamos prefijo '0'
            derecha = tabla_codigo(arbol[1], prefijo + "1")    # Recorre derecha, concatenamos prefijo '1'
            return izquierda | derecha                         # Une los diccionarios
        case 1:
            # Nodo hoja: contiene directamente el símbolo
            return {arbol[0]: prefijo}
        case 0:
            # Nodo vacío
            return dict()    # Devuelve un diccionario vacío
        case _:
            # Cualquier otro caso
            raise ValueError("Árbol mal formado")    # Devuelve error


""" Rutinas de codificación y decodificación, que traduzcan entre símbolos de fuente y su codificación binaria. """

def codificador(tabla):    # Tabla: dict {símbolo: código}
    def cod(secuencia):
        bits = []                              # Acumulador de códigos
        for x in secuencia:                    # Recorre cada símbolo
            if x not in tabla:                 # Valida símbolo conocido
                raise ValueError(f"Símbolo desconocido: {x!r}")
            bits.append(tabla[x])              # Agrega su código
        return "".join(bits)                   # Concatena todo en una tira binaria
    return cod                                 # Devuelve la función codificadora


def decodificador(arbol):   # Arbol: estructura anidada 
    def dec(cadena):
        simbolos = []                           # Salida decodificada
        pos = arbol                             # Puntero en la raíz
        for b in cadena:                        # Recorre cada bit
            if b == '0':                        # 0 → va hacia la izquierda
                pos = pos[0]
            elif b == '1':                      # 1 → va hacia la derecha
                pos = pos[1]
            else:
                raise ValueError('Sólo son válidos "0" y "1"')  # Bit inválido

            n = len(pos)                        # Tamaño del nodo actual
            if n == 2:                          # Nodo interno/subárbol → sigue leyendo
                continue
            elif n == 1:                        # Hoja → se obtuvo un símbolo
                simbolos.append(pos[0])         # Agrega el símbolo
                pos = arbol                     # Vuelve a la raíz para el próximo
            elif n == 0:                        # Nodo vacío → árbol inconsistente
                raise ValueError("Palabra inválida")
            else:                               
                raise ValueError("Árbol mal formado")  # Estructura inesperada

        if pos != arbol:                        # Si terminó a mitad de un código
            raise ValueError("Palabra inválida")

        return "".join(simbolos)                # Devuelve la palabra decodificada
    return dec                                  # Devuelve la función decodificadora


