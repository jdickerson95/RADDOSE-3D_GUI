class crystals(object):
	# this class is for crystal parameters for a loaded or created crystal
	def __init__(self,crystName="",crystType="",crystDimX=0,crystDimY=0,
				 crystDimZ=0,crystPixPerMic=0,crystAbsorpCoeff=""):
		self.crystName        = crystName
		self.type             = crystType
		self.crystDimX        = crystDimX
		self.crystDimY        = crystDimY
		self.crystDimZ        = crystDimZ
		self.pixelsPerMicron  = crystPixPerMic
		self.absCoefCalc      = crystAbsorpCoeff

class crystals_pdbCode(crystals):
	# A subclass for a single pdb file structure
	def __init__(self,crystName="",crystType="",crystDimX=0,crystDimY=0,
				 crystDimZ=0,crystPixPerMic=0,crystAbsorpCoeff="",
				 pdbcode="",solventHeavyConc=""):
		super(crystals_AverageAbsCoeffCals, self).__init__(
					crystName,crystType,crystDimX,crystDimY,
					crystDimZ,crystPixPerMic,crystAbsorpCoeff)

		self.pdbcode = pdbcode
		self.solventHeavyConc = solventHeavyConc

class crystals_userDefined(crystals):
	# A subclass for a user defined crystal composition
	def __init__(self,crystName="",crystType="",crystDimX=0,crystDimY=0,
			     crystDimZ=0,crystPixPerMic=0,crystAbsorpCoeff="",
				 unitcell_a=0,unitcell_b=0,unitcell_c=0,
				 unitcell_alpha=0,unitcell_beta=0,unitcell_gamma=0,
				 numMonomers=0,numResidues=0,numRNA=0,numDNA=0,
				 proteinHeavyAtoms="",solventHeavyConc="",
				 solventFraction=0):
		super(crystals_AverageAbsCoeffCals, self).__init__(
					crystName,crystType,crystDimX,crystDimY,
					crystDimZ,crystPixPerMic,crystAbsorpCoeff)

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

class crystals_RADDOSEv2(crystals):
	# A subclass for RADDOSE-v2 crystal inputs
	def __init__(self,crystName="",crystType="",crystDimX=0,crystDimY=0,
				 crystDimZ=0,crystPixPerMic=0,crystAbsorpCoeff="",
				 unitcell_a=0,unitcell_b=0,unitcell_c=0,
				 unitcell_alpha=0,unitcell_beta=0,unitcell_gamma=0,
				 numMonomers=0,numResidues=0,numRNA=0,numDNA=0,
				 proteinHeavyAtoms="",solventHeavyConc="",
				 solventFraction=0):
		super(crystals_AverageAbsCoeffCals, self).__init__(
					crystName,crystType,crystDimX,crystDimY,
					crystDimZ,crystPixPerMic,crystAbsorpCoeff)

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

class crystals_seqFile(crystals):
	# A subclass for sequence file-defined crystal composition
	def __init__(self,crystName="",crystType="",crystDimX=0,crystDimY=0,
				 crystDimZ=0,crystPixPerMic=0,crystAbsorpCoeff="",
				 unitcell_a=0,unitcell_b=0,unitcell_c=0,
				 unitcell_alpha=0,unitcell_beta=0,unitcell_gamma=0,
				 numMonomers=0,sequenceFile="",cproteinHeavyAtoms="",
				 solventHeavyConc="",solventFraction=0):
		super(crystals_AverageAbsCoeffCals, self).__init__(
					crystName,crystType,crystDimX,crystDimY,
					crystDimZ,crystPixPerMic,crystAbsorpCoeff)

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

class crystals_SAXSuserDefined(crystals):
	# A subclass for user-defined SAXS crystal composition inputs
	def __init__(self,crystName="",crystType="",crystDimX=0,crystDimY=0,
				 crystDimZ=0,crystPixPerMic=0,crystAbsorpCoeff="",
				 unitcell_a=0,unitcell_b=0,unitcell_c=0,
				 unitcell_alpha=0,unitcell_beta=0,unitcell_gamma=0,
				 numResidues=0,numRNA=0,numDNA=0,
				 proteinHeavyAtoms="",solventHeavyConc="",
				 solventFraction=0,proteinConc=0):
		super(crystals_AverageAbsCoeffCals, self).__init__(
					crystName,crystType,crystDimX,crystDimY,
					crystDimZ,crystPixPerMic,crystAbsorpCoeff)

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

class crystals_SAXSseqFile(crystals):
	# A subclass for sequence file-defined SAXS crystal composition inputs
	def __init__(self,crystName="",crystType="",crystDimX=0,crystDimY=0,
				 crystDimZ=0,crystPixPerMic=0,crystAbsorpCoeff="",
				 unitcell_a=0,unitcell_b=0,unitcell_c=0,
				 unitcell_alpha=0,unitcell_beta=0,unitcell_gamma=0,
				 proteinHeavyAtoms="",solventHeavyConc="",
				 solventFraction=0,proteinConc=0,sequenceFile=""):
		super(crystals_AverageAbsCoeffCals, self).__init__(
					crystName,crystType,crystDimX,crystDimY,
					crystDimZ,crystPixPerMic,crystAbsorpCoeff)

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