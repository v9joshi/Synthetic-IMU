# Import libraries
import numpy
import opensim
import os

# Where should we store all the modified model files?
modelFilePath = './ModifiedBaseModels'

if not os.path.exists(modelFilePath):
    os.mkdir(modelFilePath)

# How many new models do we want to make?
numVirtualSubjects = 2 # Making a thousand is equally easy

# Load the base model
baseModelName  = "RajagopalModel.osim"

# How much do we want to translate the IMUs by?
meanPosErrorX    = 0   
stddevPosErrorX  = 0.02

meanPosErrorY   = 0
stddevPosErrorY = 0.02

meanPosErrorZ   = 0
stddevPosErrorZ = 0.02

# Load the base model
baseModel = opensim.Model(baseModelName)

# Get the names of all of the imu frames in the base model
IMUContainer = baseModel.getMiscModelComponentSet()
numIMUFrames = IMUContainer.getSize()

frameNames = []

for iter in range(numIMUFrames):
    currFrame = IMUContainer.get(iter).getSocket('frame').getConnecteePath()
    frameNames.append(currFrame)

print(frameNames)

# Make all the model files
for currSubj in range(numVirtualSubjects):
    # Reload the base model
    baseModel      = opensim.Model(baseModelName)

    # Set the file name
    modelFileName   = modelFilePath + '/IMUplacement_Rajagopal_' + str(currSubj) + '.osim'
    
    # Modify the positions of each IMU one at a time
    for imuFrame in frameNames:
        # Get the imu frame from the body
        IMUFrame = baseModel.getComponent(imuFrame)

        # Find the position of the IMU frame
        IMUpos = IMUFrame.get_translation().to_numpy()

        # How much should we move the IMU by?        
        randomMovX = numpy.random.normal(meanPosErrorX, stddevPosErrorX, 1)
        randomMovY = numpy.random.normal(meanPosErrorY, stddevPosErrorY, 1)
        randomMovZ = numpy.random.normal(meanPosErrorZ, stddevPosErrorZ, 1)
        posError   = numpy.array([randomMovX[0], randomMovY[0], randomMovZ[0]])

        # Make the new position
        IMUpos_new = IMUpos + posError

        # Set the new position
        IMUFrame.set_translation(opensim.Vec3(IMUpos_new))

    baseModel.finalizeConnections()
    baseModel.printToXML(modelFileName)
        

