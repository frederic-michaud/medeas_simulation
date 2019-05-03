import numpy as np
import matplotlib.pyplot as plt
import os
import pickle

plt.rcParams.update({'font.size': 14})
prop_cycle = plt.rcParams['axes.prop_cycle']
colors = np.array(prop_cycle.by_key()['color'])
simulation_subfolder = "convergence_bottleneck"
D1 = 0.025
D2 = 0.1
n1 = 15
n2 = 20
n3 = 25
strenght_bottlenecks = [int(10**(-i/4+4))/10000 for i in range(0, 13)]
strenght_bottleneck = strenght_bottlenecks[6]
size_bottleneck = strenght_bottleneck
print(f"strength bottleneck = {strenght_bottleneck}")
L = 10000
length_bottleneck = 0.025

simulation_subsubfolder = os.path.join(simulation_subfolder,f'L_{L}_Ne_{strenght_bottleneck}')

fig = plt.figure()
def expected_time_two_change(n1: float, n2: float, D1: float, D2: float):
    n_effectif = n2 + np.exp(-2*(D1/n1 + D2/n2))*(1 - n1 + np.exp(2*D1/n1)*(n1-n2))
    return(n_effectif)

t22 = t33  = expected_time_two_change(size_bottleneck, 1, length_bottleneck, D2 - length_bottleneck)
t23 = 2*D1 + expected_time_two_change(size_bottleneck, 1, length_bottleneck, D2 - length_bottleneck- D1 )

t13 = t12 =  2*D2 + 1
t11 = 1

ns = [15,20,25]
npop = len(ns)

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

ts = np.array([[t11,t12,t13],[t12,t22,t23],[t13,t23,t33]])
print(ts)
b = make_b(ts)
vals, vecs = np.linalg.eigh(b)



val,vec = pickle.load(open(os.path.join(simulation_subsubfolder,"MDS_eigensystem","p1.vecs.data"),"rb"))
pointColor = colors[np.concatenate((np.full(15,0,dtype=int),np.full(20,1,dtype=int),np.full(25,2,dtype=int)))]
order = np.argsort(-val)
populations_sizes = [15,20,25]
threshold = 0
for population_size in populations_sizes:
    population_span = range(threshold,threshold+population_size)
    plt.scatter(np.sqrt(val[order[0]])*vec[population_span,order[0]],np.sqrt(val[order[1]])*vec[population_span,order[15]],c = pointColor[population_span],alpha=0.5)
    threshold = threshold + population_size
plt.legend(["Pop. 1","Pop. 2"],loc = 1)
plt.xlabel("Dimension 1")
plt.ylabel("Dimension 2")

plt.show()
fig.savefig("three_pop_bottleneck_mds.pdf")

fig = plt.figure()
Ts = np.loadtxt(open(os.path.join(simulation_subsubfolder, "all_extrapolated_T.txt")))
plt.plot(-np.sort(-val),"o",alpha = 0.5, label = "Simulated values")

T = Ts[0]
large_eg_analytical =  -2*vals/T**2
print(large_eg_analytical)
plt.plot(2,large_eg_analytical[1],"o")
plt.plot(1,large_eg_analytical[0],"o")
#plt.plot(range(1,39), 38*[2/T**2], "x", color=colors[2], label = "Analytical prediction")
#plt.plot(39, 0, "x", color=colors[2])

plt.show()


# If we were to simply plot pts, we'd lose most of the interesting
# details due to the outliers. So let's 'break' or 'cut-out' the y-axis
# into two portions - use the top (ax) for the outliers, and the bottom
# (ax2) for the details of the majority of our data
fig, (ax, ax2) = plt.subplots(2, 1, sharex=True, gridspec_kw={'height_ratios': [1, 2]})
format_common = dict(color = colors[2], marker = "_")
format_small_analy = format_common.copy()
format_small_analy.update(dict(markersize = 10, markeredgewidth = 1))
format_large_analy = format_common.copy()
format_large_analy.update(dict(markersize = 12, markeredgewidth = 2))
# plot the same data on both axes
ax.plot(-np.sort(-val),"o",alpha = 0.5, label = "Simulated values")
ax2.plot(-np.sort(-val),"o",alpha = 0.5)
ax2.plot(range(16,59),43*[2*t22**2/(T**2)],"_",**format_small_analy)
ax2.plot(range(1,15),14*[2*t11**2/(T**2)],"_",**format_small_analy)
ax2.plot(15,large_eg_analytical[1],"_",**format_large_analy)
ax2.plot(59, 0, "_", **format_large_analy)
ax.plot(0,large_eg_analytical[0],"_",label = "Analytical results",**format_large_analy)
# zoom-in / limit the view to different portions of the data
ax.set_ylim(.29, .4)  # outliers only
ax2.set_ylim(-0.0005, .021)  # most of the data

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


fig.subplots_adjust(hspace=.05,left = 0.16)
ax.legend()
ax2.set_xlabel("Eigenvalue index")
ax2.set_ylabel("  ")
ax2.set_yticks([0,0.01,0.02])
fig.text(0.04, 0.5, 'Eigenvalue', ha='center', va='center', rotation='vertical')

fig.savefig("two_pop_constant_size_eigenvalue.pdf")
