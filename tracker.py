#!/usr/bin/python

import RPi.GPIO as GPIO
import time
import math
 
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

        pwma.start(pwma_val)
        pwmb.start(pwmb_val)

        self.currentStep %= self.STEPS
        
        coils = self.STEPSEQ[self.currentStep]
        print coils
        
        self.setStep(coils)

motor = Stepper(MICROSTEP, FORWARD)
steps = 3200

GPIO.output(coil_A_1_pin, 0)
GPIO.output(coil_A_2_pin, 0)
GPIO.output(coil_B_1_pin, 0)
GPIO.output(coil_B_2_pin, 0)

try: 
    for i in range(0,steps):
        motor.goStep()
        time.sleep(0.001)
except KeyboardInterrupt:
    pass

motor = Stepper(MICROSTEP, BACK)
try: 
    for i in range(0,steps):
        motor.goStep()
        time.sleep(0.001)
except KeyboardInterrupt:
    pass


GPIO.output(coil_A_1_pin, 0)
GPIO.output(coil_A_2_pin, 0)
GPIO.output(coil_B_1_pin, 0)
GPIO.output(coil_B_2_pin, 0)

pwma.stop()
pwmb.stop()
GPIO.cleanup()


