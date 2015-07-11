from Tkinter import *
from ttk import *
import tkFileDialog
from HoverInfo import HoverInfo
from InputsHelpText import PremadeInputHelp

class PremadeInputMakerWindow():

    def __init__(self, MainGui):
        self.master = MainGui.top_premadeRunMaker
        self.premadeMakerFrame = Frame(self.master)
        self.premadeMakerFrame.pack()
        self.lightcolour = MainGui.lightcolour
        self.darkcolour = MainGui.darkcolour

        # Wedge inputs here:
        l = Label(self.master,text="Premade Input Files",style="labelFrameTitle.TLabel")
        self.inputsFrame = LabelFrame(self.master,labelwidget=l,style="MakeABeam.TFrame")
        self.inputsFrame.pack(side=TOP,padx=10, pady=10,fill=BOTH,expand=TRUE)

        #Create object that contains the help text
        self.helpText = PremadeInputHelp()

        self.rd3dInputFile = StringVar()
        self.rd3dinputFileSection()

        self.sampleModelFile = StringVar()
        self.sampleModelFileInput()

        self.sequenceFile = StringVar()
        self.sequenceFileInput()

        self.beamImageFile = StringVar()
        self.beamImageFileInput()

        self.beamApertureXFile = StringVar()
        self.beamApertureXFileInput()

        self.beamApertureYFile = StringVar()
        self.beamApertureYFileInput()

        self.expNameInput = StringVar()
        self.expNameInputSection(MainGui)

        self.inputsFrame.grid_rowconfigure(0,weight=1)
        self.inputsFrame.grid_rowconfigure(1,weight=1)
        self.inputsFrame.grid_rowconfigure(2,weight=1)
        self.inputsFrame.grid_rowconfigure(3,weight=1)
        self.inputsFrame.grid_rowconfigure(4,weight=1)
        self.inputsFrame.grid_rowconfigure(5,weight=1)
        self.inputsFrame.grid_rowconfigure(6,weight=1)
        self.inputsFrame.grid_columnconfigure(0,weight=1)
        self.inputsFrame.grid_columnconfigure(1,weight=1)
        self.inputsFrame.grid_columnconfigure(2,weight=1)
        self.inputsFrame.grid_columnconfigure(3,weight=1)
        self.inputsFrame.grid_columnconfigure(4,weight=1)
        self.inputsFrame.grid_columnconfigure(5,weight=1)
        self.inputsFrame.grid_columnconfigure(6,weight=1)

    def rd3dinputFileSection(self):
        # add RD3D input file 'load' option to runPremadeRD3DStrategyFrame frame here
        loadLabel = Label(self.inputsFrame,text="RADDOSE-3D input file load",style="inputBoxes.TLabel")
        loadLabel.grid(row=0, column=0,pady=5,padx=6,sticky=W+E)
        HoverInfo(loadLabel, self.helpText.inputFileText)
        inputLoadBox = Entry(self.inputsFrame,textvariable=self.rd3dInputFile)
        inputLoadBox.grid(row=0, column=1,columnspan=5,pady=5,sticky=W+E)
        addInputButton = Button(self.inputsFrame,text="Find File",command= lambda: self.clickInputLoad(inputLoadBox))
        addInputButton.grid(row=0, column=6,pady=5,padx=6,sticky=W+E)

    def sampleModelFileInput(self):
        loadLabel = Label(self.inputsFrame,text="Sample geometry file load",style="inputBoxes.TLabel")
        loadLabel.grid(row=1, column=0,pady=5,padx=6,sticky=W+E)
        HoverInfo(loadLabel, self.helpText.sampleGeomText)
        inputLoadBox = Entry(self.inputsFrame,textvariable=self.sampleModelFile)
        inputLoadBox.grid(row=1, column=1,columnspan=5,pady=5,sticky=W+E)
        addInputButton = Button(self.inputsFrame,text="Find File",command= lambda: self.clickInputLoad(inputLoadBox))
        addInputButton.grid(row=1, column=6,pady=5,padx=6,sticky=W+E)

    def sequenceFileInput(self):
        loadLabel = Label(self.inputsFrame,text="Sequence file load",style="inputBoxes.TLabel")
        loadLabel.grid(row=2, column=0,pady=5,padx=6,sticky=W+E)
        HoverInfo(loadLabel, self.helpText.sequenceFileText)
        inputLoadBox = Entry(self.inputsFrame,textvariable=self.sequenceFile)
        inputLoadBox.grid(row=2, column=1,columnspan=5,pady=5,sticky=W+E)
        addInputButton = Button(self.inputsFrame,text="Find File",command= lambda: self.clickInputLoad(inputLoadBox))
        addInputButton.grid(row=2, column=6,pady=5,padx=6,sticky=W+E)

    def beamImageFileInput(self):
        loadLabel = Label(self.inputsFrame,text="Beam image file load",style="inputBoxes.TLabel")
        loadLabel.grid(row=3, column=0,pady=5,padx=6,sticky=W+E)
        HoverInfo(loadLabel, self.helpText.beamImageText)
        inputLoadBox = Entry(self.inputsFrame,textvariable=self.beamImageFile)
        inputLoadBox.grid(row=3, column=1,columnspan=5,pady=5,sticky=W+E)
        addInputButton = Button(self.inputsFrame,text="Find File",command= lambda: self.clickInputLoad(inputLoadBox))
        addInputButton.grid(row=3, column=6,pady=5,padx=6,sticky=W+E)

    def beamApertureXFileInput(self):
        loadLabel = Label(self.inputsFrame,text="Beam aperture measurements (Horizontal)",style="inputBoxes.TLabel")
        loadLabel.grid(row=4, column=0,pady=5,padx=6,sticky=W+E)
        HoverInfo(loadLabel, self.helpText.beamApXText)
        inputLoadBox = Entry(self.inputsFrame,textvariable=self.beamApertureXFile)
        inputLoadBox.grid(row=4, column=1,columnspan=5,pady=5,sticky=W+E)
        addInputButton = Button(self.inputsFrame,text="Find File",command= lambda: self.clickInputLoad(inputLoadBox))
        addInputButton.grid(row=4, column=6,pady=5,padx=6,sticky=W+E)

    def beamApertureYFileInput(self):
        loadLabel = Label(self.inputsFrame,text="Beam aperture measurements (Vertical)",style="inputBoxes.TLabel")
        loadLabel.grid(row=5, column=0,pady=5,padx=6,sticky=W+E)
        HoverInfo(loadLabel, self.helpText.beamApYText)
        inputLoadBox = Entry(self.inputsFrame,textvariable=self.beamApertureYFile)
        inputLoadBox.grid(row=5, column=1,columnspan=5,pady=5,sticky=W+E)
        addInputButton = Button(self.inputsFrame,text="Find File",command= lambda: self.clickInputLoad(inputLoadBox))
        addInputButton.grid(row=5, column=6,pady=5,padx=6,sticky=W+E)

    def expNameInputSection(self, MainGui):
        # add experiment naming option to runPremadeRD3DStrategyFrame frame here. Name is what user wishes to
        # call the current experiment for future reference
        premadeRD3DStrategyLabel = Label(self.inputsFrame,text="Experiment Name",style="inputBoxes.TLabel")
        premadeRD3DStrategyLabel.grid(row=6, column=0,pady=5,padx=6,sticky=W+E)
        HoverInfo(premadeRD3DStrategyLabel, self.helpText.expNameText)
        premadeRD3DStrategyBox = Entry(self.inputsFrame,textvariable=self.expNameInput)
        premadeRD3DStrategyBox.grid(row=6, column=1,columnspan=5,pady=5,sticky=W+E)
        premadeRD3DRunButton = Button(self.inputsFrame,text="Run", command= lambda: self.runExp(MainGui))
        premadeRD3DRunButton.grid(row=6, column=6,pady=5,padx=6,sticky=W+E)

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

    def runExp(self, MainGui):
        pass
