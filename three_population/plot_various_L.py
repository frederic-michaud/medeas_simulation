import numpy as np
import matplotlib
#matplotlib.use("cairo")
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import os


from matplotlib.backends.backend_pdf import PdfPages
cwd = os.getcwd()

simulation_subfolder = "convergence_various_L"
cwd = os.getcwd()
simulation_subfolder = os.path.join(cwd, simulation_subfolder)
Ls = [int(10 ** (i / 4)) for i in range(8, 21)]  # regulary space with 4 point between each order of magnitude
all_distances = np.zeros((3,0))
for L in Ls:
    distance_summary_file = f'convergence_various_L/L_{L}.dat'
    distances = np.loadtxt(distance_summary_file)
    all_distances = np.column_stack((all_distances,np.row_stack((np.full(len(distances[:,0]),L),distances[:,0]/2,distances[:,1]/2))))
nbL = len(Ls)

prop_cycle = plt.rcParams['axes.prop_cycle']
colors = prop_cycle.by_key()['color']
dico = {"loci": all_distances[0,:].astype("int"), "distance1" :all_distances[1,:], "distance2" :all_distances[2,:]}

all_dist = pd.DataFrame(data = dico)
all_dist["loci"] = all_dist["loci"].astype('category')

ax = sns.violinplot(x = "loci", y="distance1",data = all_dist,scale="width",
                    inner="quartiles", color = colors[2], alpha =.5,
                    linewidth=0.)
mean_dist_by_L = all_dist.groupby("loci").mean()

plt.setp(ax.collections, alpha=.4)
plt.axhline(y=0.2,color = colors[2],alpha = 0.5, label = r"$D_{2,3} = 0.2$")

all_dist = pd.DataFrame(data = dico)
all_dist["loci"] = all_dist["loci"].astype('category')
ax = sns.violinplot(x = "loci", y="distance2",data = all_dist,scale="width",
                    inner=None, color = colors[0], alpha =.5,
                    linewidth=0)
mean_dist_by_L = all_dist.groupby("loci").mean()
print(mean_dist_by_L)
ax.plot(range(nbL),  mean_dist_by_L.values[:,0],"_",color = colors[2],markersize=7)
ax.plot(range(nbL),  mean_dist_by_L.values[:,1],"_",color = colors[0],markersize=7)
plt.setp(ax.collections, alpha=.4)
plt.axhline(y=0.1,color = colors[0],alpha = 0.5, label = r"$D_{1,2} = 0.1$")
_,value = plt.xticks()
#plt.xticks(range(0,nbL,4),np.array(value)[0:nbL:4])
aa = ["100","1'000","10'000", "100'000"]
plt.xticks(range(0,nbL,4),aa)


plt.legend()
plt.xlabel("Number of SNPs")
plt.ylabel("Divergence time")
plt.savefig("three_pop_various_L.pdf")

