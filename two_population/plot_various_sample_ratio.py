import numpy as np
import matplotlib
#matplotlib.use("cairo")
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import os


from matplotlib.backends.backend_pdf import PdfPages
cwd = os.getcwd()
D = 0.05

all_distances1 = [[0, 0]]
n1s = np.linspace(2,38,37,dtype=int)
for n1 in n1s:
    distance_summary_file = f'convergence_various_sample_ratio/n1_{n1}_D_{D}.dat'
    distances = np.loadtxt(distance_summary_file)
    for distance in distances:
        all_distances1 = np.append(all_distances1, [[n1, distance[0]]], axis=0)


prop_cycle = plt.rcParams['axes.prop_cycle']
colors = prop_cycle.by_key()['color']
dico = {"loci": all_distances1[1:,0].astype("int"), "distance" :all_distances1[1:,1]}
all_dist = pd.DataFrame(data = dico)
all_dist["loci"] = all_dist["loci"].astype('category')

ax = sns.violinplot(x = "loci", y="distance",data = all_dist,scale="width",
                    inner="quartiles", color = colors[0], alpha =.5,
                    linewidth=0.)
mean_dist_by_L = all_dist.groupby("loci").mean()
ax.plot(range(37),  mean_dist_by_L.values,"_",color = colors[0],markersize=7)
plt.setp(ax.collections, alpha=.4)
plt.axhline(y=0.1,color = colors[0],alpha = 0.5, label = "D = 0.1")



plt.legend()
plt.xlabel("Number of SNPs")
plt.ylabel("Divergence time")
plt.savefig("two_pop_different_ratio.pdf")