#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 13 17:03:27 2018

@author: Frederic
"""

from subprocess import Popen
import os
import numpy as np


def run_simulation_four_pops(n: int, L: int, theta: float, D1: float,D2: float,D3: float,length_bottleneck: float, size_bottleneck: float, output_folder: str):

    current_folder = os.path.dirname(os.path.realpath(__file__))
    script_folder = os.path.split(current_folder)[0]

    scrm_result = os.path.join(output_folder,'scrm.txt')
    location_run_scrm = os.path.join(script_folder, "run_scrm.py")
    #-en < t > < i > < n >: Set the size of population i to n * N0 at time t.

    scrm_command = f'{4*n} {L} -t {theta} -I 4 {n} {n} {n} {n} -ej {D1} 3 2 -ej {D2} 1 2 -ej {D3} 4 3 -en {D1-length_bottleneck} 3 {size_bottleneck} --print-model -l -1 -L'
    run_scrm = Popen(['python', location_run_scrm, scrm_command, scrm_result])
    run_scrm.communicate()

    snip_file = os.path.join(output_folder,'snip.txt')
    location_transcode = os.path.join(script_folder, "transcode.py")
    transcode_commande = f'python {location_transcode} {scrm_result} {snip_file} {4*n}'
    print(transcode_commande)
    transcode = Popen(transcode_commande.split())
    transcode.communicate()

    location_create_fake_label = os.path.join(script_folder, "create_fake_labels.py")
    label_file = os.path.join(output_folder,'fake_labs.txt')
    fake_label_command = " ".join(['python', location_create_fake_label, '-of', label_file, '-ps', str(n), str(n), str(n), str(n)])
    print(fake_label_command)
    create_label = Popen(fake_label_command.split())
    create_label.communicate()

    location_run_medeas = os.path.join(script_folder, "run_medeas.py")
    K = 4
    nb_boot_window = 50
    bootwindow = int(L/nb_boot_window)
    command = " ".join(['python', location_run_medeas, snip_file, label_file, output_folder, str(K), str(bootwindow)])
    print(command)
    medeas = Popen(command.split())
    medeas.communicate()



Ls = [int(10**(i/4)) for i in range(20,21)] #regulary space with 4 point between each order of magnitude
Ls = [10000] #regulary space with 4 point between each order of magnitude
D1 = 0.3
D2 = 0.1
D3 = 0.1
length_bottleneck = 0.05
size_bottlenecks =[int(10**(-i/4+4))/10000 for i in range(0, 13)]
size_bottlenecks = [0.001,0.01]

n = 20
theta = 3
sample_size = 3
current_folder = os.path.dirname(os.path.realpath(__file__))
simulation_subfolder = "bottleneck"
if not os.path.exists(simulation_subfolder):
    os.mkdir(simulation_subfolder)
for L in Ls:
    for size_bottleneck in size_bottlenecks:
        distance_summary_file = os.path.join(simulation_subfolder,f'L_{L}_size_bottlenecks_{size_bottleneck}.between')
        summary_file = open(distance_summary_file, "w")
        within_summary_file = os.path.join(simulation_subfolder,f'L_{L}_size_bottlenecks_{size_bottleneck}.within')
        within_summary = open(within_summary_file, "w")
        for _ in range(sample_size):
            simulation_subsubfolder = f'L_{L}_size_bottlenecks_{size_bottleneck}.dat'
            output_folder = os.path.join(current_folder, simulation_subfolder,simulation_subsubfolder)
            if not os.path.exists(output_folder):
                os.makedirs(output_folder)
            run_simulation_four_pops(n, L, theta, D1, D2, D3,length_bottleneck,size_bottleneck, output_folder)
            distance_file = os.path.join(output_folder,"all_extrapolated_distances.txt")
            distances = np.loadtxt(distance_file)
            distance1 = np.mean(distances[:, 0])
            distance2 = np.mean(distances[:, 1])
            distance3 = np.mean(distances[:, 2])
            summary_file.write(f'{distance1} {distance2}  {distance3} \n')
            summary_file.flush()
            distance_file = os.path.join(output_folder,"all_extrapolated_effective_size.txt")
            distances = np.loadtxt(distance_file)
            distance1 = np.mean(distances[:, 1])
            distance2 = np.mean(distances[:, 2])
            distance3 = np.mean(distances[:, 3])
            within_summary.write(f'{distance1} {distance2}  {distance3} \n')
            within_summary.flush()
        summary_file.close()
        within_summary.close()

