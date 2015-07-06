class beams(object):
	# this class is for beam parameters for a loaded or created beam
	def __init__(self,beamName="",beamFlux=0,beamEnergy=0):

		self.beamName     	= beamName
		self.flux         	= beamFlux
		self.energy       	= beamEnergy

	def __eq__(self, other) :
		"""This method checks to see if a beam has the same properties as
		another beam
		"""
		return self.__dict__ == other.__dict__

	def checkValidInputs(self):
		ErrorMessage = ""
		# check that beam energy can be converted to float format (from string format)
		try:
			float(self.energy)
		except ValueError:
			ErrorMessage += 'Beam energy not of compatible float format.\n'

		# check that beam flux can be converted to float format (from string format)
		try:
			float(self.flux)
		except ValueError:
			ErrorMessage += 'Beam flux not of compatible float format.\n'

		return ErrorMessage

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
			ErrorMessage += 'Rectangular collimation inputs of invalid format.\n'
		else:
			# check that beam collimation can be converted to float format (from string format)
			try:
				float(self.collimation[0])
				float(self.collimation[1])
			except ValueError:
				ErrorMessage += 'Beam collimation not of compatible float format.\n'

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
			ErrorMessage += 'Rectangular collimation inputs of invalid format.\n'
		else:
			# check that beam collimation can be converted to float format (from string format)
			try:
				float(self.collimation[0])
				float(self.collimation[1])
			except ValueError:
				ErrorMessage += 'Beam collimation not of compatible float format.\n'

		if len(self.fwhm) != 2:
			ErrorMessage += 'FWHM inputs of invalid format.\n'
		else:
			# check that beam FWHM can be converted to float format (from string format)
			try:
				float(self.fwhm[0])
				float(self.fwhm[1])
			except ValueError:
				ErrorMessage += 'Beam FWHM not of compatible float format.\n'

		return ErrorMessage

class beams_Experimental(beams):
	# subclass for Experimental type beams
	def __init__(self,beamName="",beamFlux=0,beamEnergy=0, beamPixelSize=[0,0],fileName=""):

		super(beams_Experimental, self).__init__(beamName,beamFlux,beamEnergy)

		self.type         	= 'Experimental'
		self.pixelSize		= beamPixelSize
		self.fileName  		= fileName

	def extractBeamInfo(self):
		# create a string containing information of current beam
		infoString = "Beam Name: {}\n".format(str(self.beamName))
		infoString += "Beam Type: {}\n".format(str(self.type))
		infoString += "Beam Flux: {} photons per second\n".format(str(self.flux))
		infoString += "Beam Energy: {} keV\n".format(str(self.energy))
		infoString += "Beam File Name: {}\n".format(str(self.fileName))
		infoString += "Beam Pixel Size: x = {} microns, y = {} microns\n".format(str(self.pixelSize[0]),str(self.pixelSize[1]))
		return infoString

	def checkValidInputs_subclass(self):
		ErrorMessage = ""

		if len(self.pixelSize) != 2:
			ErrorMessage += 'Beam pixelSize inputs of invalid format.\n'
		else:
			# check that beam pixel size can be converted to float format (from string format)
			try:
				float(self.pixelSize[0])
				float(self.pixelSize[1])
			except ValueError:
				ErrorMessage += 'Beam pixelSize not of compatible float format.\n'

		return ErrorMessage


