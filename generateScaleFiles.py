# Import libraries
import os
import numpy
import opensim

# Where should we store all the scale files?
scaleFilePath = './VirtualSubjectScaleFiles'

if not os.path.exists(scaleFilePath):
    os.mkdir(scaleFilePath)

# How many scaled models do we want to make?
numVirtualSubjects = 2 # Making a thousand is equally easy

# Generate a scaled model
baseModelName  = "./BaseModels/RajagopalModel.osim"
baseHeight = 1.70 # The height of the Rajagopal model

heightMean   = 1.75 # 1.61m for females, 1.75m for males from CDC tables
heightStdDev = 0.14 # 0.14m for females, 0.14m for males from CDC tables

meanScaleFactor   = heightMean/baseHeight
stddevScaleFactor = heightStdDev/heightMean

randomScaleFactors = numpy.random.normal(meanScaleFactor, stddevScaleFactor, numVirtualSubjects)

# Load the base model
baseModel = opensim.Model(baseModelName)

# Get the list of all the bodies in the base model
bodySet   = baseModel.getBodySet()
numBodies = baseModel.getNumBodies()
bodyNames = []

for currBody in range(numBodies):
    currBodyName = bodySet.get(currBody).getName()
    bodyNames.append(currBodyName)

# Make all the scale files
for currSubj in range(numVirtualSubjects):
    subjectName = 'virtual_subject_' + str(currSubj)
    currScaleFactor = randomScaleFactors[currSubj]

    # Load a generic scale tool file
    genericScaleTool = opensim.ScaleTool('./SourceFiles/genericScaleFile.xml')
    genericScaleTool.setName(subjectName)

    # Get the model maker in this scale file
    genericModelMaker = genericScaleTool.getGenericModelMaker()
    # Set the input model
    genericModelMaker.setModelFileName(baseModelName)

    # Get the model scaler in this scale file
    genericModelScaler = genericScaleTool.getModelScaler()
    genericModelScaler.setOutputModelFileName('./VirtualSubjectModels/'+ subjectName + '.osim')
    genericModelScaler.setOutputScaleFileName('./VirtualSubjectScaleSets/'+ subjectName + '.xml')

    genericModelScaler.setApply(True)

    # Get the scaling order
    scalingOrder = genericModelScaler.getScalingOrder()

    # Remove any existing scales
    while scalingOrder.getSize() > 0:
        scalingOrder.remove(0)

    # Add a manual scale
    scalingOrder.insert(0,'manualScale')

    # Get the scale set
    genericScaleSet = genericModelScaler.getScaleSet()

    # Check that this scale set is empty, if not then empty it
    if genericScaleSet.getSize() > 0:
        genericScaleSet.clearAndDestroy()

    # Make new scales for each body in the model
    for currBody in range(numBodies):
        newScaleGroup = opensim.Scale()
        newScaleGroup.setName(bodyNames[currBody] + '_scaler')
        newScaleGroup.setSegmentName(bodyNames[currBody])

        # Make a vector to set the scale value
        scaleVector = opensim.Vec3(currScaleFactor) # Uniform scaling in x,y,z

        # Set the scale value
        newScaleGroup.setScaleFactors(scaleVector)

        # Make sure this scale gets applied
        newScaleGroup.setApply(True)

        # Add this scale to the scale set
        genericScaleSet.adoptAndAppend(newScaleGroup)

    # Print this scale file
    genericScaleTool.printToXML(scaleFilePath + '/' + subjectName + '_ScaleFile.xml')
