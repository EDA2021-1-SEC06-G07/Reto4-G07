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


from sys import hexversion
from DISClib.Algorithms.Graphs.bellmanford import BellmanFord, distTo
from DISClib.DataStructures.chaininghashtable import get
import config as cf
from DISClib.ADT import list as lt
from DISClib.ADT.graph import gr
from DISClib.ADT import map as mp
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Sorting import mergesort as mes
from DISClib.Algorithms.Graphs import dijsktra as djt
from DISClib.Algorithms.Graphs import bellmanford as bmf
from DISClib.Algorithms.Graphs import scc 
from math import sin,cos,sqrt,asin,pi
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
                                              size= 1279,
                                              comparefunction= None)
    analyzer["landing_points"] = mp.newMap(numelements= 4000,
                                           maptype= 'PROBING',
                                           loadfactor= 0.4,
                                           comparefunction= None)
    return analyzer

def addConnectionArc(analyzer, connection):
    graph = analyzer['connections']
    origen = connection["\ufefforigin"]
    destino = connection["destination"]

    lat1,lon1 = encontrar_lat_lon_lp(analyzer['landing_points'],origen)
    lat2,lon2 = encontrar_lat_lon_lp(analyzer['landing_points'],destino)
    longitud = harvesine(lat1,lat2,lon1,lon2)
    
    graph1 = addLanding_point(graph,origen)
    graph2 = addLanding_point(graph1,destino)
    addConnection(graph2,origen,destino,longitud)
    
    

def addLanding_point(graph,landing_point):
    """
    Adiciona un Landing point como vertice del grafo
    """
    try:
        contains = gr.containsVertex(graph, landing_point)
        if  not contains :
            gr.insertVertex(graph, landing_point)
            
        return graph
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
def addConnection(graph, origin, destination, distance):
    """
    Adiciona un arco entre dos landing points
    """
    edge = gr.getEdge(graph, origin, destination)
    
    if edge is None:
        gr.addEdge(graph, origin, destination, distance)
    return graph

def addLandingPointMap(analyzer,landing_point):
    map = analyzer["landing_points"]
    key = landing_point["landing_point_id"]
    info_lndP = mp.newMap(numelements= 5)
    mp.put(info_lndP,'codeLP',landing_point["landing_point_id"])
    mp.put(info_lndP,'id',landing_point["id"])
    mp.put(info_lndP,'name',landing_point["name"])
    mp.put(info_lndP,'latitude',float(landing_point["latitude"]))
    mp.put(info_lndP,'longitude',float(landing_point["longitude"]))
    mp.put(map,key,info_lndP)

def addCountry(analyzer,country):
    countries = analyzer["countries"]
    name = country["CountryName"]
    name = name.lower()
    name = name.replace(' ','-')
    info = mp.newMap(numelements= 5)
    mp.put(info,'latitude',float(country['CapitalLatitude']))
    mp.put(info,'longitude',float(country['CapitalLongitude']))
    mp.put(info,'Population',country["Population"])
    mp.put(info,'Internet_Users',int(country["Internet users"]))
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

#Funciones de requerimiento
def identificar_cluster (graph,lndPoint1,lndPoint2,pMap):

    idLndP1 = obtener_codeLP(pMap,lndPoint1)
    idLndP2 = obtener_codeLP(pMap,lndPoint2)

    sccGraph = scc.KosarajuSCC(graph)
    sccCant = scc.connectedComponents(sccGraph)

    clusterLP1 = mp.get(sccGraph['idscc'],idLndP1)['value']
    clusterLP2 = mp.get(sccGraph['idscc'],idLndP2)['value']

    cfc = scc.stronglyConnected(sccGraph,idLndP1,idLndP2)

    clts = clusterLP1,clusterLP2
    rta = sccCant,cfc
    return clts,rta

def ruta_menor_distancia(graph,paisA,paisB,lpMap,cMap):
    paisA = paisA.lower()
    paisA = paisA.replace(' ','-')
    paisB = paisB.lower()
    paisB = paisB.replace(' ','-')

    lstcode1 = obtener_lP_pais(lpMap,paisA)
    lstcode2= obtener_lP_pais(lpMap,paisB)

    rta = None

    menorCosto = 99999
    menorRuta = None
    for code1 in lt.iterator(lstcode1):
        bellmanFord = bmf.BellmanFord(graph,code1)
        for code2 in lt.iterator(lstcode2):
            existRuta = bmf.hasPathTo(bellmanFord,code2)
            if existRuta:
                costoMin = bmf.distTo(bellmanFord,code2)
                if costoMin < menorCosto:
                    menorRuta = bmf.pathTo(bellmanFord,code2)

    if menorRuta != None:
        rta = menorCosto,menorRuta

    return rta
    


#Funciones auxiliares
def obtener_codeLP(pMap,key):
    key1 = key.lower()
    idname = key1.replace(' ','-')
    lst = mp.valueSet(pMap)
    idLp = None

    for vlue in lt.iterator(lst):
        value = getValue(vlue,'id')
        if  idname in value:
            idLp = getValue(vlue,'codeLP')
    return idLp

def obtener_lP_pais(lpMap,pais):
    lst = lt.newList(datastructure='ARRAY_LIST')
    lstLp = mp.valueSet(lpMap)

    for lp in lt.iterator(lstLp):
        value = getValue(lp,'id')
        if pais in value:
            code = getValue(lp,'codeLP')
            lt.addLast(lst,code)
    return lst

def menor_Lp(lst):
    menor = None
    code = None

    for elemt in lt.iterator(lst):
        distance = getValue(elemt,'distance')
        codeLp = getValue(elemt,'code')
        if menor == None:
            menor = distance
            code = codeLp
        elif distance < menor:
            menor = distance
            code = codeLp
    rta = code,menor
    return rta

def harvesine(lat1,lat2,lon1,lon2):
    r = 6371000
    c = pi/180
    d = 2*r*asin(sqrt(sin(c*(lat2-lat1)/2)**2 + cos(c*lat1)*cos(c*lat2)*sin(c*(lon2-lon1)/2)**2))
    return round((d/1000),2)

def encontrar_lat_lon_lp(lpMap,code):
    value = getValue(lpMap,code)
    lat = getValue(value,'latitude')
    lon = getValue(value,'longitude')
    return lat,lon







