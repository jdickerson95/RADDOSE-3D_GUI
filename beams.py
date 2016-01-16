from checks import checks
import datetime
import time

class beams(object):
	# this class is for beam parameters for a loaded or created beam
	def __init__(self,beamName="",beamFlux=0,beamEnergy=0):

		self.beamName     	= beamName
		self.flux         	= beamFlux
		self.energy       	= beamEnergy

		self.__creationTime =  self.getCreationTime()

	def getTimeStampedName(self):
		# create a string containing name then timestamp for unique beam identification
		timeStampedName =  self.__creationTime + " "*10 + self.beamName
		return timeStampedName

	def getCreationTime(self):
		# get time of creation of current beam object
		ts = time.time()
		creationTime = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
		return creationTime

	def __eq__(self, other) :
		"""This method checks to see if a beam has the same properties as
		another beam
		"""
		return self.__dict__ == other.__dict__

	def __eqDiffName__(self, other) :
		"""This method checks to see if a beam has the same properties as
		another beam
		"""
		compareProps_self = {attr: getattr(self, attr) for attr in vars(self) if attr not in ('beamName','_beams__creationTime')}
		compareProps_other = {attr: getattr(other, attr) for attr in vars(other) if attr not in ('beamName','_beams__creationTime')}

		return compareProps_self == compareProps_other

	def checkValidInputs(self):
		ErrorMessage = ""
		# check that beam energy can be converted to non-negative float format (from string format)
		ErrorMessage += checks(self.energy,'beam energy',False).checkIfNonNegFloat()

		# check that beam flux can be converted to float format (from string format)
		ErrorMessage += checks(self.flux,'beam flux',False).checkIfNonNegFloat()

		return ErrorMessage

	def writeRD3DBeamBlock(self):
		"""Write a text block of beam information for RADDOSE-3D

		Function to write a text block of the beam properties for a
		RADDOSE-3D input file.

		"""
		beamLines = [] # Inialise empty list
		beamLines.append("Beam") # Append the string - "Beam" - to the list
		beamPropertyDict = vars(self) # create a dictionary from the beam object properties and corresponding values

		# loop through each entry in the dictionary, create a string of the key
		# and value from the dictionary and append that to the list created above
		for beamProp in beamPropertyDict:
			if '_beams__' in beamProp:
				continue
			if (beamProp != 'fwhm' and beamProp != 'collimation' and beamProp != 'pixelSize' and beamProp != 'beamName' and beamProp != 'file'):
				string = '{} {}'.format(beamProp[0].upper()+beamProp[1:],str(beamPropertyDict[beamProp]))
				beamLines.append(string)
			if beamProp == 'fwhm':
				string = 'FWHM {} {}'.format(self.fwhm[0], self.fwhm[1])
				beamLines.append(string)
			if beamProp == 'collimation':
				string = 'Collimation Rectangular {} {}'.format(self.collimation[0], self.collimation[1])
				beamLines.append(string)
			if beamProp == 'pixelSize':
				string = 'PixelSize {} {}'.format(self.pixelSize[0], self.pixelSize[1])
				beamLines.append(string)
			if beamProp == 'file':
				string = 'File {}'.format(self.file.split("/")[-1])
				beamLines.append(string)

		# write list entries as a single text block with each list entry joined
		# by a new line character
		beamBlock = "\n".join(beamLines)

		return beamBlock #return the beam block

class beams_Tophat(beams):
	# subclass for TopHat type beams
	def __init__(self,beamName="",beamFlux=0,beamEnergy=0,beamRectColl=[]):

		super(beams_Tophat, self).__init__(beamName,beamFlux,beamEnergy)

		self.collimation  	= beamRectColl
		self.type         	= 'TopHat'

	def extractBeamInfo(self):
		# create a string containing information of current beam
		infoString = "Beam Name: {}\n".format(str(self.beamName))
		infoString += "Beam Type: {}\n".format(str(self.type))
		infoString += "Beam Flux: {} photons per second\n".format(str(self.flux))
		infoString += "Beam Energy: {} keV\n".format(str(self.energy))
		infoString += "Beam Rectangular Collimation: {} microns x {} microns\n".format(str(self.collimation[0]),str(self.collimation[1]))
		return infoString


	def checkValidInputs_subclass(self):
		ErrorMessage = ""

		if len(self.collimation) != 2:
			ErrorMessage += 'Rectangular collimation requires two inputs (horizontal and vertical).\n'
		else:
			# check that beam collimation can be converted to non-negative float format (from string format)
			ErrorMessage += checks(self.collimation[0],'horizontal (x) collimation',False).checkIfNonNegFloat()
			ErrorMessage += checks(self.collimation[1],'vertical (y) collimation',False).checkIfNonNegFloat()

		return ErrorMessage

class beams_Gaussian(beams):
	# subclass for Gaussian type beams
	def __init__(self,beamName="",beamFWHM=[0,0],
				 beamFlux=0,beamEnergy=0,beamRectColl=[]):

		super(beams_Gaussian, self).__init__(beamName,beamFlux,beamEnergy)

		self.type         	= 'Gaussian'
		self.fwhm         	= beamFWHM
		self.collimation  	= beamRectColl

	def extractBeamInfo(self):
		# create a string containing information of current beam
		infoString = "Beam Name: {}\n".format(str(self.beamName))
		infoString += "Beam Type: {}\n".format(str(self.type))
		infoString += "Beam Flux: {} photons per second\n".format(str(self.flux))
		infoString += "Beam Energy: {} keV\n".format(str(self.energy))
		infoString += "Beam FWHM: {} microns x {} microns\n".format(str(self.fwhm[0]),str(self.fwhm[1]))
		infoString += "Beam Rectangular Collimation: {} microns x {} microns\n".format(str(self.collimation[0]),str(self.collimation[1]))
		return infoString

	def checkValidInputs_subclass(self):
		ErrorMessage = ""

		if len(self.collimation) != 2:
			ErrorMessage += 'Rectangular collimation requires two inputs (horizontal and vertical).\n'
		else:
			# check that beam collimation can be converted to non-negative float format (from string format)
			ErrorMessage += checks(self.collimation[0],'horizontal (x) collimation',False).checkIfNonNegFloat()
			ErrorMessage += checks(self.collimation[1],'vertical (y) collimation',False).checkIfNonNegFloat()

		if len(self.fwhm) != 2:
			ErrorMessage += 'FWHM requires two inputs (vertical and horizontal).\n'
		else:
			# check that beam FWHM can be converted to non-negative float format (from string format)
			ErrorMessage += checks(self.fwhm[0],'vertical (X) FWHM',False).checkIfNonNegFloat()
			ErrorMessage += checks(self.fwhm[1],'horizontal (Y) FWHM',False).checkIfNonNegFloat()

		return ErrorMessage

class beams_Experimental(beams):
	# subclass for Experimental type beams
	def __init__(self,beamName="",beamFlux=0,beamEnergy=0, beamPixelSize=[0,0],fileName=""):

		super(beams_Experimental, self).__init__(beamName,beamFlux,beamEnergy)

		self.type         	= 'ExperimentalPGM'
		self.pixelSize		= beamPixelSize
		self.file  		    = fileName

	def extractBeamInfo(self):
		# create a string containing information of current beam
		infoString = "Beam Name: {}\n".format(str(self.beamName))
		infoString += "Beam Type: {}\n".format(str(self.type))
		infoString += "Beam Flux: {} photons per second\n".format(str(self.flux))
		infoString += "Beam Energy: {} keV\n".format(str(self.energy))
		infoString += "Beam File Name: {}\n".format(str(self.file))
		infoString += "Beam Pixel Size: x = {} microns, y = {} microns\n".format(str(self.pixelSize[0]),str(self.pixelSize[1]))
		return infoString

	def checkValidInputs_subclass(self):
		ErrorMessage = ""

		if len(self.pixelSize) != 2:
			ErrorMessage += 'Pixel size requires two inputs (horizontal and vertical).\n'
		else:
			# check that beam pixelSize can be converted to non-negative float format (from string format)
			ErrorMessage += checks(self.pixelSize[0],'horizontal (x) pixel size',False).checkIfNonNegFloat()
			ErrorMessage += checks(self.pixelSize[1],'vertical (y) pixel size',False).checkIfNonNegFloat()

		# check that beam file name has been entered correctly
		ErrorMessage += checks(self.file,'Beam file',False).checkIfNonBlankString()

		return ErrorMessage


