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

	def writeRD3DWedgeBlock(self):
		"""Write a text block of wedge information for RADDOSE-3D

		Function to write a text block of the wedge properties for a
		RADDOSE-3D input file.

		"""
		wedgeLines = [] # Inialise empty list
		# Ensure the Wedge line is written first into the RADDOSE-3D input file.
		wedgeString = "Wedge {} {}".format(self.angStart, self.angStop)
		wedgeLines.append(wedgeString)

		wedgePropertyDict = vars(self) # create a dictionary from the wedge object properties and corresponding values

		# Add a dictionary entries for the wedge object inputs that are in list format.
		wedgePropertyDict["StartOffset"] = '{} {} {}'.format(self.startOffsetList[0], self.startOffsetList[1], self.startOffsetList[2])
		wedgePropertyDict["TranslatePerDegree"] = '{} {} {}'.format(self.transPerDegList[0], self.transPerDegList[1], self.transPerDegList[2])

		# loop through each entry in the dictionary, create a string of the key
		# and value from the dictionary and append that to the list created above
		for wedgeProp in wedgePropertyDict:
			if (wedgeProp != 'angStart' and wedgeProp != 'angStop' and wedgeProp != 'startOffsetList'and
				wedgeProp != 'transPerDegList' and wedgePropertyDict[wedgeProp]):
				string = '{} {}'.format(wedgeProp,str(wedgePropertyDict[wedgeProp]))
				wedgeLines.append(string)

		# write list entries as a single text block with each list entry joined
		# by a new line character
		wedgeBlock = "\n".join(wedgeLines)
		
		return wedgeBlock
