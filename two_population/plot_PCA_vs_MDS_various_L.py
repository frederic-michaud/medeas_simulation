import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
import pickle
import seaborn as sns

cwd = os.getcwd()
print(cwd)
prop_cycle = plt.rcParams['axes.prop_cycle']
colors = prop_cycle.by_key()['color']

simulation_subfolder = "convergence_various_L_compare_D"
cwd = os.getcwd()
simulation_subfolder = os.path.join(cwd,simulation_subfolder)
Ls = [int(10**(i/4)) for i in range(8, 21)] #regulary space with 4 point between each order of magnitude
allTime = []
for L in Ls:
    D = 0.1
    eigensystemFile = os.path.join(simulation_subfolder,f'L_{L}_D_{D}.dat')
    with open(eigensystemFile,"rb") as f:
        lambdas_all  = pickle.load(f)
    for(lambdasp1,lambdasp2) in lambdas_all:
        lambdasp2 = -np.sort(-lambdasp2)
        lambdasp1 = -np.sort(-lambdasp1)
        n = 40
        T = (n-2)/np.sum(lambdasp2[1:])
        D_pca = 2/n*(lambdasp2[0]*T-1)
        D_mds = np.sqrt(1+2/40*(((n-2)*lambdasp1[0])/np.sum(lambdasp1[1:])-1))-1
        allTime.append((L, D_mds,D_pca))


allTime = np.array(allTime)
dico = {"loci": allTime[:,0], "distance_mds" :allTime[:,1], "distance_pca" :allTime[:,2]}
all_dist = pd.DataFrame(data = dico)
all_dist["loci"] = all_dist["loci"].astype("int").astype('category')
mean_dist_by_L = all_dist.groupby("loci").mean()

fig = plt.figure()
ax1 = fig.add_subplot(111)
sns.violinplot(x = "loci", y="distance_mds",data = all_dist,scale="width",
                    inner="quartiles", color = colors[0], alpha =.5,
                    linewidth=0., ax = ax1)
ax1.plot(range(13),  mean_dist_by_L.values[:,0],"_",color = colors[0],markersize=7, label = "MDS")


sns.violinplot(x = "loci", y="distance_pca",data = all_dist,scale="width",
                    inner="quartiles", color = colors[2], alpha =.5,
                    linewidth=0., ax = ax1)

ax1.plot(range(13),  mean_dist_by_L.values[:,1],"_",color = colors[2],markersize=7,label = "PCA")

plt.axhline(y=0.2,color = colors[3],alpha = 0.5,label = "Simulated value")
plt.setp(ax1.collections, alpha=.5)
ax1.set_xlabel("# SNPs")
ax1.set_ylabel("# Estimated split time")
ax1.legend()
_,value = plt.xticks()
plt.xticks(range(0,12,2),np.array(value)[0:12:2])
plt.savefig("compare_pca_mds.pdf")