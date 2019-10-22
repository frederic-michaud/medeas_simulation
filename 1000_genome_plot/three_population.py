import numpy as np
import matplotlib.pyplot as plt
import os
import pickle
import matplotlib.ticker as ticker

plt.rcParams.update({'font.size': 14})
prop_cycle = plt.rcParams['axes.prop_cycle']
colors = np.array(prop_cycle.by_key()['color'])
simulation_subfolder = "../../mds_1000_genome/no_prunning/medeas/triple/JPT_CHB_YRI"
label_subfolder = "../../mds_1000_genome/no_prunning/label/triple"
pop_name = "JPT_CHB_YRI"


fig = plt.figure()
print(os.getcwd())

val,vec = pickle.load(open(os.path.join(simulation_subfolder,"MDS_eigensystem","p1.vecs.data"),"rb"))
order = np.argsort(-val)


with open(os.path.join(label_subfolder,f'{pop_name}_haplo.lab'),"rb") as f:
    lines = f.readlines()

labels = [l.split()[0] for l in lines]
labels = np.array(labels,dtype=str)
populations, numerical_labels = np.unique(labels, return_inverse=True)
print(populations)
for index_population, population in enumerate(populations):
    population_span = np.where(population == labels)
    plt.scatter(np.sqrt(val[order[0]])*vec[population_span,order[0]],np.sqrt(val[order[1]])*vec[population_span,order[1]],c = colors[2*index_population],alpha=0.5, label = population)
plt.xlabel("Dimension 1")
plt.ylabel("Dimension 2")
plt.ylim((-0.01,0.01))
plt.legend(["Han Chinese ","Japanese", "Yoruba"])

fig.savefig("figure/JPT_CHB_YRI_mds.pdf")

fig = plt.figure()



Ts = np.loadtxt(open(os.path.join(simulation_subfolder, "all_extrapolated_T.txt")))
ts_between = np.loadtxt(open(os.path.join(simulation_subfolder, "all_extrapolated_distances.txt")))
ts_within = np.loadtxt(open(os.path.join(simulation_subfolder, "all_extrapolated_effective_size.txt")))
n1 = np.sum(labels == "JPT")
n2 = np.sum(labels == "CHB")
n3 = np.sum(labels == "YRI")

ns = np.array([n1,n2,n3])
n = np.sum(ns)
npop = 3

def make_b(ts: 'np.ndarray[int]') -> 'np.ndarray[float]':
    """Make the B-matrix (see paper for details)."""
    n = np.sum(ns)
    b = np.zeros((npop, npop))
    delta = np.zeros((npop,))
    for i in range(npop):
        delta[i] = (sum(ns[k] * ts[i, k] ** 2 for k in range(npop) if k != i) + ts[i, i] ** 2 * (ns[i] - 1)) / n
    delta_0 = sum(ns[i] * delta[i] for i in range(npop)) / n
    for i in range(npop):
        for j in range(npop):
            if i != j:
                b[i, j] = np.sqrt(ns[i] * ns[j]) * (ts[i, j] ** 2 - delta[i] - delta[j] + delta_0)
            else:
                b[i, j] = (ns[i] - 1) * ts[i, j] ** 2 - ns[i] * (2 * delta[i] - delta_0)
    return b
t11 = ts_within[0,0]
t22 = ts_within[0,1]
t33 = ts_within[0,2]
t12 = ts_between[0,1]
t13 = t23 = ts_between[0,0]
ts = np.array([[t11,t12,t13],[t12,t22,t23],[t13,t23,t33]])
b = make_b(ts)

vals, vecs = np.linalg.eigh(b)


fig, (ax, ax2) = plt.subplots(2, 1, sharex=True, gridspec_kw={'height_ratios': [1, 2]})

extrapolated_distance = t12 - (1+0.99684897)/2
ax.plot(-np.sort(-val),"o",alpha = 0.5, label = "Real values")
ax2.plot(-np.sort(-val),"o",alpha = 0.5)
T = Ts[0]

format_common = dict(color = colors[2], marker = "_")
format_small_analy = format_common.copy()
format_small_analy.update(dict(markersize = 1, markeredgewidth = 1))
format_large_analy = format_common.copy()
format_large_analy.update(dict(markersize = 12, markeredgewidth = 2))
ax.plot(0, -vals[0]*2/T**2,"_", label = "Analytical prediction",**format_large_analy)
ax2.plot(1, -vals[1]*2/T**2,"_", **format_large_analy)
ax2.plot(n-1, 0, "_", **format_large_analy)
all_large_eg = []
def get_95_interval(eigenvalues):
    eigenvalues = eigenvalues[eigenvalues > 0.000000001]
    eigenvalues = np.sort(eigenvalues)
    larg_eg = eigenvalues[-3]
    small_eg = eigenvalues[2]
    return((larg_eg,small_eg))
for bootstrap in range(0,101):
    t11 = ts_within[bootstrap,0]
    t22 = ts_within[bootstrap,1]
    t33 = ts_within[bootstrap,2]
    t12 = ts_between[bootstrap,1]
    t13 = t23 = ts_between[bootstrap,0]
    ts = np.array([[t11,t12,t13],[t12,t22,t23],[t13,t23,t33]])
    b = make_b(ts)
    vals, vecs = np.linalg.eigh(b)
    all_large_eg.append(vals)
all_large_eg = np.array(all_large_eg)

larger_egs = -all_large_eg[:,0]*2/Ts**2
lower_large_eg, upper_large_eg = get_95_interval(larger_egs)
ax.errorbar(0,larger_egs[0] , yerr=([larger_egs[0]-upper_large_eg],[lower_large_eg-larger_egs[0]]), c = colors[2],elinewidth = 1,solid_capstyle='projecting', capsize=3)

smaller_egs = -all_large_eg[:,1]*2/Ts**2
lower_small_eg, upper_small_eg = get_95_interval(smaller_egs)
ax2.errorbar(1,larger_egs[1] , yerr=([larger_egs[1]-upper_small_eg],[lower_small_eg-larger_egs[1]]), c = colors[2],elinewidth = 1,solid_capstyle='projecting', capsize=3)



offset = 2
for index_pop in [2,0,1]:
    end_pop = offset + ns[index_pop]-1
    ax2.plot(range(offset,end_pop),(ns[index_pop]-1)*[2*ts_within[0,index_pop]**2/T**2],**format_small_analy)
    offset = offset + ns[index_pop]


# hide the spines between ax and ax2
ax.spines['bottom'].set_visible(False)
ax2.spines['top'].set_visible(False)
ax.xaxis.tick_top()
ax.tick_params(labeltop='off')  # don't put tick labels at the top
ax2.xaxis.tick_bottom()

d = .015  # how big to make the diagonal lines in axes coordinates

kwargs = dict(transform=ax.transAxes, color='k', clip_on=False, linewidth=1)
ax.plot((-d, +d), (-2*d, +2*d), **kwargs)        # top-left diagonal
ax.plot((1 - d, 1 + d), (-2*d, +2*d), **kwargs)  # top-right diagonal

kwargs.update(transform=ax2.transAxes)  # switch to the bottom axes
ax2.plot((-d, +d), (1 - d, 1 + d), **kwargs)  # bottom-left diagonal
ax2.plot((1 - d, 1 + d), (1 - d, 1 + d), **kwargs)  # bottom-right diagonal

ax.legend()
plt.xlabel("Eigenvalue index")
fig.text(0.04, 0.5, 'Eigenvalue', ha='center', va='center', rotation='vertical')
ax2.set_ylim(-0.001,0.018)
ax.set_ylim(0.58,.7)


fig.subplots_adjust(hspace=.025,left = 0.17)
fig.savefig("figure/JPT_CHB_YRI_eigenvalue.pdf")