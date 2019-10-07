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

simulation_subfolder = "convergence_various_Ne"
cwd = os.getcwd()
simulation_subfolder = os.path.join(cwd, simulation_subfolder)
#Ls = [10000]
#Ds = [0.01,0.1,0.5,1]
#Nes = [int(10**(-i/4+4))/10000 for i in range(0, 9)]
Ls = [10002]
Ds = [0.01,0.1,0.5]
Nes = [int(10**(-i/4+4))/10000 for i in range(0, 13)]
Ls = [100002]
Ds = [0.01]
Nes = [int(10**(-i/4+4))/10000 for i in range(0, 13)]
for L in Ls:
    for D in Ds:
        all_between = []
        all_within = []
        for Ne in Nes:
            distance_summary_file = os.path.join(simulation_subfolder, f'L_{L}_D_{D}_Ne_{Ne}.dat')
            t_betweens = np.loadtxt(distance_summary_file)
            for t_between in t_betweens:
                all_between.append([L, D, Ne, t_between[0]])
            distance_summary_file = os.path.join(simulation_subfolder, f'L_{L}_D_{D}_Ne_{Ne}_coal.dat')
            t_withins = np.loadtxt(distance_summary_file)
            for t_within in t_withins:
                all_within.append([L, D, Ne, t_within])

        all_between = np.array(all_between)
        all_within = np.array(all_within)

        dico = {"nb_loci": all_between[:,0].astype("int"),
                "split_time" :all_between[:,1],
                "Ne": all_between[:,2],
                "coalescence_time_between": all_between[:,3],
                }
        all_between = pd.DataFrame(data = dico)
        all_between["nb_loci"] = all_between["nb_loci"].astype('category')


        prop_cycle = plt.rcParams['axes.prop_cycle']
        colors = prop_cycle.by_key()['color']
        plt.figure(figsize=(10,7))
        ax = sns.violinplot(x = "Ne", y="coalescence_time_between",data = all_between,scale="width",
                            inner="quartiles", color = colors[0], alpha =.5,
                            linewidth=0.)
        mean_dist_by_N = all_between.groupby("Ne").mean()
        print(mean_dist_by_N)
        ax.plot(range(len(mean_dist_by_N)),  mean_dist_by_N.values[:,1],"_",color = colors[0],markersize=7)
        plt.setp(ax.collections, alpha=.4)
        plt.axhline(y=1+2*D,color = colors[0],alpha = 0.5, label = r"$t_{1,2} expected$")
        plt.savefig("estimate_dist.pdf")



        dico = {"nb_loci": all_within[:,0].astype("int"),
                "split_time" :all_within[:,1],
                "Ne": all_within[:,2],
                "coalescence_time_within": all_within[:,3],
                }
        all_within = pd.DataFrame(data = dico)
        all_within["nb_loci"] = all_within["nb_loci"].astype('category')
        plt.figure(figsize=(10,7))

        ax = sns.violinplot(x = "Ne", y="coalescence_time_within",data = all_within,scale="width",
                            inner="quartiles", color = colors[0], alpha =.5,
                            linewidth=0.)
        plt.xlabel("Effective population size of population 2 (in unit of N)")
        plt.ylabel("mean pairwise coalescence time")
        mean_dist_by_N = all_within.groupby("Ne").mean()
        print(mean_dist_by_N)
        ts_expected = [expected_time(Ne,D) for Ne in Nes]
        ax.plot(range(len(mean_dist_by_N)-1,-1,-1), ts_expected,"x", color=colors[2], markersize=7,label = "Expected value")
        ax.plot(range(len(mean_dist_by_N)),  mean_dist_by_N.values[:,0],"_",color = colors[0],markersize=7,label="Simulation")
        plt.legend()
        plt.setp(ax.collections, alpha=.4)
        #plt.axhline(y=1.02,color = colors[0],alpha = 0.5, label = r"$t_{1,2} = 1.02$")
        plt.savefig("estimate_ts.pdf")
