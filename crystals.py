import os

class crystals(object):
	# this class is for crystal parameters for a loaded or created crystal.
	# Default absCoefCalc is set to 'Average'
	def __init__(self, crystName="", crystType="", crystDimX=0, crystDimY=0, crystDimZ=0,
				 crystPixPerMic=0, angleP=0, angleL=0, containerInfoDict={}, absCoefCalc=""):

		self.crystName        = crystName
		self.type             = crystType
		self.crystDimX        = crystDimX
		self.crystDimY        = crystDimY
		self.crystDimZ        = crystDimZ
		self.pixelsPerMicron  = crystPixPerMic
		self.angleP 		  = angleP
		self.angleL 		  = angleL
		self.absCoefCalc 	  = absCoefCalc

		# find the crystal container information, if it was provided when the crystal object was created
		self.containerInfoDict = containerInfoDict
		if self.checkContainerInfoPresent() == True:
			self.getContainerInfo()

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
		if str(self.type).lower() not in ('cuboid','spherical','cylindrical','polyhedron'):
			ErrorMessage += 'Crystal type {} not of compatible format.\n'.format(str(self.type))

		# check that crystal dimensions can be converted to float format (from string format)
		ErrorMessage += self.checkIfFloat(self.crystDimX,'x dimension')
		ErrorMessage += self.checkIfFloat(self.crystDimY,'y dimension')
		ErrorMessage += self.checkIfFloat(self.crystDimZ,'z dimension')

		# check that crystal dimensions are non-negative
		ErrorMessage += self.checkIfPositive(self.crystDimX,'x dimension')
		ErrorMessage += self.checkIfPositive(self.crystDimY,'y dimension')
		ErrorMessage += self.checkIfPositive(self.crystDimZ,'z dimension')

		# check that crystal pixelsPerMicron can be converted to float format (from string format)
		ErrorMessage += self.checkIfFloat(self.pixelsPerMicron,'pixels per micron')

		# check that crystal pixelsPerMicron value is non-negative
		ErrorMessage += self.checkIfPositive(self.pixelsPerMicron,'pixels per micron')

		# check that crystal angle P and angle L can be converted to float format (from string format)
		ErrorMessage += self.checkIfFloat(self.angleP,'angle P')
		ErrorMessage += self.checkIfFloat(self.angleL,'angle L')

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
			ErrorMessage += self.checkIfFloat(self.containerThickness,'container thickness')
			ErrorMessage += self.checkIfPositive(self.containerThickness,'container thickness')
			# check that container density can be converted to float and is non-negative
			ErrorMessage += self.checkIfFloat(self.containerDensity,'container density')
			ErrorMessage += self.checkIfPositive(self.containerDensity,'container density')
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
					# check that string contains an even number terms
					ErrorMessage += self.checkIfEvenNumTerms(self.materialElements,'material elemental composition')
					# check that every second term can be converted to float
					ErrorMessage += self.checkIfEverySecondTermFloat(self.materialElements,'material elemental composition')
		except AttributeError:
			pass 
	
		return ErrorMessage

	def checkIfEverySecondTermFloat(self,property,propertyName):
		ErrorMessage = ""
		# check every second element in list
		for value in property.split()[1::2]:
			try:
				float(value)
			except ValueError:
				ErrorMessage = 'Every second term in Crystal {} field not of compatible float format.\n'.format(propertyName)
		return ErrorMessage

	def checkIfEvenNumTerms(self,property,propertyName):
		ErrorMessage = ""
		if len(property.split()) % 2 != 0:
			ErrorMessage = 'Crystal {} input requires even number of terms.\n'.format(propertyName)
		return ErrorMessage

	def checkIfFloat(self,property,propertyName):
		ErrorMessage = ""
		try:
			float(property)
		except ValueError:
			ErrorMessage = 'Crystal {} not of compatible float format.\n'.format(propertyName)
		return ErrorMessage

	def checkIfPositive(self,property,propertyName):
		ErrorMessage = ""
		try:
			if float(property) < 0:
				ErrorMessage = 'Crystal {} must be non negative.\n'.format(propertyName)
		except ValueError:
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
	def __init__(self, crystName="", crystType="", crystDimX=0, crystDimY=0,crystDimZ=0,
				 crystPixPerMic=0, angleP=0, angleL=0, containerInfoDict={}, absCoefCalc="",
				 pdbcode="", solventHeavyConc=""):

		super(crystals_pdbCode, self).__init__(crystName, crystType, crystDimX, crystDimY, crystDimZ,
											   crystPixPerMic, angleP, angleL, containerInfoDict, absCoefCalc)

		self.pdb 			= pdbcode
		self.solventHeavyConc 	= solventHeavyConc

	def checkValidInputs_subclass(self):
		ErrorMessage = ""
		# check valid pdb code input
		if len(self.pdb) != 4:
			ErrorMessage = ErrorMessage +  'PDB code input {} not of compatible format.\n'.format(str(self.pdb))

		return ErrorMessage

	def extractCrystalInfo_composition(self):
		# create a string containing information of current crystal composition
		compositionString  	= 	"\nComposition Information:\n"
		compositionString 	+= 	"PDB code: {}\n".format(str(self.pdb))
		compositionString 	+= 	"Solvent Heavy Atom Concentration: {}\n".format(str(self.solventHeavyConc))

		return compositionString

class crystals_userDefined(crystals):
	# A subclass for a user defined crystal composition
	def __init__(self, crystName="", crystType="", crystDimX=0, crystDimY=0, crystDimZ=0,
				 crystPixPerMic=0, angleP=0, angleL=0, containerInfoDict={}, absCoefCalc="",
				 unitcell_a=0, unitcell_b=0, unitcell_c=0,
				 unitcell_alpha=0, unitcell_beta=0, unitcell_gamma=0,
				 numMonomers=0, numResidues=0, numRNA=0, numDNA=0,
				 proteinHeavyAtoms="", solventHeavyConc="", solventFraction=0):

		super(crystals_userDefined, self).__init__(crystName, crystType, crystDimX, crystDimY, crystDimZ,
												   crystPixPerMic, angleP, angleL, containerInfoDict, absCoefCalc)

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
		compositionString 	+= 	"Solvent Heavy Atom Concentration: {}\n".format(str(self.solventHeavyConc))
		compositionString 	+= 	"Solvent Fraction: {}\n".format(str(self.solventFraction))

		return compositionString

class crystals_RADDOSEv2(crystals):
	# A subclass for RADDOSE-v2 crystal inputs
	def __init__(self, crystName="", crystType="", crystDimX=0, crystDimY=0, crystDimZ=0,
				 crystPixPerMic=0, angleP=0,angleL=0, containerInfoDict={}, absCoefCalc="",
				 unitcell_a=0, unitcell_b=0, unitcell_c=0,
				 unitcell_alpha=0, unitcell_beta=0, unitcell_gamma=0,
				 numMonomers=0, numResidues=0, numRNA=0, numDNA=0,
				 proteinHeavyAtoms="", solventHeavyConc="",solventFraction=0):

		super(crystals_RADDOSEv2, self).__init__(crystName, crystType, crystDimX, crystDimY, crystDimZ,
												 crystPixPerMic, angleP, angleL, containerInfoDict, absCoefCalc)

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
		compositionString 	+= 	"Solvent Heavy Atom Concentration: {}\n".format(str(self.solventHeavyConc))
		compositionString 	+= 	"Solvent Fraction: {}\n".format(str(self.solventFraction))

		return compositionString

class crystals_seqFile(crystals):
	# A subclass for sequence file-defined crystal composition
	def __init__(self, crystName="", crystType="", crystDimX=0, crystDimY=0, crystDimZ=0,
				 crystPixPerMic=0, angleP=0, angleL=0, containerInfoDict={}, absCoefCalc="",
				 unitcell_a=0, unitcell_b=0, unitcell_c=0,
				 unitcell_alpha=0, unitcell_beta=0, unitcell_gamma=0,
				 numMonomers=0, sequenceFile="", proteinHeavyAtoms="",
				 solventHeavyConc="", solventFraction=0):

		super(crystals_seqFile, self).__init__(crystName, crystType, crystDimX, crystDimY, crystDimZ,
											   crystPixPerMic, angleP, angleL, containerInfoDict, absCoefCalc)

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
		compositionString 	+= 	"Solvent Heavy Atom Concentration: {}\n".format(str(self.solventHeavyConc))
		compositionString 	+= 	"Solvent Fraction: {}\n".format(str(self.solventFraction))

		return compositionString

class crystals_SAXSuserDefined(crystals):
	# A subclass for user-defined SAXS crystal composition inputs
	def __init__(self, crystName="", crystType="", crystDimX=0, crystDimY=0, crystDimZ=0,
				 crystPixPerMic=0, angleP=0, angleL=0, containerInfoDict={}, absCoefCalc="",
				 unitcell_a=0, unitcell_b=0, unitcell_c=0,
				 unitcell_alpha=0, unitcell_beta=0, unitcell_gamma=0,
				 numResidues=0, numRNA=0, numDNA=0,
				 proteinHeavyAtoms="", solventHeavyConc="",
				 solventFraction=0, proteinConc=0):

		super(crystals_SAXSuserDefined, self).__init__(crystName, crystType, crystDimX, crystDimY, crystDimZ,
													   crystPixPerMic, angleP, angleL, containerInfoDict, absCoefCalc)

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
		compositionString 	+= 	"Solvent Heavy Atom Concentration: {}\n".format(str(self.solventHeavyConc))
		compositionString 	+= 	"Solvent Fraction: {}\n".format(str(self.solventFraction))
		compositionString 	+= 	"Protein Concentration: {}\n".format(str(self.proteinConc))

		return compositionString

class crystals_SAXSseqFile(crystals):
	# A subclass for sequence file-defined SAXS crystal composition inputs
	def __init__(self, crystName="", crystType="", crystDimX=0, crystDimY=0, crystDimZ=0,
				 crystPixPerMic=0, angleP=0, angleL=0, containerInfoDict={}, absCoefCalc="",
				 unitcell_a=0, unitcell_b=0, unitcell_c=0,
				 unitcell_alpha=0, unitcell_beta=0, unitcell_gamma=0,
				 proteinHeavyAtoms="", solventHeavyConc="",
				 solventFraction=0, proteinConc=0, sequenceFile=""):

		super(crystals_SAXSseqFile, self).__init__(crystName, crystType, crystDimX, crystDimY, crystDimZ,
												   crystPixPerMic, angleP, angleL, containerInfoDict, absCoefCalc)

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
		self.seqFile 		= sequenceFile

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
		if not isinstance(self.seqFile, basestring):
			ErrorMessage += 'Sequence file input {} not of compatible format.\n'.format(str(self.seqFile))

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
