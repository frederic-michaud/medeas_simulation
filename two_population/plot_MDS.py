import numpy as np
import matplotlib.pyplot as plt
import os
import pickle
cwd = os.getcwd()
print(cwd)
prop_cycle = plt.rcParams['axes.prop_cycle']
colors = np.array(prop_cycle.by_key()['color'])
simulation_subfolder = "generate_mds"
fig = plt.figure()
ax = fig.add_subplot(111)
ax.spines['top'].set_color('none')
ax.spines['bottom'].set_color('none')
ax.spines['left'].set_color('none')
ax.spines['right'].set_color('none')
ax.tick_params(labelcolor='w', top='off', bottom='off', left='off', right='off')
ax.set_xlabel("Dimension 1")
ax.set_ylabel("Dimension 2")
for iL, L in enumerate([100,1000,10000,100000]):
    val,vec = pickle.load(open(f'{simulation_subfolder}/L_{L}_D_0.01/MDS_eigensystem/p2.vecs.data',"rb"))
    ax = fig.add_subplot(2,2,iL+1)
    scale = 0.1
    ax.set_xlim([-scale,scale])
    ax.set_ylim([-scale,scale])
    ax.text(0.02,scale*0.6,f'L = {L}')
    order = np.argsort(-val)
    pointColor = colors[np.concatenate((np.full(20,0,dtype=int),np.full(20,2,dtype=int)))]
    if iL in [0,1]:
        ax.set_xticks([])
    if iL in [1,3]:
        ax.set_yticks([])
    ax.scatter(np.sqrt(val[order[0]])*vec[:,order[0]],np.sqrt(val[order[1]])*vec[:,order[1]],c = pointColor,alpha=0.5)
plt.show()
fig.savefig("pca_two_population.pdf")