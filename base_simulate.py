#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 20 17:03:27 2017

@author: ivan
"""

from subprocess import Popen, PIPE
import sys
import os



folder = sys.argv[1] # folder should exist. its currently created by job_sim.sh

scrm_file_raw_result = os.path.join(folder, '_tmp_out.txt')
scrm_file_clean_result = os.path.join(folder, '_tmp_res.txt')
scrm_file_seed = os.path.join(folder, '_tmp_seed.txt')
file_fake_labs = os.path.join(folder, 'fake_labs.txt')
scrm_exec = sys.argv[2]

def run_scrm(scrm_command: str):
    with open(os.path.join(folder, 'scrm_command.txt'), 'w') as f:
        f.write(scrm_command)
    scrm = Popen(scrm_command.split(' '), stdout=PIPE)
    grep = Popen(['grep',  rb'^[0-9]*$'], stdin=scrm.stdout, stdout=PIPE)
    scrm.stdout.close()
    output = grep.communicate()
    data = output[0].decode('utf-8')

    # get the data from scrm, incl seed
    with open(scrm_file_raw_result, 'w') as f:
        f.write(data)

def transcode_scrm(n: int):
    trans = Popen(f'python transcode.py {scrm_file_raw_result} {scrm_file_clean_result} {scrm_file_seed} {n}'.split(' '),
                  stdout=sys.stdout)
    trans.communicate()

    #read and write the seed
    with open(scrm_file_seed, 'r') as f:
        seed = f.read().strip()
    with open(os.path.join(folder, FNAME), 'a') as f:
        f.write(f'{seed}')

def create_fake_label(filename_labels: str, population_sizes: List[int])->None:
    with open(filename_labels, 'w') as f:
        for population_size in population_sizes:
            for _ in population_size:
                f.write(f'pop{population_index}\n')


def run_medeas():
    medeas = Popen(['python','main.py',
                    '-asd', '-analyze', folder, FNAME])
    medeas.communicate()

run_medeas()
