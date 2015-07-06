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

class beams_Tophat(beams):
	# subclass for TopHat type beams
	def __init__(self,beamName="",beamType="",beamFWHM=[0,0],
				 beamFlux=0,beamEnergy=0,beamRectColl=[], beamPixelSize=[0,0]):

		super(beams_Tophat, self).__init__(beamName,beamFlux,beamEnergy)

		self.type         	= 'TopHat'

class beams_Gaussian(beams):
	# subclass for Gaussian type beams
	def __init__(self,beamName="",beamType="",beamFWHM=[0,0],
				 beamFlux=0,beamEnergy=0,beamRectColl=[], beamPixelSize=[0,0]):

		super(beams_Gaussian, self).__init__(beamName,beamFlux,beamEnergy)

		self.type         	= 'Gaussian'
		self.fwhm         	= beamFWHM
		self.collimation  	= beamRectColl

class beams_Experimental(beams):
	# subclass for Experimental type beams
	def __init__(self,beamName="",beamType="",beamFWHM=[0,0],
				 beamFlux=0,beamEnergy=0,beamRectColl=[], beamPixelSize=[0,0]):

		super(beams_Experimental, self).__init__(beamName,beamFlux,beamEnergy)

		self.type         	= 'Experimental'
		self.pixelSize		= beamPixelSize
		self.fileName  		= fileName


