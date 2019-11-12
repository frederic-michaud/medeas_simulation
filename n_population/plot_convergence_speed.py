import numpy as np
import matplotlib
#matplotlib.use("cairo")
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import os
import matplotlib.ticker as ticker

plt.rcParams.update({'font.size': 14})


Ls = [int(10**(i/4)) for i in range(12,21)] #regulary space with 4 point between each order of magnitude
Ks = [6]
n_individual_per_pop = 20
theta = 2
D = 0.1
current_folder = os.path.dirname(os.path.realpath(__file__))



all_between = []
all_within = []
for L in Ls:
    distance_summary_file = f'convergence_speed/L_{L}.dat'
    t_betweens = np.loadtxt(os.path.join(current_folder,distance_summary_file))
    for t_between in t_betweens:
        print(t_between)
        all_between.append([L, t_between[0],  t_between[1], t_between[2], t_between[3], t_between[4]])

all_between = np.array(all_between)

dico = {
        "L": all_between[:, 0],
        "coalescence_time_between_16": all_between[:, 1] - 1,
        "coalescence_time_between_15": all_between[:, 2] - 1,
        "coalescence_time_between_14": all_between[:, 3] - 1,
        "coalescence_time_between_13": all_between[:, 4] - 1,
        "coalescence_time_between_12": all_between[:, 5] - 1,
        }
all_coal_time = pd.DataFrame(data = dico)
all_coal_time["L"] = all_coal_time["L"].astype('category')


prop_cycle = plt.rcParams['axes.prop_cycle']
colors = prop_cycle.by_key()['color']

mean_dist_by_N = all_coal_time.groupby("L").mean()
print(mean_dist_by_N)

fig = plt.figure()


ax = sns.violinplot(x = "L", y="coalescence_time_between_12",data = all_coal_time,scale="width",
                    inner="quartiles", color = colors[0], alpha =.5,
                    linewidth=0.)
ax.plot(range(len(mean_dist_by_N)),  mean_dist_by_N.values[:,4],"_",color = colors[0],markersize=7, label = "$D_{1}$ Inferred")


ax = sns.violinplot(x = "L", y="coalescence_time_between_13",data = all_coal_time,scale="width",
                    inner="quartiles", color = colors[1], alpha =.5,
                    linewidth=0.)
ax.plot(range(len(mean_dist_by_N)),  mean_dist_by_N.values[:,3],"_",color = colors[1],markersize=7, label = "$D_{2}$ Inferred")


ax = sns.violinplot(x = "L", y="coalescence_time_between_14",data = all_coal_time,scale="width",
                    inner="quartiles", color = colors[2], alpha =.5,
                    linewidth=0.)
ax.plot(range(len(mean_dist_by_N)),  mean_dist_by_N.values[:,2],"_",color = colors[2],markersize=7, label = "$D_{3}$ Inferred")


ax = sns.violinplot(x = "L", y="coalescence_time_between_15",data = all_coal_time,scale="width",
                    inner="quartiles", color = colors[3], alpha =.5,
                    linewidth=0.)
ax.plot(range(len(mean_dist_by_N)),  mean_dist_by_N.values[:,1],"_",color = colors[3],markersize=7, label = "$D_{4}$ Inferred")


ax = sns.violinplot(x = "L", y="coalescence_time_between_16",data = all_coal_time,scale="width",
                    inner="quartiles", color = colors[4], alpha =.5,
                    linewidth=0.)
ax.plot(range(len(mean_dist_by_N)),  mean_dist_by_N.values[:,0],"_",color = colors[4],markersize=7, label = "$D_{5}$ Inferred")



plt.axhline(y=D,linestyle = "--", lw = 2,color = colors[0],alpha = 0.5, label = r"Expected")
plt.axhline(y=2*D,linestyle = "--", lw = 2,color = colors[1],alpha = 0.5, label = r"Expected")
plt.axhline(y=3*D,linestyle = "--", lw = 2,color = colors[2],alpha = 0.5, label = r"Expected")
plt.axhline(y=4*D,linestyle = "--", lw = 2,color = colors[3],alpha = 0.5, label = r"Expected")
plt.axhline(y=5*D,linestyle = "--", lw = 2,color = colors[4],alpha = 0.5, label = r"Expected")




plt.setp(ax.collections, alpha=.4)
plt.legend(ncol  = 2)
plt.ylim((0,1))
plt.xlabel(r"$L$")
plt.ylabel("Split time")
plt.xticks(range(len(Ls))[::2],["1,000", "3,163", "10,000", "31,622","100,000"])

fig.savefig("figure/n_pop.pdf")

fig = plt.figure()
