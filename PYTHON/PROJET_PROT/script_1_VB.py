#!/usr/bin/env python
# coding: utf-8

# In[1]:


"""
Ce script permet l'obtention de fichiers mgf à partir du fasta "requête" et du multifasta "base de données". Les mgf
de la base de données sont stockés dans un dossier "Database" généré par le script

Le script est à lancer sans argument. Le nom des deux fichiers d'entrée sont à renseigner après avoir lancé le script.
"""

import re, time, os

score={
"A":71.037114,
"C":103.009184,
"D":115.026943,
"E":129.0593,
"F":147.068414,
"G" :57.021464,
"H" :137.058912,
"I" : 113.084064,
"K" : 128.094963,
"L" : 113.084064,
"M" : 131.040485,
"N":  114.042927,
"P" : 97.052764,
"Q" :128.058578,
"R" :156.101111,
"S" : 87.032028,
"T": 101.047678,
"V": 99.068414,
"W": 186.079313,
"Y" : 163.063329}


bdd=input("Entrer fichier .multifasta (base de données)")
req=input("Entrer un fichier .fasta (requête)")

# 1.a) Traitement du multifasta (base de données)

dic_raw_bdd={}


with open(bdd, "r") as f:
    for line in f:
        if re.match(">", line):
            name=line[2:-1]
            dic_raw_bdd[name]=""
        else:
            dic_raw_bdd[name]+=line[:-1]

dic_dig_bdd={}

for cle in dic_raw_bdd.keys():
	seq=dic_raw_bdd[cle]
	dic_dig_bdd[cle]={}
	s=0
	n=1
	for i in range(len(seq)-1):
		if ((seq[i]=="R") or ((seq[i]=="K") and (seq[i+1]!="P"))):
			name="peptide {}".format(n)
			dic_dig_bdd[cle][name]=seq[s:i+1]
			n+=1
			s=i+1
	name="peptide {}".format(n)
	dic_dig_bdd[cle][name]=seq[s:len(seq)+1]
			

dic_bdd_mgf={}

for cle in dic_dig_bdd:
    mass_list=[]
    for pep in dic_dig_bdd[cle].keys():
        seq=dic_dig_bdd[cle][pep]
        mass=0
        for aa in seq:
            mass+=score[aa]
        mass_list.append(mass)
    mass_list.sort()
    dic_bdd_mgf[cle]=mass_list

    # Création d'un répertoire "Database"

dirName="Database"
print("Creating new directory: "+ dirName)
if not os.path.exists(dirName):
    os.mkdir(dirName)
    print("Directory '" , dirName ,  "' Created ")
else:    
    print("Directory '" , dirName ,  "' already exists")          

for prot in dic_bdd_mgf.keys():
    
    filename="Database/{}.mgf".format(prot)
    filename=filename.replace(" ", "_")

    with open(filename,"w") as f:
        f.write("COM={}\n".format(prot))
        for mass in dic_bdd_mgf[prot]:
            w_mass="{:.6f}".format(mass)
            f.write("{}\n".format(w_mass))
        print(filename, "file has been created")
        
# 1.b) Traitement du fichier "requête"
req="exemple_1.fasta"

raw_req=""

with open(req, "r") as f:
    for line in f:
        if not re.match(">", line):
            raw_req+=line[:-1]



dig_req=[]

s=0
for i in range(len(raw_req)-1):
    if ((raw_req[i]=="R") or ((raw_req[i]=="K") and (raw_req[i+1]!="P"))):
        dig_req.append(raw_req[s:i+1])
        s=i+1
dig_req.append(raw_req[s:len(raw_req)+1])
    

mgf_req=[]

for pep in dig_req:
    mass=0
    for aa in pep:
        mass+=score[aa]
    mgf_req.append(mass)

mgf_req.sort()


name=req[:-6]
filename="{}.mgf".format(name)

with open(filename,"w") as f:
    f.write("COM={}\n".format(name))
    for mass in mgf_req:
        w_mass="{:.6f}".format(mass)
        f.write("{}\n".format(w_mass))
    print(filename, "file has been created")

