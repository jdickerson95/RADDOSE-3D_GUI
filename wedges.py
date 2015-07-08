class wedges(object):
	# this class is for wedge parameters for a loaded or created wedge
	def __init__(self,angStart="",angStop="",exposTime="",angRes=2,
				startOffset=[],transPerDeg=[],rotAxBeamOffset=0):
		self.angStart     = angStart
		self.angStop      = angStop
		self.exposureTime = exposTime
		self.angRes = angRes
		self.startOffset = startOffset
		self.transPerDeg = transPerDeg
		self.rotAxBeamOffset = rotAxBeamOffset

	def checkValidInputs(self):
		ErrorMessage = ""

		# check that wedge angular start & stop can be converted to float format (from string format)
		ErrorMessage = self.checkIfFloat(self.angStart,'angular start',ErrorMessage)
		ErrorMessage = self.checkIfFloat(self.angStop,'angular stop',ErrorMessage)

		# check that wedge angular start < stop
		try:
			if float(self.angStart) > float(self.angStop):
				ErrorMessage += 'Wedge angular start greater than stop value.\n'
		except ValueError:
			pass

		# check that wedge exposure time can be converted to float format (from string format), and is positive
		ErrorMessage = self.checkIfFloat(self.exposureTime,'exposure time',ErrorMessage)
		ErrorMessage = self.checkIfPositive(self.exposureTime,'exposure time',ErrorMessage)

		# check that wedge angular resolution can be converted to float format (from string format), and is positive
		ErrorMessage = self.checkIfFloat(self.angRes,'angular resolution',ErrorMessage)
		ErrorMessage = self.checkIfPositive(self.angRes,'angular resolution',ErrorMessage)

		# check that start offset values can be converted to float format (from string format)
		ErrorMessage = self.checkIfFloat(self.startOffset[0],'start x off set',ErrorMessage)
		ErrorMessage = self.checkIfFloat(self.startOffset[1],'start y off set',ErrorMessage)
		ErrorMessage = self.checkIfFloat(self.startOffset[2],'start z off set',ErrorMessage)

		# check that translation per degree can be converted to float format (from string format)
		ErrorMessage = self.checkIfFloat(self.transPerDeg[0],'x translation per degree',ErrorMessage)
		ErrorMessage = self.checkIfFloat(self.transPerDeg[1],'y translation per degree',ErrorMessage)
		ErrorMessage = self.checkIfFloat(self.transPerDeg[2],'z translation per degree',ErrorMessage)

		# check that rotation offset can be converted to float format (from string format)
		ErrorMessage = self.checkIfFloat(self.rotAxBeamOffset,'rotation offset',ErrorMessage)

		return ErrorMessage

	def checkIfFloat(self,property,propertyName,ErrorMessage):
		try:
			float(property)
		except ValueError:
			ErrorMessage += 'Wedge {} not of compatible float format.\n'.format(propertyName)
		return ErrorMessage

	def checkIfPositive(self,property,propertyName,ErrorMessage):
		try:
			if float(property) < 0:
				ErrorMessage += 'Wedge {} must be non negative.\n'.format(propertyName)
		except ValueError:
			pass
		return ErrorMessage

	def getWedgeInfo(self):
		# create a string containing summary information for current string
		infoString = "Wedge angular start/stop: {}/{}\n".format(str(self.angStart),str(self.angStop))
		infoString += "Wedge exposure time: {}\n".format(str(self.exposureTime))
		infoString += "Wedge angular resolution: {}\n".format(str(self.angRes))
		try:
			infoString += "Wedge start offset: {} {} {}\n".format(str(self.startOffset[0]),str(self.startOffset[1]),str(self.startOffset[2]))
		except IndexError:
			pass
		try:
			infoString += "Wedge translation per degree: {} {} {}\n".format(str(self.transPerDeg[0]),str(self.transPerDeg[1]),str(self.transPerDeg[2]))
		except IndexError:
			pass
		infoString += "Wedge rotation axis beam offset: {}\n".format(str(self.rotAxBeamOffset))

		return infoString






