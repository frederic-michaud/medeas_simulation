import numpy as np
import matplotlib
#matplotlib.use("cairo")
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import os


prop_cycle = plt.rcParams['axes.prop_cycle']
colors = prop_cycle.by_key()['color']


simulation_subfolder = "convergence_various_D"
cwd = os.getcwd()
simulation_subfolder = os.path.join(cwd,simulation_subfolder)
Ls = [1000]
Ds = np.array([10**(-i/4+1) for i in range(17)])
all_distances1= [[0,0]]
sigma1 = [[0,0,0]]
for L in Ls:
    for D in Ds:
        distance_summary_file = os.path.join(simulation_subfolder,f'L_{L}_D_{D}.dat')
        distances  = np.loadtxt(distance_summary_file)
        for distance in distances:
           all_distances1 = np.append(all_distances1,[[D,distance[0]]],axis = 0)
        sigma_within = np.std(distances[1:,0],ddof=1)
        sigma_outside = np.sqrt(np.sum((distances[1:,0]-2*D)**2)/len(distances[1:,0]))
        sigma1 = np.append(sigma1,[[L,sigma_within, sigma_outside]],axis = 0)


dico = {"given_distance": all_distances1[1:,0], "distance" :0.5*all_distances1[1:,1]/all_distances1[1:,0]}
all_dist = pd.DataFrame(data = dico)
all_dist["given_distance"] = all_dist["given_distance"].astype('category')


ax = sns.violinplot(x = "given_distance", y="distance",data = all_dist,scale="width",
                    inner="quartiles", color = colors[0], alpha =.5,
                    linewidth=0.)
ax.axhline(y=1,color=colors[0],lw=.5)

plt.setp(ax.collections, alpha=.4)
mean_dist_by_L = all_dist.groupby("given_distance").mean()
ax.plot(range(17),  mean_dist_by_L.values,"_",color = colors[0],markersize=7)
ax.set_xlabel("$D_{12}$")
ax.set_ylabel("observed/expected")
ax.set_xlim((-1,16))
ax.set_ylim(0,5)
aaa = plt.xticks()
pos_ticks = [0,4,8,12,16]
plt.xticks(pos_ticks,[aaa[1][i] for i in pos_ticks])

plt.savefig("two_pop_different_D.pdf")