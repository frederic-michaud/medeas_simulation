import numpy as np
import matplotlib
#matplotlib.use("cairo")
import matplotlib.lines as mlines
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import os
fig = plt.figure()
cwd = os.getcwd()
prop_cycle = plt.rcParams['axes.prop_cycle']
colors = np.array(prop_cycle.by_key()['color'])


fig, axs = plt.subplots(2, 1)
ax = axs[0]

main_folder = os.path.dirname(os.path.realpath(__file__))
simulation_subfolder = os.path.join(main_folder, "convergence_various_L")
cwd = os.getcwd()
simulation_subfolder = os.path.join(cwd, simulation_subfolder)
Ls = [int(10 ** (i / 4)) for i in range(8, 21)]  # regulary space with 4 point between each order of magnitude
D = 0.05
all_distances1 = [[0, 0]]
for L in Ls:
    distance_summary_file = f'two_population/convergence_various_L/L_{L}_D_{D}.dat'
    distances = np.loadtxt(distance_summary_file,ndmin=2)
    for distance in distances:
        all_distances1 = np.append(all_distances1, [[L, distance[0]-1]], axis=0)




prop_cycle = plt.rcParams['axes.prop_cycle']
dico = {"loci": all_distances1[1:,0].astype("int"), "distance" :all_distances1[1:,1]}
all_dist = pd.DataFrame(data = dico)
all_dist["loci"] = all_dist["loci"].astype('category')

sns.violinplot(x = "loci", y="distance",data = all_dist,scale="width",
                    inner="quartiles", color = colors[0], alpha =.5,
                    linewidth=0., ax = ax)
mean_dist_by_L = all_dist.groupby("loci").mean()

ax.plot(range(len(Ls)),  mean_dist_by_L.values,"_",color = colors[0],markersize=7)
plt.setp(ax.collections, alpha=.4)
ax.axhline(y=2*D,color = colors[0],alpha = 0.5, label = r"$t_{1,2} = 1.1$")
ax.set_ylabel("Split time")
ax.set_xlabel(r"")
_,value = plt.xticks()
ax.set_xticks([])
ax.set_ylim((0, 0.4))
plt.subplots_adjust(hspace=0)
ax.set_xlim((-1,13))

ax = axs[1]
ax.axhline(y=0,color = "k", alpha = 0.5)
for L_index, L in enumerate(Ls):
    mds_projection = os.path.join(main_folder, f'convergence_various_L/L_{L}_D_{D}/MDS_coordinate.txt')
    projection = np.loadtxt(mds_projection)
    pop = np.array(20*[0] +  20*[1],dtype=int)
    col = colors[pop]
    ax.scatter(np.full(len(projection[:,0]),L_index),-projection[:, 0]*np.sign(projection[0,0]),c = col, s=75, alpha = 0.6,marker="_")
markers_color = [mlines.Line2D([], [], color=marker_color, marker="_", linestyle='None', alpha = 0.6) for marker_color in colors]
ax.legend(markers_color, ["Pop. 1", "Pop. 2"])

ax.set_xticks(range(0, 14, 2))
ax.set_xticklabels(Ls[::2])
ax.set_xlim((-1,13))
ax.set_xlabel(r"Number of SNPs")
ax.set_ylim((-0.175,0.175))


ax.set_ylabel("PC 1")
plt.subplots_adjust(hspace=0.01)
fig.savefig("figure/two_pop_constant_size_convergence_speed_L.pdf")


