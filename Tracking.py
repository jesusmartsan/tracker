#!/usr/bin/python

import threading

class Tracking(threading.Thread):
    def _bootstrap(self):
        super()._bootstrap()

    def stop(self):
        self.stop = True

    def track(self,motor):
        sleepTime = 1 // 16
        motor.setMode(MICROSTEP)

        while not self.stop:
        # Velocidad de seguimiento (16 micropasos/seg) = 1 paso por segundo
            motor.goStep()
            time.sleep(sleepTime)
        motor.reset()


