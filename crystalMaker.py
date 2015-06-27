from Tkinter import *
from ttk import *
import os
from crystals import crystals

class crystalMakerWindow(Frame):
	# this is a secondary crystal-maker window class here.

	def __init__(self,MainGui):
		self.master = MainGui.top_CrystMaker
		self.crystMakerFrame = Frame(self.master)
		self.crystMakerFrame.pack()

		# Crystal inputs here:
		l = Label(self.master,text="Crystal",style="labelFrameTitle.TLabel")
		currentStrategyCrystal = LabelFrame(self.master,labelwidget=l,
											style="MakeABeam.TFrame")
		currentStrategyCrystal.pack(side=TOP,padx=10, pady=10,fill=BOTH,expand=TRUE)

		# Crystal input 1 --> crystal type
		CrystalinputFrame1 = Frame(currentStrategyCrystal,style="inputBoxes.TFrame")
		CrystalinputFrame1.grid(row=0,column=0)
		CrystalinputLabel1 = Label(CrystalinputFrame1,text="Crystal Type",style="inputBoxes.TLabel")
		CrystalinputLabel1.pack(side=LEFT,pady=5,padx=6)
		self.CrystalType = StringVar()
		crystTypeList = ['Cuboid','Spherical','Polyhedron','Cylindrical']
		crystTypeOptionMenu = OptionMenu(CrystalinputFrame1, self.CrystalType,crystTypeList[0],*crystTypeList)
		crystTypeOptionMenu.pack(side=LEFT,pady=5,padx=6)

		# Crystal input 2 --> crystal dimensions
		CrystalinputFrame2 = Frame(currentStrategyCrystal,style="inputBoxes.TFrame")
		CrystalinputFrame2.grid(row=0,column=1)
		CrystalinputLabel2 = Label(CrystalinputFrame2,text="Crystal Dimensions",style="inputBoxes.TLabel")
		CrystalinputLabel2.pack(side=LEFT,pady=5,padx=6)
		self.CrystalDimX,self.CrystalDimY,self.CrystalDimZ = StringVar(),StringVar(),StringVar()
		CrystalinputBox2X = Entry(CrystalinputFrame2,textvariable=self.CrystalDimX,width=5)
		CrystalinputBox2X.pack(side=LEFT,pady=5,padx=6)
		CrystalinputBox2Y = Entry(CrystalinputFrame2,textvariable=self.CrystalDimY,width=5)
		CrystalinputBox2Y.pack(side=LEFT,pady=5,padx=6)
		CrystalinputBox2Z = Entry(CrystalinputFrame2,textvariable=self.CrystalDimZ,width=5)
		CrystalinputBox2Z.pack(side=LEFT,pady=5,padx=6)

		# Crystal input 3 --> pixels per Micron
		CrystalinputFrame3 = Frame(currentStrategyCrystal,style="inputBoxes.TFrame")
		CrystalinputFrame3.grid(row=1,column=0)
		CrystalinputLabel3 = Label(CrystalinputFrame3,text="Pixels per Micron",style="inputBoxes.TLabel")
		CrystalinputLabel3.pack(side=LEFT,pady=5,padx=6)
		self.CrystalPixPerMic = StringVar()
		CrystalinputBox3 = Entry(CrystalinputFrame3,textvariable=self.CrystalPixPerMic,width=5)
		CrystalinputBox3.pack(side=LEFT,pady=5,padx=6)

		# Crystal input 4 --> absorption coefficient
		CrystalinputFrame4 = Frame(currentStrategyCrystal,style="inputBoxes.TFrame")
		CrystalinputFrame4.grid(row=1,column=1)
		CrystalinputLabel4 = Label(CrystalinputFrame4,text="Absorption Coefficient",style="inputBoxes.TLabel")
		CrystalinputLabel4.pack(side=LEFT,pady=5,padx=6)
		self.CrystalAbsorpCoeff = StringVar()
		crystAbsCoeffList = ['Average','RADDOSE']
		crystAbsCoeffOptionMenu = OptionMenu(CrystalinputFrame4, self.CrystalAbsorpCoeff,crystAbsCoeffList[0],*crystAbsCoeffList)
		crystAbsCoeffOptionMenu.pack(side=LEFT,pady=5,padx=6)

		# create a 'make' button here to add this crystal to the list of added crystals
		crystMakeButton = Button(currentStrategyCrystal,text="Make",command= lambda: self.addMadeCryst(MainGui))
		crystMakeButton.grid(row=2,column=0,columnspan=2,pady=5)

	def addMadeCryst(self,MainGui):
		# make a new crystal object from above entered parameters and add to both listbox crystal list and
		# also list of crystal objects
		newCryst = crystals(MainGui.crystMakeName.get(),self.CrystalType.get(),self.CrystalDimX.get(),
							self.CrystalDimY.get(),self.CrystalDimZ.get(),self.CrystalPixPerMic.get(),
							self.CrystalAbsorpCoeff.get())
		MainGui.addCrystalToList(newCryst)

		# once this function runs, the toplevel window should be exited
		self.master.destroy()