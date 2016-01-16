#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
RADDOSE-3D gui template
First attempt --> 25 March 2015. Last seen on 27 June 2015
"""

from Tkinter import *
from PIL import Image, ImageTk
from ttk import *
import tkMessageBox
import tkFileDialog
import Tkinter as tk
import sys
import os
import shutil
import subprocess
import copy
import platform
import imp
import datetime
import time
import matplotlib.image as mpimg

from plotMaker import barplotWindow
from beamMaker import beamMakerWindow
from crystalMaker import crystalMakerWindow
from wedgeMaker import wedgeMakerWindow
from PremadeInputMaker import PremadeInputMakerWindow
from crystals import *
from beams import *
from wedges import wedges
from experiments import Experiments
from customMadeWidgets import *
from help import help
from RD3DInputParser import parsedRD3Dinput

try:
    imp.find_module('mayavi')
    foundMayaMod = True
except ImportError:
    foundMayaMod = False
if foundMayaMod:
    from doseStatePlot import doseStatePlot

class RADDOSEgui(Frame):
    # this is the main RADDOSE gui class here

    def __init__(self, parent):
        Frame.__init__(self, parent)

        self.parent = parent
        self.initUI()

    def initUI(self):
        # this is to delegate the creation of the user interface to the initUI() method

        ####################################################
        # set heights for list boxes here
        self.loadListHeight = 7
        # specify padding between frames within GUI window
        self.xWidth = 5
        self.yWidth = 5
        self.treeViewHeight = 5
        ####################################################

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
                                  background=self.lightcolour,borderwidth=5,font=("Helvetica", 11))

        # make a style for the added gui header title label
        styleTitle = Style()
        styleTitle.configure("Title.TLabel",foreground="white",
                             background=self.headercolour,font=("Helvetica", 26))

        # make a style for the gui header RD3D web address details
        styleTitle = Style()
        styleTitle.configure("RD3DheaderWebAddress.TLabel",foreground="white",
                             background=self.headercolour,font=("Helvetica", 16))

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
        self.pack()#fill=BOTH, expand=1)

        # the header frame here
        FrameHeader = Frame(self,style="Header.TFrame")
        FrameHeader.grid(row=0,column=0)#, sticky="nsew")

        # the body frame here
        FrameBody = Frame(self,style="BodyBackground.TFrame")
        FrameBody.grid(row=1,column=0)#, sticky="nsew")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # add a RADDOSE-3D logo here.
        # It's an ugly solution to the problem but it works. It first reads the
        # png image and extracts the red, green and blue pixels as three separate
        # matrices. It then creates a blank tk photo image object that is the
        # same size as the png image, loops through all the pixels of the tk
        # photo image and inserts the corresponding pixel values from the png
        # image. It's not pretty but it works.
        pngImage = "raddoseLogo.png"
        rgbBeamImage = mpimg.imread(pngImage)
        redPixels, greenPixels, bluePixels = rgbBeamImage[:,:,0], rgbBeamImage[:,:,1], rgbBeamImage[:,:,2]
        photo = tk.PhotoImage(width=275, height=89)
        for rowPos in xrange(0,len(rgbBeamImage[:,0])):
            for colPos in xrange(0,len(rgbBeamImage[0,:])):
                self.insertPixel(photo, (rowPos,colPos), (redPixels[rowPos,colPos]*255,greenPixels[rowPos,colPos]*255,bluePixels[rowPos,colPos]*255))
        raddoseLogolabel = Label(FrameHeader, image=photo, background=self.headercolour)
        raddoseLogolabel.image = photo # keep a reference!
        raddoseLogolabel.grid(row=0,column=0, sticky="nsew",padx=5, pady=0)

        # make a label in the header frame
        # labelHeader = Label(FrameHeader,text="Data Collection Dose Stategy GUI",style="Title.TLabel")
        # labelHeader.grid(row=1,column=0, sticky="nsew",padx=5, pady=0)
        labelHeader = Label(FrameHeader,text="GUI",style="Title.TLabel")
        labelHeader.grid(row=0,column=1, sticky="nsew",padx=5, pady=0)

        # make a text box with RD3D web address details
        RD3DWebAdress = Label(FrameHeader,text = "http://www.raddo.se/",style="RD3DheaderWebAddress.TLabel")
        RD3DWebAdress.grid(row=2,column=0, sticky="nsew",padx=5, pady=0)

        # in header frame make a help/suggestion box
        l = Label(FrameBody,text="Help/Suggestion Dialogue",style="labelFrameTitle.TLabel")
        FrameBody_Help = LabelFrame(FrameBody,labelwidget=l,style="BodyGroovy.TFrame")
        FrameBody_Help.pack(expand='yes')
        FrameBody_Help.grid(row=0,column=0, sticky="nsew",padx=5, pady=0)

        # make a series of tabs for each main body section below
        tabs = Notebook(FrameBody)
        # tabs.pack(expand='yes')
        tabs.grid(row=1,column=0, sticky="nsew",padx=5, pady=0)

        # in body frame, include a series of tabs for each part of the dose calculation
        FrameBody_Crystal = Frame(tabs,style="BodyBackground.TFrame")
        FrameBody_Beam = Frame(tabs,style="BodyBackground.TFrame")
        FrameBody_Strategy = Frame(tabs,style="BodyBackground.TFrame")
        FrameBody_Run = Frame(tabs,style="BodyBackground.TFrame")
        FrameBody_Summary = Frame(tabs,style="BodyBackground.TFrame")

        # in the crystal frame, make corrsponding labelFrame
        l = Label(FrameBody_Crystal,text="Make-a-crystal",style="labelFrameTitle.TLabel")
        LabelFrame_Crystal = LabelFrame(FrameBody_Crystal,labelwidget=l,style="BodyGroovy.TFrame")
        LabelFrame_Crystal.grid(row=0,column=0, sticky="nsew",padx=self.xWidth, pady=self.yWidth)
        FrameBody_Crystal.grid_columnconfigure(0, weight=1)

        # in the beam frame, make corrsponding labelFrame
        l = Label(FrameBody_Beam,text="Make-a-beam",style="labelFrameTitle.TLabel")
        LabelFrame_Beam = LabelFrame(FrameBody_Beam,labelwidget=l,style="BodyGroovy.TFrame")
        LabelFrame_Beam.grid(row=0,column=0, sticky="nsew",padx=self.xWidth, pady=self.yWidth)
        FrameBody_Beam.grid_columnconfigure(0, weight=1)

        # in the strategy frame, make corrsponding labelFrame
        l = Label(FrameBody_Strategy,text="Design-a-strategy",style="labelFrameTitle.TLabel")
        LabelFrame_Strategy = LabelFrame(FrameBody_Strategy,labelwidget=l,style="BodyGroovy.TFrame")
        LabelFrame_Strategy.grid(row=0,column=0, sticky="nsew",padx=self.xWidth, pady=self.yWidth)
        FrameBody_Strategy.grid_columnconfigure(0, weight=1)
        FrameBody_Strategy.grid_rowconfigure(0, weight=1)

        # in the run frame, make corrsponding labelFrame
        l = Label(FrameBody_Run,text="Run",style="labelFrameTitle.TLabel")
        LabelFrame_Run = LabelFrame(FrameBody_Run,labelwidget=l,style="BodyGroovy.TFrame")
        LabelFrame_Run.grid(row=0,column=0, sticky="nsew",padx=self.xWidth, pady=self.yWidth)
        FrameBody_Run.grid_columnconfigure(0, weight=1)
        FrameBody_Run.grid_rowconfigure(0, weight=1)

        # in the summary frame, make corrsponding labelFrame
        l = Label(FrameBody_Summary,text="Summary/Output Window",style="labelFrameTitle.TLabel")
        LabelFrame_Summary = LabelFrame(FrameBody_Summary,labelwidget=l,style="BodyGroovy.TFrame")
        LabelFrame_Summary.grid(row=1,column=0, sticky="nsew",padx=self.xWidth, pady=self.yWidth)
        FrameBody_Summary.grid_columnconfigure(0, weight=1)
        FrameBody_Summary.grid_rowconfigure(0, weight=1)
        FrameBody_Summary.grid_rowconfigure(1, weight=1)

        # add the above body frames as tabs for each part of the dose calc
        tabs.add(FrameBody_Crystal, text='crystal')
        tabs.add(FrameBody_Beam, text='beam')
        tabs.add(FrameBody_Strategy, text='strategy')
        tabs.add(FrameBody_Run, text='run')
        tabs.add(FrameBody_Summary, text='summary')

        self.makeHelpFrame(FrameBody_Help)
        self.makeCrystalFrame(LabelFrame_Crystal)
        self.makeBeamFrame(LabelFrame_Beam)
        self.makeStrategyFrame(LabelFrame_Strategy)
        self.makeRunFrame(LabelFrame_Run)
        self.makeSummaryFrame(LabelFrame_Summary)

    def makeHelpFrame(self,FrameBody_Help):
        # for help frame --> help/suggestion dialogue box
        self.varHelpBox = StringVar()
        self.helpObj = help() # create help object to be updated as inputs are loaded

        scrollbarStrategyList = Scrollbar(FrameBody_Help, orient=VERTICAL)
        self.helpBox = Text(FrameBody_Help, height=8, width=50,wrap=WORD)
        scrollbarStrategyList.pack(side=LEFT,fill=Y,pady=5, padx=3)
        self.helpBox.pack(fill=BOTH,expand=True)
        scrollbarStrategyList.config(command=self.helpBox.yview)
        self.helpBox.config(yscrollcommand=scrollbarStrategyList.set)
        # update help window
        self.updateHelp()

    def makeCrystalFrame(self,LabelFrame_Crystal):
        # for crystal frame --> make-a-crystal window
        
        # make labelframe in which a crystal can be loaded and saved
        l = Label(LabelFrame_Crystal,text="Load a crystal",style="labelFrameTitle.TLabel")
        crystLoadLabelFrame = LabelFrame(LabelFrame_Crystal,labelwidget=l,style="MakeABeam.TFrame")
        crystLoadLabelFrame.grid(row=0,column=0,columnspan=2,sticky="nsew",padx=10, pady=0)

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
        crystLoadLabelFrame.grid_rowconfigure(0,weight=1)
        crystLoadLabelFrame.grid_rowconfigure(1,weight=1)
        crystLoadLabelFrame.grid_columnconfigure(0,weight=1)
        crystLoadLabelFrame.grid_columnconfigure(1,weight=1)
        crystLoadLabelFrame.grid_columnconfigure(2,weight=1)
        crystLoadLabelFrame.grid_columnconfigure(3,weight=1)

        # make a labelframe in which a crystal can be made from scratch and saved
        l = Label(LabelFrame_Crystal,text="Make a crystal",style="labelFrameTitle.TLabel")
        crystMakeLabelFrame = LabelFrame(LabelFrame_Crystal,labelwidget=l,style="MakeABeam.TFrame")
        crystMakeLabelFrame.grid(row=1,column=0,columnspan=2 ,sticky="nsew",padx=10, pady=0)

        # allow user to give a name to a crystal and make a crystal from scratch here via button interaction
        crystMakeNameLabel = Label(crystMakeLabelFrame,text="Crystal Name",style="inputBoxes.TLabel")
        crystMakeNameLabel.grid(row=0, column=0,pady=5,padx=6,sticky=W+E)
        self.crystMakeName = StringVar()
        crystMakeNameBox = Entry(crystMakeLabelFrame,textvariable=self.crystMakeName)
        crystMakeNameBox.grid(row=0, column=1,columnspan=2,pady=5,sticky=W+E)
        makeCrystButton = Button(crystMakeLabelFrame,text="Make",command=self.clickCrystMake)
        makeCrystButton.grid(row=0, column=3,pady=5,padx=6,sticky=W+E)
        crystMakeLabelFrame.grid_rowconfigure(0,weight=1)
        crystMakeLabelFrame.grid_columnconfigure(0,weight=1)
        crystMakeLabelFrame.grid_columnconfigure(1,weight=1)
        crystMakeLabelFrame.grid_columnconfigure(2,weight=1)
        crystMakeLabelFrame.grid_columnconfigure(3,weight=1)

        # make a listbox frame in options frame to show added crystals. The listbox of added
        # crystals is created here, along with a scrollbar
        crystListFrame = Frame(LabelFrame_Crystal,style="BodyGroovy.TFrame")
        crystListFrame.grid(row=2,column=0,columnspan=2, sticky="nsew",padx=10, pady=0)
        scrollbarCrystListY = Scrollbar(crystListFrame, orient=VERTICAL)
        scrollbarCrystListX = Scrollbar(crystListFrame, orient=HORIZONTAL)

        # want to make a list of crystal object instances (here two example crystals are defined)
        exampleCryst = crystals('Example crystal','Cuboid',10,20,30,1,0,0,{},'Average')
        exampleCryst2 = crystals('Example crystal 2','Cuboid',30,20,10,2,0,0,{},'Average')
        self.crystList = [exampleCryst,exampleCryst2]

        self.crystListbox = Listbox(crystListFrame,yscrollcommand=scrollbarCrystListY.set,
                                    xscrollcommand=scrollbarCrystListX.set,height=self.loadListHeight)

        for cryst in self.crystList:
            self.crystListbox.insert(END, cryst.getTimeStampedName())
        self.crystListbox.update_idletasks()
        self.crystListbox.bind("<<ListboxSelect>>", self.onSelect)
        scrollbarCrystListY.config(command=self.crystListbox.yview)
        scrollbarCrystListX.config(command=self.crystListbox.xview)
        scrollbarCrystListX.pack(side=BOTTOM, fill=X,pady=0, padx=5)
        self.crystListbox.pack(side=LEFT,padx=10,pady=5,fill=BOTH,expand=True)
        scrollbarCrystListY.pack(side=RIGHT, fill=Y,pady=5)
        self.var3 = StringVar()

        # this button will view the currently selected crystal in the list
        viewCrystButton = Button(LabelFrame_Crystal, text="View",command=self.clickCrystView)
        viewCrystButton.grid(row=3,column=0, sticky="nsew",padx=10, pady=5)

        # this button deletes the currently selected crystal from the listbox strategy list above
        deleteCrystButton = Button(LabelFrame_Crystal, text="Delete",command=self.deleteCryst)
        deleteCrystButton.grid(row=3,column=1, sticky="nsew",padx=10, pady=5)
        LabelFrame_Crystal.grid_columnconfigure(0,weight=1)
        LabelFrame_Crystal.grid_columnconfigure(1,weight=1)
        LabelFrame_Crystal.grid_rowconfigure(0,weight=1)
        LabelFrame_Crystal.grid_rowconfigure(1,weight=1)
        LabelFrame_Crystal.grid_rowconfigure(2,weight=1)
        LabelFrame_Crystal.grid_rowconfigure(3,weight=1)

    def makeBeamFrame(self,LabelFrame_Beam):
        # for beam frame --> make-a-beam window

        # make labelframe in which a beam can be loaded and saved
        l = Label(LabelFrame_Beam,text="Load a beam",style="labelFrameTitle.TLabel")
        beamLoadLabelFrame = LabelFrame(LabelFrame_Beam,labelwidget=l,style="MakeABeam.TFrame")
        beamLoadLabelFrame.grid(row=0,column=0,columnspan=2,sticky="nsew",padx=10, pady=0)

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
        beamLoadLabelFrame.grid_rowconfigure(0,weight=1)
        beamLoadLabelFrame.grid_rowconfigure(1,weight=1)
        beamLoadLabelFrame.grid_columnconfigure(0,weight=1)
        beamLoadLabelFrame.grid_columnconfigure(1,weight=1)
        beamLoadLabelFrame.grid_columnconfigure(2,weight=1)
        beamLoadLabelFrame.grid_columnconfigure(3,weight=1)

        # make a labelframe in which a beam can be made from scratch and saved
        l = Label(LabelFrame_Beam,text="Make a beam",style="labelFrameTitle.TLabel")
        beamMakeLabelFrame = LabelFrame(LabelFrame_Beam,labelwidget=l,style="MakeABeam.TFrame")
        beamMakeLabelFrame.grid(row=1,column=0,columnspan=2,sticky="nsew",padx=10, pady=0)

        # allow user to give a name to a beam and make a beam from scratch here via button interaction
        beamMakeNameLabel = Label(beamMakeLabelFrame,text="Beam Name",style="inputBoxes.TLabel")
        beamMakeNameLabel.grid(row=1, column=0,pady=5,padx=6,sticky=W+E)
        self.beamMakeName = StringVar()
        beamMakeNameBox = Entry(beamMakeLabelFrame,textvariable=self.beamMakeName)
        beamMakeNameBox.grid(row=1, column=1,columnspan=2,pady=5,sticky=W+E)
        makeBeamButton = Button(beamMakeLabelFrame,text="Make",command=self.clickBeamMake)
        makeBeamButton.grid(row=1, column=3,pady=5,padx=6,sticky=W+E)
        beamMakeLabelFrame.grid_rowconfigure(0,weight=1)
        beamMakeLabelFrame.grid_columnconfigure(0,weight=1)
        beamMakeLabelFrame.grid_columnconfigure(1,weight=1)
        beamMakeLabelFrame.grid_columnconfigure(2,weight=1)
        beamMakeLabelFrame.grid_columnconfigure(3,weight=1)

        # make a listbox frame in options frame to show added beams. The listbox of added
        # beams is created here, along with a scrollbar
        beamListFrame = Frame(LabelFrame_Beam,style="BodyGroovy.TFrame")
        beamListFrame.grid(row=2,column=0,columnspan=2,sticky="nsew",padx=10, pady=0)
        scrollbarBeamListY = Scrollbar(beamListFrame, orient=VERTICAL)
        scrollbarBeamListX = Scrollbar(beamListFrame, orient=HORIZONTAL)
        # want to make a list of beam object instances (here two example beams are defined)
        exampleBeam = beams_Gaussian('Example beam',[25,25],10000000000,10,[100,100])
        exampleBeam2 = beams_Tophat('Example beam 2',20000000000,12,[120,120])
        self.beamList = [exampleBeam,exampleBeam2]

        self.beamListbox = Listbox(beamListFrame,yscrollcommand=scrollbarBeamListY.set, xscrollcommand=scrollbarBeamListX.set,height=self.loadListHeight)
        for beam in self.beamList:
            self.beamListbox.insert(END, beam.getTimeStampedName())
        self.beamListbox.update_idletasks()
        self.beamListbox.bind("<<ListboxSelect>>", self.onSelect)
        scrollbarBeamListY.config(command=self.beamListbox.yview)
        scrollbarBeamListX.config(command=self.beamListbox.xview)
        scrollbarBeamListX.pack(side=BOTTOM, fill=X,pady=0, padx=5)
        self.beamListbox.pack(side=LEFT,padx=5,pady=5,fill=BOTH,expand=True)
        scrollbarBeamListY.pack(side=RIGHT, fill=Y,pady=5)

        self.var3 = StringVar()

        # this button will view the currently selected crystal in the list
        viewBeamButton = Button(LabelFrame_Beam, text="View",command=self.clickBeamView)
        viewBeamButton.grid(row=3,column=0,sticky="nsew",padx=10, pady=5)

        # this button deletes the currently selected crystal from the listbox strategy list above
        deleteBeamButton = Button(LabelFrame_Beam, text="Delete",command=self.deleteBeam)
        deleteBeamButton.grid(row=3,column=1,sticky="nsew",padx=10, pady=5)
        LabelFrame_Beam.grid_columnconfigure(0,weight=1)
        LabelFrame_Beam.grid_columnconfigure(1,weight=1)
        LabelFrame_Beam.grid_rowconfigure(0,weight=1)
        LabelFrame_Beam.grid_rowconfigure(1,weight=1)
        LabelFrame_Beam.grid_rowconfigure(2,weight=1)
        LabelFrame_Beam.grid_rowconfigure(3,weight=1)

    def makeStrategyFrame(self,LabelFrame_Strategy):
        # for strategy frame --> design-a-strategy window

        # make labelframe in which a crystal can be chosen from list of added crystals
        l = Label(LabelFrame_Strategy,text="Choose a crystal",style="labelFrameTitle.TLabel")
        chooseCrystFrame = LabelFrame(LabelFrame_Strategy,labelwidget=l,style="MakeABeam.TFrame")
        chooseCrystFrame.grid(row=0,column=0,sticky="nsew",padx=10, pady=10)

        # make a dropdown list to choose one of added crystals
        self.crystChoice = StringVar(self)
        self.crystChoices = [cryst.getTimeStampedName() for cryst in self.crystList]
        self.crystChoiceMenu = dynamicOptionMenu(chooseCrystFrame, self.crystChoice,self.crystChoices[0],*self.crystChoices)
        self.crystChoiceMenu.pack(side=TOP, padx=10, pady=0,fill=BOTH)

          # make a labelframe in which the desired beam strategy can be added (including the specification of wedges)
        l = Label(LabelFrame_Strategy,text="Choose a beam",style="labelFrameTitle.TLabel")
        chooseBeamStratFrame = LabelFrame(LabelFrame_Strategy,labelwidget=l,style="MakeABeam.TFrame")
        chooseBeamStratFrame.grid(row=1,column=0,sticky="nsew",padx=10, pady=10)

          # make a dropdown list to choose a beam from the currently added beam list to add to the treeview of beam strategies
        # created below
        self.beamChoice = StringVar(self)
        self.beamChoices = [bm.getTimeStampedName() for bm in self.beamList]
        self.beamChoiceMenu = dynamicOptionMenu(chooseBeamStratFrame, self.beamChoice,self.beamChoices[0],*self.beamChoices)
        self.beamChoiceMenu.pack(side=TOP, padx=10, pady=0,fill=BOTH)

        # make a labelframe in which the desired beam strategy can be added (including the specification of wedges)
        l = Label(LabelFrame_Strategy,text="Choose exposure strategy",style="labelFrameTitle.TLabel")
        chooseBeamStratFrame = LabelFrame(LabelFrame_Strategy,labelwidget=l,style="MakeABeam.TFrame")
        chooseBeamStratFrame.grid(row=2,column=0,sticky="nsew",padx=10, pady=0)

        # make a button to incorporate the currently selected beam (in beam dropdown list above) to the treeview of beam
        # strategies below
        beamStratButton = Button(chooseBeamStratFrame,text='Add Exposure Strategy',command=self.clickAddBeamStrategy)
        beamStratButton.pack(side=TOP, padx=10, pady=0,fill=X,expand=True)

        # make a treeview to show coupled beam and wedge strategies to be used with the specified crystal above
        self.BeamStratTree = Treeview(chooseBeamStratFrame,height=self.treeViewHeight)
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

    def makeRunFrame(self,LabelFrame_Run):
        # for run frame --> run current strategy window

        # make a labelframe. This label frame is for Running the experiment once
        # the crystal, beam and wedge has been defined.
        l = Label(LabelFrame_Run,text="Run Strategy",style="labelFrameTitle.TLabel")
        runStrategyFrame = LabelFrame(LabelFrame_Run,labelwidget=l,style="MakeABeam.TFrame")
        runStrategyFrame.grid(row=0,column=0,sticky="nsew",padx=10, pady=0)
        runStrategyFrame.columnconfigure(1, weight=1)

        # make a box that allows user to uniquely name the experiment (i.e. the
        #crystal, beam and wedge combination) before running.
        expLoadNameLabel = Label(runStrategyFrame,text="Experiment Name",style="inputBoxes.TLabel")
        expLoadNameLabel.grid(row=0, column=0,pady=5,padx=6,sticky=W+E)
        self.expLoadName = StringVar()
        expLoadNameBox = Entry(runStrategyFrame,textvariable=self.expLoadName)
        expLoadNameBox.grid(row=0, column=1, columnspan=3, pady=5,padx=10,sticky=W+E)

        # make a run button to run the currently defined strategy
        runButton = Button(runStrategyFrame,text="Run",command=self.runManualExperiment)
        runButton.grid(row=1, columnspan=4, pady=10,padx=10,sticky=W+E)
        runStrategyFrame.grid_rowconfigure(0,weight=1)
        runStrategyFrame.grid_rowconfigure(1,weight=1)
        runStrategyFrame.grid_columnconfigure(0,weight=1)
        runStrategyFrame.grid_columnconfigure(1,weight=1)

        # make a listbox frame in options frame to show added experiments. The
        # listbox of added experiments is created here, along with a scrollbar.
        expListFrame = Frame(LabelFrame_Run,style="BodyGroovy.TFrame")
        expListFrame.grid(row=4,column=0,sticky="nsew",padx=10, pady=0)
        scrollbarexpList = Scrollbar(expListFrame, orient=VERTICAL)

        self.emptyExpListString = "No experiments loaded"
        self.expListbox = Listbox(expListFrame,yscrollcommand=scrollbarexpList.set,height=1)
        self.expListbox.insert(END, self.emptyExpListString)
        self.expListbox.update_idletasks()
        self.expListbox.bind("<<ListboxSelect>>", self.onSelect)
        scrollbarexpList.config(command=self.expListbox.yview)
        self.expListbox.pack(side=LEFT,padx=10,pady=5,fill=BOTH,expand=True)
        scrollbarexpList.pack(side=RIGHT, fill=Y,pady=5)
        self.var3 = StringVar()

        # this button will view the currently selected crystal in the list
        loadExpButton = Button(expListFrame, text="Load to summary window",command=self.clickLoadExperiment)
        loadExpButton.pack(side=TOP,padx=10, pady=5,fill=X,anchor=N,expand=True)

        # this button deletes the currently selected crystal from the listbox strategy list above
        deleteExpButton = Button(expListFrame, text="Delete experiment",command=self.findExperimentTodelete)
        deleteExpButton.pack(side=BOTTOM,padx=10, pady=5,fill=X,anchor=N)

        # Pre-made RADDOSE-3D run box starts here:
        # make labelframe in which a pre-made RADDOSE-3D input file can be loaded and run
        l = Label(LabelFrame_Run,text="Run pre-made job",style="labelFrameTitle.TLabel")
        runPremadeRD3DStrategyFrame = LabelFrame(LabelFrame_Run,labelwidget=l,style="MakeABeam.TFrame")
        runPremadeRD3DStrategyFrame.grid(row=5,column=0,sticky="nsew",padx=10, pady=0)

        #Add button to choose the files required for RADDOSE-3D input
        choosePremadeFilesButton = Button(runPremadeRD3DStrategyFrame,text="Choose input files",command=self.chooseInputFiles)
        choosePremadeFilesButton.grid(row=0, columnspan=4, pady=10,padx=10,sticky="nsew")
        runPremadeRD3DStrategyFrame.grid_rowconfigure(0,weight=1)
        runPremadeRD3DStrategyFrame.grid_columnconfigure(0,weight=1)

        LabelFrame_Run.grid_columnconfigure(0,weight=1)
        LabelFrame_Run.grid_rowconfigure(0,weight=1)
        LabelFrame_Run.grid_rowconfigure(1,weight=1)
        LabelFrame_Run.grid_rowconfigure(2,weight=1)
        LabelFrame_Run.grid_rowconfigure(3,weight=1)
        LabelFrame_Run.grid_rowconfigure(4,weight=1)
        LabelFrame_Run.grid_rowconfigure(5,weight=1)

        ts = time.time()
        dirTimestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d_%H-%M-%S')
        self.expCompDir = "ExpComp_"+dirTimestamp #Name of directory where strategy comparison files will be stored
        self.RADDOSEfilename = 'RADDOSE-3D-input.txt' #Create RADDOSE3D input file name

    def makeSummaryFrame(self,LabelFrame_Summary):
        # for summary frame --> summary/output window
        self.experimentDict = {}
        self.expNameList = []

        # make labelframe in which an experiment can be chosen from list of added experiments
        l = Label(LabelFrame_Summary,text="Choose an experiment",style="labelFrameTitle.TLabel")
        chooseExpFrame = LabelFrame(LabelFrame_Summary,labelwidget=l,style="MakeABeam.TFrame")
        chooseExpFrame.pack(side=TOP,padx=10, pady=0,fill=BOTH)
        # add equal weighting to 2 columns to stretch + fill frame
        for i in range(2):
            chooseExpFrame.columnconfigure(i, weight=1)

        self.expChoice = StringVar(self)
        # Check if there any experiments loaded. If so then choose the first key
        # in the experiment dictionary as an option. Otherwise let the user know
        # that there are no loaded experiments
        if self.expNameList:
            self.expChoice.set(self.expNameList[0])
        else:
            self.expChoice.set('No existing experiments')

        # Create the option menu of experiments
        self.expChoiceMenu = dynamicOptionMenu(chooseExpFrame, self.expChoice, *self.expNameList)
        self.expChoiceMenu.grid(row=0, column=0, columnspan=1,pady=5, padx=3, sticky=W+E)

        # create an experiment summary option list here to refresh the summary output text bar (below) to
        # show the details of the currently selected experiment (selected in expChoiceMenu) - either a summary
        # or the full RD3D log file can be selected
        summaryOptions = ['Experiment Summary', 'Experiment Log']
        summaryOption = StringVar()
        summaryOption.set(summaryOptions[0]) # set initial entry here
        summaryOptionMenu = OptionMenu(chooseExpFrame, summaryOption, summaryOption.get(),*summaryOptions, command= lambda x: self.updateSummary(summaryOption))
        summaryOptionMenu.grid(row=0, column=1, columnspan=1, pady=5, padx=3, sticky=W+E)

        # create button to remove currently selected experiment from list of loaded experiments
        removeExpButton = Button(chooseExpFrame, text="Remove experiment",command=self.removeExperimentFromList)
        removeExpButton.grid(row=1, column=0, columnspan=1, pady=5, padx=3, sticky=W+E)

        # create button to plot isosurfaces for currently loaded experiments within summary window
        expIsosurfacesButton = Button(chooseExpFrame, text="Dose Contours",command=self.clickDoseContours)
        expIsosurfacesButton.grid(row=1, column=1, columnspan=1, pady=5, padx=3, sticky=W+E)
        chooseExpFrame.grid_columnconfigure(0, weight=1)
        chooseExpFrame.grid_columnconfigure(1, weight=1)
        chooseExpFrame.grid_rowconfigure(0, weight=1)
        chooseExpFrame.grid_rowconfigure(1, weight=1)

        # create text box with scrollbar to detail the summary output for currently selected experiment
        expSummaryTextFrame = Frame(LabelFrame_Summary,style="MakeABeam.TFrame")

        self.raddose3Dinputtxt = StringVar()
        self.inputtxt = Text(expSummaryTextFrame, height=10,width=50,wrap=NONE)
        yscrollbarRaddoseInputFile = Scrollbar(expSummaryTextFrame, orient=VERTICAL, command=self.inputtxt.yview)
        xscrollbarRaddoseInputFile = Scrollbar(expSummaryTextFrame, orient=HORIZONTAL, command=self.inputtxt.xview)
        yscrollbarRaddoseInputFile.pack(side=LEFT,fill=Y,pady=3, padx=3)
        xscrollbarRaddoseInputFile.pack(side=BOTTOM,fill=X,pady=3, padx=3)
        self.inputtxt.pack(fill=BOTH,expand=True,pady=5, padx=10)
        self.inputtxt.config(yscrollcommand=yscrollbarRaddoseInputFile.set)
        self.inputtxt.config(xscrollcommand=xscrollbarRaddoseInputFile.set)
        expSummaryTextFrame.pack(side=TOP,fill=BOTH,expand=1)
        quote = self.raddose3Dinputtxt.get()

        # delete all current text and add new text to text widget
        self.inputtxt.delete(1.0, END)
        self.inputtxt.insert(END, quote*2)

        # make labelframe for the plotting buttons for the currently selected experiments
        l = Label(LabelFrame_Summary,text="Compare Experiments",style="labelFrameTitle.TLabel")
        ExpPlotButtonsFrame = LabelFrame(LabelFrame_Summary,labelwidget=l,style="MakeABeam.TFrame")
        ExpPlotButtonsFrame.pack(side=BOTTOM,padx=10, pady=0,fill=BOTH)
        # add equal weighting to 3 buttons to stretch + fill frame
        for i in range(3):
            ExpPlotButtonsFrame.columnconfigure(i, weight=1)

        # create button to plot dose metrics for currently loaded experiments within summary window
        expBarplotterButton = Button(ExpPlotButtonsFrame, text="Plot",command=self.clickBarplotter)
        expBarplotterButton.grid(row=0, column=0, columnspan=1, pady=5, padx=3, sticky=W+E)

        # create button to display summary details to the summary text window for currently
        # loaded experiments within summary window
        expSummaryShowButton = Button(ExpPlotButtonsFrame, text="Show Summary",command=self.clickExpShowSummary)
        expSummaryShowButton.grid(row=0, column=1, columnspan=1, pady=5, padx=3, sticky=W+E)

        # create button to save summary details to new directory for currently loaded experiments
        # within summary window
        expSaveButton = Button(ExpPlotButtonsFrame, text="Save",command=self.clickExpSave)
        expSaveButton.grid(row=0, column=2, columnspan=1, pady=5, padx=3, sticky=W+E)


    #####################################################################################################
    # below is a list of button actions in the gui

    def runManualExperiment(self):
        """Run the a manually experiment defined by the specified crystal, beam and wedge

        This function intiates the running of an experiment involving a manually defined
        strategy by the user within the GUI

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
        #########################################################################
        #Handling of additional files that may be required for RADDOSE-3D input
        fullFileVarList = []

        ##### Append files to the fullFileVarList
        # get the index of the selected crystal from the list of added crystals (in the optionmenu list)
        self.currentCrystIndex = [cryst.getTimeStampedName() for cryst in self.crystList].index(self.crystChoice.get())
        currentCrystal = self.crystList[self.currentCrystIndex]
        if hasattr(currentCrystal, 'seqFile'):
            fullFileVarList.append(currentCrystal.seqFile)
        #**********THIS ATTRIBUTE NEEDS TO BE ADDED TO THE CRYSTALS CLASS********
        if hasattr(currentCrystal, 'modelFile'):
            fullFileVarList.append(currentCrystal.modelFile)
        for currentBeam in self.beamList2Run:
            if hasattr(currentBeam,'file'):
                fullFileVarList.append(currentBeam.file)

        ##### Determine which of the files have non empty strings and put those in a
        #separate list
        nonEmptyFileList = []
        for filename in fullFileVarList:
            if filename:
                nonEmptyFileList.append(filename)

        #Copy the specified files into the current directory
        allFilesExist = self.copyFiles(nonEmptyFileList, os.getcwd())

        #Now get the file names that should correspond to the paths for the files
        #that have been copied to the current directory
        additionalFilenames = []
        for filename in nonEmptyFileList:
            additionalFilenames.append(filename.split("/")[-1])

        #########################################################################
        if allFilesExist:
            self.CurrentexpLoadName = self.expLoadName.get()
            self.strategyType = 'Manual'
            self.runExperiment(additionalFilenames)
        else:
            #This message box should never come up since these files should be checked
            #for existence when the corresponding objects are made and you can never be
            #too safe :-P
            string = """At least one of the files specified does not exist.
Please check the file names given in the input boxes and make sure they exist.
""" %()
            tkMessageBox.showinfo( "Missing files", string)

    def runPremadeRD3DExperiment(self, rd3dInputFilename, experimentName, additionalFilenames=[]):
        """Run the a premade RD3D job with premade input file

        This function intiates the running of an experiment involving a premade RD3D
        input file

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
        self.RD3DinputLoad = rd3dInputFilename
        #Check if the input file exists
        if os.path.isfile(self.RD3DinputLoad):
            self.CurrentexpLoadName = experimentName
            self.strategyType = 'Premade'
            self.runExperiment(additionalFilenames)
        else:
            string = """The file you have specified does not exist.
Please check the file path supplied.
""" %()
            tkMessageBox.showinfo( "File does not exist", string)

    def runExperiment(self, additionalFilenames=[]):
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
        expName = self.CurrentexpLoadName

        #First check that the experiment name hasn't been left blank. If so then
        #tell user that they need to supply an experiment name.
        #Otherwise check if the experiment name already exists as a directory in
        #the current folder.if it does then ask the user if they want to
        #overwrite the previous experiment.
        #Otherwise create the experiment directory and run the experiment.
        if not expName.strip():
            string = """No experiment name has been given.\nPlease give a name to the experiment that you wish to run in the 'Experiment Name' field.
            """ %()
            tkMessageBox.showinfo( "No Experiment Name", string)
        elif os.path.exists(expName):
            addQuery = tkMessageBox.askquestion( "Duplicate Experiment Names",
            "Experiment name %s already exists. Do you want to overwrite this experiment?"%(expName))
            if addQuery == 'yes':
                expTuple = self.expListbox.get(0, END) #extract list from list box
                if expName in expTuple:
                    expIndex = expTuple.index(expName) #find the index with the corresponding experiment name
                else:
                    expIndex = -1 # A number to signify that the experiment did not already exist in the GUI as an object
                deleteSuccessful = self.deleteExperiment(expIndex, expName) #delete the old experiment to be overwritten.
                if deleteSuccessful:
                    self.runStrategy(additionalFilenames) #run the strategy
            else:
                pass
        else:
            self.runStrategy(additionalFilenames)

    def runStrategy(self, additionalFilenames=[]):
        """Run RADDOSE-3D given specified crystal, beam and wedge objects

        For a manually defined strategy, this function writes an input file
        from the given crystal, beam and wedge objects. For a premade RD3D
        input file, the suitable input file is copied into the working directory
        for the experimental run. Then it runs RADDOSE-3D with that input
        file and puts all of the output files in the corresponding experiment folder.

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
        # for manual strategy need to write RD3D input file. for premade RD3D input file
        # need to copy file to new working directory for experiment and rename the file
        # to the standard input file name.
        if self.strategyType == 'Manual':
            if not self.crystList or not self.beamList2Run or not self.wedgeList2Run:
                string = """An object required to run RADDOSE-3D has not been selected for input.\nCheck that you have selected at least one crystal, beam and wedge.
                """ %()
                tkMessageBox.showinfo( "Missing object required for RADDOSE-3D input", string)
            else:
                self.writeRaddose3DInputFile()
        elif self.strategyType == 'Premade':

            oldFilename = self.RD3DinputLoad.split("/")[-1] # get the name of the file without the rest of the path
            os.rename(oldFilename, self.RADDOSEfilename) # rename the file

        succesfulRun = self.runRaddose3D(additionalFilenames)

        if succesfulRun:
            #Update the experiment list in the strategy window
            self.addToExperimentList()
            #Update experiments loaded to summary window
            self.refreshExperimentChoices()

    def clickAddBeamStrategy(self):
        # what happens when add beam strategy button clicked. Makes a new small window allowing
        # manual entry of wedge parameters for currently selected beam
        self.top_WedgeMaker=Toplevel()
        self.top_WedgeMaker.title("Make a wedge")

        # give the new window a dark background colour
        self.top_WedgeMaker.configure(bg=self.darkcolour)

        # finds separate class for secondary crystal-maker window
        self.app = wedgeMakerWindow(self)

    def updateTreeView(self, wedge):
        # add a new beam+wedge strategy to the treeview of coupled beam+wedge strategies to be input into RADDOSE3D

        Index = self.BeamStratTree.insert("" , len(self.treeviewIndexlist),    text=str(len(self.treeviewIndexlist)+1),
                                 values=(self.beamChoice.get(),wedge.angStart,wedge.angStop,wedge.exposureTime))
        self.treeviewIndexlist.append(Index)

        # get the index of the selected beam from the list of added beams (in the optionmenu list)
        self.currentBeamIndex = [bm.getTimeStampedName() for bm in self.beamList].index(self.beamChoice.get())
        # get the selected beam object here
        currentBeam = self.beamList[self.currentBeamIndex]
        # add the current beam to the list of beams to be run
        self.beamList2Run.append(currentBeam)
        # add the current wedge information for this beam to another list
        self.wedgeList2Run.append(wedge)

        # once this function runs, the toplevel window should be exited
        self.top_WedgeMaker.destroy()

        # update help window
        self.updateHelp()

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

        # update help window
        self.updateHelp()

    def refreshCrystChoices(self):
        # Reset the option menu of added crystals and delete crystals not now
        # included in the list of added crystals
        self.crystChoice.set('')
        self.crystChoiceMenu['menu'].delete(0, 'end')

        # Insert list of new options (tk._setit hooks them up to self.crystChoice)
        new_CrystChoices = [cryst.getTimeStampedName() for cryst in self.crystList]
        for choice in new_CrystChoices:
            self.crystChoiceMenu['menu'].add_command(label=choice, command=tk._setit(self.crystChoice, choice))

    # functions for the manipulation of crystal files and parameters
    def clickCrystView(self):
        # what happens when crystal view button clicked
        crystToView = self.crystList[self.crystListbox.index(ANCHOR)]
        crystInfo = self.extractCrystalInfo(crystToView)
        tkMessageBox.showinfo( "View Crystal Information", crystInfo)

    def extractCrystalInfo(self, crystalObject):
        string = crystalObject.extractCrystalInfo()

        # for non 'average' absCoefCalc crystals, also include composition info
        try:
            compositionString = crystalObject.extractCrystalInfo_composition()
            string += compositionString
        except AttributeError:
            pass
        return string

    def extractWedgeInfo(self, wedgeObject):
        string = """Total Oscillation %.2f (Angle Start: %s, End: %s) degrees\nTotal Exposure Time: %s seconds\n
""" %(float(wedgeObject.angStop) - float(wedgeObject.angStart), wedgeObject.angStart,
                          wedgeObject.angStop, wedgeObject.exposureTime)
        return string

    def updateSummary(self,summaryOption):
        if self.expNameList:
            expName = str(self.expChoice.get())
            if summaryOption.get() == 'Experiment Summary':
                self.displaySummary(expName)
            elif summaryOption.get() == 'Experiment Log':
                self.displayLog(expName)
        else:
            string = """No experiments loaded into summary window.\nPlease select an experiment on the right and click "Load to summary window".
                     """ %()
            tkMessageBox.showinfo( "No experiments loaded", string)

    def displaySummary(self, expName):
        #extract the experiment object corresponding to the chosen
        #experiment in the list
        expObject = self.experimentDict[expName]

        #Write first line of the summary giving the experiment name
        self.inputtxt.delete(1.0, END) #Delete any text already in the box
        self.inputtxt.insert(1.0, "Summary of experiment: %s\n\n"%(expName))

        #Time stamp
        self.inputtxt.insert(END, "This experiment was run on: %s\n"%(expObject.timestamp))
        self.inputtxt.insert(END, "\n")

        #Dose Summary
        self.inputtxt.insert(END, "Dose Summary:\n"%())
        self.inputtxt.insert(END, "%-43s: %-.2f MGy\n"%("Average Diffraction Weighted Dose (DWD)",expObject.dwd))
        self.inputtxt.insert(END, "%-43s: %-.2f MGy\n"%("Maximum Dose",expObject.maxDose))
        self.inputtxt.insert(END, "%-43s: %-.2f MGy\n"%("Average Dose",expObject.avgDose))
        self.inputtxt.insert(END, "%-43s: %-.2e photons\n"%("Elastic Yield",expObject.elasticYield))
        self.inputtxt.insert(END, "%-43s: %-.2e photons/MGy\n"%("Diffraction Efficiency (Elastic Yield/DWD)",expObject.diffractionEfficiency))
        self.inputtxt.insert(END, "%-43s: %-.1f%%\n"%("Used Volume",expObject.usedVolume))
        self.inputtxt.insert(END, "%-43s: %-.2e J\n"%("Absorbed Energy",expObject.absEnergy))
        self.inputtxt.insert(END, "%-43s: %-.2e 1/g\n"%("Dose Inefficiency (Max Dose/mj Absorbed)",expObject.doseInefficiency))
        self.inputtxt.insert(END, "\n")

        self.inputtxt.insert(END, "Experiment parameters:\n"%())
        #Add crystal summary
        crystalInfo = self.extractCrystalInfo(expObject.crystal)
        self.inputtxt.insert(END, crystalInfo)
        #Add beam and wedge summaries
        counter = -1
        for beamObject in expObject.beamList:
            counter += 1
            beamString = self.extractBeamInfo(beamObject)
            wedgeObject = expObject.wedgeList[counter]
            wedgeString =self.extractWedgeInfo(wedgeObject)
            self.inputtxt.insert(END, beamString+wedgeString)

    def displayLog(self, expName):
        """Display RADDOSE-3D log file for currently selected experiment within summary window

        The RADDOSE-3D log file for the currently selected experiment is printed to the summary
        text box within the left-hand side experiment summary window

        =================
        Keyword arguments
        =================
        expName:
            a unique experiment name corresponding to a unique RADDOSE-3D run,
            located within a directory of the same name

        =================
        Return parameters
        =================
        No explicit return parameters

        """
        # extract the experiment object corresponding to the chosen
        # experiment in the list
        expObject = self.experimentDict[expName]
        # Write first line of the summary giving the experiment name
        self.inputtxt.delete(1.0, END) #Delete any text already in the box
        self.inputtxt.insert(1.0, "Log for experiment: %s\n\n"%(expName))

        # Time stamp
        self.inputtxt.insert(END, "This experiment was run on: %s\n"%(expObject.timestamp))
        self.inputtxt.insert(END, "\n")

        # RD3D log printed to summary text box here
        self.inputtxt.insert(END,expObject.log)

    def clickBarplotter(self):
        # button to first check whether any strategies are loaded within summary window and
        # then create a separate window for a bar plot comparing dose metrics for all strategies
        # currently loaded within summary window
        if self.expNameList:
            # Makes a new window allowing which will contain bar plots
            self.top_summaryBarplotMaker=Toplevel()
            self.top_summaryBarplotMaker.title("Summary Dose Plots")
            # give the new window a dark background colour
            self.top_summaryBarplotMaker.configure(bg=self.darkcolour)
            # finds separate class for secondary barplotting window
            self.app = barplotWindow(self)

        else:
            string = """No experiments loaded into summary window.\nPlease select an experiment on the right and click "Load to summary window".
            """ %()
            tkMessageBox.showinfo( "No experiments loaded", string)

    def clickDoseContours(self):
        # button to first check whether any strategies are loaded within summary window and
        # then create a separate window for a bar plot comparing dose metrics for all strategies
        # currently loaded within summary window
        if self.expNameList:
            if foundMayaMod:
                m = doseStatePlot(self)
                m.configure_traits()
            else:
                string = """The Mayavi module is required to view dose contour plots but hasn't been found on your system.\nPlease check that you have it or visit \n\"http://docs.enthought.com/mayavi/mayavi/installation.html\" for installation notes.
                """ %()
                tkMessageBox.showinfo( "Mayavi Not Found", string)
        else:
            string = """No experiments loaded into summary window.\nPlease select an experiment on the right and click "Load to summary window".
            """ %()
            tkMessageBox.showinfo( "No experiments loaded", string)


    def clickExpShowSummary(self):
        #Check to see if there are experiments loaded in the summary window
        if self.expNameList:
            #Write the table
            self.inputtxt.delete(1.0, END) #Delete any text already in the box
            for row in self.tableRowEntries:
                self.inputtxt.insert(END, "{:s}\n".format(row))
        else:
            string = """No experiments loaded into summary window.\nPlease select an experiment on the right and click "Load to summary window".
            """ %()
            tkMessageBox.showinfo( "No experiments loaded", string)

    def clickExpSave(self):
        #Check to see if there are experiments loaded in the summary window
        if self.expNameList:
            #Check if Experiment compasion directory exists
            if not os.path.exists(self.expCompDir):
                os.mkdir(self.expCompDir)
            #Create the file name for the summary table
            expsToCompare = "_".join(self.expNameList)
            summaryFileNameText = "summaryTable_"+expsToCompare+".txt"
            summaryFileNameCSV = "summaryTable_"+expsToCompare+".csv"
            fullpathText = "{}/{}".format(self.expCompDir, summaryFileNameText)
            fullpathCSV = "{}/{}".format(self.expCompDir, summaryFileNameCSV)
            #Write the table to summary file
            summaryFileText = open(fullpathText, 'w')
            for row in self.tableRowEntries:
                summaryFileText.write(row+"\n")
            summaryFileText.close()

            summaryFileCSV = open(fullpathCSV, 'w')
            for row in self.csvRowEntries:
                summaryFileCSV.write(row+"\n")
            summaryFileCSV.close()
        else:
            string = """No experiments loaded into summary window.\nPlease select an experiment on the right and click "Load to summary window".
            """ %()
            tkMessageBox.showinfo( "No experiments loaded", string)

    def createSummaryTable(self):
        self.tableRowEntries = []
        self.csvRowEntries = []
        header = "Dose Summary Comparison Table"
        expHead = "{:^20s}".format("Experiment Name")
        dwdHead = "{:^10s}".format("DWD (MGy)")
        maxDoseHead = "{:^15s}".format("Max Dose (MGy)")
        avgDoseHead = "{:^15s}".format("Avg Dose (MGy)")
        elasHead = "{:^25s}".format("Elastic Yield (photons)")
        diffEffHead = "{:^38s}".format("Diffraction Efficiency (photons/MGy)")
        usedVolHead = "{:^15s}".format("Used Vol (%)")
        absEnHead = "{:^20s}".format("Abs Energy (Joules)")
        doseInEffHead = "{:^18s}".format("Dose Ineff (1/g)")
        separatorText = "{:2s}".format("|")
        separatorCSV = ","
        #Store all of the headers in a list
        summaryHeaders = [expHead, dwdHead, maxDoseHead, avgDoseHead, elasHead,
        diffEffHead, usedVolHead, absEnHead, doseInEffHead]

        textTableHeader = separatorText.join(summaryHeaders)
        csvTableHeader = separatorCSV.join(summaryHeaders)
        splitHeader = "-"*(20+10+15+15+25+38+15+
        20+18+((len(summaryHeaders) - 1) * 2))

        self.tableRowEntries.append(header)
        self.tableRowEntries.append("\n")
        self.tableRowEntries.append(textTableHeader)
        self.tableRowEntries.append(splitHeader)

        self.csvRowEntries.append(csvTableHeader)
        for expName in self.expNameList:
            expObject = self.experimentDict[expName]
            expNameEntry = "{:^20s}".format(expName)
            dwdEntry = "{:^10s}".format(str(expObject.dwd))
            maxDoseEntry = "{:^15s}".format(str(expObject.maxDose))
            avgDoseEntry = "{:^15s}".format(str(expObject.avgDose))
            elasEntry = "{:^25.2e}".format(expObject.elasticYield)
            diffEffEntry = "{:^38.2e}".format(expObject.diffractionEfficiency)
            usedVolEntry = "{:^15s}".format(str(expObject.usedVolume))
            absEnEntry = "{:^20s}".format(str(expObject.absEnergy))
            doseInEffEntry = "{:^18s}".format(str(expObject.doseInefficiency))
            entryList = [expNameEntry, dwdEntry, maxDoseEntry, avgDoseEntry, elasEntry,
            diffEffEntry, usedVolEntry, absEnEntry, doseInEffEntry]
            textTableEntry = separatorText.join(entryList)
            csvTableEntry = separatorCSV.join(entryList)
            self.tableRowEntries.append(textTableEntry)
            self.csvRowEntries.append(csvTableEntry)

    def deleteCryst(self):
        # delete the selected crystal from the listbox of added crystals. Also remove the
        # corresponding crystal object from the crystalList list
        self.crystListbox.delete(ANCHOR)
        self.crystList.pop(self.crystListbox.index(ANCHOR))
        # refresh the option menu of added crystals to keep it up to date
        self.refreshCrystChoices()

        # update help window
        self.updateHelp()

    def clickCrystMake(self):
        # what happens when crystal make button clicked. Makes a new small window allowing
        # manual entry of crystal parameters

        # first ensure that crystal to be made has been given a name, and that this is
        # different than all other loaded crystals
        if not str(self.crystMakeName.get()).strip():
            string = """No crystal name has been given.\nPlease give a name to the crystal that you wish to make.""" %()
            tkMessageBox.showinfo( "No Crystal Name", string)
        elif str(self.crystMakeName.get()) in [cryst.crystName for cryst in self.crystList]:
            tkMessageBox.showinfo( "Duplicate Crystal Names",
            "Crystal name %s already exists. Please choose another name." %(self.crystMakeName.get()))
        else:
            # if unique crystal name was given, create new pop-up window, in which to set crystal properties
            self.top_CrystMaker=Toplevel()
            self.top_CrystMaker.title("Make a crystal")

            # give the new window a dark background colour
            self.top_CrystMaker.configure(bg=self.darkcolour)

            # finds separate class for secondary crystal-maker window
            self.app = crystalMakerWindow(self)

    def chooseInputFiles(self):
        # Open new window with the options for loading a premade RADDOSE-3D job
        self.top_premadeRunMaker=Toplevel()
        self.top_premadeRunMaker.title("Premade Input files")

        # give the new window a dark background colour
        self.top_premadeRunMaker.configure(bg=self.darkcolour)

        # finds separate class for secondary crystal-maker window
        self.app = PremadeInputMakerWindow(self)

    def addCrystalToList(self, crystal):
        # add a crystal object to the list of crystals (outside of listbox)
        self.crystList.append(crystal)
        # add crystal name to loaded crystal list
        self.crystListbox.insert(END, str(crystal.getTimeStampedName()))
        # refresh the option menu of added crystals to keep it up to date
        self.refreshCrystChoices()

        # update help window
        self.updateHelp()

    def addToExperimentList(self):
        if self.emptyExpListString in self.expListbox.get(0):
            self.expListbox.delete(0, END)
        self.expListbox.insert(END, self.CurrentexpLoadName)

    def findExperimentTodelete(self):
        expListIndex = self.expListbox.index(ACTIVE) #get the index where experiment appears in list
        experimentName = self.expListbox.get(expListIndex) #get experiment name

        #Ask if user actually wants to delete the experiment
        addQuery = tkMessageBox.askquestion( "Delete Experiment",
        "Are you sure you want to delete experiment: %s?"%(experimentName))
        if addQuery == 'yes':
            self.deleteExperiment(expListIndex, experimentName)
        else:
            pass

    def deleteExperiment(self, expListIndex, experimentName):
        originalDictLength = len(self.experimentDict)
        dirIsDeleted = False
        shutil.rmtree(experimentName, onerror=self.removeFileError) # Delete experiment directory
        if not os.path.isdir(experimentName):
            if expListIndex != -1:
                self.expListbox.delete(expListIndex) #remove from experiment list box
                del self.experimentDict[experimentName] #delete from dictionary
            #check if experiment was also loaded into summary window (i.e. if
            #it's in the experiment dictionary)
            if experimentName in self.expNameList:
                self.expNameList.remove(experimentName) #remove from experiment list
                self.refreshExperimentChoices() #refresh experiment list in summary window

            #If experiment dictionary is empty then print string to experiment
            #list box to notify user that there are no existing experiments.
            if not self.experimentDict and originalDictLength > 0:
                self.expListbox.insert(0, self.emptyExpListString)
            dirIsDeleted = True
        return dirIsDeleted

    def removeFileError(self, func, path, excinfo):
        string = """Can't delete directory.
This is likely to be caused by a file in the directory being used by another process.
Please check that you have closed all applications that are using any of the related RADDOSE-3D files.""" %()
        tkMessageBox.showinfo( "Can't delete directory", string)

    def clickLoadExperiment(self):
        expListIndex = self.expListbox.index(ACTIVE) #get the index where experiment appears in list
        experimentName = self.expListbox.get(expListIndex) #get experiment name

        #Check if the experiment name has already been added to the summary
        #window list. If so then tell the user in a pop up window
        if experimentName in self.expNameList:
            string = """Experiment %s is already loaded.\n
            """ %(experimentName)
            tkMessageBox.showinfo( "Experiment already loaded", string)
        else:
            self.expNameList.append(experimentName) #add experiment name to list
            self.refreshExperimentChoices() #refresh experiment list in summary window

    def removeExperimentFromList(self):
        experimentName = str(self.expChoice.get()) #get the experiment name
        self.expNameList.remove(experimentName) #remove experiment from list
        self.refreshExperimentChoices() # update the experiment list in the summary window.


    def clickCrystLoad(self):
        # what happens when crystal load button clicked
        self.crystLoad = tkFileDialog.askopenfilename(parent=self,title='Open crystal file to load')
        self.crystLoadBox.delete(0,END)
        self.crystLoadBox.insert(0,self.crystLoad)

    def clickCrystAdd(self):
        # what happens when crystal add button clicked:
        # ensure that crystals added to GUI are given a name, and that this is different than all other loaded crystals
        if not str(self.crystLoadName.get()).strip():
            string = """No crystal name has been given.\nPlease give a name to the crystal that you wish to add.""" %()
            tkMessageBox.showinfo( "No Crystal Name", string)
        elif str(self.crystLoadName.get()) in [cryst.crystName for cryst in self.crystList]:
            tkMessageBox.showinfo( "Duplicate Crystal Names",
                                   "Crystal name %s already exists. Please choose another name." %(self.crystLoadName.get()))
        else:
            addQuery = tkMessageBox.askquestion( "Add Crystal?", "Do you want to add crystal %s?"%(str(self.crystLoadName.get())))
            if addQuery == 'yes':
                # read in RADDOSE-3D style input file to get crystal properties
                newCrystal = self.parseRaddoseInput(self.crystLoadBox.get(),'crystal')
                newCrystal.crystName = str(self.crystLoadName.get())

                # check correct crystal properties have been read from RD3D input file
                ErrorMessage = self.checkCrystInputs(newCrystal)
                if ErrorMessage != "":
                    tkMessageBox.showinfo("Invalid Input File",ErrorMessage)
                else:
                    # add crystal to loaded crystal list
                    self.addCrystalToList(newCrystal)

                # give warning if identical crystal already loaded
                warningMessage = self.checkRepeatedCryst(newCrystal)
                if warningMessage != "":
                    tkMessageBox.showinfo("Warning",warningMessage)

            else:
                pass

    def checkCrystInputs(self,newCrystal):
        # additional check to ensure correct crystal properties have been read successively
        # from premade RD3D input file
        ErrorMessage = newCrystal.checkValidInputs()
        # for the case where abscoefCalc is not 'Average', perform initial checks
        if str(newCrystal.absCoefCalc).lower() != 'average':
            ErrorMessage2 = newCrystal.checkValidInputs_subclass()
            ErrorMessage += ErrorMessage2

        return ErrorMessage

    def copyFiles(self, srcFileList, dirPath, filenames=[]):
        """Copy Source Files

        This function takes a list of files and copies them to a specified
        directory. If the specified directory doesn't already exist then it is
        created.
        ######################################################################
        ######################################################################
        # WARNING!!! IF TWO INPUT FILES WITH THE SAME EXTENSION ARE SPECIFIED
        # THEN THE RENAMING WILL NOT WORK. THE ONLY EXCEPTION IS FOR THE INPUT
        # FILE. FOR NOW THIS METHOD SHOULD BE FINE BUT IF MORE INPUTS TYPES ARE
        # IMPLEMENTED FOR RADDOSE-3D THEN THIS METHOD MAY NEED TO CHANGE.
        ######################################################################
        ######################################################################
        =================
        Keyword arguments
        =================
        srcFileList:
            a list object where is element of the list is a string that
            corresponds to a file that is intended to be moved.

        dirPath:
            The name of the directory that the files will be moved to. This is
            a string object input.

        filenames:
            A list containing strings which represent file names. The source
            files are renamed with the filenames given in this list if the
            file extensions match.

        =================
        Return parameters
        =================
        allFilesExist:
            Boolean variable that indicates whether all files that were in the
            list were present in the current directory.
        """
        allFilesExist = True
        #Loop through the list of files. For each one we need to check if a file
        #with an identical name already exists in the current working directory.
        #If it doesn't then we'll copy it to the current wroking directory.
        counter = 0
        for srcFile in srcFileList:
            if os.path.isfile(srcFile):
                nameOfFile = srcFile.split("/")[-1]
                inputFilePathIfInCurrentDir = "{}/{}".format(dirPath.replace("\\","/"), nameOfFile)
                if inputFilePathIfInCurrentDir != srcFile and len(srcFile.split("/")) > 1:
                    shutil.copy(srcFile,dirPath) # Copy file to directory

                #get extension of src file
                srcFileExt = nameOfFile.split(".")[1]
                if counter > 0:
                    for filename in filenames:
                        fileFromListExt = filename.split(".")[1]
                        if srcFileExt == fileFromListExt and not os.path.isfile(filename):
                            os.rename(nameOfFile, filename)
                            #Remove the file that we copied because we now have a
                            #renamed copy in the directory.
                            if os.path.isfile(nameOfFile):
                                os.remove(nameOfFile)
                            break
            else:
                allFilesExist = False
            counter += 1
        return allFilesExist

    def checkRepeatedCryst(self,newCrystal):
        # additional check to see whether identical crystal has previously been added
        warningMessage = ""
        for cryst in self.crystList[:-1]:
            if newCrystal.__eq__(cryst):
                warningMessage = "Previous crystal {} added with exact same properties as crystal {}. May wish to delete.\n".format(cryst.crystName,newCrystal.crystName)
        return warningMessage

    # functions for the manipulation of beam files and parameters
    def refreshBeamChoices(self):
        # Reset the option menu of added beam and delete beams not now
        # included in the list of added beams
        self.beamChoice.set('')
        self.beamChoiceMenu['menu'].delete(0, 'end')

        # Insert list of new options (tk._setit hooks them up to self.beamChoice)
        new_BeamChoices = [bm.getTimeStampedName() for bm in self.beamList]
        for choice in new_BeamChoices:
            self.beamChoiceMenu['menu'].add_command(label=choice, command=tk._setit(self.beamChoice, choice))

    def refreshExperimentChoices(self):
        # delete all options from menu
        self.expChoiceMenu['menu'].delete(0, 'end')
        # get a list of all of the current keys from the dictionary of experiments
        new_expChoices = self.expNameList
        # Insert list of new options
        for choice in new_expChoices:
            self.expChoiceMenu['menu'].add_command(label=choice, command=tk._setit(self.expChoice, choice))
        #Check if there any experiments loaded. If so then choose the first key
        #in the experiment dictionary as an option and create the comparison
        #summary table. Otherwise let the user know
        #that there are no loaded experiments
        if self.expNameList:
            self.expChoice.set(self.expNameList[0])
            self.createSummaryTable()
        else:
            self.expChoice.set('No existing experiments')

    def clickBeamView(self):
        # what happens when beam view button clicked
        beamToView = self.beamList[self.beamListbox.index(ANCHOR)]
        beamInfo = self.extractBeamInfo(beamToView)
        tkMessageBox.showinfo( "View Beam Information", beamInfo)

    def extractBeamInfo(self, beamObject):
        # determine current beam object properties, dependent on beam type
        string = beamObject.extractBeamInfo()
        return string

    def deleteBeam(self):
        self.beamListbox.delete(ANCHOR)
        self.beamList.pop(self.beamListbox.index(ANCHOR))
        # also update list of beam choices used in the right strategy window
        self.refreshBeamChoices()

        # update help window
        self.updateHelp()

    def clickBeamMake(self):
        # what happens when beam make button clicked. Makes a new small window allowing
        # manual entry of beam parameters

        # first ensure that beam to be made has been given a name, and that this is
        # different than all other loaded beams
        if not str(self.beamMakeName.get()).strip():
            string = """No beam name has been given.\nPlease give a name to the beam that you wish to make.""" %()
            tkMessageBox.showinfo( "No Beam Name", string)
        elif str(self.beamMakeName.get()) in [beam.beamName for beam in self.beamList]:
            tkMessageBox.showinfo( "Duplicate Beam Names",
            "Beam name %s already exists. Please choose another name." %(self.beamMakeName.get()))
        else:
            # if a unique beam name has been given, proceed to produce pop-up window in which beam
            # parameters can be set
            self.top_BeamMaker=Toplevel()
            self.top_BeamMaker.title("Make a beam")

            # give the new window a dark background colour
            self.top_BeamMaker.configure(bg=self.darkcolour)

            # finds a separate class for secondary beam-maker window
            self.app = beamMakerWindow(self)

    def addBeamToList(self, beam):
        # add beam name to loaded beam list
        self.beamListbox.insert(END, beam.getTimeStampedName())
        # add a beam object to the list of beams (outside of listbox)
        self.beamList.append(beam)
        # also update list of beam choices used in the right strategy window
        self.refreshBeamChoices()

        # update help window
        self.updateHelp()

    def clickBeamLoad(self):
        # what happens when beam load button clicked
        self.beamLoad = tkFileDialog.askopenfilename(parent=self,title='Open beam file to load')
        self.beamLoadBox.delete(0,END)
        self.beamLoadBox.insert(0,self.beamLoad)

    def clickBeamAdd(self):
        # what happens when beam add button clicked:
        # ensure that beams added to GUI are given a name, and that this is different than all other loaded beams
        if not str(self.beamLoadName.get()).strip():
            string = """No beam name has been given.\nPlease give a name to the beam that you wish to add.""" %()
            tkMessageBox.showinfo( "No Beam Name", string)
        elif str(self.beamLoadName.get()) in [(beam.beamName).split('_beam_',1)[0] for beam in self.beamList]:
            tkMessageBox.showinfo( "Duplicate Beam Names",
            "Beam name %s already exists. Please choose another name." %(self.beamLoadName.get()))
        else:
            addQuery = tkMessageBox.askquestion( "Add Beam?", "Do you want to add beam %s?"%(str(self.beamLoadName.get())))
            if addQuery == 'yes':
                # read in RADDOSE-3D style input file to get beam properties
                newBeamList = self.parseRaddoseInput(self.beamLoadBox.get(),'beam')

                # check correct beam properties have been read from RD3D input file
                beamError = False
                for newBeam in newBeamList:
                    ErrorMessage = self.checkBeamInputs(newBeam)
                    if ErrorMessage != "":
                        tkMessageBox.showinfo("Invalid Input File",ErrorMessage)
                        beamError = True
                if beamError == False:
                    # give warning if identical beam already loaded
                    warningMessage = ""
                    for newBeam in newBeamList:
                        warningMessage += self.checkRepeatedBeam(newBeam)
                    if warningMessage != "":
                        tkMessageBox.showinfo("Warning",warningMessage)
                    self.addRD3DInputBeamsToList(newBeamList,str(self.beamLoadName.get()))
            else:
                pass

    def checkBeamInputs(self,newBeam):
        # additional check to ensure correct beam properties have been read successively
        # from premade RD3D input file
        ErrorMessage = newBeam.checkValidInputs()
        ErrorMessage2 = newBeam.checkValidInputs_subclass()
        ErrorMessage += ErrorMessage2

        return ErrorMessage

    def checkRepeatedBeam(self,newBeam):
        # additional check to see whether identical beam has previously been added
        warningMessage = ""
        for beam in self.beamList:
            if newBeam.__eqDiffName__(beam):
                warningMessage = "Previous beam {} added with exact same properties as new beam {}. May wish to delete.\n".format(beam.beamName,newBeam.beamName)
        return warningMessage

    def onSelect(self, val):
        # what happens when select button clicked
        sender = val.widget
        idx = sender.curselection()
        value = sender.get(idx)
        self.var3.set(value)

    def updateHelp(self):
        # update the help window
        # avoid trying to locate crystList and beamList when gui initially opened
        # (before they are made)
        if self.helpObj.messageNumber != 0:
            self.helpObj.checkStates(self.crystList,'crystal')
            self.helpObj.checkStates(self.beamList,'beam')
            self.helpObj.checkStates(self.wedgeList2Run,'wedge')

        self.helpObj.getAdvice()
        self.varHelpBox.set(self.helpObj.advice)
        quote = self.varHelpBox.get()
        self.helpBox.delete(1.0, END)
        self.helpBox.insert(END, quote)

    def writeRaddose3DInputFile(self):
        """Writes an input file for RADDOSE-3D

        This function writes an input file suitable for input to RADDOSE-3D.
        This input file is placed in the corresponding experiment directory.

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

        # run the current designed strategy here
        # get the index of the selected beam from the list of added beams (in the optionmenu list)
        self.currentBeamIndex = [bm.getTimeStampedName() for bm in self.beamList].index(self.beamChoice.get())

        currentCrystal = self.crystList[self.currentCrystIndex] # get the selected crystal object here
        crystalBlock = currentCrystal.writeRD3DCrystalBlock() # write the crystal block for RADDOSE-3D input

        # Write the RADDOSE3D input file here
        try:
            RADDOSEfile = open(self.RADDOSEfilename,'w')
        except IOError:
            string = """Can't Write RADDOSE-3D input file.
    This is likely to be caused by a file in the directory being used by another process.
    Please check that you have closed all applications that are using any of the related RADDOSE-3D files.""" %()
            tkMessageBox.showinfo( "Can't Write RADDOSE-3D input file", string)
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

        RADDOSEfile = open(self.RADDOSEfilename,'a')
        counter = -1
        for currentBeam in self.beamList2Run:
            counter += 1
            currentWedge = self.wedgeList2Run[counter]
            beamBlock = currentBeam.writeRD3DBeamBlock()
            RADDOSEfile.write(beamBlock)
            RADDOSEfile.write("\n\n")
            Wedgeblock = currentWedge.writeRD3DWedgeBlock()
            RADDOSEfile.write(Wedgeblock)
            RADDOSEfile.write("\n\n")
        RADDOSEfile.close()

        #Delete contents of summary window and tell user that RADDOSE-3D is
        #being run with the specified inputs
        self.inputtxt.delete(1.0, END)
        self.inputtxt.insert(1.0, "RADDOSE-3D is now running with the following inputs:\n")
        self.readRADDOSEInputFile(self.RADDOSEfilename)
        quote = self.raddose3Dinputtxt.get()
        self.inputtxt.insert(END, quote)

    def runRaddose3D(self, additionalFilenames=[]):
        """Run RADDOSE-3D

        This function runs RADDOSE-3D and puts all of the output files into the
        corresponding experiment directory.

        =================
        Keyword arguments
        =================
        No explicit user defined parameters. Only the object is required for
        implicit input.

        =================
        Return parameters
        =================
        successfulRun:
            Booleam variable to determine whether RADDOSE-3D ran successfully or
            not.
        """
        successfulRun = False
        experimentName = self.CurrentexpLoadName #Get experiment name as string
        #If the input has come from a premade input file then we have to check
        #that the input file is suitable for RADDOSE-3D before running it.
        if self.strategyType == 'Premade':
            try:
                crystalObject, beamList, wedgeList = self.parseRaddoseInput(self.RADDOSEfilename,'all')
            except:
                string = """The premade RADDOSE-3D input file could not be successfully parsed
Please check your input file to make sure your inputs are correct.
For more help with the input file format please refer to the RADDOSE-3D user guide here:
http://www.raddo.se/user-guide.pdf
                """ %()
                tkMessageBox.showinfo("Unsuccesful parsing of input file", string)
            # give crystal object a name here
            crystalObject.crystName = experimentName+"_crystal"

            # check correct crystal properties have been read from RD3D input file
            ErrorMessage = self.checkCrystInputs(crystalObject)
            if ErrorMessage != "":
                tkMessageBox.showinfo("Invalid Input File",ErrorMessage)
                return
            else:
                # add crystal to loaded crystal list
                self.addCrystalToList(crystalObject)

                # give warning if identical crystal already loaded
                warningMessage = self.checkRepeatedCryst(crystalObject)
                if warningMessage != "":
                    tkMessageBox.showinfo("Warning",warningMessage)

            # check correct beam properties have been read from RD3D input file
            beamError = False
            for beam in beamList:
                ErrorMessage = self.checkBeamInputs(beam)
                if ErrorMessage != "":
                    tkMessageBox.showinfo("Invalid Input File",ErrorMessage)
                    beamError = True
                    return
            if beamError == False:
                # give warning if identical beam already loaded
                warningMessage = ""
                for beam in beamList:
                    warningMessage += self.checkRepeatedBeam(beam)
                if warningMessage != "":
                    tkMessageBox.showinfo("Warning",warningMessage)

            self.addRD3DInputBeamsToList(beamList,experimentName)

        #write terminal command to run RADDOSE-3D
        terminalCommand = "java -jar raddose3d.jar -i {} -r raddose.exe".format(self.RADDOSEfilename)
        process = subprocess.Popen(terminalCommand, stdout=subprocess.PIPE, shell=True) #Run RADDOSE-3D
        output = process.communicate() # interact with the process to get the data from the log.
        outputLog = output[0] # extract the output log

        if process.returncode != 0:
            print outputLog
            string = """There was an error whilst running RADDOSE-3D.\nPlease check the log file ("outputLog.txt") and your crystal, beam and wedge parameters.\nOtherwise contact the Garman Group: elspeth.garman@bioch.ox.ac.uk
            """ %()
            tkMessageBox.showinfo( "RADDOSE-3D Error", string)

        #write the output log file
        outputLogFilename = 'outputLog.txt'
        outputLogfile = open(outputLogFilename,'w')
        outputLogfile.write(outputLog)
        outputLogfile.close()

        #Create a list of all of the possible output files that are created
        fileList = [self.RADDOSEfilename, "output-DoseState.csv", "output-DoseState.R",
        "output-Summary.txt", "output-Summary.csv", "outputLog.txt",
        "output-FluencePerDoseHistCSV.csv"]

        #Go through other files that are potentially required for the RADDOSE-3D
        #run
        for additionalFile in additionalFilenames:
            fileList.append(additionalFile)

        #Move selected files to the directory corresponding to the named
        #experiment
        allFilesMoved = self.moveFiles(fileList, experimentName)
        if not allFilesMoved:
            string = """Not all of the possible experiment files were moved into the experiment directory.
This is likely to be due to a file not existing in the main directory.
Check the RADDOSE-3D log file (outputLog.txt) for more information.
This is likely to be due to RADDOSE-3D not creating certain files since they were in use by another process.
Check that you haven't got any applications open that are using files relating to the current experiment run.
""" %()
            tkMessageBox.showinfo( "Not all experiment files moved", string)

        #Create an experiment object and add it to the experiment dictionary
        pathToLogFile = '{}/{}'.format(experimentName, outputLogFilename)
        if self.strategyType == 'Manual':
            experiment = Experiments(self.crystList[self.currentCrystIndex], self.beamList2Run, self.wedgeList2Run, pathToLogFile, outputLog)
        elif self.strategyType == 'Premade':
            experiment = Experiments(crystalObject, beamList, wedgeList, pathToLogFile, outputLog)

        self.experimentDict[experimentName] = copy.deepcopy(experiment)
        self.expNameList.append(experimentName)

        # Print a summary of the RADDOSE-3D run.
        self.displaySummary(experimentName)

        if os.path.isdir(experimentName):
            successfulRun = True

        return successfulRun

    def addRD3DInputBeamsToList(self,beamList,experimentName):
        # for each beam object found in RD3D input file, give beam an unique name
        # and add to list of loaded beams
        uniqueBeamCounter = 1
        for i in xrange(0,len(beamList)):
            beam = copy.deepcopy(beamList[i])
            if i == 0:
                beam.beamName = experimentName+"_beam_"+str(uniqueBeamCounter)
                self.addBeamToList(beam)
            elif i > 0:
                for j in xrange(0,i):
                    if beam.__eq__(beamList[j]):
                        break
                    elif j == i-1:
                        uniqueBeamCounter += 1
                        beam.beamName = experimentName+"_beam_"+str(uniqueBeamCounter)
                        self.addBeamToList(beam)

    def parseRaddoseInput(self,pathToRaddoseInput,returnType):
        """Parses the RADDOSE-3D Input file and returns the a crystal object, a
        list of beam objects and a list of wedge objects. returnType specifies
        which objects should be returned ('crystal': crystal, 'beam': beam list,
         'all': everything)
        """
        parsedInput = parsedRD3Dinput(pathToRaddoseInput,[],[],[])
        parsedInput.parseRaddoseInput()

        if returnType == 'crystal':
            return (parsedInput.crystal)
        elif returnType == 'beam':
            return (parsedInput.beamList)
        elif returnType == 'all':
            return (parsedInput.crystal,parsedInput.beamList,parsedInput.wedgeList)

    def moveFiles(self, srcFileList, dirPath):
        """Move Source Files

        This function takes a list of files and moves them to a specified
        directory. If the specified directory doesn't already exist then it is
        created.
        =================
        Keyword arguments
        =================
        srcFileList:
            a list object where is element of the list is a string that
            corresponds to a file that is intended to be moved.

        dirPath:
            The name of the directory that the files will be moved to. This is
            a string object input.

        =================
        Return parameters
        =================
        allFilesExist:
            Boolean variable that indicates whether all files that were in the
            list were present in the current directory.
        """
        allFilesExist = True
        if not os.path.isdir(dirPath): #check to determine if directory already exists
            os.mkdir(dirPath) # make the directory if it doesn't exist
        #Loop through the list of files. For each one we need to check if a file
        #with an identical name already exists in the specified directory. If it
        #does then we need to delete it first before moving the file over.
        for srcFile in srcFileList:
            if os.path.isfile(srcFile):
                if os.path.isfile("{}/{}".format(dirPath,srcFile)):
                    os.remove("{}/{}".format(dirPath,srcFile))
                shutil.move(srcFile,"{}/{}".format(dirPath,srcFile))
            elif srcFile != "output-FluencePerDoseHistCSV.csv":
                allFilesExist = False
        return allFilesExist

    def readRADDOSEInputFile(self,filename):
        # read in a RADDOSE-3D input txt file
        fileOpen = open(filename,'r')
        filelines = fileOpen.readlines()
        fileString = ' '.join(filelines)
        self.raddose3Dinputtxt.set(fileString)

    def _quit(self):
        # what happens when close button clicked.
        self.quit()     # stops mainloop
        self.destroy()  # this is necessary on Windows to prevent

    def insertPixel(self, image, pos, color):
        """Place pixel at pos=(x,y) on image, with color=(r,g,b)."""
        r,g,b = color
        x,y = pos
        image.put("#%02x%02x%02x" % (r,g,b), (y, x))

def center(win):
    """
    centers a tkinter window
    :param win: the root or Toplevel window to center
    """
    win.update_idletasks()
    width = win.winfo_width()
    frm_width = win.winfo_rootx() - win.winfo_x()
    win_width = width + 2 * frm_width
    height = win.winfo_height()
    titlebar_height = win.winfo_rooty() - win.winfo_y()
    win_height = height + titlebar_height + frm_width
    x = win.winfo_screenwidth() // 2 - win_width // 2
    y = win.winfo_screenheight() // 2 - win_height // 2
    win.geometry('{}x{}+{}+{}'.format(width, height, x, y))
    win.deiconify()

def main():
    # when the script is run in python, do the following:
    root = Tk()
    # widthScrSizeFrac = 0.9
    # heightScrSizeFrac = 0.9
    # width = root.winfo_screenwidth()
    # height = root.winfo_screenheight()
    # root.geometry(str(int(round(width*widthScrSizeFrac))) + "x" + str(int(round(height*heightScrSizeFrac))))
    app = RADDOSEgui(root)
    app.pack(fill=BOTH,expand=YES)
    center(root)
    root.mainloop()
    return app

if __name__ == '__main__':
    main()
