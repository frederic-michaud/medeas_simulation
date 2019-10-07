#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 13 17:03:27 2018

@author: Frederic
"""

from subprocess import Popen
import os
import numpy as np


# We consider population the following tree ((1,2),((3,4),(5,6))) where 1 & 2 are african, (3,4) could be asian and (5,6) european.
# (1,2) don't go through a bottleneck but 3,4,5,6 do. We will also consider that the split time between 5 and 6 is lower
# than the split time between 4 and 3.

D_deepest = 0.3
D_africa = 0.05
D_europe = 0.018
D_europe_asia = 0.15
D_asia = 0.025
length_bottleneck = 0.01


def run_simulation_four_pops(n: int, L: int, theta: float, size_bottleneck: float, output_folder: str):

    current_folder = os.path.dirname(os.path.realpath(__file__))
    script_folder = os.path.split(current_folder)[0]

    scrm_result = os.path.join(output_folder,'scrm.txt')
    location_run_scrm = os.path.join(script_folder, "run_scrm.py")
    #-en < t > < i > < n >: Set the size of population i to n * N0 at time t.
    # -ej < t > < j > < i >: Adds a specialization event in population i that creates population j
    scrm_command = f'{6*n} {L} -t {theta} -I 6 {n} {n} {n} {n} {n} {n} \
-ej {D_deepest} 3 1 \
-ej {D_africa} 2 1 \
-ej {D_europe_asia} 5 3 \
-ej {D_europe} 6 5 \
-ej {D_asia} 4 3 \
-en {D_deepest-length_bottleneck} 3 {size_bottleneck} \
--print-model -l -1 -L'
    run_scrm = Popen(['python', location_run_scrm, scrm_command, scrm_result])
    run_scrm.communicate()

    snip_file = os.path.join(output_folder,'snip.txt')
    location_transcode = os.path.join(script_folder, "transcode.py")
    transcode_commande = f'python {location_transcode} {scrm_result} {snip_file} {6*n}'
    print(transcode_commande)
    transcode = Popen(transcode_commande.split())
    transcode.communicate()

    location_create_fake_label = os.path.join(script_folder, "create_fake_labels.py")
    label_file = os.path.join(output_folder,'fake_labs.txt')
    fake_label_command = " ".join(['python', location_create_fake_label, '-of', label_file, '-ps', str(n), str(n), str(n), str(n), str(n), str(n)])
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
Ls = [100000] #regulary space with 4 point between each order of magnitude

size_bottlenecks = [0.02]

n = 20
theta = 3
sample_size = 1
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
            run_simulation_four_pops(n, L, theta, size_bottleneck, output_folder)
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

