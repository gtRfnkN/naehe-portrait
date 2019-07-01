#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Raspberry Pi Family Portrait
# Copyright (C) 2015 Wasili Adamow
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from modules.CountdownThread import CountDownThread
from modules.ButtonThread import ButtonThread

import modules.logger as logger

import RPi.GPIO as GPIO
import time, subprocess, os, requests
from evdev import uinput, ecodes as e

# Buttons the prefix name
# the key is the GPIO-Pin of the Raspberry Pi, the value is the tag name of the button
# eg: "20: 'sw' means the Button at GPIO BCM20 triggers an image for the tag 'sw'
# special buttons: SH = shuffle images; RF = refresh web site
BUTTONS = {20: 'sw', 16: 'bl', 12: 'gr', 26: 'rd', 19: 'ye', 06: 'SH', 05: 'RF'}

# upload URL
UPL_URL = 'http://PORTRAITWEBSITE/upload.php'

# possible resolutions for the webcam and the current one
# bigger images need longer to take and to upload
RESOLUTIONS = {'full': '1920x1080', 'semi': '1280x720', 'low': '640x480'}
RES_USE = 'semi'

# ID of the working dir
GROUPID = 'default'

# callback to trigger the browser shuffle (send 'S' key)
def shuffle(state):
	if state:
		with uinput.UInput() as ui:
			ui.write(e.EV_KEY, e.KEY_S, 1)
			ui.write(e.EV_KEY, e.KEY_S, 0)
			ui.syn()

# callback to trigger the browser refresh (send 'CTRL+R' key)
def refresh(state):
	if state:
		with uinput.UInput() as ui:
			ui.write(e.EV_KEY, e.KEY_LEFTCTRL, 1)
			ui.write(e.EV_KEY, e.KEY_R, 1)
			ui.write(e.EV_KEY, e.KEY_LEFTCTRL, 0)
			ui.write(e.EV_KEY, e.KEY_R, 0)
			ui.syn()

# start picture taking process (start the countdown thread)
def cheese(cid, val):
	global countdownThread
	if val and not countdownThread:
		countdownThread = CountDownThread([0,1,2,3,4], [], 1, shoot, reset, cid)
		countdownThread.daemon = True
		countdownThread.start()

# tkae a picture by calling the command line tool
def shoot(cid):
	global countdownThread
	filename = "%s/output/%s-%d.jpg" % (os.path.dirname(os.path.realpath(__file__)), cid, int(time.time()))
	logger.log("filename: %s"%filename)
	try:
		subprocess.call(["fswebcam", "-r", RESOLUTIONS[RES_USE], "--no-banner", filename])

		files = {'file': open(filename, 'rb')}
		r = requests.post(UPL_URL+'?id='+GROUPID, files=files)
	except Exception, e:
		logger.log(e)
		raise e

# reset the countdownThread
def reset():
	global countdownThread
	countdownThread = False



if __name__ == "__main__":
	logger.createlogClient("testing", os.path.dirname(os.path.realpath(__file__))+"/")

	# thread used to show the countdown and call back for the actual picture taking process
	global countdownThread
	countdownThread = False

	# button listener thread managing callbacks for different events (photo, shuffle, random)
	buttonThread = ButtonThread(cheese, BUTTONS, shuffle, 'SH', refresh, 'RF')
	buttonThread.daemon = True
	buttonThread.start()

	try:
		while True:
			pass
	except Exception, e:
		logger.log(e)
		raise e
	finally:
		print "stopping"
		countdownThread.stop()
		buttonThread.stop()
		GPIO.cleanup()