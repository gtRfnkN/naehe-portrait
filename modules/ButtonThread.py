import threading, time
import RPi.GPIO as GPIO

class ButtonThread(threading.Thread):

    def __init__ (self, callback, pins, callbackShuffle, shuffleId, callbackRefresh, refreshId):
        threading.Thread.__init__(self)
        self._stop = threading.Event()

        GPIO.setmode(GPIO.BCM)

        # buttons
        self.pins = pins
        self.shuffleId = shuffleId
        self.refreshId = refreshId

        # function to deal with events
        self.callback = callback
        self.callbackShuffle = callbackShuffle
        self.callbackRefresh = callbackRefresh

        # init Buttons and last values
        self.lastState = dict()
        for pin, name in self.pins.iteritems():
            GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
            self.lastState[pin] = False

        # sleep duration between loops
        self.sleepduration = 0.05

    # as long as running and func is set: send the serial output to the func
    def run(self):
      while not self.stopped():
        # check button state (only when the button is available)
        for pin, name in self.pins.iteritems():
            state = GPIO.input(pin)
            if state != self.lastState[pin]:
                if name == self.shuffleId: # shuffle button
                    if self.callbackShuffle:
                        self.callbackShuffle(state)
                elif name == self.refreshId: # refresh button
                    if self.callbackRefresh:
                        self.callbackRefresh(state)
                else:
                    if self.callback: # picture buttons
                        self.callback(name, state)
                self.lastState[pin] = state
              
        time.sleep(self.sleepduration)

    # save the given func for feedback
    def bind(self, callback):
        self.callback = callback
        self.callback(self.lastState)

    # clear the func
    def unbind(self):
        self.callback = None

    # stop the thread
    def stop(self):
        self._stop.set()

    # is the thread stopped?
    def stopped(self):
        return self._stop.is_set()