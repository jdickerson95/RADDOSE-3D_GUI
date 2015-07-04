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
		self.advice = ('Welcome to the RADDOSE-3D interface.\n' 
					  'Currently 2 model crystals and 2 model beams are loaded.\n'
					  'Please first create/load a new crystal or beam for your experiment.\n'
					  'Alternatively use the ready-made crystal and beams to design a strategy.\n')

	def getAdvice(self):
		# when interface first opened, display welcome message
		if self.messageNumber == 0:
			self.welcomeMessage()
			self.updateMessageNumber()
		else:
			self.updateMessageNumber()
			# obtain current text for help text box
			adviceSummary,adviceBreakdown = self.createAdviceString()
			# combine the advice summary and breakdown sections to create full advice string
			self.advice = adviceSummary + '\nAdvice:\n' + adviceBreakdown

	def createAdviceString(self):
		# update help advice depending on whether crystals, beams, strategies are loaded.
		# Advice string broken into summary and breakdown sections
		adviceSummary,adviceBreakdown = "",""
		tickMark = u'\u2713\t'
		questionMark = '?\t'
		if self.crystAdded == False:
			adviceSummary += questionMark
			adviceSummary += 'No crystal found.\n' 
			adviceBreakdown += 'Please load a premade crystal file or make a crystal using the make-a-crystal window.\n'
			return (adviceSummary,adviceBreakdown)
		elif self.crystAdded == True:
			adviceSummary += tickMark
			adviceSummary += 'Crystal found.\n' 

		if self.beamAdded == False:
			adviceSummary += questionMark
			adviceSummary += 'No beam found.\n' 
			adviceBreakdown += 'Please load a premade beam file or make a beam using the make-a-beam window.\n'
			return (adviceSummary,adviceBreakdown)
		elif self.beamAdded == True:
			adviceSummary += tickMark
			adviceSummary += 'Beam found.\n'

		if self.stratLoaded == False:
			adviceSummary += questionMark
			adviceSummary += 'No strategy found.\n' 
			adviceBreakdown += 'Please create a strategy using added crystals and beams.\n'
			return (adviceSummary,adviceBreakdown)
		elif self.stratLoaded == True:
			adviceSummary += tickMark
			adviceSummary += 'Strategy found.\n'
			adviceBreakdown += 'A strategy has been loaded. Additional exposure strategies can be added, or the current strategy can now be run.'

		return (adviceSummary,adviceBreakdown)

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














