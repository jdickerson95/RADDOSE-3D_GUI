
from Tkinter import *
from ttk import *
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import os
import imp
# look for seaborn module to import
try:
    imp.find_module('seaborn')
    foundSeaborn = True
except ImportError:
    foundSeaborn = False
if foundSeaborn == True:
	import seaborn as sns

class barplotWindow(Frame):
	# this is a secondary plotting window class here. It is where all the dose summary bar plots
	# will be created

    def __init__(self,MainGui):
    	currentExpDict = MainGui.experimentDict
    	currentExpNameList = MainGui.expNameList
        self.compPlotDir = "{}/{}".format(MainGui.stratCompDir, "Plots")
        self.master = MainGui.top_summaryBarplotMaker
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

    	# create option list to select which dose metric to plot
        self.doseMetricToPlot = StringVar()
        self.MetricNameListDict = {'DWD'       : "Average Diffraction Weighted Dose",
    							   'maxDose'   : "Max Dose",
    							   'avgDose'   : "Average Dose (Whole Crystal)",
    							   'elasYield' : "Elastic Yield",
    							   'diffEff'   : "Diffraction Efficiency (Elastic Yield/DWD)",
    							   'usedVol'   : "Used Volume",
    							   'absEnergy' : "Absorbed Energy (last wedge of data)",
    							   'doseIneff' : "Dose Inefficiency (Max Dose/mJ Absorbed)"}

        self.unitsDict = {'DWD'       : 'Dose (MGy)',
    					  'maxDose'   : 'Dose (MGy)',
    				      'avgDose'   : 'Dose (MGy)',
    					  'elasYield' : "Photons",
    					  'diffEff'   : "Photons/MGy",
    					  'usedVol'   : "Percent (%)",
    					  'absEnergy' : "Joules (J)",
    					  'doseIneff' : "1/grams"}

        self.doseMetricToPlot.set(self.MetricNameListDict['DWD']) # default value to show in option list
        doseMetricOptionMenu = OptionMenu(plotButtonFrame, self.doseMetricToPlot,self.MetricNameListDict['DWD'],
    				   self.MetricNameListDict['DWD'],
    				   self.MetricNameListDict['maxDose'],
    				   self.MetricNameListDict['avgDose'],
    				   self.MetricNameListDict['elasYield'],
    				   self.MetricNameListDict['diffEff'],
    				   self.MetricNameListDict['usedVol'],
    				   self.MetricNameListDict['absEnergy'],
    				   self.MetricNameListDict['doseIneff'],
    				   command= lambda x: self.refreshPlot(currentExpNameList))

    	# create lists of metrics over all currently loaded strategies
        self.metricListDict = {'DWD':[],'maxDose':[],'avgDose':[], 'elasYield':[], 'diffEff':[], 'usedVol':[], 'absEnergy':[], 'doseIneff':[]}
        for expName in currentExpNameList:
    		expObject = currentExpDict[expName]
    		self.metricListDict['DWD'].append(expObject.dwd)
    		self.metricListDict['maxDose'].append(expObject.maxDose)
    		self.metricListDict['avgDose'].append(expObject.avgDose)
    		self.metricListDict['elasYield'].append(expObject.elasticYield)
    		self.metricListDict['diffEff'].append(expObject.diffractionEfficiency)
    		self.metricListDict['usedVol'].append(expObject.usedVolume)
    		self.metricListDict['absEnergy'].append(expObject.absEnergy)
    		self.metricListDict['doseIneff'].append(expObject.doseInefficiency)

    	# create an initial barplot figure here
    	# bar plot parameters for specified bar plot
        y = np.array(self.metricListDict['DWD'])
        ylabel = self.unitsDict['DWD']
        self.plotBarplot(self.doseMetricToPlot.get(),currentExpNameList,ylabel,y)

    	# put buttons and dose metric selection list within plottingFrame frame
        doseMetricOptionMenu.grid(row=0, column=0,pady=10, padx=10, sticky=W)
        self.saveButton .grid(row=0, column=1,pady=10, padx=10, sticky=W+E)
        self.quitButton.grid(row=0, column=2,pady=10, padx=10, sticky=E)

    def plotBarplot(self,currentDoseMetric,currentExpNameList,ylabel,y):
    	# a matlibplot figure axis should be created here
    	self.doseCompareFig = plt.Figure(figsize=(10, 10), dpi=80, facecolor='w', edgecolor='k')
    	self.canvasForBarplot = FigureCanvasTkAgg(self.doseCompareFig, master=self.plottingFrame)
    	self.canvasForBarplot.show()
    	self.canvasForBarplot.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1.0)
    	self.axBarplot = self.doseCompareFig.add_subplot(111)

    	# create x axis array here
    	x = np.arange(len(y))
    	if not foundSeaborn:
    		bar_width = 0.35
    		opacity = 0.4
    		self.doseBarplot = self.axBarplot.bar(x,y,bar_width,alpha=opacity,color='b')
    	else:
    		bar_width = 0
    		# try:
    		self.doseBarplot = sns.barplot(x,y,ax=self.axBarplot)
    		# except NameError:
    		# 	pass

    	xTickMarks = [str(expName) for expName in currentExpNameList]
    	self.axBarplot.set_xticks(x+0.5*bar_width)
    	xtickNames = self.axBarplot.set_xticklabels(xTickMarks)
    	plt.setp(xtickNames, rotation=0, fontsize=16)
    	self.axBarplot.set_ylim(0, y.max()*(1.2))
    	self.axBarplot.set_xlabel('Strategy', fontsize=24)
    	self.axBarplot.set_ylabel(str(ylabel), fontsize=24)
    	self.axBarplot.set_title(str(currentDoseMetric),fontsize=24)

    	self.canvasForBarplot.draw()

    def refreshPlot(self,currentExpNameList):
    	# when a new dose metric is selected from dropdown option list, click to refresh bar plot
    	currentDoseMetric = self.doseMetricToPlot.get()
    	if currentDoseMetric == self.MetricNameListDict['DWD']:
    		y = np.array(self.metricListDict['DWD'])
    		x = np.arange(len(y))
    		ylabel = self.unitsDict['DWD']
    	elif currentDoseMetric == self.MetricNameListDict['maxDose']:
    		y = np.array(self.metricListDict['maxDose'])
    		x = np.arange(len(y))
    		ylabel = self.unitsDict['maxDose']
    	elif currentDoseMetric == self.MetricNameListDict['avgDose']:
    		y = np.array(self.metricListDict['avgDose'])
    		x = np.arange(len(y))
    		ylabel = self.unitsDict['avgDose']
    	elif currentDoseMetric == self.MetricNameListDict['elasYield']:
    		y = np.array(self.metricListDict['elasYield'])
    		x = np.arange(len(y))
    		ylabel = self.unitsDict['elasYield']
    	elif currentDoseMetric == self.MetricNameListDict['diffEff']:
    		y = np.array(self.metricListDict['diffEff'])
    		x = np.arange(len(y))
    		ylabel = self.unitsDict['diffEff']
    	elif currentDoseMetric == self.MetricNameListDict['usedVol']:
    		y = np.array(self.metricListDict['usedVol'])
    		x = np.arange(len(y))
    		ylabel = self.unitsDict['usedVol']
    	elif currentDoseMetric == self.MetricNameListDict['absEnergy']:
    		y = np.array(self.metricListDict['absEnergy'])
    		x = np.arange(len(y))
    		ylabel = self.unitsDict['absEnergy']
    	elif currentDoseMetric == self.MetricNameListDict['doseIneff']:
    		y = np.array(self.metricListDict['doseIneff'])
    		x = np.arange(len(y))
    		ylabel = self.unitsDict['doseIneff']

    	self.killOldFig()
    	self.plotBarplot(currentDoseMetric,currentExpNameList,ylabel,y)

    def killOldFig(self):
    	self.canvasForBarplot.get_tk_widget().destroy()

    def close_windows(self):
    	self.master.destroy()

    def savePlot(self):
    	# make directory to hold comparison plots if it does not exist
    	if not os.path.exists(self.compPlotDir):
            os.makedirs(self.compPlotDir)

    	# save plot to the plot directory
    	self.doseCompareFig.savefig('./%s/%s.png' %(self.compPlotDir,self.doseMetricToPlot.get()))
