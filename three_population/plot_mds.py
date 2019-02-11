import numpy as np
import matplotlib
#matplotlib.use("cairo")
import matplotlib.pyplot as plt
import pickle
import os

prop_cycle = plt.rcParams['axes.prop_cycle']
colors = np.array(prop_cycle.by_key()['color'])
from matplotlib.backends.backend_pdf import PdfPages
cwd = os.getcwd()

simulation_subfolder = "generate_mds"
cwd = os.getcwd()
simulation_subfolder = os.path.join(cwd, simulation_subfolder)
fig = plt.figure()
ax = fig.add_subplot(111)
ax.spines['top'].set_color('none')
ax.spines['bottom'].set_color('none')
ax.spines['left'].set_color('none')
ax.spines['right'].set_color('none')
ax.tick_params(labelcolor='w', top='off', bottom='off', left='off', right='off')
ax.set_xlabel("Dimension 1")
ax.set_ylabel("Dimension 2")
colors_three_pop = np.concatenate((np.full(20,colors[0]),np.full(20,colors[4]),np.full(20,colors[2])))
for iL, L in enumerate([100,1000,10000,100000]):
    location_vector = os.path.join (simulation_subfolder, f'/{simulation_subfolder}/L_{L}/MDS_eigensystem/p2.vecs.data')
    val,vec = pickle.load(open(location_vector,"rb"))
    ax = fig.add_subplot(2,2,iL+1)
    ax.set_xlim([-0.3,0.3])
    if iL in [0,1]:
        ax.set_xticks([])
    if iL in [1,3]:
        ax.set_yticks([])
    ax.set_ylim([-0.3,0.3])
    ax.text(0.02,0.2,f'L = {L}')
    order = np.argsort(-val)
    dir_x = 1
    if iL == 0:
        dir_x = -1
    dir_y = 1
    if iL in [2,3]:
        dir_y = -1
    ax.scatter(dir_x*vec[:,order[0]],dir_y*vec[:,order[1]],c = colors_three_pop,alpha = 0.5)
fig.show()
fig.savefig(os.path.join("mds_three_population.pdf"))
