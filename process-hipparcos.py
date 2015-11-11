#
# We read the Hipparcos data on stdin, and output Night360 data on stdout.
#

import math
import re
import sys

def deg2rad(d):
	return d*2*3.14159265/180.0

def radec2vec(ra,dec):
	return [math.cos(dec)*math.cos(ra),math.sin(dec),math.cos(dec)*math.sin(ra)]

def process_entry(line):
	fields = re.split("\s+", line)
	#print fields

	# Convert RA,Dec to a normalized cartesian vector
	# 0,0 is 1,0,0, pi/2,0 is 0,0,1, and 0,pi/2 is 0,1,0
	ra = float(fields[4])
	dec = float(fields[5])
	#v = [math.cos(dec)*math.cos(ra),math.sin(dec),math.cos(dec)*math.sin(ra)]
	v = radec2vec(ra,dec)

	# Multiply that by the distance
	parallax = float(fields[6])
	if parallax > 0:
		dist = 1000 / parallax
	else:
		dist = 0
	v[0] *= dist
	v[1] *= dist
	v[2] *= dist

	# Now find the proper motion, convert that to 3-space motion
	pmra = deg2rad(float(fields[7])*0.000290888) # Convert mas to rad
	pmdec = deg2rad(float(fields[8])*0.000290888)
	SCALE = 500
	v2 = radec2vec(ra+pmra/SCALE, dec+pmdec/SCALE)
	v2[0] *= dist
	v2[1] *= dist
	v2[2] *= dist
	v2[0] -= v[0]
	v2[1] -= v[1]
	v2[2] -= v[2]
	vel = [v2[0]*SCALE, v2[1]*SCALE, v2[2]*SCALE]

	print v[0], v[1], v[2], vel[0], vel[1], vel[2]

for line in sys.stdin.xreadlines():
	line = line.strip(" \r\n")
	if len(line) == 0:
		continue
	process_entry(line)
