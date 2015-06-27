
from Tkinter import *
from ttk import *
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

class barplotWindow(Frame):
	# this is a secondary plotting window class here. It is where all the dose summary bar plots
	# will be created

	def __init__(self,MainGui):
		currentExpDict = MainGui.experimentDict
		currentExpNameList = MainGui.expNameList
		self.master = MainGui.top_summaryBarplotMaker
		self.plottingFrame = Frame(self.master)
		self.plottingFrame.pack()

		# create frame for buttons and dose metric list
		plotButtonFrame = Frame(self.plottingFrame,style="BodyGroovy.TFrame")
		plotButtonFrame.pack(side=BOTTOM, fill=BOTH, expand=True)
		# weight the 3 button columns to stretch across bottom of figure
		plotButtonFrame.columnconfigure(0, weight=1)
		plotButtonFrame.columnconfigure(1, weight=1)
		plotButtonFrame.columnconfigure(2, weight=1)

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
					   self.MetricNameListDict['doseIneff'])

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

		# a matlibplot figure axis should be created here
		doseCompareFig = plt.Figure(figsize=(10, 10), dpi=80, facecolor='w', edgecolor='k')
		self.canvasForBarplot = FigureCanvasTkAgg(doseCompareFig, master=self.plottingFrame)
		self.canvasForBarplot.show()
		self.canvasForBarplot.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1.0)
		self.axBarplot = doseCompareFig.add_subplot(111)

		# bar plot parameters for DWD bar plot
		bar_width = 0.35
		opacity = 0.4
		y = np.array(self.metricListDict['DWD'])
		x = np.arange(len(y))
		self.doseBarplot = self.axBarplot.bar(x,y,bar_width,alpha=opacity,color='b')
		xTickMarks = [str(expName) for expName in currentExpNameList]
		self.axBarplot.set_xticks(x+0.5*bar_width)
		xtickNames = self.axBarplot.set_xticklabels(xTickMarks)
		plt.setp(xtickNames, rotation=0, fontsize=16)
		self.axBarplot.set_ylim(0, y.max()*(1.2))
		self.axBarplot.set_xlabel('Strategy', fontsize=24)
		self.axBarplot.set_ylabel('Dose (MGy)', fontsize=24)
		self.axBarplot.set_title('Average Diffraction Weighted Dose',fontsize=24)

		self.canvasForBarplot.draw()

		# create a plot refresh button for when the selected dose metric is changed
		self.plotRefreshButton = Button(plotButtonFrame, text = 'Refresh', width = 25, command = self.refreshPlot)

		# put buttons and dose metric selection list within plottingFrame frame
		doseMetricOptionMenu.grid(row=0, column=0,pady=5, padx=5, sticky=W+E)
		self.plotRefreshButton.grid(row=0, column=1,pady=5, padx=5, sticky=W+E)
		self.quitButton.grid(row=0, column=2,pady=5, padx=5, sticky=W+E)

	def refreshPlot(self):
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

		# update bars with new dose metric values here
		for bar, x in zip(self.doseBarplot,y):
			bar.set_height(x)
		self.axBarplot.set_ylim(0, y.max()*(1.2))
		self.axBarplot.set_title(str(currentDoseMetric),fontsize=24)
		self.axBarplot.set_ylabel(ylabel, fontsize=24)
		# replot figure by redrawing canvas
		self.canvasForBarplot.draw()

	def close_windows(self):
		self.master.destroy()