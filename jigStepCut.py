#!/usr/bin/env python

toolDia = 25

xMin = -14.0
xMax = -2080.0 # -2084
yMin = -171.2
yMax = -184.5 # -282

xStart = xMin - 25.0
yStart = (yMin + yMax)/2.0
zSafety = 25.0
zStart = 5 # 5 mm above material surface

plungeInterval = -2
cutMove = 12.0 # mm, how much each cut takes off

feedRate = 700 # mm/min
feedRatePlunge = 100 # mm/min

# Global locations
xCurrentMin = 0.0
xCurrentMax = 0.0
yCurrentMin = 0.0
yCurrentMax = 0.0
zCurrent = 0.0

script = ""

def header():
    global script
    script = script + "G21 " # set machine to mm
    script = script + "G90;\n" # set machine to absolute location
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
    g1Move(xCurrentMin, yCurrentMin, zCurrent, feedRate)
    g1Move(xCurrentMax, yCurrentMin, zCurrent, feedRate)
    g1Move(xCurrentMax, yCurrentMax, zCurrent, feedRate)
    g1Move(xCurrentMin, yCurrentMax, zCurrent, feedRate)
    g1Move(xCurrentMin, yCurrentMin, zCurrent, feedRate)

def zCutLeadIn():
    global zCurrent
    # go to start position
    returnToStart()
    # plunge to material surface
    g1Move(xStart, yStart, zCurrent, feedRatePlunge)
    # Set new zCurrent
    zCurrent = zCurrent + plungeInterval
    # cut diagonally down
    g1Move(xMin, yStart, zCurrent, feedRate)
    # go to corner
    g1Move(xMin, yMin, zCurrent, feedRate)

def initializeCurrentLocations():
    global xCurrentMin
    global xCurrentMax
    global yCurrentMin
    global yCurrentMax
    xCurrentMin = xMin
    xCurrentMax = xMax
    yCurrentMin = yMin
    yCurrentMax = yMax

def iterateCurrentLocations():
    # zCurent changed in zCutLeadIn()
    global xCurrentMin
    global xCurrentMax
    global yCurrentMin
    global yCurrentMax
    xCurrentMin = xCurrentMin - cutMove
    xCurrentMax = xCurrentMax + cutMove
    yCurrentMin = yCurrentMin - cutMove
    yCurrentMax = yCurrentMax + cutMove 

def makePocket():
    initializeCurrentLocations()
    while yCurrentMin > yStart:
        makeOutline()
        iterateCurrentLocations()
    returnToStart()

def returnToStart():
    global script
    script = script + "G0Z" + str(zSafety) + ";\n"
    g0Move(xStart, yStart, zSafety)
    g0Move(xStart, yStart, zStart)

def printIt():
    global script
    print(script)

def writeToFile():
    global script
    f = open("jigStepCut.nc", "w")
    f.write(script)
    f.close()    

def main():
    initializeCurrentLocations()
    header()
    # first cut
    zCutLeadIn()
    makePocket()
    # second cut
    zCutLeadIn()
    makePocket()

    # third cut
    zCutLeadIn()
    makePocket()

    # fourth cut
    zCutLeadIn()
    makePocket()
    
    printIt()
    writeToFile()

main()