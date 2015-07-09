class checks(object):
	# this class is for checking input values
	def __init__(self,property=[],propertyName="",optional=False):

		self.property     	= property
		self.propertyName   = propertyName
		self.optional		= optional

	def ignoreIfBlankAndOptional(self,ErrorMessage):
		# if an input is optional and left blank, this check rewrites that particular checks
		# error message to blank
		if (self.optional == True and len(self.property) == 0):
				return ""
		else:
			return ErrorMessage

	def checkHeavyAtomFormat(self):
		# this check is for heavy atoms in protein and solvent. It combines the below checks to
		# check that string contains an even number of terms, and that every second term can
		# be converted to a float
		ErrorMessage = self.checkIfEvenNumTerms()
		ErrorMessage += self.checkIfEverySecondTermFloat()

		# check whether left blank & optional
		ErrorMessage = self.ignoreIfBlankAndOptional(ErrorMessage)
		return ErrorMessage

	def checkIfEverySecondTermFloat(self):
		ErrorMessage = ""
		# check if every second element in list is non-negative float
		for value in self.property.split()[1::2]:
			Error = self.checkIfNonNegFloat()
			if len(Error) != 0:
				ErrorMessage += 'Every second term in {} field not of compatible non-negative float format.\n'.format(self.propertyName)

		# check whether left blank & optional
		ErrorMessage = self.ignoreIfBlankAndOptional(ErrorMessage)
		return ErrorMessage

	def checkIfEvenNumTerms(self):
		ErrorMessage = ""
		if len(self.property.split()) % 2 != 0:
			ErrorMessage = '{} input requires even number of terms.\n'.format(self.propertyName)

		# check whether left blank & optional
		ErrorMessage = self.ignoreIfBlankAndOptional(ErrorMessage)
		return ErrorMessage

	def checkIfNonNegFloat(self):
		# check if string can be converted to a float, and the float is non-negative
		ErrorMessage = self.checkIfFloat()
		ErrorMessage += self.checkIfPositive()

		# check whether left blank & optional
		ErrorMessage = self.ignoreIfBlankAndOptional(ErrorMessage)
		return ErrorMessage

	def checkIfNonNegInt(self):
		# check if string can be converted to a integer, and the integer is non-negative
		ErrorMessage = self.checkIfInt()
		ErrorMessage += self.checkIfPositive()

		# check whether left blank & optional
		ErrorMessage = self.ignoreIfBlankAndOptional(ErrorMessage)
		return ErrorMessage

	def checkIfInt(self):
		ErrorMessage = ""
		if not isinstance( self.property, ( int, long ) ):
			ErrorMessage = '{} not of compatible integer format.\n'.format(self.propertyName)

		# check whether left blank & optional
		ErrorMessage = self.ignoreIfBlankAndOptional(ErrorMessage)
		return ErrorMessage

	def checkIfFloat(self):
		ErrorMessage = ""
		try:
			float(self.property)
		except ValueError:
			ErrorMessage = '{} not of compatible float format.\n'.format(self.propertyName)

		# check whether left blank & optional
		ErrorMessage = self.ignoreIfBlankAndOptional(ErrorMessage)
		return ErrorMessage

	def checkIfPositive(self):
		ErrorMessage = ""
		try:
			if float(self.property) < 0:
				ErrorMessage = '{} must be non negative.\n'.format(self.propertyName)
		except ValueError:
			pass

		# check whether left blank & optional
		ErrorMessage = self.ignoreIfBlankAndOptional(ErrorMessage)
		return ErrorMessage

	def checkIfFloatBetween01(self):
		# this specific check determines whether string can be converted to
		# a float which is between 0 and 1
		ErrorMessage = ""
		try:
			float(self.property)
			if (0 > float(self.property) or 1 < float(self.property)):
				ErrorMessage += '{} must be between 0 and 1.\n'.format(self.propertyName)
		except ValueError:
			ErrorMessage += '{} not of compatible float format.\n'.format(self.propertyName)

		# check whether left blank & optional
		ErrorMessage = self.ignoreIfBlankAndOptional(ErrorMessage)
		return ErrorMessage

	def checkIfNonBlankString(self):
		# this check is to determine whether an input was actually entered within a field
		ErrorMessage = ""
		if len(self.property) == 0:
			ErrorMessage = '{} input is blank.\n'.format(self.propertyName)

		# check whether left blank & optional
		ErrorMessage = self.ignoreIfBlankAndOptional(ErrorMessage)
		return ErrorMessage
