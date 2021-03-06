#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 13 17:03:27 2018

@author: Frederic
"""

from subprocess import Popen
import os
import numpy as np
import sys

def run_simulation_two_pops(n1: int, n2: int, L: int, theta: float, D: float,output_folder):

    current_folder = os.path.dirname(os.path.realpath(__file__))
    script_folder = os.path.split(current_folder)[0]

    scrm_result = os.path.join(output_folder,'scrm.txt')
    location_run_scrm = os.path.join(script_folder, "run_scrm.py")
    scrm_command = f'{n1+n2} {L} -t {theta} -I 2 {n1} {n2} -ej {D} 1 2 --print-model -l -1 -L'
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


L = sys.argv[1]
D = sys.argv[2]

current_folder = os.path.dirname(os.path.realpath(__file__))
simulation_subfolder = "convergence_given_parameter"
result_subfolder_fullpath = os.path.join(current_folder,simulation_subfolder)


distance_summary_file = os.path.join(result_subfolder_fullpath,f'L_{L}_D_{D}.dat')


simulation_subsubfolder = f'L_{L}_D_{D}'

output_folder = os.path.join(current_folder, simulation_subfolder,simulation_subsubfolder)
if not os.path.exists(output_folder):
    os.makedirs(output_folder)
n1 = 20
n2 = 20
run_simulation_two_pops(n1, n2, int(L), 2, float(D),output_folder)


