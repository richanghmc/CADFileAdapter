# CADFileAdapter

Given the CAD file of a labware object, this repository will automatically generate a CAD file for an adapter that would allow that object to snap into a rectangle on the the deck of opentron robot. The adapter generated will be attached to the labware object, which alters the size enough to snap into the rectangle on the robot.


# To Do
1. Learn what CAD is and how to use it
2. Figure out dimensions of Opentron
3. Figure out dimensions of labware object on CAD file
4. Implement an algorithm that takes in the general shape of the labware object CAD file, then produces an object that can both clamp onto the opentron and attach to the object.