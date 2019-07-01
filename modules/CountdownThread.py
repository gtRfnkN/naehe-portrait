#!/usr/bin/env python
import threading, time
import RPi.GPIO as GPIO
import shiftpi

class CountDownThread(threading.Thread):
    def __init__(self, pinsRed, pinsGreen, sleepduration, callback_shoot, callback_reset, cid):
        threading.Thread.__init__(self)
        self._stop = threading.Event()

        # GPIO pins
        self.pinsRed = pinsRed
        self.pinsGreen = pinsGreen

        shiftpi.shiftRegisters(1)
        shiftpi.startupMode(shiftpi.HIGH, True)

        self.step = 0
        self.flag = False
        self.sleepduration = sleepduration

        self.callback_shoot = callback_shoot
        self.callback_reset = callback_reset
        self.cid = cid

    # as long as running and func is set: send the serial output to the func
    def run(self):
        while not self.stopped():            
            self.write()

            if self.step > len(self.pinsRed)+len(self.pinsGreen)+1: # stop after the last step
                self.stop()
                self.callback_reset()
            elif self.step > len(self.pinsRed)+len(self.pinsGreen)-2 and not self.flag: # trigger the picture callback
                self.flag = True
                self.callback_shoot(self.cid)

            self.step += self.sleepduration
            time.sleep(self.sleepduration)

    def write(self):
        for k, p in enumerate(self.pinsRed): # first the red lights
            val = shiftpi.LOW if k <= self.step else shiftpi.HIGH
            shiftpi.digitalWrite(p, val)

        for k, p in enumerate(self.pinsGreen): # then the green ones
            val = shiftpi.LOW if k+len(self.pinsRed) <= self.step else shiftpi.HIGH
            shiftpi.digitalWrite(p, val)

    # stop the thread
    def stop(self):
        shiftpi.startupMode(shiftpi.LOW, True)
        self._stop.set()

    # is the thread stopped?
    def stopped(self):
        return self._stop.is_set()