# Import libraries
import os
import glob
import opensim
from util.buildAnalysisTool import buildAnalysisTool

# Build the analysis tool
if __name__=="__main__":
    # Where are all the models located?
    modelPath = os.path.abspath('./tmp/VirtualSubjectModels')

    # The outputs go here
    resultsPath = os.path.abspath('./VirtualSubjectResults')

    if not os.path.exists(resultsPath):
        os.mkdir(resultsPath)

    # Set the coordinates file name and the general analysis file name
    coordinatesFileName = os.path.abspath("./util/walking_motion.sto")
    analysisFileName = os.path.abspath("./util/opensenseIMUDataReporter.xml")


    # Find all the scaled models
    scaledModelList = glob.glob(modelPath + '/*.osim')

    # Loop through each model, make an analysis tool for it, and then run it
    for scaledModelFile in scaledModelList:
        # Set the model file name
        modelFileName = scaledModelFile
        modelFileName = modelFileName

        # Build the analysis tool for this model
        buildAnalysisTool(modelFileName, coordinatesFileName, analysisFileName, resultsPath)

        # Load the tool again, have to do this to associate the model
        testTool = opensim.AnalyzeTool(analysisFileName)

        # Set the output file name
        outputFileHeader = 'virtual_subject_' + scaledModelFile.split('_')[2][:-5]
        testTool.setName(outputFileHeader)

        # Run the analysis tool to generate output data
        testTool.run()
