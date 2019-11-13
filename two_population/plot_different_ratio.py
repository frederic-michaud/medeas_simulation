import numpy as np
import matplotlib
#matplotlib.use("cairo")
import matplotlib.lines as mlines
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import os


cwd = os.getcwd()
D = 0.05
fig, axs = plt.subplots(2, 1)

all_distances1 = [[0, 0]]
n1s = np.linspace(2,20,19,dtype=int)
main_folder = os.path.dirname(os.path.realpath(__file__))

for n1 in n1s:
    distance_summary_file = os.path.join(main_folder, f'convergence_various_sample_ratio/n1_{n1}_D_{D}.dat')
    distances = np.loadtxt(distance_summary_file)
    for distance in distances:
        all_distances1 = np.append(all_distances1, [[n1, distance[0]-1]], axis=0)


prop_cycle = plt.rcParams['axes.prop_cycle']
colors = np.array(prop_cycle.by_key()['color'])
dico = {"n1": all_distances1[1:,0].astype("int"), "distance" :all_distances1[1:,1]}
all_dist = pd.DataFrame(data = dico)
all_dist["n1"] = all_dist["n1"].astype('category')

sns.violinplot(x = "n1", y="distance",data = all_dist,scale="width",
                    inner="quartiles", color = colors[0], alpha =.5,
                    linewidth=0., ax=axs[0])
ax = axs[0]
mean_dist_by_L = all_dist.groupby("n1").mean()
ax.plot(range(len(n1s)),  mean_dist_by_L.values,"_",color = colors[0],markersize=7)
plt.setp(ax.collections, alpha=.4)
ax.axhline(y=0.1,color = colors[0],alpha = 0.5, label = r"$D = 0.1$")
#ax.set_xticks(np.linspace(-2,18,11,dtype=int))
#ax.set_xticklabels([ a+"%" for a in np.linspace(0,50,11,dtype=int).astype(str)])
ax.set_xticks([])

ax.set_ylim((0,0.2))
ax.legend()
#ax.set_xlabel(r"$\frac{n_1}{n_1 + n_2}$")
plt.subplots_adjust(hspace=0)
ax.set_xlabel("")
ax.set_ylabel("Split time")


# ax = axs[1]
# ax.axvline(x=0,color = "k", alpha = 0.5)
# for n1 in n1s[::2]:
#     mds_projection =os.path.join(main_folder, f'convergence_various_sample_ratio/n1_{n1}_D_{D}/MDS_coordinate.txt')
#     projection = np.loadtxt(mds_projection)
#     pop = np.array(n1*[0] +  (40-n1)*[1])
#     col = colors[pop]
#     ax.scatter(-projection[:, 0]*np.sign(projection[0,0]),np.full(len(projection[:,0]), n1-2),c = col, s=75, alpha = 0.6)
# markers_color = [mlines.Line2D([], [], color=marker_color, marker="o", linestyle='None', alpha = 0.6) for marker_color in colors]
# ax.legend(markers_color, ["Pop. 1", "Pop. 2"])
# ax.set_yticks(np.linspace(-2,18,6,dtype=int))
# ax.set_yticklabels([ a+"%" for a in np.linspace(0,50,6,dtype=int).astype(str)])
# ax.set_ylabel(r"$\frac{n_1}{n_1 + n_2}$")
# ax.set_xlabel(r"PC 1")


ax = axs[1]
ax.axhline(y=0,color = "k", alpha = 0.5)
for n1 in n1s:
    mds_projection = os.path.join(main_folder, f'convergence_various_sample_ratio/n1_{n1}_D_{D}/MDS_coordinate.txt')
    projection = np.loadtxt(mds_projection)
    pop = np.array(n1*[0] +  (40-n1)*[1])
    col = colors[pop]
    ax.scatter(np.full(len(projection[:,0]), n1-2),-projection[:, 0]*np.sign(projection[0,0]),c = col, s=75, alpha = 0.6)
markers_color = [mlines.Line2D([], [], color=marker_color, marker="o", linestyle='None', alpha = 0.6) for marker_color in colors]
ax.legend(markers_color, ["Pop. 1", "Pop. 2"])
ax.set_xticks(np.linspace(-2,18,11,dtype=int))
ax.set_xticklabels([ a+"%" for a in np.linspace(0,50,11,dtype=int).astype(str)])
ax.set_xlabel(r"$\frac{n_1}{n_1 + n_2}$")
ax.set_ylim((-0.175,0.175))

ax.set_ylabel(r"PC 1")

#plt.show()
plt.subplots_adjust(hspace=0.01)
plt.savefig("figure/two_pop_different_ratio.pdf")