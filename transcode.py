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
def transcode(infile: str, outfile: str, nb_individual: int,nb_remove: int):
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
        count_loci = 0
        for locus in loci:
            #for snp in range(len(locus[0])):
            snp = 0
            listsnp = [locus[individual][snp] for individual in range(nb_individual)]
            listint = list(map(int, listsnp))
            nb_polymorphism = sum(listint)
            #if nb_polymorphism > 5 and nb_polymorphism < 20: #always true, but allow to remove singleton or doublon easly
            if nb_polymorphism > nb_remove:
                count_loci = count_loci + 1
                for individual in range(nb_individual):
                    s = locus[individual][snp]
                    f.write(str(int(s) + 1))
                    if individual < nb_individual - 1:
                        f.write(' ')
                f.write('\n')
    print(f'nb of polymorph loci: {count_loci}')

infile = sys.argv[1]
outfile = sys.argv[2]
nb_individual = int(sys.argv[3])
if len(sys.argv) > 4:
    maf = float(sys.argv[4])
    nb_remove = int(maf * nb_individual)
else:
    nb_remove = 0
transcode(infile, outfile, nb_individual, nb_remove)