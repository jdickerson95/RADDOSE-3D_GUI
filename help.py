class help(object):
	def __init__(self,crystAdded=False,beamAdded=False,
					  stratLoaded=False,stratRun=False,
					  advice=""):
		self.crystAdded = crystAdded
		self.beamAdded = beamAdded
		self.stratLoaded = stratLoaded
		self.stratRun = stratRun
		self.advice = advice

	def getAdvice(self):
		self.advice = ""
		# if neither crystal made or loaded into gui
		if self.crystAdded == False:
			self.advice += 'No crystal found. Please load a premade crystal file or make a crystal.\n'
			return
		elif self.crystAdded == True:
			self.advice += 'Crystal found.\n' 

		if self.beamAdded == False:
			self.advice += 'No beam found. Please load a premade beam file or make a beam.\n'
			return
		elif self.beamAdded == True:
			self.advice += 'Beam found.\n'

		if self.stratLoaded == False and self.stratRun == False:
			self.advice += 'Please create a strategy using added crystals and beams.\n'

	def checkStates(self,list,type):
		if len(list) != 0:
			if type == 'crystal':
				self.crystAdded = True
			elif type == 'beam':
				self.beamAdded = True














