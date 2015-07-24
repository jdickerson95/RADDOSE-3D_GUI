from Tkinter import *
from ttk import *
from crystals import *
import tkMessageBox
import tkFileDialog
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

        # Crystal input --> default cuboid crystal dimension
        self.CrystalDimX,self.CrystalDimY,self.CrystalDimZ = StringVar(),StringVar(),StringVar()
        self.CrystalDimX.set("")
        self.CrystalDimY.set("")
        self.CrystalDimZ.set("")

        # Crystal input --> wireframe type and model file for a polyhedron crystal
        self.crystalWireFrameType, self.crystalModelFile, = StringVar(),StringVar(),
        self.crystalModelFile.set("")
        self.crystalWireFrameType.set("obj")
        self.crystalDimInputs(self.CrystalType)

        # Crystal input --> pixels per Micron
        self.CrystalPixPerMic = StringVar()
        self.CrystalPixPerMic.set("0.5")
        self.crystalPixPerMicInputs()

        # Crystal input --> Angle P and Angle L - these angles define the
        #orientation of the crystal with respect to the beam and rotation axis.
        self.crystalAngleP = StringVar()
        self.crystalAngleL = StringVar()
        self.crystalAngleP.set("0")
        self.crystalAngleL.set("0")
        self.crystalAngleInputs()

        #Crystal input --> Inputs for crystal composition. This is dependent on
        #Absorption Coefficient (AbsCoeff) type chosen
        self.pdbcode = StringVar()
        self.pdbcode.set("")
        self.unitcell_a = StringVar()
        self.unitcell_a.set("")
        self.unitcell_b = StringVar()
        self.unitcell_b.set("")
        self.unitcell_c = StringVar()
        self.unitcell_c.set("")
        self.unitcell_alpha = StringVar()
        self.unitcell_alpha.set("90")
        self.unitcell_beta = StringVar()
        self.unitcell_beta.set("90")
        self.unitcell_gamma = StringVar()
        self.unitcell_gamma.set("90")
        self.numMonomers =  StringVar()
        self.numMonomers.set("")
        self.numResidues = StringVar()
        self.numResidues.set("")
        self.numRNA = StringVar()
        self.numRNA.set("0")
        self.numDNA = StringVar()
        self.numDNA.set("0")
        self.proteinHeavyAtoms = StringVar()
        self.proteinHeavyAtoms.set("")
        self.solventHeavyConc = StringVar()
        self.solventHeavyConc.set("")
        self.solventFraction = StringVar()
        self.solventFraction.set("")
        self.proteinConc = StringVar()
        self.proteinConc.set("")
        self.sequenceFile = StringVar()
        self.sequenceFile.set("")
        self.crystalCompositionInputs(self.crystalAbsCoeffType)

        self.materialMixture = StringVar()
        self.materialMixture.set("")
        self.materialElements = StringVar()
        self.materialElements.set("")
        self.containerThickness = StringVar()
        self.containerThickness.set("")
        self.containerDensity = StringVar()
        self.containerDensity.set("")
        self.containerTypeInputs(self.containerType)

        # create a 'make' button here to add this crystal to the list of added crystals
        self.crystalMakeButton(MainGui)
        self.currentStrategyCrystal.grid_rowconfigure(0,weight=1)
        self.currentStrategyCrystal.grid_rowconfigure(1,weight=1)
        self.currentStrategyCrystal.grid_rowconfigure(2,weight=1)
        self.currentStrategyCrystal.grid_rowconfigure(3,weight=1)
        self.currentStrategyCrystal.grid_rowconfigure(4,weight=1)
        self.currentStrategyCrystal.grid_rowconfigure(5,weight=1)
        self.currentStrategyCrystal.grid_rowconfigure(6,weight=1)
        self.currentStrategyCrystal.grid_rowconfigure(7,weight=1)
        self.currentStrategyCrystal.grid_rowconfigure(8,weight=1)
        self.currentStrategyCrystal.grid_rowconfigure(9,weight=1)
        self.currentStrategyCrystal.grid_rowconfigure(10,weight=1)
        self.currentStrategyCrystal.grid_rowconfigure(11,weight=1)
        self.currentStrategyCrystal.grid_rowconfigure(12,weight=1)
        self.currentStrategyCrystal.grid_columnconfigure(0,weight=1)
        self.currentStrategyCrystal.grid_columnconfigure(1,weight=1)
        self.currentStrategyCrystal.grid_columnconfigure(2,weight=1)
        self.currentStrategyCrystal.grid_columnconfigure(3,weight=1)

    def crystalTypeInputs(self,MainGui):
        # Crystal input 1 --> crystal type
        CrystalinputLabel1 = Label(self.currentStrategyCrystal,text="Crystal Type",style="inputBoxes.TLabel")
        CrystalinputLabel1.grid(row=0,column=0,sticky=E,pady=5,padx=6)
        self.crystTypeDict = {'Cuboid'      : "Cuboid",
                              'Spherical'   : "Spherical",
                              'Cylindrical' : "Cylindrical",
                              'Polyhedron'  : "Polyhedron"}
        crystTypeList = self.crystTypeDict.keys()
        crystTypeOptionMenu = OptionMenu(self.currentStrategyCrystal, self.CrystalType, self.CrystalType.get(),*crystTypeList, command= lambda x: self.update(self.CrystalType,self.crystalAbsCoeffType,self.containerType,MainGui))
        crystTypeOptionMenu.grid(row=0,column=1,sticky=W,pady=5,padx=6)
        self.hoverType = HoverInfo(CrystalinputLabel1, self.helpText.typeText)

    def crystalDimInputs(self,crystTypeValue):
        # Crystal input 2 --> crystal dimensions
        if crystTypeValue.get() in ('Cuboid','Spherical','Cylindrical'):

            CrystalinputLabel2 = Label(self.currentStrategyCrystal,text="Crystal Dimensions:",style="inputBoxes.TLabel")
            CrystalinputLabel2.grid(row=0,column=2,sticky=E,pady=5,padx=6)
            self.hoverDims = HoverInfo(CrystalinputLabel2, self.helpText.dimsText)

            self.CrystalDimsInputsFrame = Frame(self.currentStrategyCrystal,style="inputBoxes.TFrame")
            self.CrystalDimsInputsFrame.grid(row=0,column=3,sticky=W,pady=5,padx=6)

            if crystTypeValue.get() == 'Cuboid':
                CrystalDimXLabel = Label(self.CrystalDimsInputsFrame,text="x = ",style="inputBoxes.TLabel")
                CrystalDimXLabel.grid(row=0,column=0,sticky=E,pady=5,padx=6)
                CrystalinputBox2X = Entry(self.CrystalDimsInputsFrame,textvariable=self.CrystalDimX,width=5)
                CrystalinputBox2X.grid(row=0,column=1,sticky=W+E,pady=5,padx=6)
                CrystalDimYLabel = Label(self.CrystalDimsInputsFrame,text="y = ",style="inputBoxes.TLabel")
                CrystalDimYLabel.grid(row=0,column=2,sticky=E,pady=5,padx=6)
                CrystalinputBox2Y = Entry(self.CrystalDimsInputsFrame,textvariable=self.CrystalDimY,width=5)
                CrystalinputBox2Y.grid(row=0,column=3,sticky=W+E,pady=5,padx=6)
                CrystalDimZLabel = Label(self.CrystalDimsInputsFrame,text="z = ",style="inputBoxes.TLabel")
                CrystalDimZLabel.grid(row=0,column=4,sticky=E,pady=5,padx=6)
                CrystalinputBox2Z = Entry(self.CrystalDimsInputsFrame,textvariable=self.CrystalDimZ,width=5)
                CrystalinputBox2Z.grid(row=0,column=5,sticky=W+E,pady=5,padx=6)
                self.CrystalDimsInputsFrame.grid_rowconfigure(0,weight=1)
                self.CrystalDimsInputsFrame.grid_columnconfigure(0,weight=1)
                self.CrystalDimsInputsFrame.grid_columnconfigure(1,weight=1)
                self.CrystalDimsInputsFrame.grid_columnconfigure(2,weight=1)
                self.CrystalDimsInputsFrame.grid_columnconfigure(3,weight=1)
                self.CrystalDimsInputsFrame.grid_columnconfigure(4,weight=1)
                self.CrystalDimsInputsFrame.grid_columnconfigure(5,weight=1)

            elif crystTypeValue.get() == 'Spherical':
                CrystalDimXLabel = Label(self.CrystalDimsInputsFrame,text="Diameter = ",style="inputBoxes.TLabel")
                CrystalDimXLabel.grid(row=0,column=0,sticky=E,pady=5,padx=6)
                CrystalinputBox2X = Entry(self.CrystalDimsInputsFrame,textvariable=self.CrystalDimX,width=5)
                CrystalinputBox2X.grid(row=0,column=1,sticky=W+E,pady=5,padx=6)
                self.CrystalDimsInputsFrame.grid_rowconfigure(0,weight=1)
                self.CrystalDimsInputsFrame.grid_columnconfigure(0,weight=1)
                self.CrystalDimsInputsFrame.grid_columnconfigure(1,weight=1)

            elif crystTypeValue.get() == 'Cylindrical':
                CrystalDimXLabel = Label(self.CrystalDimsInputsFrame,text="Diameter = ",style="inputBoxes.TLabel")
                CrystalDimXLabel.grid(row=0,column=0,sticky=E,pady=5,padx=6)
                CrystalinputBox2X = Entry(self.CrystalDimsInputsFrame,textvariable=self.CrystalDimX,width=5)
                CrystalinputBox2X.grid(row=0,column=1,sticky=W+E,pady=5,padx=6)
                CrystalDimYLabel = Label(self.CrystalDimsInputsFrame,text="Height = ",style="inputBoxes.TLabel")
                CrystalDimYLabel.grid(row=0,column=2,sticky=E,pady=5,padx=6)
                CrystalinputBox2Y = Entry(self.CrystalDimsInputsFrame,textvariable=self.CrystalDimY,width=5)
                CrystalinputBox2Y.grid(row=0,column=3,sticky=W+E,pady=5,padx=6)
                self.CrystalDimsInputsFrame.grid_rowconfigure(0,weight=1)
                self.CrystalDimsInputsFrame.grid_columnconfigure(0,weight=1)
                self.CrystalDimsInputsFrame.grid_columnconfigure(1,weight=1)
                self.CrystalDimsInputsFrame.grid_columnconfigure(2,weight=1)
                self.CrystalDimsInputsFrame.grid_columnconfigure(3,weight=1)

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
            inputsFrame = Frame(self.currentStrategyCrystal,style="inputBoxes.TFrame")
            inputsFrame.grid(row=0,column=3,sticky=W,pady=5,padx=6)
            inputLoadBox = Entry(inputsFrame,textvariable=self.crystalModelFile)
            inputLoadBox.grid(row=0, column=0,columnspan=2,pady=5,sticky=W+E)
            addInputButton = Button(inputsFrame,text="Find File",command= lambda: self.clickInputLoad(inputLoadBox))
            addInputButton.grid(row=0, column=2,pady=5,padx=6,sticky=W+E)
            inputsFrame.grid_rowconfigure(0,weight=1)
            inputsFrame.grid_columnconfigure(0,weight=1)
            inputsFrame.grid_columnconfigure(1,weight=1)
            inputsFrame.grid_columnconfigure(2,weight=1)

        #Set the input boxes to their current values
        self.CrystalDimX.set(self.CrystalDimX.get())
        self.CrystalDimY.set(self.CrystalDimY.get())
        self.CrystalDimZ.set(self.CrystalDimZ.get())
        self.crystalModelFile.set(self.crystalModelFile.get())

    def crystalPixPerMicInputs(self):
        # Crystal input 3 --> pixels per Micron
        CrystalinputLabel3 = Label(self.currentStrategyCrystal,text="Pixels per Micron",style="inputBoxes.TLabel")
        CrystalinputLabel3.grid(row=1,column=0,sticky=E,pady=5,padx=6)
        self.hoverPix = HoverInfo(CrystalinputLabel3, self.helpText.pixPerMicText)
        CrystalinputBox3 = Entry(self.currentStrategyCrystal,textvariable=self.CrystalPixPerMic,width=5)
        CrystalinputBox3.grid(row=1,column=1,sticky=W,pady=5,padx=6)
        self.CrystalPixPerMic.set(self.CrystalPixPerMic.get())

    def crystalAngleInputs(self):
        CrystalAnglePLabel = Label(self.currentStrategyCrystal,text="Angle P = ",style="inputBoxes.TLabel")
        CrystalAnglePLabel.grid(row=1,column=2,sticky=E,pady=5,padx=6)
        self.hoverAngP = HoverInfo(CrystalAnglePLabel, self.helpText.anglePText)
        CrystalAnglePInputBox = Entry(self.currentStrategyCrystal,textvariable=self.crystalAngleP,width=5)
        CrystalAnglePInputBox.grid(row=1,column=3,sticky=W,pady=5,padx=6)
        self.crystalAngleP.set(self.crystalAngleP.get())

        CrystalAngleLLabel = Label(self.currentStrategyCrystal,text="Angle L = ",style="inputBoxes.TLabel")
        CrystalAngleLLabel.grid(row=2,column=2,sticky=E,pady=5,padx=6)
        self.hoverAngL = HoverInfo(CrystalAngleLLabel, self.helpText.angleLText)
        CrystalAnglePInputBox = Entry(self.currentStrategyCrystal,textvariable=self.crystalAngleL,width=5)
        CrystalAnglePInputBox.grid(row=2,column=3,sticky=W,pady=5,padx=6)
        self.crystalAngleL.set(self.crystalAngleL.get())

    def crystalAbsCoeffTypeInputs(self, MainGui):
        # Crystal input 4 --> absorption coefficient
        CrystalinputLabel4 = Label(self.currentStrategyCrystal,text="Absorption Coefficient",style="inputBoxes.TLabel")
        CrystalinputLabel4.grid(row=3,column=0,sticky=E,pady=5,padx=6)
        self.hoverAbsCoeff = HoverInfo(CrystalinputLabel4, self.helpText.absCoeffText)
        self.crystAbsCoeffDict = {'Average protein composition'     : "Average",
                                  'Using PDB code'                  : "EXP",
                                  'User defined composition'        : "RD3D",
                                  'RADDOSE version 2'               : "RDV2",
                                   'using sequence file'             : "Sequence",
                                  'SAXS (user defined composition)' : "SAXS",
                                  'SAXS (sequence file)'            : "SAXSseq"}
        crystAbsCoeffList = self.crystAbsCoeffDict.keys()
        crystAbsCoeffOptionMenu = OptionMenu(self.currentStrategyCrystal, self.crystalAbsCoeffType, self.crystalAbsCoeffType.get(), *crystAbsCoeffList, command= lambda x: self.update(self.CrystalType,self.crystalAbsCoeffType,self.containerType,MainGui))
        crystAbsCoeffOptionMenu.grid(row=3,column=1,sticky=W,pady=5,padx=6)

    def crystalCompositionInputs(self, absCoeffTypeValue):

        if 'Using PDB code' in absCoeffTypeValue.get():
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
            #Configure the row and columns for the unit cell inputs frame
            self.UnitcellInputsFrame.grid_rowconfigure(0,weight=1)
            self.UnitcellInputsFrame.grid_rowconfigure(1,weight=1)
            self.UnitcellInputsFrame.grid_rowconfigure(2,weight=1)
            self.UnitcellInputsFrame.grid_columnconfigure(0,weight=1)
            self.UnitcellInputsFrame.grid_columnconfigure(1,weight=1)
            self.UnitcellInputsFrame.grid_columnconfigure(2,weight=1)
            self.UnitcellInputsFrame.grid_columnconfigure(3,weight=1)

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
            #Configure the row and columns for the unit cell inputs frame
            self.UnitcellInputsFrame.grid_rowconfigure(0,weight=1)
            self.UnitcellInputsFrame.grid_rowconfigure(1,weight=1)
            self.UnitcellInputsFrame.grid_rowconfigure(2,weight=1)
            self.UnitcellInputsFrame.grid_columnconfigure(0,weight=1)
            self.UnitcellInputsFrame.grid_columnconfigure(1,weight=1)
            self.UnitcellInputsFrame.grid_columnconfigure(2,weight=1)
            self.UnitcellInputsFrame.grid_columnconfigure(3,weight=1)

        elif 'using sequence file' in absCoeffTypeValue.get():
            CrystalNumMonLabel = Label(self.currentStrategyCrystal,text="Number of monomers",style="inputBoxes.TLabel")
            CrystalNumMonLabel.grid(row=4,column=0,sticky=E,pady=5,padx=6)
            self.hoverNumMon = HoverInfo(CrystalNumMonLabel, self.helpText.numMonText)
            CrystalNumMonInputBox = Entry(self.currentStrategyCrystal,textvariable=self.numMonomers,width=14)
            CrystalNumMonInputBox.grid(row=4,column=1,sticky=W,pady=5,padx=6)

            CrystalSeqResLabel = Label(self.currentStrategyCrystal,text="Sequence file",style="inputBoxes.TLabel")
            CrystalSeqResLabel.grid(row=4,column=2,sticky=E,pady=5,padx=6)
            self.hoverSeqRes = HoverInfo(CrystalSeqResLabel, self.helpText.seqFileText)
            inputsFrame = Frame(self.currentStrategyCrystal,style="inputBoxes.TFrame")
            inputsFrame.grid(row=4,column=3,sticky=W,pady=5,padx=6)
            inputLoadBox = Entry(inputsFrame,textvariable=self.sequenceFile)
            inputLoadBox.grid(row=0, column=0,columnspan=2,pady=5,sticky=W+E)
            addInputButton = Button(inputsFrame,text="Find File",command= lambda: self.clickInputLoad(inputLoadBox))
            addInputButton.grid(row=0, column=2,pady=5,padx=6,sticky=W+E)
            inputsFrame.grid_rowconfigure(0,weight=1)
            inputsFrame.grid_columnconfigure(0,weight=1)
            inputsFrame.grid_columnconfigure(1,weight=1)
            inputsFrame.grid_columnconfigure(2,weight=1)

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
            #Configure the row and columns for the unit cell inputs frame
            self.UnitcellInputsFrame.grid_rowconfigure(0,weight=1)
            self.UnitcellInputsFrame.grid_rowconfigure(1,weight=1)
            self.UnitcellInputsFrame.grid_rowconfigure(2,weight=1)
            self.UnitcellInputsFrame.grid_columnconfigure(0,weight=1)
            self.UnitcellInputsFrame.grid_columnconfigure(1,weight=1)
            self.UnitcellInputsFrame.grid_columnconfigure(2,weight=1)
            self.UnitcellInputsFrame.grid_columnconfigure(3,weight=1)

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
            #Configure the row and columns for the unit cell inputs frame
            self.UnitcellInputsFrame.grid_rowconfigure(0,weight=1)
            self.UnitcellInputsFrame.grid_rowconfigure(1,weight=1)
            self.UnitcellInputsFrame.grid_rowconfigure(2,weight=1)
            self.UnitcellInputsFrame.grid_columnconfigure(0,weight=1)
            self.UnitcellInputsFrame.grid_columnconfigure(1,weight=1)
            self.UnitcellInputsFrame.grid_columnconfigure(2,weight=1)
            self.UnitcellInputsFrame.grid_columnconfigure(3,weight=1)

        elif 'SAXS (sequence file)' in absCoeffTypeValue.get():
            CrystalProtConcLabel = Label(self.currentStrategyCrystal,text="Protein concentration",style="inputBoxes.TLabel")
            CrystalProtConcLabel.grid(row=4,column=0,sticky=E,pady=5,padx=6)
            self.hoverProtConc = HoverInfo(CrystalProtConcLabel, self.helpText.protConcText)
            CrystalNumMonInputBox = Entry(self.currentStrategyCrystal,textvariable=self.proteinConc,width=14)
            CrystalNumMonInputBox.grid(row=4,column=1,sticky=W,pady=5,padx=6)

            CrystalSeqResLabel = Label(self.currentStrategyCrystal,text="Sequence file",style="inputBoxes.TLabel")
            CrystalSeqResLabel.grid(row=4,column=2,sticky=E,pady=5,padx=6)
            self.hoverSeqRes = HoverInfo(CrystalSeqResLabel, self.helpText.seqFileText)
            inputsFrame = Frame(self.currentStrategyCrystal,style="inputBoxes.TFrame")
            inputsFrame.grid(row=4,column=3,sticky=W,pady=5,padx=6)
            inputLoadBox = Entry(inputsFrame,textvariable=self.sequenceFile)
            inputLoadBox.grid(row=0, column=0,columnspan=2,pady=5,sticky=W+E)
            addInputButton = Button(inputsFrame,text="Find File",command= lambda: self.clickInputLoad(inputLoadBox))
            addInputButton.grid(row=0, column=2,pady=5,padx=6,sticky=W+E)
            inputsFrame.grid_rowconfigure(0,weight=1)
            inputsFrame.grid_columnconfigure(0,weight=1)
            inputsFrame.grid_columnconfigure(1,weight=1)
            inputsFrame.grid_columnconfigure(2,weight=1)

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

            #Configure the row and columns for the unit cell inputs frame
            self.UnitcellInputsFrame.grid_rowconfigure(0,weight=1)
            self.UnitcellInputsFrame.grid_rowconfigure(1,weight=1)
            self.UnitcellInputsFrame.grid_rowconfigure(2,weight=1)
            self.UnitcellInputsFrame.grid_columnconfigure(0,weight=1)
            self.UnitcellInputsFrame.grid_columnconfigure(1,weight=1)
            self.UnitcellInputsFrame.grid_columnconfigure(2,weight=1)
            self.UnitcellInputsFrame.grid_columnconfigure(3,weight=1)

        #Set the input boxes to their current values
        self.pdbcode.set(self.pdbcode.get())
        self.unitcell_a.set(self.unitcell_a.get())
        self.unitcell_b.set(self.unitcell_b.get())
        self.unitcell_c.set(self.unitcell_c.get())
        self.unitcell_alpha.set(self.unitcell_alpha.get())
        self.unitcell_beta.set(self.unitcell_beta.get())
        self.unitcell_gamma.set(self.unitcell_gamma.get())
        self.numMonomers.set(self.numMonomers.get())
        self.numResidues.set(self.numResidues.get())
        self.numRNA.set(self.numRNA.get())
        self.numRNA.set(self.numDNA.get())
        self.proteinHeavyAtoms.set(self.proteinHeavyAtoms.get())
        self.solventHeavyConc.set(self.solventHeavyConc.get())
        self.solventFraction.set(self.solventFraction.get())
        self.proteinConc.set(self.proteinConc.get())
        self.sequenceFile.set(self.sequenceFile.get())

    def sampleContainerTypeInputs(self, MainGui):
        # Crystal input  --> Sample container type
        containerTypeInputLabel = Label(self.currentStrategyCrystal,text="Type of sample container",style="inputBoxes.TLabel")
        containerTypeInputLabel.grid(row=9,column=0,sticky=E,pady=5,padx=6)
        self.hoverConType = HoverInfo(containerTypeInputLabel, self.helpText.conTypeText)
        self.containerTypeDict = {'No container'                  : "None",
                                  'Specify mixture'               : "Mixture",
                                  'Specify elemental composition' : "Elemental"}
        containerTypeList = self.containerTypeDict.keys()
        containerTypeOptionMenu = OptionMenu(self.currentStrategyCrystal, self.containerType, self.containerType.get(), *containerTypeList, command= lambda x: self.update(self.CrystalType,self.crystalAbsCoeffType,self.containerType,MainGui))
        containerTypeOptionMenu.grid(row=9,column=1,sticky=W,pady=5,padx=6)

    def containerTypeInputs(self, containerTypeValue):

        if 'Specify mixture' in containerTypeValue.get():
            containerMixtureLabel = Label(self.currentStrategyCrystal,text="Mixture",style="inputBoxes.TLabel")
            containerMixtureLabel.grid(row=10,column=0,sticky=E,pady=5,padx=6)
            self.hoverConMix = HoverInfo(containerMixtureLabel, self.helpText.conMixText)
            self.mixtureDict = {'A-150 Tissue-Equivalent Plastic' : "a150",
                                'Adipose Tissue (ICRU-44)' : "adipose",
                                'Dry Air (near sea level)': "air",
                                'Alanine' : "alanine",
                                'Bakelite' : "bakelite",
                                'Blood, Whole (ICRU-44)': "blood",
                                'Bone, Cortical (ICRU-44)':"bone",
                                'B-100 Bone-Equivalent Plastic':"b100",
                                'Brain, Grey/White Matter (ICRU-44)':"brain",
                                'Breast Tissue (ICRU-44)':"breast",
                                'C-552 Air-equivalent Plastic':"c552",
                                'Cadmium Telluride':"telluride",
                                'Calcium Fluoride':"fluoride",
                                'Calcium Sulfate':"calcium",
                                '15 mmol L-1 Ceric Ammonium Sulfate Solution':'ceric',
                                'Cesium Iodide':"cesium",
                                'Ordinary Concrete':"concrete",
                                'Barite Concrete (Type BA)':"concreteba",
                                'Eye Lens (ICRU-44)':"eye",
                                'Standard Fricke Ferrous Sulfate':"fricke",
                                'Gadolinium Oxysulfide':"gadolinium",
                                'Gafchromic Sensor':"gafchromic",
                                'Gallium Arsenide':"gallium",
                                'Pyrex (Borosilicate Glass)':"pyrex",
                                'Lead Glass':"glass",
                                'Lithium Fluoride':"lithiumflu",
                                'Lithium Tetraborate':"lithium",
                                'Lung Tissue (ICRU-44)':"lung",
                                'Magnesium Tetroborate':"magnesium",
                                'Mercuric Iodide':"mercuric",
                                'Muscle, Skeletal (ICRU-44)':"muscle",
                                'Ovary (ICRU-44)':"ovary",
                                'Photographic Emulsion, Kodak Type AA':"kodak",
                                'Photographic Emulsion, Standard Nuclear':"photoemul",
                                'Plastic Scintillator, Vinyltoluene':"vinyl",
                                'Polyethylene':"polyethylene",
                                'Mylar (Polyethylene Terephthalate)':"mylar",
                                'Polymethyl Methacrylate':"pmma",
                                'Polystyrene':"polystyrene",
                                'Teflon (Polytetrafluoroethylene)':"teflon",
                                'Polyvinyl Chloride':"polyvinyl",
                                'Radiochromic Dye Film, Nylon Base':"nylonfilm",
                                'Testis (ICRU-44)':"testis",
                                'Tissue, Soft (ICRU-44)':"tissue",
                                'Tissue, Soft (ICRU Four-Component)':"tissue4",
                                'Tissue-Equivalent Gas, Methane Based':"temethane",
                                'Tissue-Equivalent Gas, Propane Based':"tepropane",
                                'Liquid Water':"water"}

            self.materialMixture.set('Dry Air (near sea level)') # set initial material here
            containerMixtureOptionMenu = OptionMenu(self.currentStrategyCrystal,self.materialMixture, self.materialMixture.get(), *self.mixtureDict.keys())
            containerMixtureOptionMenu.grid(row=10,column=1,columnspan=2,sticky=W,pady=5,padx=6)

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

        #Set input boxes to their corresponding current values
        self.materialMixture.set(self.materialMixture.get())
        self.materialElements.set(self.materialElements.get())
        self.containerThickness.set(self.containerThickness.get())
        self.containerDensity.set(self.containerDensity.get())

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

    def clickInputLoad(self,inputBox):
        """Load a pre-made file

        Function to allow file search and load of a pre-made input file

        =================
        Keyword arguments
        =================
        inputBox:
            The input text box that should be populated with the file path once
            a file is selected.

        =================
        Return parameters
        =================
        No explicit return parameters

        """
        self.inputLoad = tkFileDialog.askopenfilename(parent=self.master,title='Load input file')
        inputBox.delete(0,END)
        inputBox.insert(0,self.inputLoad)

    def addMadeCryst(self,MainGui):
        # make a new crystal object from above entered parameters and add to both listbox crystal list and
        # also list of crystal objects

        # first create dictionary for container info
        self.containerInfoDict = {}
        if self.containerTypeDict[self.containerType.get()] == 'Mixture':
            self.containerInfoDict["Type"] = self.containerTypeDict[self.containerType.get()]
            self.containerInfoDict["Mixture"] = self.mixtureDict[self.materialMixture.get()]
            self.containerInfoDict["Thickness"] = self.containerThickness.get()
            self.containerInfoDict["Density"] = self.containerDensity.get()

        elif self.containerTypeDict[self.containerType.get()] == 'Elemental':
            self.containerInfoDict["Type"] = self.containerTypeDict[self.containerType.get()]
            self.containerInfoDict["Elements"] = self.materialElements.get()
            self.containerInfoDict["Thickness"] = self.containerThickness.get()
            self.containerInfoDict["Density"] = self.containerDensity.get()

        ########################################################################################
        #Check if files exist before adding them
        allFilesExist = True
        possibleFiles = [self.crystalModelFile.get(), self.sequenceFile.get()]
        for eachFile in possibleFiles:
            if eachFile:
                if not os.path.isfile(eachFile):
                    allFilesExist = False
        ########################################################################################

        # make a new crystal object with class determined by absCoefCalc input type
        if 'Average protein composition' in self.crystalAbsCoeffType.get():
            newCryst = crystals(MainGui.crystMakeName.get(),self.crystTypeDict[self.CrystalType.get()],
                                self.CrystalDimX.get(),self.CrystalDimY.get(),self.CrystalDimZ.get(),
                                self.CrystalPixPerMic.get(),self.crystalAngleP.get(),self.crystalAngleL.get(),
                                self.containerInfoDict,self.crystAbsCoeffDict[self.crystalAbsCoeffType.get()],
                                self.crystalModelFile.get())

        elif 'Using PDB code' in self.crystalAbsCoeffType.get():
            newCryst = crystals_pdbCode(MainGui.crystMakeName.get(),self.CrystalType.get(),self.CrystalDimX.get(),
                                        self.CrystalDimY.get(),self.CrystalDimZ.get(),self.CrystalPixPerMic.get(),
                                        self.crystalAngleP.get(),self.crystalAngleL.get(),self.containerInfoDict,
                                        self.crystAbsCoeffDict[self.crystalAbsCoeffType.get()],self.crystalModelFile.get(),
                                        self.pdbcode.get(),self.solventHeavyConc.get())

        elif 'User defined composition' in self.crystalAbsCoeffType.get():
            newCryst = crystals_userDefined(MainGui.crystMakeName.get(),self.CrystalType.get(),self.CrystalDimX.get(),
                                            self.CrystalDimY.get(),self.CrystalDimZ.get(),self.CrystalPixPerMic.get(),
                                            self.crystalAngleP.get(),self.crystalAngleL.get(),self.containerInfoDict,
                                            self.crystAbsCoeffDict[self.crystalAbsCoeffType.get()],self.crystalModelFile.get(),
                                            self.unitcell_a.get(),self.unitcell_b.get(),self.unitcell_c.get(),
                                            self.unitcell_alpha.get(),self.unitcell_beta.get(),self.unitcell_gamma.get(),
                                            self.numMonomers.get(),self.numResidues.get(),self.numRNA.get(),self.numDNA.get(),
                                            self.proteinHeavyAtoms.get(),self.solventHeavyConc.get(),self.solventFraction.get())

        elif 'RADDOSE version 2' in self.crystalAbsCoeffType.get():
            newCryst = crystals_RADDOSEv2(MainGui.crystMakeName.get(),self.CrystalType.get(),self.CrystalDimX.get(),
                                            self.CrystalDimY.get(),self.CrystalDimZ.get(),self.CrystalPixPerMic.get(),
                                            self.crystalAngleP.get(),self.crystalAngleL.get(),self.containerInfoDict,
                                            self.crystAbsCoeffDict[self.crystalAbsCoeffType.get()],self.crystalModelFile.get(),
                                            self.unitcell_a.get(),self.unitcell_b.get(),self.unitcell_c.get(),
                                            self.unitcell_alpha.get(),self.unitcell_beta.get(),self.unitcell_gamma.get(),
                                            self.numMonomers.get(),self.numResidues.get(),self.numRNA.get(),self.numDNA.get(),
                                            self.proteinHeavyAtoms,self.solventHeavyConc.get(),self.solventFraction.get())

        elif 'using sequence file' in self.crystalAbsCoeffType.get():
            newCryst = crystals_seqFile(MainGui.crystMakeName.get(),self.CrystalType.get(),self.CrystalDimX.get(),
                                        self.CrystalDimY.get(),self.CrystalDimZ.get(),self.CrystalPixPerMic.get(),
                                        self.crystalAngleP.get(),self.crystalAngleL.get(),self.containerInfoDict,
                                        self.crystAbsCoeffDict[self.crystalAbsCoeffType.get()],self.crystalModelFile.get(),
                                        self.unitcell_a.get(),self.unitcell_b.get(),self.unitcell_c.get(),
                                        self.unitcell_alpha.get(),self.unitcell_beta.get(),self.unitcell_gamma.get(),
                                        self.numMonomers.get(),self.sequenceFile.get(),self.proteinHeavyAtoms.get(),
                                        self.solventHeavyConc.get(),self.solventFraction.get())

        elif 'SAXS (user defined composition)' in self.crystalAbsCoeffType.get():
            newCryst = crystals_SAXSuserDefined(MainGui.crystMakeName.get(),self.CrystalType.get(),self.CrystalDimX.get(),
                                                self.CrystalDimY.get(),self.CrystalDimZ.get(),self.CrystalPixPerMic.get(),
                                                self.crystalAngleP.get(),self.crystalAngleL.get(),self.containerInfoDict,
                                                self.crystAbsCoeffDict[self.crystalAbsCoeffType.get()],self.crystalModelFile.get(),
                                                self.unitcell_a.get(),self.unitcell_b.get(),self.unitcell_c.get(),
                                                self.unitcell_alpha.get(),self.unitcell_beta.get(),self.unitcell_gamma.get(),
                                                self.numResidues.get(),self.numRNA.get(),self.numDNA.get(),
                                                self.proteinHeavyAtoms.get(),self.solventHeavyConc.get(),
                                                self.solventFraction.get(),self.proteinConc.get())

        elif 'SAXS (sequence file)' in self.crystalAbsCoeffType.get():
            newCryst = crystals_SAXSseqFile(MainGui.crystMakeName.get(),self.CrystalType.get(),self.CrystalDimX.get(),
                                            self.CrystalDimY.get(),self.CrystalDimZ.get(),self.CrystalPixPerMic.get(),
                                            self.crystalAngleP.get(),self.crystalAngleL.get(),self.containerInfoDict,
                                            self.crystAbsCoeffDict[self.crystalAbsCoeffType.get()],self.crystalModelFile.get(),
                                            self.unitcell_a.get(),self.unitcell_b.get(),self.unitcell_c.get(),
                                            self.unitcell_alpha.get(),self.unitcell_beta.get(),self.unitcell_gamma.get(),
                                            self.proteinHeavyAtoms.get(),self.solventHeavyConc.get(),
                                            self.solventFraction.get(),self.proteinConc.get(),self.sequenceFile.get())

        # update dimensions of crystal depending on crystal type specified
        newCryst.setDimsByCrystType()

        # check the crystal parameters are valid
        ErrorMessage = MainGui.checkCrystInputs(newCryst)
        if ErrorMessage != "":
                    tkMessageBox.showinfo("Invalid Input File",ErrorMessage)
        elif not allFilesExist:
            string = """At least one of the files specified does not exist.
        Please check the file names given in the input boxes and make sure they exist.
        """ %()
            tkMessageBox.showinfo( "No Experiment Name", string)
        else:
            # add new crystal to list of loaded crystals
            MainGui.addCrystalToList(newCryst)

            # give warning if identical crystal already loaded
            warningMessage = MainGui.checkRepeatedCryst(newCryst)
            if warningMessage != "":
                tkMessageBox.showinfo("Warning",warningMessage)

            # once this function runs, the toplevel window should be exited
            self.master.destroy()
