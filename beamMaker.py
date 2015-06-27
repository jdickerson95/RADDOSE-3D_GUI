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
		currentStrategyBeam = LabelFrame(MainGui.top_BeamMaker,labelwidget=l,
											style="MakeABeam.TFrame")
		currentStrategyBeam.pack(side=TOP,padx=10, pady=10,fill=BOTH,expand=TRUE)

		# Beam input 1 --> Beam type
		BeaminputFrame1 = Frame(currentStrategyBeam,style="inputBoxes.TFrame")
		BeaminputFrame1.grid(row=0,column=0)
		BeaminputLabel1 = Label(BeaminputFrame1,text="Beam Type",style="inputBoxes.TLabel")
		BeaminputLabel1.pack(side=LEFT,pady=5,padx=6)
		self.BeamType = StringVar()
		beamTypeList = ['Gaussian','TopHat']
		beamTypeListOptionMenu = OptionMenu(BeaminputFrame1, self.BeamType,beamTypeList[0],*beamTypeList)
		beamTypeListOptionMenu.pack(side=LEFT,pady=5,padx=6)

		# Beam input 2 --> FWHM
		BeaminputFrame2 = Frame(currentStrategyBeam,style="inputBoxes.TFrame")
		BeaminputFrame2.grid(row=0,column=1)
		BeaminputLabel2 = Label(BeaminputFrame2,text="FWHM",style="inputBoxes.TLabel")
		BeaminputLabel2.pack(side=LEFT,pady=5,padx=6)
		self.BeamFWHMVertical,self.BeamFWHMHorizontal, = StringVar(),StringVar()
		BeamFWHMVerticalBox = Entry(BeaminputFrame2,textvariable=self.BeamFWHMVertical,width=5)
		BeamFWHMVerticalBox.pack(side=LEFT,pady=5,padx=6)
		BeamFWHMHorizontalBox = Entry(BeaminputFrame2,textvariable=self.BeamFWHMHorizontal,width=5)
		BeamFWHMHorizontalBox.pack(side=LEFT,pady=5,padx=6)

		# Beam input 3 --> flux
		BeaminputFrame3 = Frame(currentStrategyBeam,style="inputBoxes.TFrame")
		BeaminputFrame3.grid(row=1,column=0)
		BeaminputLabel3 = Label(BeaminputFrame3,text="Flux",style="inputBoxes.TLabel")
		BeaminputLabel3.pack(side=LEFT,pady=5,padx=6)
		self.BeamFlux = StringVar()
		BeaminputBox3 = Entry(BeaminputFrame3,textvariable=self.BeamFlux,width=5)
		BeaminputBox3.pack(side=LEFT,pady=5,padx=6)

		# Beam input 4 --> Energy
		BeaminputFrame4 = Frame(currentStrategyBeam,style="inputBoxes.TFrame")
		BeaminputFrame4.grid(row=1,column=1)
		BeaminputLabel4 = Label(BeaminputFrame4,text="Energy",style="inputBoxes.TLabel")
		BeaminputLabel4.pack(side=LEFT,pady=5,padx=6)
		self.BeamEnergy = StringVar()
		BeaminputBox4 = Entry(BeaminputFrame4,textvariable=self.BeamEnergy,width=5)
		BeaminputBox4.pack(side=LEFT,pady=5,padx=6)

		# Beam input 5 --> Rectangular Collimation
		BeaminputFrame5 = Frame(currentStrategyBeam,style="inputBoxes.TFrame")
		BeaminputFrame5.grid(row=2,column=0)
		BeaminputLabel5 = Label(BeaminputFrame5,text="Rectangular Collimation",style="inputBoxes.TLabel")
		BeaminputLabel5.pack(side=LEFT,pady=5,padx=6)
		self.BeamRectCollVert,self.BeamRectCollHoriz, = StringVar(),StringVar()
		BeamRectCollVertBox = Entry(BeaminputFrame5,textvariable=self.BeamRectCollVert,width=5)
		BeamRectCollVertBox.pack(side=LEFT,pady=5,padx=6)
		BeamRectCollHorizBox = Entry(BeaminputFrame5,textvariable=self.BeamRectCollHoriz,width=5)
		BeamRectCollHorizBox.pack(side=LEFT,pady=5,padx=6)

		# create a 'make' button here to add this beam to the list of added beams
		beamMakeButton = Button(currentStrategyBeam,text="Make",command= lambda: self.addMadeBeam(MainGui))
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