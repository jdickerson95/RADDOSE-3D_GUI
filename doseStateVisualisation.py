import numpy as np

doseStateFile = "output-DoseState.csv" #file path of dose state csv

isoValues = np.array([63,64,65,66,67]) #values for the isosurfaces

data = np.genfromtxt(doseStateFile, delimiter=",")

x_pos = np.unique(data[:,0])
y_pos = np.unique(data[:,1])
z_pos = np.unique(data[:,2])

X, Y, Z = np.meshgrid(x_pos, y_pos, z_pos)

dose = data[:,3].reshape(X.shape)
