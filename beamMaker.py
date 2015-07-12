from Tkinter import *
from ttk import *
from beams import *
import tkMessageBox
import tkFileDialog
from HoverInfo import HoverInfo
from InputsHelpText import BeamInputHelp

class beamMakerWindow(Frame):
    # this is a secondary beam-maker window class here.

    def __init__(self,MainGui):
        self.master = MainGui.top_BeamMaker
        self.beamMakerFrame = Frame(self.master)
        self.beamMakerFrame.pack()

        # Beam inputs here:
        l = Label(MainGui.top_BeamMaker,text="Beam",style="labelFrameTitle.TLabel")
        self.currentStrategyBeam = LabelFrame(self.master,labelwidget=l,
                                            style="MakeABeam.TFrame")
        self.currentStrategyBeam.pack(side=TOP,padx=10, pady=10,fill=BOTH,expand=TRUE)

        #Create object that contains the help text
        self.helpText = BeamInputHelp()

        # Beam input --> Beam type
        self.BeamType = StringVar()
        self.BeamType.set('Gaussian')
        self.beamTypeInputs(MainGui)

        # Beam input --> FWHM
        self.BeamFWHMVertical,self.BeamFWHMHorizontal, = StringVar(),StringVar()
        self.BeamFWHMVertical.set("")
        self.BeamFWHMHorizontal.set("")
        self.beamFWHMInputs(self.BeamType)

        # Beam input --> flux
        self.BeamFlux = StringVar()
        self.BeamFlux.set("")
        self.beamFluxInputs()

        # Beam input --> Energy
        self.BeamEnergy = StringVar()
        self.BeamEnergy.set("")
        self.beamEnergyInputs()

        # Beam input --> Rectangular Collimation
        self.BeamRectCollVert,self.BeamRectCollHoriz, = StringVar(),StringVar()
        self.BeamRectCollVert.set("")
        self.BeamRectCollHoriz.set("")
        self.beamRectCollInputs()

        # Beam input --> File containing the experimental beam image.
        self.beamFile = StringVar()
        self.beamFile.set("")
        self.beamFileInput(self.BeamType)

        #Beam input --> File containing aperture measurements in Horizontal
        #direction
        self.beamApertureXFile = StringVar()
        self.beamApertureXFile.set("")
        self.beamApertureXFileInput(self.BeamType)

        #Beam input --> File containing aperture measurements in Vertical
        #direction
        self.beamApertureYFile = StringVar()
        self.beamApertureYFile.set("")
        self.beamApertureYFileInput(self.BeamType)

        # Beam input --> x and y size of the pixels in the image.
        self.beamPixSizeX = StringVar()
        self.beamPixSizeY = StringVar()
        self.beamPixSizeX.set("")
        self.beamPixSizeY.set("")
        self.beamPixelSizeInput(self.BeamType)

        # create a 'make' button here to add this beam to the list of added beams
        self.beamMakeButton(MainGui)

        self.currentStrategyBeam.grid_rowconfigure(0,weight=1)
        self.currentStrategyBeam.grid_rowconfigure(1,weight=1)
        self.currentStrategyBeam.grid_rowconfigure(2,weight=1)
        self.currentStrategyBeam.grid_rowconfigure(3,weight=1)
        self.currentStrategyBeam.grid_rowconfigure(4,weight=1)
        self.currentStrategyBeam.grid_rowconfigure(5,weight=1)
        self.currentStrategyBeam.grid_rowconfigure(6,weight=1)
        self.currentStrategyBeam.grid_rowconfigure(7,weight=1)
        self.currentStrategyBeam.grid_rowconfigure(8,weight=1)
        self.currentStrategyBeam.grid_rowconfigure(9,weight=1)
        self.currentStrategyBeam.grid_columnconfigure(0,weight=1)
        self.currentStrategyBeam.grid_columnconfigure(1,weight=1)

    def beamTypeInputs(self,MainGui):
        # Beam input 1 --> Beam type
        BeaminputLabel1 = Label(self.currentStrategyBeam,text="Beam Type",style="inputBoxes.TLabel")
        BeaminputLabel1.grid(row=0,column=0,sticky=E,pady=5,padx=6)
        self.hoverType = HoverInfo(BeaminputLabel1, self.helpText.typeText)
        self.beamTypeDict = {'Gaussian'     : "Gaussian",
                             'TopHat'       : "Tophat",
                             'Experimental' : "ExperimentalPGM"}
        beamTypeList = self.beamTypeDict.keys()
        beamTypeListOptionMenu = OptionMenu(self.currentStrategyBeam, self.BeamType,self.BeamType.get(),*beamTypeList,command= lambda x: self.update(self.BeamType,MainGui))
        beamTypeListOptionMenu.grid(row=0,column=1,sticky=W+E,pady=5,padx=6)

    def beamFWHMInputs(self,beamType):
        # Beam input 2 --> FWHM
        if beamType.get() == 'Gaussian':
            BeaminputLabel2 = Label(self.currentStrategyBeam,text="FWHM",style="inputBoxes.TLabel")
            BeaminputLabel2.grid(row=1,column=0,sticky=E)
            self.hoverfwhm = HoverInfo(BeaminputLabel2, self.helpText.fwhmText)
            BeamFWHMInputsFrame = Frame(self.currentStrategyBeam,style="inputBoxes.TFrame")
            BeamFWHMInputsFrame.grid(row=1,column=1,sticky=W+E)
            BeamFWHMVerticalBox = Entry(BeamFWHMInputsFrame,textvariable=self.BeamFWHMVertical,width=5)
            BeamFWHMVerticalBox.grid(row=0,column=0,sticky=W+E,pady=5,padx=6)
            BeamFWHMHorizontalBox = Entry(BeamFWHMInputsFrame,textvariable=self.BeamFWHMHorizontal,width=5)
            BeamFWHMHorizontalBox.grid(row=0,column=1,sticky=W+E,pady=5,padx=6)
            BeamFWHMInputsFrame.grid_rowconfigure(0, weight=1)
            BeamFWHMInputsFrame.grid_columnconfigure(0, weight=1)
            BeamFWHMInputsFrame.grid_columnconfigure(1, weight=1)

        self.BeamFWHMVertical.set(self.BeamFWHMVertical.get())
        self.BeamFWHMHorizontal.set(self.BeamFWHMHorizontal.get())

    def beamFluxInputs(self):
        # Beam input 3 --> flux
        BeaminputLabel3 = Label(self.currentStrategyBeam,text="Flux",style="inputBoxes.TLabel")
        BeaminputLabel3.grid(row=2,column=0,sticky=E,pady=5,padx=6)
        self.hoverFlux = HoverInfo(BeaminputLabel3, self.helpText.fluxText)
        BeaminputBox3 = Entry(self.currentStrategyBeam,textvariable=self.BeamFlux,width=5)
        BeaminputBox3.grid(row=2,column=1,sticky=W+E,pady=5,padx=6)
        self.BeamFlux.set(self.BeamFlux.get())

    def beamEnergyInputs(self):
        # Beam input 4 --> Energy
        BeaminputLabel4 = Label(self.currentStrategyBeam,text="Energy",style="inputBoxes.TLabel")
        BeaminputLabel4.grid(row=3,column=0,sticky=E,pady=5,padx=6)
        self.hoverEnergy = HoverInfo(BeaminputLabel4, self.helpText.energyText)
        BeaminputBox4 = Entry(self.currentStrategyBeam,textvariable=self.BeamEnergy,width=5)
        BeaminputBox4.grid(row=3,column=1,sticky=W+E,pady=5,padx=6)
        self.BeamEnergy.set(self.BeamEnergy.get())

    def beamRectCollInputs(self):
        # Beam input 5 --> Rectangular Collimation
        BeaminputLabel5 = Label(self.currentStrategyBeam,text="Rectangular Collimation",style="inputBoxes.TLabel")
        BeaminputLabel5.grid(row=4,column=0,sticky=E,pady=5,padx=6)
        self.hoverColl = HoverInfo(BeaminputLabel5, self.helpText.collText)
        BeamRectCollInputsFrame = Frame(self.currentStrategyBeam,style="inputBoxes.TFrame")
        BeamRectCollInputsFrame.grid(row=4,column=1,sticky=W+E)
        BeamRectCollVertBox = Entry(BeamRectCollInputsFrame,textvariable=self.BeamRectCollVert,width=5)
        BeamRectCollVertBox.grid(row=0,column=0,sticky=W+E,pady=5,padx=6)
        BeamRectCollHorizBox = Entry(BeamRectCollInputsFrame,textvariable=self.BeamRectCollHoriz,width=5)
        BeamRectCollHorizBox.grid(row=0,column=1,sticky=W+E,pady=5,padx=6)
        BeamRectCollInputsFrame.grid_rowconfigure(0, weight=1)
        BeamRectCollInputsFrame.grid_columnconfigure(0, weight=1)
        BeamRectCollInputsFrame.grid_columnconfigure(1, weight=1)

        self.BeamRectCollVert.set(self.BeamRectCollVert.get())
        self.BeamRectCollHoriz.set(self.BeamRectCollHoriz.get())

    def beamFileInput(self,beamType):
        # Beam input 2 --> FWHM
        if beamType.get() == 'Experimental':
            BeamFileInputLabel = Label(self.currentStrategyBeam,text="Beam Image File",style="inputBoxes.TLabel")
            BeamFileInputLabel.grid(row=5,column=0,sticky=E,pady=5,padx=6)
            self.hoverFile = HoverInfo(BeamFileInputLabel, self.helpText.fileText)
            inputsFrame = Frame(self.currentStrategyBeam,style="inputBoxes.TFrame")
            inputsFrame.grid(row=5,column=1,sticky=W,pady=5,padx=6)
            inputLoadBox = Entry(inputsFrame,textvariable=self.beamFile)
            inputLoadBox.grid(row=0, column=0,columnspan=5,pady=5,sticky=W+E)
            addInputButton = Button(inputsFrame,text="Find File",command= lambda: self.clickInputLoad(inputLoadBox))
            addInputButton.grid(row=0, column=5,pady=5,padx=6,sticky=W+E)
            inputsFrame.grid_rowconfigure(0,weight=1)
            inputsFrame.grid_columnconfigure(0,weight=1)
            inputsFrame.grid_columnconfigure(1,weight=1)
            inputsFrame.grid_columnconfigure(2,weight=1)
            inputsFrame.grid_columnconfigure(3,weight=1)
            inputsFrame.grid_columnconfigure(4,weight=1)
            inputsFrame.grid_columnconfigure(5,weight=1)
        else:
            self.beamFile.set(self.beamFile.get())

    def beamApertureXFileInput(self,beamType):
        if beamType.get() == 'Experimental':
            loadLabel = Label(self.currentStrategyBeam,text="Beam aperture measurements (Horizontal)",style="inputBoxes.TLabel")
            loadLabel.grid(row=6, column=0,pady=5,padx=6,sticky=W+E)
            HoverInfo(loadLabel, self.helpText.beamApXText)
            inputsFrame = Frame(self.currentStrategyBeam,style="inputBoxes.TFrame")
            inputsFrame.grid(row=6,column=1,sticky=W,pady=5,padx=6)
            inputLoadBox = Entry(inputsFrame,textvariable=self.beamApertureXFile)
            inputLoadBox.grid(row=0, column=0,columnspan=5,pady=5,sticky=W+E)
            addInputButton = Button(inputsFrame,text="Find File",command= lambda: self.clickInputLoad(inputLoadBox))
            addInputButton.grid(row=0, column=5,pady=5,padx=6,sticky=W+E)
            inputsFrame.grid_rowconfigure(0,weight=1)
            inputsFrame.grid_columnconfigure(0,weight=1)
            inputsFrame.grid_columnconfigure(1,weight=1)
            inputsFrame.grid_columnconfigure(2,weight=1)
            inputsFrame.grid_columnconfigure(3,weight=1)
            inputsFrame.grid_columnconfigure(4,weight=1)
            inputsFrame.grid_columnconfigure(5,weight=1)
        else:
            self.beamApertureXFile.set(self.beamApertureXFile.get())


    def beamApertureYFileInput(self,beamType):
        if beamType.get() == 'Experimental':
            loadLabel = Label(self.currentStrategyBeam,text="Beam aperture measurements (Vertical)",style="inputBoxes.TLabel")
            loadLabel.grid(row=7, column=0,pady=5,padx=6,sticky=W+E)
            HoverInfo(loadLabel, self.helpText.beamApYText)
            inputsFrame = Frame(self.currentStrategyBeam,style="inputBoxes.TFrame")
            inputsFrame.grid(row=7,column=1,sticky=W,pady=5,padx=6)
            inputLoadBox = Entry(inputsFrame,textvariable=self.beamApertureYFile)
            inputLoadBox.grid(row=0, column=0,columnspan=5,pady=5,sticky=W+E)
            addInputButton = Button(inputsFrame,text="Find File",command= lambda: self.clickInputLoad(inputLoadBox))
            addInputButton.grid(row=0, column=5,pady=5,padx=6,sticky=W+E)
            inputsFrame.grid_rowconfigure(0,weight=1)
            inputsFrame.grid_columnconfigure(0,weight=1)
            inputsFrame.grid_columnconfigure(1,weight=1)
            inputsFrame.grid_columnconfigure(2,weight=1)
            inputsFrame.grid_columnconfigure(3,weight=1)
            inputsFrame.grid_columnconfigure(4,weight=1)
            inputsFrame.grid_columnconfigure(5,weight=1)
        else:
            self.beamApertureYFile.set(self.beamApertureYFile.get())

    def beamPixelSizeInput(self,beamType):
        # Beam input 2 --> FWHM
        if beamType.get() == 'Experimental':
            BeamPixelSizeInputLabel = Label(self.currentStrategyBeam,text="Pixel Size (x, y - microns)",style="inputBoxes.TLabel")
            BeamPixelSizeInputLabel.grid(row=8,column=0,sticky=E,pady=5,padx=6)
            self.hoverPixelSize = HoverInfo(BeamPixelSizeInputLabel, self.helpText.pixSizeText)
            BeamPixelSizeInputsFrame = Frame(self.currentStrategyBeam,style="inputBoxes.TFrame")
            BeamPixelSizeInputsFrame.grid(row=8,column=1,sticky=W+E)
            BeamPixelSizeXBox = Entry(BeamPixelSizeInputsFrame,textvariable=self.beamPixSizeX,width=5)
            BeamPixelSizeXBox.grid(row=0,column=0,sticky=W+E,pady=5,padx=6)
            BeamPixelSizeYBox = Entry(BeamPixelSizeInputsFrame,textvariable=self.beamPixSizeY,width=5)
            BeamPixelSizeYBox.grid(row=0,column=1,sticky=W+E,pady=5,padx=6)
            BeamPixelSizeInputsFrame.grid_rowconfigure(0, weight=1)
            BeamPixelSizeInputsFrame.grid_columnconfigure(0, weight=1)
            BeamPixelSizeInputsFrame.grid_columnconfigure(1, weight=1)
        else:
            self.beamPixSizeX.set(self.beamPixSizeX.get())
            self.beamPixSizeY.set(self.beamPixSizeY.get())

    def update(self,beamType,MainGui):
        # remove all widgets within the current beam-maker frame
        for widget in self.currentStrategyBeam.winfo_children():
            widget.destroy()

        # recreate new updated widgets for beam inputs
        self.beamTypeInputs(MainGui)
        self.beamFWHMInputs(self.BeamType)
        self.beamFluxInputs()
        self.beamEnergyInputs()
        self.beamRectCollInputs()
        self.beamFileInput(self.BeamType)
        self.beamApertureXFileInput(self.BeamType)
        self.beamApertureYFileInput(self.BeamType)
        self.beamPixelSizeInput(self.BeamType)
        self.beamMakeButton(MainGui)

    def beamMakeButton(self,MainGui):
        # create a 'make' button here to add this beam to the list of added beams
        beamMakeButton = Button(self.currentStrategyBeam,text="Make",command= lambda: self.addMadeBeam(MainGui))
        beamMakeButton.grid(row=9,column=0,columnspan=3,pady=5)

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

    def addMadeBeam(self,MainGui):
        # make a new beam object from above entered parameters and add to both listbox beam list and
        # also list of beam objects

        if self.beamTypeDict[self.BeamType.get()] == 'Gaussian':
            newBeam = beams_Gaussian(MainGui.beamMakeName.get(),
                                     [self.BeamFWHMVertical.get(),self.BeamFWHMHorizontal.get()],
                                     self.BeamFlux.get(),self.BeamEnergy.get(),
                                     [self.BeamRectCollVert.get(),self.BeamRectCollHoriz.get()])
        elif self.beamTypeDict[self.BeamType.get()] == 'Tophat':
            newBeam = beams_Tophat(MainGui.beamMakeName.get(),self.BeamFlux.get(),self.BeamEnergy.get(),
                                   [self.BeamRectCollVert.get(),self.BeamRectCollHoriz.get()])
        elif self.beamTypeDict[self.BeamType.get()] == 'ExperimentalPGM':
            newBeam = beams_Experimental(MainGui.beamMakeName.get(),self.BeamFlux.get(),self.BeamEnergy.get(),
                                    [self.beamPixSizeX.get(),self.beamPixSizeY.get()],self.beamFile.get())

        # check the beams parameters are valid
        ErrorMessage = MainGui.checkBeamInputs(newBeam)
        if ErrorMessage != "":
                    tkMessageBox.showinfo("Invalid Input File",ErrorMessage)
        else:
			# give warning if identical beam already loaded
			warningMessage = MainGui.checkRepeatedBeam(newBeam)
			if warningMessage != "":
				tkMessageBox.showinfo("Warning",warningMessage)

			# add new beam to list of loaded beams
			MainGui.addBeamToList(newBeam)

			# once this function runs, the toplevel window should be exited
			self.master.destroy()
