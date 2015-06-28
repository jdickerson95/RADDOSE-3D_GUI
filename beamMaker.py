from Tkinter import *
from ttk import *
from beams import beams

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
		BeaminputFrame1 = Frame(self.currentStrategyBeam,style="inputBoxes.TFrame")
		BeaminputFrame1.grid(row=0,column=0)
		BeaminputLabel1 = Label(BeaminputFrame1,text="Beam Type",style="inputBoxes.TLabel")
		BeaminputLabel1.pack(side=LEFT,pady=5,padx=6)
		beamTypeList = ['Gaussian','TopHat']
		beamTypeListOptionMenu = OptionMenu(BeaminputFrame1, self.BeamType,self.BeamType.get(),*beamTypeList,command= lambda x: self.update(self.BeamType,MainGui))
		beamTypeListOptionMenu.pack(side=LEFT,pady=5,padx=6)

	def beamFWHMInputs(self,beamType):
		# Beam input 2 --> FWHM
		if beamType.get() == 'Gaussian':
			BeaminputFrame2 = Frame(self.currentStrategyBeam,style="inputBoxes.TFrame")
			BeaminputFrame2.grid(row=0,column=1)
			BeaminputLabel2 = Label(BeaminputFrame2,text="FWHM",style="inputBoxes.TLabel")
			BeaminputLabel2.pack(side=LEFT,pady=5,padx=6)
			BeamFWHMVerticalBox = Entry(BeaminputFrame2,textvariable=self.BeamFWHMVertical,width=5)
			BeamFWHMVerticalBox.pack(side=LEFT,pady=5,padx=6)
			BeamFWHMHorizontalBox = Entry(BeaminputFrame2,textvariable=self.BeamFWHMHorizontal,width=5)
			BeamFWHMHorizontalBox.pack(side=LEFT,pady=5,padx=6)
		elif beamType.get() == 'TopHat':
			self.BeamFWHMVertical.set("")
			self.BeamFWHMHorizontal.set("")

	def beamFluxInputs(self):
		# Beam input 3 --> flux
		BeaminputFrame3 = Frame(self.currentStrategyBeam,style="inputBoxes.TFrame")
		BeaminputFrame3.grid(row=1,column=0)
		BeaminputLabel3 = Label(BeaminputFrame3,text="Flux",style="inputBoxes.TLabel")
		BeaminputLabel3.pack(side=LEFT,pady=5,padx=6)
		BeaminputBox3 = Entry(BeaminputFrame3,textvariable=self.BeamFlux,width=5)
		BeaminputBox3.pack(side=LEFT,pady=5,padx=6)

	def beamEnergyInputs(self):
		# Beam input 4 --> Energy
		BeaminputFrame4 = Frame(self.currentStrategyBeam,style="inputBoxes.TFrame")
		BeaminputFrame4.grid(row=1,column=1)
		BeaminputLabel4 = Label(BeaminputFrame4,text="Energy",style="inputBoxes.TLabel")
		BeaminputLabel4.pack(side=LEFT,pady=5,padx=6)
		BeaminputBox4 = Entry(BeaminputFrame4,textvariable=self.BeamEnergy,width=5)
		BeaminputBox4.pack(side=LEFT,pady=5,padx=6)

	def beamRectCollInputs(self):
		# Beam input 5 --> Rectangular Collimation
		BeaminputFrame5 = Frame(self.currentStrategyBeam,style="inputBoxes.TFrame")
		BeaminputFrame5.grid(row=2,column=0)
		BeaminputLabel5 = Label(BeaminputFrame5,text="Rectangular Collimation",style="inputBoxes.TLabel")
		BeaminputLabel5.pack(side=LEFT,pady=5,padx=6)
		BeamRectCollVertBox = Entry(BeaminputFrame5,textvariable=self.BeamRectCollVert,width=5)
		BeamRectCollVertBox.pack(side=LEFT,pady=5,padx=6)
		BeamRectCollHorizBox = Entry(BeaminputFrame5,textvariable=self.BeamRectCollHoriz,width=5)
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
		beamMakeButton = Button(self.currentStrategyBeam,text="Make",command= lambda: self.addMadeBeam(MainGui))
		beamMakeButton.grid(row=3,column=0,columnspan=2,pady=5)

	def addMadeBeam(self,MainGui):
		# make a new beam object from above entered parameters and add to both listbox beam list and
		# also list of beam objects
		newBeam = beams(MainGui.beamMakeName.get(),self.BeamType.get(),
						[self.BeamFWHMVertical.get(),self.BeamFWHMHorizontal.get()],
						self.BeamFlux.get(),self.BeamEnergy.get(),
						[self.BeamRectCollVert.get(),self.BeamRectCollHoriz.get()])
		MainGui.addBeamToList(newBeam)

		# once this function runs, the toplevel window should be exited
		self.master.destroy()