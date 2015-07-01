from Tkinter import *
from ttk import *
from scitools.std import *
import numpy as np
from mayavi import mlab

class doseStatePlotWindow(Frame):
	# this is a secondary plotting window class here. It is where all the dose
    # state plot is created

	def __init__(self,MainGui):
        currentExpNameList = MainGui.expNameList
		self.master = MainGui.top_doseStatePlotMaker
		self.plottingFrame = Frame(self.master)
		self.plottingFrame.pack()

        # create frame for buttons and dose metric list
		plotButtonFrame = Frame(self.plottingFrame,style="BodyGroovy.TFrame")
		plotButtonFrame.pack(side=TOP,padx=10, pady=0, fill=BOTH, expand=True)
		# weight the 2 button columns to stretch across bottom of figure
		plotButtonFrame.columnconfigure(0, weight=1)
		plotButtonFrame.columnconfigure(1, weight=1)

        # create figure save button to save currently displayed plot
		self.saveButton = Button(plotButtonFrame, text = 'Save', width = 25, command = self.savePlot)

		# create quit button to leave plotting window
		self.quitButton = Button(plotButtonFrame, text = 'Quit', width = 25, command = self.close_windows)

        # Create option menu to select which crystal dose state to plot
        self.crystalStateToPlot = StringVar()
        self.crystalStateToPlot.set(expName = str(MainGui.expChoice.get())) # get currently selected experiment name
		crystalStateOptionMenu = OptionMenu(plotButtonFrame, self.crystalStateToPlot, currentExpNameList,
					   command= lambda x: self.refreshPlot())

        # create dose state here
		self.plotDoseState(self.doseMetricToPlot.get())

		# put buttons and dose metric selection list within plottingFrame frame
		crystalStateOptionMenu.grid(row=0, column=0,pady=10, padx=10, sticky=W)
		self.saveButton.grid(row=0, column=1,pady=10, padx=10, sticky=W+E)
		self.quitButton.grid(row=0, column=2,pady=10, padx=10, sticky=E)

    def plotDoseState(self,currentExp):
        self.doseStateFig = mlab.figure(figsize=(10, 10), dpi=80, facecolor='w', edgecolor='k')
		self.canvasForDoseStatePlot = FigureCanvasTkAgg(self.doseStateFig, master=self.plottingFrame)
		self.canvasForDoseStatePlot.show()
		self.canvasForDoseStatePlot.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1.0)

        rfilename = "{}/output-DoseState.R".format(currentExp)
        dose = getDoseStateFromR(rfilename)
        mlab.contour3d(dose, colormap='hot', contours=[dose.min(), (dose.max()-dose.min())/2.0, dose.max()], transparent=False, opacity=0.5, vmin=0, vmax=30)
        mlab.outline()
        mlab.colorbar(orientation='vertical')

    def refreshPlot(self):
        # when a new dose metric is selected from dropdown option list, click to refresh bar plot
    	currentExp = self.crystalStateToPlot.get()
        self.killOldFig()
		self.plotBarplot(currentExp)

	def close_windows(self):
		self.master.destroy()

	def savePlot(self):
		pass
