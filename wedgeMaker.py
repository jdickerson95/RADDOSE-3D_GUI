from Tkinter import *
from ttk import *
from wedges import wedges
from HoverInfo import HoverInfo
import tkMessageBox
from InputsHelpText import WedgeInputHelp

class wedgeMakerWindow():

    def __init__(self, MainGui):
        self.master = MainGui.top_WedgeMaker
        self.wedgeMakerFrame = Frame(self.master)
        self.wedgeMakerFrame.pack()
        self.lightcolour = MainGui.lightcolour
        self.darkcolour = MainGui.darkcolour

        # Wedge inputs here:
        l = Label(self.master,text="Wedge",style="labelFrameTitle.TLabel")
        self.currentStrategyWedge = LabelFrame(self.master,labelwidget=l,
                          style="MakeABeam.TFrame")
        self.currentStrategyWedge.pack(side=TOP,padx=10, pady=10,fill=BOTH,expand=TRUE)

        #Create object that contains the help text
        self.helpText = WedgeInputHelp()

        # wedge input --> angular range start
        self.WedgeAngRangeStart = StringVar()
        self.wedgeAngRangeStartInputs()

        # wedge input --> angular range stop
        self.WedgeAngRangeStop = StringVar()
        self.wedgeAngRangeStopInputs()

        # wedge input --> exposure time
        self.WedgeExposTime = StringVar()
        self.WedgeExposTimeInputs()

        # wedge input --> Angular resolution
        self.angRes = StringVar()
        self.angResInput()

        # #wedge input --> Start offset
        self.startOffsetX = StringVar()
        self.startOffsetY = StringVar()
        self.startOffsetZ = StringVar()
        self.startOffsetInput()

        #wedge input --> Translation per degree
        self.transPerDegX = StringVar()
        self.transPerDegY = StringVar()
        self.transPerDegZ = StringVar()
        self.transPerDegInput()

        #wedge input --> Amount that beam is translated from rotation axis
        self.rotAxBeamOffset = StringVar()
        self.rotAxBeamOffsetInput()

        # create visual wedge in Frame
        self.createVisualWedge()

        # create a Wedge "make" button
        self.addWedgeMakeButton(MainGui)

        self.currentStrategyWedge.grid_rowconfigure(0,weight=1)
        self.currentStrategyWedge.grid_rowconfigure(1,weight=1)
        self.currentStrategyWedge.grid_rowconfigure(2,weight=1)
        self.currentStrategyWedge.grid_rowconfigure(3,weight=1)
        self.currentStrategyWedge.grid_rowconfigure(4,weight=1)
        self.currentStrategyWedge.grid_rowconfigure(5,weight=1)
        self.currentStrategyWedge.grid_rowconfigure(6,weight=1)
        self.currentStrategyWedge.grid_rowconfigure(7,weight=1)
        self.currentStrategyWedge.grid_columnconfigure(0,weight=1)
        self.currentStrategyWedge.grid_columnconfigure(1,weight=1)
        self.currentStrategyWedge.grid_columnconfigure(2,weight=1)

    def wedgeAngRangeStartInputs(self):
        # Wedge input --> Wedge angular range (start)
        WedgeinputLabel1 = Label(self.currentStrategyWedge,text="Angular Range (Start)",style="inputBoxes.TLabel")
        WedgeinputLabel1.grid(row=0,column=0,sticky=E,pady=5,padx=6)
        self.hoverStart = HoverInfo(WedgeinputLabel1, self.helpText.angStartText)
        WedgeinputBox1 = Entry(self.currentStrategyWedge,textvariable=self.WedgeAngRangeStart,width=5)
        WedgeinputBox1.grid(row=0,column=1,sticky=W,pady=5,padx=6)
        # preset start angle for wedge
        self.WedgeAngRangeStart.set("0")

    def wedgeAngRangeStopInputs(self):
        # Wedge input --> Wedge angular range (stop)
        WedgeinputLabel2 = Label(self.currentStrategyWedge,text="Angular Range (Stop)",style="inputBoxes.TLabel")
        WedgeinputLabel2.grid(row=1,column=0,sticky=E,pady=5,padx=6)
        self.hoverStop = HoverInfo(WedgeinputLabel2, self.helpText.angStopText)
        WedgeinputBox2 = Entry(self.currentStrategyWedge,textvariable=self.WedgeAngRangeStop,width=5)
        WedgeinputBox2.grid(row=1,column=1,sticky=W,pady=5,padx=6)
        # preset end angle for wedge
        self.WedgeAngRangeStop.set("180")

    def WedgeExposTimeInputs(self):
        # Wedge input --> Wedge total exposure time
        WedgeinputLabel3 = Label(self.currentStrategyWedge,text="Total Exposure Time",style="inputBoxes.TLabel")
        WedgeinputLabel3.grid(row=2,column=0,sticky=E,pady=5,padx=6)
        self.hoverExpos = HoverInfo(WedgeinputLabel3, self.helpText.exposText)
        WedgeinputBox3 = Entry(self.currentStrategyWedge,textvariable=self.WedgeExposTime,width=5)
        WedgeinputBox3.grid(row=2,column=1,sticky=W,pady=5,padx=6)
        # preset total exposure time for wedge
        self.WedgeExposTime.set("180")

    def angResInput(self):
        # Wedge input --> Angular resolution
        WedgeinputLabel = Label(self.currentStrategyWedge,text="Angular resolution",style="inputBoxes.TLabel")
        WedgeinputLabel.grid(row=3,column=0,sticky=E,pady=5,padx=6)
        self.hoverAngRes = HoverInfo(WedgeinputLabel, self.helpText.angRes)
        WedgeinputBox = Entry(self.currentStrategyWedge,textvariable=self.angRes,width=5)
        WedgeinputBox.grid(row=3,column=1,sticky=W,pady=5,padx=6)
        # preset angular resolution
        self.angRes.set("2")

    def startOffsetInput(self):
        # Wedge input --> Start Offset
        WedgeinputLabel = Label(self.currentStrategyWedge,text="Start offset",style="inputBoxes.TLabel")
        WedgeinputLabel.grid(row=4,column=0,sticky=E,pady=5,padx=6)
        self.hoverStartOffset = HoverInfo(WedgeinputLabel, self.helpText.startOffText)
        startOffsetInputsFrame = Frame(self.currentStrategyWedge,style="inputBoxes.TFrame")
        startOffsetInputsFrame.grid(row=4,column=1,sticky=W)
        startOffsetXLabel = Label(startOffsetInputsFrame,text="x = ",style="inputBoxes.TLabel")
        startOffsetXLabel.grid(row=0,column=0,sticky=W,pady=5,padx=6)
        startOffsetXBox = Entry(startOffsetInputsFrame,textvariable=self.startOffsetX,width=5)
        startOffsetXBox.grid(row=0,column=1,sticky=W,pady=5,padx=6)
        startOffsetYLabel = Label(startOffsetInputsFrame,text="y = ",style="inputBoxes.TLabel")
        startOffsetYLabel.grid(row=0,column=2,sticky=W,pady=5,padx=6)
        startOffsetYBox = Entry(startOffsetInputsFrame,textvariable=self.startOffsetY,width=5)
        startOffsetYBox.grid(row=0,column=3,sticky=W,pady=5,padx=6)
        startOffsetZLabel = Label(startOffsetInputsFrame,text="z = ",style="inputBoxes.TLabel")
        startOffsetZLabel.grid(row=0,column=4,sticky=W,pady=5,padx=6)
        startOffsetZBox = Entry(startOffsetInputsFrame,textvariable=self.startOffsetZ,width=5)
        startOffsetZBox.grid(row=0,column=5,sticky=W,pady=5,padx=6)
        startOffsetInputsFrame.grid_rowconfigure(0,weight=1)
        startOffsetInputsFrame.grid_columnconfigure(0,weight=1)
        startOffsetInputsFrame.grid_columnconfigure(1,weight=1)
        startOffsetInputsFrame.grid_columnconfigure(2,weight=1)
        startOffsetInputsFrame.grid_columnconfigure(3,weight=1)
        startOffsetInputsFrame.grid_columnconfigure(4,weight=1)
        startOffsetInputsFrame.grid_columnconfigure(5,weight=1)
        # preset starting offsets
        self.startOffsetX.set("0")
        self.startOffsetY.set("0")
        self.startOffsetZ.set("0")

    def transPerDegInput(self):
        # Wedge input --> Translation per degree
        WedgeinputLabel = Label(self.currentStrategyWedge,text="Translation per degree",style="inputBoxes.TLabel")
        WedgeinputLabel.grid(row=5,column=0,sticky=E,pady=5,padx=6)
        self.hoverTrans = HoverInfo(WedgeinputLabel, self.helpText.transText)
        transPerDegInputsFrame = Frame(self.currentStrategyWedge,style="inputBoxes.TFrame")
        transPerDegInputsFrame.grid(row=5,column=1,sticky=W)
        transPerDegXLabel = Label(transPerDegInputsFrame,text="x = ",style="inputBoxes.TLabel")
        transPerDegXLabel.grid(row=0,column=0,sticky=W,pady=5,padx=6)
        transPerDegXBox = Entry(transPerDegInputsFrame,textvariable=self.transPerDegX,width=5)
        transPerDegXBox.grid(row=0,column=1,sticky=W,pady=5,padx=6)
        transPerDegYLabel = Label(transPerDegInputsFrame,text="y = ",style="inputBoxes.TLabel")
        transPerDegYLabel.grid(row=0,column=2,sticky=W,pady=5,padx=6)
        transPerDegYBox = Entry(transPerDegInputsFrame,textvariable=self.transPerDegY,width=5)
        transPerDegYBox.grid(row=0,column=3,sticky=W,pady=5,padx=6)
        transPerDegZLabel = Label(transPerDegInputsFrame,text="z = ",style="inputBoxes.TLabel")
        transPerDegZLabel.grid(row=0,column=4,sticky=W,pady=5,padx=6)
        transPerDegZBox = Entry(transPerDegInputsFrame,textvariable=self.transPerDegZ,width=5)
        transPerDegZBox.grid(row=0,column=5,sticky=W,pady=5,padx=6)
        transPerDegInputsFrame.grid_rowconfigure(0,weight=1)
        transPerDegInputsFrame.grid_columnconfigure(0,weight=1)
        transPerDegInputsFrame.grid_columnconfigure(1,weight=1)
        transPerDegInputsFrame.grid_columnconfigure(2,weight=1)
        transPerDegInputsFrame.grid_columnconfigure(3,weight=1)
        transPerDegInputsFrame.grid_columnconfigure(4,weight=1)
        transPerDegInputsFrame.grid_columnconfigure(5,weight=1)
        # preset translations per degree
        self.transPerDegX.set("0")
        self.transPerDegY.set("0")
        self.transPerDegZ.set("0")

    def rotAxBeamOffsetInput(self):
        # Wedge input --> The offset between the beam axis and the rotation axis
        WedgeinputLabel = Label(self.currentStrategyWedge,text="Rotation and beam axis offset",style="inputBoxes.TLabel")
        WedgeinputLabel.grid(row=6,column=0,sticky=E,pady=5,padx=6)
        self.hoverRot = HoverInfo(WedgeinputLabel, self.helpText.rotText)
        WedgeinputBox = Entry(self.currentStrategyWedge,textvariable=self.rotAxBeamOffset,width=5)
        WedgeinputBox.grid(row=6,column=1,sticky=W,pady=5,padx=6)
        # preset offset
        self.rotAxBeamOffset.set("0")

    def createVisualWedge(self):
        # make an example visual wedge here
        C = Canvas(self.currentStrategyWedge, bg=self.lightcolour, height=200, width=200)
        coord = 0, 20, 190, 190
        C.create_arc(coord, start=0, extent=150, fill=self.darkcolour)
        C.grid(row=0,column=2,rowspan=6)

    def addWedgeMakeButton(self, MainGui):
        # create a 'make' button here to add this wedge to the list of added beam strategies in treeview list
        wedgeMakeButton = Button(self.currentStrategyWedge, text="Make", command= lambda: self.addStrategy(MainGui))
        wedgeMakeButton.grid(row=7,column=1,pady=5)

    def addStrategy(self, MainGui):
        # make a new wedge object
        currentWedge = wedges(self.WedgeAngRangeStart.get(),self.WedgeAngRangeStop.get(),self.WedgeExposTime.get(),
                              self.angRes.get(),[self.startOffsetX.get(),self.startOffsetY.get(),self.startOffsetZ.get()],
                              [self.transPerDegX.get(),self.transPerDegY.get(),self.transPerDegZ.get()],self.rotAxBeamOffset.get())

        # check the wedge parameters are valid
        ErrorMessage = currentWedge.checkValidInputs()
        if ErrorMessage != "":
                    tkMessageBox.showinfo("Invalid Input File",ErrorMessage)
        else:
            #update the tree view
            MainGui.updateTreeView(currentWedge)
            # once this function runs, the toplevel window should be exited
            self.master.destroy()
