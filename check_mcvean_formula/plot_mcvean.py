import matplotlib.pyplot as plt
import pickle
import numpy as np
from matplotlib import rc


with open("final_result.dat","rb") as f:
    (ns,all_mean_distance,all_std_distance,all_expected_distance) = pickle.load(f)
ns = np.array(ns)
fake_value = np.arange(0,len(ns))
plt.plot(ns, all_mean_distance,marker = ".", label='Simulated value')
plt.plot(ns, all_expected_distance,marker = ".", label="Approximated value")
plt.xscale("log")
plt.xlabel("$n$")
plt.ylabel(r"$\delta_{i,j}$")
plt.legend()
plt.xticks([4,6,8,10,20,40,60,80,100],[4,6,8,10,20,40,60,80,100])
plt.savefig("mcvean_approximation.pdf")
