# Generate scaled models
import os
import glob
import opensim

# Check if the target folder exists
modelPath = './VirtualSubjectModels'
scaleSetPath = './VirtualSubjectScaleSets'

if not os.path.exists(modelPath):
    os.mkdir(modelPath)

if not os.path.exists(scaleSetPath):
    os.mkdir(scaleSetPath)

# Where are all the scale files located?
scaleFileDirectory = './VirtualSubjectScaleFiles'

# Get a list of all the files located there
scaleFileList = glob.glob(scaleFileDirectory + '/*.xml')

# Load each file in this folder and run it
for fileName in scaleFileList:
    currScaleFile = opensim.ScaleTool(fileName)
    currScaleFile.run()
