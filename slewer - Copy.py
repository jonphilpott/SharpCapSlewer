clr.AddReference("ASCOM.DriverAccess")
from ASCOM.DriverAccess import *
import time
import math

# Replace this with the name of your mount. For celestron mounts 
# this should be ASCOM.Celestron.Telescope. Make sure you connected
# to the mount in another app, e.g Cartes du Ciel. 
t = Telescope("ScopeSim.Telescope")

# How far to slew for each frame in R.A
RA_SLEW_HOURS = 1.0/15
# How far to slew for each frame in Declination
DEC_SLEW_DEG = 1

# How many frames along R.A
RA_FRAME_SIZE = 3
# How many frames along Declinatino
DEC_FRAME_SIZE = 3

# How long, in seconds, to wait after the slew before capturing the image.
CAMERA_WAIT = 0
 
def runSlew():
	RA_NOW = t.RightAscension
	DEC_NOW = t.Declination
	RA_1_DEG = (1.0/15) 
	
	print ("Mount currently at: RA: %f DEC: %F" %(RA_NOW, DEC_NOW));
	
	RA_HALF = 0.25 * (RA_FRAME_SIZE * RA_SLEW_HOURS)
	DEC_HALF = 0.25 * (DEC_FRAME_SIZE * DEC_SLEW_DEG)
	
	print ("RA_HALF: %f DEC_HALF: %f " % (RA_HALF, DEC_HALF))
	
	RA_START = RA_NOW - RA_HALF
	DEC_START = DEC_NOW - DEC_HALF
 	
 	print ("RA_START: %f DEC_START: %f " % (RA_START, DEC_START))
	
	for ra in range(0, RA_FRAME_SIZE):
		RA = RA_START + (ra * RA_SLEW_HOURS)
		for dec in range(0, DEC_FRAME_SIZE):
			DEC = DEC_START + (dec * DEC_SLEW_DEG)
			print ("Slewing to: %f, %f" % (RA, DEC));
 			t.SlewToCoordinates(RA, DEC);
 			print "Waiting....";
			time.sleep(SLEW_WAIT + CAMERA_WAIT)
			print "CAPTURING IMAGE.";
			try:
				SharpCap.SelectedCamera.CaptureSingleFrameTo("%s\\%03d_%03d.png" % (SharpCap.CaptureFolder, ra, dec))
			except:
				pass
	t.SlewToCoordinates(RA_NOW, DEC_NOW)
	
SharpCap.AddCustomButton("Run Slew", None, "Run %d x %d Slew" % (RA_FRAME_SIZE, DEC_FRAME_SIZE), runSlew)



