import numpy as np
import matplotlib
#matplotlib.use("cairo")
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import os
plt.rcParams.update({'font.size': 14})
fig = plt.figure()
cwd = os.getcwd()

simulation_subfolder = "two_population/convergence_various_L"
cwd = os.getcwd()
simulation_subfolder = os.path.join(cwd, simulation_subfolder)
Ls = [int(10 ** (i / 4)) for i in range(8, 21)]  # regulary space with 4 point between each order of magnitude
D = 0.1
all_distances1 = [[0, 0]]
for L in Ls:
    distance_summary_file = f'two_population/convergence_various_L/L_{L}_D_{D}.dat'
    distances = np.loadtxt(distance_summary_file,ndmin=2)
    for distance in distances:
        all_distances1 = np.append(all_distances1, [[L, distance[0]]], axis=0)




prop_cycle = plt.rcParams['axes.prop_cycle']
colors = prop_cycle.by_key()['color']
dico = {"loci": all_distances1[1:,0].astype("int"), "distance" :all_distances1[1:,1]}
all_dist = pd.DataFrame(data = dico)
all_dist["loci"] = all_dist["loci"].astype('category')

ax = sns.violinplot(x = "loci", y="distance",data = all_dist,scale="width",
                    inner="quartiles", color = colors[0], alpha =.5,
                    linewidth=0.)
mean_dist_by_L = all_dist.groupby("loci").mean()
print(all_dist.groupby('loci')['distance'].quantile(0.05))
print(all_dist.groupby('loci')['distance'].quantile(0.95))
ax.plot(range(len(Ls)),  mean_dist_by_L.values,"_",color = colors[0],markersize=7)
plt.setp(ax.collections, alpha=.4)
plt.axhline(y=1.1,color = colors[0],alpha = 0.5, label = r"$t_{1,2} = 1.1$")


_,value = plt.xticks()
plt.xticks(range(0,14,2),np.array(value)[0:14:2])


plt.legend()
plt.xlabel("Number of SNPs")
plt.ylabel("Mean coalescence time")
fig.savefig("figure/two_pop_constant_size_convergence_speed_L.pdf")


