class help(object):
	def __init__(self,crystAdded=False,beamAdded=False,
					  stratLoaded=False,stratRun=False,
					  advice="",messageNumber=0):
		self.crystAdded = crystAdded
		self.beamAdded = beamAdded
		self.stratLoaded = stratLoaded
		self.stratRun = stratRun
		self.advice = advice
		self.messageNumber = messageNumber 

	def welcomeMessage(self):
		# this is the welcome message for when gui opened
		self.advice = """ Welcome to the RADDOSE-3D interface. 
					  Currently 2 model crystals and 2 model beams are loaded.
					  Please first create/load a new crystal or beam for your experiment.
					  Alternatively use the ready-made crystal and beams to design a strategy.
					  """

	def getAdvice(self):
		# when interface first opened, display welcome message
		if self.messageNumber == 0:
			self.welcomeMessage()
			self.updateMessageNumber()
		else:
			self.updateMessageNumber()
			self.advice = ""
			# update help advice depending on whether crystals, beams, strategies are loaded
			if self.crystAdded == False:
				self.advice += 'No crystal found. Please load a premade crystal file or make a crystal using the make-a-crystal window.\n'
				return
			elif self.crystAdded == True:
				self.advice += 'Crystal found.\n' 

			if self.beamAdded == False:
				self.advice += 'No beam found. Please load a premade beam file or make a beam using the make-a-beam window.\n'
				return
			elif self.beamAdded == True:
				self.advice += 'Beam found.\n'

			if self.stratLoaded == False:
				self.advice += 'Please create a strategy using added crystals and beams.\n'
				return
			elif self.stratLoaded == True:
				self.advice += 'A strategy has been loaded. Additional exposure strategies can be added, or the current strategy can now be run.'

	def checkStates(self,list,type):
		# inputs a list of crystal, beam or wedge objects (type = 'crystal','beam','wedge')
		# to determine whether crystals, beams or wedges have been added to interface
		if len(list) != 0:
			if type == 'crystal':
				self.crystAdded = True
			elif type == 'beam':
				self.beamAdded = True
			elif type == 'wedge':
				self.stratLoaded = True

		elif len(list) == 0:
			if type == 'crystal':
				self.crystAdded = False
			elif type == 'beam':
				self.beamAdded = False
			elif type == 'wedge':
				self.stratLoaded = False

	def updateMessageNumber(self):
		# increase message number by 1
		self.messageNumber += 1














