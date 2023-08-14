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

# Set the names of the bodies with IMUs attached to them
bodyNames = ['torso', 
            'pelvis',
            'tibia_r',
            'femur_r',
            'calcn_r',
            'tibia_l',
            'femur_l',
            'calcn_l']

# Make all the model files
for currSubj in range(numVirtualSubjects):
    # Load the base model
    baseModel      = opensim.Model(baseModelName)

    # Set the file name
    modelFileName   = modelFilePath + '/IMUplacement_Rajagopal_' + str(currSubj) + '.osim'
    
    # Modify the positions of each IMU one at a time
    for body in bodyNames:
        # Get the body from the model file
        currBody = baseModel.getBodySet().get(body)

        # Get the imu frame from the body
        IMUFrame = currBody.getComponent(body + '_imu')

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
        

