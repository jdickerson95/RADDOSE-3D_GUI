from Tkinter import *
from ttk import *
from beams import *
import tkMessageBox
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
		self.beamFWHMInputs(self.BeamType)

		# Beam input --> flux
		self.BeamFlux = StringVar()
		self.beamFluxInputs()

		# Beam input --> Energy
		self.BeamEnergy = StringVar()
		self.beamEnergyInputs()

		# Beam input --> Rectangular Collimation
		self.BeamRectCollVert,self.BeamRectCollHoriz, = StringVar(),StringVar()
		self.beamRectCollInputs(self.BeamType)

		# Beam input --> File containing the experimental beam image.
		self.beamFile = StringVar()
		self.beamFileInput(self.BeamType)

		# Beam input --> x and y size of the pixels in the image.
		self.beamPixSizeX = StringVar()
		self.beamPixSizeY = StringVar()
		self.beamPixelSizeInput(self.BeamType)

		# create a 'make' button here to add this beam to the list of added beams
		self.beamMakeButton(MainGui)

	def beamTypeInputs(self,MainGui):
		# Beam input 1 --> Beam type
		BeaminputLabel1 = Label(self.currentStrategyBeam,text="Beam Type",style="inputBoxes.TLabel")
		BeaminputLabel1.grid(row=0,column=0,sticky=E,pady=5,padx=6)
		self.hoverType = HoverInfo(BeaminputLabel1, self.helpText.typeText)
		self.beamTypeDict = {'Gaussian'     : "Gaussian",
		                     'TopHat'       : "Tophat",
							 'Experimental' : "Experimental"}
		beamTypeList = self.beamTypeDict.keys()
		beamTypeListOptionMenu = OptionMenu(self.currentStrategyBeam, self.BeamType,self.BeamType.get(),*beamTypeList,command= lambda x: self.update(self.BeamType,MainGui))
		beamTypeListOptionMenu.grid(row=0,column=1,sticky=W,pady=5,padx=6)

	def beamFWHMInputs(self,beamType):
		# Beam input 2 --> FWHM
		if beamType.get() == 'Gaussian':
			BeaminputLabel2 = Label(self.currentStrategyBeam,text="FWHM",style="inputBoxes.TLabel")
			BeaminputLabel2.grid(row=1,column=0,sticky=E)
			self.hoverfwhm = HoverInfo(BeaminputLabel2, self.helpText.fwhmText)
			BeamFWHMInputsFrame = Frame(self.currentStrategyBeam,style="inputBoxes.TFrame")
			BeamFWHMInputsFrame.grid(row=1,column=1,sticky=W)
			BeamFWHMVerticalBox = Entry(BeamFWHMInputsFrame,textvariable=self.BeamFWHMVertical,width=5)
			BeamFWHMVerticalBox.pack(side=LEFT,pady=5,padx=6)
			BeamFWHMHorizontalBox = Entry(BeamFWHMInputsFrame,textvariable=self.BeamFWHMHorizontal,width=5)
			BeamFWHMHorizontalBox.pack(side=LEFT,pady=5,padx=6)
		else:
			self.BeamFWHMVertical.set("")
			self.BeamFWHMHorizontal.set("")

	def beamFluxInputs(self):
		# Beam input 3 --> flux
		BeaminputLabel3 = Label(self.currentStrategyBeam,text="Flux",style="inputBoxes.TLabel")
		BeaminputLabel3.grid(row=2,column=0,sticky=E,pady=5,padx=6)
		self.hoverFlux = HoverInfo(BeaminputLabel3, self.helpText.fluxText)
		BeaminputBox3 = Entry(self.currentStrategyBeam,textvariable=self.BeamFlux,width=5)
		BeaminputBox3.grid(row=2,column=1,sticky=W,pady=5,padx=6)

	def beamEnergyInputs(self):
		# Beam input 4 --> Energy
		BeaminputLabel4 = Label(self.currentStrategyBeam,text="Energy",style="inputBoxes.TLabel")
		BeaminputLabel4.grid(row=3,column=0,sticky=E,pady=5,padx=6)
		self.hoverEnergy = HoverInfo(BeaminputLabel4, self.helpText.energyText)
		BeaminputBox4 = Entry(self.currentStrategyBeam,textvariable=self.BeamEnergy,width=5)
		BeaminputBox4.grid(row=3,column=1,sticky=W,pady=5,padx=6)

	def beamRectCollInputs(self, beamType):
		# Beam input 5 --> Rectangular Collimation
		if beamType.get() == 'Experimental':
			self.BeamRectCollVert.set("0")
			self.BeamRectCollHoriz.set("0")
		else:
			if beamType.get() == 'Gaussian':
				BeaminputLabel5 = Label(self.currentStrategyBeam,text="Rectangular Collimation (optional)",style="inputBoxes.TLabel")
			else:
				BeaminputLabel5 = Label(self.currentStrategyBeam,text="Rectangular Collimation",style="inputBoxes.TLabel")
			BeaminputLabel5.grid(row=4,column=0,sticky=E,pady=5,padx=6)
			self.hoverColl = HoverInfo(BeaminputLabel5, self.helpText.collText)
			BeamRectCollInputsFrame = Frame(self.currentStrategyBeam,style="inputBoxes.TFrame")
			BeamRectCollInputsFrame.grid(row=4,column=1,sticky=W)
			BeamRectCollVertBox = Entry(BeamRectCollInputsFrame,textvariable=self.BeamRectCollVert,width=5)
			BeamRectCollVertBox.pack(side=LEFT,pady=5,padx=6)
			BeamRectCollHorizBox = Entry(BeamRectCollInputsFrame,textvariable=self.BeamRectCollHoriz,width=5)
			BeamRectCollHorizBox.pack(side=LEFT,pady=5,padx=6)

	def beamFileInput(self,beamType):
		# Beam input 2 --> FWHM
		if beamType.get() == 'Experimental':
			BeamFileInputLabel = Label(self.currentStrategyBeam,text="File",style="inputBoxes.TLabel")
			BeamFileInputLabel.grid(row=4,column=0,sticky=E,pady=5,padx=6)
			self.hoverFile = HoverInfo(BeamFileInputLabel, self.helpText.fileText)
			BeamFileInputBox = Entry(self.currentStrategyBeam,textvariable=self.beamFile,width=5)
			BeamFileInputBox.grid(row=4,column=1,columnspan=2,sticky=W+E,pady=5,padx=6)
		else:
			self.beamFile.set("")

	def beamPixelSizeInput(self,beamType):
		# Beam input 2 --> FWHM
		if beamType.get() == 'Experimental':
			BeamPixelSizeInputLabel = Label(self.currentStrategyBeam,text="Pixel Size (x, y - microns)",style="inputBoxes.TLabel")
			BeamPixelSizeInputLabel.grid(row=5,column=0,sticky=E,pady=5,padx=6)
			self.hoverPixelSize = HoverInfo(BeamPixelSizeInputLabel, self.helpText.pixSizeText)
			BeamPixelSizeInputsFrame = Frame(self.currentStrategyBeam,style="inputBoxes.TFrame")
			BeamPixelSizeInputsFrame.grid(row=5,column=1,sticky=W)
			BeamPixelSizeXBox = Entry(BeamPixelSizeInputsFrame,textvariable=self.beamPixSizeX,width=5)
			BeamPixelSizeXBox.pack(side=LEFT,pady=5,padx=6)
			BeamPixelSizeYBox = Entry(BeamPixelSizeInputsFrame,textvariable=self.beamPixSizeY,width=5)
			BeamPixelSizeYBox.pack(side=LEFT,pady=5,padx=6)
		else:
			self.beamPixSizeX.set("0")
			self.beamPixSizeY.set("0")

	def update(self,beamType,MainGui):
		# remove all widgets within the current beam-maker frame
		for widget in self.currentStrategyBeam.winfo_children():
			widget.destroy()

		# recreate new updated widgets for beam inputs
		self.beamTypeInputs(MainGui)
		self.beamFWHMInputs(self.BeamType)
		self.beamFluxInputs()
		self.beamEnergyInputs()
		self.beamRectCollInputs(self.BeamType)
		self.beamFileInput(self.BeamType)
		self.beamPixelSizeInput(self.BeamType)
		self.beamMakeButton(MainGui)

	def beamMakeButton(self,MainGui):
		# create a 'make' button here to add this beam to the list of added beams
		beamMakeButton = Button(self.currentStrategyBeam,text="Make",command= lambda: self.addMadeBeam(MainGui))
		beamMakeButton.grid(row=6,column=0,columnspan=3,pady=5)

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
		elif self.beamTypeDict[self.BeamType.get()] == 'Experimental':
			newBeam = beams_Experimental(MainGui.beamMakeName.get(),self.BeamFlux.get(),self.BeamEnergy.get(),
									[self.beamPixSizeX.get(),self.beamPixSizeY.get()],self.beamFile.get())

		# check the beams parameters are valid
		ErrorMessage = MainGui.checkBeamInputs(newBeam)
		if ErrorMessage != "":
					tkMessageBox.showinfo("Invalid Input File",ErrorMessage)
		else:
			# add new beam to list of loaded beams
			MainGui.addBeamToList(newBeam)

			# once this function runs, the toplevel window should be exited
			self.master.destroy()
