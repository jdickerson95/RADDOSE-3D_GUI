import os
from checks import checks
import datetime
import time

class crystals(object):
	# this class is for crystal parameters for a loaded or created crystal.
	# Default absCoefCalc is set to 'Average'
	def __init__(self, crystName="", crystType="", crystDimX="", crystDimY="", crystDimZ="",
				 crystPixPerMic="", angleP="", angleL="", containerInfoDict={}, absCoefCalc="",modelFile=""):

		self.crystName        = crystName
		self.type             = crystType
		self.crystDimX        = crystDimX
		self.crystDimY        = crystDimY
		self.crystDimZ        = crystDimZ
		self.pixelsPerMicron  = crystPixPerMic
		self.angleP 		  = angleP
		self.angleL 		  = angleL
		self.absCoefCalc 	  = absCoefCalc
		self.modelFile 		  = modelFile

		# find the crystal container information, if it was provided when the crystal object was created
		self.containerInfoDict = containerInfoDict
		if self.checkContainerInfoPresent() == True:
			self.getContainerInfo()

		self.__creationTime =  self.getCreationTime()

	def getTimeStampedName(self):
		# create a string containing name then timestamp for unique crystal identification
		timeStampedName =  self.__creationTime + " "*10 + self.crystName
		return timeStampedName

	def getCreationTime(self):
		# get time of creation of current crystal object
		ts = time.time()
		creationTime = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
		return creationTime

	def __eq__(self, other) :
		"""This method checks to see if a crystal has the same properties as
		another crystal
		"""
		compareProps_self = {attr: getattr(self, attr) for attr in vars(self) if attr not in ('crystName','_crystals__creationTime')}
		compareProps_other = {attr: getattr(other, attr) for attr in vars(other) if attr not in ('crystName','_crystals__creationTime')}

		return compareProps_self == compareProps_other

	def setDimsByCrystType(self):
		# depending of the crystal type specified, update the dimensions 
		# of the crystal to the fixed format below
		crystalType = str(self.type).lower()
		if crystalType != 'polyhedron':
			self.modelFile = ""
			self.wireFrameType = ""
		else:
			self.wireFrameType = 'OBJ'
			
		if crystalType == 'spherical':
			self.crystDimY = ""
			self.crystDimZ = ""
		elif crystalType == 'cylindrical':
			self.crystDimZ = ""
		elif crystalType == 'polyhedron':
			self.crystDimX = ""
			self.crystDimY = ""
			self.crystDimZ = ""


	def checkContainerInfoPresent(self):
		# check whether container info has been provided for crystal
		try:
			self.containerInfoDict["Type"]
		except KeyError:
			return False
		if self.containerInfoDict["Type"] in ('Mixture','Elemental'):
			return True
		else:
			return False

	def getContainerInfo(self):
		# get info regarding crystal container
		self.containerType       	= self.containerInfoDict["Type"]
		self.containerThickness 	= self.containerInfoDict["Thickness"]
		self.containerDensity 		= self.containerInfoDict["Density"]
		if self.containerType == 'Mixture':
			self.materialMixture	= self.containerInfoDict["Mixture"]
		elif self.containerType == 'Elemental':
			self.materialElements 	= self.containerInfoDict["Elements"]

	def checkValidInputs(self):
		ErrorMessage = ""
		# check valid crystal type
		crystalType = str(self.type).lower()
		if crystalType not in ('cuboid','spherical','cylindrical','polyhedron'):
			ErrorMessage += 'Crystal type {} not of compatible format.\n'.format(str(self.type))

		# check that relevant crystal dimensions (dependent of crystal type) can be converted to 
		# non-negative float format (from string format)
		if crystalType in ('cuboid','spherical','cylindrical'):
			ErrorMessage += checks(self.crystDimX,'x dimension',False).checkIfNonNegFloat()
		if crystalType in ('cuboid','cylindrical'):
			ErrorMessage += checks(self.crystDimY,'y dimension',False).checkIfNonNegFloat()
		if crystalType in ('cuboid'):
			ErrorMessage += checks(self.crystDimZ,'z dimension',False).checkIfNonNegFloat()
		if crystalType in ('polyhedron'):
			ErrorMessage += checks(self.modelFile,'model file',False).checkIfNonBlankString()
			if str(self.wireFrameType).lower() != 'obj':
				ErrorMessage += 'Wire frame type not of compatible .obj format\n'

		# check that crystal pixelsPerMicron can be converted to non-negative float format (from string format)
		ErrorMessage += checks(self.pixelsPerMicron,'pixels per micron',False).checkIfNonNegFloat()

		# check that crystal angle P and angle L can be converted to float format (from string format)
		ErrorMessage += checks(self.angleP,'angle P',True).checkIfFloat()
		ErrorMessage += checks(self.angleL,'angle L',True).checkIfFloat()

		# check that absCoefCalc value of valid form
		if str(self.absCoefCalc).lower() not in ('average','exp','rd3d','rdv2','sequence','saxs','saxsseq'):
			ErrorMessage += 'Crystal absorption coefficient {} not of compatible format.\n'.format(str(self.absCoefCalc))

		# check container information is valid (if present)
		try:
			self.containerType
			# check that container type of suitable format
			if str(self.containerType).lower() not in ('mixture','elemental','none'):
				ErrorMessage += 'Crystal container type {} not of compatible format.\n'.format(str(self.containerType))

			# check that container thickness can be converted to float and is non-negative
			ErrorMessage += checks(self.containerThickness,'container thickness',False).checkIfNonNegFloat()

			# check that container density can be converted to float and is non-negative
			ErrorMessage += checks(self.containerDensity,'container density',False).checkIfNonNegFloat()

			# check that if 'mixture' type specified, then corresponding mixture is a non-empty string
			if str(self.containerType).lower() == 'mixture':
				if not isinstance(self.materialMixture, basestring):
					ErrorMessage += 'Crystal container mixture not of compatible string format.\n'
				elif len(self.materialMixture) == 0:
					ErrorMessage += 'Crystal container mixture field is blank.\n'

			# check that if 'elemental' type specified, then corresponding element composition is a non-empty string
			if str(self.containerType).lower() == 'elemental':
				if not isinstance(self.materialElements, basestring):
					ErrorMessage += 'Crystal container elemental composition not of compatible string format.\n'
				elif len(self.materialElements) == 0:
					ErrorMessage += 'Crystal container elemental composition field is blank.\n'
				else:
					# check that suitable heavy atom string formatting
					ErrorMessage += checks(self.materialElements,'material elemental composition',False).checkHeavyAtomFormat()
		except AttributeError:
			pass

		return ErrorMessage

	def extractCrystalInfo(self):
		# create a string containing information of current crystal
		summaryString 	= 	"Crystal Name: {}\n".format(str(self.crystName))
		summaryString 	+= 	"Type: {}\n".format(str(self.type))
		summaryString 	+= 	"Dimensions: {} {} {} (microns in x,y,z)\n".format(str(self.crystDimX),str(self.crystDimY),str(self.crystDimZ))
		summaryString 	+= 	"Pixels per Micron: {}\n".format(str(self.pixelsPerMicron))
		summaryString 	+= 	"Angle P: {}\n".format(str(self.angleP))
		summaryString 	+= 	"Angle L: {}\n".format(str(self.angleL))
		summaryString 	+= 	"Absorption Coeffient Calculation: {}\n".format(str(self.absCoefCalc))

		# if container information was provided, include in summary
		try:
			self.containerType
		except AttributeError:
			return summaryString
		if self.containerType in ('Mixture','Elemental'):
			containerString  	= 	"\nContainer Information:\n"
			containerString 	+= 	"Container Type: {}\n".format(str(self.containerType))
			if self.containerType == 'Mixture':
				containerString 	+= 	"Material Mixture: {}\n".format(str(self.materialMixture))
			elif self.containerType == 'Elemental':
				containerString 	+= 	"Material Elements: {}\n".format(str(self.materialElements))
			containerString 	+= 	"Container Thickness: {}\n".format(str(self.containerThickness))
			containerString 	+= 	"Container Density: {}\n".format(str(self.containerDensity))
			summaryString += containerString

		return summaryString

class crystals_pdbCode(crystals):
	# A subclass for a single pdb file structure
	def __init__(self, crystName="", crystType="", crystDimX="", crystDimY="",crystDimZ="",
				 crystPixPerMic="", angleP="", angleL="", containerInfoDict={}, absCoefCalc="",
				 modelFile="", pdbcode="", solventHeavyConc=""):

		super(crystals_pdbCode, self).__init__(crystName, crystType, crystDimX, crystDimY, crystDimZ,
											   crystPixPerMic, angleP, angleL, containerInfoDict, absCoefCalc, modelFile)

		self.pdb 			= pdbcode
		self.solventHeavyConc 	= solventHeavyConc

	def checkValidInputs_subclass(self):
		ErrorMessage = ""

		# check valid pdb code input
		if len(self.pdb) != 4:
			ErrorMessage += 'PDB code input {} not of compatible format.\n'.format(str(self.pdb))

		# check that crystal solventHeavyConc formatting is correct
		ErrorMessage += checks(self.solventHeavyConc,'solvent heavy atom concentration',True).checkHeavyAtomFormat()

		return ErrorMessage

	def extractCrystalInfo_composition(self):
		# create a string containing information of current crystal composition
		compositionString  	= 	"\nComposition Information:\n"
		compositionString 	+= 	"PDB code: {}\n".format(str(self.pdb))
		compositionString 	+= 	"Solvent Heavy Atom Concentration: {}\n".format(str(self.solventHeavyConc))

		return compositionString

class crystals_userDefined(crystals):
	# A subclass for a user defined crystal composition
	def __init__(self, crystName="", crystType="", crystDimX="", crystDimY="", crystDimZ="",
				 crystPixPerMic="", angleP="", angleL="", containerInfoDict={}, absCoefCalc="", modelFile="", 
				 unitcell_a="", unitcell_b="", unitcell_c="",
				 unitcell_alpha="", unitcell_beta="", unitcell_gamma="",
				 numMonomers="", numResidues="", numRNA="", numDNA="",
				 proteinHeavyAtoms="", solventHeavyConc="", solventFraction=""):

		super(crystals_userDefined, self).__init__(crystName, crystType, crystDimX, crystDimY, crystDimZ,
												   crystPixPerMic, angleP, angleL, containerInfoDict, absCoefCalc, modelFile)

		self.unitcell_a 		= unitcell_a
		self.unitcell_b 		= unitcell_b
		self.unitcell_c 		= unitcell_c
		self.unitcell_alpha 	= unitcell_alpha
		self.unitcell_beta 		= unitcell_beta
		self.unitcell_gamma 	= unitcell_gamma
		self.numMonomers 		= numMonomers
		self.numResidues 		= numResidues
		self.numRNA 			= numRNA
		self.numDNA 			= numDNA
		self.proteinHeavyAtoms 	= proteinHeavyAtoms
		self.solventHeavyConc 	= solventHeavyConc
		self.solventFraction 	= solventFraction

	def checkValidInputs_subclass(self):
		ErrorMessage = ""

		# check that unit cell dimensions can be converted to non-negative float format (from string format)
		ErrorMessage += checks(self.unitcell_a,'unit cell a dimension',False).checkIfNonNegFloat()
		ErrorMessage += checks(self.unitcell_b,'unit cell b dimension',False).checkIfNonNegFloat()
		ErrorMessage += checks(self.unitcell_c,'unit cell c dimension',False).checkIfNonNegFloat()
		ErrorMessage += checks(self.unitcell_alpha,'unit cell angle alpha',True).checkIfNonNegFloat()
		ErrorMessage += checks(self.unitcell_beta,'unit cell angle beta',True).checkIfNonNegFloat()
		ErrorMessage += checks(self.unitcell_gamma,'unit cell angle gamma',True).checkIfNonNegFloat()

		# check that number of monomers/residues has been filled in and can be converted to non-negative integers
		ErrorMessage += checks(self.numMonomers,'number of monomers',False).checkIfNonNegInt()
		ErrorMessage += checks(self.numResidues,'number of residues',False).checkIfNonNegInt()

		# check that number of RNA/DNA nucleotides can be converted to non-negative integers
		ErrorMessage += checks(self.numRNA,'number of RNA nucleotides',True).checkIfNonNegInt()
		ErrorMessage += checks(self.numDNA,'number of DNA nucleotides',True).checkIfNonNegInt()

		# check that crystal proteinHeavyAtoms formatting is correct
		ErrorMessage += checks(self.proteinHeavyAtoms,'heavy atoms in protein',True).checkHeavyAtomFormat()

		# check that crystal solventHeavyConc formatting is correct
		ErrorMessage += checks(self.solventHeavyConc,'solvent heavy atom concentration',True).checkHeavyAtomFormat()

		# check that solvent fraction is float between 0 and 1
		ErrorMessage += checks(self.solventFraction,'solvent fraction',True).checkIfFloatBetween01()

		return ErrorMessage

	def extractCrystalInfo_composition(self):
		# create a string containing information of current crystal composition
		compositionString  	= 	"\nComposition Information:\n"
		compositionString 	+= 	"Unit Cell Dimensions: {} {} {} (microns in a,b,c)\n".format(str(self.unitcell_a),str(self.unitcell_b),str(self.unitcell_c))
		compositionString 	+= 	"Unit Cell Angles: {} {} {} (degrees in alpha,beta,gamma)\n".format(str(self.unitcell_alpha),str(self.unitcell_beta),str(self.unitcell_gamma))
		compositionString 	+= 	"Number of Monomers: {}\n".format(str(self.numMonomers))
		compositionString 	+= 	"Number of Residues: {}\n".format(str(self.numResidues))
		compositionString 	+= 	"Number of RNA: {}\n".format(str(self.numRNA))
		compositionString 	+= 	"Number of DNA: {}\n".format(str(self.numDNA))
		compositionString 	+= 	"Protein Heavy Atom number: {}\n".format(str(self.proteinHeavyAtoms))
		compositionString 	+= 	"Solvent Heavy Atom Concentration: {}\n".format(str(self.solventHeavyConc))
		compositionString 	+= 	"Solvent Fraction: {}\n".format(str(self.solventFraction))

		return compositionString

class crystals_RADDOSEv2(crystals):
	# A subclass for RADDOSE-v2 crystal inputs
	def __init__(self, crystName="", crystType="", crystDimX="", crystDimY="", crystDimZ="",
				 crystPixPerMic="", angleP="",angleL="", containerInfoDict={}, absCoefCalc="", modelFile="", 
				 unitcell_a="", unitcell_b="", unitcell_c="",
				 unitcell_alpha="", unitcell_beta="", unitcell_gamma="",
				 numMonomers="", numResidues="", numRNA="", numDNA="",
				 proteinHeavyAtoms="", solventHeavyConc="",solventFraction=""):

		super(crystals_RADDOSEv2, self).__init__(crystName, crystType, crystDimX, crystDimY, crystDimZ,
												 crystPixPerMic, angleP, angleL, containerInfoDict, absCoefCalc, modelFile)

		self.unitcell_a 		= unitcell_a
		self.unitcell_b 		= unitcell_b
		self.unitcell_c 		= unitcell_c
		self.unitcell_alpha 	= unitcell_alpha
		self.unitcell_beta 		= unitcell_beta
		self.unitcell_gamma 	= unitcell_gamma
		self.numMonomers 		=  numMonomers
		self.numResidues 		= numResidues
		self.numRNA 			= numRNA
		self.numDNA 			= numDNA
		self.proteinHeavyAtoms 	= proteinHeavyAtoms
		self.solventHeavyConc 	= solventHeavyConc
		self.solventFraction 	= solventFraction

	def checkValidInputs_subclass(self):
		ErrorMessage = ""

		# check that unit cell dimensions can be converted to non-negative float format (from string format)
		ErrorMessage += checks(self.unitcell_a,'unit cell a dimension',False).checkIfNonNegFloat()
		ErrorMessage += checks(self.unitcell_b,'unit cell b dimension',False).checkIfNonNegFloat()
		ErrorMessage += checks(self.unitcell_c,'unit cell c dimension',False).checkIfNonNegFloat()
		ErrorMessage += checks(self.unitcell_alpha,'unit cell angle alpha',True).checkIfNonNegFloat()
		ErrorMessage += checks(self.unitcell_beta,'unit cell angle beta',True).checkIfNonNegFloat()
		ErrorMessage += checks(self.unitcell_gamma,'unit cell angle gamma',True).checkIfNonNegFloat()

		# check that number of monomers/residues has been filled in and can be converted to non-negative integers
		ErrorMessage += checks(self.numMonomers,'number of monomers',False).checkIfNonNegInt()
		ErrorMessage += checks(self.numResidues,'number of residues',False).checkIfNonNegInt()

		# check that number of RNA/DNA nucleotides can be converted to non-negative integers
		ErrorMessage += checks(self.numRNA,'number of RNA nucleotides',True).checkIfNonNegInt()
		ErrorMessage += checks(self.numDNA,'number of DNA nucleotides',True).checkIfNonNegInt()

		# check that crystal proteinHeavyAtoms formatting is correct
		ErrorMessage += checks(self.proteinHeavyAtoms,'heavy atoms in protein',True).checkHeavyAtomFormat()

		# check that crystal solventHeavyConc formatting is correct
		ErrorMessage += checks(self.solventHeavyConc,'solvent heavy atom concentration',True).checkHeavyAtomFormat()

		# check that solvent fraction is float between 0 and 1
		ErrorMessage += checks(self.solventFraction,'solvent fraction',True).checkIfFloatBetween01()

		return ErrorMessage

	def extractCrystalInfo_composition(self):
		# create a string containing information of current crystal composition
		compositionString  	= 	"\nComposition Information:\n"
		compositionString 	+= 	"Unit Cell Dimensions: {} {} {} (microns in a,b,c)\n".format(str(self.unitcell_a),str(self.unitcell_b),str(self.unitcell_c))
		compositionString 	+= 	"Unit Cell Angles: {} {} {} (degrees in alpha,beta,gamma)\n".format(str(self.unitcell_alpha),str(self.unitcell_beta),str(self.unitcell_gamma))
		compositionString 	+= 	"Number of Monomers: {}\n".format(str(self.numMonomers))
		compositionString 	+= 	"Number of Residues: {}\n".format(str(self.numResidues))
		compositionString 	+= 	"Number of RNA: {}\n".format(str(self.numRNA))
		compositionString 	+= 	"Number of DNA: {}\n".format(str(self.numDNA))
		compositionString 	+= 	"Protein Heavy Atom number: {}\n".format(str(self.proteinHeavyAtoms))
		compositionString 	+= 	"Solvent Heavy Atom Concentration: {}\n".format(str(self.solventHeavyConc))
		compositionString 	+= 	"Solvent Fraction: {}\n".format(str(self.solventFraction))

		return compositionString

class crystals_seqFile(crystals):
	# A subclass for sequence file-defined crystal composition
	def __init__(self, crystName="", crystType="", crystDimX="", crystDimY="", crystDimZ="",
				 crystPixPerMic="", angleP="", angleL="", containerInfoDict={}, absCoefCalc="", modelFile="", 
				 unitcell_a="", unitcell_b="", unitcell_c="",
				 unitcell_alpha="", unitcell_beta="", unitcell_gamma="",
				 numMonomers="", sequenceFile="", proteinHeavyAtoms="",
				 solventHeavyConc="", solventFraction=""):

		super(crystals_seqFile, self).__init__(crystName, crystType, crystDimX, crystDimY, crystDimZ,
											   crystPixPerMic, angleP, angleL, containerInfoDict, absCoefCalc, modelFile)

		self.unitcell_a 		= unitcell_a
		self.unitcell_b 		= unitcell_b
		self.unitcell_c 		= unitcell_c
		self.unitcell_alpha 	= unitcell_alpha
		self.unitcell_beta 		= unitcell_beta
		self.unitcell_gamma 	= unitcell_gamma
		self.numMonomers 		=  numMonomers
		self.seqFile 			= sequenceFile
		self.proteinHeavyAtoms 	= proteinHeavyAtoms
		self.solventHeavyConc 	= solventHeavyConc
		self.solventFraction 	= solventFraction

	def checkValidInputs_subclass(self):
		ErrorMessage = ""

		# check that unit cell dimensions can be converted to non-negative float format (from string format)
		ErrorMessage += checks(self.unitcell_a,'unit cell a dimension',False).checkIfNonNegFloat()
		ErrorMessage += checks(self.unitcell_b,'unit cell b dimension',False).checkIfNonNegFloat()
		ErrorMessage += checks(self.unitcell_c,'unit cell c dimension',False).checkIfNonNegFloat()
		ErrorMessage += checks(self.unitcell_alpha,'unit cell angle alpha',True).checkIfNonNegFloat()
		ErrorMessage += checks(self.unitcell_beta,'unit cell angle beta',True).checkIfNonNegFloat()
		ErrorMessage += checks(self.unitcell_gamma,'unit cell angle gamma',True).checkIfNonNegFloat()

		# check that number of monomers has been filled in and can be converted to a non-negative integer
		ErrorMessage += checks(self.numMonomers,'number of monomers',False).checkIfNonNegInt()

		# check that crystal proteinHeavyAtoms formatting is correct
		ErrorMessage += checks(self.proteinHeavyAtoms,'heavy atoms in protein',True).checkHeavyAtomFormat()

		# check that crystal solventHeavyConc formatting is correct
		ErrorMessage += checks(self.solventHeavyConc,'solvent heavy atom concentration',True).checkHeavyAtomFormat()

		# check that solvent fraction is float between 0 and 1
		ErrorMessage += checks(self.solventFraction,'solvent fraction',True).checkIfFloatBetween01()

		# check that sequence file name has been entered
		ErrorMessage += checks(self.seqFile,'sequence file',False).checkIfNonBlankString()

		return ErrorMessage

	def extractCrystalInfo_composition(self):
		# create a string containing information of current crystal composition
		compositionString  	= 	"\nComposition Information:\n"
		compositionString 	+= 	"Unit Cell Dimensions: {} {} {} (microns in a,b,c)\n".format(str(self.unitcell_a),str(self.unitcell_b),str(self.unitcell_c))
		compositionString 	+= 	"Unit Cell Angles: {} {} {} (degrees in alpha,beta,gamma)\n".format(str(self.unitcell_alpha),str(self.unitcell_beta),str(self.unitcell_gamma))
		compositionString 	+= 	"Number of Monomers: {}\n".format(str(self.numMonomers))
		compositionString 	+= 	"Protein Heavy Atom number: {}\n".format(str(self.proteinHeavyAtoms))
		compositionString 	+= 	"Solvent Heavy Atom Concentration: {}\n".format(str(self.solventHeavyConc))
		compositionString 	+= 	"Solvent Fraction: {}\n".format(str(self.solventFraction))
		compositionString   +=  "Sequence File: {}\n".format(str(self.seqFile))

		return compositionString

class crystals_SAXSuserDefined(crystals):
	# A subclass for user-defined SAXS crystal composition inputs
	def __init__(self, crystName="", crystType="", crystDimX="", crystDimY="", crystDimZ="",
				 crystPixPerMic="", angleP="", angleL="", containerInfoDict={}, absCoefCalc="", modelFile="", 
				 unitcell_a="", unitcell_b="", unitcell_c="",
				 unitcell_alpha="", unitcell_beta="", unitcell_gamma="",
				 numResidues="", numRNA="", numDNA="",
				 proteinHeavyAtoms="", solventHeavyConc="",
				 solventFraction="", proteinConc=""):

		super(crystals_SAXSuserDefined, self).__init__(crystName, crystType, crystDimX, crystDimY, crystDimZ,
													   crystPixPerMic, angleP, angleL, containerInfoDict, absCoefCalc, modelFile)

		self.unitcell_a 		= unitcell_a
		self.unitcell_b 		= unitcell_b
		self.unitcell_c 		= unitcell_c
		self.unitcell_alpha 	= unitcell_alpha
		self.unitcell_beta 		= unitcell_beta
		self.unitcell_gamma 	= unitcell_gamma
		self.numResidues 		= numResidues
		self.numRNA 			= numRNA
		self.numDNA 			= numDNA
		self.proteinHeavyAtoms 	= proteinHeavyAtoms
		self.solventHeavyConc 	= solventHeavyConc
		self.solventFraction 	= solventFraction
		self.proteinConc 		= proteinConc

	def checkValidInputs_subclass(self):
		ErrorMessage = ""

		# check that unit cell dimensions can be converted to non-negative float format (from string format)
		ErrorMessage += checks(self.unitcell_a,'unit cell a dimension',False).checkIfNonNegFloat()
		ErrorMessage += checks(self.unitcell_b,'unit cell b dimension',False).checkIfNonNegFloat()
		ErrorMessage += checks(self.unitcell_c,'unit cell c dimension',False).checkIfNonNegFloat()
		ErrorMessage += checks(self.unitcell_alpha,'unit cell angle alpha',True).checkIfNonNegFloat()
		ErrorMessage += checks(self.unitcell_beta,'unit cell angle beta',True).checkIfNonNegFloat()
		ErrorMessage += checks(self.unitcell_gamma,'unit cell angle gamma',True).checkIfNonNegFloat()

		# check that protein concentration can be converted to non-negative float format (from string)
		ErrorMessage += checks(self.proteinConc,'protein concentration',False).checkIfNonNegFloat()

		# check that number of residues has been filled in and can be converted to a non-negative integer
		ErrorMessage += checks(self.numResidues,'number of residues',False).checkIfNonNegInt()

		# check that number of RNA/DNA nucleotides can be converted to non-negative integers
		ErrorMessage += checks(self.numRNA,'number of RNA nucleotides',True).checkIfNonNegInt()
		ErrorMessage += checks(self.numDNA,'number of DNA nucleotides',True).checkIfNonNegInt()

		# check that crystal proteinHeavyAtoms formatting is correct
		ErrorMessage += checks(self.proteinHeavyAtoms,'heavy atoms in protein',True).checkHeavyAtomFormat()

		# check that crystal solventHeavyConc formatting is correct
		ErrorMessage += checks(self.solventHeavyConc,'solvent heavy atom concentration',True).checkHeavyAtomFormat()

		# check that solvent fraction is float between 0 and 1
		ErrorMessage += checks(self.solventFraction,'solvent fraction',True).checkIfFloatBetween01()

		return ErrorMessage

	def extractCrystalInfo_composition(self):
		# create a string containing information of current crystal composition
		compositionString  	= 	"\nComposition Information:\n"
		compositionString 	+= 	"Unit Cell Dimensions: {} {} {} (microns in a,b,c)\n".format(str(self.unitcell_a),str(self.unitcell_b),str(self.unitcell_c))
		compositionString 	+= 	"Unit Cell Angles: {} {} {} (degrees in alpha,beta,gamma)\n".format(str(self.unitcell_alpha),str(self.unitcell_beta),str(self.unitcell_gamma))
		compositionString 	+= 	"Number of Residues: {}\n".format(str(self.numResidues))
		compositionString 	+= 	"Number of RNA: {}\n".format(str(self.numRNA))
		compositionString 	+= 	"Number of DNA: {}\n".format(str(self.numDNA))
		compositionString 	+= 	"Protein Heavy Atom number: {}\n".format(str(self.proteinHeavyAtoms))
		compositionString 	+= 	"Solvent Heavy Atom Concentration: {}\n".format(str(self.solventHeavyConc))
		compositionString 	+= 	"Solvent Fraction: {}\n".format(str(self.solventFraction))
		compositionString 	+= 	"Protein Concentration: {}\n".format(str(self.proteinConc))

		return compositionString

class crystals_SAXSseqFile(crystals):
	# A subclass for sequence file-defined SAXS crystal composition inputs
	def __init__(self, crystName="", crystType="", crystDimX="", crystDimY="", crystDimZ="",
				 crystPixPerMic="", angleP="", angleL="", containerInfoDict={}, absCoefCalc="", modelFile="", 
				 unitcell_a="", unitcell_b="", unitcell_c="",
				 unitcell_alpha="", unitcell_beta="", unitcell_gamma="",
				 proteinHeavyAtoms="", solventHeavyConc="",
				 solventFraction="", proteinConc="", sequenceFile=""):

		super(crystals_SAXSseqFile, self).__init__(crystName, crystType, crystDimX, crystDimY, crystDimZ,
												   crystPixPerMic, angleP, angleL, containerInfoDict, absCoefCalc, modelFile)

		self.unitcell_a 		= unitcell_a
		self.unitcell_b 		= unitcell_b
		self.unitcell_c 		= unitcell_c
		self.unitcell_alpha		= unitcell_alpha
		self.unitcell_beta 		= unitcell_beta
		self.unitcell_gamma 	= unitcell_gamma
		self.proteinHeavyAtoms 	= proteinHeavyAtoms
		self.solventHeavyConc 	= solventHeavyConc
		self.solventFraction 	= solventFraction
		self.proteinConc 		= proteinConc
		self.seqFile 			= sequenceFile


	def checkValidInputs_subclass(self):
		ErrorMessage = ""

		# check that unit cell dimensions can be converted to non-negative float format (from string format)
		ErrorMessage += checks(self.unitcell_a,'unit cell a dimension',False).checkIfNonNegFloat()
		ErrorMessage += checks(self.unitcell_b,'unit cell b dimension',False).checkIfNonNegFloat()
		ErrorMessage += checks(self.unitcell_c,'unit cell c dimension',False).checkIfNonNegFloat()
		ErrorMessage += checks(self.unitcell_alpha,'unit cell angle alpha',True).checkIfNonNegFloat()
		ErrorMessage += checks(self.unitcell_beta,'unit cell angle beta',True).checkIfNonNegFloat()
		ErrorMessage += checks(self.unitcell_gamma,'unit cell angle gamma',True).checkIfNonNegFloat()

		# check that protein concentration can be converted to non-negative float format (from string)
		ErrorMessage += checks(self.proteinConc,'protein concentration',False).checkIfNonNegFloat()

		# check that crystal proteinHeavyAtoms formatting is correct
		ErrorMessage += checks(self.proteinHeavyAtoms,'heavy atoms in protein',True).checkHeavyAtomFormat()

		# check that crystal solventHeavyConc formatting is correct
		ErrorMessage += checks(self.solventHeavyConc,'solvent heavy atom concentration',True).checkHeavyAtomFormat()

		# check that solvent fraction is float between 0 and 1
		ErrorMessage += checks(self.solventFraction,'solvent fraction',True).checkIfFloatBetween01()

		# check that sequence file name has been entered
		ErrorMessage += checks(self.seqFile,'sequence file',False).checkIfNonBlankString()

		return ErrorMessage

	def extractCrystalInfo_composition(self):
		# create a string containing information of current crystal composition
		compositionString  	= 	"\nComposition Information:\n"
		compositionString 	+= 	"Unit Cell Dimensions: {} {} {} (microns in a,b,c)\n".format(str(self.unitcell_a),str(self.unitcell_b),str(self.unitcell_c))
		compositionString 	+= 	"Unit Cell Angles: {} {} {} (degrees in alpha,beta,gamma)\n".format(str(self.unitcell_alpha),str(self.unitcell_beta),str(self.unitcell_gamma))
		compositionString 	+= 	"Protein Heavy Atom number: {}\n".format(str(self.proteinHeavyAtoms))
		compositionString 	+= 	"Solvent Heavy Atom Concenctration: {}\n".format(str(self.solventHeavyConc))
		compositionString 	+= 	"Solvent Fraction: {}\n".format(str(self.solventFraction))
		compositionString 	+= 	"Protein Concentration: {}\n".format(str(self.proteinConc))
		compositionString 	+= 	"Sequence File: {}\n".format(str(self.seqFile))

		return compositionString
