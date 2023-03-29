#!/usr/bin/env python
# coding: utf-8

# In[37]:


import time, os
start=time.time()

# On stocke les données des fichiers dans des dictionnaires.

a=open("aliases-rno.tsv","r")
mir_MIMAT={}
for line in a:
    line=line[:-1].split("\t")
    MIMAT=line[0]
    mirID=line[1].split(";")
    for ID in mirID:
        mir_MIMAT[ID]=MIMAT   # Clé = ID miR -> Valeur= MIMAT

a.close()

b=open("ncbi-refseq-rno.tsv","r") 
refseq_gID={}
for line in b:
    line=line[:-1].split("\t")
    gID=line[0].strip()
    transID=line[1].strip()
    refseq_gID[transID]=gID  # Clé = ID transcrit -> Valeur= ID gène
b.close()



#Ces deux premiers dico vont nous permettre de relier les informations nécessaire à la création des fichiers finaux

f=open("predictions-rno.txt")
final=[] #Liste qui contiendra un dictionnaire {"MIMAT" , "gene ID", "score"} pour chaque gene.
        #Le format liste permettra de trier les dictionnaires par ordre décroissant de scores
for line in f:
    linecopy=line[:-1].split("\t")
    refseq=linecopy[1].strip()
    mirID=linecopy[0].strip()
    score=float(linecopy[2])
    if refseq not in refseq_gID.keys():  #On vérifie que le transcrit est associé à un ID de gène
        gID="missing-gene"
        
    else:
        gID=refseq_gID[refseq]
        
    if mirID not in mir_MIMAT.keys(): #On vérifie que le miR est associé à un MIMAT
        mimat="missing-mimat"
        print(mirID)
    else:
        mimat=mir_MIMAT[mirID]
    dico_ligne={"MIMAT":mimat, "gID":gID, "score":score}
    final.append(dico_ligne)
f.close()

final.sort(key=lambda x: x.get('score'), reverse=True)  #On trie les dictionnaires par score décroissant



misg=[]  #Liste pour les transcrits sans ID de gène
dic_final={}   #Dictionnaire : Clé=MIMAT -> Valeur= Liste des lignes à écrire dans le fichier (ID gène et Score)
for dic in final:
    if dic["gID"]=="missing-gene":
        misg.append("{}\t{}\n".format(dic["MIMAT"],dic["score"]))
    else:
        if dic["MIMAT"] not in dic_final.keys():
            dic_final[dic["MIMAT"]]=["{}\t{}\n".format(dic["gID"],dic["score"])]
        else:
            dic_final[dic["MIMAT"]].append("{}\t{}\n".format(dic["gID"],dic["score"]))

            
            
# Création d'un répertoire "output"

dirName="Output"
print("Creating new directory: "+ dirName)
if not os.path.exists(dirName):
    os.mkdir(dirName)
    print("Directory '" , dirName ,  "' Created ")
else:    
    print("Directory '" , dirName ,  "' already exists")          
    
    
    
#Création du fichier "missing-gene"

print("Looking for transcripts without genes ID...")
if len(misg)>0: 
    with open("Output/missing-genes.txt", "w") as file:
        file.write((",".join(misg)).replace(",",""))
    print("\t"+str(len(misg))+" transcripts found without genes ID.'missing-genes.txt' file created.")
else:
    print("\t 0 transcript was found without gene ID.")

    
    
#Création des fichiers MIMAT

count=0 #Compteur pour connaître le nombre de fichier MIMAT créés
for mim in dic_final.keys():
    count+=1
    nomfichier="Output/{}.txt".format(mim)
    with open(nomfichier,"w") as file:
        file.write((",".join(dic_final[mim])).replace(",",""))
        
#Vérification de l'existence de miARN sans MIMAT

print("Looking for miARN without MIMAT...")
if ("missing-mimat" in dic_final.keys()):
    missing=len(dic_final["missing-mimat"])
    print("\t"+str(missing)+" miARN found without MIMAT.'missing-mimat.txt' file created." )
    count=count-1
else:
    print("\t 0 miARN was found without MIMAT.")

#Résultats finaux
end=time.time()
print("Results: \n \t"+str(count)+" MIMAT files have been created \n \t"+ str(end-start)+ " seconds to process")

