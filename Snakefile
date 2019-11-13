from snakemake.remote.FTP import RemoteProvider

report: "report/workflow.rst"

configfile: "config.yaml"

populations = config["populations"] if "populations" in config.keys() else ["CEU","YRI","LWK"]

all_pairs = []


rule all:
    input:
        "figure/two_pop_constant_size_mds.pdf",
        "figure/two_pop_constant_size_eigenvalue.pdf",
        "figure/three_pop_example_eigenvalue.pdf",
        "figure/three_pop_example_mds.pdf",
        "figure/three_pop_example_distance.pdf",
        "figure/three_pop_example_eigenvector.pdf",
        "figure/MDS_1_2.pdf",
        "figure/MDS_3_4.pdf",
        "figure/MDS_5_6.pdf",
        "figure/YRI_JPT_CHB_mds.pdf",
        "figure/YRI_JPT_CHB_eigenvalue.pdf",
        "figure/JPT_CHB_eigenvalues.pdf",
        "figure/JPT_CHB_mds.pdf",
        "figure/two_pop_constant_size_convergence_speed_L.pdf",
        "figure/three_pop_t.pdf",
        "figure/three_pop_mds.pdf",
        "figure/three_pop_eigenvalue.pdf",
        "figure/pp_plot_marchenko_pastur_fit.pdf",
        "figure/marchenko-pastur.pdf",
        "figure/mcvean_approximation.pdf",
        "figure/6_pop_constant_size.pdf",
        "figure/two_pop_different_ratio.pdf"

rule simulate_mcvean_formula:
    output:
        directory("check_mcvean_formula/panmictic_pop")
    shell:
        "python check_mcvean_formula/simplex_few_individuals.py"

rule plot_mcvean_formula:
    input:
        directory("check_mcvean_formula/panmictic_pop")
    output:
        "figure/mcvean_approximation.pdf"
    shell:
        "python check_mcvean_formula/plot_mcvean.py"




rule simulate_marchenko_pastur_single_population:
    output:
        directory("single_population/marchenko_pastur")
    shell:
        "python single_population/marchenko_pastur.py"

rule plot_marchenko_pastur:
    input:
        directory("single_population/marchenko_pastur")
    output:
        "figure/pp_plot_marchenko_pastur_fit.pdf",
        "figure/marchenko-pastur.pdf"
    shell:
        "python 1000_genome_plot/marchenko-pastur-fit.py {config[location_1000_value]}"



rule two_pop_eigenvalue:
    input:
        directory("two_population/convergence_various_D/L_10000_D_0.1")
    output:
        "figure/two_pop_constant_size_eigenvalue.pdf"
    shell:
        "python two_population/plot_eigenvalue_paper.py"

rule two_pop_mds:
    input:
        directory("two_population/convergence_various_D/L_10000_D_0.1")
    output:
        "figure/two_pop_constant_size_mds.pdf"
    shell:
        "python two_population/plot_MDS_paper.py"

rule two_pop_simulate_given_parameter:
    output:
        directory("two_population/convergence_various_D/L_{L}_D_{D}")
    shell:
        "python two_population/simulate_given_parameters.py {wildcards.L} {wildcards.D}"

rule two_pop_simulate_convergence_L:
    output:
        directory("two_population/convergence_various_L")
    shell:
        "python two_population/simulate_two_population.py"

rule two_pop_plot_convergence_L:
    input:
        directory("two_population/convergence_various_D")
    output:
        "figure/two_pop_constant_size_convergence_speed_L.pdf"
    shell:
        "python two_population/plot_various_L.py"

rule two_pop_simulate_convergence_D:
    output:
        directory("two_population/convergence_various_D")
    shell:
        "python two_population/convergence_various_D.py"

rule two_pop_plot_convergence_D:
    input:
        directory("two_population/convergence_various_D")
    output:
        "figure/two_pop_different_D.pdf"
    shell:
        "python two_population/plot_various_D.py"

rule two_pop_simulate_various_ratio:
    output:
        directory("two_population/convergence_various_sample_ratio")
    shell:
        "python two_population/simulate_different_ratio.py"

rule two_pop_plot_various_ratio:
    input:
        "two_population/convergence_various_sample_ratio"
    output:
        "figure/two_pop_different_ratio.pdf"
    shell:
        "python two_population/plot_different_ratio.py"

rule two_population_1000_genome_mds:
    output:
        "figure/JPT_CHB_eigenvalues.pdf",
        "figure/JPT_CHB_mds.pdf"
    shell:
        "python 1000_genome_plot/two_population_constant_size.py  {config[location_1000_value]}"




rule three_pop_example:
    output:
        "figure/three_pop_example_eigenvalue.pdf",
        "figure/three_pop_example_mds.pdf",
        "figure/three_pop_example_distance.pdf",
        "figure/three_pop_example_eigenvector.pdf"
    shell:
        "python 1000_genome_plot/example_3pop.py"

rule three_pop_simulate_bottleneck:
    output:
        directory("three_population/convergence_bottleneck")
    shell:
        "python three_population/three_population_bottleneck.py"

rule three_population_plot_bottleneck:
    input:
        directory("three_population/convergence_bottleneck")
    output:
        "figure/three_pop_t.pdf"
    shell:
        "python three_population/plot_bottleneck.py"

rule three_population_simulation_mds_and_eigenvalue:
    input:
        directory("three_population/convergence_bottleneck")
    output:
        "figure/three_pop_mds.pdf",
        "figure/three_pop_eigenvalue.pdf"
    shell:
        "python three_population/plot_MDS_and_eigenvalue_paper.py"


rule three_population_1000_genome_mds:
    output:
        "figure/YRI_JPT_CHB_mds.pdf",
        "figure/YRI_JPT_CHB_eigenvalue.pdf"
    shell:
        "python 1000_genome_plot/three_population.py {config[location_1000_value]}"

rule simulate_six_population_constant_size:
    output:
        directory("n_population/convergence_speed")
    shell:
        "python n_population/n_population.py"

rule plot_six_population_constant_size:
    input:
        "n_population/convergence_speed"
    output:
        "figure/6_pop_constant_size.pdf"
    shell:
        "python n_population/plot_convergence_speed.py"


rule six_population_1000_genome_mds:
    output:
        "figure/MDS_1_2.pdf",
        "figure/MDS_3_4.pdf",
        "figure/MDS_5_6.pdf"
    shell:
        "python 1000_genome_plot/six_population.py {config[location_1000_value]}"
