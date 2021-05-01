#! /usr/bin/env python
import sys
import os
import pandas as pd
import collections
import re
#from Bio.PDB import *
import matplotlib.pyplot as plt
import numpy as np
import argparse

# Make a dictionary of mutation position and highest Kext at that position
#Requires at minimum to inputs. First is the metrics file which is a csv containing Mutation header in one column followed by mutations
#and metrics in another column with a header for the metric. Enter the header of the metric you want to analyze.
#Ex. 
def metric_dict(infile, column, pos):
    df = pd.read_csv(infile, sep=',', header=0, na_values = 'F')
    df['position'] = df[pos].apply(lambda x: re.sub("\D", "", x)).astype('int32')
    df = df.dropna()
    positions = df['position'].to_list()
    try:
        column_list = df[column].to_list()
    except KeyError as error:
        print(error)
        print("It doesn't look like \'%s\' is a header in your file. Please enter an appropriate metric header with -m flag"%column)
        sys.exit(1)
    
    pos_kext_tup = list(zip(positions, column_list))
    print(pos_kext_tup)
    d = collections.defaultdict(list)
    
    for k, v in pos_kext_tup:
        d[k].append(v)
    
    return d, df

def make_plots(df, column):
    ax1 = df.plot.scatter(x='position', y=column, c=column, colormap='seismic')    
    plt.legend()
    plt.savefig(infile[0:-4]+'_%s_scatter.png'%column)
    #plt.show()
    print(df[column])
            
def replace_B_factors(d, pdb, column, monomer_chain):
    #Make new dictionary with only maximum values for each position
    d_max = {}
    b_data = {}
    
    for position, fold_list in d.items():
        d_max[position] = max(fold_list)
    
    print('dmax:', d_max)
    df = pd.DataFrame.from_dict(d, orient = 'index').sort_index()
    df.to_csv(pdb[0:-4]+'_%s_grouped.csv'%column)

    #Replace B factor in text file file with Fold change. Assign -1 to positions that are not in the dictionary
    with open(pdb, 'r') as infile:
        with open(pdb[0:-4]+'_data_%s.txt'%column, 'w') as outfile:
            for line in infile:
                
                if line.startswith("ATOM"):
                    line = line.strip().split()
                    
                    if int(line[5]) in d_max.keys():
                        line[10] = d_max[int(line[5])]
                    
                    else:
                        line[10] = -1
                    
                    chain = line[4]
                    resn = line[3]
                    resi = line[5]
                    name = line[2]
                    b = line[10]
                    
                    if chain==monomer_chain:
                        line = [chain, resn, resi, name, b]
                        str_line = (' ').join([str(i) for i in line])
                        outfile.write(str_line+'\n')
                    #b_data.setdefault(chain, {})[resi] = (b, resn)
                    #print('b_data', b_data)
    return d_max, b_data
    

    #--CALL MAIN
if __name__=='__main__':
    
    #--COMMAND LINE ARGUMENTS
    parser = argparse.ArgumentParser()
    parser.add_argument("-p,", "--pdb", required='True', help="Enter the Protein PDB file")
    parser.add_argument("-f", "--filename", required='True', help="Enter the input csv file with metrics")
    parser.add_argument("-c", "--chain", default='A', help="Enter the molecule chain ID")
    parser.add_argument("-m", "--metric", default="Fold Kext", help="Enter the column name of metric you want to analyze")
    parser.add_argument("-l", "--mutation", default="Last_Mutation", help="Enter the header used for amino acid position column e.g. Last Mutation")
    args = parser.parse_args()
    pdb = args.pdb
    infile = args.filename
    chain = args.chain
    metric= args.metric
    position = args.mutation
    #infile = sys.argv[1]
    #pdb = sys.argv[2]
    
    #--CALL FUNCTIONS
    d, df = metric_dict(infile, column=metric, pos=position)
    make_plots(df, column=metric)
    replace_B_factors(d, pdb, column=metric, monomer_chain=chain)
   
   




            
    
    
    
    

