#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 13 17:03:27 2018

@author: Frederic
"""

from subprocess import Popen

folder = "hello"
def run_simulation_two_pops(n1: int, n2: int, L: int, theta: float, D: float):
    # run scrm  for simulations
    scrm_command = f'{n1+n2} {L} -t {theta} -I 2 {n1} {n2} -ej {D} 1 2 --print-model -l -1 -L'
    run_scrm = Popen(['python','/Users/fmichaud/PycharmProjects/medeas_simulations/run_scrm.py',  scrm_command,folder])
    run_scrm.communicate()

    snip_file = '/Users/fmichaud/PycharmProjects/medeas_simulations/two_population/hello/output.txt'
    transcode = Popen(['python','/Users/fmichaud/PycharmProjects/medeas_simulations/transcode.py', "hello/_tmp_out.txt", snip_file,str(n1+n2)])
    transcode.communicate()

    label_file = '/Users/fmichaud/PycharmProjects/medeas_simulations/two_population/hello/fake_labs.txt'
    command = " ".join(['python', '/Users/fmichaud/PycharmProjects/medeas_simulations/create_fake_labels.py', '-of', label_file, '-ps', str(n1), str(n2)])
    print(command)
    create_label = Popen(command.split())
    create_label.communicate()



    output_folder = '/Users/fmichaud/PycharmProjects/medeas_simulations/two_population/hello/'
    transcode = Popen(['python','/Users/fmichaud/PycharmProjects/medeas_simulations/run_medeas.py', snip_file,label_file,output_folder])
    transcode.communicate()

Ls = [2000]
D = 0.2
for L in Ls:
    run_simulation_two_pops(25, 25, int(L), 2, D)