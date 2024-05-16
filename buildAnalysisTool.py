import opensim

# Build the analysis tool
def buildAnalysisTool(modelFileName, coordinatesFileName, analysisFileName, resultsDir):
    # Make an analysis tool
    testTool = opensim.AnalyzeTool()
    testTool.setModelFilename(modelFileName)
    testTool.setName(analysisFileName[:-4])

    # Set the states files for the model
    coordsData = opensim.Storage(coordinatesFileName)
    testTool.setCoordinatesFileName(coordinatesFileName)

    # Set the analysis duration
    startTime = coordsData.getFirstTime()
    endTime = coordsData.getLastTime()

    testTool.setStartTime(startTime)
    testTool.setFinalTime(endTime)

    # Set the output folder
    testTool.setResultsDir(resultsDir)

    # Make an analysis set
    newAnalysisSet = testTool.updAnalysisSet()

    # Make the IMU data reporter
    dataReporter = opensim.IMUDataReporter()

    # Set properties for the data reporter
    dataReporter.setOn(True)
    dataReporter.setStartTime(startTime)
    dataReporter.setEndTime(endTime)

    # What outputs do you want?
    dataReporter.set_report_accelerometer_signals(True)
    dataReporter.set_report_gyroscope_signals(True)
    dataReporter.set_report_orientations(True)
    dataReporter.set_compute_accelerations_without_forces(True)

    # Outputs in degrees?
    dataReporter.setInDegrees(True)

    # Add the data reporter to the analysis set
    newAnalysisSet.adoptAndAppend(dataReporter)

    # Print the analysis file
    testTool.printToXML(analysisFileName)
