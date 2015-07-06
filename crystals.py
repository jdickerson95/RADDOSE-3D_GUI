import os

class crystals(object):
	# this class is for crystal parameters for a loaded or created crystal.
	# Default absCoefCalc is set to 'Average'
	def __init__(self,crystName="",crystType="",crystDimX=0,crystDimY=0,
				 crystDimZ=0,crystPixPerMic=0,angleP=0,angleL=0,containerInfoDict={}):
		self.crystName        = crystName
		self.type             = crystType
		self.crystDimX        = crystDimX
		self.crystDimY        = crystDimY
		self.crystDimZ        = crystDimZ
		self.pixelsPerMicron  = crystPixPerMic
		self.angleP 		  = angleP
		self.angleL 		  = angleL
		self.absCoeffCalc 	  = 'Average'

		try:
			materialMixture,materialElements,containerThickness,containerDensity = self.getContainerInfo(containerInfoDict)
			self.materialMixture  = materialMixture
			self.materialElements = materialElements
			self.containerThickness = containerThickness
			self.containerDensity = containerDensity
		except KeyError:
			pass

	def getContainerInfo(self,containerInfoDict):
		# get info regarding crystal container
		materialMixture = containerInfoDict["Mixture"]
		materialElements = containerInfoDict["Elements"]
		containerThickness = containerInfoDict["Thickness"]
		containerDensity = containerInfoDict["Density"]
		return (materialMixture,materialElements,containerThickness,containerDensity)

	def checkValidInputs(self):
		ErrorMessage = ""
		# check valid crystal type
		if self.type not in ('Cuboid','Spherical','Cylindrical','Polyhedron'):
			ErrorMessage = ErrorMessage +  'Crystal type %s not of compatible format.\n' %(self.type)

		# check that crystal dimensions can be converted to float format (from string format)
		try:
			float(self.crystDimX)
			float(self.crystDimY)
			float(self.crystDimZ)
		except ValueError:
			ErrorMessage = ErrorMessage + 'Crystal dimensions not of compatible float format.\n'

		# check that crystal pixelsPerMicron can be converted to float format (from string format)
		try:
			float(self.pixelsPerMicron)
		except ValueError:
			ErrorMessage = ErrorMessage + 'Crystal pixelsPerMicron input not of compatible float format.\n'

		# check that crystal angle P and angle L can be converted to float format (from string format)
		try:
			float(self.angleP)
			float(self.angleL)
		except ValueError:
			ErrorMessage = ErrorMessage + 'Crystal angle L or angle P input not of compatible float format.\n'

		return ErrorMessage

	def extractCrystalInfo(self):
		# create a string containing information of current crystal
		string = """Crystal Name: %s\nType: %s\nDimensions: %s %s %s (microns in x,y,z)\nPixels per Micron: %s\nAngle P: %s\nAngle L: %s\n
""" %(str(self.crystName),str(self.type),
		          		str(self.crystDimX),str(self.crystDimY),
		          		str(self.crystDimZ),str(self.pixelsPerMicron),
		          		str(self.angleP),str(self.angleL))
		return string

class crystals_pdbCode(crystals):
	# A subclass for a single pdb file structure
	def __init__(self,crystName="",crystType="",crystDimX=0,crystDimY=0,
				 crystDimZ=0,crystPixPerMic=0,angleP=0,angleL=0,containerInfoDict={},
				 pdbcode="",solventHeavyConc=""):
		super(crystals_pdbCode, self).__init__(
					crystName,crystType,crystDimX,crystDimY,
					crystDimZ,crystPixPerMic,angleP,angleL)

		self.pdbcode = pdbcode
		self.solventHeavyConc = solventHeavyConc
		self.absCoeffCalc = 'EXP'

	def checkValidInputs_subclass(self):
		ErrorMessage = ""
		# check valid pdb code input
		if len(self.pdbcode) != 4:
			ErrorMessage = ErrorMessage +  'PDB code input %s not of compatible format.\n' %(self.pdbcode)
		return ErrorMessage

class crystals_userDefined(crystals):
	# A subclass for a user defined crystal composition
	def __init__(self,crystName="",crystType="",crystDimX=0,crystDimY=0,
			     crystDimZ=0,crystPixPerMic=0,angleP=0,angleL=0,containerInfoDict={},
				 unitcell_a=0,unitcell_b=0,unitcell_c=0,
				 unitcell_alpha=0,unitcell_beta=0,unitcell_gamma=0,
				 numMonomers=0,numResidues=0,numRNA=0,numDNA=0,
				 proteinHeavyAtoms="",solventHeavyConc="",
				 solventFraction=0):
		super(crystals_userDefined, self).__init__(
					crystName,crystType,crystDimX,crystDimY,
					crystDimZ,crystPixPerMic,angleP,angleL,containerInfoDict)

		self.unitcell_a = unitcell_a
		self.unitcell_b = unitcell_b
		self.unitcell_c = unitcell_c
		self.unitcell_alpha = unitcell_alpha
		self.unitcell_beta = unitcell_beta
		self.unitcell_gamma = unitcell_gamma
		self.numMonomers =  numMonomers
		self.numResidues = numResidues
		self.numRNA = numRNA
		self.numDNA = numDNA
		self.proteinHeavyAtoms = proteinHeavyAtoms
		self.solventHeavyConc = solventHeavyConc
		self.solventFraction = solventFraction
		self.absCoeffCalc = 'RDV3'

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
			ErrorMessage = ErrorMessage + 'Crystal numMonomers input not of compatible float format.\n'

		try:
			float(self.numResidues)
		except ValueError:
			ErrorMessage = ErrorMessage + 'Crystal numResidues input not of compatible float format.\n'

		try:
			float(self.numRNA)
		except ValueError:
			ErrorMessage = ErrorMessage + 'Crystal numRNA input not of compatible float format.\n'

		try:
			float(self.numDNA)
		except ValueError:
			ErrorMessage = ErrorMessage + 'Crystal numDNA input not of compatible float format.\n'

		try:
			float(self.solventFraction)
		except ValueError:
			ErrorMessage = ErrorMessage + 'Crystal solventFraction input not of compatible float format.\n'

		return ErrorMessage


class crystals_RADDOSEv2(crystals):
	# A subclass for RADDOSE-v2 crystal inputs
	def __init__(self,crystName="",crystType="",crystDimX=0,crystDimY=0,
				 crystDimZ=0,crystPixPerMic=0,angleP=0,angleL=0,containerInfoDict={},
				 unitcell_a=0,unitcell_b=0,unitcell_c=0,
				 unitcell_alpha=0,unitcell_beta=0,unitcell_gamma=0,
				 numMonomers=0,numResidues=0,numRNA=0,numDNA=0,
				 proteinHeavyAtoms="",solventHeavyConc="",
				 solventFraction=0):
		super(crystals_RADDOSEv2, self).__init__(
					crystName,crystType,crystDimX,crystDimY,
					crystDimZ,crystPixPerMic,angleP,angleL,containerInfoDict)

		self.unitcell_a = unitcell_a
		self.unitcell_b = unitcell_b
		self.unitcell_c = unitcell_c
		self.unitcell_alpha = unitcell_alpha
		self.unitcell_beta = unitcell_beta
		self.unitcell_gamma = unitcell_gamma
		self.numMonomers =  numMonomers
		self.numResidues = numResidues
		self.numRNA = numRNA
		self.numDNA = numDNA
		self.proteinHeavyAtoms = proteinHeavyAtoms
		self.solventHeavyConc = solventHeavyConc
		self.solventFraction = solventFraction
		self.absCoeffCalc = 'RDV2'

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
			ErrorMessage = ErrorMessage + 'Crystal numMonomers input not of compatible float format.\n'

		try:
			float(self.numResidues)
		except ValueError:
			ErrorMessage = ErrorMessage + 'Crystal numResidues input not of compatible float format.\n'

		try:
			float(self.numRNA)
		except ValueError:
			ErrorMessage = ErrorMessage + 'Crystal numRNA input not of compatible float format.\n'

		try:
			float(self.numDNA)
		except ValueError:
			ErrorMessage = ErrorMessage + 'Crystal numDNA input not of compatible float format.\n'

		try:
			float(self.solventFraction)
		except ValueError:
			ErrorMessage = ErrorMessage + 'Crystal solventFraction input not of compatible float format.\n'

		return ErrorMessage

class crystals_seqFile(crystals):
	# A subclass for sequence file-defined crystal composition
	def __init__(self,crystName="",crystType="",crystDimX=0,crystDimY=0,
				 crystDimZ=0,crystPixPerMic=0,angleP=0,angleL=0,containerInfoDict={},
				 unitcell_a=0,unitcell_b=0,unitcell_c=0,
				 unitcell_alpha=0,unitcell_beta=0,unitcell_gamma=0,
				 numMonomers=0,sequenceFile="",proteinHeavyAtoms="",
				 solventHeavyConc="",solventFraction=0):
		super(crystals_seqFile, self).__init__(
					crystName,crystType,crystDimX,crystDimY,
					crystDimZ,crystPixPerMic,angleP,angleL,containerInfoDict)

		self.unitcell_a = unitcell_a
		self.unitcell_b = unitcell_b
		self.unitcell_c = unitcell_c
		self.unitcell_alpha = unitcell_alpha
		self.unitcell_beta = unitcell_beta
		self.unitcell_gamma = unitcell_gamma
		self.numMonomers =  numMonomers
		self.proteinHeavyAtoms = proteinHeavyAtoms
		self.solventHeavyConc = solventHeavyConc
		self.solventFraction = solventFraction
		self.absCoeffCalc = 'RDV3'


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
			ErrorMessage = ErrorMessage + 'Crystal numMonomers input not of compatible float format.\n'

		try:
			float(self.solventFraction)
		except ValueError:
			ErrorMessage = ErrorMessage + 'Crystal solventFraction input not of compatible float format.\n'

		return ErrorMessage

class crystals_SAXSuserDefined(crystals):
	# A subclass for user-defined SAXS crystal composition inputs
	def __init__(self,crystName="",crystType="",crystDimX=0,crystDimY=0,
				 crystDimZ=0,crystPixPerMic=0,angleP=0,angleL=0,containerInfoDict={},
				 unitcell_a=0,unitcell_b=0,unitcell_c=0,
				 unitcell_alpha=0,unitcell_beta=0,unitcell_gamma=0,
				 numResidues=0,numRNA=0,numDNA=0,
				 proteinHeavyAtoms="",solventHeavyConc="",
				 solventFraction=0,proteinConc=0):
		super(crystals_SAXSuserDefined, self).__init__(
					crystName,crystType,crystDimX,crystDimY,
					crystDimZ,crystPixPerMic,angleP,angleL,containerInfoDict)

		self.unitcell_a = unitcell_a
		self.unitcell_b = unitcell_b
		self.unitcell_c = unitcell_c
		self.unitcell_alpha = unitcell_alpha
		self.unitcell_beta = unitcell_beta
		self.unitcell_gamma = unitcell_gamma
		self.numResidues = numResidues
		self.numRNA = numRNA
		self.numDNA = numDNA
		self.proteinHeavyAtoms = proteinHeavyAtoms
		self.solventHeavyConc = solventHeavyConc
		self.solventFraction = solventFraction
		self.proteinConc = proteinConc
		self.absCoeffCalc = 'RDV3'

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
			float(self.numResidues)
		except ValueError:
			ErrorMessage = ErrorMessage + 'Crystal numResidues input not of compatible float format.\n'

		try:
			float(self.numRNA)
		except ValueError:
			ErrorMessage = ErrorMessage + 'Crystal numRNA input not of compatible float format.\n'

		try:
			float(self.numDNA)
		except ValueError:
			ErrorMessage = ErrorMessage + 'Crystal numDNA input not of compatible float format.\n'

		try:
			float(self.solventFraction)
		except ValueError:
			ErrorMessage = ErrorMessage + 'Crystal solventFraction input not of compatible float format.\n'

		return ErrorMessage

class crystals_SAXSseqFile(crystals):
	# A subclass for sequence file-defined SAXS crystal composition inputs
	def __init__(self,crystName="",crystType="",crystDimX=0,crystDimY=0,
				 crystDimZ=0,crystPixPerMic=0,angleP=0,angleL=0,containerInfoDict={},
				 unitcell_a=0,unitcell_b=0,unitcell_c=0,
				 unitcell_alpha=0,unitcell_beta=0,unitcell_gamma=0,
				 proteinHeavyAtoms="",solventHeavyConc="",
				 solventFraction=0,proteinConc=0,sequenceFile=""):
		super(crystals_SAXSseqFile, self).__init__(
					crystName,crystType,crystDimX,crystDimY,
					crystDimZ,crystPixPerMic,angleP,angleL,containerInfoDict)

		self.unitcell_a = unitcell_a
		self.unitcell_b = unitcell_b
		self.unitcell_c = unitcell_c
		self.unitcell_alpha = unitcell_alpha
		self.unitcell_beta = unitcell_beta
		self.unitcell_gamma = unitcell_gamma
		self.proteinHeavyAtoms = proteinHeavyAtoms
		self.solventHeavyConc = solventHeavyConc
		self.solventFraction = solventFraction
		self.proteinConc = proteinConc
		self.sequenceFile = sequenceFile
		self.absCoeffCalc = 'RDV3'

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
			float(self.solventFraction)
		except ValueError:
			ErrorMessage = ErrorMessage + 'Crystal solventFraction input not of compatible float format.\n'

		# check sequence file input is string
		if not isinstance(self.sequenceFile, basestring):
			ErrorMessage = ErrorMessage +  'Sequence file input %s not of compatible format.\n' %(self.sequenceFile)

		return ErrorMessage