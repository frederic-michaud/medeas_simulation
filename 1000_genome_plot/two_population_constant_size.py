import numpy as np
import matplotlib.pyplot as plt
import os
import pickle
import matplotlib.ticker as ticker

plt.rcParams.update({'font.size': 14})
prop_cycle = plt.rcParams['axes.prop_cycle']
colors = np.array(prop_cycle.by_key()['color'])
simulation_subfolder = "../../../Desktop/medeas_1000_genome"
pop_name = "pops_JPT_CHB"
simulation_subsub_folder = os.path.join(simulation_subfolder,f"pops_JPT_CHB")

fig = plt.figure()
print(os.getcwd())

val,vec = pickle.load(open(os.path.join(simulation_subsub_folder,"MDS_eigensystem","p1.vecs.data"),"rb"))
order = np.argsort(-val)


with open(os.path.join(simulation_subfolder,f'{pop_name}_haplo.lab'),"rb") as f:
    lines = f.readlines()

labels = [l.split()[0] for l in lines]
labels = np.array(labels)
populations, numerical_labels = np.unique(labels, return_inverse=True)

for index_population, population in enumerate(populations):
    population_span = np.where(population == labels)
    plt.scatter(np.sqrt(val[order[0]])*vec[population_span,order[0]],np.sqrt(val[order[1]])*vec[population_span,order[1]],c = colors[2*index_population],alpha=0.5, label = population)
plt.xlabel("Dimension 1")
plt.ylabel("Dimension 2")
plt.legend(["Han Chinese ","Japanese"])
plt.show()
fig.savefig("JPT_CHB_mds.pdf")

fig = plt.figure()
Ts = np.loadtxt(open(os.path.join(simulation_subsub_folder, "all_extrapolated_T.txt")))
t12 = np.loadtxt(open(os.path.join(simulation_subsub_folder, "all_extrapolated_distances.txt")))
t11,t22 = np.transpose(np.loadtxt(open(os.path.join(simulation_subsub_folder, "all_extrapolated_effective_size.txt"))))
n1 = np.sum(labels == labels[0])
n2 = np.sum(labels == labels[-1])
n = n1 + n2
t22_sorted = np.sort(t22)
print(f"t22 mean: {np.mean(t22)}")
print(f"lower 2: {t22_sorted[2]}")
print(f"upper 3: {t22_sorted[-3]}")
t12_sorted = np.sort(t12)
print(f"t12 mean: {np.mean(t12)}")
print(f"lower 2: {t12_sorted[2]}")
print(f"upper 3: {t12_sorted[-3]}")

extrapolated_distance = t12 - (1+0.99684897)/2
plt.plot(-np.sort(-val),"o",alpha = 0.5, label = "Real values")
T = Ts[0]
plt.plot(range(5,n-5), (n-10)*[2/T**2],"_", color=colors[2], label = "Analytical prediction",markersize = 4,markeredgewidth = 2)
plt.plot(n-1, 0, "_", color=colors[2],markersize = 12,markeredgewidth = 2)

D = extrapolated_distance

largest_egs = 2/(n*Ts**2)*(n+2*n1*n2*D*(D+2))
largest_eg = largest_egs[0]
largest_egs = largest_egs[largest_egs>0]
largest_egs = np.sort(largest_egs)
print(largest_egs)
large_largest_eg = largest_egs[-3]
small_largest_eg = largest_egs[2]

print(largest_eg)
plt.plot(0,largest_eg, "_", color=colors[2],markersize = 12,markeredgewidth = 2)
plt.errorbar(0,largest_eg , yerr=([largest_eg-large_largest_eg],[small_largest_eg-largest_eg]), c = colors[2],elinewidth = 1,solid_capstyle='projecting', capsize=3)
#plt.plot(0,large_largest_eg, "x", color=colors[1])
#plt.plot(0,small_largest_eg,largest_eg, "x", color=colors[1])
plt.legend()
plt.xlabel("Eigenvalue index")
plt.ylabel("Eigenvalue")

plt.show()

fig.savefig("JPT_CHB_eigenvalue.pdf")