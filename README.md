# Synthetic-IMU
 Making synthetic IMU data using Opensim

Note: This only works with opensim4.5
Older versions of opensim report gyroscope signals in the global frame instead of the local frame.

# Order of operations - 
1. Run generateScaleFiles.py
2. Run generateScaledModels.py
3. Run runAnalysisTool.py

Congrats, your output acceleration, angular velocity and orientation files are in "Results"
