import numpy as np
import matplotlib
#matplotlib.use("cairo")
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import os


cwd = os.getcwd()
def expected_time(n2: float, D: float):
    n_effectif = n2 + np.exp(-2*D/n2)*(1-n2)
    return(n_effectif)

def expected_time_two_change(n1: float, n2: float, D1: float, D2: float):
    n_effectif = n2 + np.exp(-2*(D1/n1+D2/n2))*(1-n1+ np.exp(2*D1/n1)*(n1-n2))
    return(n_effectif)

simulation_subfolder = "convergence_various_Ne"
cwd = os.getcwd()
simulation_subfolder = os.path.join(cwd, simulation_subfolder)
Ls = [100000] #regulary space with 4 point between each order of magnitude
D1 = 0.05
D2 = 0.2
n1 = 20
n2 = 20
n3 = 20
Ne_small1 = 0.5
Ne_small2s = [int(10**(-i/4+4))/10000 for i in range(1, 13)]

#### test for debugging
Ls = [200001] #regulary space with 4 point between each order of magnitude
D1 = 0.05
D2 = 0.2
n1 = 20
n2 = 20
n3 = 20
Ne_small1 = 0.001
Ne_small2s = [0.001]
### end test debugging

for L in Ls:
    all_between = []
    all_within = []
    for Ne_small2 in Ne_small2s:
        between_summary_file = os.path.join(simulation_subfolder,f'L_{L}_Ne_{Ne_small2}.between')

        t_betweens = np.loadtxt(between_summary_file)
        for t_between in t_betweens:
            all_between.append([L, D1, D2, Ne_small1, Ne_small2, t_between[0],  t_between[1]])

        within_summary_file = os.path.join(simulation_subfolder, f'L_{L}_Ne_{Ne_small2}.within')
        t_withins = np.loadtxt(within_summary_file)
        for t_within in t_withins:
            all_within.append([L, D1, D2, Ne_small1, Ne_small2, t_within[0],  t_within[1]])

    all_between = np.array(all_between)
    all_within = np.array(all_within)

    dico = {"nb_loci": all_between[:,0].astype("int"),
            "split_time_1" :all_between[:,1],
            "split_time_2": all_between[:, 2],
            "Ne1": all_between[:,3],
            "Ne2": all_between[:, 4],
            "coalescence_time_between_12": all_between[:,5],
            "coalescence_time_between_13": all_between[:, 6],
            }
    all_between = pd.DataFrame(data = dico)
    all_between["nb_loci"] = all_between["nb_loci"].astype('category')


    prop_cycle = plt.rcParams['axes.prop_cycle']
    colors = prop_cycle.by_key()['color']
    plt.figure(figsize=(10,7))
    ax = sns.violinplot(x = "Ne2", y="coalescence_time_between_12",data = all_between,scale="width",
                        inner="quartiles", color = colors[0], alpha =.5,
                        linewidth=0.)
    mean_dist_by_N = all_between.groupby("Ne2").mean()
    print(mean_dist_by_N)
    ax.plot(range(len(mean_dist_by_N)),  mean_dist_by_N.values[:,3],"_",color = colors[0],markersize=7)
    plt.setp(ax.collections, alpha=.4)
    plt.axhline(y=1+2*D2,color = colors[0],alpha = 0.5, label = r"$t_{1,2} expected$")
    plt.legend()
    #plt.savefig("estimate_dist.pdf")
    plt.show()

    plt.figure(figsize=(10,7))
    ax = sns.violinplot(x = "Ne2", y="coalescence_time_between_13",data = all_between,scale="width",
                        inner="quartiles", color = colors[0], alpha =.5,
                        linewidth=0.)
    mean_dist_by_N = all_between.groupby("Ne2").mean()
    print(mean_dist_by_N)
    ax.plot(range(len(mean_dist_by_N)),  mean_dist_by_N.values[:,4],"_",color = colors[0],markersize=7)
    plt.setp(ax.collections, alpha=.4)
    plt.axhline(y=2*D1 + expected_time(Ne_small1, 0.15),color = colors[0],alpha = 0.5, label = r"$t_{1,2} expected$")
    plt.legend()
    #plt.savefig("estimate_dist.pdf")
    plt.show()

    dico = {"nb_loci": all_within[:,0].astype("int"),
            "split_time_1" :all_within[:,1],
            "split_time_2": all_within[:, 2],
            "Ne1": all_within[:,3],
            "Ne2": all_within[:, 4],
            "coalescence_time_within_1": all_within[:,5],
            "coalescence_time_within_2": all_within[:, 6],
            }
    all_within = pd.DataFrame(data = dico)
    all_within["nb_loci"] = all_within["nb_loci"].astype('category')
    plt.figure(figsize=(10,7))

    ax = sns.violinplot(x = "Ne2", y="coalescence_time_within_1",data = all_within,scale="width",
                        inner="quartiles", color = colors[0], alpha =.5,
                        linewidth=0.)
    plt.xlabel("Effective population size of population 2 (in unit of N)")
    plt.ylabel("mean pairwise coalescence time")
    mean_dist_by_N = all_within.groupby("Ne2").mean()
    print(mean_dist_by_N)

    ts_expected = [expected_time(Ne_small1,D2) for _ in Ne_small2s]
    ax.plot(range(len(mean_dist_by_N)-1,-1,-1), ts_expected,"x", color=colors[2], markersize=7,label = "Expected value")
    ax.plot(range(len(mean_dist_by_N)),  mean_dist_by_N.values[:,3],"_",color = colors[0],markersize=7,label="Simulation")
    plt.legend()
    plt.setp(ax.collections, alpha=.4)
    plt.show()


    #plt.savefig("estimate_ts.pdf")
    plt.figure(figsize=(10,7))

    ax = sns.violinplot(x = "Ne2", y="coalescence_time_within_2",data = all_within,scale="width",
                        inner="quartiles", color = colors[0], alpha =.5,
                        linewidth=0.)
    plt.xlabel("Effective population size of population 2 (in unit of N)")
    plt.ylabel("mean pairwise coalescence time")
    mean_dist_by_N = all_within.groupby("Ne2").mean()
    print(mean_dist_by_N)
    ts_expected = [expected_time_two_change(Ne_small1, Ne_small2, D2-D1, D1) for Ne_small2 in Ne_small2s]
    ax.plot(range(len(mean_dist_by_N)-1,-1,-1), ts_expected,"x", color=colors[2], markersize=7,label = "Expected value")
    ax.plot(range(len(mean_dist_by_N)),  mean_dist_by_N.values[:,4],"_",color = colors[0],markersize=7,label="Simulation")
    plt.legend()
    plt.setp(ax.collections, alpha=.4)
    plt.show()
