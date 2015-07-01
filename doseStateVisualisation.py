from scitools.std import *
from mayavi import mlab

def parseCrystalSizeLine(line):
    colonIndex = line.find(':')
    splitLine = line[colonIndex+1:-1].split()
    crystDims = (int(splitLine[0]), int(splitLine[2]), int(splitLine[4]))
    return crystDims

def getDoseStateFromR(filename):
    with open(filename, "r") as rCode:
        for line in rCode:
            if "Crystal size" in line:
                crystalDims = parseCrystalSizeLine(line)
                crystalDose = zeros(crystalDims)
            elif "dose[,," in line:
                for zDim in xrange(1, crystalDims[2] + 1):
                    string = "dose[,,{}]".format(zDim)
                    if string in line:
                        openBracketIndex = line.find("(")
                        closeBracketIndex = line.find(")")
                        zDimTuple = eval(line[openBracketIndex:closeBracketIndex+1])
                        zDimArray = array(zDimTuple)
                        crystalDose[:,:,zDim-1] = zDimArray.reshape(crystalDims[1],crystalDims[0]).transpose()
    return crystalDose

dose = getDoseStateFromR("output-DoseState.R")
mlab.contour3d(dose, colormap='hot', contours=[0.1, 20, 30], transparent=False, opacity=0.5, vmin=0, vmax=30)
mlab.outline()
mlab.colorbar(orientation='vertical')
