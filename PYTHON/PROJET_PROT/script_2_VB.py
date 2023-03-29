#!/usr/bin/env python
# coding: utf-8

# In[1]:


"""
Ce script permet l'obtention du meilleur match entre les masses présentes dans le fichier .mgf de la protéine requête et
celles des protéines de la base de données.

Ce script est à utiliser après avoir généré les fichiers mgf nécessaires à l'aide du script 1.

Le script est à lancer sans argument. Le nom du fichier .mgf à comparer à la base de données est à renseigner après avoir
le script.
"""


import re, os

#2 Trouver le meilleur match entre la requête et la bdd

#2.a def fonction de comparaison

def hits(a,b, erreur=0):
    a.sort()
    b.sort()
    hit=0
    for i in a:
        b=list(filter(lambda x : (x>= (i-erreur)), b))
        for t in b:
            if ((t-erreur)<=i) and (i<=(t+erreur)):
                hit+=1

    return (hit)

#2.b importer mgf requête

req=input("Entrer un fichier .mgf (requête):  ")
mgf_req=[]

with open(req,"r") as f:
    for line in f:
        if re.match("\d", line):
            mgf_req.append(float(line[:-1]))


top=0
mgf_top={}

for fileName in os.listdir("Database"):
    mgf_bdd=[]
    if (fileName != ".ipynb_checkpoints"):
        name="Database/{}".format(fileName)
        with open(name,"r") as f:
            for line in f:
                if re.match("\d", line):
                    mgf_bdd.append(float(line[:-1]))
        match= hits(mgf_req, mgf_bdd)
        if (match > top) :
            top=match
            mgf_top={}
            mgf_top[fileName]= mgf_bdd
        elif (match == top):
            mgf_top[fileName]= mgf_bdd

print("Avec un total de {} hits, ce(s) fichier(s) a (ont) le plus de hits avec le fichier requête: ".format(top))
for name in mgf_top.keys():
    print(name, " : ", mgf_top[name])

