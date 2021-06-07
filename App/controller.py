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
 """

import config as cf
from App import model
import csv


"""
El controlador se encarga de mediar entre la vista y el modelo.
"""

# Inicialización del Catálogo de libros
def init():
    """
    Llama la funcion de inicializacion  del modelo.
    """
    # analyzer es utilizado para interactuar con el modelo
    analyzer = model.newAnalyzer()
    return analyzer

# Funciones para la carga de datos
def loadLanding_Points(analyzer):
    file = cf.data_dir + 'landing_points.csv'
    input_file = csv.DictReader(open(file, encoding='utf-8',errors='ignore'))
    for landing_point in input_file:
        model.addLandingPointMap(analyzer,landing_point) 
    return analyzer

def loadCountries(analyzer):
    file = cf.data_dir + 'countries.csv'
    input_file = csv.DictReader(open(file, encoding='utf-8',errors='ignore'))
    for country in input_file:
        model.addCountry(analyzer,country) 
    return analyzer

def loadConnection(analyzer):
    """
    Carga los datos de los archivos CSV en el modelo.
    Se crea un arco entre cada par de estaciones que
    pertenecen al mismo servicio y van en el mismo sentido.

    addRoutConnection crea conexiones entre diferentes rutas
    servidas en una misma estación.
    """
    connectionfile = cf.data_dir + "connections.csv"
    input_file = csv.DictReader(open(connectionfile, encoding="utf-8"),
                                delimiter=",")
    for connection in input_file:
        model.addConnectionArc(analyzer, connection)
    return analyzer

def totalLanding_Points(analyzer):
    return model.totalLanding_Points(analyzer)

def vertices(analyzer):
    return model.vertices(analyzer)

def countries(analyzer):
    return model.countries(analyzer)

def countryInfo(analyzer,country):
    return model.countryInfo(analyzer,country)

def totalArcs(analyzer):
    return model.totalArcs(analyzer)

def getValue(map,key):
    return model.getValue(map,key)

def vertInfo(analyzer,landing_point):
    return model.vertInfo(analyzer,landing_point)

def CountrySize(analyzer):
    return model.CountrySize(analyzer)
# Funciones de ordenamiento

# Funciones de consulta sobre el catálogo
def requerimiento1(graph,lndP1,lndP2,pMap):
    return model.identificar_cluster(graph,lndP1,lndP2,pMap)

def requerimiento3(graph,paisA,paisB,lpMap,cMap):
    return model.ruta_menor_distancia(graph,paisA,paisB,lpMap,cMap)