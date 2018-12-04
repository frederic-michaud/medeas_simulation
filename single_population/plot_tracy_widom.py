import numpy as np
import pickle
import matplotlib.pyplot as plt
import os
import scipy.stats
import scipy.stats
import scipy.special
simulation_subfolder1 = "single_population"
simulation_subfolder2 = "tracy_widom"
current_folder = os.getcwd()
home_folder = os.path.split(current_folder)[0]
simulation_subfolder = os.path.join(home_folder,simulation_subfolder1,simulation_subfolder2)
L = 5000
n = 100

fig = plt.figure()
ax = fig.add_subplot(111)
ax.set_xlabel("Renormalized largest eigenvalue")
ax.set_ylabel(r"Probability density function")

ax = fig.add_subplot(111)

input_files = open(os.path.join(simulation_subfolder,f'L_{L}n_{n}/tracy_widom.dat'),"r")
tws = []
for line in input_files:
    tw = line.split(" ")[4]
    tws.append(float(tw))
tws = np.array(tws)
ax.hist(tws,20,normed=1,label = "Simulated value")
tw_distrib = np.loadtxt(os.path.join(home_folder,simulation_subfolder1, "tracy_widom_pdf.dat"))
ax.plot(tw_distrib[:, 0], tw_distrib[:, 1], label = "theoretical value")
plt.legend()
plt.savefig(os.path.join(home_folder, simulation_subfolder1, "tracy_widom_example_cumulative.pdf"))
