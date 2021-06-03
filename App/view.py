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

def optionTwo(analyzer):
    print("\nCargando información  ....")
    controller.loadConnection(analyzer)
    controller.loadLanding_Points(analyzer)
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
    
while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n')
    if int(inputs[0]) == 1:
        print('\n')
        print("Inicializando ....")
        print('\n')
        analyzer = controller.init()
    elif int(inputs[0]) == 2:
        optionTwo(analyzer)
    else:
        sys.exit(0)
sys.exit(0)
