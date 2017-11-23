#!/usr/bin/python

# TODO: Control de errores

import RPi.GPIO as GPIO
import time
import math
import threading
 
GPIO.setmode(GPIO.BCM)
  
# Fijamos los pines a utilizar para cada una de las bobinas
coil_A_1_pin = 22
coil_A_2_pin = 23
coil_B_1_pin = 6
coil_B_2_pin = 12
pwma_control = 24
pwmb_control = 25
   
# Indicamos que los pines son de salida
GPIO.setup(coil_A_1_pin, GPIO.OUT)
GPIO.setup(coil_A_2_pin, GPIO.OUT)
GPIO.setup(coil_B_1_pin, GPIO.OUT)
GPIO.setup(coil_B_2_pin, GPIO.OUT)
GPIO.setup(pwma_control, GPIO.OUT)
GPIO.setup(pwmb_control, GPIO.OUT)

pwma = GPIO.PWM(pwma_control,1600)
pwmb = GPIO.PWM(pwmb_control,1600)

pwma.start(0)
pwmb.start(0)

# Direccion de movimiento
FORWARD = 1
BACK = -1

# Modos de funcionamiento
SINGLE = 1
DOUBLE = 2
INTERLEAVE = 3
MICROSTEP = 4

class Stepper:
    MICROSTEPS = 16
    STEPS = 4
#    MICROSTEPSEQ = [[1,0,0,1],[1,1,1,1],[0,1,0,1],[1,1,1,1],[0,1,1,0],[1,1,1,1],[1,0,1,0],[1,1,1,1]]
#    MICROSTEPSEQ = [[1,0,1,0],[1,1,1,1],[0,1,1,0],[1,1,1,1],[0,1,0,1],[1,1,1,1],[1,0,0,1],[1,1,1,1]]
    STEPSEQ = [[1,0,1,0],[0,1,1,0],[0,1,0,1],[1,0,0,1]]

    def __init__(self,mode,direction):
        self.currentStep = 0
        self.currentMStep = 0
        self.mode = mode
        self.dir = direction
        self.stepCount = 0

    def setMode(self,mode):
        self.mode = mode

    def setDirection(self,direction):
        self.dir = direccion

    def setStep(self,coils):
#        print coils
        GPIO.output(coil_A_1_pin, coils[0])
        GPIO.output(coil_A_2_pin, coils[1])
        GPIO.output(coil_B_1_pin, coils[2])
        GPIO.output(coil_B_2_pin, coils[3])

    def goStep(self):
        # Por defecto, el valor de corriente es el 100%
        pwma_val = pwmb_val = 100

        # Control de pasos completos
        if (self.mode == SINGLE):
            self.currentStep += self.dir
            self.stepCount += 1 

        # Revisar la posibilidad de dobles pasos, aunque parece que no es necesario
#        elif (self.mode == DOUBLE):
#            if not (self.currentStep % 2):
#                # Caso raro, estamos en un paso par, se multiplica por la direccion, que vale 1 o -1
#                self.currentStep += self.dir*self.MICROSTEPS//2
#            else: 
#                self.currentStep += self.dir*self.MICROSTEPS
        # Revisar la posibilidad de medios pasos, aunque parece que no es necesario
#        elif (self.mode == INTERLEAVE):
#            self.currentStep += self.dir*self.MICROSTEPS//2

        # Control por micropasos
        elif ((self.mode == MICROSTEP) and (not (self.currentMStep % self.MICROSTEPS))):
            print "Paso..."+str(self.currentStep)
            self.currentStep += self.dir
            self.currentMStep += 1
            self.currentMStep %= self.MICROSTEPS
        elif (self.mode == MICROSTEP and (self.currentMStep % self.MICROSTEPS)):
            self.currentMStep += 1
            self.currentMStep %= self.MICROSTEPS

            pwma_val = math.sin(360.0*self.currentStep/64.0)
            pwmb_val = math.cos(360.0*self.currentStep/64.0)

            if (pwma_val < 0):
                pwma_val *= -1
            if (pwmb_val < 0):
                pwmb_val *= -1
        print pwma_val

        pwma.start(pwma_val)
        pwmb.start(pwmb_val)

        self.currentStep %= self.STEPS
        
        coils = self.STEPSEQ[self.currentStep]
        print coils
        
        self.setStep(coils)

    def reset(self):
        GPIO.output(coil_A_1_pin, 0)
        GPIO.output(coil_A_2_pin, 0)
        GPIO.output(coil_B_1_pin, 0)
        GPIO.output(coil_B_2_pin, 0)

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


class Astro:
    def __init__(self,name,ra,dec):
        self.name = name
        self.ra = Coords(ra)
        self.dec = Coords(dec)

    def getRA(self):
        return self.ra

    def getDEC(self):
        return self.dec

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

def track(motor):
    sleepTime = 1 // 16
    motor.setMode(MICROSTEP)

    while True:
    # Velocidad de seguimiento (16 micropasos/seg) = 1 paso por segundo
        motor.goStep()
        time.sleep(sleepTime)
    motor.reset()

# Mueve hacia el astro seleccionado y hace seguimiento
def move(currentAstro, newAstro, motorAR, motorDEC):
    secsRA = Coords.diffCoordSecs(currentAstro.getRA(), newAstro.getRA())
    secsDEC = Coords.diffCoordSecs(currentAstro.getDEC(), newAstro.getDEC())

    nStepsRA = int(secsRA // 15)
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
    for i in range (0,nStepsRA):
        motorRA.goStep()
        time.sleep(0.001)

    motorAR.reset()
#    motorDEC.reset()

#    trackingThread = threading.Thread(target=track, args=(motorRA))
#    trackingThread.start()

    return 0
#    return trackingThread


# Detiene el seguimiento
def stopMotion(motionThreadId, motorRA):
    trackingThread.stop()
    motorRA.reset

# TEST
#motor = Stepper(MICROSTEP, FORWARD)
#steps = 3200

# Inicializamos los motores
#motor.reset()

motorRA = Stepper(MICROSTEP, FORWARD)
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
            motionThreadId = move(currentAstro, newAstro, motorRA, motorDEC=None)
        elif (opt == 5):
            stopMotion(motionThreadId, motorRA)
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





