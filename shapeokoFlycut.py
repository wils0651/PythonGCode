#!/usr/bin/env python

toolDia = 22

# extents of the machine
endX = -200 # -2084
endY = -50 # -282

startX = -1
startY = -1
startZ = 5 # 5 mm above material surface

# zeroZ = -20
plungeInterval = -1
cutMove = 10 # mm, how much each cut takes off

feedRate = 700 # mm/min
feedRatePlunge = 100 # mm/min

# Global locations
currentZ = 0

script = ""

def header():
    global script
    script = script + "G21 " # set machine to mm
    script = script + "G90;\n" # set machine to absolute location
    returnToStart()
    # script = script + "G10 L20 P1 X-1 Y-1;\n" # set the G54 coordinate system at current location
    script = script + "G10 L2 P1 X0 Y0;\n" # set the G54 coordinate system to machine zero
    script = script + "G54;\n" # put machine in G54 coordinate system

def g0Move(x, y, z):
    global script
    script = script + "G0"
    script = script + "X" + str(x)
    script = script + "Y" + str(y)
    script = script + "Z" + str(z) + ";\n"

def g1Move(x, y, z, f):
    global script
    script = script + "G1"
    script = script + "X" + str(x)
    script = script + "Y" + str(y)
    script = script + "Z" + str(z)
    script = script + "F" + str(f) + ";\n"

def makeOutline():
    g0Move(startX, endY, 1) # g0 to position to start feed in
    g1Move(startX, startY, currentZ, feedRate)
    g1Move(endX, startY, currentZ, feedRate)
    g1Move(endX, endY, currentZ, feedRate)
    g1Move(startX, endY, currentZ, feedRate)
    g1Move(startX, startY, currentZ, feedRate)

def makeSingleRow(y, yCutMove):
    cutY = y - yCutMove
    # plunge down
    g1Move(startX, y, currentZ, feedRatePlunge)
    # g1 over to new row
    g1Move(startX, cutY, currentZ, feedRate)
    # cut row
    g1Move(endX, cutY, currentZ, feedRate)
    # g0 up
    g0Move(endX, cutY, startZ)
    # g0 to start position
    g0Move(startX, cutY, startZ)
    return cutY


def makeRows():
    # iterate through all the rows in the y direction
    currentY = startY
    while currentY - cutMove > endY:
        currentY = makeSingleRow(currentY, cutMove)

def returnToStart():
    global script
    script = script + "G0Z" + str(startZ) + ";\n"
    g0Move(startX, startY, startZ)

def printIt():
    global script
    print(script)

def writeToFile():
    global script
    f = open("flycut.nc", "w")
    f.write(script)
    f.close()    

def main():
    global currentZ
    currentZ = plungeInterval
    header()
    makeOutline()
    makeRows()
    returnToStart()
    printIt()
    writeToFile()

main()