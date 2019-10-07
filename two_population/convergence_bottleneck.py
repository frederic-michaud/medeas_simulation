#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 13 17:03:27 2018

@author: Frederic
"""

from subprocess import Popen
import os
import numpy as np
import warnings

def run_simulation_two_pops(n1: int, n2: int, L: int, theta: float, D: float, strength_bottleneck,length_bottleneck, output_folder):

    current_folder = os.path.dirname(os.path.realpath(__file__))
    script_folder = os.path.split(current_folder)[0]

    scrm_result = os.path.join(output_folder,'scrm.txt')
    location_run_scrm = os.path.join(script_folder, "run_scrm.py")
    #-en < t > < i > < n >: Set the size of population i to n * N0 at time t.

    scrm_command = f'{n1+n2} {L} -t {theta} -I 2 {n1} {n2} -ej {D} 2 1 -en {D - length_bottleneck} 2 {strength_bottleneck} --print-model -l -1 -L'
    run_scrm = Popen(['python', location_run_scrm, scrm_command, scrm_result])
    run_scrm.communicate()

    snip_file = os.path.join(output_folder,'snip.txt')
    location_transcode = os.path.join(script_folder, "transcode.py")
    transcode_commande = f'python {location_transcode} {scrm_result} {snip_file} {n1+n2}'
    print(transcode_commande)
    transcode = Popen(transcode_commande.split())
    transcode.communicate()

    location_create_fake_label = os.path.join(script_folder, "create_fake_labels.py")
    label_file = os.path.join(output_folder,'fake_labs.txt')
    fake_label_command = " ".join(['python', location_create_fake_label, '-of', label_file, '-ps', str(n1), str(n2)])
    print(fake_label_command)
    create_label = Popen(fake_label_command.split())
    create_label.communicate()

    location_run_medeas = os.path.join(script_folder, "run_medeas.py")
    K = 2
    nb_boot_window = 50
    bootwindow = int(L/nb_boot_window)
    command = " ".join(['python',location_run_medeas, snip_file,label_file,output_folder,str(K),str(bootwindow)])
    print(command)
    medeas = Popen(command.split())
    medeas.communicate()


Ls = [100000]

D=0.1
Nes = [int(10**(-i/4+4))/10000 for i in range(0, 13)]
sample_size = 6
current_folder = os.path.dirname(os.path.realpath(__file__))
simulation_subfolder = "convergence_bottleneck"
result_subfolder_fullpath = os.path.join(current_folder, simulation_subfolder)
if not os.path.exists(result_subfolder_fullpath):
    os.makedirs(result_subfolder_fullpath)
strength_bottlenecks = [1,0.1,0.01,0.001]
length_bottleneck = 0.01
for L in Ls:
    for strength_bottleneck in strength_bottlenecks:
        distance_summary_file = os.path.join(result_subfolder_fullpath, f'L_{L}_bl_{strength_bottleneck}.dat')
        summary_file = open(distance_summary_file, "w")
        coalescence_summary_file = os.path.join(result_subfolder_fullpath, f'L_{L}_bl_{strength_bottleneck}_coal.dat')
        coalescence_summary = open(coalescence_summary_file, "w")
        for _ in range(sample_size):
            simulation_subsubfolder = f'L_{L}_bl_{strength_bottleneck}'
            output_folder = os.path.join(current_folder, simulation_subfolder, simulation_subsubfolder)
            if not os.path.exists(output_folder):
                os.makedirs(output_folder)
            n1 = 20
            n2 = 20
            theta = 2.
            run_simulation_two_pops(n1, n2, int(L), theta, D,strength_bottleneck,length_bottleneck, output_folder)

            distance_file = os.path.join(output_folder, "all_extrapolated_distances.txt")
            effective_size_file = os.path.join(output_folder, "all_extrapolated_effective_size.txt")
            distance = 0
            sd = 0
            if os.path.isfile(distance_file):
                distances = np.loadtxt(distance_file)
                distance = np.mean(distances)
                sd = np.std(distances)
                summary_file.write(f'{distance} {sd} \n')
            else:
                warnings.warn('the file {distance_file} does not exist')
            if os.path.isfile(effective_size_file):
                effective_sizes = np.loadtxt(effective_size_file)
                effective_size = np.mean(effective_sizes,axis=0)
                sd = np.std(effective_sizes)
                coalescence_summary.write(f'{effective_size[1]} \n')
            else:
                warnings.warn('the file {coalescence_summary} does not exist')



        summary_file.close()
        coalescence_summary.close()

