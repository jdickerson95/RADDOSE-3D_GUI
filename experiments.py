import datetime
import time

class Experiments(object):
	#This class creates experiment objects. Experiments are defined by a unique
	#crystal, set of beams and a corresponding set of wedges. The experiment
	#will also contain information about the RADDOSE-3D run such as the various
	#aggregate dose metrics (e.g. the DWD, max dose, and average dose metrics)
	#and the time stamp when the experiment was run. The log is the information
	#output when RADDOSE-3D was run for this particular experiment.
	def __init__(self, crystal, beamList, wedgeList, pathToRaddose3dLog, log):
		self.crystal = crystal
		self.beamList = beamList
		self.wedgeList = wedgeList
		dwd, maxDose, avgDose, elasYield, diffEff, usedVol, absEnergy, doseIneff = self.parseRaddoseOutput(pathToRaddose3dLog)
		self.dwd = dwd
		self.maxDose = maxDose
		self.avgDose = avgDose
		self.elasticYield = elasYield
		self.diffractionEfficiency = diffEff
		self.usedVolume = usedVol
		self.absEnergy = absEnergy
		self.doseInefficiency = doseIneff
		ts = time.time()
		self.timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
		self.log = log


	def parseRaddoseOutput(self,pathToRaddose3dLog):
		"""Parses the RADDOSE-3D log and returns the specified dose value.
		"""

		raddoseOutput = open(pathToRaddose3dLog,'r')

		parseDoseDWD   = "Average Diffraction Weighted Dose"
		parseDoseMax   = "Max Dose"
		parseDoseAvg   = "Average Dose (Whole Crystal)"
		parseElasYield = "Elastic Yield "
		parseDiffEff   = "Diffraction Efficiency"
		parseUsedVol   = "Used Volume"
		parseAbsEnergy = "Absorbed Energy"
		parseDoseIneff = "Dose Inefficiency"

		for line in raddoseOutput:
			if parseDoseDWD in line and "MGy" in line:
				dwdDose = self.parseRaddoseLine(line)
			elif parseDoseMax in line and "MGy" in line:
				maxDose = self.parseRaddoseLine(line)
			elif parseDoseAvg in line and "MGy" in line:
				avgDose = self.parseRaddoseLine(line)
			elif parseElasYield in line:
				elasYield = self.parseRaddoseLine(line)
			elif parseDiffEff in line:
				diffEff = self.parseRaddoseLine(line)
			elif parseUsedVol in line:
				usedVol = self.parseRaddoseLine(line)
			elif parseAbsEnergy in line:
				absEnergy = self.parseRaddoseLine(line)
			elif parseDoseIneff in line:
				doseIneff = self.parseRaddoseLine(line)

		raddoseOutput.close()

		return (dwdDose, maxDose, avgDose, elasYield, diffEff, usedVol, absEnergy, doseIneff)

	def parseRaddoseLine(self, raddoseLine):
		"""Parses a line from the RADDDOSE-3D and returns the laast numerical
		value from the line.
		"""
		value = 0
		splitLine = raddoseLine.split(" ")
		for element in splitLine:
			if self.isfloat(element):
				value = float(element)
			elif "%" in splitLine[-1]:
				strValue = splitLine[-1]
				strippedVal = strValue.strip()
				value = float(strippedVal[0:-1])
		return value

	def isfloat(self, value):
		"""Checks whether a value can be parsed as a float.
		"""
		try:
			float(value)
			return True
		except ValueError:
			return False
