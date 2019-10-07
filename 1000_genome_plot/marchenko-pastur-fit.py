import numpy as np
import matplotlib.pyplot as plt
import os
import pickle
import scipy.optimize
prop_cycle = plt.rcParams['axes.prop_cycle']
colors = np.array(prop_cycle.by_key()['color'])
font = {'family' : 'normal',
        'size'   : 24}

plt.rc('font', **font)

#%%

def get_density_bound(T: float, L: float, N: int):
    """Get the boundary of the Marchenko-Pastur distribution
    """
    a = 2/T**2 * (1 - np.sqrt(N/L))**2
    b = 2/T**2 * (1 + np.sqrt(N/L))**2
    return (a,b)

def density_function_partial(x: float, T: float, L: float, N: int) -> float:
    """Marchenko-Pastur distribution function on interval
    a < x < b.
    """
    a, b = get_density_bound(T, L, N)
    sigma2 = 2/T**2
    ab = N/L
    density = 1/(2*np.math.pi*sigma2)*(np.sqrt((a-x)*(x-b)))/(x*ab)
    return density

def density_function(x: float, T: float, L: int, N: int):
    """Marchenko-Pastur distribution function for
    arbitrary x from total tree length 'T' and number of markers L.
    """
    a, b = get_density_bound(T, L, N)
    if x <= a:
        return 0
    if x >= b:
        return 0
    return density_function_partial(x, T, L, N)

#%%
def CDF_MP_not_normlized(x: float,a: float, b: float) -> float:
    """Integral of Marchenko-Pastur distribution function on interval
    a < x < b.
    """
    arc1 = np.arcsin((2*x - a - b)/(b - a)/1.0000000001)
    arc2 = np.arcsin(((a+b)*x-2*a*b)/x/(b - a)/1.0000000001)
    res = (np.sqrt((b-x)*(x-a))
            + (a+b)*arc1/2
            - np.sqrt(a*b)*arc2
            + np.pi*((a+b)/2 - np.sqrt(a*b))/2)
    return res
def CDF_MP(x: float,T: float, L: float, N: int) -> float:
    """Integral of Marchenko-Pastur distribution function on interval
    a < x < b.
    """
    a, b = get_density_bound(T, L, N)
    if x <= a:
        return 0.0
    if x >= b:
        return 1.0
    return CDF_MP_not_normlized(x,a,b)/CDF_MP_not_normlized(b,a,b)

#%%
def get_T_and_L_fit(lambdas):
    N = len(lambdas)

    def get_range_T_L():
        lambda_max = 1.1*lambdas[-1]
        lambda_min = lambdas[1]/1.1
        r = np.sqrt(lambda_max/lambda_min)
        L = N*((1-r)/(r+1))**2
        T = np.sqrt(2*(1+np.sqrt(N/L))**2/lambda_max)
        return((T, L))
    T_initial, L_initial = get_range_T_L()

    def CDF_MP_without_N(x: float, T: float, L: float) -> float:
        return CDF_MP(x, T, L, N)
    (T, L), pcov = scipy.optimize.curve_fit(np.vectorize(CDF_MP_without_N, otypes=[np.float]),
                       lambdas, np.linspace(0,1,len(lambdas)),
                       p0 = (T_initial, L_initial))
    return((T, L))

#%%
def plot_mp_vs_histogram(lambdas, show = True, title = "mp.pdf"):
    plt.cla()
    T, L = get_T_and_L_fit(lambdas)
    N = len(lambdas)
    a, b = get_density_bound(T, L, N)
    plt.hist(lambdas, 25, density=1, edgecolor='blue', alpha=0.75, label="Observed distribution",)
    xs = np.arange(a * 0.95, b / 0.95, (b - a) / 500)
    cdfs = [density_function(x, T, L, N) for x in xs]
    plt.plot(xs, cdfs, c=colors[2])
    plt.fill(xs, cdfs, c=colors[2], alpha=0.2, label="fitted Marchenko-Pastur")
    plt.xlabel("Bulk eigenvalue")
    plt.ylabel("Probability density function")
    plt.legend(loc="upper right")
    if show:
        plt.show()
    else:
        plt.savefig(title)


def plot_mp_vs_histogram_reduce(lambdas, ax):
    T, L = get_T_and_L_fit(lambdas)
    N = len(lambdas)
    a, b = get_density_bound(T, L, N)
    ax.hist(lambdas, 25, density=1, edgecolor='blue', alpha=0.75, label="Observed distribution")
    xs = np.arange(a * 0.95, b / 0.95, (b - a) / 500)
    cdfs = [density_function(x, T, L, N) for x in xs]
    print(cdfs)
    cdfs = cdfs/(np.sum(cdfs))*500/(b-a) #normalizing the function
    ax.plot(xs, cdfs, c=colors[2])
    ax.fill(xs, cdfs, c=colors[2], alpha=0.2, label="Marchenko-Pastur")




def get_pp_points(lambdas):
    T, L = get_T_and_L_fit(lambdas)
    N = len(lambdas)
    tobeplotted = [CDF_MP(x, T, L, N) for x in lambdas]
    return np.array(tobeplotted)


#%% Plot all MP on the same plot
fig, axes = plt.subplots(2,2,figsize=(12,9))

#%% Simulated data
simulation_subfolder = "../single_population/marchenko_pastur"
simulation_subsub_folder = os.path.join(simulation_subfolder,f"L_10000")
val, vec = pickle.load(open(os.path.join(simulation_subsub_folder, "MDS_eigensystem/p2.vecs.data"), "rb"))
pp_simulation = get_pp_points(val[1:])
plot_mp_vs_histogram_reduce(val[1:], axes[0][0])


#%%
simulation_subfolder = "../../../mds_1000_genome/random_prunning/medeas/single/YRI/"
val, vec = pickle.load(open(os.path.join(simulation_subfolder, "MDS_eigensystem/p2.vecs.data"), "rb"))
pp_random_prunning = get_pp_points(val[1:])
plot_mp_vs_histogram_reduce(val[1:],  axes[1][1])

#%%
simulation_subfolder = "../../../mds_1000_genome/plink_prunning/medeas/single/YRI/"
val, vec = pickle.load(open(os.path.join(simulation_subfolder, "MDS_eigensystem/p2.vecs.data"), "rb"))
pp_plink_prunning = get_pp_points(val[1:])
plot_mp_vs_histogram_reduce(val[1:],  axes[1][0])

#%%
simulation_subfolder = "../../../mds_1000_genome/no_prunning/medeas/single/YRI/"
val, vec = pickle.load(open(os.path.join(simulation_subfolder, "MDS_eigensystem/p2.vecs.data"), "rb"))
pp_no_prunning = get_pp_points(val[1:])
plot_mp_vs_histogram_reduce(val[1:],  axes[0][1])
fig.text(0.5, 0.03, 'Eigenvalue', ha='center')
fig.text(0.03, 0.5, 'Eigenvalue density', va='center', rotation='vertical')
#plt.show()
plt.savefig("marchenko-pastur.pdf")
#%% Plotting pp value plot
plt.figure()
plt.plot(pp_simulation, np.linspace(0,1,num= len(pp_simulation)),label = "Simulated value")
plt.plot(pp_no_prunning, np.linspace(0,1,num= len(pp_no_prunning)), label = " No prunning")
plt.plot(pp_plink_prunning, np.linspace(0,1,num= len(pp_plink_prunning)), label = "Plink prunning")
plt.plot(pp_random_prunning, np.linspace(0,1,num= len(pp_random_prunning)), label = "Random prunning")
plt.plot([0,1],[0,1],'k',lw = 0.5, label = "expected")
plt.xlabel("Theoretical distribution")
plt.ylabel("Observed distribution")
plt.legend()
plt.savefig("pp_plot_marchenko_pastur_fit.pdf")




#%%
