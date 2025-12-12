from typing import NamedTuple 
from datetime import datetime, date, time 
import csv
from collections import defaultdict
Vuelo = NamedTuple("Vuelo",      
  [("operador", str), # Compañía aérea que operaba el vuelo (opcional) 
   ("codigo", str),   # Código de vuelo (opcional) 
   ("ruta", str),     # Ruta del vuelo (opcional) 
   ("modelo", str)])  # Modelo de avión que operaba el vuelo (opcional) 
 
Desastre = NamedTuple("Desastre",      
  [("fecha", date),               # Fecha del desastre aéreo 
    ("hora", time | None),        # Hora del desastre (opcional) 
    ("localizacion", str),        # Localización del desastre 
    ("supervivientes",int),       # Supervivientes 
    ("fallecidos",int),           # Fallecidos     
    ("fallecidos_en_tierra",int), # Fallecidos en tierra (no eran pasajeros del vuelo) 
    ("operacion",str),        # Momento operativo del vuelo cuando ocurrió el desastre 
    ("vuelos", list[Vuelo])]) # Vuelos implicados en el desastre


def lee_desastres(fichero:str)->list[Desastre]:
    lista_desastres = []
    with open(fichero, encoding='utf-8') as f:
        lector = csv.reader(f, delimiter=';')
        next(lector)  # Saltar la cabecera
        for fila in lector:
            fecha = parsea_fecha(fila[0])
            hora = parsea_hora(fila[1])
            localizacion = fila[2]  
            supervivientes = int(fila[7])
            fallecidos = int(fila[8])
            fallecidos_en_tierra = int(fila[9])
            operacion = fila[10]
            vuelos = parsea_vuelos(fila[3], fila[4], fila[5], fila[6])
            desastre = Desastre(fecha, hora, localizacion, supervivientes, fallecidos, fallecidos_en_tierra, operacion, vuelos)
            
            
            lista_desastres.append(desastre)
    return lista_desastres

def parsea_fecha(fecha:str) -> date:
    return datetime.strptime(fecha, "%d/%m/%Y").date()

def parsea_hora(hora:str) -> time|None:
    if hora == "":
        return None
    return datetime.strptime(hora, "%H:%M").time()

def parsea_vuelos(operadores:str, codigos:str, rutas:str,modelos:str) -> list[Vuelo]:
    lista_vuelos = []
    operadores_list = operadores.split('/')   
    codigos_list = codigos.split('/')
    rutas_list = rutas.split('/')
    modelos_list = modelos.split('/')
    for operador, codigo, ruta, modelo in zip(operadores_list, codigos_list, rutas_list, modelos_list):
        vuelo = Vuelo(operador, codigo, ruta, modelo)
        lista_vuelos.append(vuelo)
    return lista_vuelos


"""
dada  una  lista  desastres  de  tuplas  de  tipo  Desastre  y  un 
número que por defecto tomará el valor None, debe devolver una lista ordenada de tuplas (localización, fecha 
y  hora  del  desastre,  fallecidos  en  tierra)  de  aquellos  desastres  que  resultaron  con  fallecidos  en  tierra,  que  no 
eran  pasajeros  de  las  aeronaves  afectadas.  Esta  lista  se  presentará  en  orden  descendente  y  el  resultado  se 
limitará a los peores “n” desastres, es decir, aquéllos en los que hubo más fallecidos en tierra.
"""
def desastres_con_fallecidos_en_tierra(desastres:list[Desastre],n:int|None=None)->list[tuple[str,date,time,int]]:
    lista_desastres_tierra = []
    for desastre in desastres:
        if desastre.fallecidos_en_tierra > 0:
            lista_desastres_tierra.append((desastre.localizacion, desastre.fecha, desastre.hora, desastre.fallecidos_en_tierra))
    return sorted(lista_desastres_tierra, key = lambda x:x[3], reverse = True)[:n]

"""
dada  una  lista  desastres  de  tuplas  de  tipo  Desastre,  debe  devolver  una  tupla 
(década, número de desastres con colisiones) correspondiente a la década donde se produjeron mayor número 
de desastres que implicaron a 2 o más vuelos.
"""
def decada_mas_colisiones(desastres:list[Desastre]) -> tuple[int,int]:
    decadas = defaultdict(int)

    for desastre in desastres:
        if len(desastre.vuelos) >= 2:  # colisión: 2 o más vuelos
            decada = (desastre.fecha.year // 10) * 10
            decadas[decada] += 1

    return max(decadas.items(), key=lambda x: x[1])