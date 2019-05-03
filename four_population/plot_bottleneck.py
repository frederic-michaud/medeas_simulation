
import matplotlib
#matplotlib.use("cairo")
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import os


cwd = os.getcwd()
def expected_time(n2: float, D: float):
    n_effectif = n2 + np.exp(-2*D/n2)*(1-n2)
    return(n_effectif)

def expected_time_two_change(n1: float, n2: float, D1: float, D2: float):
    n_effectif = n2 + np.exp(-2 * (D1 / n1 + D2 / n2)) * (1 - n1) + np.exp(-2 * D2 / n2) * (n1 - n2)
    return(n_effectif)

Ls = [int(10**(i/4)) for i in range(20,21)] #regulary space with 4 point between each order of magnitude
Ls = [10000] #regulary space with 4 point between each order of magnitude
D1 = 0.3
D2 = 0.1
D3 = 0.1
length_bottleneck = 0.05
size_bottlenecks =[int(10**(-i/4+4))/10000 for i in range(0, 13)]


n = 20
theta = 3
sample_size = 5
current_folder = os.path.dirname(os.path.realpath(__file__))
simulation_subfolder = "bottleneck"
if not os.path.exists(simulation_subfolder):
    os.mkdir(simulation_subfolder)
for L in Ls:
    all_between = []
    all_within = []
    for size_bottleneck in size_bottlenecks:

        between_summary_file = os.path.join(simulation_subfolder,f'L_{L}_size_bottlenecks_{size_bottleneck}.between')
        t_betweens = np.loadtxt(between_summary_file)
        for t_between in t_betweens:
            t_between = np.sort(t_between)
            all_between.append([size_bottleneck, t_between[0], t_between[1], t_between[2]])

        within_summary_file = os.path.join(simulation_subfolder,f'L_{L}_size_bottlenecks_{size_bottleneck}.within')
        t_withins = np.loadtxt(within_summary_file)
        for t_within in t_withins:
            all_within.append([size_bottleneck, t_within[0], t_within[1], t_within[2]])

    all_between = np.array(all_between)
    all_within = np.array(all_within)

    dico = {"size_bottleneck": all_between[:,0],
            "coalescence_time_between_34": all_between[:,1],
            "coalescence_time_between_12": all_between[:, 2],
            "coalescence_time_between_14": all_between[:, 3]
            }
    all_between = pd.DataFrame(data = dico)
    all_between["size_bottleneck"] = all_between["size_bottleneck"].astype('category')


    prop_cycle = plt.rcParams['axes.prop_cycle']
    colors = prop_cycle.by_key()['color']
    print(all_between)
    mean_dist_by_N = all_between.groupby("size_bottleneck").mean()
    print(mean_dist_by_N)

    plt.figure(figsize=(10,7))
    ax = sns.violinplot(x = "size_bottleneck", y="coalescence_time_between_14",data = all_between,scale="width",
                        inner="quartiles", color = colors[0], alpha =.5,
                        linewidth=0.)
    ax.plot(range(len(mean_dist_by_N)),  mean_dist_by_N.values[:,2],"_",color = colors[0],markersize=7)
    plt.axhline(y=1+2*D1, linestyle = "--",color = colors[0],alpha = 0.5, label = r"$t_{1,4} expected$",lw= 2)

    ax = sns.violinplot(x = "size_bottleneck", y="coalescence_time_between_12",data = all_between,scale="width",
                        inner="quartiles", color = colors[2], alpha =.5,
                        linewidth=0.)
    ax.plot(range(len(mean_dist_by_N)),  mean_dist_by_N.values[:,1],"_",color = colors[2],markersize=7)
    plt.axhline(y=1+2*D2, linestyle = "--", color = colors[2],alpha = 0.5, label = r"$t_{1,2} expected$",lw= 2)

    ax = sns.violinplot(x = "size_bottleneck", y="coalescence_time_between_34",data = all_between,scale="width",
                        inner="quartiles", color = colors[3], alpha =.5,
                        linewidth=0.)
    ax.plot(range(len(mean_dist_by_N)),  mean_dist_by_N.values[:,0],"_",color = colors[3],markersize=7)
    print(np.sort(size_bottlenecks))
    ts_expected = 2*D2 + np.array([expected_time_two_change(size_bottleneck, 1,length_bottleneck , 0.15) for size_bottleneck in np.sort(size_bottlenecks)])
    ax.plot(np.array(range(len(size_bottlenecks))),ts_expected,"--",color = colors[3],alpha = 0.5, label = r"$t_{3,4} expected$",lw= 2)
    #plt.axhline(y=2*(D1-length_bottleneck), linestyle="--", color=colors[2], alpha=0.5, label=r"$t_{1,2} expected$", lw=2)
    plt.setp(ax.collections, alpha=.4)
    plt.legend()

    plt.show()



    dico = {"size_bottleneck": all_within[:,0],
            "coalescence_time_within_2": all_within[:,1],
            "coalescence_time_within_3": all_within[:, 2],
            "coalescence_time_within_4": all_within[:, 3]
            }
    all_within = pd.DataFrame(data = dico)
    all_within["size_bottleneck"] = all_within["size_bottleneck"].astype('category')
    mean_dist_by_N = all_within.groupby("size_bottleneck").mean()
    plt.figure(figsize=(10,7))
    ax = sns.violinplot(x = "size_bottleneck", y="coalescence_time_within_2",data = all_within,scale="width",
                        inner="quartiles", color = colors[0], alpha =.5,
                        linewidth=0.)
    ax.plot(range(len(mean_dist_by_N)),  mean_dist_by_N.values[:,0],"_",color = colors[0],markersize=7)
    plt.axhline(y=1, linestyle = "--",color = colors[0],alpha = 0.5, label = r"$t_{2,2} expected$",lw= 2)

    ax = sns.violinplot(x = "size_bottleneck", y="coalescence_time_within_3",data = all_within,scale="width",
                        inner="quartiles", color = colors[2], alpha =.5,
                        linewidth=0.)
    ax.plot(range(len(mean_dist_by_N)),  mean_dist_by_N.values[:,1],"_",color = colors[2],markersize=7)

    ax = sns.violinplot(x = "size_bottleneck", y="coalescence_time_within_4",data = all_within,scale="width",
                        inner="quartiles", color = colors[3], alpha =.5,
                        linewidth=0.)
    ax.plot(range(len(mean_dist_by_N)),  mean_dist_by_N.values[:,2],"_",color = colors[3],markersize=7)
    print(np.sort(size_bottlenecks))
    ts_expected = np.array([expected_time_two_change(size_bottleneck, 1,length_bottleneck , (D1 - length_bottleneck)) for size_bottleneck in np.sort(size_bottlenecks)])
    ax.plot(np.array(range(len(size_bottlenecks))),ts_expected,"--",color = colors[3],alpha = 0.5, label = r"$t_{3,4} expected$",lw= 2)
    plt.setp(ax.collections, alpha=.4)
    plt.legend()

    plt.show()
