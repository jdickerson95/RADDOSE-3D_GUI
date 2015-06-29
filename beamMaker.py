from Tkinter import *
from ttk import *
from beams import beams
import tkMessageBox

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

		# Beam input 1 --> Beam type
		self.BeamType = StringVar()
		self.BeamType.set('Gaussian')
		self.beamTypeInputs(MainGui)
	
		# Beam input 2 --> FWHM
		self.BeamFWHMVertical,self.BeamFWHMHorizontal, = StringVar(),StringVar()
		self.beamFWHMInputs(self.BeamType)

		# Beam input 3 --> flux
		self.BeamFlux = StringVar()
		self.beamFluxInputs()

		# Beam input 4 --> Energy
		self.BeamEnergy = StringVar()
		self.beamEnergyInputs()

		# Beam input 5 --> Rectangular Collimation
		self.BeamRectCollVert,self.BeamRectCollHoriz, = StringVar(),StringVar()
		self.beamRectCollInputs()

		# create a 'make' button here to add this beam to the list of added beams
		self.beamMakeButton(MainGui)
		
	def beamTypeInputs(self,MainGui):
		# Beam input 1 --> Beam type
		BeaminputLabel1 = Label(self.currentStrategyBeam,text="Beam Type",style="inputBoxes.TLabel")
		BeaminputLabel1.grid(row=0,column=0,sticky=E,pady=5,padx=6)
		beamTypeList = ['Gaussian','TopHat']
		beamTypeListOptionMenu = OptionMenu(self.currentStrategyBeam, self.BeamType,self.BeamType.get(),*beamTypeList,command= lambda x: self.update(self.BeamType,MainGui))
		beamTypeListOptionMenu.grid(row=0,column=1,sticky=W,pady=5,padx=6)

	def beamFWHMInputs(self,beamType):
		# Beam input 2 --> FWHM
		if beamType.get() == 'Gaussian':
			BeaminputLabel2 = Label(self.currentStrategyBeam,text="FWHM",style="inputBoxes.TLabel")
			BeaminputLabel2.grid(row=1,column=0,sticky=E)
			BeamFWHMInputsFrame = Frame(self.currentStrategyBeam,style="inputBoxes.TFrame")
			BeamFWHMInputsFrame.grid(row=1,column=1,sticky=W)
			BeamFWHMVerticalBox = Entry(BeamFWHMInputsFrame,textvariable=self.BeamFWHMVertical,width=5)
			BeamFWHMVerticalBox.pack(side=LEFT,pady=5,padx=6)
			BeamFWHMHorizontalBox = Entry(BeamFWHMInputsFrame,textvariable=self.BeamFWHMHorizontal,width=5)
			BeamFWHMHorizontalBox.pack(side=LEFT,pady=5,padx=6)
		elif beamType.get() == 'TopHat':
			self.BeamFWHMVertical.set("0")
			self.BeamFWHMHorizontal.set("0")

	def beamFluxInputs(self):
		# Beam input 3 --> flux
		BeaminputLabel3 = Label(self.currentStrategyBeam,text="Flux",style="inputBoxes.TLabel")
		BeaminputLabel3.grid(row=2,column=0,sticky=E,pady=5,padx=6)
		BeaminputBox3 = Entry(self.currentStrategyBeam,textvariable=self.BeamFlux,width=5)
		BeaminputBox3.grid(row=2,column=1,sticky=W,pady=5,padx=6)

	def beamEnergyInputs(self):
		# Beam input 4 --> Energy
		BeaminputLabel4 = Label(self.currentStrategyBeam,text="Energy",style="inputBoxes.TLabel")
		BeaminputLabel4.grid(row=3,column=0,sticky=E,pady=5,padx=6)
		BeaminputBox4 = Entry(self.currentStrategyBeam,textvariable=self.BeamEnergy,width=5)
		BeaminputBox4.grid(row=3,column=1,sticky=W,pady=5,padx=6)

	def beamRectCollInputs(self):
		# Beam input 5 --> Rectangular Collimation
		BeaminputLabel5 = Label(self.currentStrategyBeam,text="Rectangular Collimation",style="inputBoxes.TLabel")
		BeaminputLabel5.grid(row=4,column=0,sticky=E,pady=5,padx=6)
		BeamRectCollInputsFrame = Frame(self.currentStrategyBeam,style="inputBoxes.TFrame")
		BeamRectCollInputsFrame.grid(row=4,column=1,sticky=W)
		BeamRectCollVertBox = Entry(BeamRectCollInputsFrame,textvariable=self.BeamRectCollVert,width=5)
		BeamRectCollVertBox.pack(side=LEFT,pady=5,padx=6)
		BeamRectCollHorizBox = Entry(BeamRectCollInputsFrame,textvariable=self.BeamRectCollHoriz,width=5)
		BeamRectCollHorizBox.pack(side=LEFT,pady=5,padx=6)

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
		self.beamMakeButton(MainGui)

	def beamMakeButton(self,MainGui):
		# create a 'make' button here to add this beam to the list of added beams
		beamMakeButton = Button(self.currentStrategyBeam,text="Make",command= lambda: self.addMadeBeam(MainGui))
		beamMakeButton.grid(row=5,column=0,columnspan=3,pady=5)

	def addMadeBeam(self,MainGui):
		# make a new beam object from above entered parameters and add to both listbox beam list and
		# also list of beam objects
		newBeam = beams(MainGui.beamMakeName.get(),self.BeamType.get(),
						[self.BeamFWHMVertical.get(),self.BeamFWHMHorizontal.get()],
						self.BeamFlux.get(),self.BeamEnergy.get(),
						[self.BeamRectCollVert.get(),self.BeamRectCollHoriz.get()])

		# check the beams parameters are valid
		ErrorMessage = MainGui.checkBeamInputs(newBeam)
		if ErrorMessage != "":
					tkMessageBox.showinfo("Invalid Input File",ErrorMessage)
		else:
			# add new beam to list of loaded beams
			MainGui.addBeamToList(newBeam)

			# once this function runs, the toplevel window should be exited
			self.master.destroy()