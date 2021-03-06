#!/usr/bin/python

## Author: Eric FONTANILLAS
## Date: 21.12.10
## Object: Test for compositional bias in genome and proteome as marker of thermal adaptation (comparison between 2 "hot" species: Ap and Ps and one "cold" species: Pg)

#############
### DEF 0 ###
#############
def simplify_fasta_name(fasta_name):
    L=["Ap", "Ac", "Ps", "Pf", "Pg", "Pp"]

    for abbreviation in L:
        if abbreviation in fasta_name:
            new_fasta_name = abbreviation

    return(new_fasta_name)
##########################################

###########
## DEF1 ##
###########
## Generates bash, with key = fasta name; value = sequence (WITH GAP, IF ANY, REMOVED IN THIS FUNCTION)

def dico(fasta_file):

    count_fastaName=0
    F1 = open(fasta_file, "r")
    
    bash1 = {}
    while 1:
        nextline = F1.readline()
        #print nextline
        if not nextline :
            break
        
        if nextline[0] == ">":
            count_fastaName = count_fastaName + 1
            fasta_name = nextline[1:-1]
            nextline = F1.readline()
            sequence = nextline[:-1]
            
            if fasta_name not in bash1.keys():
                fasta_name = simplify_fasta_name(fasta_name)  ### DEF 0 ###
                bash1[fasta_name] = sequence
            else:
                print fasta_name

    # Find alignment length
    kk = bash1.keys()
    key0 = kk[0]
    seq0 = bash1[key0]
    ln_seq = len(seq0)

    F1.close()
    
    return(bash1)
#####################################



##################
###### DEF2 ######
##################
def base_composition(seq):
      count_A=string.count(seq, "A") + string.count(seq, "a")
      count_T=string.count(seq, "T") + string.count(seq, "t")
      count_C=string.count(seq, "C") + string.count(seq, "c")
      count_G=string.count(seq, "G") + string.count(seq, "g")


      CG = count_C+count_G
      AT = count_T+count_A
      
      AG = count_A+count_G
      TC = count_T+count_C

      ## 1 ## Search for compositional bias in genome as marker of thermal adaptation: CG vs AT
      ratio_CG_AT = float(CG)/float(AT)
      percent_CG = float(CG)/(float(AT) + float(CG))*100
      
      ## 2 ## Search for compositional bias in genome as marker of thermal adaptation: AG vs TC
      ratio_purine_pyrimidine=float(AG)/float(TC)
      percent_purine=float(AG)/(float(AG)+float(TC))*100      
      
      ## 3 ## Nucleotide proportions
      ln = len(seq)
      prop_A = float(count_A)/float(ln)
      prop_T = float(count_T)/float(ln)
      prop_C = float(count_C)/float(ln)
      prop_G = float(count_G)/float(ln)
      
      return(percent_CG, percent_purine, prop_A, prop_T, prop_C, prop_G)
##############################################

##################
###### DEF3 ######
##################
def purine_loading(seq):
      count_A=string.count(seq, "A") + string.count(seq, "a")
      count_T=string.count(seq, "T") + string.count(seq, "t")
      count_C=string.count(seq, "C") + string.count(seq, "c")
      count_G=string.count(seq, "G") + string.count(seq, "g")
      
      TOTAL = count_C+count_G+count_T+count_A

      ## PLI : Purine loading indice (Forsdyke et al.)
      # (G-C)/N * 1000 et (A-T)/N * 1000
      
      DIFF_GC = count_G - count_C
      DIFF_AT = count_A - count_T

      # Per bp
      PLI_GC = float(DIFF_GC)/float(TOTAL)
      PLI_AT = float(DIFF_AT)/float(TOTAL)
      
      # Per 1000 bp
      PLI_GC_1000 = PLI_GC*1000
      PLI_AT_1000 = PLI_AT*1000

      return(TOTAL, DIFF_GC, DIFF_AT,PLI_GC,PLI_AT,PLI_GC_1000,PLI_AT_1000)
##############################################

###################
### RUN RUN RUN ###
###################
import string, os


## 1 ## List taxa
LT = ["Ap","Ac","Pg","Pf","Ps", "Pp"]

## 2 ## PathIN
fileIN_properties = open("01_AminoAcid_Properties2.csv", "r")

#Path_IN_loci_NUC = "/home/umr7144/game/efontanillas/efontanillas_on_projet/20_NGS_assemblages/ILLUMINA_Alvinellidae_BranchHarborNYC/06_Get_Orthologs_on_N77_TBLASTX_with_Ps_from_clusters/script/05_GetLocusOrtholog_plus_alignwithBLASTALIGN_plus_checkwithPRANK/09_FILTER2/06_CDS_with_M_fromDataset_min50aa/02_CDS_No_Missing_Data_nuc"
Path_IN_loci_NUC = "./00_Concatenation_AllSites"
Lloci_NUC = os.listdir(Path_IN_loci_NUC)

# Path_IN_loci_AA = "02_CDS_No_Missing_Data_aa_CDS_withM"
# Lloci_AA = os.listdir(Path_IN_loci_AA)

## 3 ## PathOUT
## 3.1 ## NUC composition
fileOUT_NUC=open("10_nuc_compositions.csv","w")
fileOUT_NUC.write("LOCUS,")
for taxa in LT:
    fileOUT_NUC.write("%s_prop_A,%s_prop_T,%s_prop_C,%s_prop_G," %(taxa,taxa,taxa,taxa))
fileOUT_NUC.write("\n")

## 3.2 ## NUC percent_GC
fileOUT_percent_GC=open("11_percent_GC.csv","w")
fileOUT_percent_GC.write("LOCUS,")
for taxa in LT:
    fileOUT_percent_GC.write("%s_percent_GC," %(taxa))
fileOUT_percent_GC.write("\n")

## 3.3 ## NUC percent_purine
fileOUT_percent_purine=open("12_percent_purine.csv","w")
fileOUT_percent_purine.write("LOCUS,")
for taxa in LT:
    fileOUT_percent_purine.write("%s_percent_purine," %(taxa))
fileOUT_percent_purine.write("\n")

## 3.4 ## Purine Load
fileOUT_Purine_Load=open("12_Purine_Load_Indice.csv", "w")
fileOUT_Purine_Load.write("LOCUS,")
for taxa in LT:
    fileOUT_Purine_Load.write("%s_TOTAL,%s_DIFF_GC,%s_DIFF_AT,%s_PLI_GC1000,%s_PLI_AT1000," %(taxa,taxa,taxa,taxa,taxa))
fileOUT_Purine_Load.write("\n")

#####################
## 4 ## Process Loci
#####################
for locus in Lloci_NUC:
    print locus
    path_locus = "%s/%s" %(Path_IN_loci_NUC, locus)
    bash = dico(path_locus)

    fileOUT_NUC.write("%s," %locus)
    fileOUT_percent_GC.write("%s," %locus)
    fileOUT_percent_purine.write("%s," %locus)
    fileOUT_Purine_Load.write("%s," %locus)
    #print bash
    for taxa in LT:
        seq = bash[taxa]
        percent_GC, percent_purine,prop_A, prop_T, prop_C, prop_G = base_composition(seq)   ### DEF2 ###
        TOTAL, DIFF_GC, DIFF_AT,PLI_GC,PLI_AT,PLI_GC_1000,PLI_AT_1000 = purine_loading(seq) ### DEF3 ###
        fileOUT_NUC.write("%.5f,%.5f,%.5f,%.5f," %(prop_A,prop_T,prop_C,prop_G))
        fileOUT_percent_GC.write("%.5f," %percent_GC)
        fileOUT_percent_purine.write("%.5f," %percent_purine)
        fileOUT_Purine_Load.write("%d,%d,%d,%.5f,%.5f," %(TOTAL, DIFF_GC, DIFF_AT,PLI_GC_1000, PLI_AT_1000))
    fileOUT_NUC.write("\n")
    fileOUT_percent_GC.write("\n")
    fileOUT_percent_purine.write("\n")
    fileOUT_Purine_Load.write("\n")
fileOUT_NUC.close()
fileOUT_percent_GC.close()
fileOUT_percent_purine.close()
fileOUT_Purine_Load.close()
