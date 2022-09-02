# Import libraries
import os
import glob
import opensim
from buildAnalysisTool import *

# Build the analysis tool
if __name__=="__main__":
    # Where are all the models located?
    modelPath = './Models'

    # The outputs go here
    resultsPath = './Results'

    if not os.path.exists(resultsPath):
        os.mkdir(resultsPath)

    # Set the coordinates file name and the general analysis file name
    coordinatesFileName = "walking_motion.sto"
    analysisFileName = "opensenseIMUDataReporter.xml"

    # Find all the scaled models
    scaledModelList = glob.glob(modelPath + '/*.osim')

    # Loop through each model, make an analysis tool for it, and then run it
    for scaledModelFile in scaledModelList:
        # Set the model file name
        modelFileName = scaledModelFile

        # Build the analysis tool for this model
        buildAnalysisTool(modelFileName, coordinatesFileName, analysisFileName)

        # Load the tool again, have to do this to associate the model
        testTool = opensim.AnalyzeTool(analysisFileName)

        # Set the output file name
        outputFileHeader = 'virtual_subject_' + scaledModelFile.split('_')[2][:-5]
        testTool.setName(outputFileHeader)

        # Run the analysis tool to generate output data
        testTool.run()
