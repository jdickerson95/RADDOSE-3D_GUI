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

        self.unitcellText = """Specifies the unit cell dimensions of the crystal
inputs a, b and c specify the unit cell lengths in angstroms. Alpha, beta and gamma
specify the unit cell angles in degrees. If the unit cell angles are not given then
they will default to 90 degrees"""

        self.unitcellSAXSText = """Specifies a volume to calculate the sample composition.
The unit cell for the SAXS case is not taken literally as a unit cell in the
crystal sense. Instead it specifies a volume of sufficient size to contain at
least 1 complete protein molecule. If the unit cell values are not explicitly
given then each dimension will default to 1000 Angstroms and the cell angles will
default to 90 degrees. When RADDOSE-3D is run, the log file will give the number
of protein molecules in the given volume and will give a warning if it is less
than 1. If this is the case then the unit cell dimensions should be increased
manually.
 """

        self.numMonText = """ Specifies the number of protein monomers in the unit cell.
Only integers (whole numbers) should be given. This should not be confused with
the number of monomers in the asymmetric unit.
"""

        self.numResText = """Specifies the number of residues per protein monomer.
Only integers (whole numbers) should be given. The number and types of atoms for each
residue are given as:
amino acid = 5 carbon + 1.35 Nitrogren + 1.5 Oxygen + 8 Hydrogen.
Any sulfur atoms, e.g. from CYS and MET residues, should be added explicitly with
the "Heavy atoms in protein" option.
"""

        self.numRNAText = """Specifies the number of RNA nucleotides per monomer.
Only integers (whole numbers) should be given. The number and types of atoms for each
nucleotide (assuming average nucleotide content) are given as:
mean nucleotide = 9.5 carbon + 3.75 Nitrogren + 7 Oxygen + 11.25 Hydrogen + 1 Phosphorus.
Explicit atom specification with the "Heavy atoms in protein" option can be used
if more accuracy is necessary.
The default value is 0.
"""

        self.numDNAText = """Specifies the number of DNA nucleotides per monomer.
Only integers (whole numbers) should be given. The number and types of atoms for each
nucleotide (assuming average nucleotide content) are given as:
mean nucleotide = 9.75 carbon + 4 Nitrogren + 6 Oxygen + 11.75 Hydrogen + 1 Phosphorus.
Explicit atom specification with the "Heavy atoms in protein" option can be used
if more accuracy is necessary.
The default value is 0.
"""

        self.protHeavyText = """Specifies a list of atoms to add to the protein part of the absorption.
Each atomic species is defined by a two character string for the elemental
symbol and an integer (whole) number of atoms of that species per monomer.

Example:
To specify 10 sulfur atoms and 2 selenium atoms per monomer the input would be:
S 10 Se 2
"""
        self.solHeavyText = """Specifies a concentration of elements in the solvent (not including water).
The concentration should be given in millimoles per litre. Oxygen and lighter
elements should not be specified.

Example:
To specify 1 Molar sodium chloride in the solvent the input would be:
Na 1000 Cl 1000
"""

        self.solFracText = """Specifies the fraction of the unit cell that is occupied by the solvent.
If this value is not given then it is estimated from the number of residues, RNA
and DNA per monomer using the densities 1.35g/ml for protein, 1.35g/ml for DNA
and 1.30g/ml for RNA.

Only numerical values are accepted for this field and should be between 0 and 1.
"""

        self.protConcText = """Species the protein concentration of the sample in grams per litre.
Only numerical values are accepted for this field
"""

        self.conTypeText = """Specifies the type of container in which the sample (SAXS solution or crystal) is contained.
Currently there are three options:

1) None - The sample is not contained in anything. This is the default option
and is the case for any standard crystallography experiment.

2) Mixture - Defines a container encasing the irradiated sample which is a
mixture of elements, determined by the name of the mixture. There are specific
mixtures available in a drop down list for this option.

3) Elemental - Defines a container encasing the irradiated sample in terms of
its component elements. If this option is selected then the user must specify
the list of the material's component elements.

The information about the absorption properties of the container material is
extracted from the National Institute of Standards and Technology (NIST) tables
online. Therefore you need an internet connection if you choose a "mixture" or
"elemental" container composition.
"""

        self.conMixText = """Specifies the material of which the sample container is made given by the name of the mixture.
Choose from the list of predefined mixtures that are available on the National
Institute of Standards and Technology (NIST) website.
"""

        self.conElText = """Specifies the material of which the sample container is made given by the list of component elements.
Each atomic species is defined by a two character string for the elemental symbol and an
integer (whole) number of atoms.

Example:
If the material of the container is quartz (SAXS experiments are often performed
using a quartz capillary) which has the atomic formula: Si02 then the input would
be:
Si 1 O 2
"""
        self.conThick = """Specifies the thickness of the container encasing the sample.
The thickness should be given in units of microns.

Only numerical values are accepted for this field.
"""

        self.conDens = """Specifies the density of the container encasing the sample.
The density should be given in the units grams/centimetre.

Only numerical values are accepted for this field.
"""

        self.seqFileText= """Specifies the path to the sequence file.
This file should be a plain text file in fasta format:
http://blast.ncbi.nlm.nih.gov/blastcgihelp.shtml.        
"""


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
