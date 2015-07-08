class wedges(object):
	# this class is for wedge parameters for a loaded or created wedge
	def __init__(self,angStart="",angStop="",exposTime="",angRes=0,
				startOffset=[],transPerDeg=[],rotAxBeamOffset=0):
		self.angStart     = angStart
		self.angStop      = angStop
		self.exposureTime = exposTime
		self.angRes = angRes
		self.startOffset = startOffset
		self.transPerDeg = transPerDeg
		self.rotAxBeamOffset = rotAxBeamOffset

	