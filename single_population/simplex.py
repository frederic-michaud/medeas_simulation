#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 13 17:03:27 2018

@author: Frederic
"""

from subprocess import Popen
import os
import numpy as np


def run_simulation_single_pop(n: int, L: int, theta: float, output_folder):

    current_folder = os.path.dirname(os.path.realpath(__file__))
    script_folder = os.path.split(current_folder)[0]

    scrm_result = os.path.join(output_folder,'scrm.txt')
    location_run_scrm = os.path.join(script_folder, "run_scrm.py")
    scrm_command = f'{n} {L} -t {theta} --print-model -l -1 -L'
    run_scrm = Popen(['python', location_run_scrm, scrm_command, scrm_result])
    run_scrm.communicate()

    snip_file = os.path.join(output_folder,'snip.txt')
    location_transcode = os.path.join(script_folder, "transcode.py")
    transcode_commande = f'python {location_transcode} {scrm_result} {snip_file} {n}'
    print(transcode_commande)
    transcode = Popen(transcode_commande.split())
    transcode.communicate()

    location_create_fake_label = os.path.join(script_folder, "create_fake_labels.py")
    label_file = os.path.join(output_folder,'fake_labs.txt')
    fake_label_command = " ".join(['python', location_create_fake_label, '-of', label_file, '-ps', str(n)])
    print(fake_label_command)
    create_label = Popen(fake_label_command.split())
    create_label.communicate()

    location_run_medeas = os.path.join(script_folder, "run_medeas.py")
    K = 1
    nb_boot_window = 50
    bootwindow = int(L/nb_boot_window)
    command = " ".join(['python',location_run_medeas, snip_file,label_file,output_folder,str(K),str(bootwindow)])
    print(command)
    medeas = Popen(command.split())
    medeas.communicate()


Ls = [int(10**(i/4)) for i in range(12,13)] #regulary space with 4 point between each order of magnitude
Ls = [1000]
current_folder = os.path.dirname(os.path.realpath(__file__))
simulation_subfolder = "simplex"
for L in Ls:
    simulation_subsubfolder = f'L_{L}'
    output_folder = os.path.join(current_folder, simulation_subfolder,simulation_subsubfolder)
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    theta = 2
    n = 500
    run_simulation_single_pop(n, L, theta, output_folder)

