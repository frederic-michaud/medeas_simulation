#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 20 17:03:27 2017

@author: ivan
"""

medeas_exec = "/Users/fmichaud/PycharmProjects/medeas/main.py"

from subprocess import Popen
import sys

def run_medeas(medeas_exec: str,
                snip_file: str,
               label_file: str,
               output_folder: str,
               K: int,
               bootsize: int,
               outgroup: str
               ):

    command = " ".join(['python',medeas_exec,
                    '--simulation',
                    ' -sf', snip_file,
                    '-lf',label_file,
                    '--output_folder',output_folder,
                    '-K',K,
                    '-bws', bootsize,
                    '-bsn','100'
                    ])
    print(command)
    medeas = Popen(command.split())
    medeas.communicate()

snip_file = sys.argv[1]
label_file = sys.argv[2]
output_folder = sys.argv[3]
K = 0
bootsize = 10
outgroup = "pop0 pop1"
if len(sys.argv) > 4:
    K = sys.argv[4]
if len(sys.argv) > 5:
    bootsize = sys.argv[5]

run_medeas(medeas_exec,snip_file, label_file,output_folder,K,bootsize,outgroup)
