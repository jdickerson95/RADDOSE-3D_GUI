from Tkinter import *
from ttk import *
from wedges import wedges


class wedgeMakerWindow(Frame):

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

        # wedge input --> angular range start
        self.WedgeAngRangeStart = StringVar()
        self.wedgeAngRangeStartInputs()

        # wedge input --> angular range stop
        self.WedgeAngRangeStop = StringVar()
        self.wedgeAngRangeStopInputs()

        # wedge input --> exposure time
        self.WedgeExposTime = StringVar()
        self.WedgeExposTimeInputs()

        # create visual wedge in Frame
        self.createVisualWedge()

        # create a Wedge "make" button
        self.addWedgeMakeButton(MainGui)

    def wedgeAngRangeStartInputs(self):
        # Wedge input --> Wedge angular range (start)
        WedgeinputFrame1 = Frame(self.currentStrategyWedge,style="inputBoxes.TFrame")
        WedgeinputFrame1.grid(row=0,column=0)
        WedgeinputLabel1 = Label(WedgeinputFrame1,text="Angular Range (Start)",style="inputBoxes.TLabel")
        WedgeinputLabel1.pack(side=LEFT,pady=5,padx=6)
        WedgeinputBox1 = Entry(WedgeinputFrame1,textvariable=self.WedgeAngRangeStart,width=5)
        WedgeinputBox1.pack(side=LEFT,pady=5,padx=6)
        # preset start angle for wedge
        self.WedgeAngRangeStart.set("0")

    def wedgeAngRangeStopInputs(self):
        # Wedge input --> Wedge angular range (stop)
        WedgeinputFrame2 = Frame(self.currentStrategyWedge,style="inputBoxes.TFrame")
        WedgeinputFrame2.grid(row=1,column=0)
        WedgeinputLabel2 = Label(WedgeinputFrame2,text="Angular Range (Stop)",style="inputBoxes.TLabel")
        WedgeinputLabel2.pack(side=LEFT,pady=5,padx=6)
        WedgeinputBox2 = Entry(WedgeinputFrame2,textvariable=self.WedgeAngRangeStop,width=5)
        WedgeinputBox2.pack(side=LEFT,pady=5,padx=6)
        # preset end angle for wedge
        self.WedgeAngRangeStop.set("180")

    def WedgeExposTimeInputs(self):
        # Wedge input --> Wedge total exposure time
        WedgeinputFrame3 = Frame(self.currentStrategyWedge,style="inputBoxes.TFrame")
        WedgeinputFrame3.grid(row=2,column=0)
        WedgeinputLabel3 = Label(WedgeinputFrame3,text="Total Exposure Time",style="inputBoxes.TLabel")
        WedgeinputLabel3.pack(side=LEFT,pady=5,padx=6)
        WedgeinputBox3 = Entry(WedgeinputFrame3,textvariable=self.WedgeExposTime,width=5)
        WedgeinputBox3.pack(side=LEFT,pady=5,padx=6)
        # preset total exposure time for wedge
        self.WedgeExposTime.set("180")

    def createVisualWedge(self):
        # make an example visual wedge here
        C = Canvas(self.currentStrategyWedge, bg=self.lightcolour, height=100, width=100)
        coord = 0, 20, 100, 100
        C.create_arc(coord, start=0, extent=150, fill=self.darkcolour)
        C.grid(row=0,column=1,rowspan=4)

    def addWedgeMakeButton(self, MainGui):
        # create a 'make' button here to add this wedge to the list of added beam strategies in treeview list
        wedgeMakeButton = Button(self.currentStrategyWedge, text="Make", command= lambda: self.addStrategy(MainGui))
        wedgeMakeButton.grid(row=4,column=0,pady=5)

    def addStrategy(self, MainGui):
        # make a new wedge object
        currentWedge = wedges(self.WedgeAngRangeStart.get(),self.WedgeAngRangeStop.get(),self.WedgeExposTime.get())
        #update the tree view
        MainGui.updateTreeView(currentWedge)
        # once this function runs, the toplevel window should be exited
        self.master.destroy()
