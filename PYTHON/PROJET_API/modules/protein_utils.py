import requests
from requests.adapters import HTTPAdapter, Retry
import sys
import numpy as np
import json


def get_uniprot_accession_and_full_name(gene: str, orga: str):
    requestURL = f"https://www.ebi.ac.uk/proteins/api/proteins?offset=0&size=100&gene={gene}&organism={orga}"
    s = requests.Session()

    retries = Retry(total=5,
                    backoff_factor=0.1,
                    status_forcelist=[400, 500, 502, 503, 504 ])

    s.mount('http://', HTTPAdapter(max_retries=retries))
    r = s.get(requestURL, headers={"Accept": "application/json"})                            # récupère les uniprot ID et full name à partir 
    if not r.ok:                                                                             # des couples gene organisme
        r.raise_for_status()
        sys.exit()

    decoded = r.json()
    ids_uniprot = list()
    fullnames_uniprot = list()
    for i in decoded:
        ids_uniprot.append(i["accession"])
        if "submittedName" in i["protein"]:
            fullnames_uniprot.append(i["protein"]["submittedName"][0]["fullName"]["value"]
                                     ) if i["protein"]["submittedName"][0]["fullName"]["value"] not in fullnames_uniprot else fullnames_uniprot
        elif "recommendedName" in i["protein"]:
            fullnames_uniprot.append(
                i["protein"]["recommendedName"]["fullName"]["value"]) if i["protein"]["recommendedName"]["fullName"]["value"] not in fullnames_uniprot else fullnames_uniprot
    if ids_uniprot == []:
        ids_uniprot = ["Data not found"]
    if fullnames_uniprot == []:
        fullnames_uniprot = ["Data not Found"]
    return ids_uniprot, fullnames_uniprot


def get_prosite_id(uniprot_ids: list):
    if "Data not found" in uniprot_ids:             # récupère les prosite id à partir des uniprot ID (la requete est faite part groupe d'ID inférieur a 10)
        return "Data not found"
    else:
        chunks = len(uniprot_ids)//10+1
        uniprot_id_chunk = np.array_split(uniprot_ids, chunks)
        prosite = list()
        for i in uniprot_id_chunk:
            c = "%0A".join(i)
            try:
                requestURL = f"https://prosite.expasy.org/cgi-bin/prosite/PSScan.cgi?seq={c}&output=json"
                s = requests.Session()
                retries = Retry(total=5,
                            backoff_factor=0.1,
                            status_forcelist=[400, 500, 502, 503, 504 ])
                s.mount('http://', HTTPAdapter(max_retries=retries))
                r = s.get(requestURL)
                decoded = json.loads(r.text, strict=False)
                for i in decoded["matchset"]:
                    if i["signature_ac"] not in prosite:
                        prosite.append(i["signature_ac"])
            except json.JSONDecodeError:
                pass
        return prosite
