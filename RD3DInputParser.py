from crystals import *
from beams import *
from wedges import *
import copy

class parsedRD3Dinput(object):
	# this class is for a parsed RD3D input file
	def __init__(self,RD3DInputPath="",crystal=[],beamList=[],wedgeList=[]):

		self.RD3DInputPath     	= RD3DInputPath
		self.crystal         	= crystal
		self.beamList       	= beamList
		self.wedgeList 			= wedgeList

	def parseRaddoseInput(self):
		"""Parses the RADDOSE-3D Input file and returns the a crystal object, a
		list of beam objects and a list of wedge objects. returnType specifies
		which objects should be returned ('crystal': crystal, 'beam': beam list,
		 'all': everything)
		"""

		raddoseInput = open(self.RD3DInputPath,'r')

		crystalBlock = False
		beamBlock    = False
		wedgeBlock   = False

		crystalInfoDict = {} # create an empty crystal block dictionary to be filled
		beamInfoDict = {} # create an empty beam block dictionary to be filled
		wedge = wedges() #create default wedge

		for line in raddoseInput:

			# if empty line, skip over
			if  self.emptyLine(line) == True:
				continue
			line = self.curateLine(line) # remove comment part of line
			# ignore empty line once comment removed
			if  self.emptyLine(line) == True:
				continue

			if "Crystal" in line:
				crystalBlock = True
				beamBlock    = False
				wedgeBlock   = False

			elif "Beam" in line:
				crystalBlock = False
				beamBlock    = True
				wedgeBlock   = False

				# append wedge object to wedge list if this is not first beam (for input files with 
				# multiple beams & wedges)
				if len(self.beamList) != 0:
					self.wedgeList.append(copy.deepcopy(wedge))
					wedge = wedges() # make a new wedge object

			elif "Wedge" in line:
				crystalBlock = False
				beamBlock    = False
				wedgeBlock   = True

				# convert beam block dictionary into suitable beam object
				beam = self.beamDict2Obj(beamInfoDict)  
				self.beamList.append(copy.deepcopy(beam))
				beamInfoDict = {} # create new dictionary in case another beam later in file

			if crystalBlock:
				crystalInfoDict = self.parseCrystalLine(line,crystalInfoDict)

			elif beamBlock:
				beamInfoDict = self.parseBeamLine(line,beamInfoDict)

			elif wedgeBlock:
				wedge = self.parseWedgeLine(line,wedge)

		self.wedgeList.append(copy.deepcopy(wedge)) #append final wedge
		raddoseInput.close()

		# convert crystal block dictionary into suitable crystal object
		self.crystal = self.crystDict2Obj(crystalInfoDict)

	def curateLine(self,line):
		#removes comment part from line
		commentChars = ['#','!']
		commentCharIndices = []
		for commentChar in commentChars: #look for comment characters and store the index in list
			index = line.find(commentChar)
			commentCharIndices.append(index)

		if sorted(commentCharIndices)[-1] > -1: # check for positive indices
			minIndex = min(i for i in commentCharIndices if i > -1) #find smallest positive index
			line = line[0:minIndex] #remove comment part from line

		return line # return the comment-less line

	def emptyLine(self,line):
		# if empty line, flag
		try:
			line.split()[0]
			return False
		except IndexError:
			return True

	def parseWedgeLine(self,line,wedge):
		# parse RD3D input file wedge block 
		if line.split()[0].lower() == 'wedge':
			angles = line.split()[1:]
			wedge.angStart = angles[0]
			wedge.angStop  = angles[1]
		elif line.split()[0].lower() == 'exposuretime':
			wedge.exposureTime = line.split()[1]
		elif line.split()[0].lower() == 'angres':
			wedge.angRes = line.split()[1]
		elif line.split()[0].lower() == 'startoffset':
			wedge.startOffset = line.split()[1:]
		elif line.split()[0].lower() == 'transperdeg':
			wedge.transPerDeg = line.split()[1:]
		elif line.split()[0].lower() == 'rotaxmeamoffset':
			wedge.transperdeg = line.split()[1]
		return wedge

	def parseCrystalLine(self,line,crystalInfoDict):
		if line.split()[0] not in ('Crystal'):
			try:
				line.split()[2]
				crystalInfoDict[line.split()[0].lower()] = line.split()[1:]
			except IndexError:
				crystalInfoDict[line.split()[0].lower()] = line.split()[1]
		return crystalInfoDict

	def crystDict2Obj(self,crystalInfoDict):
		# convert the dictionary of input lines from RD3D input file
		# crystal block to correct crystals class subclass
		crystal = self.findCrystalClass(crystalInfoDict)
		crystal = self.getCrystalDictInfo(crystalInfoDict,crystal)
		crystal = self.getUnitCellDictInfo(crystalInfoDict,crystal)
		crystal = self.getCrystCompositionDictInfo(crystalInfoDict,crystal)
		crystal = self.getCrystalContainerInfo(crystalInfoDict,crystal)

		return crystal

	def findCrystalClass(self,crystalInfoDict):
		if crystalInfoDict["abscoefcalc"].lower() == 'average':
			crystal = crystals()
		elif crystalInfoDict["abscoefcalc"].lower() == 'exp':
			crystal = crystals_pdbCode()
		elif crystalInfoDict["abscoefcalc"].lower() == 'rd3d':
			crystal = crystals_userDefined()
		elif crystalInfoDict["abscoefcalc"].lower() == 'rdv2':
			crystal = crystals_RADDOSEv2()
		elif crystalInfoDict["abscoefcalc"].lower() == 'sequence':
			crystal = crystals_seqFile()
		elif crystalInfoDict["abscoefcalc"].lower() == 'saxs':
			crystal = crystals_SAXSuserDefined()
		elif crystalInfoDict["abscoefcalc"].lower() == 'saxsseq':
			crystal = crystals_SAXSseqFile()

		return crystal

	def getCrystalDictInfo(self,crystalInfoDict,crystal):
		# retrieve crystal type/dimension/pixPerMic etc properties from 
		# RD3D input file 
		crystal.type             	= crystalInfoDict["type"]

		if str(crystal.type).lower() in ('cuboid','spherical','cylindrical'):
			crystal.crystDimX       = crystalInfoDict["dimensions"][0]
		if str(crystal.type).lower() in ('cuboid','cylindrical'):
			crystal.crystDimY       = crystalInfoDict["dimensions"][1]
		if str(crystal.type).lower() in ('cuboid'):
			crystal.crystDimZ       = crystalInfoDict["dimensions"][2]
		if str(crystal.type).lower() in ('polyhedron'):
			crystal.modelFile		= crystalInfoDict["modelfile"]
			crystal.wireFrameType	= crystalInfoDict["wireframetype"]

		crystal.pixelsPerMicron  	= crystalInfoDict["pixelspermicron"]
		crystal.angleP 		  		= crystalInfoDict["anglep"]
		crystal.angleL 		  		= crystalInfoDict["anglel"]
		crystal.absCoefCalc 	 	= crystalInfoDict["abscoefcalc"]
		return crystal

	def getUnitCellDictInfo(self,crystalInfoDict,crystal):
		if not crystalInfoDict["abscoefcalc"].lower() in ('average','exp'):
			crystal.unitcell_a 		= crystalInfoDict["unitcell"][0]
			crystal.unitcell_b 		= crystalInfoDict["unitcell"][1]
			crystal.unitcell_c 		= crystalInfoDict["unitcell"][2]
			try:
				crystal.unitcell_alpha 	= crystalInfoDict["unitcell"][3]
			except IndexError:
				pass
			try:
				crystal.unitcell_beta 	= crystalInfoDict["unitcell"][4]
			except IndexError:
				pass
			try:
				crystal.unitcell_gamma 	= crystalInfoDict["unitcell"][5]
			except IndexError:
				pass

		return crystal

	def getCrystCompositionDictInfo(self,crystalInfoDict,crystal):
		if crystalInfoDict["abscoefcalc"].lower() in ('average'):
			return crystal

		if crystalInfoDict["abscoefcalc"].lower() in ('rd3d','rdv2'):
			crystal.numMonomers 		=  crystalInfoDict["nummonomers"]
			crystal.numResidues 		= crystalInfoDict["numresidues"]
			crystal.numRNA 				= crystalInfoDict["numrna"]
			crystal.numDNA 				= crystalInfoDict["numdna"]
		elif crystalInfoDict["abscoefcalc"].lower() in ('sequence'):
			crystal.numMonomers 		=  crystalInfoDict["nummonomers"]
			crystal.seqFile				= crystalInfoDict["seqfile"]
		elif crystalInfoDict["abscoefcalc"].lower() in ('saxs'):
			crystal.numResidues 		= crystalInfoDict["numresidues"]
			crystal.numRNA 				= crystalInfoDict["numrna"]
			crystal.numDNA 				= crystalInfoDict["numdna"]
			crystal.proteinConc 		= crystalInfoDict["proteinconc"]
		elif crystalInfoDict["abscoefcalc"].lower() in ('saxsseq'):
			crystal.seqFile				= crystalInfoDict["seqfile"]
			crystal.proteinConc 		= crystalInfoDict["proteinconc"]
		elif crystalInfoDict["abscoefcalc"].lower() in ('exp'):
			crystal.pdb = crystalInfoDict["pdb"]

		crystal.solventHeavyConc 	= " ".join(crystalInfoDict["solventheavyconc"])

		if not crystalInfoDict["abscoefcalc"].lower() in ('exp'):
			crystal.proteinHeavyAtoms 	= " ".join(crystalInfoDict["proteinheavyatoms"])
			crystal.solventFraction 	= crystalInfoDict["solventfraction"]

		return crystal

	def getCrystalContainerInfo(self,crystalInfoDict,crystal):
		# get crystal container information if present
		try:
			crystal.containerType 		= crystalInfoDict["containertype"]
		except KeyError:
			pass
		try:
			crystal.materialElements 	= crystalInfoDict["materialelements"]
		except KeyError:
			pass
		try:
			crystal.materialMixture 	= crystalInfoDict["materialmixture"]
		except KeyError:
			pass
		try:
			crystal.containerThickness 	= crystalInfoDict["containerthickness"]
		except KeyError:
			pass
		try:
			crystal.containerDensity 	= crystalInfoDict["containerdensity"]
		except KeyError:
			pass

		return crystal

	def parseBeamLine(self,line,beamInfoDict):
		if line.split()[0] in ('Beam'):
			return beamInfoDict

		if line.split()[0] not in ('Collimation'):
			try:
				line.split()[2]
				beamInfoDict[line.split()[0].lower()] = line.split()[1:]
			except IndexError:
				beamInfoDict[line.split()[0].lower()] = line.split()[1]
		else:
			beamInfoDict[line.split()[0].lower()] = line.split()[2:]
		return beamInfoDict

	def beamDict2Obj(self,beamInfoDict):
		# convert the dictionary of input lines from RD3D input file
		# beam block to correct beam class subclass
		beam = self.findBeamClass(beamInfoDict)
		beam = self.getBeamDictInfo(beamInfoDict,beam)
		beam = self.getBeamTypeSpecificInfo(beamInfoDict,beam)

		return beam

	def findBeamClass(self,beamInfoDict):
		if beamInfoDict["type"].lower() == 'tophat':
			beam = beams_Tophat()
		elif beamInfoDict["type"].lower() == 'gaussian':
			beam = beams_Gaussian()	
		elif beamInfoDict["type"].lower() == 'experimental':
			beam = beams_Experimental()

		return beam

	def getBeamDictInfo(self,beamInfoDict,beam):
		beam.flux        = beamInfoDict["flux"]
		beam.energy        = beamInfoDict["energy"]

		return beam

	def getBeamTypeSpecificInfo(self,beamInfoDict,beam):
		if beam.type == 'TopHat':
			beam.collimation  	= beamInfoDict["collimation"]
		elif beam.type == 'Gaussian':
			beam.fwhm         	= beamInfoDict["fwhm"]
			beam.collimation  	= beamInfoDict["collimation"]
		elif beam.type == 'Experimental':
			beam.pixelSize 		= beamInfoDict["pixelsize"]
			beam.file 			= beamInfoDict["file"]

		return beam
