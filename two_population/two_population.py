#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 13 17:03:27 2018

@author: Frederic
"""
import ...
def run_simulation_two_pops(n1: int, n2: int, L: int, theta: float, D: float):
    # create fake labels because medeas needs that


    # run scrm  for simulations
    scrm_command = f'{scrm_exec} {n1+n2} {L} -t {theta} -I 2 {n1} {n2} -ej {D} 1 2 --print-model -l -1 -L'
    run_scrm(scrm_command)
    transcode_scrm(n1+n2)

if SIMULATION_CASE == 2:
    Ls = [2000]
    D = 8
    for L in Ls:
        run_simulation_two_pops(100, 100, int(L), 2, D)