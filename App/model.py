"""
 * Copyright 2020, Departamento de sistemas y Computación,
 * Universidad de Los Andes
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
 *
 * Contribuciones:
 *
 * Dario Correal - Version inicial
 """


import config as cf
from DISClib.ADT import list as lt
from DISClib.ADT.graph import gr
from DISClib.ADT import map as mp
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Sorting import shellsort as sa
assert cf

def newAnalyzer():
    analyzer= {"connections": None,
             "countries": None,
             "landing_points": None
    }
        
    analyzer["countries"] = mp.newMap(numelements=10000,
                                          maptype="PROBING",
                                          comparefunction= None)
    analyzer["connections"] = gr.newGraph(datastructure='ADJ_LIST',
                                              directed= True,
                                              size= 10000,
                                              comparefunction= None
                                              )
    return analyzer

def addConnectionArc(analyzer, connection):
    print(connection)
    origen = connection["\ufefforigin"]
    destino = connection["destination"]
    longitud = connection["cable_length"]
    addLanding_point(analyzer,origen)
    addLanding_point(analyzer,destino)
    addConnection(analyzer,origen,destino,longitud)
    
    

def addLanding_point(analyzer,landing_point):
    """
    Adiciona un Landing point como vertice del grafo
    """
    try:
        if not gr.containsVertex(analyzer['connections'], landing_point):
            gr.insertVertex(analyzer['connections'], landing_point)
        return analyzer
    except Exception as exp:
        error.reraise(exp, 'model:addstop')
        

def addConnection(analyzer, origin, destination, distance):
    """
    Adiciona un arco entre dos estaciones
    """
    edge = gr.getEdge(analyzer['connections'], origin, destination)
    if edge is None:
        gr.addEdge(analyzer['connections'], origin, destination, distance)
    return analyzer


    
    

# Construccion de modelos

# Funciones para agregar informacion al catalogo

# Funciones para creacion de datos

# Funciones de consulta

# Funciones utilizadas para comparar elementos dentro de una lista

# Funciones de ordenamiento
