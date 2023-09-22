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
baseModelName  = "./BaseModels/RajagopalModel.osim"

# How much do we want to translate the IMUs by?
# Depth/Distance from bone
meanPosErrorX    = 0
stddevPosErrorX  = 0.02

# Rotational error in placement
minPlacementErrorAngle      = 0
maxPlacementErrorAngle      = 2*numpy.pi

minPlacementErrorRadius     = 0
maxPlacementErrorRadius     = 0.001

# Rotational error in orientation using XYZ Euler angles
# Roll/Long axis
minOrientationErrorXAngle    =  0*numpy.pi
maxOrientationErrorXAngle    =  0*numpy.pi

# Pitch/Short axis
minOrientationErrorYAngle    =  0*numpy.pi  
maxOrientationErrorYAngle    =  0*numpy.pi

# Yaw/Alignment with gravity/vertical
minOrientationErrorZAngle    =  -0.25*numpy.pi
maxOrientationErrorZAngle    =   0.25*numpy.pi

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

        # Find the position and orientation of the IMU frame
        IMUpos = IMUFrame.get_translation().to_numpy()
        IMUang = IMUFrame.get_orientation().to_numpy()

        # How much should we move the IMU by?        
        randomMovX      = numpy.random.normal(meanPosErrorX, stddevPosErrorX, 1)
        randomRotTheta  = numpy.random.uniform(minPlacementErrorAngle, maxPlacementErrorAngle, 1)
        randomMovRadius = numpy.random.normal(minPlacementErrorRadius, maxPlacementErrorRadius, 1)

        randomMovY      = randomMovRadius*numpy.cos(randomRotTheta)
        randomMovZ      = randomMovRadius*numpy.sin(randomRotTheta)

        posError        = numpy.array([randomMovX[0], randomMovY[0], randomMovZ[0]])

        # Make the new position
        IMUpos_new = IMUpos + posError

        # Set the new position
        IMUFrame.set_translation(opensim.Vec3(IMUpos_new))

        # Rotate the IMU
        randomRotThetaX = numpy.random.uniform(minOrientationErrorXAngle, maxOrientationErrorXAngle, 1)
        randomRotThetaY = numpy.random.uniform(minOrientationErrorYAngle, maxOrientationErrorYAngle, 1)
        randomRotThetaZ = numpy.random.uniform(minOrientationErrorZAngle, maxOrientationErrorZAngle, 1)

        angError        = numpy.array([randomRotThetaX[0], randomRotThetaY[0], randomRotThetaZ[0]])

        # Make the new orientation
        IMUang_new = IMUang + angError

        # Set the new position
        IMUFrame.set_orientation(opensim.Vec3(IMUang_new))



    baseModel.finalizeConnections()
    baseModel.printToXML(modelFileName)
        

