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

        self.dimsText = """Specify the dimensions for the chosen crystal type.
Please see help text on the "Crystal Type" label for information about the
dimensions required for each crystal type.
Only numerical values are accepted for these fields. The units for the dimension
values are microns.
"""

        self.modelText = """Specify the filename for the file containing the geometry of the crystal.
Currently only .obj (geometry denition) files can be read. The model and the
.obj files can be generated using the free and open source 3D animation software
BLENDER. (NOTE: if you are exporting a Wavefront (.obj) file in BLENDER, then
select the option "Triangulate Faces" before you finalise the export. RADDOSE-3D
only works with triangular faces for the polygons).
"""

        self.pixPerMicText = """Specifies the resolution of the voxel grid used to represent the crystal in voxels/micron.
If this is not specified then the value will default to 0.5 voxels/micron.

Note: When running RADDOSE-3D with larger dimensions (e.g. SAXS samples generally
require millimetre dimensions in diameter) a high value for this input will result
in longer processing times, and possibly an error if the resolution is too high.
Reducing this value (i.e. reducing the resolution) may be necessary if the
simulation takes too long or crashes with a "Java heap space" error.
"""

        self.anglePText = """Sets the angle in the plane of the loop between the
crystal and the goniometer axis. The angle should be given in degrees. If a
value is not specified then it will default to 0. The exception to this is when
a user is running a SAXS experiment. If either of the "SAXS" options are selected
for the "Absorption Coefficient" input, then the angle P is defaulted to 90 degrees
so that the beam direction is perpendicular to the height dimension of the capillary
(cylinder).


For a diagram explaining this value please see the official RADDOSE-3D user guide:
http://www.raddo.se/user-guide.pdf

Only numerical values are accepted for this field.
"""

        self.angleLText = """Sets the loop angle in the plane of the crystal loop
and the goniometer (rotation) axis. The angle should be given in degrees. If a
value is not specified then it will default to 0.

For a diagram explaining this value please see the official RADDOSE-3D user guide:
http://www.raddo.se/user-guide.pdf

Only numerical values are accepted for this field.
"""

        self.absCoeffText = """Species how the program should calculate the absorption coefficients
There are currently 7 different options:

1) Average protein composition - RADDOSE-3D assumes an absorption coefficient of
0.237mm^-1 and an attenuation coefficient of 0.281mm^-1. These values are
representative of an average crystal at an incident X-ray beam energy of 12.4 keV
(1 Angstrom wavelength).

2) Using PDB code - This option tells RADDOSE-3D that it should calculate the
absorption coefficients from a PDB file.

3) User defined composition - This option tells RADDOSE-3D that the user will
manually specify the composition of the crystal and will use the Java
implementation of the absorption coefficient calculation to calculate the
absorption coefficients.

4) RADDOSE version 2 - This option tells RADDOSE-3D that the user will
manually specify the composition of the crystal and will use the FORTRAN
implementation of the absorption coefficient calculation from the previous
RADDOSE version 2 to calculate the absorption coefficients.

5) using sequence file - This option tells RADDOSE-3D that the user will provide
a sequence file (in fasta format: http://blast.ncbi.nlm.nih.gov/blastcgihelp.shtml)
to specify the crystal sample composition.

6) SAXS (user defined composition) - This option tells RADDOSE-3D that the user
will manually specify the composition of the SAXS sample and will use the Java
implementation of the absorption coefficient calculation to calculate the
absorption coefficients.

7) SAXS (sequence file) - This option tells RADDOSE-3D that the user will
provide a sequence file (in fasta format: http://blast.ncbi.nlm.nih.gov/blastcgihelp.shtml)
to specify the SAXS sample composition.
"""

        self.pdbText = """Specifies the four letter pdb code from which the crystal composition is obtained.
Currently the RADDOSE-3D only reads PDB files from online database and not local files.
"""

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
