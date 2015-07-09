from checks import checks

class wedges(object):
	# this class is for wedge parameters for a loaded or created wedge
	def __init__(self,angStart="",angStop="",exposTime="",angularResolution=2,
				startOffsetList=[],transPerDegList=[],rotAxBeamOffset=0):
		self.angStart     = angStart
		self.angStop      = angStop
		self.exposureTime = exposTime
		self.angularResolution = angularResolution
		self.startOffsetList = startOffsetList
		self.transPerDegList = transPerDegList
		self.rotAxBeamOffset = rotAxBeamOffset

	def checkValidInputs(self):
		ErrorMessage = ""

		# check that wedge angular start & stop can be converted to float format (from string format)
		ErrorMessage += checks(self.angStart,'wedge start',False).checkIfFloat()
		ErrorMessage += checks(self.angStop,'wedge start',False).checkIfFloat()

		# check that wedge angular start < stop
		try:
			if float(self.angStart) > float(self.angStop):
				ErrorMessage += 'Wedge angular start greater than stop value.\n'
		except ValueError:
			pass

		# check that wedge exposure time can be converted to float format (from string format), and is positive
		ErrorMessage += checks(self.exposureTime,'exposure time',False).checkIfNonNegFloat()

		# check that wedge angular resolution can be converted to float format (from string format), and is positive
		ErrorMessage += checks(self.angularResolution,'angular resolution',True).checkIfNonNegFloat()

		# check that start offset values can be converted to float format (from string format)
		ErrorMessage += checks(self.startOffsetList[0],'start x off set',True).checkIfFloat()
		ErrorMessage += checks(self.startOffsetList[1],'start y off set',True).checkIfFloat()
		ErrorMessage += checks(self.startOffsetList[2],'start z off set',True).checkIfFloat()

		# check that translation per degree can be converted to float format (from string format)
		ErrorMessage += checks(self.transPerDegList[0],'x translation per degree',True).checkIfFloat()
		ErrorMessage += checks(self.transPerDegList[1],'y translation per degree',True).checkIfFloat()
		ErrorMessage += checks(self.transPerDegList[2],'z translation per degree',True).checkIfFloat()

		# check that rotation offset can be converted to float format (from string format)
		ErrorMessage += checks(self.rotAxBeamOffset,'rotation offset',True).checkIfFloat()

		return ErrorMessage

	def getWedgeInfo(self):
		# create a string containing summary information for current string
		infoString = "Wedge angular start/stop: {}/{}\n".format(str(self.angStart),str(self.angStop))
		infoString += "Wedge exposure time: {}\n".format(str(self.exposureTime))
		infoString += "Wedge angular resolution: {}\n".format(str(self.angularResolution))
		try:
			infoString += "Wedge start offset: {} {} {}\n".format(str(self.startOffsetList[0]),str(self.startOffsetList[1]),str(self.startOffsetList[2]))
		except IndexError:
			pass
		try:
			infoString += "Wedge translation per degree: {} {} {}\n".format(str(self.transPerDegList[0]),str(self.transPerDegList[1]),str(self.transPerDegList[2]))
		except IndexError:
			pass
		infoString += "Wedge rotation axis beam offset: {}\n".format(str(self.rotAxBeamOffset))

		return infoString
