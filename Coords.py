#!/usr/bin/python

class Coords:
    def __init__(self,coord):
        self.coord = coord
        self.hour = coord.split("-")[0]
        self.mins = coord.split("-")[1]
        self.secs = coord.split("-")[2]

    # Devuelve la coordenada en segundos
    def coordToSecs(self):
        secs = int(self.hour) * 60
        secs += int(self.mins) * 60
        secs += int(self.secs)
        return secs

    # Devuelve la coordenada en 
    def getCoord(self):
        return self.coord

    # Diferencia de coordenadas en segundos
    def diffCoordSecs(coord1,coord2):
        return float(coord1.coordToSecs()) - float(coord2.coordToSecs())


