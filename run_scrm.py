#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 20 17:03:27 2017

@author: ivan
"""

import sys
import os
from subprocess import Popen, PIPE


scrm_command = sys.argv[1]
scrm_file_raw_result = sys.argv[2]

def run_scrm(scrm_command: str):
    scrm_exec = "scrm"
    full_command = scrm_exec + " " + scrm_command
    print(full_command)
    scrm = Popen(full_command.split(' '), stdout=PIPE)
    grep = Popen(['grep',  rb'^[0-9]*$'], stdin=scrm.stdout, stdout=PIPE)
    scrm.stdout.close()
    output = grep.communicate()
    data = output[0].decode('utf-8')

    # get the data from scrm, incl seed
    with open(scrm_file_raw_result, 'w') as f:
        f.write(data)

run_scrm(scrm_command)