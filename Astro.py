#!/usr/bin/python

from Coords import *

class Astro:
    def __init__(self,name,ra,dec):
        self.name = name
        self.ra = Coords(ra)
        self.dec = Coords(dec)

    def getRA(self):
        return self.ra

    def getDEC(self):
        return self.dec


