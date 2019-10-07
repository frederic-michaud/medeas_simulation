import numpy as np
import matplotlib.pyplot as plt
import os
import pickle
import matplotlib.ticker as ticker
import matplotlib.animation as animation


plt.rcParams.update({'font.size': 14})
prop_cycle = plt.rcParams['axes.prop_cycle']
colors = np.array(prop_cycle.by_key()['color'])
simulation_subfolder = "../../../Desktop/medeas_1000_genome/"
pop_name = "all_pop"
simulation_subsub_folder = os.path.join(simulation_subfolder,f"all/pop_all")

fig = plt.figure()
print(os.getcwd())


delta = pickle.load(open(os.path.join(simulation_subsub_folder, "asd_matrices", "p1.asd.data"), "rb"))
delta = delta
def calc_mds(delta):
    N = len(delta)

    a = -delta ** 2 / 2

    at0 = np.sum(a, 0) / N
    att = np.sum(a) / N ** 2

    one = np.ones((N,))
    b = a - np.outer(at0, one) - np.outer(one, at0) + att

    lambdas, vecs = np.linalg.eigh(b)
    return(lambdas,vecs)

lambdas,vecs = calc_mds(delta)


with open(os.path.join(simulation_subfolder,f'label/all/pop_all_haplo.lab'),"rb") as f:
    lines = f.readlines()
labels = [l.split()[0] for l in lines]
labels = np.array(labels,dtype=str)
populations, numerical_labels = np.unique(labels, return_inverse=True)
order = np.argsort(-lambdas)
nb_individuals = len(lambdas)
ind_colors = colors[numerical_labels]
p = range(0,5)
for individual in range(nb_individuals):
    if not (labels[individual] =="CEU" or labels[individual] =="TSI"):
        plt.plot(p, np.sqrt(lambdas[order[p]])*vecs[individual,order[p]],c = ind_colors[individual])
for individual in range(nb_individuals):
    if (labels[individual] =="CEU" or labels[individual] =="TSI"):
        plt.plot(p, np.sqrt(lambdas[order[p]])*vecs[individual,order[p]],c = ind_colors[individual])
plt.show()
plt.cla()

populations = ['LWK', "YRI", 'CHB', 'JPT', 'TSI','CEU']
label_pop = ["African 1 (LWK)", "African 2 (YRI)", "Asian 1 (CHB)", "Asian 2 (JPT)","European 1 (TSI)","European 2 (CEU)"]
order = np.argsort(-lambdas)
print(populations)
def plot_axis(p, q):
    fig = plt.figure(figsize=(6,6))
    for index_population, population in enumerate(populations):
        population_span = np.where(population == labels)
        plt.plot(np.sign(vecs[0, order[p]]) * np.sqrt(lambdas[order[p]]) * vecs[population_span, order[p]],
                 np.sign(vecs[0, order[q]]) * np.sqrt(lambdas[order[q]]) * vecs[population_span, order[q]],
                 color='none')
        plt.scatter(np.sign(vecs[0, order[p]]) * np.sqrt(lambdas[order[p]]) * vecs[population_span, order[p]],
                    np.sign(vecs[0, order[q]]) * np.sqrt(lambdas[order[q]]) * vecs[population_span, order[q]],
                    c=colors[index_population], alpha=0.5, label=label_pop[index_population])
    plt.xticks([])
    plt.yticks([])
    #plt.legend(loc='upper center', bbox_to_anchor=(.25, 1.05), ncol=3)
    plt.legend()
    plt.xlabel(f"PC {p + 1}")
    plt.ylabel(f"PC {q + 1}")
    fig.patch.set_facecolor('blue')
    fig.patch.set_alpha(0.7)
    fig.savefig(f"MDS_pres_{p+1}_{q+1}.pdf", edgecolor='blue',facecolor="none")
    plt.cla()

plot_axis(0,1)
plot_axis(2,3)
symbol = ["*","+","^","_"]
def plot_axis_lighter(p, q):
    plt.figure(figsize=(6,6))
    for index_population, population in enumerate(populations):
        population_span = np.where(population == labels)
        plt.plot(np.sign(vecs[0, order[p]]) * np.sqrt(lambdas[order[p]]) * vecs[population_span, order[p]],
                 np.sign(vecs[0, order[q]]) * np.sqrt(lambdas[order[q]]) * vecs[population_span, order[q]],
                 color='none')
        if index_population < 4:
            plt.scatter(np.sign(vecs[0, order[p]]) * np.sqrt(lambdas[order[p]]) * vecs[population_span, order[p]],
                    np.sign(vecs[0, order[q]]) * np.sqrt(lambdas[order[q]]) * vecs[population_span, order[q]],
                    c="lightgrey", alpha=0.5,marker=symbol[index_population], label=label_pop[index_population])
        else:
            plt.scatter(np.sign(vecs[0, order[p]]) * np.sqrt(lambdas[order[p]]) * vecs[population_span, order[p]],
                        np.sign(vecs[0, order[q]]) * np.sqrt(lambdas[order[q]]) * vecs[population_span, order[q]],
                        c=colors[index_population], alpha=0.5, label=label_pop[index_population])
    plt.xticks([])
    plt.yticks([])
    #plt.legend(loc='upper center', bbox_to_anchor=(.25, 1.05), ncol=3)
    plt.legend()
    plt.xlabel(f"PC {p+1}")
    plt.ylabel(f"PC {q + 1}")
    plt.savefig(f"MDS_pres_{p+1}_{q+1}.pdf", edgecolor='blue',facecolor="none")
    plt.cla()
plot_axis_lighter(4,5)
