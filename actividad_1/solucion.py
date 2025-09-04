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


""" Una rutina de análisis de frecuencias que estime en base a la salida de una fuente su
tabla de frecuencias. """

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


""" Una rutina que genere, en base a la tabla de frecuencias de una DMS un arbol de
Huffman óptimo para dicha fuente. """

def huffman(frecs):     # Genera un árbol de Huffman a partir de la tabla de frecuencias
    
    # Parámetro: frecs : diccionario {símbolo: frecuencia}
    # Devuelve: arbol : lista anidada
    
    # Crea una lista de nodos como [frecuencia, símbolo] 
    nodos = [[freq, [sim]] for sim, freq in frecs.items()]  # Cada nodo es una decisión  """ EL PROFE HACE AL REVES [sim], freq y abajo toma x[1]"""

    # Iteramos hasta que quede un solo árbol
    while len(nodos) > 1:
        nodos = sorted(nodos, key=lambda x: x[0])    # Ordenamos los nodos por frecuencia ascendente para ver cuáles son los de menor frecuencia

        # Tomamos los dos nodos con menor frecuencia
        a = nodos.pop(0)
        b = nodos.pop(0)
        
        nuevo = [a[0] + b[0], [a[1], b[1]]]    # Combinamos en un nuevo nodo """ver nombre nuevo"""
        nodos.append(nuevo)                    # Volvemos a agregarlo a la lista de nodos

    return nodos[0][1]    # Devuelve el nodo final que contiene la estructura del árbol (las decisiones)


""" Una rutina que, dado un arbol de decisión genere una tabla de códigos """

def tabla_codigo(arbol, prefijo=""):     # Genera un diccionario de códigos binarios a partir del árbol de Huffman
    
    # Parámetro: arbol : lista anidada; prefijo : str
    # Devuelve: tabla : diccionario {símbolo: código binario}
    
    # Si el árbol es un símbolo (hoja), devolvemos su código
    if isinstance(arbol, str):
        return {arbol: prefijo}

    # Si es un subárbol, concatenamos prefijo '0' a la izquierda y '1' a la derecha
    izquierda = tabla_codigo(arbol[0], prefijo + "0")
    derecha = tabla_codigo(arbol[1], prefijo + "1")

    # Combinamos ambos diccionarios y devolvemos
    izquierda.update(derecha)
    return izquierda

"""CORREGIR tabla"""

def tabla_codigo(arbol, prefijo=""):
    
    arboles = []
    return len(arboles)