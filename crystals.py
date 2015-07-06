import os

class crystals(object):
	# this class is for crystal parameters for a loaded or created crystal.
	# Default absCoefCalc is set to 'Average'
	def __init__(self, crystName="", crystType="", crystDimX=0, crystDimY=0, crystDimZ=0,
				 crystPixPerMic=0, angleP=0, angleL=0, containerInfoDict={}):

		self.crystName        = crystName
		self.type             = crystType
		self.crystDimX        = crystDimX
		self.crystDimY        = crystDimY
		self.crystDimZ        = crystDimZ
		self.pixelsPerMicron  = crystPixPerMic
		self.angleP 		  = angleP
		self.angleL 		  = angleL
		self.absCoeffCalc 	  = 'Average'

		# find the crystal container information, if it was provided when the crystal object was created
		self.containerInfoDict = containerInfoDict
		try:
			materialMixture,materialElements,containerThickness,containerDensity = self.getContainerInfo()
			self.materialMixture  	= materialMixture
			self.materialElements 	= materialElements
			self.containerThickness = containerThickness
			self.containerDensity 	= containerDensity
		except KeyError:
			pass

	def checkContainerInfoPresent(self):
		# check whether container info has been provided for crystal
		if len(self.containerInfoDict) != 0:
			return True
		else:
			return False

	def getContainerInfo(self):
		# get info regarding crystal container
		materialMixture		= self.containerInfoDict["Mixture"]
		materialElements 	= self.containerInfoDict["Elements"]
		containerThickness 	= self.containerInfoDict["Thickness"]
		containerDensity 	= self.containerInfoDict["Density"]

		return (materialMixture,materialElements,containerThickness,containerDensity)

	def checkValidInputs(self):
		ErrorMessage = ""
		# check valid crystal type
		if self.type not in ('Cuboid','Spherical','Cylindrical','Polyhedron'):
			ErrorMessage += 'Crystal type {} not of compatible format.\n'.format(str(self.type))

		# check that crystal dimensions can be converted to float format (from string format)
		try:
			float(self.crystDimX)
			float(self.crystDimY)
			float(self.crystDimZ)
		except ValueError:
			ErrorMessage += 'Crystal dimensions not of compatible float format.\n'

		# check that crystal pixelsPerMicron can be converted to float format (from string format)
		try:
			float(self.pixelsPerMicron)
		except ValueError:
			ErrorMessage += 'Crystal pixelsPerMicron input not of compatible float format.\n'

		# check that crystal angle P and angle L can be converted to float format (from string format)
		try:
			float(self.angleP)
			float(self.angleL)
		except ValueError:
			ErrorMessage += 'Crystal angle L or angle P input not of compatible float format.\n'

		return ErrorMessage

	def extractCrystalInfo(self):
		# create a string containing information of current crystal
		summaryString 	= 	"Crystal Name: {}\n".format(str(self.crystName))
		summaryString 	+= 	"nType: {}\n".format(str(self.type))
		summaryString 	+= 	"Dimensions: {} {} {} (microns in x,y,z)\n".format(str(self.crystDimX),str(self.crystDimY),str(self.crystDimZ))
		summaryString 	+= 	"Pixels per Micron: {}\n".format(str(self.pixelsPerMicron))
		summaryString 	+= 	"Angle P: {}\n".format(str(self.angleP))
		summaryString 	+= 	"Angle L: {}\n".format(str(self.angleL))

		# if container information was provided, include in summary
		if self.checkContainerInfoPresent() == True:
			containerString  	= 	"\nContainer Information:\n"
			containerString 	+= 	"Material Mixture: {}\n".format(str(self.materialMixture))
			containerString 	+= 	"Material Elements: {}\n".format(str(self.materialElements))
			containerString 	+= 	"Container Thickness: {}\n".format(str(self.containerThickness))
			containerString 	+= 	"Container Density: {}\n".format(str(self.containerDensity))
			summaryString += containerString

		return summaryString

class crystals_pdbCode(crystals):
	# A subclass for a single pdb file structure
	def __init__(self, crystName="", crystType="", crystDimX=0, crystDimY=0,crystDimZ=0,
				 crystPixPerMic=0, angleP=0, angleL=0, containerInfoDict={}, 
				 pdbcode="", solventHeavyConc=""):

		super(crystals_pdbCode, self).__init__(crystName, crystType, crystDimX, crystDimY, crystDimZ,
											   crystPixPerMic, angleP, angleL, containerInfoDict)

		self.pdbcode 			= pdbcode
		self.solventHeavyConc 	= solventHeavyConc
		self.absCoeffCalc 		= 'EXP'

	def checkValidInputs_subclass(self):
		ErrorMessage = ""
		# check valid pdb code input
		if len(self.pdbcode) != 4:
			ErrorMessage = ErrorMessage +  'PDB code input {} not of compatible format.\n'.format(str(self.pdbcode))

		return ErrorMessage

	def extractCrystalInfo_composition(self):
		# create a string containing information of current crystal composition
		compositionString  	= 	"\nComposition Information:\n"
		compositionString 	+= 	"PDB code: {}\n".format(str(self.pdbcode))
		compositionString 	+= 	"Solvent Heavy Atom Conc: {}\n".format(str(self.solventHeavyConc))

		return compositionString

class crystals_userDefined(crystals):
	# A subclass for a user defined crystal composition
	def __init__(self, crystName="", crystType="", crystDimX=0, crystDimY=0, crystDimZ=0,
				 crystPixPerMic=0, angleP=0, angleL=0, containerInfoDict={},
				 unitcell_a=0, unitcell_b=0, unitcell_c=0,
				 unitcell_alpha=0, unitcell_beta=0, unitcell_gamma=0,
				 numMonomers=0, numResidues=0, numRNA=0, numDNA=0,
				 proteinHeavyAtoms="", solventHeavyConc="", solventFraction=0):

		super(crystals_userDefined, self).__init__(crystName, crystType, crystDimX, crystDimY, crystDimZ,
												   crystPixPerMic, angleP, angleL, containerInfoDict)

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
		self.absCoeffCalc 		= 'RDV3'

	def checkValidInputs_subclass(self):
		ErrorMessage = ""
		# check that unit cell dimensions can be converted to float format (from string format)
		try:
			float(self.unitcell_a)
			float(self.unitcell_b)
			float(self.unitcell_c)
			float(self.unitcell_alpha)
			float(self.unitcell_beta)
			float(self.unitcell_gamma)
		except ValueError:
			ErrorMessage += 'Unit cell dimensions not of compatible float format.\n'

		try:
			float(self.numMonomers)
		except ValueError:
			ErrorMessage += 'Crystal numMonomers input not of compatible float format.\n'

		try:
			float(self.numResidues)
		except ValueError:
			ErrorMessage += 'Crystal numResidues input not of compatible float format.\n'

		try:
			float(self.numRNA)
		except ValueError:
			ErrorMessage += 'Crystal numRNA input not of compatible float format.\n'

		try:
			float(self.numDNA)
		except ValueError:
			ErrorMessage += 'Crystal numDNA input not of compatible float format.\n'

		try:
			float(self.solventFraction)
		except ValueError:
			ErrorMessage += 'Crystal solventFraction input not of compatible float format.\n'

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
		compositionString 	+= 	"Solvent Heavy Atom Conc: {}\n".format(str(self.solventHeavyConc))
		compositionString 	+= 	"Solvent Fraction: {}\n".format(str(self.solventFraction))

		return compositionString

class crystals_RADDOSEv2(crystals):
	# A subclass for RADDOSE-v2 crystal inputs
	def __init__(self, crystName="", crystType="", crystDimX=0, crystDimY=0, crystDimZ=0,
				 crystPixPerMic=0, angleP=0,angleL=0, containerInfoDict={},
				 unitcell_a=0, unitcell_b=0, unitcell_c=0,
				 unitcell_alpha=0, unitcell_beta=0, unitcell_gamma=0,
				 numMonomers=0, numResidues=0, numRNA=0, numDNA=0,
				 proteinHeavyAtoms="", solventHeavyConc="",solventFraction=0):

		super(crystals_RADDOSEv2, self).__init__(crystName, crystType, crystDimX, crystDimY, crystDimZ,
												 crystPixPerMic, angleP, angleL, containerInfoDict)

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
		self.absCoeffCalc 		= 'RDV2'

	def checkValidInputs_subclass(self):
		ErrorMessage = ""
		# check that unit cell dimensions can be converted to float format (from string format)
		try:
			float(self.unitcell_a)
			float(self.unitcell_b)
			float(self.unitcell_c)
			float(self.unitcell_alpha)
			float(self.unitcell_beta)
			float(self.unitcell_gamma)
		except ValueError:
			ErrorMessage = ErrorMessage + 'Unit cell dimensions not of compatible float format.\n'

		try:
			float(self.numMonomers)
		except ValueError:
			ErrorMessage += 'Crystal numMonomers input not of compatible float format.\n'

		try:
			float(self.numResidues)
		except ValueError:
			ErrorMessage += 'Crystal numResidues input not of compatible float format.\n'

		try:
			float(self.numRNA)
		except ValueError:
			ErrorMessage += 'Crystal numRNA input not of compatible float format.\n'

		try:
			float(self.numDNA)
		except ValueError:
			ErrorMessage += 'Crystal numDNA input not of compatible float format.\n'

		try:
			float(self.solventFraction)
		except ValueError:
			ErrorMessage += 'Crystal solventFraction input not of compatible float format.\n'

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
		compositionString 	+= 	"Solvent Heavy Atom Conc: {}\n".format(str(self.solventHeavyConc))
		compositionString 	+= 	"Solvent Fraction: {}\n".format(str(self.solventFraction))

		return compositionString

class crystals_seqFile(crystals):
	# A subclass for sequence file-defined crystal composition
	def __init__(self, crystName="", crystType="", crystDimX=0, crystDimY=0, crystDimZ=0,
				 crystPixPerMic=0, angleP=0, angleL=0, containerInfoDict={},
				 unitcell_a=0, unitcell_b=0, unitcell_c=0,
				 unitcell_alpha=0, unitcell_beta=0, unitcell_gamma=0,
				 numMonomers=0, sequenceFile="", proteinHeavyAtoms="",
				 solventHeavyConc="", solventFraction=0):

		super(crystals_seqFile, self).__init__(crystName, crystType, crystDimX, crystDimY, crystDimZ,
											   crystPixPerMic, angleP, angleL, containerInfoDict)

		self.unitcell_a 		= unitcell_a
		self.unitcell_b 		= unitcell_b
		self.unitcell_c 		= unitcell_c
		self.unitcell_alpha 	= unitcell_alpha
		self.unitcell_beta 		= unitcell_beta
		self.unitcell_gamma 	= unitcell_gamma
		self.numMonomers 		=  numMonomers
		self.proteinHeavyAtoms 	= proteinHeavyAtoms
		self.solventHeavyConc 	= solventHeavyConc
		self.solventFraction 	= solventFraction
		self.absCoeffCalc 		= 'RDV3'

	def checkValidInputs_subclass(self):
		ErrorMessage = ""
		# check that unit cell dimensions can be converted to float format (from string format)
		try:
			float(self.unitcell_a)
			float(self.unitcell_b)
			float(self.unitcell_c)
			float(self.unitcell_alpha)
			float(self.unitcell_beta)
			float(self.unitcell_gamma)
		except ValueError:
			ErrorMessage += 'Unit cell dimensions not of compatible float format.\n'

		try:
			float(self.numMonomers)
		except ValueError:
			ErrorMessage += 'Crystal numMonomers input not of compatible float format.\n'

		try:
			float(self.solventFraction)
		except ValueError:
			ErrorMessage += 'Crystal solventFraction input not of compatible float format.\n'

		return ErrorMessage

	def extractCrystalInfo_composition(self):
		# create a string containing information of current crystal composition
		compositionString  	= 	"\nComposition Information:\n"
		compositionString 	+= 	"Unit Cell Dimensions: {} {} {} (microns in a,b,c)\n".format(str(self.unitcell_a),str(self.unitcell_b),str(self.unitcell_c))
		compositionString 	+= 	"Unit Cell Angles: {} {} {} (degrees in alpha,beta,gamma)\n".format(str(self.unitcell_alpha),str(self.unitcell_beta),str(self.unitcell_gamma))
		compositionString 	+= 	"Number of Monomers: {}\n".format(str(self.numMonomers))
		compositionString 	+= 	"Protein Heavy Atom number: {}\n".format(str(self.proteinHeavyAtoms))
		compositionString 	+= 	"Solvent Heavy Atom Conc: {}\n".format(str(self.solventHeavyConc))
		compositionString 	+= 	"Solvent Fraction: {}\n".format(str(self.solventFraction))

		return compositionString

class crystals_SAXSuserDefined(crystals):
	# A subclass for user-defined SAXS crystal composition inputs
	def __init__(self, crystName="", crystType="", crystDimX=0, crystDimY=0, crystDimZ=0,
				 crystPixPerMic=0, angleP=0, angleL=0, containerInfoDict={},
				 unitcell_a=0, unitcell_b=0, unitcell_c=0,
				 unitcell_alpha=0, unitcell_beta=0, unitcell_gamma=0,
				 numResidues=0, numRNA=0, numDNA=0,
				 proteinHeavyAtoms="", solventHeavyConc="",
				 solventFraction=0, proteinConc=0):

		super(crystals_SAXSuserDefined, self).__init__(crystName, crystType, crystDimX, crystDimY, crystDimZ,
													   crystPixPerMic, angleP, angleL, containerInfoDict)

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
		self.absCoeffCalc 		= 'RDV3'

	def checkValidInputs_subclass(self):
		ErrorMessage = ""
		# check that unit cell dimensions can be converted to float format (from string format)
		try:
			float(self.unitcell_a)
			float(self.unitcell_b)
			float(self.unitcell_c)
			float(self.unitcell_alpha)
			float(self.unitcell_beta)
			float(self.unitcell_gamma)
		except ValueError:
			ErrorMessage += 'Unit cell dimensions not of compatible float format.\n'

		try:
			float(self.numResidues)
		except ValueError:
			ErrorMessage += 'Crystal numResidues input not of compatible float format.\n'

		try:
			float(self.numRNA)
		except ValueError:
			ErrorMessage += 'Crystal numRNA input not of compatible float format.\n'

		try:
			float(self.numDNA)
		except ValueError:
			ErrorMessage += 'Crystal numDNA input not of compatible float format.\n'

		try:
			float(self.solventFraction)
		except ValueError:
			ErrorMessage += 'Crystal solventFraction input not of compatible float format.\n'

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
		compositionString 	+= 	"Solvent Heavy Atom Conc: {}\n".format(str(self.solventHeavyConc))
		compositionString 	+= 	"Solvent Fraction: {}\n".format(str(self.solventFraction))
		compositionString 	+= 	"Protein Conc: {}\n".format(str(self.proteinConc))

		return compositionString

class crystals_SAXSseqFile(crystals):
	# A subclass for sequence file-defined SAXS crystal composition inputs
	def __init__(self, crystName="", crystType="", crystDimX=0, crystDimY=0, crystDimZ=0,
				 crystPixPerMic=0, angleP=0, angleL=0, containerInfoDict={},
				 unitcell_a=0, unitcell_b=0, unitcell_c=0,
				 unitcell_alpha=0, unitcell_beta=0, unitcell_gamma=0,
				 proteinHeavyAtoms="", solventHeavyConc="",
				 solventFraction=0, proteinConc=0, sequenceFile=""):

		super(crystals_SAXSseqFile, self).__init__(crystName, crystType, crystDimX, crystDimY, crystDimZ,
												   crystPixPerMic, angleP, angleL, containerInfoDict)

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
		self.sequenceFile 		= sequenceFile
		self.absCoeffCalc 		= 'RDV3'

	def checkValidInputs_subclass(self):
		ErrorMessage = ""
		# check that unit cell dimensions can be converted to float format (from string format)
		try:
			float(self.unitcell_a)
			float(self.unitcell_b)
			float(self.unitcell_c)
			float(self.unitcell_alpha)
			float(self.unitcell_beta)
			float(self.unitcell_gamma)
		except ValueError:
			ErrorMessage += 'Unit cell dimensions not of compatible float format.\n'

		try:
			float(self.solventFraction)
		except ValueError:
			ErrorMessage += 'Crystal solventFraction input not of compatible float format.\n'

		# check sequence file input is string
		if not isinstance(self.sequenceFile, basestring):
			ErrorMessage += 'Sequence file input {} not of compatible format.\n'.format(str(self.sequenceFile))

		return ErrorMessage

	def extractCrystalInfo_composition(self):
		# create a string containing information of current crystal composition
		compositionString  	= 	"\nComposition Information:\n"
		compositionString 	+= 	"Unit Cell Dimensions: {} {} {} (microns in a,b,c)\n".format(str(self.unitcell_a),str(self.unitcell_b),str(self.unitcell_c))
		compositionString 	+= 	"Unit Cell Angles: {} {} {} (degrees in alpha,beta,gamma)\n".format(str(self.unitcell_alpha),str(self.unitcell_beta),str(self.unitcell_gamma))
		compositionString 	+= 	"Protein Heavy Atom number: {}\n".format(str(self.proteinHeavyAtoms))
		compositionString 	+= 	"Solvent Heavy Atom Conc: {}\n".format(str(self.solventHeavyConc))
		compositionString 	+= 	"Solvent Fraction: {}\n".format(str(self.solventFraction))
		compositionString 	+= 	"Protein Conc: {}\n".format(str(self.proteinConc))
		compositionString 	+= 	"Sequence File: {}\n".format(str(self.sequenceFile))

		return compositionString

