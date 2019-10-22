#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 13 17:03:27 2018

@author: Frederic
"""

from subprocess import Popen
import subprocess
import os
import numpy as np
import pickle
import matplotlib.pyplot as plt

def run_simulation_single_pop(n: int, L: int, theta: float, output_folder: str):

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
    nb_boot_window = 100
    bootwindow = int(L/nb_boot_window)
    command = " ".join(['python',location_run_medeas, snip_file,label_file,output_folder,str(bootwindow)])
    print(command)
    medeas = Popen(command.split(),stdout=subprocess.PIPE)
    output = medeas.communicate()
    return(output[0])



current_folder = os.path.dirname(os.path.realpath(__file__))
nb_replicate = 1
simulation_subfolder = "panmictic_pop"
L = 1000000
theta = 2

ns = np.concatenate((np.arange(4,10),np.arange(10,101,10)))

print(ns)
all_mean_distance = []
all_std_distance = []
all_expected_distance = []
for n in ns:
    simulation_subsubfolder = f'n_{n}'
    output_folder = os.path.join(current_folder, simulation_subfolder, simulation_subsubfolder)
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    run_simulation_single_pop(n, L, theta, output_folder)
    dist = pickle.load(open(os.path.join(output_folder,"asd_matrices","p1.asd.data"),"rb"))
    all_valide_dist = dist[np.tril_indices(4,-1)] # We take only 6 elements in the upper corner so that we don't have
    #different sampling scheme for different n. We don't use all the info at end.
    T = 2*np.sum(1/np.arange(1,n))
    print(all_valide_dist)
    print(f"mean value: {np.mean(all_valide_dist)} \n sigma: {np.std(all_valide_dist)} \n expected value: {2/T}")
    all_mean_distance.append(np.mean(all_valide_dist))
    all_std_distance.append(np.std(all_valide_dist))
    all_expected_distance.append(2/T)
with open("final_result.txt","w") as f:
    f.write(" ".join(map(str,ns)))
    f.write(" ".join(map(str,all_mean_distance)))
    f.write(" ".join(map(str,all_std_distance)))
    f.write(" ".join(map(str,all_expected_distance)))
with open("final_result.dat","wb") as f:
    pickle.dump((ns,all_mean_distance,all_std_distance,all_expected_distance),f)
