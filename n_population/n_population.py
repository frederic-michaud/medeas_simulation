#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 20 17:03:27 2018

@author: Frederic
"""

import os
from subprocess import Popen
import numpy as np
import warnings
def run_simulation_n_pops(n_pop : int,n_individual_per_pop: int, L: int,
                              theta: float, D: float,
                              output_folder):

    current_folder = os.path.dirname(os.path.realpath(__file__))
    script_folder = os.path.split(current_folder)[0]
    n_individual_tot = n_individual_per_pop*n_pop
    scrm_result = os.path.join(output_folder,'scrm.txt')
    location_run_scrm = os.path.join(script_folder, "run_scrm.py")
    all_pop_string = n_pop*(str(n_individual_per_pop) + " ")
    all_split_string = " ".join([f'-ej {D*i} {i} {i+1}' for i in range(1,n_pop)])
    scrm_command = f'{n_individual_tot} {L} -t {theta} -I {n_pop} {all_pop_string}{all_split_string} --print-model -l -1 -L'
    run_scrm = Popen(['python', location_run_scrm, scrm_command, scrm_result])
    run_scrm.communicate()

    snip_file = os.path.join(output_folder,'snip.txt')
    location_transcode = os.path.join(script_folder, "transcode.py")
    transcode_commande = f'python {location_transcode} {scrm_result} {snip_file} {n_individual_tot}'
    print(transcode_commande)
    transcode = Popen(transcode_commande.split())
    transcode.communicate()

    location_create_fake_label = os.path.join(script_folder, "create_fake_labels.py")
    label_file = os.path.join(output_folder,'fake_labs.txt')
    fake_label_command = " ".join(['python', location_create_fake_label, '-of', label_file, '-ps',all_pop_string])
    print(fake_label_command)
    create_label = Popen(fake_label_command.split())
    create_label.communicate()

    location_run_medeas = os.path.join(script_folder, "run_medeas.py")
    K = n_pop
    nb_boot_window = 50
    bootwindow = int(L/nb_boot_window)
    command = " ".join(['python',location_run_medeas, snip_file,label_file,output_folder,str(K),str(bootwindow),f'pop{n_pop-1}'])
    print(command)
    medeas = Popen(command.split())
    medeas.communicate()



Ls = [int(10**(i/4)) for i in range(8,21)] #regulary space with 4 point between each order of magnitude
Ks = [2,3,4,5,6]
n_individual_per_pop = 15
theta = 2
sample_size = 25
D = 0.05
current_folder = os.path.dirname(os.path.realpath(__file__))
simulation_subfolder = "convergence_speed"
if not os.path.exists(simulation_subfolder):
    os.mkdir(simulation_subfolder)
output_folder = os.path.join(current_folder,simulation_subfolder)
if not os.path.exists("all_distance"):
    os.mkdir("all_distance")


for L in Ls:
    for K in Ks:
        distance_summary_file = f'all_distance/L_{L}_K_{K}.dat'
        summary_file = open(distance_summary_file,"w")
        for _ in range(sample_size):
            simulation_subsubfolder = f'L_{L}'
            simulation_subsubsubfolder = f'K_{K}'
            output_folder = os.path.join(current_folder, simulation_subfolder,simulation_subsubfolder,simulation_subsubsubfolder)
            if not os.path.exists(output_folder):
                os.makedirs(output_folder)
            run_simulation_n_pops(K, n_individual_per_pop, L, theta, D, output_folder)
            distance_file = os.path.join(output_folder,"all_extrapolated_distances.txt")
            if os.path.isfile(distance_file):
                distances = np.loadtxt(distance_file, ndmin=2)
                distances_average = np.mean(distances, axis=0)
                summary_file.write(" ".join(map(str, distances_average)) + '\n')
            else:
                warnings.warn('the file {distance_file} does not exist')

        summary_file.close()

