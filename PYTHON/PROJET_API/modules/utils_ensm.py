import requests
from requests.adapters import HTTPAdapter, Retry

DIVISION = {"EnsemblBacteria": "bacteria",
            "EnsemblMetazoa": "metazoa",
            "EnsemblProtists": "protist",
            "EnsemblFungi": "fungi",
            "EnsemblPlants": "plants",
            "EnsemblVertebrates": "www"
            }


def get_lookup_content(orga: str, gene: str):                          #récupère les ID ainsi que les transcrits et protéines selon 
    transcrit = list()                                                 # un couple organisme gene dans la banque de données d'ensembl
    translate = list()
    s = requests.Session()
    retries = Retry(total=5,
                backoff_factor=0.1,
                status_forcelist=[400, 500, 502, 503, 504 ])
    s.mount('http://', HTTPAdapter(max_retries=retries))
    server = f"https://rest.ensembl.org/lookup/symbol/{orga}/{gene}?expand=1"
    r = s.get(server, headers={"Content-Type": "application/json"})
    if not r.ok:
        return "Data not found"
    else:
        decoded = r.json()
        for i in decoded["Transcript"]:
            transcrit.append(i["id"])
            if "Translation" in i.keys():
                translate.append(i["Translation"]["id"])

        return decoded['id'], transcrit, translate


def get_orth_url(id_ref: str, reign: str):
    ids = {}
    s = requests.Session()
    retries = Retry(total=5,
                backoff_factor=0.1,
                status_forcelist=[400, 500, 502, 503, 504 ])
    s.mount('http://', HTTPAdapter(max_retries=retries))
    server = f"https://rest.ensembl.org/homology/id/{id_ref}?type=orthologues;format=condensed"
    urls = list()
    r = s.get(server, headers={"Content-Type": "application/json"})                      # récupère les URLs des orthologues
    decoded = r.json()
    while decoded["data"] == []:
        r = requests.get(server, headers={"Content-Type": "application/json"})
        decoded = r.json()
    for i in decoded["data"][0]["homologies"]:
        if i['id'] not in ids:
            ids[i['id']] = "_"
        orga = i['species']
        url = f"https://{reign}.ensembl.org/{orga}/Gene/Summary?db=core;g={i['id']}"
        urls.append(url)

    return urls


def get_gb_url(orga: str, id: str, reign: str):                                                    

    return f"https://{reign}.ensembl.org/{orga}/Gene/Summary?db=core;g={id}"


def get_species():
    dico_species = dict()                                   # récupère toutes les espèces dans ensembl pour savoir si elles existent dedans
    server = "https://rest.ensembl.org/info/species?"       # évitant de chercher des choses qui n'existent pas, et permettant de récupérer
    for k in DIVISION:                                      # le reigne de l'organisme
        s = requests.Session()
        retries = Retry(total=5,
                    backoff_factor=0.1,
                    status_forcelist=[400, 500, 502, 503, 504 ])
        s.mount('http://', HTTPAdapter(max_retries=retries))
        url_species = f"{server}division={k}"
        r = s.get(url_species, headers={
            "Content-Type": "application/json"})
        decoded = r.json()
        for i in decoded['species']:
            if i["name"] not in dico_species:
                dico_species[i["name"]] = DIVISION[k]

    return dico_species
