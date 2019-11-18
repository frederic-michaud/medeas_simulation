import numpy as np
import matplotlib.pyplot as plt
import os
import pickle
import matplotlib.ticker as ticker
import matplotlib.lines as mlines
import matplotlib.colors as plt_colors
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




def get_index(i, ns):
    ns = np.concatenate((np.array([0]), ns))
    index_ind = np.cumsum(ns)
    index_pop = np.where(np.logical_and(i < index_ind[1:],i >=  index_ind[:-1]))[0][0]
    return index_pop

def get_dist(i, j, ns):
    pop_i = get_index(i, ns)
    pop_j = get_index(j, ns)
    distance = 0
    if i==j:
        distance = 0
    elif pop_i == pop_j:
        if pop_i == 0:
            distance = t11
        if pop_i == 1:
            distance = t22
        if pop_i == 2:
            distance = t33

    elif (pop_i == 1 and pop_j == 2) or (pop_i == 2 and pop_j == 1):
        distance = t23
    else:
        distance = t13

    return distance


def calc_mds(distance_matrix) -> None:
    """Read distance matrix from 'file', calculate the eigensystem,
    and store it into 'outfile'.
    """
    N = len(distance_matrix)
    a = -distance_matrix**2/2
    at0 = np.sum(a, 0)/N
    att = np.sum(a)/N**2
    one = np.ones((N,))
    b = a - np.outer(at0, one) - np.outer(one, at0) + att

    lambdas, vecs = np.linalg.eigh(b)
    order = np.argsort(-lambdas)
    return lambdas[order], vecs[:, order]



def plot_mds(coordinate, p, q, label_given, title = "mds.pdf"):
    prop_cycle = plt.rcParams['axes.prop_cycle']
    prop_cycle = prop_cycle * (1 + len(np.unique(label_given)) // len(prop_cycle))
    colors = prop_cycle.by_key()['color']
    plt.rcParams.update({'font.size': 22})
    fig, ax = plt.subplots(figsize=(8, 8))
    for population_index, population_name in enumerate(np.unique(label_given)):
        position_population = np.where(population_name == label_given)
        color_value = colors[1:4][population_index]
        ax.scatter(coordinate.T[p, position_population].ravel(), coordinate.T[q, position_population].ravel(),
                   c=color_value, s=75, alpha=0.6)
    plt.legend(np.unique(label_given))
    leg = ax.get_legend()
    for point in leg.legendHandles:
        point.set_color('black')

    markers_color = [mlines.Line2D([], [], color=marker_color, marker="o", linestyle='None') for marker_color in colors[1:4]]
    plt.legend(markers_color, np.unique(label_given), title="Population", bbox_to_anchor=(1.04, 0.5),
               loc="center left", borderaxespad=0)

    ax.set_xlabel(f'PC. {p + 1}')
    ax.set_ylabel(f'PC. {q + 1}')
    fig.savefig(title,bbox_inches="tight")
    plt.close()

label_pop = ["pop 1","pop 2","pop 3"]
label_given = np.repeat(label_pop, ns)
nb_individual =np.sum(ns)
distance_matrix = np.array([[get_dist(i, j, ns) for i in range(nb_individual)] for j in range(nb_individual)])
eigenvalue, eigenvector = calc_mds(distance_matrix)
plot_mds(eigenvector, 0, 1, label_given, "figure/three_pop_example_mds.pdf")
fig, ax = plt.subplots(figsize=(8, 8))
color_panel = list(zip([0,t33/t13,t22/t13,t23/t13,t11/t13,1],
                       ["#ffffff"+"99", colors[3]+"99", colors[2]+"99", colors[4]+"99",colors[1]+"99",colors[0]+"99"]))
my_colors = plt_colors.LinearSegmentedColormap.from_list("hello",color_panel)

plt.imshow(distance_matrix, my_colors)
plt.tick_params(
    axis='x',          # changes apply to the x-axis
    which='both',      # both major and minor ticks are affected
    bottom=True,
    top=True,
    labelbottom=False)
plt.tick_params(
    axis='y',          # changes apply to the x-axis
    which='both',      # both major and minor ticks are affected
    left=True,
    right=True,
    labelleft=False)
plt.grid(color="k")

plt.yticks(np.array(range(nb_individual))+0.5)
start_position = np.cumsum(np.concatenate((np.full(1,0 ),ns)))
plt.xticks(start_position-0.5)
plt.yticks(start_position-0.5)
for index_position in range(len(start_position) - 1):
    plt.text((start_position[index_position] + start_position[index_position + 1]) / 2, -1,
             label_pop[index_position],
             verticalalignment='bottom',
             horizontalalignment='center',
             rotation=90
             )
    plt.text(-1, (start_position[index_position] + start_position[index_position + 1]) / 2,
             label_pop[index_position],
             verticalalignment='center',
             horizontalalignment='right',
             )

plt.savefig("figure/three_pop_example_distance.pdf")


plt.figure(figsize=(8, 8))
max_eg = np.max(eigenvector)
min_eg = np.min(eigenvector)
position_0 = -min_eg/(max_eg - min_eg)
print(position_0)
color_panel = list(zip([0,0.1,position_0,0.9,1],
                       [colors[1],colors[0],"#ffffff",colors[2],colors[3]]))

my_colors = plt_colors.LinearSegmentedColormap.from_list("hello",color_panel)
plt.imshow(eigenvector, my_colors)
plt.xlabel("eigenvector index")
plt.ylabel("individual")
cbar = plt.colorbar()
cbar.ax.set_ylabel("Eigenvector component", rotation=-90, va="bottom")
plt.savefig("figure/three_pop_example_eigenvector.pdf")
