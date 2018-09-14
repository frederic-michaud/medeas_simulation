#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 19 12:11:31 2017

@author: ivan

This file generate files readable from medeas from files
 generated by scrm.
"""

import sys

# According to scrm, and we follow the convention here, a locus is
# a physical region which  might contain various snp.
def transcode(infile: str, outfile: str, nb_individual: int):
    print(f'n = {nb_individual}')
    with open(infile) as f:
        data = f.readlines()

    data = [d.strip() for d in data]
    data = [d for d in data[1:] if d]
    nb_loci = len(data) // nb_individual
    loci = [None] * nb_loci
    print(f'number of loci: {nb_loci}')

    for i in range(nb_loci):
        loci[i] = data[i * nb_individual:(i + 1) * nb_individual]

    with open(outfile, 'w') as f:
        for locus in loci:
            #for snp in range(len(locus[0])):
            for snp in range(1):
                for individual in range(nb_individual):
                    s = locus[individual][snp]
                    f.write(str(int(s) + 1))
                    if individual < nb_individual - 1:
                        f.write(' ')
                f.write('\n')

infile = sys.argv[1]
outfile = sys.argv[2]
nb_individual = sys.argv[3]
transcode(infile, outfile, int(nb_individual))