from Tkinter import *
from ttk import *
from crystals import crystals
import tkMessageBox

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

		# Crystal input --> crystal type
		self.CrystalType = StringVar()
		self.CrystalType.set('Cuboid')
		self.crystalTypeInputs(MainGui)

		# Crystal input --> default cuboid crystal dimensions
		self.CrystalDimX,self.CrystalDimY,self.CrystalDimZ = StringVar(),StringVar(),StringVar()
		self.crystalDimInputs(self.CrystalType)

		# Crystal input --> wireframe type and model file for a polyhedron crystal
		self.crystalWireFrameType, self.crystalModelFile, = StringVar(),StringVar(),
		self.crystalDimInputs(self.CrystalType)

		# Crystal input --> pixels per Micron
		self.crystalPixPerMicInputs()

		# Crystal input --> absorption coefficient
		self.crystalAbsCoeffInputs()

		# create a 'make' button here to add this crystal to the list of added crystals
		self.crystalMakeButton(MainGui)


	def crystalTypeInputs(self,MainGui):
		# Crystal input 1 --> crystal type
		CrystalinputLabel1 = Label(self.currentStrategyCrystal,text="Crystal Type",style="inputBoxes.TLabel")
		CrystalinputLabel1.grid(row=0,column=0,sticky=E,pady=5,padx=6)
		crystTypeList = ['Cuboid','Spherical', 'Cylindrical', 'Polyhedron']
		crystTypeOptionMenu = OptionMenu(self.currentStrategyCrystal, self.CrystalType,self.CrystalType.get(),*crystTypeList, command= lambda x: self.update(self.CrystalType,MainGui))
		crystTypeOptionMenu.grid(row=0,column=1,sticky=W,pady=5,padx=6)

	def crystalDimInputs(self,value):
		# Crystal input 2 --> crystal dimensions
		if value.get() in ('Cuboid','Spherical','Cylindrical'):

			CrystalinputLabel2 = Label(self.currentStrategyCrystal,text="Crystal Dimensions (microns):",style="inputBoxes.TLabel")
			CrystalinputLabel2.grid(row=0,column=2,sticky=E,pady=5,padx=6)

			self.CrystalDimsInputsFrame = Frame(self.currentStrategyCrystal,style="inputBoxes.TFrame")
			self.CrystalDimsInputsFrame.grid(row=0,column=3,sticky=W,pady=5,padx=6)

			if value.get() == 'Cuboid':
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

			elif value.get() == 'Spherical':
				CrystalDimXLabel = Label(self.CrystalDimsInputsFrame,text="Diameter = ",style="inputBoxes.TLabel")
				CrystalDimXLabel.pack(side=LEFT,pady=5,padx=6)
				CrystalinputBox2X = Entry(self.CrystalDimsInputsFrame,textvariable=self.CrystalDimX,width=5)
				CrystalinputBox2X.pack(side=LEFT,pady=5,padx=6)
				self.CrystalDimY.set(0)
				self.CrystalDimZ.set(0)

			elif value.get() == 'Cylindrical':
				CrystalDimXLabel = Label(self.CrystalDimsInputsFrame,text="Diameter = ",style="inputBoxes.TLabel")
				CrystalDimXLabel.pack(side=LEFT,pady=5,padx=6)
				CrystalinputBox2X = Entry(self.CrystalDimsInputsFrame,textvariable=self.CrystalDimX,width=5)
				CrystalinputBox2X.pack(side=LEFT,pady=5,padx=6)
				CrystalDimXLabel = Label(self.CrystalDimsInputsFrame,text="Height = ",style="inputBoxes.TLabel")
				CrystalDimXLabel.pack(side=LEFT,pady=5,padx=6)
				CrystalinputBox2X = Entry(self.CrystalDimsInputsFrame,textvariable=self.CrystalDimY,width=5)
				CrystalinputBox2X.pack(side=LEFT,pady=5,padx=6)
				self.CrystalDimZ.set(0)

		elif value.get() == 'Polyhedron':
			# CrystalWireFrameTypeLabel = Label(self.currentStrategyCrystal,text="WireFrameType = ",style="inputBoxes.TLabel")
			# CrystalWireFrameTypeLabel.grid(row=0,column=2,sticky=E,pady=5,padx=6)
			# crystWireFrameTypeList = ['obj']
			# crystTypeOptionMenu = OptionMenu(self.currentStrategyCrystal, self.crystalWireFrameType, self.crystalWireFrameType.get(), *crystWireFrameTypeList)
			# crystTypeOptionMenu.grid(row=0,column=3,sticky=W,pady=5,padx=6)
			CrystalModelFileLabel = Label(self.currentStrategyCrystal,text="Model File (.obj) = ",style="inputBoxes.TLabel")
			CrystalModelFileLabel.grid(row=0,column=2,sticky=E,pady=5,padx=6)
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
		self.CrystalPixPerMic = StringVar()
		CrystalinputBox3 = Entry(self.currentStrategyCrystal,textvariable=self.CrystalPixPerMic,width=5)
		CrystalinputBox3.grid(row=1,column=1,sticky=W,pady=5,padx=6)

	def crystalAbsCoeffInputs(self):
		# Crystal input 4 --> absorption coefficient
		CrystalinputLabel4 = Label(self.currentStrategyCrystal,text="Absorption Coefficient",style="inputBoxes.TLabel")
		CrystalinputLabel4.grid(row=1,column=2,sticky=E,pady=5,padx=6)
		self.CrystalAbsorpCoeff = StringVar()
		crystAbsCoeffList = ['Average','RADDOSE']
		crystAbsCoeffOptionMenu = OptionMenu(self.currentStrategyCrystal, self.CrystalAbsorpCoeff,crystAbsCoeffList[0],*crystAbsCoeffList)
		crystAbsCoeffOptionMenu.grid(row=1,column=3,sticky=W,pady=5,padx=6)

	def update(self,value,MainGui):

		# remove all widgets within the current crystal-maker frame
		for widget in self.currentStrategyCrystal.winfo_children():
			widget.destroy()

		self.crystalTypeInputs(MainGui)
		self.crystalDimInputs(value)
		self.crystalPixPerMicInputs()
		self.crystalAbsCoeffInputs()
		self.crystalMakeButton(MainGui)

	def crystalMakeButton(self,MainGui):
		# create a 'make' button here to add this crystal to the list of added crystals
		crystMakeButton = Button(self.currentStrategyCrystal,text="Make",command= lambda: self.addMadeCryst(MainGui))
		crystMakeButton.grid(row=4,column=0,columnspan=3,pady=5)

	def addMadeCryst(self,MainGui):
		# make a new crystal object from above entered parameters and add to both listbox crystal list and
		# also list of crystal objects
		newCryst = crystals(MainGui.crystMakeName.get(),self.CrystalType.get(),self.CrystalDimX.get(),
							self.CrystalDimY.get(),self.CrystalDimZ.get(),self.CrystalPixPerMic.get(),
							self.CrystalAbsorpCoeff.get())

		# check the crystal parameters are valid
		ErrorMessage = MainGui.checkCrystInputs(newCryst)
		if ErrorMessage != "":
					tkMessageBox.showinfo("Invalid Input File",ErrorMessage)
		else:
			# add new crystal to list of loaded crystals
			MainGui.addCrystalToList(newCryst)

			# once this function runs, the toplevel window should be exited
			self.master.destroy()
