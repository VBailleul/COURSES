#!/usr/bin/python3
# -*- coding : uft-8 -*-
import requests
from requests.adapters import HTTPAdapter, Retry

def interpro(uniprot_ids):
    ipr_list = []
    links = []
    for uniprot_id in uniprot_ids:
        s = requests.Session()

        retries = Retry(total=5,
                    backoff_factor=0.1,
                    status_forcelist=[400, 500, 502, 503, 504 ])


        s.mount('http://', HTTPAdapter(max_retries=retries))
        server = "https://www.ebi.ac.uk/interpro/api/"
        ext = "/entry/interpro/protein/uniprot/"+str(uniprot_id)
        r = s.get(server+ext)
        # Check si le retour est valide
        jason = True
        try:
            res = r.json()
        except:
            jason = False
        # Si le retour est valide ajoute les IPRs correspondant aux protéines si ils ne sont pas déjà dans la liste
        if jason == True:
            res = r.json()
            for i in range(len(res['results'])):
                if res['results'][i]['metadata']['accession'] not in ipr_list:
                    ipr_list.append(res['results'][i]['metadata']['accession'])
        links.append('https://www.ebi.ac.uk/interpro/protein/' +
                     str(uniprot_id)+'/')
    return (ipr_list, links)
