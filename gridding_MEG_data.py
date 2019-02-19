import pandas as pd
import mne
import matplotlib.pyplot as plt
import numpy as np
import scipy.interpolate as si
import os
import time

# Once 
gridMinimum = -100
gridMaximum = 100
gridStep = 4
indexToPlot = 1760

colName = ['chNum', 'x', 'y', 'unk1', 'unk2', 'chName']
layoutDf = pd.read_csv('/home/timb/NM306mag.lay', header=None, names=colName, delimiter=' ')

dataDir = '/media/NAS/timb/data/camcan/proc_data/TaskSensorAnalysis_transdef/CC620264'

x = layoutDf['x'].tolist()
y = layoutDf['y'].tolist()

evoked = mne.read_evokeds(os.path.join(dataDir, 'transdef_transrest_mf2pt2_task_raw_buttonPress_duration=3.4s_cleaned-epo-ave.fif'))[0]
evoked.pick_types(meg='mag')
a = evoked.data

data = a

gridSpacing = np.arange(gridMinimum,gridMaximum+gridStep,gridStep)
numGrids = gridSpacing.shape[0]

originalGrid = np.asarray([x,y]).T

[x1,y1] = np.meshgrid(gridSpacing, gridSpacing, sparse=True)

# Once per record

t1 = time.time()
newData_linear = si.griddata(originalGrid, data, (x1,y1), method='linear', fill_value=0)
elapsed = time.time()-t1
print(elapsed*75000/60/60)

plt.pcolor(range(numGrids), range(numGrids), newData_linear[:,:,indexToPlot], cmap='RdBu_r')
plt.colorbar()
plt.show()
