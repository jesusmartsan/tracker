#!/usr/bin/python

import threading
import time

class Tracking(threading.Thread):
    def _bootstrap(self):
        super()._bootstrap()

    def __init__(self,motor):
        threading.Thread.__init__(self)
        self.motor = motor
        self.stopflag = False

        self.trackingThread = threading.Thread(target=self.track, args=(self.motor,))
        self.trackingThread.start()

    def stop(self):
        self.stopflag = True
        self.motor.reset()

    def track(self, motor):
        sleepTime = 0.062   # 1/16 segundos

        while not self.stopflag:
        # Velocidad de seguimiento (16 micropasos/seg) = 1 paso por segundo
            self.motor.goStep()
            time.sleep(sleepTime)
