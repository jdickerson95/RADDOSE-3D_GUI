class crystals(object):
	# this class is for crystal parameters for a loaded or created crystal
	def __init__(self,crystName="",crystType="",crystDimX=0,crystDimY=0,
				 crystDimZ=0,crystPixPerMic=0):
		self.crystName        = crystName
		self.type             = crystType
		self.crystDimX        = crystDimX
		self.crystDimY        = crystDimY
		self.crystDimZ        = crystDimZ
		self.pixelsPerMicron  = crystPixPerMic

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

		return ErrorMessage

	def extractCrystalInfo(self):
		# create a string containing information of current crystal
		string = """Crystal Name: %s\nType: %s\nDimensions: %s %s %s (microns in x,y,z)\nPixels per Micron: %s\n
""" %(str(self.crystName),str(self.type),
		          		str(self.crystDimX),str(self.crystDimY),
		          		str(self.crystDimZ),str(self.pixelsPerMicron))
		return string

class crystals_pdbCode(crystals):
	# A subclass for a single pdb file structure
	def __init__(self,crystName="",crystType="",crystDimX=0,crystDimY=0,
				 crystDimZ=0,crystPixPerMic=0,
				 pdbcode="",solventHeavyConc=""):
		super(crystals_AverageAbsCoeffCals, self).__init__(
					crystName,crystType,crystDimX,crystDimY,
					crystDimZ,crystPixPerMic)

		self.pdbcode = pdbcode
		self.solventHeavyConc = solventHeavyConc

	def getAbsCoeffType(self):
		return 'PDB code'

	def checkValidInputs_subclass(self):
		ErrorMessage = ""
		# check valid pdb code input
		if len(self.pdbcode) != 4:
			ErrorMessage = ErrorMessage +  'PDB code input %s not of compatible format.\n' %(self.pdbcode)
		return ErrorMessage

class crystals_userDefined(crystals):
	# A subclass for a user defined crystal composition
	def __init__(self,crystName="",crystType="",crystDimX=0,crystDimY=0,
			     crystDimZ=0,crystPixPerMic=0,
				 unitcell_a=0,unitcell_b=0,unitcell_c=0,
				 unitcell_alpha=0,unitcell_beta=0,unitcell_gamma=0,
				 numMonomers=0,numResidues=0,numRNA=0,numDNA=0,
				 proteinHeavyAtoms="",solventHeavyConc="",
				 solventFraction=0):
		super(crystals_AverageAbsCoeffCals, self).__init__(
					crystName,crystType,crystDimX,crystDimY,
					crystDimZ,crystPixPerMic)

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

	def getAbsCoeffType(self):
		return 'User Defined'

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
				 crystDimZ=0,crystPixPerMic=0,
				 unitcell_a=0,unitcell_b=0,unitcell_c=0,
				 unitcell_alpha=0,unitcell_beta=0,unitcell_gamma=0,
				 numMonomers=0,numResidues=0,numRNA=0,numDNA=0,
				 proteinHeavyAtoms="",solventHeavyConc="",
				 solventFraction=0):
		super(crystals_AverageAbsCoeffCals, self).__init__(
					crystName,crystType,crystDimX,crystDimY,
					crystDimZ,crystPixPerMic)

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

	def getAbsCoeffType(self):
		return 'RADDOSE-v2'

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
				 crystDimZ=0,crystPixPerMic=0,
				 unitcell_a=0,unitcell_b=0,unitcell_c=0,
				 unitcell_alpha=0,unitcell_beta=0,unitcell_gamma=0,
				 numMonomers=0,sequenceFile="",proteinHeavyAtoms="",
				 solventHeavyConc="",solventFraction=0):
		super(crystals_AverageAbsCoeffCals, self).__init__(
					crystName,crystType,crystDimX,crystDimY,
					crystDimZ,crystPixPerMic)

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

	def getAbsCoeffType(self):
		return 'Sequence File'

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
				 crystDimZ=0,crystPixPerMic=0,
				 unitcell_a=0,unitcell_b=0,unitcell_c=0,
				 unitcell_alpha=0,unitcell_beta=0,unitcell_gamma=0,
				 numResidues=0,numRNA=0,numDNA=0,
				 proteinHeavyAtoms="",solventHeavyConc="",
				 solventFraction=0,proteinConc=0):
		super(crystals_AverageAbsCoeffCals, self).__init__(
					crystName,crystType,crystDimX,crystDimY,
					crystDimZ,crystPixPerMic)

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

	def getAbsCoeffType(self):
		return 'SAXS User Defined'

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
				 crystDimZ=0,crystPixPerMic=0,
				 unitcell_a=0,unitcell_b=0,unitcell_c=0,
				 unitcell_alpha=0,unitcell_beta=0,unitcell_gamma=0,
				 proteinHeavyAtoms="",solventHeavyConc="",
				 solventFraction=0,proteinConc=0,sequenceFile=""):
		super(crystals_AverageAbsCoeffCals, self).__init__(
					crystName,crystType,crystDimX,crystDimY,
					crystDimZ,crystPixPerMic)

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

	def getAbsCoeffType(self):
		return 'SAXS Sequence File'

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