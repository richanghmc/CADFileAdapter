import openpyscad as ops

# Opentron modules dimensions
# Thermocycler module - 316 x 172 x 154mm (l x w x h)
# Temperature module - 194 x 90 x 128mm
# Magnetic module - 128mm x 86mm x 90mm
#
# Sample labware - 130mm x 130mm x 50mm
#

Thermocycler_mod = ops.Cube([31.6, 17.2, 15.4]).color("Red").translate([0,0,0])
Temperature_mod = ops.Cube([19.4, 9, 12.8]).color("Blue").translate([0,50,0])
Magnetic_mod = ops.Cube([12.8, 8.6, 9]).color("Green").translate([50,0,0])
Sample_labware = ops.Cube([13, 13, 5]).color("Yellow").translate([50,50,0])

Thermocycler_mod.write("dimension.scad")
Temperature_mod.write("dimension.scad")
Magnetic_mod.write("dimension.scad")
Sample_labware.write("dimension.scad")

(Temperature_mod + Thermocycler_mod + Magnetic_mod + Sample_labware).write("dimension.scad")
