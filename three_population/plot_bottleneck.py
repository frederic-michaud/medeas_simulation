import numpy as np
import matplotlib
#matplotlib.use("cairo")
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import os
import matplotlib.ticker as ticker

plt.rcParams.update({'font.size': 14})

cwd = os.getcwd()
def expected_time(n2: float, D: float):
    n_effectif = n2 + np.exp(-2*D/n2)*(1-n2)
    return(n_effectif)

def expected_time_two_change(n1: float, n2: float, D1: float, D2: float):
    n_effectif = n2 + np.exp(-2*(D1/n1+D2/n2))*(1-n1+ np.exp(2*D1/n1)*(n1-n2))
    return(n_effectif)

simulation_subfolder = "convergence_bottleneck"
cwd = os.getcwd()
simulation_subfolder = os.path.join(cwd, simulation_subfolder)
Ls = [int(10**(i/4)) for i in range(8,25)] #regulary space with 4 point between each order of magnitude
Ls = [int(10**(i/4)) for i in range(8,21)] #regulary space with 4 point between each order of magnitude
Ls = [10000] #regulary space with 4 point between each order of magnitude
D1 = 0.025
D2 = 0.1
n1 = 15
n2 = 20
n3 = 25
strenght_bottlenecks = [int(10**(-i/4+4))/10000 for i in range(0, 9)]

length_bottleneck = 0.025



for L in Ls:
    all_between = []
    all_within = []
    for strenght_bottleneck in strenght_bottlenecks:
        between_summary_file = os.path.join(simulation_subfolder, f'L_{L}_Ne_{strenght_bottleneck}.between')

        t_betweens = np.loadtxt(between_summary_file)
        for t_between in t_betweens:
            all_between.append([strenght_bottleneck, t_between[0],  t_between[1]])

        within_summary_file = os.path.join(simulation_subfolder,f'L_{L}_Ne_{strenght_bottleneck}.within')
        t_withins = np.loadtxt(within_summary_file)
        for t_within in t_withins:
            all_within.append([strenght_bottleneck, t_within[0],  t_within[1]])

    all_between = np.array(all_between)
    all_within = np.array(all_within)

    dico = {
            "strength_bottleneck": all_between[:, 0],
            "coalescence_time_between_12": all_between[:,1],
            "coalescence_time_between_23": all_between[:, 2],
            "coalescence_time_within_1": all_within[:, 1],
            "coalescence_time_within_2": all_within[:, 2],
            }
    all_coal_time = pd.DataFrame(data = dico)
    all_coal_time["strength_bottleneck"] = all_coal_time["strength_bottleneck"].astype('category')


    prop_cycle = plt.rcParams['axes.prop_cycle']
    colors = prop_cycle.by_key()['color']

    mean_dist_by_N = all_coal_time.groupby("strength_bottleneck").mean()
    print(mean_dist_by_N)

    fig = plt.figure()


    ax = sns.violinplot(x = "strength_bottleneck", y="coalescence_time_between_12",data = all_coal_time,scale="width",
                        inner="quartiles", color = colors[0], alpha =.5,
                        linewidth=0.)
    ax.plot(range(len(mean_dist_by_N)),  mean_dist_by_N.values[:,0],"_",color = colors[0],markersize=7, label = "$t_{1,2}$ Simulated")
    plt.axhline(y=1+2*D2,linestyle = "--", lw = 2,color = colors[0],alpha = 0.5, label = r"$t_{1,2}$ Expected")

    ax = sns.violinplot(x = "strength_bottleneck", y="coalescence_time_between_23",data = all_coal_time,scale="width",
                        inner="quartiles", color = colors[1], alpha =.5,
                        linewidth=0.)
    ax.plot(range(len(mean_dist_by_N)),  mean_dist_by_N.values[:,1],"_",color = colors[1],markersize=7,label = r"$t_{2,3}$ Simulated")

    ts_expected = np.array(
        [2*D1 + expected_time_two_change(size_bottleneck, 1, length_bottleneck, D2 - length_bottleneck) for size_bottleneck in
         np.sort(strenght_bottlenecks)])
    ax.plot(np.array(range(len(strenght_bottlenecks))), ts_expected, "--", color=colors[1], alpha=0.5,
            label=r"$t_{2,3}$ Expected", lw=2)


    ax = sns.violinplot(x = "strength_bottleneck", y="coalescence_time_within_1",data = all_coal_time,scale="width",
                        inner="quartiles", color = colors[2], alpha =.5,
                        linewidth=0.)
    ax.plot(range(len(mean_dist_by_N)),  mean_dist_by_N.values[:,2],"_",color = colors[2],markersize=7, label=r"$t_{2,2}$ Simulated")

    ts_expected = np.array([expected_time_two_change(size_bottleneck, 1, length_bottleneck, D2 - length_bottleneck) for size_bottleneck in np.sort(strenght_bottlenecks)])
    ax.plot(np.array(range(len(strenght_bottlenecks))), ts_expected, "--", color=colors[2], alpha=0.5,label=r"$t_{2,2}$ Expected", lw=2)
    plt.setp(ax.collections, alpha=.4)
    plt.legend()
    plt.xlabel(r"$N_e$ Bottleneck")
    plt.ylabel("Mean coalescent time")
    plt.xticks([0,2,4,6,8],[r"$10^{-2}$",r"$10^{-3/2}$",r"$10^{-1}$",r"$10^{-1/2}$",r"$10^{0}$"])

    plt.show()
    fig.savefig("three_pop_t.pdf")

    fig = plt.figure()
