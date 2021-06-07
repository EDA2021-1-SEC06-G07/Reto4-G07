"""
 * Copyright 2020, Departamento de sistemas y Computación, Universidad
 * de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along withthis program.  If not, see <http://www.gnu.org/licenses/>.
 """

import config as cf
import sys
from App import controller
from DISClib.ADT import list as lt
import time
import tracemalloc
assert cf


"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""

def printMenu():
    print("Bienvenido")
    print("1- Crear catálogo")
    print("2- Cargar información en el cátalogo")
catalog = None

"""
Menu principal
"""
def getTime():
    return(float(time.perf_counter()*1000))

def getMemory():
    return tracemalloc.take_snapshot()

def deltaMemory(start_memory,stop_memory):
    memory_diff = stop_memory.compare_to(start_memory, "filename")
    delta_memory = 0.0
    for stat in memory_diff:
        delta_memory = delta_memory + stat. size_diff
    delta_memory = delta_memory/1024.0
    return delta_memory

def optionTwo(analyzer):
    print("\nCargando información  ....")
    controller.loadLanding_Points(analyzer)
    controller.loadConnection(analyzer)
    controller.loadCountries(analyzer)
    numvertex = controller.totalLanding_Points(analyzer)
    numarc = controller.totalArcs(analyzer)
    vert = controller.vertices(analyzer)
    countries = controller.CountrySize(analyzer)
    print('\n')
    print("********INORMACIÓN CARGADA********")
    print('\n')
    print('Número de vertices en el grafo: ' + str(numvertex))
    print('\n')
    print('Número de arcos en el grafo: ' + str(numarc))
    print('\n')
    print('Número de paises cargados:', countries)
    print('\n')
    prim_el = lt.firstElement(vert)
    mapinfo = controller.vertInfo(analyzer,prim_el)
    name = controller.getValue(mapinfo,'name')
    id = controller.getValue(mapinfo,'id')
    latitude = controller.getValue(mapinfo,'latitude')
    longitude = controller.getValue(mapinfo,'longitude')
    print("Información del primer Landing Point cargado:")
    print ("Nombre:",name)
    print("Identificador:",id)
    print("Latitude:", latitude)
    print("Longitude:",longitude)
    print('\n')
    country = controller.countries(analyzer)
    prim_country = lt.lastElement(country)
    country_info = controller.countryInfo(analyzer,prim_country)
    population = controller.getValue(country_info,'Population')
    users = controller.getValue(country_info,'Internet_Users')
    print("Información del último país cargado:")
    print("Nombre:", prim_country)
    print("Población:",population)
    print("Usuarios de Internet:", users)
    print('\n')

def optionThree(R1,lp1,lp2):
    infClst,rta = R1
    cant,pertenece = rta
    cls1,cls2 = infClst
    print('\n')
    print('***** Req No. 1 resultados *****')
    print()
    print(f'Cantidad de clústeres dentro de la red: {cant}')
    print()
    if pertenece:
        print(f'(+) Los landing Points {lp1} y {lp2} pertenecen al mismo clúster.')
    else:
        print(f'(-) Los landing Points {lp1} y {lp2} NO pertenecen al mismo clúster.')
    print()
    print(f'El landing Point {lndP1} pertenece al cluster {cls1}.')
    print(f'El landing Point {lndP2} pertenece al cluster {cls2}.')
    print('\n')
    
def optionFour(analyzer):
    edgess = controller.edge(analyzer["connections"])
    nameycables, cablest = controller.req_2(edgess)
    print(nameycables)
    print("\n")
    print("El total de cables conectados a estos Landing Points son:",cablest)

def optionFive(rta,p1,p2):
    print('\n')
    print('***** Req No. 3 resultados *****')
    print()

    if rta != None:
        ruta, costo = rta
        print(f'[Ruta]: {ruta}')
        print(f'[costo]: {costo}')
    else:
        print(f'No existe ruta mínima entre {paisA} y {paisB}')
    print() 

while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n')
    if int(inputs[0]) == 1:
        print('\n')
        print("Inicializando ....")
        print('\n')
        analyzer = controller.init()
    elif int(inputs[0]) == 2:
        tracemalloc.start()
        delta_time = -1.0
        delta_memory = -1.0
    
        start_time= getTime()
        start_memory = getMemory()
        
        optionTwo(analyzer)

        stop_time = getTime()
        stop_memory = getMemory()
        tracemalloc.stop()
        delta_time = stop_time - start_time
        delta_memory = deltaMemory(start_memory, stop_memory)
        print(delta_time, delta_memory)

    elif int(inputs[0]) == 3:
        lndP1 = str(input('Nombre Landing point 1: '))
        lndP2 = str(input('Nombre Landing point 2: '))
        tracemalloc.start()
        delta_time = -1.0
        delta_memory = -1.0
    
        start_time= getTime()
        start_memory = getMemory()
        
        R1 = controller.requerimiento1(analyzer["connections"],lndP1,lndP2,analyzer['landing_points'])

        stop_time = getTime()
        stop_memory = getMemory()
        tracemalloc.stop()
        delta_time = stop_time - start_time
        delta_memory = deltaMemory(start_memory, stop_memory)
        print(delta_time, delta_memory)
        optionThree(R1,lndP1,lndP2)
    elif int(inputs[0]) == 4:
        optionFour(analyzer)
    elif int(inputs[0]) == 5:
        paisA = str(input('Nombre del país origen: '))
        paisB = str(input('Nombre del país destino: '))
        tracemalloc.start()
        delta_time = -1.0
        delta_memory = -1.0
    
        start_time= getTime()
        start_memory = getMemory()
        
        rta = controller.requerimiento3(analyzer['connections'],paisA,paisB,analyzer['landing_points'],analyzer['countries'])

        stop_time = getTime()
        stop_memory = getMemory()
        tracemalloc.stop()
        delta_time = stop_time - start_time
        delta_memory = deltaMemory(start_memory, stop_memory)
        print(delta_time, delta_memory)
        optionFive(rta,paisA,paisB)

        
    else:
        sys.exit(0)
sys.exit(0)
    

    
