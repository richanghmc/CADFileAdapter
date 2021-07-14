import openpyscad as ops
import math
import stl
from stl import mesh
import numpy
from solid import *
from solid.utils import *

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

# find the max dimensions, so we can know the bounding box, getting the height,
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


def generateAdapter(xsize=128, ysize=86, zsize=15):
    """
    Take in the dimensions of the stl file generated from the 
    find_mins_max function and create an apporpriate sized adapter.
    """
    base = cube([126,84,12])
    if xsize*ysize <= 11008:
        inner = cube([xsize,ysize,zsize])
        width_padding = (128-xsize)/2
        height_padding = (86-ysize)/2
        noLipAdapter = difference()(
            base,
            up(4)(right(width_padding)(forward(height_padding)(inner)))
        )
        adapter = union()(
            noLipAdapter,
            color("red")(up(-1)(right(-1)(forward(-1)((cube([128,86,1]))))))
        )
    else:
        upper_component = cube([xsize+10,ysize+10,15])
        labware = cube([xsize,ysize,zsize])
        width_padding = (xsize-118)/2
        height_padding = (ysize-76)/2
        trapezoid = union()(
            color("green")(
            polyhedron(points=([[0,0,0],[xsize+10,0,0],[xsize+10,ysize+10,0],[0,ysize+10,0],
            [(xsize-116)/2,(ysize-74)/2,12],[126+(xsize-116)/2,(ysize-74)/2,12],[126+(xsize-116)/2,84+(ysize-74)/2,12],[(xsize-116)/2,84+(ysize-74)/2,12]]),
            faces=([[0,1,2,3],[4,5,1,0],[5,6,2,1],[6,7,3,2],[7,4,0,3],[7,6,5,4]]))
            )
        )
        container = difference()(
            color("red")(
                upper_component   
            ),
            up(5)(right(5)(forward(5)(labware)))
        )
        hollow_base = difference()(
            base,
            up(2)(forward(2)(right(2)(cube([122,80,8]))))
        )
        adapter = union()(
            color("blue")(up(-2.5)(right(width_padding)(forward(height_padding)((cube([128,86,2.5])))))),
            right(width_padding+1)(forward(height_padding+1)(hollow_base)),
            up(21)(container),
            rotate([180,0,0])(up(-21)(forward(-ysize-10)((trapezoid))))
        )
    scad_render_to_file(adapter, 'CADAdapter.scad')