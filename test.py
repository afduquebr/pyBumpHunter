# Here we test pyBumpHunter.
# The result can be compared to what can be obtained with the original C++ version.
# We will use histograms ranging between 0 and 20 with 60 even bins.

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pyBumpHunter as BH
from datetime import datetime  ## Used to compute the execution time
import uproot as upr  ## Used to read data from a root file


# Open the file
File = upr.open('data.root')
File.items()

# Background
bkg = File['bkg'].arrays(outputtype=np.array)

# Data
data = File['data'].arrays(outputtype=np.array)

# Position of the bump in the data
Lth = 5.5

# Range for the hitograms (same that the one used with C++ BumpHunter)
rang = [0,20]

# Plot the 2 distributions
F = plt.figure(figsize=(12,8))
plt.title('Test distribution')
plt.hist((bkg,data),bins=60,histtype='step',range=rang,label=('bakground','data'))
plt.legend()
plt.savefig('results_py/hist.png',bbox_inches='tight')
plt.close(F)


# Call the BumpHunter function
print('###FIRST CALL###')
begin = datetime.now()
BH.BumpHunter(
    data,bkg,Rang=rang,
    Width_min=2,
    Width_max=6,
    Width_step=1,
    Scan_step=1,
    npe=800,
    NWorker=1,
    Seed=666
)
end = datetime.now()
print('time={}'.format(end-begin))
print('')

# Print bump
BH.PrintBumpInfo()
BH.PrintBumpTrue(data,bkg)
print('   mean (true) = {}'.format(Lth))
print('')


# Get and save tomography plot
BH.GetTomography(data,filename='results_py/tomography1.png')


# Get and save bump plot
BH.PlotBump(data,bkg,filename='results_py/bump1.png')


# Get and save statistics plot
BH.PlotBHstat(show_Pval=True,filename='results_py/BH_statistics1.png')


# Change Parameters and cal BumpHunter function with keepparam argument
BH.scan_step='half'
BH.seed=42
print('###SECOND CALL###')
begin = datetime.now()
BH.BumpHunter(data,bkg,keepparam=True)
end = datetime.now()
print('time={}'.format(end-begin))
print('')

# Print new bump
BH.PrintBumpInfo()
BH.PrintBumpTrue(data,bkg)
print('   mean (true) = {}'.format(Lth))
print('')


# Get and save new tomography plot
BH.GetTomography(data,filename='results_py/tomography2.png')


# Get and save new bump plot
BH.PlotBump(data,bkg,filename='results_py/bump2.png')


# Get and save new statistics plot
BH.PlotBHstat(show_Pval=True,filename='results_py/BH_statistics2.png')


