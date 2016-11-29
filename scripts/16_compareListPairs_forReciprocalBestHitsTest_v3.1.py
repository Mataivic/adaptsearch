#!/usr/bin/python
## AUTHOR: Eric Fontanillas
## LAST VERSION: 14/08/14 by Julie BAFFARD


## Blast Run 1 : 01_SOUTH_final_batchs_1-9_15858seq.assembly VS. 02_NORTH_gscope_24770seqAfterAssemblage_cap3.fas
## Blast Run 2 (RECIPROCAL) : 13_onlyMatch.fasta (= matches of Blast Run 1 + filtering) VS. 01_SOUTH_final_batchs_1-9_15858seq.assembly

## THIS SCRIPT WILL COMPARE THE TWO LISTS OF PAIR GENERATED BY THE 2 RECIPROCAL RUNS OF BLAST:
# 09_PairwiseNames_longName_filtered_300bp.csv
# 13_PairwiseNames_long_names.csv

MIN_LENGTH = 1

############################
##### DEF1 : Get Pairs #####
############################
def get_pairs(fasta_file_path):
    F2 = open(fasta_file_path, "r")
    list_pairwises = []
    while 1:
        next2 = F2.readline()
        if not next2:
            break
        if next2[0] == ">":
            fasta_name_query = next2[1:-1]
            next3 = F2.readline()
            fasta_seq_query = next3[:-1]
            next3 = F2.readline()    ## jump one empty line (if any after the sequence)
            fasta_name_match = next3[1:-1]
            next3 = F2.readline()
            fasta_seq_match = next3[:-1]
            pairwise = [fasta_name_query,fasta_seq_query,fasta_name_match,fasta_seq_match]
            
            ## ADD pairwise with condition
            list_pairwises.append(pairwise)
    F2.close()
    return(list_pairwises)
#########################################################


#################################
##### DEF2 : Get Short Name ##### 
#################################
def get_short_name(long_name):

    S1 = string.split(long_name, "||")
    S2 = string.split(S1[0], " ")

    short_name  = S2[0]
    
    
    return(short_name)
##########################################################


###################
### RUN RUN RUN ###
###################

import string, os, sys

### 1 ### INPUT/OUTPUT
SHORT_FILE = sys.argv[1] ## short-name-query_short-name-db

path_out = "%s/17_ReciprocalHits_%s.fasta" %(SHORT_FILE, SHORT_FILE) 
file_out = open(path_out, "w")

fasta_file_path1 = "%s/09_PairwiseMatch_filtered_%s.fasta" %(SHORT_FILE, SHORT_FILE) 
fasta_file_path2 = "%s/15_PairwiseMatch_filtered_%s.fasta" %(SHORT_FILE, SHORT_FILE) 

## 2 ## RUN
##Get pair of sequences (ALL PAIRS AVAILABLE BEFORE FILTERING FOR Best Reciprocal Hits)
list_pairwises1 = get_pairs(fasta_file_path1)     ### DEF1 ###
list_pairwises2 = get_pairs(fasta_file_path2)     ### DEF1 ###

ln1 = len(list_pairwises1)
ln2 = len(list_pairwises2)

### Detect reciprocal best hits (pairs)
list_overlapping_pairwises = []               ### Will content pair reciprocally found as Best Blastx HIT
i = 1
for pair in list_pairwises1:
    long_name_query1 = pair[0]
    short_name_query1 =  get_short_name(long_name_query1)        ### DEF2 ###

    long_name_match1 = pair[2]
    short_name_match1 =  get_short_name(long_name_match1)        ### DEF2 ###

    j = 0
    for pair2 in list_pairwises2:
        long_name_query2 = pair2[0]
        short_name_query2 =  get_short_name(long_name_query2)        ### DEF6 ###

        long_name_match2 = pair2[2]
        short_name_match2 =  get_short_name(long_name_match2)        ### DEF6 ###

        LLLL = [short_name_query2, short_name_match2]

        if short_name_query1 in LLLL and short_name_match1 in LLLL:
            j = j+1

    if j == 1:
        list_overlapping_pairwises.append(pair)      
    i = i+1   

### Print the output
for pair3 in list_overlapping_pairwises:
    file_out.write(">%s\n" % pair3[0])
    file_out.write("%s\n" % pair3[1])    
    file_out.write(">%s\n" % pair3[2])
    file_out.write("%s\n" % pair3[3])

file_out.close()
