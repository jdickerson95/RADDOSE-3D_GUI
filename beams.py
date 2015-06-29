class beams(object):
	# this class is for beam parameters for a loaded or created beam
	def __init__(self,beamName="",beamType="",beamFWHM=[0,0],
				 beamFlux=0,beamEnergy=0,beamRectColl=[], beamPixelSize=[0,0]):
		self.beamName     	= beamName
		self.type         	= beamType
		self.fwhm         	= beamFWHM
		self.flux         	= beamFlux
		self.energy       	= beamEnergy
		self.collimation  	= beamRectColl
		self.pixelSize		= beamPixelSize

	def __eq__(self, other) :
		"""This method checks to see if a beam has the same properties as
		another beam
		"""
		return self.__dict__ == other.__dict__