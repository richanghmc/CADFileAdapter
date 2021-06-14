import openpyscad as ops
import math
import stl
from stl import mesh
import numpy

import os
import sys

# Opentron modules dimensions
# Thermocycler module - 316 x 172 x 154mm (l x w x h)
# Temperature module - 194 x 90 x 128mm
# Magnetic module - 128mm x 86mm x 90mm
#
# Sample labware - 130mm x 130mm x 50mm
#

# Thermocycler_mod = ops.Cube([31.6, 17.2, 15.4]).color("Red").translate([0,0,0])
# Temperature_mod = ops.Cube([19.4, 9, 12.8]).color("Blue").translate([0,50,0])
# Magnetic_mod = ops.Cube([12.8, 8.6, 9]).color("Green").translate([50,0,0])
# Sample_labware = ops.Cube([13, 13, 5]).color("Yellow").translate([50,50,0])

# Thermocycler_mod.write("dimension.scad")
# Temperature_mod.write("dimension.scad")
# Magnetic_mod.write("dimension.scad")
# Sample_labware.write("dimension.scad")

# (Temperature_mod + Thermocycler_mod + Magnetic_mod + Sample_labware).write("dimension.scad")


if len(sys.argv) < 2:
    sys.exit('Usage: %s [stl file]' % sys.argv[0])

if not os.path.exists(sys.argv[1]):
    sys.exit('ERROR: file %s was not found!' % sys.argv[1])

# this stolen from numpy-stl documentation
# https://pypi.python.org/pypi/numpy-stl

# find the max dimensions, so we can know the bounding box, getting the height,
# width, length (because these are the step size)...
def find_mins_maxs(obj):
    minx = maxx = miny = maxy = minz = maxz = None
    for p in obj.points:
        # p contains (x, y, z)
        if minx is None:
            minx = p[stl.Dimension.X]
            maxx = p[stl.Dimension.X]
            miny = p[stl.Dimension.Y]
            maxy = p[stl.Dimension.Y]
            minz = p[stl.Dimension.Z]
            maxz = p[stl.Dimension.Z]
        else:
            maxx = max(p[stl.Dimension.X], maxx)
            minx = min(p[stl.Dimension.X], minx)
            maxy = max(p[stl.Dimension.Y], maxy)
            miny = min(p[stl.Dimension.Y], miny)
            maxz = max(p[stl.Dimension.Z], maxz)
            minz = min(p[stl.Dimension.Z], minz)
    return minx, maxx, miny, maxy, minz, maxz

main_body = mesh.Mesh.from_file(sys.argv[1])

minx, maxx, miny, maxy, minz, maxz = find_mins_maxs(main_body)
xsize = maxx-minx
ysize = maxy-miny
zsize = maxz-minz

def generateAdapter(xsize, ysize, zsize):
    """
    Take in the dimensions of the stl file generated from the 
    find_mins_max function and create an apporpriate sized adapter.
    """
    # take in the size of the stl file
    # create constants that represent the deck dimensions (128 mm x 86 mm)
    # try to generate a file that will create the adapter


print ("File: Deck plate Adapter.stl", sys.argv[1])

print ("X size:",xsize)
print ("Y size:", ysize)
print ("Z size:", zsize)
print ("X position:",minx)
print ("Y position:",miny)
print ("Z position:",minz)
print(minz,maxz)
print("NE Quadrant: translate([",-minx, ",",-miny,",",-minz,"])")
print("NW Quadrant: rotate([0,0,90]) translate([",-minx, ",",-miny,",",-minz,"])")
print("SW Quadrant: rotate([0,0,180]) translate([",-minx, ",",-miny,",",-minz,"])")
print("NE Quadrant: rotate([0,0,-90]) translate([",-minx, ",",-miny,",",-minz,"])")
print("Center: translate([",-(minx + (xsize/2)), ",",-(miny + (ysize/2)),",",-(minz + (zsize/2)),"])")