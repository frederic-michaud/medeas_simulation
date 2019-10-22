import numpy as np
import matplotlib.pyplot as plt
import os
import pickle
import matplotlib.ticker as ticker

plt.rcParams.update({'font.size': 14})
prop_cycle = plt.rcParams['axes.prop_cycle']
colors = np.array(prop_cycle.by_key()['color'])

fig = plt.figure()




ns = np.array([10,8,6])
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

#alpha is the first split and beta the second one
alpha = 0.2
beta = 0.1
D_beta = 0.05
D_alpha = 0.1

t11 = 1
t22 = alpha + np.exp(-D_alpha/alpha)*(1-alpha)
t33 = beta + np.exp(-D_alpha/alpha - D_beta/beta)*(1 - alpha + np.exp(D_alpha/alpha)*(alpha-beta))

t23 = D_beta + alpha + np.exp(-(D_alpha-D_beta)/alpha)*(1-alpha)
t13 = t12 = 1 + D_alpha
ts = np.array([[t11,t12,t13],[t12,t22,t23],[t13,t23,t33]])
print(ts)
b = make_b(ts)

vals, vecs = np.linalg.eigh(b)
vals = -2*vals
args_plot = {"marker" : "o","alpha" : 0.5,"linestyle" : 'None'}
plt.plot((1,2),(vals[0],vals[1]),label = "Between populations",**args_plot)
plt.plot(range(3,2 + ns[0]),np.full(ns[0]-1,t11**2),label = "Within first population",**args_plot)
plt.plot(range(2 + ns[0],1 + ns[0] + ns[1]),np.full(ns[1]-1,t22**2),label = "Within second population",**args_plot)
plt.plot(range(1 + ns[0] + ns[1],n),np.full(ns[2]-1,t33**2),label = "Within third population",**args_plot)
plt.plot(n,0,label = "Constant eigenvector",**args_plot)
plt.xlabel("Eigenvalue index")
plt.ylabel("Eigenvalue")
plt.legend()
fig.savefig("figure/three_pop_example_eigenvalue.pdf")
