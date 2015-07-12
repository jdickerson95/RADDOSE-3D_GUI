from Tkinter import *
from ttk import *
import tkMessageBox
import tkFileDialog
from HoverInfo import HoverInfo
from InputsHelpText import PremadeInputHelp
import os
import shutil
import BeamModule

class PremadeInputMakerWindow():

    def __init__(self, MainGui):
        self.master = MainGui.top_premadeRunMaker
        self.premadeMakerFrame = Frame(self.master)
        self.premadeMakerFrame.pack()
        self.lightcolour = MainGui.lightcolour
        self.darkcolour = MainGui.darkcolour

        # Wedge inputs here:
        l = Label(self.master,text="Premade Input Files",style="labelFrameTitle.TLabel")
        self.inputsFrame = LabelFrame(self.master,labelwidget=l,style="MakeABeam.TFrame")
        self.inputsFrame.pack(side=TOP,padx=10, pady=10,fill=BOTH,expand=TRUE)

        #Create object that contains the help text
        self.helpText = PremadeInputHelp()

        self.rd3dInputFile = StringVar()
        self.rd3dInputFile.set("")
        self.rd3dinputFileSection()

        self.sampleModelFile = StringVar()
        self.sampleModelFile.set("")
        self.sampleModelFileInput()

        self.sequenceFile = StringVar()
        self.sequenceFile.set("")
        self.sequenceFileInput()

        self.beamImageFile = StringVar()
        self.beamImageFile.set("")
        self.beamImageFileInput()

        self.beamApertureXFile = StringVar()
        self.beamApertureXFile.set("")
        self.beamApertureXFileInput()

        self.beamApertureYFile = StringVar()
        self.beamApertureYFile.set("")
        self.beamApertureYFileInput()

        self.expNameInput = StringVar()
        self.expNameInput.set("")
        self.expNameInputSection(MainGui)

        self.inputsFrame.grid_rowconfigure(0,weight=1)
        self.inputsFrame.grid_rowconfigure(1,weight=1)
        self.inputsFrame.grid_rowconfigure(2,weight=1)
        self.inputsFrame.grid_rowconfigure(3,weight=1)
        self.inputsFrame.grid_rowconfigure(4,weight=1)
        self.inputsFrame.grid_rowconfigure(5,weight=1)
        self.inputsFrame.grid_rowconfigure(6,weight=1)
        self.inputsFrame.grid_columnconfigure(0,weight=1)
        self.inputsFrame.grid_columnconfigure(1,weight=1)
        self.inputsFrame.grid_columnconfigure(2,weight=1)
        self.inputsFrame.grid_columnconfigure(3,weight=1)
        self.inputsFrame.grid_columnconfigure(4,weight=1)
        self.inputsFrame.grid_columnconfigure(5,weight=1)
        self.inputsFrame.grid_columnconfigure(6,weight=1)

    def rd3dinputFileSection(self):
        # add RD3D input file 'load' option to runPremadeRD3DStrategyFrame frame here
        loadLabel = Label(self.inputsFrame,text="RADDOSE-3D input file load",style="inputBoxes.TLabel")
        loadLabel.grid(row=0, column=0,pady=5,padx=6,sticky=W+E)
        HoverInfo(loadLabel, self.helpText.inputFileText)
        inputLoadBox = Entry(self.inputsFrame,textvariable=self.rd3dInputFile)
        inputLoadBox.grid(row=0, column=1,columnspan=5,pady=5,sticky=W+E)
        addInputButton = Button(self.inputsFrame,text="Find File",command= lambda: self.clickInputLoad(inputLoadBox))
        addInputButton.grid(row=0, column=6,pady=5,padx=6,sticky=W+E)

    def sampleModelFileInput(self):
        loadLabel = Label(self.inputsFrame,text="Sample geometry file load",style="inputBoxes.TLabel")
        loadLabel.grid(row=1, column=0,pady=5,padx=6,sticky=W+E)
        HoverInfo(loadLabel, self.helpText.sampleGeomText)
        inputLoadBox = Entry(self.inputsFrame,textvariable=self.sampleModelFile)
        inputLoadBox.grid(row=1, column=1,columnspan=5,pady=5,sticky=W+E)
        addInputButton = Button(self.inputsFrame,text="Find File",command= lambda: self.clickInputLoad(inputLoadBox))
        addInputButton.grid(row=1, column=6,pady=5,padx=6,sticky=W+E)

    def sequenceFileInput(self):
        loadLabel = Label(self.inputsFrame,text="Sequence file load",style="inputBoxes.TLabel")
        loadLabel.grid(row=2, column=0,pady=5,padx=6,sticky=W+E)
        HoverInfo(loadLabel, self.helpText.sequenceFileText)
        inputLoadBox = Entry(self.inputsFrame,textvariable=self.sequenceFile)
        inputLoadBox.grid(row=2, column=1,columnspan=5,pady=5,sticky=W+E)
        addInputButton = Button(self.inputsFrame,text="Find File",command= lambda: self.clickInputLoad(inputLoadBox))
        addInputButton.grid(row=2, column=6,pady=5,padx=6,sticky=W+E)

    def beamImageFileInput(self):
        loadLabel = Label(self.inputsFrame,text="Beam image file load",style="inputBoxes.TLabel")
        loadLabel.grid(row=3, column=0,pady=5,padx=6,sticky=W+E)
        HoverInfo(loadLabel, self.helpText.beamImageText)
        inputLoadBox = Entry(self.inputsFrame,textvariable=self.beamImageFile)
        inputLoadBox.grid(row=3, column=1,columnspan=5,pady=5,sticky=W+E)
        addInputButton = Button(self.inputsFrame,text="Find File",command= lambda: self.clickInputLoad(inputLoadBox))
        addInputButton.grid(row=3, column=6,pady=5,padx=6,sticky=W+E)

    def beamApertureXFileInput(self):
        loadLabel = Label(self.inputsFrame,text="Beam aperture measurements (Horizontal)",style="inputBoxes.TLabel")
        loadLabel.grid(row=4, column=0,pady=5,padx=6,sticky=W+E)
        HoverInfo(loadLabel, self.helpText.beamApXText)
        inputLoadBox = Entry(self.inputsFrame,textvariable=self.beamApertureXFile)
        inputLoadBox.grid(row=4, column=1,columnspan=5,pady=5,sticky=W+E)
        addInputButton = Button(self.inputsFrame,text="Find File",command= lambda: self.clickInputLoad(inputLoadBox))
        addInputButton.grid(row=4, column=6,pady=5,padx=6,sticky=W+E)

    def beamApertureYFileInput(self):
        loadLabel = Label(self.inputsFrame,text="Beam aperture measurements (Vertical)",style="inputBoxes.TLabel")
        loadLabel.grid(row=5, column=0,pady=5,padx=6,sticky=W+E)
        HoverInfo(loadLabel, self.helpText.beamApYText)
        inputLoadBox = Entry(self.inputsFrame,textvariable=self.beamApertureYFile)
        inputLoadBox.grid(row=5, column=1,columnspan=5,pady=5,sticky=W+E)
        addInputButton = Button(self.inputsFrame,text="Find File",command= lambda: self.clickInputLoad(inputLoadBox))
        addInputButton.grid(row=5, column=6,pady=5,padx=6,sticky=W+E)

    def expNameInputSection(self, MainGui):
        # add experiment naming option to runPremadeRD3DStrategyFrame frame here. Name is what user wishes to
        # call the current experiment for future reference
        premadeRD3DStrategyLabel = Label(self.inputsFrame,text="Experiment Name",style="inputBoxes.TLabel")
        premadeRD3DStrategyLabel.grid(row=6, column=0,pady=5,padx=6,sticky=W+E)
        HoverInfo(premadeRD3DStrategyLabel, self.helpText.expNameText)
        premadeRD3DStrategyBox = Entry(self.inputsFrame,textvariable=self.expNameInput)
        premadeRD3DStrategyBox.grid(row=6, column=1,columnspan=5,pady=5,sticky=W+E)
        premadeRD3DRunButton = Button(self.inputsFrame,text="Run", command= lambda: self.runExp(MainGui))
        premadeRD3DRunButton.grid(row=6, column=6,pady=5,padx=6,sticky=W+E)

    def clickInputLoad(self,inputBox):
        """Load a pre-made file

        Function to allow file search and load of a pre-made input file

        =================
        Keyword arguments
        =================
        inputBox:
            The input text box that should be populated with the file path once
            a file is selected.

        =================
        Return parameters
        =================
        No explicit return parameters

        """
        self.inputLoad = tkFileDialog.askopenfilename(parent=self.master,title='Load input file')
        inputBox.delete(0,END)
        inputBox.insert(0,self.inputLoad)

    def runExp(self, MainGui):
        #Check that an experiment name was given
        if self.expNameInput.get():
            #Check if the RADDOSE-3D input file has been supplied
            if os.path.isfile(self.rd3dInputFile.get()):
                #Return collimation and pixel size beam parameters from Input
                #file
                beamParams = self.getBeamParamsFromInput(self.rd3dInputFile.get())
                #Make sure horizontal collimation parameter is inpt first
                collimation = [beamParams[1], beamParams[0]]
                pixelSize = [beamParams[2], beamParams[3]]

                beamFileInputIsFine = self.processExperimentalBeam(collimation, pixelSize)

                if beamFileInputIsFine:
                    #Get a full list of all the variables representing file names
                    fullFileVarList = [self.rd3dInputFile.get(), self.sampleModelFile.get(),
                                       self.sequenceFile.get(), self.beamImageFile]

                    #Determine which of the files have non empty strings and put those in a
                    #separate list
                    nonEmptyFileList = []
                    for filename in fullFileVarList:
                        if filename:
                            nonEmptyFileList.append(filename)

                    if len(nonEmptyFileList) > 1:
                        #Parse the input file to determine the names of any other files
                        filenames = self.getFileNamesFromRD3DInput(self.rd3dInputFile.get())
                    else:
                        filenames = []

                    #Copy the specified files into the current directory and rename them
                    #according to the names specified in the input file
                    allFilesExist = self.copyFiles(nonEmptyFileList, os.getcwd(), filenames)

                    if allFilesExist:
                        MainGui.runPremadeRD3DExperiment(self.rd3dInputFile.get().split("/")[-1],self.expNameInput.get(),filenames)
                        # once this function runs, the toplevel window should be exited
                        self.master.destroy()
                    else:
                        string = """At least one of the files specified does not exist.
            Please check the file names given in the input boxes and make sure they exist.
            """ %()
                        tkMessageBox.showinfo( "No Experiment Name", string)
            else:
                string = """RADDOSE-3D input file was not specified. Please give the path to the input file.
        """ %()
                tkMessageBox.showinfo( "RADDOSE-3D Input file not specified", string)
        else:
            string = """No experiment name has been given.\nPlease give a name to the experiment that you wish to run in the 'Experiment Name' field.
            """ %()
            tkMessageBox.showinfo( "No Experiment Name", string)

    def copyFiles(self, srcFileList, dirPath, filenames):
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

    def getFileNamesFromRD3DInput(self, rd3dInputFile):
        """Extract additonal file names from RADDOSE-3D input file

        This function takes a string containing the path to the RADDOSE-3D
        input file. It parses the file and looks for lines that contain
        paths to other files required for the RADDOSE-3D simulation. It
        stores the strings corresponding to these additional files in a list
        and returns the list.
        =================
        Keyword arguments
        =================
        rd3dInputFile:
            String corresponding to the path of the RADDOSE-3D input file.

        =================
        Return parameters
        =================
        filenameList:
            A list containing strings with the names of the additional files
            required for the RADDOSE-3D simulation.
        """
        try:
            rd3dFile = open(rd3dInputFile, "r")
        except IOError:
            string = """The RADDOSE-3D input file could not be read.
Please make sure that it is not being used by any other processes.
    """ %()
            tkMessageBox.showinfo( "Cannot read file", string)
        modelFilename = ""
        sequenceFilename = ""
        beamFilename = ""
        filenameList = []
        for line in rd3dFile:
            if "modelfile" in line.lower():
                modelFilename = line.split()[1]
            elif "seqfile" in line.lower() or "sequencefile" in line.lower():
                sequenceFilename = line.split()[1]
            elif ".pgm" in line:
                beamFilename = line.split()[1]
        if modelFilename:
            filenameList.append(modelFilename)
        if sequenceFilename:
            filenameList.append(sequenceFilename)
        if beamFilename:
            filenameList.append(beamFilename)
        return filenameList

    def getBeamParamsFromInput(self, rd3dInputFile):
        """Extract beam parameters from RADDOSE-3D input file

        This function takes a string containing the path to the RADDOSE-3D
        input file. It parses the file and looks for lines that contain the
        pixel size values and the collimation values and returns those
        parameters
        =================
        Keyword arguments
        =================
        rd3dInputFile:
            String corresponding to the path of the RADDOSE-3D input file.

        =================
        Return parameters
        =================
        beamParams:
            A list containing strings with the pixel size and collimation
            parameters for RADDOSE-3D input.
        """
        try:
            rd3dFile = open(rd3dInputFile, "r")
        except IOError:
            string = """The RADDOSE-3D input file could not be read.
Please make sure that it is not being used by any other processes.
    """ %()
            tkMessageBox.showinfo( "Cannot read file", string)
        collimationVert = ""
        collimationHorz = ""
        pixelX          = ""
        pixelY          = ""
        beamParams = []
        for line in rd3dFile:
            if "collimation" in line.lower():
                collimationVert = line.split()[2]
                collimationHorz = line.split()[3]
            elif "pixelsize" in line.lower() or "sequencefile" in line.lower():
                pixelX          = line.split()[1]
                pixelY          = line.split()[2]
        beamParams = [collimationVert, collimationHorz, pixelX, pixelY]
        return beamParams

    def processExperimentalBeam(self, collimation, pixelSize):
        # To be honest I did the if statements as I went along without actually
        # thinking about how to structure them. So some of the conditions may be
        #redundant. Or worse, I may not catch some errors (I think the former is
        # more likley though).
        beamFileInputIsFine = True
        apertureDiameter = 10 #in microns. This is the diameter of the aperture
        #used to do the measurements
        apertureStep = 2 #in microns. This is the distance from one measurement
        #to the next in the aperture scan.

        #The relative weighting of red, green and blue in colour beam images
        #when performing the grayscale conversion.
        red = 0.45
        green = 0.45
        blue = 0.1

        if os.path.isfile(self.beamImageFile.get()) and ".pgm" in self.beamImageFile.get():
            self.beamImageFile = self.beamImageFile.get()
        elif ((".pgm" in self.beamImageFile.get() and len(self.beamImageFile.get().split("/")) == 1 and
        not os.path.isfile(self.beamImageFile.get())) or not self.beamImageFile.get()):
            if (os.path.isfile(self.beamApertureXFile.get()) and os.path.isfile(self.beamApertureYFile.get()) and
            ".dat" in self.beamApertureXFile.get() and ".dat" in self.beamApertureYFile.get()):
                if not self.beamImageFile.get():
                    self.beamImageFile = "beamInput.pgm"
                else:
                    self.beamImageFile = self.beamImageFile.get()
                BeamModule.Beam.initialiseBeamFromApMeas(self.beamApertureXFile.get(),self.beamApertureYFile.get(),
                                                            "threshold", apertureDiameter, apertureStep,
                                                                        self.beamImageFile,"gaussfitconv",True,"smoothgauss")
            elif os.path.isfile(self.beamImageFile.get()):
                beamFileInputIsFine = False
                beamFileWarningMessage = """The aperture measurement files either don't exist or they are not in a compatible format (.dat).
    """
                tkMessageBox.showinfo("Problem with aperture measurement files",beamFileWarningMessage)
            else:
                beamFileInputIsFine = False
                beamFileWarningMessage = """Not all the necessary files required to process a beam image were given.
Please see the documentation for more information."""
                tkMessageBox.showinfo("Problem with aperture measurement files",beamFileWarningMessage)
        elif ".png" in self.beamImageFile.get() and os.path.isfile(self.beamImageFile.get()):
            if collimation[0] and collimation[1] and pixelSize[0] and pixelSize[1]:
                filenameWithExt = self.beamImageFile.get().split("/")[-1]
                filenameWOExt = filenameWithExt.split(".")[0]
                pgmFilename = "{}.pgm".format(filenameWOExt)
                BeamModule.Beam.initialiseBeamFromPNG(self.beamImageFile.get(),red, green, blue, pgmFilename,
                [float(collimation[0]), float(collimation[1])],
                [float(pixelSize[0]), float(pixelSize[1])])
                self.beamImageFile = pgmFilename
            else:
                beamFileInputIsFine = False
                beamFileWarningMessage = """There is incomplete information about the pixel size and the
collimation. If you would like to use a png file of the experimental beam then these parameters
must be specified in the input so that the conversion process can estimate a suitable background
correction for the image.
"""
                tkMessageBox.showinfo("Pixel Size and/or Collimation not Specified",beamFileWarningMessage)

        elif len(self.beamImageFile.get().split("/")) > 1 and not os.path.isfile(self.beamImageFile.get()):
            beamFileInputIsFine = False
            beamFileWarningMessage = """The filename that you have supplied has not been found.
Please check the file path to ensure the file exists.
"""
            tkMessageBox.showinfo("beam image file has not been found",beamFileWarningMessage)
        else:
            beamFileInputIsFine = False
            beamFileWarningMessage = """The file type you have supplied is incompatible with this program.
Only aperture measurements in ".dat" format or image files in ".pgm" or "png" format are compatible.
"""
            tkMessageBox.showinfo("Incompatible file type",beamFileWarningMessage)
        return beamFileInputIsFine
