#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 13 17:03:27 2018

@author: Frederic
"""

from subprocess import Popen
import os
import numpy as np



## population 1 remain the last one and is the ancestral population (i.e. african)
## population 2 and 3 goes through a bottleneck directly after diverging from pop 1, and split a rather long time after that
# Population 3 is the first one to disapear
def run_simulation_three_pops(n1: int, n2: int, n3: int, L: int, theta: float, D1: float,D2: float,strenght_bottleneck: float, length_bottleneck: float,output_folder):

    current_folder = os.path.dirname(os.path.realpath(__file__))
    script_folder = os.path.split(current_folder)[0]

    scrm_result = os.path.join(output_folder,'scrm.txt')
    location_run_scrm = os.path.join(script_folder, "run_scrm.py")
    # -en < t > < i > < n >: Set the size of population i to n * N0 at time t.
    # -ej < t > < j > < i >: Adds a specialization event in population i that creates population j
    scrm_command = f'{n1+n2+n3} {L} -t {theta} -I 3 {n1} {n2} {n3} -ej {D1} 3 2 -ej {D2} 2 1 -en 0 2 1 -en {D2 - length_bottleneck} 2 {strenght_bottleneck} --print-model -l -1 -L'
    run_scrm = Popen(['python', location_run_scrm, scrm_command, scrm_result])
    run_scrm.communicate()

    snip_file = os.path.join(output_folder,'snip.txt')
    location_transcode = os.path.join(script_folder, "transcode.py")
    transcode_commande = f'python {location_transcode} {scrm_result} {snip_file} {n1+n2+n3}'
    print(transcode_commande)
    transcode = Popen(transcode_commande.split())
    transcode.communicate()

    location_create_fake_label = os.path.join(script_folder, "create_fake_labels.py")
    label_file = os.path.join(output_folder,'fake_labs.txt')
    fake_label_command = " ".join(['python', location_create_fake_label, '-of', label_file, '-ps', str(n1), str(n2), str(n3)])
    print(fake_label_command)
    create_label = Popen(fake_label_command.split())
    create_label.communicate()

    location_run_medeas = os.path.join(script_folder, "run_medeas.py")
    K = 3
    nb_boot_window = 50
    bootwindow = int(L/nb_boot_window)
    command = " ".join(['python',location_run_medeas, snip_file,label_file,output_folder,str(bootwindow)])
    print(command)
    medeas = Popen(command.split())
    medeas.communicate()



Ls = [10000] #regulary space with 4 point between each order of magnitude
D1 = 0.025
D2 = 0.1
n1 = 15
n2 = 20
n3 = 25
strenght_bottlenecks = [int(10**(-i/4+4))/10000 for i in range(0, 9)]
length_bottleneck = 0.025

theta = 3
sample_size = 100


current_folder = os.path.dirname(os.path.realpath(__file__))
simulation_subfolder = "convergence_bottleneck"
simulation_subfolder = os.path.join(current_folder,simulation_subfolder)
if not os.path.exists(simulation_subfolder):
    os.mkdir(simulation_subfolder)
for L in Ls:
    for strenght_bottleneck in strenght_bottlenecks:
        within_summary_file = os.path.join(simulation_subfolder,f'L_{L}_Ne_{strenght_bottleneck}.within')
        between_summary_file = os.path.join(simulation_subfolder, f'L_{L}_Ne_{strenght_bottleneck}.between')
        summary_within = open(within_summary_file, "w")
        summary_between= open(between_summary_file, "w")
        for _ in range(sample_size):
            simulation_subsubfolder = f'L_{L}_Ne_{strenght_bottleneck}'
            output_folder = os.path.join(simulation_subfolder,simulation_subsubfolder)
            if not os.path.exists(output_folder):
                os.makedirs(output_folder)
            run_simulation_three_pops(n1, n2, n3, L, theta, D1, D2, strenght_bottleneck , length_bottleneck, output_folder)
            distance_file = os.path.join(output_folder,"between_population_coalescence_time.txt")
            distances  = np.loadtxt(distance_file, skiprows = 1)
            distance1 = np.mean(distances[:,0])
            distance2 = np.mean(distances[:, 1])
            summary_between.write(f'{distance1} {distance2} \n')
            summary_between.flush()
            distance_file = os.path.join(output_folder,"within_population_coalescence_time.txt")
            distances  = np.loadtxt(distance_file, skiprows = 1)
            effective_size_1 = np.mean(distances[:,1])
            effective_size_2 = np.mean(distances[:, 2])
            summary_within.write(f'{effective_size_1} {effective_size_2} \n')
            summary_within.flush()
        summary_between.close()
        summary_within.close()

