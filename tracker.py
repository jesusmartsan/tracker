#!/usr/bin/python

import RPi.GPIO as GPIO
import time
 
GPIO.setmode(GPIO.BCM)
  
# Fijamos los pines a utilizar para cada una de las bobinas
coil_A_1_pin = 22
coil_A_2_pin = 23
coil_B_1_pin = 6
coil_B_2_pin = 12
   
# Indicamos que los pines son de salida
GPIO.setup(coil_A_1_pin, GPIO.OUT)
GPIO.setup(coil_A_2_pin, GPIO.OUT)
GPIO.setup(coil_B_1_pin, GPIO.OUT)
GPIO.setup(coil_B_2_pin, GPIO.OUT)

# Direccion de movimiento
FORWARD = 1
BACKWARD = -1

# Modos de funcionamiento
SINGLE = 1
DOUBLE = 2
INTERLEAVE = 3
MICROSTEP = 4

class Stepper:
    MICROSTEPS = 8
#    MICROSTEPSEQ = [[1,0,0,0],[1,0,0,1],[1,1,0,0],[0,1,0,0],[0,1,1,0],[0,0,1,0],[0,0,1,1],[0,0,0,1]]
    MICROSTEPSEQ = [[1,0,0,1],[1,1,1,1],[0,1,0,1],[1,1,1,1],[0,1,1,0],[1,1,1,1],[1,0,1,0],[1,1,1,1]]
    MICROSTEPSEQ = [[1,0,1,0],[1,1,1,1],[0,1,1,0],[1,1,1,1],[0,1,0,1],[1,1,1,1],[1,0,0,1],[1,1,1,1]]

    def __init__(self,mode,direction):
        self.currentStep = 0
        self.currentMStep = 0
        self.mode = mode
        self.dir = direction
        stepCount = 0

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
        if (self.mode == SINGLE):
            if (self.currentStep % 2):
                # Caso raro, estamos en un paso impar, se multiplica por la direccion, que vale 1 o -1
                self.currentStep += self.dir*self.MICROSTEPS//2
            else:
#                self.currentStep += self.dir*self.MICROSTEPS
                self.currentStep += self.dir*2
                self.stepCount += 1 
        elif (self.mode == DOUBLE):
            if not (self.currentStep % 2):
                # Caso raro, estamos en un paso par, se multiplica por la direccion, que vale 1 o -1
                self.currentStep += self.dir*self.MICROSTEPS//2
            else: 
                self.currentStep += self.dir*self.MICROSTEPS
        elif (self.mode == INTERLEAVE):
            self.currentStep += self.dir*self.MICROSTEPS//2
        elif ((self.mode == MICROSTEP) and (not (self.currentMStep % self.MICROSTEPS))):
            print self.currentMStep
            self.currentStep += self.dir*2
            self.currentMStep += 1
            self.currentMStep %= self.MICROSTEPS
        elif (self.mode == MICROSTEP and (self.currentMStep % self.MICROSTEPS)):
            coils = [1,1,1,1]
            self.currentMStep += 1
            self.currentMStep %= self.MICROSTEPS

#        else:
            # TODO: Devolver algo y parar la ejecucion
#            print ("Modo no reconocido")
#            return
        
#        self.currentStep += self.MICROSTEPS * 4
#        self.currentStep %= self.MICROSTEPS * 4

        #print "Antes: "+str(self.currentStep)
        self.currentStep %= self.MICROSTEPS
        #print "Despues: "+str(self.currentStep)

        # Si estamos usando micropasos, repetimos lo mismo
        #coils = self.MICROSTEPSEQ[self.currentStep//(self.MICROSTEPS//2)]
        coils = self.MICROSTEPSEQ[self.currentStep]
        
        print coils

        self.setStep(coils)

motor = Stepper(MICROSTEP, FORWARD)
motor = Stepper(MICROSTEP, BACKWARD)
steps = 2000

GPIO.output(coil_A_1_pin, 0)
GPIO.output(coil_A_2_pin, 0)
GPIO.output(coil_B_1_pin, 0)
GPIO.output(coil_B_2_pin, 0)

for i in range(0,steps):
    motor.goStep()
    time.sleep(0.001)

GPIO.output(coil_A_1_pin, 0)
GPIO.output(coil_A_2_pin, 0)
GPIO.output(coil_B_1_pin, 0)
GPIO.output(coil_B_2_pin, 0)

