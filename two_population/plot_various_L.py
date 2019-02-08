import numpy as np
import matplotlib
#matplotlib.use("cairo")
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import os


from matplotlib.backends.backend_pdf import PdfPages
cwd = os.getcwd()

simulation_subfolder = "convergence_speed"
cwd = os.getcwd()
simulation_subfolder = os.path.join(cwd, simulation_subfolder)
Ls = [int(10 ** (i / 4)) for i in range(8, 20)]  # regulary space with 4 point between each order of magnitude
D = 0.01
all_distances1 = [[0, 0]]
for L in Ls:
    distance_summary_file = f'convergence_various_L/L_{L}_D_{D}.dat'
    distances = np.loadtxt(distance_summary_file)
    for distance in distances:
        all_distances1 = np.append(all_distances1, [[L, distance[0]]], axis=0)

all_distances2 = [[0, 0]]
D = 0.1
for L in Ls:
    distance_summary_file = f'convergence_various_L/L_{L}_D_{D}.dat'
    distances = np.loadtxt(distance_summary_file)
    for distance in distances:
        all_distances2 = np.append(all_distances2, [[L, distance[0]]], axis=0)


prop_cycle = plt.rcParams['axes.prop_cycle']
colors = prop_cycle.by_key()['color']
dico = {"loci": all_distances1[1:,0].astype("int"), "distance" :all_distances1[1:,1]}
all_dist = pd.DataFrame(data = dico)
all_dist["loci"] = all_dist["loci"].astype('category')

ax = sns.violinplot(x = "loci", y="distance",data = all_dist,scale="width",
                    inner="quartiles", color = colors[0], alpha =.5,
                    linewidth=0.)
mean_dist_by_L = all_dist.groupby("loci").mean()
ax.plot(range(12),  mean_dist_by_L.values,"_",color = colors[0],markersize=7)
plt.setp(ax.collections, alpha=.4)
plt.axhline(y=0.02,color = colors[0],alpha = 0.5, label = "D = 0.02")
dico = {"loci": all_distances2[1:,0].astype("int"), "distance" :all_distances2[1:,1]}
all_dist = pd.DataFrame(data = dico)
all_dist["loci"] = all_dist["loci"].astype('category')
ax = sns.violinplot(x = "loci", y="distance",data = all_dist,scale="width",
                    inner=None, color = colors[2], alpha =.5,
                    linewidth=0)
mean_dist_by_L = all_dist.groupby("loci").mean()
ax.plot(range(12),  mean_dist_by_L.values,"_",color = colors[2],markersize=7)
plt.setp(ax.collections, alpha=.4)
plt.axhline(y=0.2,color = colors[2],alpha = 0.5, label = "D = 0.2")
_,value = plt.xticks()
plt.xticks(range(0,12,2),np.array(value)[0:12:2])



plt.legend()
plt.xlabel("Number of SNPs")
plt.ylabel("Divergence time")
plt.savefig("two_pop_convergence_speed.pdf")

plt.cla()
prop_cycle = plt.rcParams['axes.prop_cycle']
colors = prop_cycle.by_key()['color']
dico = {"loci": all_distances2[1:,0].astype("int"), "distance" :all_distances2[1:,1]}
all_dist = pd.DataFrame(data = dico)
all_dist["loci"] = all_dist["loci"].astype('category')
ax = sns.violinplot(x = "loci", y="distance",data = all_dist,scale="width",
                    inner=None, color = colors[2], alpha =.5,
                    linewidth=0)
mean_dist_by_L = all_dist.groupby("loci").mean()
ax.plot(range(12),  mean_dist_by_L.values,"_",color = colors[2],markersize=7)
plt.setp(ax.collections, alpha=.4)
plt.axhline(y=0.2,color = colors[2],alpha = 0.5, label = "$D_{12} = 0.2$")
_,value = plt.xticks()
plt.xticks(range(0,12,2),np.array(value)[0:12:2])



plt.legend()
plt.xlabel("Number of SNPs")
plt.ylabel("split time")
plt.savefig("two_pop_convergence_speed2.pdf")