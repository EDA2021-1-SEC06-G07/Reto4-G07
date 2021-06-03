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


from DISClib.DataStructures.chaininghashtable import get
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
        
    analyzer["countries"] = mp.newMap(numelements=1000,
                                          maptype="PROBING",
                                          comparefunction= None)
    analyzer["connections"] = gr.newGraph(datastructure='ADJ_LIST',
                                              directed= True,
                                              size= 10000,
                                              comparefunction= None)
    analyzer["landing_points"] = mp.newMap(numelements= 4000,
                                           maptype= 'PROBING',
                                           loadfactor= 0.4,
                                           comparefunction= None)
    return analyzer

def addConnectionArc(analyzer, connection):
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
        
    

def totalLanding_Points(analyzer):
    "Retorna el número de landing points"
    return  gr.numVertices(analyzer["connections"])

def totalArcs(analyzer):
    "Retorna elnúmero de Arcos"
    return gr.numEdges(analyzer["connections"])
   
    

# Construccion de modelos

# Funciones para agregar informacion al catalogo
def addLandingPointMap(analyzer,landing_point):
    lp = analyzer["landing_points"]
    code = landing_point["landing_point_id"]
    info = mp.newMap(numelements= 4)
    mp.put(info,'id',landing_point["id"])
    mp.put(info,'name',landing_point["name"])
    mp.put(info,'latitude',landing_point["latitude"])
    mp.put(info,'longitude',landing_point["longitude"])
    mp.put(lp,code,info)

def addConnection(analyzer, origin, destination, distance):
    """
    Adiciona un arco entre dos landing points
    """
    edge = gr.getEdge(analyzer['connections'], origin, destination)
    if edge is None:
        gr.addEdge(analyzer['connections'], origin, destination, distance)
    return analyzer

def addCountry(analyzer,country):
    countries = analyzer["countries"]
    name = country["CountryName"]
    info = mp.newMap(numelements= 2)
    mp.put(info,'Population',country["Population"])
    mp.put(info,'Internet_Users',country["Internet users"])
    mp.put(countries,name,info)
    

# Funciones para creacion de datos

# Funciones de consulta
def vertices(analyzer):
    return gr.vertices(analyzer["connections"])
   
def vertInfo(analyzer,landing_point):
    mapa_info = getValue(analyzer["landing_points"],landing_point)
    return mapa_info
      
def getValue(map,key):
    entry = mp.get(map,key)
    return me.getValue(entry)

def CountrySize(analyzer):
    return mp.size(analyzer["countries"])

def countries(analyzer):
    return mp.keySet(analyzer["countries"])
    
def countryInfo(analyzer,country):
    "Recibe un país y devuelve la información del país en este caso la información está como un mapa"
    map_info = getValue(analyzer["countries"],country)
    return map_info
# Funciones utilizadas para comparar elementos dentro de una lista

# Funciones de ordenamiento
