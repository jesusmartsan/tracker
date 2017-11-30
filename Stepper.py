#!/usr/bin/python

import RPi.GPIO as GPIO
import time
import math
import threading
 
# Modos de funcionamiento
SINGLE = 1
DOUBLE = 2
INTERLEAVE = 3
MICROSTEP = 4

# Direccion de movimiento
FORWARD = 1
BACK = -1

class Stepper:
    MICROSTEPS = 16
    STEPS = 4
#    MICROSTEPSEQ = [[1,0,0,1],[1,1,1,1],[0,1,0,1],[1,1,1,1],[0,1,1,0],[1,1,1,1],[1,0,1,0],[1,1,1,1]]
#    MICROSTEPSEQ = [[1,0,1,0],[1,1,1,1],[0,1,1,0],[1,1,1,1],[0,1,0,1],[1,1,1,1],[1,0,0,1],[1,1,1,1]]
    STEPSEQ = [[1,0,1,0],[0,1,1,0],[0,1,0,1],[1,0,0,1]]

    def __init__(self,mode,direction,pwma_control,pwmb_control,a1_pin,a2_pin,b1_pin,b2_pin):
        self.currentStep = 0
        self.currentMStep = 0
        self.mode = mode
        self.pwma = pwma
        self.pwmb = pwmb
        self.dir = direction
        self.stepCount = 0
        self.a1_pin = a1_pin
        self.a2_pin = a2_pin
        self.b1_pin = b1_pin
        self.b2_pin = b2_pin
        self.pwma_control = pwma_control
        self.pwmb_control = pwmb_control

        # Indicamos que los pines son de salida
        GPIO.setup(self.a1_pin, GPIO.OUT)
        GPIO.setup(self.a2_pin, GPIO.OUT)
        GPIO.setup(self.b1_pin, GPIO.OUT)
        GPIO.setup(self.b2_pin, GPIO.OUT)
        GPIO.setup(self.pwma_control, GPIO.OUT)
        GPIO.setup(self.pwmb_control, GPIO.OUT)

        self.pwma = GPIO.PWM(self.pwma_control,1600)
        self.pwmb = GPIO.PWM(self.pwmb_control,1600)

        self.pwma.start(0)
        self.pwmb.start(0)


    def setMode(self,mode):
        self.mode = mode

    def setDirection(self,direction):
        self.dir = direccion

    def setStep(self,coils):
#        print coils
        GPIO.output(self.a1_pin, coils[0])
        GPIO.output(self.a2_pin, coils[1])
        GPIO.output(self.b1_pin, coils[2])
        GPIO.output(self.b2_pin, coils[3])

    def goStep(self):
        # Por defecto, el valor de corriente es el 100%
        pwma_val = pwmb_val = 100

        # Control de pasos completos
        if (self.mode == SINGLE):
            self.currentStep += self.dir
            self.stepCount += 1 

        # Control por micropasos
        elif ((self.mode == MICROSTEP) and (not (self.currentMStep % self.MICROSTEPS))):
            #print "Paso..."+str(self.currentStep)
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

        self.pwma.start(pwma_val)
        self.pwmb.start(pwmb_val)

        self.currentStep %= self.STEPS
        
        coils = self.STEPSEQ[self.currentStep]
        
        self.setStep(coils)

    def reset(self):
        GPIO.output(coil_A_1_pin, 0)
        GPIO.output(coil_A_2_pin, 0)
        GPIO.output(coil_B_1_pin, 0)
        GPIO.output(coil_B_2_pin, 0)

