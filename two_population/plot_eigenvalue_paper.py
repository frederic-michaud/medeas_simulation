import numpy as np
import matplotlib.pyplot as plt
import os
import pickle

plt.rcParams.update({'font.size': 14})
prop_cycle = plt.rcParams['axes.prop_cycle']
colors = np.array(prop_cycle.by_key()['color'])
main_folder = os.path.dirname(os.path.realpath(__file__))
simulation_subfolder = "convergence_various_L"
D = 0.1
L = 10000
simulation_subsub_folder = os.path.join(main_folder, simulation_subfolder,f"L_{L}_D_{D}")
val,vec = pickle.load(open(os.path.join(simulation_subsub_folder,"MDS_eigensystem","p1.vecs.data"),"rb"))
fig = plt.figure()
Ts = np.loadtxt(open(os.path.join(simulation_subsub_folder, "all_T.txt")))
plt.plot(-np.sort(-val),"o",alpha = 0.5, label = "Simulated values")
T = Ts[0]
plt.plot(range(1,39), 38*[2/T**2], "x", color=colors[2], label = "Analytical prediction")
plt.plot(39, 0, "x", color=colors[2])
D = 2*D
largest_eg = 2/(T**2)*(1+40/2*D*(D+2))
plt.plot(0,largest_eg, "x", color=colors[2])
plt.legend()
plt.xlabel("Eigenvalue index")
plt.ylabel("Eigenvalue")
fig.savefig("figure/two_pop_constant_size_eigenvalue.pdf")
