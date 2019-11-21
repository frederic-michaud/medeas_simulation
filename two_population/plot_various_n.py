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
import matplotlib.lines as mlines
simulation_subfolder = "two_population/convergence_various_n"
main_folder = os.path.dirname(os.path.realpath(__file__))
cwd = os.getcwd()
simulation_subfolder = os.path.join(cwd, simulation_subfolder)
fig, axs = plt.subplots(2, 1)
ax = axs[0]


L =10000
D = 0.05
all_distances1 = [[0, 0]]
ns = np.array([2,4,8,16,32,64,128])
for n in ns:
    distance_summary_file = f'two_population/convergence_various_n/n_{n}_D_{D}.dat'
    distances = np.loadtxt(distance_summary_file,ndmin=2)
    for distance in distances:
        all_distances1 = np.append(all_distances1, [[2*n, distance[0] -1]], axis=0)




prop_cycle = plt.rcParams['axes.prop_cycle']
colors = np.array(prop_cycle.by_key()['color'])
dico = {"n": all_distances1[1:,0].astype("int"), "distance" :all_distances1[1:,1]}
all_dist = pd.DataFrame(data = dico)
all_dist["n"] = all_dist["n"].astype('category')

sns.violinplot(x = "n", y="distance",data = all_dist,scale="width",
                    inner="quartiles", color = colors[0], alpha =.5,
                    linewidth=0., ax = ax)
mean_dist_by_L = all_dist.groupby("n").mean()
ax.plot(range(len(ns)),  mean_dist_by_L.values,"_",color = colors[0],markersize=7)
plt.setp(ax.collections, alpha=.4)
ax.axhline(y=2*D,color = colors[0],alpha = 0.5, label = r"$t_{1,2} = 1.1$")
ax.set_xlabel("")
ax.set_xticks([])
ax.set_xlim((-0.5,6.5))
ax.set_ylabel("D")
plt.subplots_adjust(hspace=0)


ax = axs[1]
ax.axhline(y=0,color = "k", alpha = 0.5)
for n_index, n in enumerate(ns):
    mds_projection = os.path.join(main_folder, f'convergence_various_n/n_{n}_D_{D}/MDS_coordinate.txt')
    projection = np.loadtxt(mds_projection)
    pop = np.array(n*[0] +  n*[1],dtype=int)
    col = colors[pop]
    ax.scatter(np.full(len(projection[:,0]),n_index),-projection[:, 0]*np.sign(projection[0,0]),c = col, s=75, alpha = 0.6,marker="_")
markers_color = [mlines.Line2D([], [], color=marker_color, marker="_", linestyle='None', alpha = 0.6) for marker_color in colors]
ax.legend(markers_color, ["Pop. 1", "Pop. 2"])

ax.set_xticks(range(len(ns)))
ax.set_xticklabels(ns)
ax.set_xlim((-0.5,6.5))
ax.set_xlabel(r"n")
ax.set_ylabel("PC 1")
plt.subplots_adjust(hspace=0.01)
#plt.show()
plt.tight_layout()
fig.savefig("figure/two_pop_constant_size_convergence_speed_n.pdf")


