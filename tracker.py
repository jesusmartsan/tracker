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
    dec="79-13-54"

    astro = Astro("test",ra,dec)
    return astro

# Mueve hacia el astro seleccionado y hace seguimiento
def move(currentAstro, newAstro, motorAR, motorDEC):
    secsRA = Coords.diffCoordSecs(currentAstro.getRA(), newAstro.getRA())
    secsDEC = Coords.diffCoordSecs(currentAstro.getDEC(), newAstro.getDEC())

    print currentAstro.getRA().coordToSecs()
    print newAstro.getRA().coordToSecs()
    print secsRA

    nStepsRA = int(secsRA*3*144)# // 15)
    nStepsDEC = 0#secsDEC // 15

    motorRA.reset()
    motorRA.setMode(SINGLE)

##    motorDEC.reset
#    motorDEC.setMode(SINGLE)

    # Buscamos la coordenada DEC
    for i in range (0,nStepsDEC):
#        motorDEC.goStep()
        time.sleep(0.001)
   
    # Buscamos la coordenada AR
    print nStepsRA
    for i in range (0,nStepsRA):
        motorRA.goStep()
        time.sleep(0.001)

    motorAR.reset()
#    motorDEC.reset()

    trackingThread = TrackThread(target=track, args=(motorRA,))
    trackingThread.start()

#    return 0
    trackingThread = None
    return trackingThread


# Detiene el seguimiento
def stopMotion(motionThread, motorRA):
    motionThread.stop()
    motionThread.join()
    motorRA.reset()

# TEST
#motor = Stepper(MICROSTEP, FORWARD)
#steps = 3200

# Inicializamos los motores
#motor.reset()

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
            motionThread = move(currentAstro, newAstro, motorRA, motorDEC=None)
        elif (opt == 5):
            stopMotion(motionThread, motorRA)
        elif (opt == 6):
            motorRA.reset()
            motorDEC.reset()
            pwma.stop()
            pwmb.stop()
            GPIO.cleanup()
            break
        else:
            print "Error"
except KeyboardInterrupt:
    stopMotion(motionThreadId, motorRA)
    motorRA.reset()
    motorDEC.reset()
    pwma.stop()
    pwmb.stop()
    GPIO.cleanup()





