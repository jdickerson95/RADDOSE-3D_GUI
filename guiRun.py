#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
RADDOSE-3D gui template
First attempt --> 25 March 2015. Last seen on 1 April 2015
"""

from Tkinter import *
from PIL import Image, ImageTk
from ttk import *
import tkMessageBox
import tkFileDialog
import Tkinter as tk
import sys
import os
#from GUI2RADDOSE3DINPUT import *

#####################################################################################################
class beams(object):
	# this class is for beam parameters for a loaded or created beam
	def __init__(self,beamName="",beamType="",beamFWHM=[],
				 beamFlux=0,beamEnergy=0,beamRectColl=[], beamPixelSize=[]):
		self.beamName     	= beamName
		self.type         	= beamType
		self.fwhm         	= beamFWHM
		self.flux         	= beamFlux
		self.energy       	= beamEnergy
		self.collimation  	= beamRectColl
		self.pixelSize		= beamPixelSize

#####################################################################################################
class crystals(object):
	# this class is for crystal parameters for a loaded or created crystal
	def __init__(self,crystName="",crystType="",crystDimX=0,crystDimY=0,
				 crystDimZ=0,crystPixPerMic=0,crystAbsorpCoeff=""):
		self.crystName        = crystName
		self.type             = crystType
		self.crystDimX        = crystDimX
		self.crystDimY        = crystDimY
		self.crystDimZ        = crystDimZ
		self.pixelsPerMicron  = crystPixPerMic
		self.absCoefCalc      = crystAbsorpCoeff

#####################################################################################################
class wedges(object):
	# this class is for wedge parameters for a loaded or created wedge
	def __init__(self,angStart="",angStop="",exposTime=""):
		self.angStart     = angStart
		self.angStop      = angStop
		self.exposureTime = exposTime

#####################################################################################################
class dynamicOptionMenu(OptionMenu):
	# this little class is for a small option menu from which a dropdown selection box of both loaded
	# crystals and beams can be added to the current strategy - in the right window of the gui
	def __init__(self, *args, **kw):
		self._command = kw.get("command")
		OptionMenu.__init__(self, *args, **kw)
	def addOption(self, label):
		self["menu"].add_command(label=label,
		command=tk._setit(variable, label, self._command))

#####################################################################################################
class VerticalScrolledFrame(Frame):
  	# this class is for a vertical scrolled frame that actually seems to work!
    def __init__(self, parent, *args, **kw):
        Frame.__init__(self, parent, *args, **kw)

        # create a canvas object and a vertical scrollbar for scrolling it
        vscrollbar = Scrollbar(self, orient=VERTICAL)
        vscrollbar.pack(fill=Y, side=RIGHT, expand=False)
        canvas = Canvas(self, bd=0, highlightthickness=0,
                        yscrollcommand=vscrollbar.set)
        canvas.pack(side=LEFT, fill=BOTH, expand=True)
        vscrollbar.config(command=canvas.yview)

        # reset the view
        canvas.xview_moveto(0)
        canvas.yview_moveto(0)

        # make a style for my vertical scroll frame widget here
        vertScrollStyleFrame = Style()
        vertScrollStyleFrame.configure('vertScrollStyle.TFrame',background='#005b96',foreground='#005b96')

        # create a frame inside the canvas which will be scrolled with it
        self.interior = interior = Frame(canvas,style='vertScrollStyle.TFrame')
        interior_id = canvas.create_window(0, 0, window=interior,
                                           anchor=NW)

        # track changes to the canvas and frame width and sync them,
        # also updating the scrollbar
        def _configure_interior(event):
            # update the scrollbars to match the size of the inner frame
            size = (interior.winfo_reqwidth(), interior.winfo_reqheight())
            canvas.config(scrollregion="0 0 %s %s" % size)
            if interior.winfo_reqwidth() != canvas.winfo_width():
                # update the canvas's width to fit the inner frame
                canvas.config(width=interior.winfo_reqwidth())
        interior.bind('<Configure>', _configure_interior)

        def _configure_canvas(event):
            if interior.winfo_reqwidth() != canvas.winfo_width():
                # update the inner frame's width to fill the canvas
                canvas.itemconfigure(interior_id, width=canvas.winfo_width())
        canvas.bind('<Configure>', _configure_canvas)

#####################################################################################################
class toggledFrame(Frame):
		# this is class to create a toggle frame - so that you can hide/expand a certain part of the window
		# from view
	def __init__(self, parent, text='',**options):
		Frame.__init__(self, parent, **options)
		self.show=IntVar()
		self.show.set(0)

		# make a style for my toggle frame widgets here
		toggleStyleFrame = Style()
		toggleStyleFrame.configure('teststyle.TFrame',background='#005b96',foreground='#005b96')
		toggleStyleLabel = Style()
		toggleStyleLabel.configure('teststyle.TLabel',background='#005b96',foreground='white',font=("Helvetica", 16))

		# make the frames and labels for my toggle box here
		self.titleFrame=Frame(self,style='teststyle.TFrame')
		self.titleFrame.pack(fill=X, expand=1)
		Label(self.titleFrame, text=text,style='teststyle.TLabel').pack(side=LEFT, fill=X, expand=1,padx=5)
		self.toggleButton=Checkbutton(self.titleFrame, width=2,text='+', command=self.toggle,
										  variable=self.show, style='Toolbutton')
		self.toggleButton.pack(side=LEFT)
		self.subFrame=Frame(self, relief=SUNKEN,borderwidth=1,style='teststyle.TFrame')
	def toggle(self):
		if bool(self.show.get()):
		    self.subFrame.pack(fill=X, expand=1)
		    self.toggleButton.configure(text='-')
		else:
		    self.subFrame.forget()
		    self.toggleButton.configure(text='+')

#####################################################################################################
class RADDOSEgui(Frame):
	# this is the main RADDOSE gui class here

	def __init__(self, parent):
		Frame.__init__(self, parent)

		self.parent = parent
		self.initUI()

	def initUI(self):
		# this is to delegate the creation of the user interface to the initUI() method

		# define the colourscheme here
		self.darkcolour = "#383838"
		self.lightcolour = "#2d5867"
		self.headercolour = "#1e2e4d"

		# give the gui a title here
		self.parent.title("gui test")

		# set style for the window here
		self.style = Style()
		self.style.theme_use("default")
		self.style.configure("TFrame", background="#333")

		# set style for the header here
		styleHeader = Style()
		styleHeader.configure("Header.TFrame", foreground="black", background=self.headercolour)

		# set style for the body background here
		styleBodyBackground = Style()
		styleBodyBackground.configure("BodyBackground.TFrame", foreground="black", background=self.darkcolour)

		# set a basic style for the individual subframes within the body frame
		styleBodyLabelFrame = Style()
		styleBodyLabelFrame.configure("BodyGroovy.TFrame", foreground="black",
									background=self.lightcolour,relief=GROOVE,borderwidth=5)

		# make a style for the frame which surrounds entry box and label combos
		styleInputBoxesFrame = Style()
		styleInputBoxesFrame.configure("inputBoxes.TFrame",foreground="white",
									   background=self.lightcolour,borderwidth=5)
		styleInputBoxes = Style()
		styleInputBoxes.configure("inputBoxes.TLabel",foreground="white",
							      background=self.lightcolour,borderwidth=5,font=("Helvetica", 12))

		# make a style for the added gui header title label
		styleTitle = Style()
		styleTitle.configure("Title.TLabel",foreground="white",
							 background=self.headercolour,font=("Helvetica", 26))

		# make an additional style for the added label titles to labelframe widgets
		styleLabelFrameTitle = Style()
		styleLabelFrameTitle.configure("labelFrameTitle.TLabel",foreground="white",
									   background=self.lightcolour,font=("Helvetica", 14))

		# make a style for the 'load/make a crystal/beam' frames
		styleMakeABeamFrame = Style()
		styleMakeABeamFrame.configure("MakeABeam.TFrame",foreground="white",relief=GROOVE,
									  background=self.lightcolour,font=("Helvetica", 14),borderwidth=5)

		#####################################################################################################
		# make a menu bar header here
		menubar = Menu(self.parent)
		self.parent.config(menu=menubar)
		fileMenu = Menu(menubar)
		fileMenu.add_command(label="Exit", command=self._quit)
		menubar.add_cascade(label="File", menu=fileMenu)

		#####################################################################################################
		# geometry management for the gui
		self.pack(fill=BOTH, expand=1)

		# the header frame here
		FrameHeader = Frame(self,style="Header.TFrame")
		FrameHeader.pack(fill=BOTH)

		# the body frame here
		FrameBody = Frame(self,style="BodyBackground.TFrame")
		FrameBody.pack(fill=BOTH,expand=1)

		# make a label in the header frame
		labelHeader = Label(FrameHeader,text="Data Collection Dose Stategy GUI",style="Title.TLabel")
		labelHeader.pack()

		# in body frame make a left, middle and right side
		FrameBodyLeft = Frame(FrameBody,style="BodyBackground.TFrame")
		FrameBodyLeft.pack(side=LEFT,fill=BOTH,expand=1)
		FrameBodyMiddle = Frame(FrameBody,style="BodyBackground.TFrame")
		FrameBodyMiddle.pack(side=LEFT,fill=BOTH,expand=1)
		FrameBodyRight = Frame(FrameBody,style="BodyBackground.TFrame")
		FrameBodyRight.pack(side=LEFT,fill=BOTH,expand=1)

		# in left body frame make a top and bottom
		l = Label(FrameBodyLeft,text="Help/Suggestion Dialogue",style="labelFrameTitle.TLabel")
		FrameBodyLeftTop = LabelFrame(FrameBodyLeft,labelwidget=l,style="BodyGroovy.TFrame")
		FrameBodyLeftTop.pack(side=TOP,padx=10, pady=10,fill=BOTH)

		l = Label(FrameBodyLeft,text="Summary/Output Window",style="labelFrameTitle.TLabel")
		FrameBodyLeftBottom = LabelFrame(FrameBodyLeft,labelwidget=l,style="BodyGroovy.TFrame")
		FrameBodyLeftBottom.pack(side=BOTTOM,padx=10, pady=10,fill=BOTH,expand=1)

		# in middle body frame make a top and bottom
		l = Label(FrameBodyMiddle,text="Make-a-crystal",style="labelFrameTitle.TLabel")
		FrameBodyMiddleTop = LabelFrame(FrameBodyMiddle,labelwidget=l,style="BodyGroovy.TFrame")
		FrameBodyMiddleTop.pack(side=TOP,padx=10, pady=10,fill=BOTH,expand=1)

		l = Label(FrameBodyMiddle,text="Make-a-beam",style="labelFrameTitle.TLabel")
		FrameBodyMiddleBottom = LabelFrame(FrameBodyMiddle,labelwidget=l,style="BodyGroovy.TFrame")
		FrameBodyMiddleBottom.pack(side=BOTTOM,padx=10, pady=10,fill=BOTH,expand=1)

		# in right body frame make a LabelFrame in which a strategy can be created and run
		l = Label(FrameBodyRight,text="Design-a-strategy",style="labelFrameTitle.TLabel")
		LabelFrameBodyRight = LabelFrame(FrameBodyRight,labelwidget=l,style="BodyGroovy.TFrame")
		LabelFrameBodyRight.pack(side=TOP,padx=10, pady=10,fill=BOTH,expand=1)


		#####################################################################################################
		# for top left body --> help/suggestion dialogue box
		self.varHelpBox = StringVar()
		self.readHelpFile()

		scrollbarStrategyList = Scrollbar(FrameBodyLeftTop, orient=VERTICAL)
		T = Text(FrameBodyLeftTop, height=8, width=35,wrap=WORD)
		scrollbarStrategyList.pack(side=LEFT,fill=Y)
		T.pack(side=LEFT,expand=True)
		scrollbarStrategyList.config(command=T.yview)
		T.config(yscrollcommand=scrollbarStrategyList.set)
		quote = self.varHelpBox.get()
		T.insert(END, quote*2)

		miniButtonFrame = Frame(FrameBodyLeftTop,style="labelFrameTitle.TLabel")
		miniButtonFrame.pack(side=RIGHT,padx=5)
		helpButton = Button(miniButtonFrame, text="Help",command=self.clickHelp)
		helpButton.pack(side=TOP,pady=5)
		printButton = Button(miniButtonFrame, text="Print")
		printButton.pack(side=BOTTOM,pady=5)


		#####################################################################################################
		# for bottom left body --> summary/output window
		self.raddose3Dinputtxt = StringVar()
		scrollbarRaddoseInputFile = Scrollbar(FrameBodyLeftBottom, orient=VERTICAL)
		self.inputtxt = Text(FrameBodyLeftBottom, height=100,width=60,wrap=WORD,font=("Helvetica", 8))
		scrollbarRaddoseInputFile.pack(side=LEFT,fill=Y)
		self.inputtxt.pack(side=LEFT,expand=True)
		scrollbarStrategyList.config(command=self.inputtxt.yview)
		self.inputtxt.config(yscrollcommand=scrollbarRaddoseInputFile.set)
		quote = self.raddose3Dinputtxt.get()
		# delete all current text and add new text to text widget
		self.inputtxt.delete(1.0, END)
		self.inputtxt.insert(END, quote*2)


		#####################################################################################################
		# for top middle body --> make-a-crystal window

		# make labelframe in which a crystal can be loaded and saved
		l = Label(FrameBodyMiddleTop,text="Load a crystal",style="labelFrameTitle.TLabel")
		crystLoadLabelFrame = LabelFrame(FrameBodyMiddleTop,labelwidget=l,style="MakeABeam.TFrame")
		crystLoadLabelFrame.pack(side=TOP,padx=10, pady=0,fill=BOTH)

		# add crystal 'load' option to crystLoadLabelFrame frame here
		crystLoadLabel = Label(crystLoadLabelFrame,text="Crystal Load",style="inputBoxes.TLabel")
		crystLoadLabel.grid(row=0, column=0,pady=5,padx=6,sticky=W+E)
		self.crystLoad = StringVar()
		self.crystLoadBox = Entry(crystLoadLabelFrame,textvariable=self.crystLoad)
		self.crystLoadBox.grid(row=0, column=1,columnspan=2,pady=5,sticky=W+E)
		addCrystButton = Button(crystLoadLabelFrame,text="Find File",command=self.clickCrystLoad)
		addCrystButton.grid(row=0, column=3,pady=5,padx=6,sticky=W+E)

		# add crystal naming option to crystLoadLabelFrame frame here. Name is what user wishes to
		# call the current crystal for future reference
		crystLoadNameLabel = Label(crystLoadLabelFrame,text="Crystal Name",style="inputBoxes.TLabel")
		crystLoadNameLabel.grid(row=1, column=0,pady=5,padx=6,sticky=W+E)
		self.crystLoadName = StringVar()
		crystLoadNameBox = Entry(crystLoadLabelFrame,textvariable=self.crystLoadName)
		crystLoadNameBox.grid(row=1, column=1,columnspan=2,pady=5,sticky=W+E)
		addCrystButton = Button(crystLoadLabelFrame,text="Add",command=self.clickCrystAdd)
		addCrystButton.grid(row=1, column=3,pady=5,padx=6,sticky=W+E)

		# make a labelframe in which a crystal can be made from scratch and saved
		l = Label(FrameBodyMiddleTop,text="Make a crystal",style="labelFrameTitle.TLabel")
		crystMakeLabelFrame = LabelFrame(FrameBodyMiddleTop,labelwidget=l,style="MakeABeam.TFrame")
		crystMakeLabelFrame.pack(side=TOP,padx=10, pady=5,fill=BOTH)

		# allow user to give a name to a crystal and make a crystal from scratch here via button interaction
		crystMakeNameLabel = Label(crystMakeLabelFrame,text="Crystal Name",style="inputBoxes.TLabel")
		crystMakeNameLabel.grid(row=1, column=0,pady=5,padx=6,sticky=W+E)
		self.crystMakeName = StringVar()
		crystMakeNameBox = Entry(crystMakeLabelFrame,textvariable=self.crystMakeName)
		crystMakeNameBox.grid(row=1, column=1,columnspan=2,pady=5,sticky=W+E)
		makeCrystButton = Button(crystMakeLabelFrame,text="Make",command=self.clickCrystMake)
		makeCrystButton.grid(row=1, column=3,pady=5,padx=6,sticky=W+E)

		# make a listbox frame in options frame to show added crystals. The listbox of added
		# crystals is created here, along with a scrollbar
		crystListFrame = Frame(FrameBodyMiddleTop,style="BodyGroovy.TFrame")
		crystListFrame.pack(side=TOP,fill=BOTH,padx=5,pady=0)
		scrollbarCrystList = Scrollbar(crystListFrame, orient=VERTICAL)

		# want to make a list of crystal object instances (here two example crystals are defined)
		exampleCryst = crystals('Example crystal','Cuboid',10,20,30,1,'Average')
		exampleCryst2 = crystals('Example crystal 2','Cuboid',30,20,10,2,'RADDOSE')
		self.crystList = [exampleCryst,exampleCryst2]

		self.crystListbox = Listbox(crystListFrame,yscrollcommand=scrollbarCrystList.set,height=1)
		for cryst in self.crystList:
		    self.crystListbox.insert(END, cryst.crystName)
		self.crystListbox.update_idletasks()
		self.crystListbox.bind("<<ListboxSelect>>", self.onSelect)
		scrollbarCrystList.config(command=self.crystListbox.yview)
		self.crystListbox.pack(side=LEFT,padx=10,pady=5,fill=BOTH,expand=True)
		scrollbarCrystList.pack(side=RIGHT, fill=Y,pady=5)
		self.var3 = StringVar()

		# this button will view the currently selected crystal in the list
		viewCrystButton = Button(FrameBodyMiddleTop, text="View",command=self.clickCrystView)
		viewCrystButton.pack(side=LEFT,padx=10, pady=5,fill=X,anchor=N,expand=True)

		# this button deletes the currently selected crystal from the listbox strategy list above
		deleteCrystButton = Button(FrameBodyMiddleTop, text="Delete",command=self.deleteCryst)
		deleteCrystButton.pack(side=LEFT,padx=10, pady=5,fill=X,anchor=N)


		#####################################################################################################
		# for bottom middle body --> make-a-beam window

		# make labelframe in which a beam can be loaded and saved
		l = Label(FrameBodyMiddleBottom,text="Load a beam",style="labelFrameTitle.TLabel")
		beamLoadLabelFrame = LabelFrame(FrameBodyMiddleBottom,labelwidget=l,style="MakeABeam.TFrame")
		beamLoadLabelFrame.pack(side=TOP,padx=10, pady=0,fill=BOTH)

		# add beam 'load' option to beamLoadLabelFrame frame here
		beamLoadLabel = Label(beamLoadLabelFrame,text="Beam Load",style="inputBoxes.TLabel")
		beamLoadLabel.grid(row=0, column=0,pady=5,padx=6,sticky=W+E)
		self.beamLoad = StringVar()
		self.beamLoadBox = Entry(beamLoadLabelFrame,textvariable=self.beamLoad)
		self.beamLoadBox.grid(row=0, column=1,columnspan=2,pady=5,sticky=W+E)
		addBeamButton = Button(beamLoadLabelFrame,text="Find File",command=self.clickBeamLoad)
		addBeamButton.grid(row=0, column=3,pady=5,padx=6,sticky=W+E)

		# add beam naming option to beamLoadLabelFrame frame here. Name is what user wishes to
		# call the current beam for future reference
		beamLoadNameLabel = Label(beamLoadLabelFrame,text="Beam Name",style="inputBoxes.TLabel")
		beamLoadNameLabel.grid(row=1, column=0,pady=5,padx=6,sticky=W+E)
		self.beamLoadName = StringVar()
		beamLoadNameBox = Entry(beamLoadLabelFrame,textvariable=self.beamLoadName)
		beamLoadNameBox.grid(row=1, column=1,columnspan=2,pady=5,sticky=W+E)
		addBeamButton = Button(beamLoadLabelFrame,text="Add",command=self.clickBeamAdd)
		addBeamButton.grid(row=1, column=3,pady=5,padx=6,sticky=W+E)

		# make a labelframe in which a beam can be made from scratch and saved
		l = Label(FrameBodyMiddleBottom,text="Make a beam",style="labelFrameTitle.TLabel")
		beamMakeLabelFrame = LabelFrame(FrameBodyMiddleBottom,labelwidget=l,style="MakeABeam.TFrame")
		beamMakeLabelFrame.pack(side=TOP,padx=10, pady=5,fill=BOTH)

		# allow user to give a name to a beam and make a beam from scratch here via button interaction
		beamMakeNameLabel = Label(beamMakeLabelFrame,text="Beam Name",style="inputBoxes.TLabel")
		beamMakeNameLabel.grid(row=1, column=0,pady=0,padx=6,sticky=W+E)
		self.beamMakeName = StringVar()
		beamMakeNameBox = Entry(beamMakeLabelFrame,textvariable=self.beamMakeName)
		beamMakeNameBox.grid(row=1, column=1,columnspan=2,pady=5,sticky=W+E)
		makeBeamButton = Button(beamMakeLabelFrame,text="Make",command=self.clickBeamMake)
		makeBeamButton.grid(row=1, column=3,pady=5,padx=6,sticky=W+E)

		# make a listbox frame in options frame to show added beams. The listbox of added
		# beams is created here, along with a scrollbar
		beamListFrame = Frame(FrameBodyMiddleBottom,style="BodyGroovy.TFrame")
		beamListFrame.pack(side=TOP,fill=BOTH,padx=5,pady=0)
		scrollbarBeamList = Scrollbar(beamListFrame, orient=VERTICAL)

		# want to make a list of beam object instances (here two example beams are defined)
		exampleBeam = beams('Example beam',"Gaussian",[25,25],10000000000,10,[100,100],[2,2])
		exampleBeam2 = beams('Example beam 2',"Top Hat",[50,50],20000000000,12,[120,120],[1,1])
		self.beamList = [exampleBeam,exampleBeam2]

		self.beamListbox = Listbox(beamListFrame,yscrollcommand=scrollbarBeamList.set,height=1)
		for beam in self.beamList:
		    self.beamListbox.insert(END, beam.beamName)
		self.beamListbox.update_idletasks()
		self.beamListbox.bind("<<ListboxSelect>>", self.onSelect)
		scrollbarBeamList.config(command=self.beamListbox.yview)
		self.beamListbox.pack(side=LEFT,padx=10,pady=5,fill=BOTH,expand=True)
		scrollbarBeamList.pack(side=RIGHT, fill=Y,pady=5)
		self.var3 = StringVar()

		# this button will view the currently selected crystal in the list
		viewBeamButton = Button(FrameBodyMiddleBottom, text="View",command=self.clickBeamView)
		viewBeamButton.pack(side=LEFT,padx=10, pady=5,fill=X,anchor=N,expand=True)

		# this button deletes the currently selected crystal from the listbox strategy list above
		deleteBeamButton = Button(FrameBodyMiddleBottom, text="Delete",command=self.deleteBeam)
		deleteBeamButton.pack(side=LEFT,padx=10, pady=5,fill=X,anchor=N)


		#####################################################################################################
		# for right body --> design-a-strategy window

		# make labelframe in which a crystal can be chosen from list of added crystals
		l = Label(LabelFrameBodyRight,text="Choose a crystal",style="labelFrameTitle.TLabel")
		chooseCrystFrame = LabelFrame(LabelFrameBodyRight,labelwidget=l,style="MakeABeam.TFrame")
		chooseCrystFrame.pack(side=TOP,padx=10, pady=0,fill=BOTH)

		# make a dropdown list to choose one of added crystals
		self.crystChoice = StringVar(self)
		self.crystChoices = [cryst.crystName for cryst in self.crystList]
		self.crystChoiceMenu = dynamicOptionMenu(chooseCrystFrame, self.crystChoice,self.crystChoices[0],*self.crystChoices)
		self.crystChoiceMenu.pack(side=TOP, padx=10, pady=10,fill=BOTH)

          # make a labelframe in which the desired beam strategy can be added (including the specification of wedges)
		l = Label(LabelFrameBodyRight,text="Choose a beam",style="labelFrameTitle.TLabel")
		chooseBeamStratFrame = LabelFrame(LabelFrameBodyRight,labelwidget=l,style="MakeABeam.TFrame")
		chooseBeamStratFrame.pack(side=TOP,padx=10, pady=0,fill=BOTH)

          # make a dropdown list to choose a beam from the currently added beam list to add to the treeview of beam strategies
		# created below
		self.beamChoice = StringVar(self)
		self.beamChoices = [bm.beamName for bm in self.beamList]
		self.beamChoiceMenu = dynamicOptionMenu(chooseBeamStratFrame, self.beamChoice,self.beamChoices[0],*self.beamChoices)
		self.beamChoiceMenu.pack(side=TOP, padx=10, pady=0,fill=BOTH)

		# make a labelframe in which the desired beam strategy can be added (including the specification of wedges)
		l = Label(LabelFrameBodyRight,text="Choose exposure strategy",style="labelFrameTitle.TLabel")
		chooseBeamStratFrame = LabelFrame(LabelFrameBodyRight,labelwidget=l,style="MakeABeam.TFrame")
		chooseBeamStratFrame.pack(side=TOP,padx=10, pady=0,fill=BOTH)

		# make a button to incorporate the currently selected beam (in beam dropdown list above) to the treeview of beam
		# strategies below
		beamStratButton = Button(chooseBeamStratFrame,text='Add Exposure Strategy',command=self.clickAddBeamStrategy)
		beamStratButton.pack(side=TOP, padx=10, pady=0,fill=X,expand=True)

		# make a treeview to show coupled beam and wedge strategies to be used with the specified crystal above
		self.BeamStratTree = Treeview(chooseBeamStratFrame)
		self.BeamStratTree["columns"]=("one","two","three","four")
		self.BeamStratTree.column("#0",width=30)
		self.BeamStratTree.column("one", width=100 )
		self.BeamStratTree.column("two", width=70)
		self.BeamStratTree.column("three", width=70)
		self.BeamStratTree.column("four", width=90)
		self.BeamStratTree.heading("one", text="Beam")
		self.BeamStratTree.heading("two", text="Start Angle")
		self.BeamStratTree.heading("three", text="Stop Angle")
		self.BeamStratTree.heading("four", text="Exposure Time")
		# define a counter here to specify the number of the beam+wedge strategy in the treeview of beam strategies.
		# also create a list of indices of inserted entries in treeview, to allow easier deletion by index later. Also
		# create lists of beam and wedge objects corresponding to entries in the treeview list.
		self.BeamStratcounter = 1
		self.treeviewIndexlist = []
		self.beamList2Run,self.wedgeList2Run = [],[]
		self.BeamStratTree.pack(side=TOP,padx=10, pady=10,fill=BOTH)

		# make a button to remove the last beam+wedge entry from the treeview list of beam+wedge strategies for current
		# crystal
		beamStratRemoveButton = Button(chooseBeamStratFrame,text='Remove last entry',command=self.clickRemoveBeamStrategy)
		beamStratRemoveButton.pack(side=TOP, padx=10, pady=0,fill=X,expand=True)

		# make a labelframe. This label frame is for Running the experiment once
		# the crystal, beam and wedge has been defined.
		l = Label(LabelFrameBodyRight,text="Run Strategy",style="labelFrameTitle.TLabel")
		runStrategyFrame = LabelFrame(LabelFrameBodyRight,labelwidget=l,style="MakeABeam.TFrame")
		runStrategyFrame.pack(side=BOTTOM,padx=10, pady=10,fill=BOTH)

		# make a box that allows user to uniquely name the experiment (i.e. the
		#crystal, beam and wedge combination) before running.
		expLoadNameLabel = Label(runStrategyFrame,text="Experiment Name",style="inputBoxes.TLabel")
		expLoadNameLabel.grid(row=0, column=0,pady=5,padx=6,sticky=W+E)
		self.expLoadName = StringVar()
		expLoadNameBox = Entry(runStrategyFrame,textvariable=self.expLoadName)
		expLoadNameBox.grid(row=0, column=1, columnspan=2, pady=5,sticky=W+E)

		# make a run button to run the currently defined strategy
		runButton = Button(runStrategyFrame,text="Run",command=self.runExperiment)
		runButton.grid(row=1, columnspan=3, pady=10,padx=10,sticky=W+E)

	#####################################################################################################
	# below is a list of button actions in the gui

	def runExperiment(self):
		"""Run the experiment defined by the specified crystal, beam and wedge

		This function checks whether the experiment name already exists. If it
		doesn't already exist then it will create a directory with the current
		experiment name and then run RADDOSE-3D which the chosen crystal, beam
		and wedge paramters. Otherwise, if the experiment name already exists
		then a pop up dialogue is created which asks the user whether they want
		to overwrite the current experiment that already exists under the same
		name.

		=================
		Keyword arguments
		=================
		No explicit user defined parameters. Only the object is required for
		implicit input.

		=================
		Return parameters
		=================
		No explicit return parameters
		"""
		expName = str(self.expLoadName.get()) #get experiment name as a string

		#First check that the experiment name hasn't been left blank. If so then
		#tell user that they need to supply an experiment name.
		#Otherwise check if the experiment name already exists as a directory in
		#the current folder.if it does then ask the user if they want to
		#overwrite the previous experiment.
		#Otherwise create the experiment directory and run the experiment.
		if not expName:
			string = """No experiment name has been given.\nPlease give a name to the experiment that you wish to run in the 'Experiment Name' field.
			""" %()
			tkMessageBox.showinfo( "No Experiment Name", string)
		elif os.path.exists(expName):
			addQuery = tkMessageBox.askquestion( "Duplicate Experiment Names",
			"Experiment name %s already exists. Do you want to overwrite this experiment?"%(expName))
			if addQuery == 'yes':
				self.runStrategy()
			else:
				pass
		else:
			os.mkdir(expName)
			self.runStrategy()

	def runStrategy(self):
		"""Run RADDOSE-3D given specified crystal, beam and wedge objects

		This function writes an input file from the given crystal, beam and
		wedge objects. Then it runs RADDOSE-3D with that input file and puts all
		of the output files in the corresponding experiment folder.

		=================
		Keyword arguments
		=================
		No explicit user defined parameters. Only the object is required for
		implicit input.

		=================
		Return parameters
		=================
		No explicit return parameters
		"""
		self.writeRaddose3DInputFile()

	def clickAddBeamStrategy(self):
		# what happens when add beam strategy button clicked. Makes a new small window allowing
		# manual entry of wedge parameters for currently selected beam
		self.top_WedgeMaker=Toplevel()
		self.top_WedgeMaker.title("Make a wedge")

		# give the new window a dark background colour
		self.top_WedgeMaker.configure(bg=self.darkcolour)

		# Wedge inputs here:
		l = Label(self.top_WedgeMaker,text="Wedge",style="labelFrameTitle.TLabel")
		currentStrategyWedge = LabelFrame(self.top_WedgeMaker,labelwidget=l,
											style="MakeABeam.TFrame")
		currentStrategyWedge.pack(side=TOP,padx=10, pady=10,fill=BOTH,expand=TRUE)

		# Wedge input 1 --> Wedge angular range (start)
		WedgeinputFrame1 = Frame(currentStrategyWedge,style="inputBoxes.TFrame")
		WedgeinputFrame1.grid(row=0,column=0)
		WedgeinputLabel1 = Label(WedgeinputFrame1,text="Angular Range (Start)",style="inputBoxes.TLabel")
		WedgeinputLabel1.pack(side=LEFT,pady=5,padx=6)
		self.WedgeAngRangeStart = StringVar()
		WedgeinputBox1 = Entry(WedgeinputFrame1,textvariable=self.WedgeAngRangeStart,width=5)
		WedgeinputBox1.pack(side=LEFT,pady=5,padx=6)

		# Wedge input 2 --> Wedge angular range (stop)
		WedgeinputFrame2 = Frame(currentStrategyWedge,style="inputBoxes.TFrame")
		WedgeinputFrame2.grid(row=1,column=0)
		WedgeinputLabel2 = Label(WedgeinputFrame2,text="Angular Range (Stop)",style="inputBoxes.TLabel")
		WedgeinputLabel2.pack(side=LEFT,pady=5,padx=6)
		self.WedgeAngRangeStop = StringVar()
		WedgeinputBox2 = Entry(WedgeinputFrame2,textvariable=self.WedgeAngRangeStop,width=5)
		WedgeinputBox2.pack(side=LEFT,pady=5,padx=6)

		# Wedge input 3 --> Wedge total exposure time
		WedgeinputFrame3 = Frame(currentStrategyWedge,style="inputBoxes.TFrame")
		WedgeinputFrame3.grid(row=2,column=0)
		WedgeinputLabel3 = Label(WedgeinputFrame3,text="Total Exposure Time",style="inputBoxes.TLabel")
		WedgeinputLabel3.pack(side=LEFT,pady=5,padx=6)
		self.WedgeExposTime = StringVar()
		WedgeinputBox3 = Entry(WedgeinputFrame3,textvariable=self.WedgeExposTime,width=5)
		WedgeinputBox3.pack(side=LEFT,pady=5,padx=6)

		# make an example visual wedge here
		C = Canvas(currentStrategyWedge, bg=self.lightcolour, height=100, width=100)
		coord = 0, 20, 100, 100
		C.create_arc(coord, start=0, extent=150, fill=self.darkcolour)
		C.grid(row=0,column=1,rowspan=4)

		# create a 'make' button here to add this wedge to the list of added beam strategies in treeview list
		wedgeMakeButton = Button(currentStrategyWedge,text="Make",command=self.addBeamStrategy)
		wedgeMakeButton.grid(row=4,column=0,pady=5)

	def addBeamStrategy(self):
		# add a new beam+wedge strategy to the treeview of coupled beam+wedge strategies to be input into RADDOSE3D

		# make a new wedge object
		currentWedge = wedges(self.WedgeAngRangeStart.get(),self.WedgeAngRangeStop.get(),self.WedgeExposTime.get())
		Index = self.BeamStratTree.insert("" , len(self.treeviewIndexlist),    text=str(len(self.treeviewIndexlist)+1),
								 values=(self.beamChoice.get(),currentWedge.angStart,currentWedge.angStop,currentWedge.exposureTime))
		self.treeviewIndexlist.append(Index)
		print self.treeviewIndexlist

		# get the index of the selected beam from the list of added beams (in the optionmenu list)
		self.currentBeamIndex = [bm.beamName for bm in self.beamList].index(self.beamChoice.get())
		# get the selected beam object here
		currentBeam = self.beamList[self.currentBeamIndex]
		# add the current beam to the list of beams to be run
		self.beamList2Run.append(currentBeam)
		# add the current wedge information for this beam to another list
		self.wedgeList2Run.append(currentWedge)

		# once this function runs, the toplevel window should be exited
		self.top_WedgeMaker.destroy()

	def clickRemoveBeamStrategy(self):
		# what happens when the remove beam strategy button is clicked. This removes the last entry in the treeview
		# of beam+wedge couples currently saved.

		# first find last entry in treeview
		lastIndex = self.treeviewIndexlist[-1]

		# delete this entry from the treeview of beam+wedge couples
		self.BeamStratTree.delete(lastIndex)

		# remove this index from the reference list of treeview indices
		self.treeviewIndexlist.pop(-1)

		# remove the last object from the list of added beam and wedge objects to be written into RADDOSE input script
		# to correspond to updated treeview list
		self.beamList2Run.pop(-1)
		self.wedgeList2Run.pop(-1)

	def refreshCrystChoices(self):
	    # Reset the option menu of added crystals and delete crystals not now
	    # included in the list of added crystals
	    self.crystChoice.set('')
	    self.crystChoiceMenu['menu'].delete(0, 'end')

	    # Insert list of new options (tk._setit hooks them up to self.crystChoice)
	    new_CrystChoices = [cryst.crystName for cryst in self.crystList]
	    for choice in new_CrystChoices:
	        self.crystChoiceMenu['menu'].add_command(label=choice, command=tk._setit(self.crystChoice, choice))

	# functions for the manipulation of crystal files and parameters
	def clickCrystView(self):
		# what happens when crystal view button clicked
		crystToView = self.crystList[self.crystListbox.index(ANCHOR)]
		crystInfo ="""Name: %s\nType: %s\nDimensions: %s %s %s\nPixels per Micron: %s\nAbsorption Coefficient: %s
		           """ %(str(crystToView.crystName),str(crystToView.crystType),
		          		str(crystToView.crystDimX),str(crystToView.crystDimY),
		          		str(crystToView.crystDimZ),str(crystToView.crystPixPerMic),
		          		str(crystToView.crystAbsorpCoeff))
		tkMessageBox.showinfo( "View Crystal Information", crystInfo)

		print str(crystToView.crystDimX)
		print str(crystToView.crystDimY)
		print str(crystToView.crystDimZ)

	def deleteCryst(self):
		# delete the selected crystal from the listbox of added crystals. Also remove the
		# corresponding crystal object from the crystalList list
		self.crystListbox.delete(ANCHOR)
		self.crystList.pop(self.crystListbox.index(ANCHOR))
		# refresh the option menu of added crystals to keep it up to date
		self.refreshCrystChoices()

	def clickCrystMake(self):
		# what happens when crystal make button clicked. Makes a new small window allowing
		# manual entry of crystal parameters
		self.top_CrystMaker=Toplevel()
		self.top_CrystMaker.title("Make a crystal")

		# give the new window a dark background colour
		self.top_CrystMaker.configure(bg=self.darkcolour)

		# Crystal inputs here:
		l = Label(self.top_CrystMaker,text="Crystal",style="labelFrameTitle.TLabel")
		currentStrategyCrystal = LabelFrame(self.top_CrystMaker,labelwidget=l,
											style="MakeABeam.TFrame")
		currentStrategyCrystal.pack(side=TOP,padx=10, pady=10,fill=BOTH,expand=TRUE)

		# Crystal input 1 --> crystal type
		CrystalinputFrame1 = Frame(currentStrategyCrystal,style="inputBoxes.TFrame")
		CrystalinputFrame1.grid(row=0,column=0)
		CrystalinputLabel1 = Label(CrystalinputFrame1,text="Crystal Type",style="inputBoxes.TLabel")
		CrystalinputLabel1.pack(side=LEFT,pady=5,padx=6)
		self.CrystalType = StringVar()
		CrystalinputBox1 = Entry(CrystalinputFrame1,textvariable=self.CrystalType,width=5)
		CrystalinputBox1.pack(side=LEFT,pady=5,padx=6)

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
		CrystalinputBox4 = Entry(CrystalinputFrame4,textvariable=self.CrystalAbsorpCoeff,width=5)
		CrystalinputBox4.pack(side=LEFT,pady=5,padx=6)

		# create a 'make' button here to add this crystal to the list of added crystals
		crystMakeButton = Button(currentStrategyCrystal,text="Make",command=self.addMadeCryst)
		crystMakeButton.grid(row=2,column=0,columnspan=2,pady=5)

	def addMadeCryst(self):
		# make a new crystal object from above entered parameters and add to both listbox crystal list and
		# also list of crystal objects
		newCryst = crystals(self.crystMakeName.get(),self.CrystalType.get(),self.CrystalDimX.get(),
							self.CrystalDimY.get(),self.CrystalDimZ.get(),self.CrystalPixPerMic.get(),
							self.CrystalAbsorpCoeff.get())
		self.crystList.append(newCryst)
		self.crystListbox.insert(END, str(newCryst.crystName))

		# refresh the option menu of added crystals to keep it up to date
		self.refreshCrystChoices()

		# once this function runs, the toplevel window should be exited
		self.top_CrystMaker.destroy()

	def clickCrystLoad(self):
		# what happens when crystal load button clicked
		self.crystLoad = tkFileDialog.askopenfilename(parent=self,title='Open crystal file to load')
		self.crystLoadBox.delete(0,END)
		self.crystLoadBox.insert(0,self.crystLoad)

	def clickCrystAdd(self):
		# what happens when crystal add button clicked
		addQuery = tkMessageBox.askquestion( "Add Crystal?", "Do you want to add crystal %s?"%(str(self.crystLoadName.get())))
		if addQuery == 'yes':
			self.crystListbox.insert(END, str(self.crystLoadName.get()))

			# add a crystal object to the list of crystals (outside of listbox)
			self.crystList.append(crystals(self.crystLoadName.get(),'?','?','?','?','?','?'))

			# also update list of crystal choices used in the right strategy window
			self.refreshCrystChoices()
		else:
			pass

	# functions for the manipulation of beam files and parameters
	def refreshBeamChoices(self):
	    # Reset the option menu of added beam and delete beams not now
	    # included in the list of added beams
	    self.beamChoice.set('')
	    self.beamChoiceMenu['menu'].delete(0, 'end')

	    # Insert list of new options (tk._setit hooks them up to self.beamChoice)
	    new_BeamChoices = [bm.beamName for bm in self.beamList]
	    for choice in new_BeamChoices:
	        self.beamChoiceMenu['menu'].add_command(label=choice, command=tk._setit(self.beamChoice, choice))


	def clickBeamView(self):
		# what happens when beam view button clicked
		beamToView = self.beamList[self.beamListbox.index(ANCHOR)]
		beamInfo ="""Name: %s\nType: %s\nFWHM: %s\nFlux: %s\nEnergy: %s\nRectangular Collimation: %s
		           """ %(str(beamToView.beamName),str(beamToView.beamType),
		          		str(beamToView.beamFWHM),str(beamToView.beamFlux),
		          		str(beamToView.beamEnergy),str(beamToView.beamRectColl))
		tkMessageBox.showinfo( "View Beam Information", beamInfo)

	def deleteBeam(self):
		self.beamListbox.delete(ANCHOR)
		self.beamList.pop(self.beamListbox.index(ANCHOR))
		# also update list of beam choices used in the right strategy window
		self.refreshBeamChoices()

	def clickBeamMake(self):
		# what happens when beam make button clicked. Makes a new small window allowing
		# manual entry of beam parameters
		self.top_BeamMaker=Toplevel()
		self.top_BeamMaker.title("Make a beam")

		# give the new window a dark background colour
		self.top_BeamMaker.configure(bg=self.darkcolour)

		# Beam inputs here:
		l = Label(self.top_BeamMaker,text="Beam",style="labelFrameTitle.TLabel")
		currentStrategyBeam = LabelFrame(self.top_BeamMaker,labelwidget=l,
											style="MakeABeam.TFrame")
		currentStrategyBeam.pack(side=TOP,padx=10, pady=10,fill=BOTH,expand=TRUE)

		# Beam input 1 --> Beam type
		BeaminputFrame1 = Frame(currentStrategyBeam,style="inputBoxes.TFrame")
		BeaminputFrame1.grid(row=0,column=0)
		BeaminputLabel1 = Label(BeaminputFrame1,text="Beam Type",style="inputBoxes.TLabel")
		BeaminputLabel1.pack(side=LEFT,pady=5,padx=6)
		self.BeamType = StringVar()
		BeaminputBox1 = Entry(BeaminputFrame1,textvariable=self.BeamType,width=5)
		BeaminputBox1.pack(side=LEFT,pady=5,padx=6)

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

		# Crystal input 4 --> Energy
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
		beamMakeButton = Button(currentStrategyBeam,text="Make",command=self.addMadeBeam)
		beamMakeButton.grid(row=3,column=0,columnspan=2,pady=5)

	def addMadeBeam(self):
		# make a new beam object from above entered parameters and add to both listbox beam list and
		# also list of beam objects
		newBeam = beams(self.beamMakeName.get(),self.BeamType.get(),
						[self.BeamFWHMVertical.get(),self.BeamFWHMHorizontal.get()],
						self.BeamFlux.get(),self.BeamEnergy.get(),
						[self.BeamRectCollVert.get(),self.BeamRectCollHoriz.get()])
		self.beamList.append(newBeam)
		self.beamListbox.insert(END, str(newBeam.beamName))

		# refresh the option menu of added beams to keep it up to date
		self.refreshBeamChoices()

		# once this function runs, the toplevel window should be exited
		self.top_BeamMaker.destroy()

	def clickBeamLoad(self):
		# what happens when beam load button clicked
		self.beamLoad = tkFileDialog.askopenfilename(parent=self,title='Open beam file to load')
		self.beamLoadBox.delete(0,END)
		self.beamLoadBox.insert(0,self.beamLoad)

	def clickBeamAdd(self):
		# what happens when beam add button clicked
		addQuery = tkMessageBox.askquestion( "Add Beam?", "Do you want to add beam %s?"%(str(self.beamLoadName.get())))
		if addQuery == 'yes':
			self.beamListbox.insert(END, str(self.beamLoadName.get()))
			# add a beam object to the list of beams (outside of listbox)
			self.beamList.append(beams(self.beamLoadName.get(),'?',['?','?'],'?','?',['?','?']))

			# also update list of beam choices used in the right strategy window
			self.refreshBeamChoices()
		else:
			pass

	def onSelect(self, val):
		# what happens when select button clicked
		sender = val.widget
		idx = sender.curselection()
		value = sender.get(idx)
		self.var3.set(value)

	def readHelpFile(self):
		# read in a txt file to add to helpBox in top left body frame. Currently the txt file
		# 'sampletxt.txt' is just a template file, but will eventually contain all the suggested
		# output from each RADDOSE run
		fileOpen = open('sampletxt.txt','r')
		filelines = fileOpen.readlines()
		fileString = ' '.join(filelines)
		self.varHelpBox.set(fileString)

	def writeRaddose3DInputFile(self):
		# run the current designed strategy here
        # get the index of the selected crystal from the list of added crystals (in the optionmenu list)
		self.currentCrystIndex = [cryst.crystName for cryst in self.crystList].index(self.crystChoice.get())
        # get the index of the selected beam from the list of added beams (in the optionmenu list)
		self.currentBeamIndex = [bm.beamName for bm in self.beamList].index(self.beamChoice.get())

		currentCrystal = self.crystList[self.currentCrystIndex] # get the selected crystal object here
		crystalBlock = self.writeCrystalBlock(currentCrystal) #write the crystal block for RADDOSE-3D input

        # want to write a RADDOSE3D input file here
		RADDOSEfilename = '{}/RADDOSE-3D-input.txt'.format(str(self.expLoadName.get()))
		RADDOSEfile = open(RADDOSEfilename,'w')
		RADDOSEfile.write(crystalBlock)
		RADDOSEfile.write("\n\n")
		RADDOSEfile.close()

		# for each added beam+wedge couple in the treeview list of current strategies, create a
		# RADDOSE3D input
		# first check that number of included beam and wedge objects to be written into RADDOSE3D
		# input file is the same here
		if len(self.beamList2Run) != len(self.wedgeList2Run):
			print 'Inconsistent numbers of beam and wedges to be written to RADDOSE-3D input file'
			print '---> terminating script'
			sys.exit()

		RADDOSEfile = open(RADDOSEfilename,'a')
		counter = -1
		for currentBeam in self.beamList2Run:
			counter += 1
			currentWedge = self.wedgeList2Run[counter]
			beamBlock = self.writeBeamBlock(currentBeam)
			RADDOSEfile.write(beamBlock)
			RADDOSEfile.write("\n\n")
			Wedgeblock = self.writeWedgeBlock(currentWedge)
			RADDOSEfile.write(Wedgeblock)
			RADDOSEfile.write("\n\n")
		RADDOSEfile.close()

		# read the RADDOSE-3D input file to update the output window to show the new RADDOSE-3D input file
		self.readRADDOSEInputFile(RADDOSEfilename)
		quote = self.raddose3Dinputtxt.get()
		self.inputtxt.insert(END, quote)

	def writeCrystalBlock(self, crystalObj):
		"""Write a text block of crystal information for RADDOSE-3D

		Function to write a text block of the crystal properties for a
		RADDOSE-3D input file.

		=================
		Keyword arguments
		=================
		crystalObj:
			a 'crystals' object whose properties contain the required properties
			for RADDOSE-3D input.

		=================
		Return parameters
		=================
		crystBlock:
			a string block that contains the crystal information in the form
			required for input into RADDOSE-3D

		"""
		crystLines = [] #Inialise empty list
		crystLines.append("Crystal") # Append the string - "Crystal" - to the list
		crystPropertyDict = vars(crystalObj) #create a dictionary from the crystal object properties and corresponding values

		#Add a dictionary entry that puts all three crystal dimension values into a string
		crystPropertyDict["Dimensions"] = '{} {} {}'.format(crystalObj.crystDimX, crystalObj.crystDimY, crystalObj.crystDimZ)

		#loop through each entry in the dictionary, create a string of the key
		#and value from the dictionary and append that to the list created above
		for crystProp in crystPropertyDict:
			if crystProp != 'crystDimX' and crystProp != 'crystDimY' and crystProp != 'crystDimZ' and crystProp != 'crystName':
				string = '{} {}'.format(crystProp,str(crystPropertyDict[crystProp]))
				crystLines.append(string)

		#write list entries as a single text block with each list entry joined
		#by a new line character
		crystBlock = "\n".join(crystLines)
		return crystBlock #return the crystal block

	def writeBeamBlock(self, beamObj):
		"""Write a text block of beam information for RADDOSE-3D

		Function to write a text block of the beam properties for a
		RADDOSE-3D input file.

		=================
		Keyword arguments
		=================
		beamObj:
			a 'beams' object whose properties contain the required properties
			for RADDOSE-3D input.

		=================
		Return parameters
		=================
		beamBlock:
			a string block that contains the beam information in the form
			required for input into RADDOSE-3D

		"""
		beamLines = [] #Inialise empty list
		beamLines.append("Beam") # Append the string - "Beam" - to the list
		beamPropertyDict = vars(beamObj) #create a dictionary from the beam object properties and corresponding values

		#Add a dictionary entry that puts beam FWHM dimensions values into a string
		beamPropertyDict["FWHM"] = '{} {}'.format(beamObj.fwhm[0], beamObj.fwhm[1])
		#Add a dictionary entry that puts beam collimation dimensions values into a string
		beamPropertyDict["Collimation"] = '{} {}'.format(beamObj.collimation[0], beamObj.collimation[1])
		#Add a dictionary entry that puts beam pixel size dimensions values into a string
		beamPropertyDict["PixelSize"] = '{} {}'.format(beamObj.pixelSize[0], beamObj.pixelSize[1])

		#loop through each entry in the dictionary, create a string of the key
		#and value from the dictionary and append that to the list created above
		for beamProp in beamPropertyDict:
			if beamProp != 'fwhm' and beamProp != 'collimation' and beamProp != 'pixelSize' and beamProp != 'beamName':
				string = '{} {}'.format(beamProp,str(beamPropertyDict[beamProp]))
				beamLines.append(string)

		#write list entries as a single text block with each list entry joined
		#by a new line character
		beamBlock = "\n".join(beamLines)
		return beamBlock #return the beam block

	def writeWedgeBlock(self, wedgeObj):
		"""Write a text block of wedge information for RADDOSE-3D

		Function to write a text block of the wedge properties for a
		RADDOSE-3D input file.

		=================
		Keyword arguments
		=================
		wedgeObj:
			a 'wedges' object whose properties contain the required properties
			for RADDOSE-3D input.

		=================
		Return parameters
		=================
		wedgeBlock:
			a string block that contains the wedge information in the form
			required for input into RADDOSE-3D

		"""
		wedgeLines = [] #Inialise empty list
		#Ensure the Wedge line is written first into the RADDOSE-3D input file.
		wedgeString = "Wedge {} {}".format(wedgeObj.angStart, wedgeObj.angStop)
		wedgeLines.append(wedgeString)

		wedgePropertyDict = vars(wedgeObj) #create a dictionary from the wedge object properties and corresponding values

		#loop through each entry in the dictionary, create a string of the key
		#and value from the dictionary and append that to the list created above
		for wedgeProp in wedgePropertyDict:
			if wedgeProp != 'angStart' and wedgeProp != 'angStop':
				string = '{} {}'.format(wedgeProp,str(wedgePropertyDict[wedgeProp]))
				wedgeLines.append(string)

		#write list entries as a single text block with each list entry joined
		#by a new line character
		wedgeBlock = "\n".join(wedgeLines)
		return wedgeBlock

	def readRADDOSEInputFile(self,filename):
		# read in a RADDOSE-3D input txt file
		fileOpen = open(filename,'r')
		filelines = fileOpen.readlines()
		fileString = ' '.join(filelines)
		self.raddose3Dinputtxt.set(fileString)

	def clickHelp(self):
		# what happens when help button clicked
		tkMessageBox.showinfo( "Help", "You clicked help")

	def _quit(self):
		# what happens when close button clicked.
		self.quit()     # stops mainloop
		self.destroy()  # this is necessary on Windows to prevent


def main():
	# when the script is run in python, do the following:
    root = Tk()
    app = RADDOSEgui(root)
    root.mainloop()

if __name__ == '__main__':
    main()
