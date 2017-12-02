#!/usr/bin/python

# TODO: Control de errores

import RPi.GPIO as GPIO
import time
import math
import threading
from Stepper import *
from Astro import *
from Coords import *
from Tracking import *

GPIO.setmode(GPIO.BCM)
  
# Fijamos los pines a utilizar para cada una de las bobinas
a1_pin = 22
a2_pin = 23
b1_pin = 6
b2_pin = 12
pwma_control = 24
pwmb_control = 25
   
# Se ejecuta cuando el telescopio apunta a la polar para calibrar la posicion
def polarAlign():
    return Astro("polar", "2-31-50", "89-15-51")
    # Buscar coordenadas de la estrella polar en stellarium

# Busca en stellarium
def findAstro():
#    url = "http://localhost:8090/api/objects/find?str="+astro"+&info"

    astrostr = input("Introduzca el nombre a buscar: ")
    # Parsear la salida para obtener AR y DEC
    ra = ""
    dec = ""
    astro = Astro(ra,dec)

    return astro


# Pregunta por coordenadas de forma manual
def manualCoords():
#    ra = input("Introduzca la coordenada Ascension Recta (H-M-S): ")
#    dec = input("Introduzca la coordenada Declinacion (H-M-S): ")
    ra="5-22-32"
    ra="1-0-0"
    dec="79-13-54"

    astro = Astro("test",ra,dec)
    return astro

# Mueve hacia el astro seleccionado y hace seguimiento
def move(currentAstro, newAstro, motorAR, motorDEC):
    secsRA = Coords.diffCoordSecs(newAstro.getRA(), currentAstro.getRA())
    secsDEC = Coords.diffCoordSecs(newAstro.getDEC(), currentAstro.getDEC())

    print currentAstro.getRA().coordToSecs()
    print newAstro.getRA().coordToSecs()
    print "secsRA = "+str(secsRA)

    nStepsDEC = 0#secsDEC // 15
    nStepsRA = int(secsRA)

#    if (nStepsDEC < 0):
#        nStepsDEC *= -1
#        motorDEC.setDirection(Stepper.BACK)
#    else:
#        motorDEC.setDirection(Stepper.FORWARD)

    if (nStepsRA < 0):
        nStepsRA *= -1
        motorRA.setDirection(Stepper.BACK)
    else:
        motorRA.setDirection(Stepper.FORWARD)

##    motorDEC.reset
#    motorDEC.setMode(SINGLE)

    motorRA.reset()
    motorRA.setMode(Stepper.SINGLE)

    # Buscamos la coordenada DEC
    for i in range (0,nStepsDEC):
#        motorDEC.goStep()
        time.sleep(0.001)
   
    # Buscamos la coordenada AR
    for i in range (0,nStepsRA//10):
        motorRA.goStep()
        time.sleep(0.001)

    motorRA.reset()
#    motorDEC.reset()

    motorRA.setDirection(Stepper.FORWARD)
    motorRA.setMode(Stepper.MICROSTEP)

    track = Tracking(motorRA)
    #trackingThread = track.run()

    print "paso"

#    return 0
    return track


# Detiene el seguimiento
def stopMotion(motionThread, motorRA):
    motionThread.stop()
    motorRA.reset()

motionThread = None

motorRA = Stepper(pwma_control, pwmb_control, a1_pin, a2_pin, b1_pin, b2_pin)
#motorDEC = Stepper(MICROSTEP, FORWARD)

try:
    while True:
        print "Selecciona una de las siguientes opciones"
        print "1.- Alineacion Polar: Seleccione esta opcion cuando el telescopio apunte a la estrella polar"
        print "2.- Buscar astro: Busca un astro en la BD"
        print "3.- Introducir coordenadas manualmente (formato H-M-S(AR)/H-M-S(DEC))"
        print "4.- Mover telescopio a las coordenadas seleccionadas o al astro seleccionado"
        print "5.- Parar el seguimiento del astro seleccionado"
        print "6.- Salir"
        opt = input ("Opcion: ")

        if (opt == 1):
            currentAstro = polarAlign()
        elif (opt == 2):
            newAstro = findAstro()
        elif (opt == 3):
            newAstro = manualCoords()
        elif (opt == 4):
            if (motionThread != None):
                stopMotion(motionThread, motorRA)
            motionThread = move(currentAstro, newAstro, motorRA, motorDEC=None)
            currentAstro = newAstro
        elif (opt == 5):
            stopMotion(motionThread, motorRA)
        elif (opt == 6):
            if (motionThread != None):
                stopMotion(motionThread, motorRA)
 #               motionThread.join()
            motorRA.reset()
        #    motorDEC.reset()
            GPIO.cleanup()
            break
        else:
            print "Error"
except KeyboardInterrupt:
    if (motionThread != None):
        stopMotion(motionThread, motorRA)
#        motionThread.join()
    motorRA.reset()
#    motorDEC.reset()
    GPIO.cleanup()





