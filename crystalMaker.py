from Tkinter import *
from ttk import *
from crystals import crystals
import tkMessageBox
from HoverInfo import HoverInfo
from InputsHelpText import CrystalInputHelp

class crystalMakerWindow(Frame):
	# this is a secondary crystal-maker window class here.

	def __init__(self,MainGui):
		self.master = MainGui.top_CrystMaker
		self.crystMakerFrame = Frame(self.master)
		self.crystMakerFrame.pack()

		# Crystal inputs here:
		l = Label(self.master,text="Crystal",style="labelFrameTitle.TLabel")
		self.currentStrategyCrystal = LabelFrame(self.master,labelwidget=l,
											style="MakeABeam.TFrame")
		self.currentStrategyCrystal.pack(side=TOP,padx=10, pady=10,fill=BOTH,expand=TRUE)

		#Create object that contains the help text
		self.helpText = CrystalInputHelp()

		# Crystal input --> crystal type
		self.CrystalType = StringVar()
		self.CrystalType.set('Cuboid')

		# Crystal input --> absorption coefficient
		self.crystalAbsCoeffType = StringVar()
		self.crystalAbsCoeffType.set('Average protein composition')

		#Crystal input --> container type
		self.containerType = StringVar()
		self.containerType.set("No container")

		self.crystalTypeInputs(MainGui)
		self.crystalAbsCoeffTypeInputs(MainGui)
		self.sampleContainerTypeInputs(MainGui)

		# Crystal input --> default cuboid crystal dimensions
		self.CrystalDimX,self.CrystalDimY,self.CrystalDimZ = StringVar(),StringVar(),StringVar()

		# Crystal input --> wireframe type and model file for a polyhedron crystal
		self.crystalWireFrameType, self.crystalModelFile, = StringVar(),StringVar(),
		self.crystalDimInputs(self.CrystalType)

		# Crystal input --> pixels per Micron
		self.crystalPixPerMicInputs()

		# Crystal input --> Angle P and Angle L - these angles define the
		#orientation of the crystal with respect to the beam and rotation axis.
		self.crystalAngleInputs()

		#Crystal input --> Inputs for crystal composition. This is dependent on
		#Absorption Coefficient (AbsCoeff) type chosen
		self.pdbcode = StringVar()
		self.unitcell_a = StringVar()
		self.unitcell_b = StringVar()
		self.unitcell_c = StringVar()
		self.unitcell_alpha = StringVar()
		self.unitcell_beta = StringVar()
		self.unitcell_gamma = StringVar()
		self.numMonomers =  StringVar()
		self.numResidues = StringVar()
		self.numRNA = StringVar()
		self.numDNA = StringVar()
		self.proteinHeavyAtoms = StringVar()
		self.solventHeavyConc = StringVar()
		self.solventFraction = StringVar()
		self.proteinConc = StringVar()
		self.sequenceFile = StringVar()
		self.crystalCompositionInputs(self.crystalAbsCoeffType)

		self.materialMixture = StringVar()
		self.materialElements = StringVar()
		self.containerThickness = StringVar()
		self.containerDensity = StringVar()
		self.containerTypeInputs(self.containerType)

		# create a 'make' button here to add this crystal to the list of added crystals
		self.crystalMakeButton(MainGui)

	def crystalTypeInputs(self,MainGui):
		# Crystal input 1 --> crystal type
		CrystalinputLabel1 = Label(self.currentStrategyCrystal,text="Crystal Type",style="inputBoxes.TLabel")
		CrystalinputLabel1.grid(row=0,column=0,sticky=E,pady=5,padx=6)
		crystTypeList = ['Cuboid','Spherical', 'Cylindrical', 'Polyhedron']
		crystTypeOptionMenu = OptionMenu(self.currentStrategyCrystal, self.CrystalType, self.CrystalType.get(),*crystTypeList, command= lambda x: self.update(self.CrystalType,self.crystalAbsCoeffType,self.containerType,MainGui))
		crystTypeOptionMenu.grid(row=0,column=1,sticky=W,pady=5,padx=6)
		self.hoverType = HoverInfo(CrystalinputLabel1, self.helpText.typeText)


	def crystalDimInputs(self,crystTypeValue):
		# Crystal input 2 --> crystal dimensions
		if crystTypeValue.get() in ('Cuboid','Spherical','Cylindrical'):

			CrystalinputLabel2 = Label(self.currentStrategyCrystal,text="Crystal Dimensions (microns):",style="inputBoxes.TLabel")
			CrystalinputLabel2.grid(row=0,column=2,sticky=E,pady=5,padx=6)
			self.hoverDims = HoverInfo(CrystalinputLabel2, self.helpText.dimsText)

			self.CrystalDimsInputsFrame = Frame(self.currentStrategyCrystal,style="inputBoxes.TFrame")
			self.CrystalDimsInputsFrame.grid(row=0,column=3,sticky=W,pady=5,padx=6)

			if crystTypeValue.get() == 'Cuboid':
				CrystalDimXLabel = Label(self.CrystalDimsInputsFrame,text="x = ",style="inputBoxes.TLabel")
				CrystalDimXLabel.pack(side=LEFT,pady=5,padx=6)
				CrystalinputBox2X = Entry(self.CrystalDimsInputsFrame,textvariable=self.CrystalDimX,width=5)
				CrystalinputBox2X.pack(side=LEFT,pady=5,padx=6)
				CrystalDimYLabel = Label(self.CrystalDimsInputsFrame,text="y = ",style="inputBoxes.TLabel")
				CrystalDimYLabel.pack(side=LEFT,pady=5,padx=6)
				CrystalinputBox2Y = Entry(self.CrystalDimsInputsFrame,textvariable=self.CrystalDimY,width=5)
				CrystalinputBox2Y.pack(side=LEFT,pady=5,padx=6)
				CrystalDimZLabel = Label(self.CrystalDimsInputsFrame,text="z = ",style="inputBoxes.TLabel")
				CrystalDimZLabel.pack(side=LEFT,pady=5,padx=6)
				CrystalinputBox2Z = Entry(self.CrystalDimsInputsFrame,textvariable=self.CrystalDimZ,width=5)
				CrystalinputBox2Z.pack(side=LEFT,pady=5,padx=6)

			elif crystTypeValue.get() == 'Spherical':
				CrystalDimXLabel = Label(self.CrystalDimsInputsFrame,text="Diameter = ",style="inputBoxes.TLabel")
				CrystalDimXLabel.pack(side=LEFT,pady=5,padx=6)
				CrystalinputBox2X = Entry(self.CrystalDimsInputsFrame,textvariable=self.CrystalDimX,width=5)
				CrystalinputBox2X.pack(side=LEFT,pady=5,padx=6)
				self.CrystalDimY.set(0)
				self.CrystalDimZ.set(0)

			elif crystTypeValue.get() == 'Cylindrical':
				CrystalDimXLabel = Label(self.CrystalDimsInputsFrame,text="Diameter = ",style="inputBoxes.TLabel")
				CrystalDimXLabel.pack(side=LEFT,pady=5,padx=6)
				CrystalinputBox2X = Entry(self.CrystalDimsInputsFrame,textvariable=self.CrystalDimX,width=5)
				CrystalinputBox2X.pack(side=LEFT,pady=5,padx=6)
				CrystalDimXLabel = Label(self.CrystalDimsInputsFrame,text="Height = ",style="inputBoxes.TLabel")
				CrystalDimXLabel.pack(side=LEFT,pady=5,padx=6)
				CrystalinputBox2X = Entry(self.CrystalDimsInputsFrame,textvariable=self.CrystalDimY,width=5)
				CrystalinputBox2X.pack(side=LEFT,pady=5,padx=6)
				self.CrystalDimZ.set(0)

		elif crystTypeValue.get() == 'Polyhedron':
			####################################################################
			#Currently the only input for wireframe type in RADDOSE-3D (as of
			#4th July 2015) is "obj". This means we have currently set the
			#crystal wireframe type to be "obj". If in future there are more
			#options then we require a drop-down menu for the choices. The
			#commented code below is the code required for the option menu for
			#the case when there are more options for the wireframe type.
			####################################################################
			# CrystalWireFrameTypeLabel = Label(self.currentStrategyCrystal,text="WireFrameType = ",style="inputBoxes.TLabel")
			# CrystalWireFrameTypeLabel.grid(row=0,column=2,sticky=E,pady=5,padx=6)
			# crystWireFrameTypeList = ['obj']
			# crystTypeOptionMenu = OptionMenu(self.currentStrategyCrystal, self.crystalWireFrameType, self.crystalWireFrameType.get(), *crystWireFrameTypeList)
			# crystTypeOptionMenu.grid(row=0,column=3,sticky=W,pady=5,padx=6)
			CrystalModelFileLabel = Label(self.currentStrategyCrystal,text="Model File (.obj) = ",style="inputBoxes.TLabel")
			CrystalModelFileLabel.grid(row=0,column=2,sticky=E,pady=5,padx=6)
			self.hoverModel = HoverInfo(CrystalModelFileLabel, self.helpText.modelText)
			CrystalModelFileInputBox = Entry(self.currentStrategyCrystal,textvariable=self.crystalModelFile,width=14)
			CrystalModelFileInputBox.grid(row=0,column=3,sticky=W,pady=5,padx=6)
			self.CrystalDimX.set(0)
			self.CrystalDimY.set(0)
			self.CrystalDimZ.set(0)
			self.crystalWireFrameType.set("obj")

	def crystalPixPerMicInputs(self):
		# Crystal input 3 --> pixels per Micron
		CrystalinputLabel3 = Label(self.currentStrategyCrystal,text="Pixels per Micron",style="inputBoxes.TLabel")
		CrystalinputLabel3.grid(row=1,column=0,sticky=E,pady=5,padx=6)
		self.hoverPix = HoverInfo(CrystalinputLabel3, self.helpText.pixPerMicText)
		self.CrystalPixPerMic = StringVar()
		CrystalinputBox3 = Entry(self.currentStrategyCrystal,textvariable=self.CrystalPixPerMic,width=5)
		CrystalinputBox3.grid(row=1,column=1,sticky=W,pady=5,padx=6)

	def crystalAngleInputs(self):
		CrystalAnglePLabel = Label(self.currentStrategyCrystal,text="Angle P = ",style="inputBoxes.TLabel")
		CrystalAnglePLabel.grid(row=1,column=2,sticky=E,pady=5,padx=6)
		self.hoverAngP = HoverInfo(CrystalAnglePLabel, self.helpText.anglePText)
		self.crystalAngleP = StringVar()
		CrystalAnglePInputBox = Entry(self.currentStrategyCrystal,textvariable=self.crystalAngleP,width=5)
		CrystalAnglePInputBox.grid(row=1,column=3,sticky=W,pady=5,padx=6)

		CrystalAngleLLabel = Label(self.currentStrategyCrystal,text="Angle L = ",style="inputBoxes.TLabel")
		CrystalAngleLLabel.grid(row=2,column=2,sticky=E,pady=5,padx=6)
		self.hoverAngL = HoverInfo(CrystalAngleLLabel, self.helpText.angleLText)
		self.crystalAngleL = StringVar()
		CrystalAnglePInputBox = Entry(self.currentStrategyCrystal,textvariable=self.crystalAngleL,width=5)
		CrystalAnglePInputBox.grid(row=2,column=3,sticky=W,pady=5,padx=6)

	def crystalAbsCoeffTypeInputs(self, MainGui):
		# Crystal input 4 --> absorption coefficient
		CrystalinputLabel4 = Label(self.currentStrategyCrystal,text="Absorption Coefficient",style="inputBoxes.TLabel")
		CrystalinputLabel4.grid(row=3,column=0,sticky=E,pady=5,padx=6)
		self.hoverAbsCoeff = HoverInfo(CrystalinputLabel4, self.helpText.absCoeffText)
		crystAbsCoeffList = ['Average protein composition', 'Using PDB code', 'User defined composition',
		'RADDOSE version 2', 'using sequence file', 'SAXS (user defined composition)', 'SAXS (sequence file)']
		crystAbsCoeffOptionMenu = OptionMenu(self.currentStrategyCrystal, self.crystalAbsCoeffType, self.crystalAbsCoeffType.get(), *crystAbsCoeffList, command= lambda x: self.update(self.CrystalType,self.crystalAbsCoeffType,self.containerType,MainGui))
		crystAbsCoeffOptionMenu.grid(row=3,column=1,sticky=W,pady=5,padx=6)

	def crystalCompositionInputs(self, absCoeffTypeValue):

		if 'Average protein composition' in absCoeffTypeValue.get():
			self.solventHeavyConc.set("0")
			self.pdbcode.set("0")
			self.unitcell_a.set("0")
			self.unitcell_b.set("0")
			self.unitcell_c.set("0")
			self.unitcell_alpha.set("0")
			self.unitcell_beta.set("0")
			self.unitcell_gamma.set("0")
			self.numMonomers.set("0")
			self.numResidues.set("0")
			self.numRNA.set("0")
			self.numDNA.set("0")
			self.proteinHeavyAtoms.set("Na 0")
			self.solventFraction.set("0")
			self.proteinConc.set("0")
			self.sequenceFile.set("0")

		elif 'Using PDB code' in absCoeffTypeValue.get():
			CrystalPDBLabel = Label(self.currentStrategyCrystal,text="PDB code",style="inputBoxes.TLabel")
			CrystalPDBLabel.grid(row=4,column=0,sticky=E,pady=5,padx=6)
			self.hoverPDB = HoverInfo(CrystalPDBLabel, self.helpText.pdbText)
			CrystalPDBInputBox = Entry(self.currentStrategyCrystal,textvariable=self.pdbcode,width=14)
			CrystalPDBInputBox.grid(row=4,column=1,sticky=W,pady=5,padx=6)

			CrystalHeavySolLabel = Label(self.currentStrategyCrystal,text="Solvent Heavy Concentration (optional)",style="inputBoxes.TLabel")
			CrystalHeavySolLabel.grid(row=4,column=2,sticky=E,pady=5,padx=6)
			self.hoverSolHeavy = HoverInfo(CrystalHeavySolLabel, self.helpText.solHeavyText)
			CrystalSolConcInputBox = Entry(self.currentStrategyCrystal,textvariable=self.solventHeavyConc,width=14)
			CrystalSolConcInputBox.grid(row=4,column=3,columnspan=4,sticky=W,pady=5,padx=6)
			self.unitcell_a.set("0")
			self.unitcell_b.set("0")
			self.unitcell_c.set("0")
			self.unitcell_alpha.set("0")
			self.unitcell_beta.set("0")
			self.unitcell_gamma.set("0")
			self.numMonomers.set("0")
			self.numResidues.set("0")
			self.numRNA.set("0")
			self.numDNA.set("0")
			self.proteinHeavyAtoms.set("Na 0")
			self.solventFraction.set("0")
			self.proteinConc.set("0")
			self.sequenceFile.set("0")

		elif 'User defined composition' in absCoeffTypeValue.get():
			CrystalNumMonLabel = Label(self.currentStrategyCrystal,text="Number of monomers",style="inputBoxes.TLabel")
			CrystalNumMonLabel.grid(row=4,column=0,sticky=E,pady=5,padx=6)
			self.hoverNumMon = HoverInfo(CrystalNumMonLabel, self.helpText.numMonText)
			CrystalNumMonInputBox = Entry(self.currentStrategyCrystal,textvariable=self.numMonomers,width=14)
			CrystalNumMonInputBox.grid(row=4,column=1,sticky=W,pady=5,padx=6)

			CrystalNumResLabel = Label(self.currentStrategyCrystal,text="Number of residues",style="inputBoxes.TLabel")
			CrystalNumResLabel.grid(row=4,column=2,sticky=E,pady=5,padx=6)
			self.hoverNumRes = HoverInfo(CrystalNumResLabel, self.helpText.numResText)
			CrystalNumResInputBox = Entry(self.currentStrategyCrystal,textvariable=self.numResidues,width=14)
			CrystalNumResInputBox.grid(row=4,column=3,sticky=W,pady=5,padx=6)

			CrystalNumRNALabel = Label(self.currentStrategyCrystal,text="Number of RNA nucleotides (optional)",style="inputBoxes.TLabel")
			CrystalNumRNALabel.grid(row=5,column=0,sticky=E,pady=5,padx=6)
			self.hoverNumRNA = HoverInfo(CrystalNumRNALabel, self.helpText.numRNAText)
			CrystalNumRNAInputBox = Entry(self.currentStrategyCrystal,textvariable=self.numRNA,width=14)
			CrystalNumRNAInputBox.grid(row=5,column=1,sticky=W,pady=5,padx=6)

			CrystalNumDNALabel = Label(self.currentStrategyCrystal,text="Number of DNA nucleotides (optional)",style="inputBoxes.TLabel")
			CrystalNumDNALabel.grid(row=5,column=2,sticky=E,pady=5,padx=6)
			self.hoverNumDNA = HoverInfo(CrystalNumDNALabel, self.helpText.numDNAText)
			CrystalNumDNAInputBox = Entry(self.currentStrategyCrystal,textvariable=self.numDNA,width=14)
			CrystalNumDNAInputBox.grid(row=5,column=3,sticky=W,pady=5,padx=6)

			CrystalHeavyProtLabel = Label(self.currentStrategyCrystal,text="Heavy atoms in protein (optional)",style="inputBoxes.TLabel")
			CrystalHeavyProtLabel.grid(row=6,column=0,sticky=E,pady=5,padx=6)
			self.hoverHeavyProt = HoverInfo(CrystalHeavyProtLabel, self.helpText.protHeavyText)
			CrystalHeavyProtInputBox = Entry(self.currentStrategyCrystal,textvariable=self.proteinHeavyAtoms,width=14)
			CrystalHeavyProtInputBox.grid(row=6,column=1,sticky=W,pady=5,padx=6)

			CrystalHeavySolLabel = Label(self.currentStrategyCrystal,text="Solvent Heavy Concentration (optional)",style="inputBoxes.TLabel")
			CrystalHeavySolLabel.grid(row=6,column=2,sticky=E,pady=5,padx=6)
			self.hoverSolHeavy = HoverInfo(CrystalHeavySolLabel, self.helpText.solHeavyText)
			CrystalHeavySolInputBox = Entry(self.currentStrategyCrystal,textvariable=self.solventHeavyConc,width=14)
			CrystalHeavySolInputBox.grid(row=6,column=3,sticky=W,pady=5,padx=6)

			CrystalSolFracLabel = Label(self.currentStrategyCrystal,text="Solvent fraction (optional)",style="inputBoxes.TLabel")
			CrystalSolFracLabel.grid(row=7,column=0,sticky=E,pady=5,padx=6)
			self.hoverSolFrac = HoverInfo(CrystalSolFracLabel, self.helpText.solFracText)
			CrystalSolFracInputBox = Entry(self.currentStrategyCrystal,textvariable=self.solventFraction,width=14)
			CrystalSolFracInputBox.grid(row=7,column=1,sticky=W,pady=5,padx=6)

			CrystalUnitcellLabel = Label(self.currentStrategyCrystal,text="Unit Cell Dimensions",style="inputBoxes.TLabel")
			CrystalUnitcellLabel.grid(row=8,column=0,sticky=E,pady=5,padx=6)
			self.hoverUnitcell = HoverInfo(CrystalUnitcellLabel, self.helpText.unitcellText)
			self.UnitcellInputsFrame = Frame(self.currentStrategyCrystal,style="inputBoxes.TFrame")
			self.UnitcellInputsFrame.grid(row=8,column=1,sticky=W,pady=5,padx=6)
			unitCellALabel = Label(self.UnitcellInputsFrame,text="a = ",style="inputBoxes.TLabel")
			unitCellALabel.grid(row=0,column=0,sticky=E,pady=5,padx=6)
			unitCellABox = Entry(self.UnitcellInputsFrame,textvariable=self.unitcell_a,width=5)
			unitCellABox.grid(row=0,column=1,sticky=W,pady=5,padx=6)
			unitCellBLabel = Label(self.UnitcellInputsFrame,text="b = ",style="inputBoxes.TLabel")
			unitCellBLabel.grid(row=1,column=0,sticky=E,pady=5,padx=6)
			unitCellBBox = Entry(self.UnitcellInputsFrame,textvariable=self.unitcell_b,width=5)
			unitCellBBox.grid(row=1,column=1,sticky=W,pady=5,padx=6)
			unitCellCLabel = Label(self.UnitcellInputsFrame,text="c = ",style="inputBoxes.TLabel")
			unitCellCLabel.grid(row=2,column=0,sticky=E,pady=5,padx=6)
			unitCellCBox = Entry(self.UnitcellInputsFrame,textvariable=self.unitcell_c,width=5)
			unitCellCBox.grid(row=2,column=1,sticky=W,pady=5,padx=6)
			unitCellAlphaLabel = Label(self.UnitcellInputsFrame,text="alpha = ",style="inputBoxes.TLabel")
			unitCellAlphaLabel.grid(row=0,column=2,sticky=E,pady=5,padx=6)
			unitCellAlphaBox = Entry(self.UnitcellInputsFrame,textvariable=self.unitcell_alpha,width=5)
			unitCellAlphaBox.grid(row=0,column=3,sticky=W,pady=5,padx=6)
			unitCellBetaLabel = Label(self.UnitcellInputsFrame,text="beta = ",style="inputBoxes.TLabel")
			unitCellBetaLabel.grid(row=1,column=2,sticky=E,pady=5,padx=6)
			unitCellBetaBox = Entry(self.UnitcellInputsFrame,textvariable=self.unitcell_beta,width=5)
			unitCellBetaBox.grid(row=1,column=3,sticky=W,pady=5,padx=6)
			unitCellGammaLabel = Label(self.UnitcellInputsFrame,text="gamma = ",style="inputBoxes.TLabel")
			unitCellGammaLabel.grid(row=2,column=2,sticky=E,pady=5,padx=6)
			unitCellGammaBox = Entry(self.UnitcellInputsFrame,textvariable=self.unitcell_gamma,width=5)
			unitCellGammaBox.grid(row=2,column=3,sticky=W,pady=5,padx=6)
			self.pdbcode.set("0")
			self.proteinConc.set("0")
			self.sequenceFile.set("0")

		elif 'RADDOSE version 2' in absCoeffTypeValue.get():
			CrystalNumMonLabel = Label(self.currentStrategyCrystal,text="Number of monomers",style="inputBoxes.TLabel")
			CrystalNumMonLabel.grid(row=4,column=0,sticky=E,pady=5,padx=6)
			self.hoverNumMon = HoverInfo(CrystalNumMonLabel, self.helpText.numMonText)
			CrystalNumMonInputBox = Entry(self.currentStrategyCrystal,textvariable=self.numMonomers,width=14)
			CrystalNumMonInputBox.grid(row=4,column=1,sticky=W,pady=5,padx=6)

			CrystalNumResLabel = Label(self.currentStrategyCrystal,text="Number of residues",style="inputBoxes.TLabel")
			CrystalNumResLabel.grid(row=4,column=2,sticky=E,pady=5,padx=6)
			self.hoverNumRes = HoverInfo(CrystalNumResLabel, self.helpText.numResText)
			CrystalNumResInputBox = Entry(self.currentStrategyCrystal,textvariable=self.numResidues,width=14)
			CrystalNumResInputBox.grid(row=4,column=3,sticky=W,pady=5,padx=6)

			CrystalNumRNALabel = Label(self.currentStrategyCrystal,text="Number of RNA nucleotides (optional)",style="inputBoxes.TLabel")
			CrystalNumRNALabel.grid(row=5,column=0,sticky=E,pady=5,padx=6)
			self.hoverNumRNA = HoverInfo(CrystalNumRNALabel, self.helpText.numRNAText)
			CrystalNumRNAInputBox = Entry(self.currentStrategyCrystal,textvariable=self.numRNA,width=14)
			CrystalNumRNAInputBox.grid(row=5,column=1,sticky=W,pady=5,padx=6)

			CrystalNumDNALabel = Label(self.currentStrategyCrystal,text="Number of DNA nucleotides (optional)",style="inputBoxes.TLabel")
			CrystalNumDNALabel.grid(row=5,column=2,sticky=E,pady=5,padx=6)
			self.hoverNumDNA = HoverInfo(CrystalNumDNALabel, self.helpText.numDNAText)
			CrystalNumDNAInputBox = Entry(self.currentStrategyCrystal,textvariable=self.numDNA,width=14)
			CrystalNumDNAInputBox.grid(row=5,column=3,sticky=W,pady=5,padx=6)

			CrystalHeavyProtLabel = Label(self.currentStrategyCrystal,text="Heavy atoms in protein (optional)",style="inputBoxes.TLabel")
			CrystalHeavyProtLabel.grid(row=6,column=0,sticky=E,pady=5,padx=6)
			self.hoverHeavyProt = HoverInfo(CrystalHeavyProtLabel, self.helpText.protHeavyText)
			CrystalHeavyProtInputBox = Entry(self.currentStrategyCrystal,textvariable=self.proteinHeavyAtoms,width=14)
			CrystalHeavyProtInputBox.grid(row=6,column=1,sticky=W,pady=5,padx=6)

			CrystalHeavySolLabel = Label(self.currentStrategyCrystal,text="Solvent Heavy Concentration (optional)",style="inputBoxes.TLabel")
			CrystalHeavySolLabel.grid(row=6,column=2,sticky=E,pady=5,padx=6)
			self.hoverSolHeavy = HoverInfo(CrystalHeavySolLabel, self.helpText.solHeavyText)
			CrystalHeavySolInputBox = Entry(self.currentStrategyCrystal,textvariable=self.solventHeavyConc,width=14)
			CrystalHeavySolInputBox.grid(row=6,column=3,sticky=W,pady=5,padx=6)

			CrystalSolFracLabel = Label(self.currentStrategyCrystal,text="Solvent fraction",style="inputBoxes.TLabel")
			CrystalSolFracLabel.grid(row=7,column=0,sticky=E,pady=5,padx=6)
			self.hoverSolFrac = HoverInfo(CrystalSolFracLabel, self.helpText.solFracText)
			CrystalSolFracInputBox = Entry(self.currentStrategyCrystal,textvariable=self.solventFraction,width=14)
			CrystalSolFracInputBox.grid(row=7,column=1,sticky=W,pady=5,padx=6)

			CrystalUnitcellLabel = Label(self.currentStrategyCrystal,text="Unit Cell Dimensions",style="inputBoxes.TLabel")
			CrystalUnitcellLabel.grid(row=8,column=0,sticky=E,pady=5,padx=6)
			self.hoverUnitcell = HoverInfo(CrystalUnitcellLabel, self.helpText.unitcellText)
			self.UnitcellInputsFrame = Frame(self.currentStrategyCrystal,style="inputBoxes.TFrame")
			self.UnitcellInputsFrame.grid(row=8,column=1,sticky=W,pady=5,padx=6)
			unitCellALabel = Label(self.UnitcellInputsFrame,text="a = ",style="inputBoxes.TLabel")
			unitCellALabel.grid(row=0,column=0,sticky=E,pady=5,padx=6)
			unitCellABox = Entry(self.UnitcellInputsFrame,textvariable=self.unitcell_a,width=5)
			unitCellABox.grid(row=0,column=1,sticky=W,pady=5,padx=6)
			unitCellBLabel = Label(self.UnitcellInputsFrame,text="b = ",style="inputBoxes.TLabel")
			unitCellBLabel.grid(row=1,column=0,sticky=E,pady=5,padx=6)
			unitCellBBox = Entry(self.UnitcellInputsFrame,textvariable=self.unitcell_b,width=5)
			unitCellBBox.grid(row=1,column=1,sticky=W,pady=5,padx=6)
			unitCellCLabel = Label(self.UnitcellInputsFrame,text="c = ",style="inputBoxes.TLabel")
			unitCellCLabel.grid(row=2,column=0,sticky=E,pady=5,padx=6)
			unitCellCBox = Entry(self.UnitcellInputsFrame,textvariable=self.unitcell_c,width=5)
			unitCellCBox.grid(row=2,column=1,sticky=W,pady=5,padx=6)
			unitCellAlphaLabel = Label(self.UnitcellInputsFrame,text="alpha = ",style="inputBoxes.TLabel")
			unitCellAlphaLabel.grid(row=0,column=2,sticky=E,pady=5,padx=6)
			unitCellAlphaBox = Entry(self.UnitcellInputsFrame,textvariable=self.unitcell_alpha,width=5)
			unitCellAlphaBox.grid(row=0,column=3,sticky=W,pady=5,padx=6)
			unitCellBetaLabel = Label(self.UnitcellInputsFrame,text="beta = ",style="inputBoxes.TLabel")
			unitCellBetaLabel.grid(row=1,column=2,sticky=E,pady=5,padx=6)
			unitCellBetaBox = Entry(self.UnitcellInputsFrame,textvariable=self.unitcell_beta,width=5)
			unitCellBetaBox.grid(row=1,column=3,sticky=W,pady=5,padx=6)
			unitCellGammaLabel = Label(self.UnitcellInputsFrame,text="gamma = ",style="inputBoxes.TLabel")
			unitCellGammaLabel.grid(row=2,column=2,sticky=E,pady=5,padx=6)
			unitCellGammaBox = Entry(self.UnitcellInputsFrame,textvariable=self.unitcell_gamma,width=5)
			unitCellGammaBox.grid(row=2,column=3,sticky=W,pady=5,padx=6)
			self.pdbcode.set("0")
			self.proteinConc.set("0")
			self.sequenceFile.set("0")

		elif 'using sequence file' in absCoeffTypeValue.get():
			CrystalNumMonLabel = Label(self.currentStrategyCrystal,text="Number of monomers",style="inputBoxes.TLabel")
			CrystalNumMonLabel.grid(row=4,column=0,sticky=E,pady=5,padx=6)
			self.hoverNumMon = HoverInfo(CrystalNumMonLabel, self.helpText.numMonText)
			CrystalNumMonInputBox = Entry(self.currentStrategyCrystal,textvariable=self.numMonomers,width=14)
			CrystalNumMonInputBox.grid(row=4,column=1,sticky=W,pady=5,padx=6)

			CrystalSeqResLabel = Label(self.currentStrategyCrystal,text="Sequence file",style="inputBoxes.TLabel")
			CrystalSeqResLabel.grid(row=4,column=2,sticky=E,pady=5,padx=6)
			self.hoverSeqRes = HoverInfo(CrystalSeqResLabel, self.helpText.seqFileText)
			CrystalNumResInputBox = Entry(self.currentStrategyCrystal,textvariable=self.sequenceFile,width=14)
			CrystalNumResInputBox.grid(row=4,column=3,sticky=W,pady=5,padx=6)

			CrystalHeavyProtLabel = Label(self.currentStrategyCrystal,text="Heavy atoms in protein (optional)",style="inputBoxes.TLabel")
			CrystalHeavyProtLabel.grid(row=6,column=0,sticky=E,pady=5,padx=6)
			self.hoverHeavyProt = HoverInfo(CrystalHeavyProtLabel, self.helpText.protHeavyText)
			CrystalHeavyProtInputBox = Entry(self.currentStrategyCrystal,textvariable=self.proteinHeavyAtoms,width=14)
			CrystalHeavyProtInputBox.grid(row=6,column=1,sticky=W,pady=5,padx=6)

			CrystalHeavySolLabel = Label(self.currentStrategyCrystal,text="Solvent Heavy Concentration (optional)",style="inputBoxes.TLabel")
			CrystalHeavySolLabel.grid(row=6,column=2,sticky=E,pady=5,padx=6)
			self.hoverSolHeavy = HoverInfo(CrystalHeavySolLabel, self.helpText.solHeavyText)
			CrystalHeavySolInputBox = Entry(self.currentStrategyCrystal,textvariable=self.solventHeavyConc,width=14)
			CrystalHeavySolInputBox.grid(row=6,column=3,sticky=W,pady=5,padx=6)

			CrystalSolFracLabel = Label(self.currentStrategyCrystal,text="Solvent fraction (optional)",style="inputBoxes.TLabel")
			CrystalSolFracLabel.grid(row=7,column=0,sticky=E,pady=5,padx=6)
			self.hoverSolFrac = HoverInfo(CrystalSolFracLabel, self.helpText.solFracText)
			CrystalSolFracInputBox = Entry(self.currentStrategyCrystal,textvariable=self.solventFraction,width=14)
			CrystalSolFracInputBox.grid(row=7,column=1,sticky=W,pady=5,padx=6)

			CrystalUnitcellLabel = Label(self.currentStrategyCrystal,text="Unit Cell Dimensions",style="inputBoxes.TLabel")
			CrystalUnitcellLabel.grid(row=8,column=0,sticky=E,pady=5,padx=6)
			self.hoverUnitcell = HoverInfo(CrystalUnitcellLabel, self.helpText.unitcellText)
			self.UnitcellInputsFrame = Frame(self.currentStrategyCrystal,style="inputBoxes.TFrame")
			self.UnitcellInputsFrame.grid(row=8,column=1,sticky=W,pady=5,padx=6)
			unitCellALabel = Label(self.UnitcellInputsFrame,text="a = ",style="inputBoxes.TLabel")
			unitCellALabel.grid(row=0,column=0,sticky=E,pady=5,padx=6)
			unitCellABox = Entry(self.UnitcellInputsFrame,textvariable=self.unitcell_a,width=5)
			unitCellABox.grid(row=0,column=1,sticky=W,pady=5,padx=6)
			unitCellBLabel = Label(self.UnitcellInputsFrame,text="b = ",style="inputBoxes.TLabel")
			unitCellBLabel.grid(row=1,column=0,sticky=E,pady=5,padx=6)
			unitCellBBox = Entry(self.UnitcellInputsFrame,textvariable=self.unitcell_b,width=5)
			unitCellBBox.grid(row=1,column=1,sticky=W,pady=5,padx=6)
			unitCellCLabel = Label(self.UnitcellInputsFrame,text="c = ",style="inputBoxes.TLabel")
			unitCellCLabel.grid(row=2,column=0,sticky=E,pady=5,padx=6)
			unitCellCBox = Entry(self.UnitcellInputsFrame,textvariable=self.unitcell_c,width=5)
			unitCellCBox.grid(row=2,column=1,sticky=W,pady=5,padx=6)
			unitCellAlphaLabel = Label(self.UnitcellInputsFrame,text="alpha = ",style="inputBoxes.TLabel")
			unitCellAlphaLabel.grid(row=0,column=2,sticky=E,pady=5,padx=6)
			unitCellAlphaBox = Entry(self.UnitcellInputsFrame,textvariable=self.unitcell_alpha,width=5)
			unitCellAlphaBox.grid(row=0,column=3,sticky=W,pady=5,padx=6)
			unitCellBetaLabel = Label(self.UnitcellInputsFrame,text="beta = ",style="inputBoxes.TLabel")
			unitCellBetaLabel.grid(row=1,column=2,sticky=E,pady=5,padx=6)
			unitCellBetaBox = Entry(self.UnitcellInputsFrame,textvariable=self.unitcell_beta,width=5)
			unitCellBetaBox.grid(row=1,column=3,sticky=W,pady=5,padx=6)
			unitCellGammaLabel = Label(self.UnitcellInputsFrame,text="gamma = ",style="inputBoxes.TLabel")
			unitCellGammaLabel.grid(row=2,column=2,sticky=E,pady=5,padx=6)
			unitCellGammaBox = Entry(self.UnitcellInputsFrame,textvariable=self.unitcell_gamma,width=5)
			unitCellGammaBox.grid(row=2,column=3,sticky=W,pady=5,padx=6)
			self.pdbcode.set("0")
			self.proteinConc.set("0")
			self.numResidues.set("0")
			self.numRNA.set("0")
			self.numDNA.set("0")

		elif 'SAXS (user defined composition)' in absCoeffTypeValue.get():
			CrystalProtConcLabel = Label(self.currentStrategyCrystal,text="Protein concentration",style="inputBoxes.TLabel")
			CrystalProtConcLabel.grid(row=4,column=0,sticky=E,pady=5,padx=6)
			self.hoverProtConc = HoverInfo(CrystalProtConcLabel, self.helpText.protConcText)
			CrystalNumMonInputBox = Entry(self.currentStrategyCrystal,textvariable=self.proteinConc,width=14)
			CrystalNumMonInputBox.grid(row=4,column=1,sticky=W,pady=5,padx=6)

			CrystalNumResLabel = Label(self.currentStrategyCrystal,text="Number of residues",style="inputBoxes.TLabel")
			CrystalNumResLabel.grid(row=4,column=2,sticky=E,pady=5,padx=6)
			self.hoverNumRes = HoverInfo(CrystalNumResLabel, self.helpText.numResText)
			CrystalNumResInputBox = Entry(self.currentStrategyCrystal,textvariable=self.numResidues,width=14)
			CrystalNumResInputBox.grid(row=4,column=3,sticky=W,pady=5,padx=6)

			CrystalNumRNALabel = Label(self.currentStrategyCrystal,text="Number of RNA nucleotides (optional)",style="inputBoxes.TLabel")
			CrystalNumRNALabel.grid(row=5,column=0,sticky=E,pady=5,padx=6)
			self.hoverNumRNA = HoverInfo(CrystalNumRNALabel, self.helpText.numRNAText)
			CrystalNumRNAInputBox = Entry(self.currentStrategyCrystal,textvariable=self.numRNA,width=14)
			CrystalNumRNAInputBox.grid(row=5,column=1,sticky=W,pady=5,padx=6)

			CrystalNumDNALabel = Label(self.currentStrategyCrystal,text="Number of DNA nucleotides (optional)",style="inputBoxes.TLabel")
			CrystalNumDNALabel.grid(row=5,column=2,sticky=E,pady=5,padx=6)
			self.hoverNumDNA = HoverInfo(CrystalNumDNALabel, self.helpText.numDNAText)
			CrystalNumDNAInputBox = Entry(self.currentStrategyCrystal,textvariable=self.numDNA,width=14)
			CrystalNumDNAInputBox.grid(row=5,column=3,sticky=W,pady=5,padx=6)

			CrystalHeavyProtLabel = Label(self.currentStrategyCrystal,text="Heavy atoms in protein (optional)",style="inputBoxes.TLabel")
			CrystalHeavyProtLabel.grid(row=6,column=0,sticky=E,pady=5,padx=6)
			self.hoverHeavyProt = HoverInfo(CrystalHeavyProtLabel, self.helpText.protHeavyText)
			CrystalHeavyProtInputBox = Entry(self.currentStrategyCrystal,textvariable=self.proteinHeavyAtoms,width=14)
			CrystalHeavyProtInputBox.grid(row=6,column=1,sticky=W,pady=5,padx=6)

			CrystalHeavySolLabel = Label(self.currentStrategyCrystal,text="Solvent Heavy Concentration (optional)",style="inputBoxes.TLabel")
			CrystalHeavySolLabel.grid(row=6,column=2,sticky=E,pady=5,padx=6)
			self.hoverSolHeavy = HoverInfo(CrystalHeavySolLabel, self.helpText.solHeavyText)
			CrystalHeavySolInputBox = Entry(self.currentStrategyCrystal,textvariable=self.solventHeavyConc,width=14)
			CrystalHeavySolInputBox.grid(row=6,column=3,sticky=W,pady=5,padx=6)

			CrystalSolFracLabel = Label(self.currentStrategyCrystal,text="Solvent fraction (optional)",style="inputBoxes.TLabel")
			CrystalSolFracLabel.grid(row=7,column=0,sticky=E,pady=5,padx=6)
			self.hoverSolFrac = HoverInfo(CrystalSolFracLabel, self.helpText.solFracText)
			CrystalSolFracInputBox = Entry(self.currentStrategyCrystal,textvariable=self.solventFraction,width=14)
			CrystalSolFracInputBox.grid(row=7,column=1,sticky=W,pady=5,padx=6)

			CrystalUnitcellLabel = Label(self.currentStrategyCrystal,text="Unit Cell Dimensions (optional)",style="inputBoxes.TLabel")
			CrystalUnitcellLabel.grid(row=8,column=0,sticky=E,pady=5,padx=6)
			self.hoverUnitcell = HoverInfo(CrystalUnitcellLabel, self.helpText.unitcellSAXSText)
			self.UnitcellInputsFrame = Frame(self.currentStrategyCrystal,style="inputBoxes.TFrame")
			self.UnitcellInputsFrame.grid(row=8,column=1,sticky=W,pady=5,padx=6)
			unitCellALabel = Label(self.UnitcellInputsFrame,text="a = ",style="inputBoxes.TLabel")
			unitCellALabel.grid(row=0,column=0,sticky=E,pady=5,padx=6)
			unitCellABox = Entry(self.UnitcellInputsFrame,textvariable=self.unitcell_a,width=5)
			unitCellABox.grid(row=0,column=1,sticky=W,pady=5,padx=6)
			unitCellBLabel = Label(self.UnitcellInputsFrame,text="b = ",style="inputBoxes.TLabel")
			unitCellBLabel.grid(row=1,column=0,sticky=E,pady=5,padx=6)
			unitCellBBox = Entry(self.UnitcellInputsFrame,textvariable=self.unitcell_b,width=5)
			unitCellBBox.grid(row=1,column=1,sticky=W,pady=5,padx=6)
			unitCellCLabel = Label(self.UnitcellInputsFrame,text="c = ",style="inputBoxes.TLabel")
			unitCellCLabel.grid(row=2,column=0,sticky=E,pady=5,padx=6)
			unitCellCBox = Entry(self.UnitcellInputsFrame,textvariable=self.unitcell_c,width=5)
			unitCellCBox.grid(row=2,column=1,sticky=W,pady=5,padx=6)
			unitCellAlphaLabel = Label(self.UnitcellInputsFrame,text="alpha = ",style="inputBoxes.TLabel")
			unitCellAlphaLabel.grid(row=0,column=2,sticky=E,pady=5,padx=6)
			unitCellAlphaBox = Entry(self.UnitcellInputsFrame,textvariable=self.unitcell_alpha,width=5)
			unitCellAlphaBox.grid(row=0,column=3,sticky=W,pady=5,padx=6)
			unitCellBetaLabel = Label(self.UnitcellInputsFrame,text="beta = ",style="inputBoxes.TLabel")
			unitCellBetaLabel.grid(row=1,column=2,sticky=E,pady=5,padx=6)
			unitCellBetaBox = Entry(self.UnitcellInputsFrame,textvariable=self.unitcell_beta,width=5)
			unitCellBetaBox.grid(row=1,column=3,sticky=W,pady=5,padx=6)
			unitCellGammaLabel = Label(self.UnitcellInputsFrame,text="gamma = ",style="inputBoxes.TLabel")
			unitCellGammaLabel.grid(row=2,column=2,sticky=E,pady=5,padx=6)
			unitCellGammaBox = Entry(self.UnitcellInputsFrame,textvariable=self.unitcell_gamma,width=5)
			unitCellGammaBox.grid(row=2,column=3,sticky=W,pady=5,padx=6)
			self.pdbcode.set("0")
			self.numMonomers.set("0")
			self.sequenceFile.set("0")

		elif 'SAXS (sequence file)' in absCoeffTypeValue.get():
			CrystalProtConcLabel = Label(self.currentStrategyCrystal,text="Protein concentration",style="inputBoxes.TLabel")
			CrystalProtConcLabel.grid(row=4,column=0,sticky=E,pady=5,padx=6)
			self.hoverProtConc = HoverInfo(CrystalProtConcLabel, self.helpText.protConcText)
			CrystalNumMonInputBox = Entry(self.currentStrategyCrystal,textvariable=self.proteinConc,width=14)
			CrystalNumMonInputBox.grid(row=4,column=1,sticky=W,pady=5,padx=6)

			CrystalSeqResLabel = Label(self.currentStrategyCrystal,text="Sequence file",style="inputBoxes.TLabel")
			CrystalSeqResLabel.grid(row=4,column=2,sticky=E,pady=5,padx=6)
			self.hoverSeqRes = HoverInfo(CrystalSeqResLabel, self.helpText.seqFileText)
			CrystalNumResInputBox = Entry(self.currentStrategyCrystal,textvariable=self.sequenceFile,width=14)
			CrystalNumResInputBox.grid(row=4,column=3,sticky=W,pady=5,padx=6)

			CrystalHeavyProtLabel = Label(self.currentStrategyCrystal,text="Heavy atoms in protein (optional)",style="inputBoxes.TLabel")
			CrystalHeavyProtLabel.grid(row=6,column=0,sticky=E,pady=5,padx=6)
			self.hoverHeavyProt = HoverInfo(CrystalHeavyProtLabel, self.helpText.protHeavyText)
			CrystalHeavyProtInputBox = Entry(self.currentStrategyCrystal,textvariable=self.proteinHeavyAtoms,width=14)
			CrystalHeavyProtInputBox.grid(row=6,column=1,sticky=W,pady=5,padx=6)

			CrystalHeavySolLabel = Label(self.currentStrategyCrystal,text="Solvent Heavy Concentration (optional)",style="inputBoxes.TLabel")
			CrystalHeavySolLabel.grid(row=6,column=2,sticky=E,pady=5,padx=6)
			self.hoverSolHeavy = HoverInfo(CrystalHeavySolLabel, self.helpText.solHeavyText)
			CrystalHeavySolInputBox = Entry(self.currentStrategyCrystal,textvariable=self.solventHeavyConc,width=14)
			CrystalHeavySolInputBox.grid(row=6,column=3,sticky=W,pady=5,padx=6)

			CrystalSolFracLabel = Label(self.currentStrategyCrystal,text="Solvent fraction (optional)",style="inputBoxes.TLabel")
			CrystalSolFracLabel.grid(row=7,column=0,sticky=E,pady=5,padx=6)
			self.hoverSolFrac = HoverInfo(CrystalSolFracLabel, self.helpText.solFracText)
			CrystalSolFracInputBox = Entry(self.currentStrategyCrystal,textvariable=self.solventFraction,width=14)
			CrystalSolFracInputBox.grid(row=7,column=1,sticky=W,pady=5,padx=6)

			CrystalUnitcellLabel = Label(self.currentStrategyCrystal,text="Unit Cell Dimensions (optional)",style="inputBoxes.TLabel")
			CrystalUnitcellLabel.grid(row=8,column=0,sticky=E,pady=5,padx=6)
			self.hoverUnitcell = HoverInfo(CrystalUnitcellLabel, self.helpText.unitcellSAXSText)
			self.UnitcellInputsFrame = Frame(self.currentStrategyCrystal,style="inputBoxes.TFrame")
			self.UnitcellInputsFrame.grid(row=8,column=1,sticky=W,pady=5,padx=6)
			unitCellALabel = Label(self.UnitcellInputsFrame,text="a = ",style="inputBoxes.TLabel")
			unitCellALabel.grid(row=0,column=0,sticky=E,pady=5,padx=6)
			unitCellABox = Entry(self.UnitcellInputsFrame,textvariable=self.unitcell_a,width=5)
			unitCellABox.grid(row=0,column=1,sticky=W,pady=5,padx=6)
			unitCellBLabel = Label(self.UnitcellInputsFrame,text="b = ",style="inputBoxes.TLabel")
			unitCellBLabel.grid(row=1,column=0,sticky=E,pady=5,padx=6)
			unitCellBBox = Entry(self.UnitcellInputsFrame,textvariable=self.unitcell_b,width=5)
			unitCellBBox.grid(row=1,column=1,sticky=W,pady=5,padx=6)
			unitCellCLabel = Label(self.UnitcellInputsFrame,text="c = ",style="inputBoxes.TLabel")
			unitCellCLabel.grid(row=2,column=0,sticky=E,pady=5,padx=6)
			unitCellCBox = Entry(self.UnitcellInputsFrame,textvariable=self.unitcell_c,width=5)
			unitCellCBox.grid(row=2,column=1,sticky=W,pady=5,padx=6)
			unitCellAlphaLabel = Label(self.UnitcellInputsFrame,text="alpha = ",style="inputBoxes.TLabel")
			unitCellAlphaLabel.grid(row=0,column=2,sticky=E,pady=5,padx=6)
			unitCellAlphaBox = Entry(self.UnitcellInputsFrame,textvariable=self.unitcell_alpha,width=5)
			unitCellAlphaBox.grid(row=0,column=3,sticky=W,pady=5,padx=6)
			unitCellBetaLabel = Label(self.UnitcellInputsFrame,text="beta = ",style="inputBoxes.TLabel")
			unitCellBetaLabel.grid(row=1,column=2,sticky=E,pady=5,padx=6)
			unitCellBetaBox = Entry(self.UnitcellInputsFrame,textvariable=self.unitcell_beta,width=5)
			unitCellBetaBox.grid(row=1,column=3,sticky=W,pady=5,padx=6)
			unitCellGammaLabel = Label(self.UnitcellInputsFrame,text="gamma = ",style="inputBoxes.TLabel")
			unitCellGammaLabel.grid(row=2,column=2,sticky=E,pady=5,padx=6)
			unitCellGammaBox = Entry(self.UnitcellInputsFrame,textvariable=self.unitcell_gamma,width=5)
			unitCellGammaBox.grid(row=2,column=3,sticky=W,pady=5,padx=6)
			self.pdbcode.set("0")
			self.numMonomers.set("0")
			self.numResidues.set("0")
			self.numRNA.set("0")
			self.numDNA.set("0")

	def sampleContainerTypeInputs(self, MainGui):
		# Crystal input  --> Sample container type
		containerTypeInputLabel = Label(self.currentStrategyCrystal,text="Type of sample container",style="inputBoxes.TLabel")
		containerTypeInputLabel.grid(row=9,column=0,sticky=E,pady=5,padx=6)
		self.hoverConType = HoverInfo(containerTypeInputLabel, self.helpText.conTypeText)
		containerTypeList = ['No container', 'Specify mixture', 'Specify elemental composition']
		containerTypeOptionMenu = OptionMenu(self.currentStrategyCrystal, self.containerType, self.containerType.get(), *containerTypeList, command= lambda x: self.update(self.CrystalType,self.crystalAbsCoeffType,self.containerType,MainGui))
		containerTypeOptionMenu.grid(row=9,column=1,sticky=W,pady=5,padx=6)

	def containerTypeInputs(self, containerTypeValue):
			if 'No container' in containerTypeValue.get():
				self.materialMixture.set("0")
				self.materialElements.set("Na 0")
				self.containerThickness.set("0")
				self.containerDensity.set("0")

			elif 'Specify mixture' in containerTypeValue.get():
				containerMixtureLabel = Label(self.currentStrategyCrystal,text="Mixture",style="inputBoxes.TLabel")
				containerMixtureLabel.grid(row=10,column=0,sticky=E,pady=5,padx=6)
				self.hoverConMix = HoverInfo(containerMixtureLabel, self.helpText.conMixText)
				containerMixtureInputBox = Entry(self.currentStrategyCrystal,textvariable=self.materialMixture,width=14)
				containerMixtureInputBox.grid(row=10,column=1,columnspan=2,sticky=W,pady=5,padx=6)

				containerThicknessLabel = Label(self.currentStrategyCrystal,text="Container thickness",style="inputBoxes.TLabel")
				containerThicknessLabel.grid(row=11,column=0,sticky=E,pady=5,padx=6)
				self.hoverConThick = HoverInfo(containerThicknessLabel, self.helpText.conThick)
				containerThicknessInputBox = Entry(self.currentStrategyCrystal,textvariable=self.containerThickness,width=14)
				containerThicknessInputBox.grid(row=11,column=1,sticky=W,pady=5,padx=6)

				containerDensityLabel = Label(self.currentStrategyCrystal,text="Container density",style="inputBoxes.TLabel")
				containerDensityLabel.grid(row=11,column=2,sticky=E,pady=5,padx=6)
				self.hoverConDens = HoverInfo(containerDensityLabel, self.helpText.conDens)
				containerDensityInputBox = Entry(self.currentStrategyCrystal,textvariable=self.containerDensity,width=14)
				containerDensityInputBox.grid(row=11,column=3,sticky=W,pady=5,padx=6)
				self.materialElements.set("Na 0")

			elif 'Specify elemental composition' in containerTypeValue.get():
				containerElementalLabel = Label(self.currentStrategyCrystal,text="Elemental composition",style="inputBoxes.TLabel")
				containerElementalLabel.grid(row=10,column=0,sticky=E,pady=5,padx=6)
				self.hoverConEl = HoverInfo(containerElementalLabel, self.helpText.conElText)
				containerMixtureInputBox = Entry(self.currentStrategyCrystal,textvariable=self.materialElements,width=14)
				containerMixtureInputBox.grid(row=10,column=1,columnspan=2,sticky=W,pady=5,padx=6)

				containerThicknessLabel = Label(self.currentStrategyCrystal,text="Container thickness",style="inputBoxes.TLabel")
				containerThicknessLabel.grid(row=11,column=0,sticky=E,pady=5,padx=6)
				self.hoverConThick = HoverInfo(containerThicknessLabel, self.helpText.conThick)
				containerThicknessInputBox = Entry(self.currentStrategyCrystal,textvariable=self.containerThickness,width=14)
				containerThicknessInputBox.grid(row=11,column=1,sticky=W,pady=5,padx=6)

				containerDensityLabel = Label(self.currentStrategyCrystal,text="Container density",style="inputBoxes.TLabel")
				containerDensityLabel.grid(row=11,column=2,sticky=E,pady=5,padx=6)
				self.hoverConDens = HoverInfo(containerDensityLabel, self.helpText.conDens)
				containerDensityInputBox = Entry(self.currentStrategyCrystal,textvariable=self.containerDensity,width=14)
				containerDensityInputBox.grid(row=11,column=3,sticky=W,pady=5,padx=6)
				self.materialMixture.set("0")


	def update(self, crystTypeValue, absCoeffTypeValue, containerTypeValue, MainGui):

		# remove all widgets within the current crystal-maker frame
		for widget in self.currentStrategyCrystal.winfo_children():
			widget.destroy()

		self.crystalTypeInputs(MainGui)
		self.crystalAbsCoeffTypeInputs(MainGui)
		self.sampleContainerTypeInputs(MainGui)
		self.crystalDimInputs(crystTypeValue)
		self.crystalPixPerMicInputs()
		self.crystalAngleInputs()
		self.crystalMakeButton(MainGui)
		self.crystalCompositionInputs(absCoeffTypeValue)
		self.containerTypeInputs(containerTypeValue)

	def crystalMakeButton(self,MainGui):
		# create a 'make' button here to add this crystal to the list of added crystals
		crystMakeButton = Button(self.currentStrategyCrystal,text="Make",command= lambda: self.addMadeCryst(MainGui))
		crystMakeButton.grid(row=12,columnspan=3,pady=5)

	def addMadeCryst(self,MainGui):
		# make a new crystal object from above entered parameters and add to both listbox crystal list and
		# also list of crystal objects

		if 'Average protein composition' in self.crystalAbsCoeffType.get():
			newCryst = crystals(MainGui.crystMakeName.get(),self.CrystalType.get(),self.CrystalDimX.get(),
								self.CrystalDimY.get(),self.CrystalDimZ.get(),self.CrystalPixPerMic.get())
		
		elif 'Using PDB code' in self.crystalAbsCoeffType.get():
			newCryst = crystals_pdbCode(MainGui.crystMakeName.get(),self.CrystalType.get(),self.CrystalDimX.get(),
										self.CrystalDimY.get(),self.CrystalDimZ.get(),self.CrystalPixPerMic.get(),
							 			self.pdbcode,self.solventHeavyConc)

		elif 'User defined composition' in self.crystalAbsCoeffType.get():
			newCryst = crystals_userDefined(MainGui.crystMakeName.get(),self.CrystalType.get(),self.CrystalDimX.get(),
											self.CrystalDimY.get(),self.CrystalDimZ.get(),self.CrystalPixPerMic.get(),
				 							self.unitcell_a,self.unitcell_b,self.unitcell_c,
				 							self.unitcell_alpha,self.unitcell_beta,self.unitcell_gamma,
				 							self.numMonomers,self.numResidues,self.numRNA,self.numDNA,
				 							self.proteinHeavyAtoms,self.solventHeavyConc,self.solventFraction)

		elif 'RADDOSE version 2' in self.crystalAbsCoeffType.get():
			newCryst = crystals_RADDOSEv2(MainGui.crystMakeName.get(),self.CrystalType.get(),self.CrystalDimX.get(),
										  self.CrystalDimY.get(),self.CrystalDimZ.get(),self.CrystalPixPerMic.get(),
				 						  self.unitcell_a,self.unitcell_b,self.unitcell_c,
				 						  self.unitcell_alpha,self.unitcell_beta,self.unitcell_gamma,
				 						  self.numMonomers,self.numResidues,self.numRNA,self.numDNA,
				 						  self.proteinHeavyAtoms,self.solventHeavyConc,self.solventFraction)

		elif 'using sequence file' in self.crystalAbsCoeffType.get():
			newCryst = crystals_seqFile(MainGui.crystMakeName.get(),self.CrystalType.get(),self.CrystalDimX.get(),
										self.CrystalDimY.get(),self.CrystalDimZ.get(),self.CrystalPixPerMic.get(),
										self.unitcell_a,self.unitcell_b,self.unitcell_c,
				 						self.unitcell_alpha,self.unitcell_beta,self.unitcell_gamma,
				 						self.numMonomers,self.sequenceFile,self.proteinHeavyAtoms,
				 						self.solventHeavyConc,self.solventFraction)

		elif 'SAXS (user defined composition)' in self.crystalAbsCoeffType.get():
			newCryst = crystals_SAXSuserDefined(MainGui.crystMakeName.get(),self.CrystalType.get(),self.CrystalDimX.get(),
												self.CrystalDimY.get(),self.CrystalDimZ.get(),self.CrystalPixPerMic.get(),
				 								self.unitcell_a,self.unitcell_b,self.unitcell_c,
				 								self.unitcell_alpha,self.unitcell_beta,self.unitcell_gamma,
				 								self.numResidues,self.numRNA,self.numDNA,
				 								self.proteinHeavyAtoms,self.solventHeavyConc,
				 								self.solventFraction,self.proteinConc)

		elif 'SAXS (sequence file)' in self.crystalAbsCoeffType.get():
			newCryst = crystals_SAXSseqFile(MainGui.crystMakeName.get(),self.CrystalType.get(),self.CrystalDimX.get(),
											self.CrystalDimY.get(),self.CrystalDimZ.get(),self.CrystalPixPerMic.get(),
											self.unitcell_a,self.unitcell_b,self.unitcell_c,
				 							self.unitcell_alpha,self.unitcell_beta,self.unitcell_gamma,
				 							self.proteinHeavyAtoms,self.solventHeavyConc,
				 							self.solventFraction,self.proteinConc,self.sequenceFile)

		# check the crystal parameters are valid
		ErrorMessage = MainGui.checkCrystInputs(newCryst)
		if ErrorMessage != "":
					tkMessageBox.showinfo("Invalid Input File",ErrorMessage)
		else:
			# add new crystal to list of loaded crystals
			MainGui.addCrystalToList(newCryst)

			# once this function runs, the toplevel window should be exited
			self.master.destroy()
