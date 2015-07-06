class CrystalInputHelp():
    def __init__(self):
        self.typeText = """Specify the type of the crystal.
This determines the shape of the crystal and ultimately determines the dimensions
that are required for input. Currently there are 4 types that can be selected:

1) Cuboid - defines a cuboid shaped crystal. Hence the dimensions required
for specification are the length, width and height (x, y, z). the z dimension is
parallel to the beam direction. The y direction is parallel to the rotation axis.
the x direction is perpendicular to both y and z.

2) Spherical - defines a spherical crystal. The dimension required for input is
the diameter.

3) Cylindrical - defines a cylindrical shaped crystal. The dimensions required
for input are the diameter of the circular cross-section and the height of the
cylinder.

4) Polyhedron - defines an arbitrary shaped crystal as a polyhedron. Instead of
explicitly giving dimensions for the arbitrary shaped crystal, a file containing
the vertices and faces of the crystal object should be given.
"""

        self.dimsText = "Need to sort out the text: dimensions"
        self.modelText = "Need to sort out the text: model"
        self.pixPerMicText = "Need to sort out the text: Pix per mic"
        self.anglePText = "Need to sort out the text: angleP"
        self.angleLText = "Need to sort out the text: angleL"
        self.absCoeffText = "Need to sort out the text: abs coeff"
        self.pdbText = "Need to sort out the text: pdb"
        self.unitcellText = "Need to sort out the text: unitcell - crystal"
        self.unitcellSAXSText = "Need to sort out the text: unitcell - saxs"
        self.numMonText = "Need to sort out the text: num mon"
        self.numResText = "Need to sort out the text: num res"
        self.numRNAText = "Need to sort out the text: num rna"
        self.numDNAText = "Need to sort out the text: num dna"
        self.protHeavyText = "Need to sort out the text: prot heavy"
        self.solHeavyText = "Need to sort out the text: sol heavy"
        self.solFracText = "Need to sort out the text: sol frac"
        self.protConcText = "Need to sort out the text: prot conc"
        self.conTypeText = "Need to sort out the text: con type"
        self.conMixText = "Need to sort out the text: con mixture"
        self.conElText = "Need to sort out the text: con Elemental"
        self.conThick = "Need to sort out the text: con thickness"
        self.conDens = "Need to sort out the text: con dens"
        self.seqFileText= "Need to out the text: seq File"


class BeamInputHelp():
    def __init__(self):
        self.typeText = "Need to sort out the text: type"
        self.fluxText = "Need to sort out the text: flux"
        self.energyText = "Need to sort out the text: energy"
        self.collText = "Need to sort out the text: collimation"
        self.fwhmText = "Need to sort out the text: fwhm"
        self.fileText = "Need to sort out the text: file"
        self.pixSizeText = "Need to sort out the text: pix size"

class WedgeInputHelp():
    def __init__(self):
        self.angStartText = "Need to sort out the text: start ang"
        self.angStopText = "Need to sort out the text: stop ang"
        self.exposText = "Need to sort out the text: exposure time"
        self.angRes = "Need to sort out the text: angular resolution"
        self.startOffText = "Need to sort out the text: start offset"
        self.transText = "Need to sort out the text: trans per deg"
        self.rotText = "Need to sort out the text: rotation & beam axis offset"
