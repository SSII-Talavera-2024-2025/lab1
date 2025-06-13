#!/usr/bin/python3
# arista.py - Define una arista del grafo con sus atributos

class Arista:
    def __init__(self):
        self.id = ""  # ID de la arista
        self.origen = ""  # Nodo de inicio
        self.destino = ""  # Nodo de destino
        self.distancia = ""  # Longitud de la arista
        self.osmid = ""  # ID de OpenStreetMap
        self.carretera = ""  # Tipo de carretera
        self.interseccion = ""  # Tipo de intersección
        self.sentido_unico = ""  # Si es de un solo sentido
        self.invertida = ""  # Si está invertida
        self.geometria = ""  # Geometría de la arista
        self.velocidad_kph = ""  # Velocidad en km/h
        self.referencia = ""  # Referencia
        self.nombre = ""  # Nombre de la calle
        self.puente = ""  # Si es un puente
        self.carriles = ""  # Número de carriles
        self.velocidad_max = ""  # Velocidad máxima
        self.tunel = ""  # Si es un túnel