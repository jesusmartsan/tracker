#import RPi.GPIO as GPIO
import time
 
#GPIO.setmode(GPIO.BCM)
  
# Fijamos los pines a utilizar para cada una de las bobinas
coil_A_1_pin = 22
coil_A_2_pin = 23
coil_B_1_pin = 6
coil_B_2_pin = 12
   
# Indicamos que los pines son de salida
#GPIO.setup(enable_pin, GPIO.OUT)
#GPIO.setup(coil_A_1_pin, GPIO.OUT)
#GPIO.setup(coil_A_2_pin, GPIO.OUT)
#GPIO.setup(coil_B_1_pin, GPIO.OUT)
#GPIO.setup(coil_B_2_pin, GPIO.OUT)

# Direccion de movimiento
FORWARD = 1
BACKWARD = -1

# Modos de funcionamiento
SINGLE = 1
DOUBLE = 2
INTERLEAVE = 3
MICROSTEP = 4

test = 0
coils = []

class Stepper:
    MICROSTEPS = 8
    MICROSTEPSEQ = [[1,0,0,0],[1,1,0,0],[0,1,0,0],[0,1,1,0],[0,0,1,0],[0,0,1,1],[0,0,0,1],[1,0,0,1]]

    def __init__(self, mode, direction):
        print "init"
        self.currentStep = 0
        self.mode = mode
        self.dir = direction

    def setMode(mode):
        self.mode = mode

    def setDirection(self, direction):
        self.dir = direccion

    def setStep(self, coils):
        print coils
#        GPIO.output(coil_A_1_pin, coils[0])
#        GPIO.output(coil_A_2_pin, coils[1])
#        GPIO.output(coil_B_1_pin, coils[2])
#        GPIO.output(coil_B_2_pin, coils[3])

    def goStep(self):
        if (self.mode == SINGLE):
            if ((self.currentStep//(self.MICROSTEPS//2)) % 2):
                # Caso raro, estamos en un paso impar, se multiplica por la direccion, que vale 1 o -1
                self.currentStep += self.dir*self.MICROSTEPS//2
            else:
                self.currentStep += self.dir*self.MICROSTEPS
        elif (self.mode == DOUBLE):
            if not ((self.currentStep//(self.MICROSTEPS//2)) % 2):
                # Caso raro, estamos en un paso par, se multiplica por la direccion, que vale 1 o -1
                self.currentStep += self.dir*self.MICROSTEPS//2
            else: 
                self.currentStep += self.dir*self.MICROSTEPS
        elif (self.mode == INTERLEAVE):
            self.currentStep += self.dir*self.MICROSTEPS//2
        elif (self.mode == MICROSTEP):
            self.currentStep += self.dir

        else:
            # TODO: Devolver algo y parar la ejecucion
            print ("Modo no reconocido")
        
        self.currentStep += self.MICROSTEPS * 4
        self.currentStep %= self.MICROSTEPS * 4

        # Si estamos usando micropasos, repetimos lo mismo
        if (self.mode == MICROSTEP):
            if (self.currentStep >= 0) and (self.currentStep < self.MICROSTEPS):
                coils = [1, 1, 0, 0]
            elif (self.currentStep >= self.MICROSTEPS) and (self.currentStep < self.MICROSTEPS*2):
                coils = [0, 1, 1, 0]
            elif (self.currentStep >= self.MICROSTEPS*2) and (self.currentStep < self.MICROSTEPS*3):
                coils = [0, 0, 1, 1]
            elif (self.currentStep >= self.MICROSTEPS*3) and (self.currentStep < self.MICROSTEPS*4):
                coils = [1, 0, 0, 1]
        else:
            coils = self.MICROSTEPSEQ[self.currentStep//(self.MICROSTEPS//2)]

        self.setStep(coils)
        print self.currentStep

motor = Stepper(SINGLE, FORWARD)
steps = 200

for i in range(0,steps):
    motor.goStep()


