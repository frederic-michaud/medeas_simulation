import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import os


cwd = os.getcwd()

simulation_subfolder = "convergence_various_L_changing_maf"
cwd = os.getcwd()
simulation_subfolder = os.path.join(cwd, simulation_subfolder)
Ls = [int(10 ** (i / 4)) for i in range(12, 24)]  # regulary space with 4 point between each order of magnitude
nb_Ls = len(Ls)
D = 0.01
all_distances1 = [[0, 0]]
maf=0
for L in Ls:
    distance_summary_file = f'convergence_various_L_changing_maf/L_{L}_D_{D}_maf_{maf}.dat'
    distances = np.loadtxt(distance_summary_file,ndmin=2)
    for distance in distances:
        all_distances1 = np.append(all_distances1, [[L, distance[0]]], axis=0)

all_distances2 = [[0, 0]]
maf=0.01
for L in Ls:
    distance_summary_file = f'convergence_various_L_changing_maf/L_{L}_D_{D}_maf_{maf}.dat'
    distances = np.loadtxt(distance_summary_file,ndmin=2)
    for distance in distances:
        all_distances2 = np.append(all_distances2, [[L, distance[0]]], axis=0)

all_distances3 = [[0, 0]]
maf=0.05
for L in Ls:
    distance_summary_file = f'convergence_various_L_changing_maf/L_{L}_D_{D}_maf_{maf}.dat'
    distances = np.loadtxt(distance_summary_file,ndmin=2)
    for distance in distances:
        all_distances3 = np.append(all_distances3, [[L, distance[0]]], axis=0)


prop_cycle = plt.rcParams['axes.prop_cycle']
colors = prop_cycle.by_key()['color']
dico = {"loci": all_distances1[1:,0].astype("int"), "distance" :all_distances1[1:,1]}
all_dist = pd.DataFrame(data = dico)
all_dist["loci"] = all_dist["loci"].astype('category')

ax = sns.violinplot(x = "loci", y="distance",data = all_dist,scale="width",
                    inner="quartiles", color = colors[0], alpha =.5,
                    linewidth=0.)
mean_dist_by_L = all_dist.groupby("loci").mean()
ax.plot(range(nb_Ls),  mean_dist_by_L.values[:,0],"_",color = colors[0],markersize=7, label = r"maf = 0")
plt.setp(ax.collections, alpha=.4)


#
dico = {"loci": all_distances2[1:,0].astype("int"), "distance" :all_distances2[1:,1]}
all_dist = pd.DataFrame(data = dico)
all_dist["loci"] = all_dist["loci"].astype('category')
ax = sns.violinplot(x = "loci", y="distance",data = all_dist,scale="width",
                    inner=None, color = colors[1], alpha =.5,
                    linewidth=0)
mean_dist_by_L = all_dist.groupby("loci").mean()
ax.plot(range(nb_Ls),  mean_dist_by_L.values[:,0],"_",color = colors[1],markersize=7, label = r"maf = 0.01")
plt.setp(ax.collections, alpha=.4)


_,value = plt.xticks()
plt.xticks(range(0,nb_Ls,2),np.array(value)[0:nb_Ls:2])

dico = {"loci": all_distances3[1:,0].astype("int"), "distance" :all_distances3[1:,1]}
all_dist = pd.DataFrame(data = dico)
all_dist["loci"] = all_dist["loci"].astype('category')
ax = sns.violinplot(x = "loci", y="distance",data = all_dist,scale="width",
                    inner=None, color = colors[2], alpha =.5,
                    linewidth=0)
mean_dist_by_L = all_dist.groupby("loci").mean()
ax.plot(range(nb_Ls),  mean_dist_by_L.values[:,0],"_",color = colors[2],markersize=7, label = r"maf = 0.05")
plt.setp(ax.collections, alpha=.4)


plt.axhline(y=0.02,color = "k",alpha = 0.5, label = r"Theoretical value",lw = 0.5)
_,value = plt.xticks()
plt.xticks(range(0,nb_Ls,2),np.array(value)[0:nb_Ls:2])
plt.ylim((0.015,0.03))


plt.legend()
plt.xlabel("Number of SNPs")
plt.ylabel("Divergence time")
plt.savefig("two_pop_convergence_various_maf.pdf")

