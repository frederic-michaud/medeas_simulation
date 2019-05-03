import numpy as np
import matplotlib
#matplotlib.use("cairo")
import matplotlib.pyplot as plt
import pickle
import os

prop_cycle = plt.rcParams['axes.prop_cycle']
colors = np.array(prop_cycle.by_key()['color'])
from matplotlib.backends.backend_pdf import PdfPages
cwd = os.getcwd()

simulation_subfolder = "generate_mds"
cwd = os.getcwd()
simulation_subfolder = os.path.join(cwd, simulation_subfolder)


L = 10000
location_vector = os.path.join (simulation_subfolder, f'/{simulation_subfolder}/L_{L}/asd_matrices/p1.asd.data')
delta = pickle.load(open(location_vector,"rb"))
plt.imshow(delta)

n1 = n2 = n3 = 20
positions = (n1 /2, n1 + n2/2,n1 + n2 + n3/2)
labels =("Pop. 1","Pop. 2","Pop. 3")
plt.xticks(positions,labels , rotation='vertical')
plt.yticks(positions, labels)
#plt.show()
plt.savefig(os.path.join("delta_three_population.pdf"),facecolor='None')
