#!/usr/bin/env python
## AUTHOR: Eric Fontanillas
## LAST VERSION: 14/08/14 by Julie BAFFARD

MINIMUM_LENGTH = 1    #bp


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
            fasta_name_query = next2[:-1]
            next3 = F2.readline()
            fasta_seq_query = next3[:-1]
            next3 = F2.readline()    ## jump one empty line (if any after the sequence)
            fasta_name_match = next3[:-1]
            next3 = F2.readline()
            fasta_seq_match = next3[:-1]
            pairwise = [fasta_name_query,fasta_seq_query,fasta_name_match,fasta_seq_match]
            
            ## ADD pairwise with condition
            list_pairwises.append(pairwise)
    F2.close()

    return(list_pairwises)
##############################################

#################################
##### DEF2 : Extract length #####
#################################
def extract_length(length_string):   # format length string = 57...902
    l3 = string.split(length_string, "...")
    n1 = string.atoi(l3[0])
    n2 = string.atoi(l3[1])
    length = n2-n1

    return(length)
##############################################


####################################
##### DEF3 : Remove Redondancy ##### 
####################################
def filter_redondancy_and_length(list_paireu, MIN_LENGTH):
    
    bash1 = {}
    list_pairout = []
    
    for pair in list_paireu:
         query_name = pair[0]
         query_seq = pair[1]
         match_name = pair[2]
         match_seq = pair[3]

         l1 = string.split(query_name, "||")
         short_query_name = l1[0][1:]
         length_matched =  extract_length(l1[1])               ### DEF2 ###
         l2 = string.split(match_name, "||")
         short_match_name = l2[0][1:]
         binom = "%s_%s" %(short_query_name, short_match_name)

         ## TEST FOR REDONDANCY
         ## REDONDANCY OF BINOME!!!! => MATCHE BETWEEN THE SAME 2 CONTIGS, BUT AT DIFFERENT POSITIONS ON THE CONTIG
         ## REDONDANCY NOT REMOVED HERE:
         ## 1/ Several "TERA" match with one "APN"  (Counted in script "09_formatMatch_getBackNucleotides.py")
         ## 2/ Several "APN" match with one "TERA" (Counted
         if binom not in bash1.keys():
             bash1[binom] = [query_name, query_seq, match_name, match_seq, length_matched]
         else:
             old_length = bash1[binom][-1]
             if length_matched > old_length:
                 bash1[binom] = [query_name, query_seq, match_name, match_seq, length_matched]

    
    for bino in bash1.keys():
        length = bash1[bino][-1]
        if length > MIN_LENGTH:
            list_pairout.append(bash1[bino])

    return(list_pairout)
##############################################


#######################
##### RUN RUN RUN #####
#######################
import string, os, time, re, sys

## 1 ## INPUT/OUTPUT
SHORT_FILE = sys.argv[1] #short-name-query_short-name-db

F_IN = "%s/06_PairwiseMatch_%s.fasta" %(SHORT_FILE, SHORT_FILE) 

F_OUT = "%s/09_PairwiseMatch_filtered_%s.fasta" %(SHORT_FILE, SHORT_FILE) 
File_OUT = open(F_OUT, "w")

F_OUT2 = "%s/09_onlyMatch_filtered_%s.fasta" %(SHORT_FILE, SHORT_FILE) 
File_OUT2 = open(F_OUT2, "w")

## 2 ## RUN
list_pairwises = get_pairs(F_IN)           ### DEF1 ###
list_pairwises_filtered1 = filter_redondancy_and_length(list_pairwises, MINIMUM_LENGTH)                ### DEF3 ###

i = 0
for pair in list_pairwises_filtered1:
     i = i+1

     ## Write pairwise alignment
     File_OUT.write("%s\n" %pair[0])
     File_OUT.write("%s\n" %pair[1])
     File_OUT.write("%s\n" %pair[2])
     File_OUT.write("%s\n" %pair[3])

     ## Write only "matches" [AND UNGAP THEM: needed before the 2nd run of blast]
     File_OUT2.write("%s\n" %pair[2])
     seq_match = pair[3]
     seq_match_ungapped = string.replace(seq_match, "-", "")
     File_OUT2.write("%s\n" %seq_match_ungapped)
    
File_OUT.close()
File_OUT2.close()
