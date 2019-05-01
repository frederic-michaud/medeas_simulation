import numpy as np
import matplotlib.pyplot as plt
import os
import pickle

plt.rcParams.update({'font.size': 14})
prop_cycle = plt.rcParams['axes.prop_cycle']
colors = np.array(prop_cycle.by_key()['color'])
simulation_subfolder = "convergence_various_L"
D = 0.05
L = 10000
simulation_subsub_folder = os.path.join(simulation_subfolder,f"L_{L}_D_{D}")

fig = plt.figure()


val,vec = pickle.load(open(os.path.join(simulation_subsub_folder,"MDS_eigensystem","p1.vecs.data"),"rb"))
pointColor = colors[np.concatenate((np.full(20,0,dtype=int),np.full(20,2,dtype=int)))]
order = np.argsort(-val)
populations_sizes = [20,20]
threshold = 0
for population_size in populations_sizes:
    population_span = range(threshold,threshold+population_size)
    plt.scatter(np.sqrt(val[order[0]])*vec[population_span,order[0]],np.sqrt(val[order[1]])*vec[population_span,order[1]],c = pointColor[population_span],alpha=0.5)
    threshold = threshold + population_size
plt.legend(["Pop. 1","Pop. 2"],loc = 1)
plt.xlabel("Dimension 1")
plt.ylabel("Dimension 2")
plt.show()
fig.savefig("two_pop_constant_size_mds.pdf")

fig = plt.figure()
Ts = np.loadtxt(open(os.path.join(simulation_subsub_folder, "all_extrapolated_T.txt")))
plt.plot(-np.sort(-val),"o",alpha = 0.5, label = "Simulated values")
T = Ts[0]
plt.plot(range(1,39), 38*[2/T**2], "x", color=colors[2], label = "Analytical prediction")
plt.plot(39, 0, "x", color=colors[2])
D = 2*D
largest_eg = 2/(T**2)*(1+40/2*D*(D+2))
print(largest_eg)
plt.plot(0,largest_eg, "x", color=colors[2])
plt.legend()
plt.show()
fig.savefig("two_pop_constant_size_eigenvalue.pdf")