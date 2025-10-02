# Actividad 2: Fuentes con memoria 

import numpy as np
import random 
import codecs


""" CADENA DE MARKOV """

# T=np.array([[0.3,0,0.7],
#             [0.5,0.5,0],
#             [0.3,0.7,0]])

# print(np.array([[1,0,0]])@T)

# print(np.linalg.matrix_power(T,100))  # T@T@T@T..... n veces

# Ctrl k + Ctrl c para comentar todas las lineas seleccionadas

################################################################################

""" TABLA DE MARKOV """

with open("C:/Users/Usuario/SISCOM DIGITAL/donquijote.txt", "r", encoding="utf-8") as f:
    texto = f.read()   # Lee todo el texto

    
def markov_analiza_por_caracteres(texto, nletras_estado):
    tabla = dict()
    estado = tuple()
    
    for c in texto + texto[:nletras_estado]:    # Le agrego +... para que no haya estados iniciales o sin salidas
        if len(estado) < nletras_estado:
            estado = estado + (c,)
            continue
        if estado not in tabla:
            tabla[estado] = {c:1}
        elif c in tabla[estado]:
            tabla[estado][c] += 1
        else:
            tabla[estado][c] = 1
            
        estado = estado[1:] + (c,)       
            
    return tabla

# tabla = markov_analiza_por_caracteres(texto,3)
# print (tabla)


""" Rutina de simulación de fuente discreta con memoria a partir de su tabla de frecuencias de símbolos."""

def simular_fuente_con_memoria(tabla, estado_inicial, longitud):
    salida = []
    estado = estado_inicial

    for _ in range(longitud):
        if estado not in tabla:
            break  # Si el estado no está en la tabla, cortamos

        simbolos = list(tabla[estado].keys())   # Posibles siguientes símbolos
        pesos = list(tabla[estado].values())    # Frecuencias como pesos

        siguiente = random.choices(simbolos, pesos, k=1)[0]  # Elegimos según probabilidad // Choices me devuelve una lista
        salida.append(siguiente)

        # Avanza al próximo estado
        estado = estado[1:] + (siguiente,)

    return "".join(salida)


# PROBAR
# Generar tabla desde Don Quijote
# tabla = markov_analiza_por_caracteres(texto,4)

# Definir estado inicial (por ejemplo, los 3 primeros caracteres del texto)
# estado_inicial = tuple(texto[:4])

# Simular una secuencia 
cadena = simular_fuente_con_memoria(tabla, estado_inicial,1000)
print(cadena)




################################################################################

# Lempel–Ziv:

# No necesita probabilidades (es universal)
# Aprende las estadísticas “sobre la marcha” (va construyendo su propio diccionario dinámico)
# Aprovecha la dependencia de largo plazo de la fuente (cada nueva frase se representa en términos de una referencia a una frase anterior + un carácter nuevo)

#1 Lectura secuencial: Se lee la fuente símbolo por símbolo (puede ser texto, bits, etc.)
#2 Diccionario de frases: Se mantiene una lista de frases que ya han aparecido. Cada frase tiene un índice en el diccionario
#3 Codificación de nueva frase: Si la secuencia actual no está en el diccionario, se añade como frase nueva
#5 Para codificarla, se envía: El índice de la frase más larga previa que coincide, seguido del nuevo símbolo que la extiende
#6 Decodificación: El receptor reconstruye el mensaje manteniendo el mismo diccionario en paralelo. Dado un índice y un símbolo, puede recuperar la frase original

# Variante: LZ77: usa una ventana deslizante sobre el texto y codifica en forma (desplazamiento, longitud, símbolo)
# El algoritmo trabaja con una ventana deslizante que contiene dos partes:
# Buffer de búsqueda: contiene los últimos símbolos ya procesados.
# Buffer de entrada: contiene los siguientes símbolos aún no procesados.
# Representación de un símbolo: Cada salida del LZ77 se codifica como (length, offset, next_symbol) donde:
# length (longitud): cuántos símbolos coinciden (cod unario-binario) (se transmite primero)
# offset (desplazamiento): cuántos símbolos hacia atrás en el buffer de búsqueda se encuentra la coincidencia (cod binario longitud fija)
# next_symbol: el símbolo que sigue después de la coincidencia (para continuar la reconstrucción)


################################################################################


#------------ FUNCIONES AUXILIARES ------------

def literal(caracter):    # sourcery skip: for-append-to-extend
    cod = ["1"]
    
    for B in codecs.encode(caracter):
        cod.append(f"{B:08b}")
    
    return "".join(cod)


def decod_literal(cod, indice, salida):
    
    if cod[indice] != "1":
        return indice
    
    if cod.startswith("0", indice+1):
        x = bytes((int(cod[indice+1:indice+9],2),))
        salida.append(codecs.decode(x, "utf-8"))
        return indice+9
    
    elif cod.startswith("110", indice+1):    
        x = bytes((int(cod[indice+1:indice+9], 2),
                int(cod[indice+9:indice+17], 2),))
        salida.append(codecs.decode(x, "utf-8"))
        return indice+17
    
    elif cod.startswith("1110", indice+1):
        x = bytes((int(cod[indice+1:indice+9], 2),
                int(cod[indice+9:indice+17], 2),
                int(cod[indice+17:indice+25], 2),))
        salida.append(codecs.decode(x, "utf-8"))
        return indice+25
    
    elif cod.startswith("11110", indice+1):
        x = bytes((int(cod[indice+1:indice+9], 2),
                int(cod[indice+9:indice+17], 2),
                int(cod[indice+17:indice+25], 2),
                int(cod[indice+25:indice+33], 2),))
        salida.append(codecs.decode(x, "utf-8"))
        return indice+33
    
    else:
        return ValueError("Error: Prefijo utf-8 no reconocido")    

    
def buscar_coincidencia(texto, indice, tamaño_ventana):
    longitud_max = 0
    inicio_max = 0
    inicio = 0
    
    while inicio < tamaño_ventana and inicio < indice:       # indice-1-inicio >=0 --> inicio <= indice-1     (tengo que ir cambiando los primeros valores max)
        longitud = 0
        pos = indice-1-inicio
        
        while texto[pos:pos+longitud+1] == texto[indice:indice+longitud+1]:
            longitud +=1
        
        if longitud > longitud_max:
            longitud_max = longitud 
            inicio_max = inicio
        inicio += 1
    
    return (longitud_max, inicio_max)   


def inserta_coincidencia(salida, longitud, inicio):
    k = len(salida) - 1
    pos = len(salida[k]) - 1
    
    while pos < inicio:
        k -= 1
        pos += len(salida[k])
    coincidencia = salida[k][pos-inicio:]
    k += 1
    while len(coincidencia) < longitud and k < len(salida):
        coincidencia += salida[k]
        k += 1
    if len(coincidencia) < longitud:
        k = len(coincidencia)
        coincidencia = coincidencia * ((longitud+(k-1))//k)
    
    salida.append(coincidencia[:longitud])
            


#------------ COMPRESOR ------------

def lz77_compresor(texto, tamaño_ventana):
    indice = 0
    salida = []
    nbits_inicio = (tamaño_ventana-1).bit_length()
    nbits_literal_minimo = 9
    
    while indice < len(texto):
        longitud, inicio = buscar_coincidencia(texto, indice, tamaño_ventana)
        nbits_longitud = longitud.bit_length() * 2 - 1
        if longitud > 1 and nbits_longitud + nbits_inicio < longitud * nbits_literal_minimo:
            codigo_coincidencia = f"{longitud:0{nbits_longitud}b}{inicio:0{nbits_inicio}b}"
            salida.append(codigo_coincidencia)
            indice += longitud
        else:    
            salida_bits = literal(texto[indice])
            salida.append(salida_bits)
            indice += 1 
    
    return "".join(salida)
    

#------------ DECOMPRESOR ------------

def lz77_decompresor(cod, tamaño_ventana):
    indice = 0
    salida = []
    nbits_inicio = (tamaño_ventana-1).bit_length()

    while indice < len(cod):
        if cod[indice] == "0":      # Si empieza con 0 es una coincidencia 
            nbits_longitud = 1
            while cod[indice] == "0":
                nbits_longitud += 1
                indice += 1
            longitud = int(cod[indice:indice+nbits_longitud], 2)
            indice += nbits_longitud
            inicio = int(cod[indice:indice+nbits_inicio], 2)
            indice += nbits_inicio
            inserta_coincidencia(salida, longitud, inicio)
        elif cod[indice] == "1":    # Si empieza con 1 es un literal    
            indice = decod_literal(cod, indice, salida)
        else:
            return ValueError("Error: Valor distinto de 0 o 1") 
        
    return "".join(salida)


# PROBAR 
texto = "hola aloh"
compresor = lz77_compresor(texto, 16)
print(compresor)
decompresor = lz77_decompresor(compresor, 16)
print(decompresor)

