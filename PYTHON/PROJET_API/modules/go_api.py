import requests
from requests.adapters import HTTPAdapter, Retry

def GO_api(uniprot_ids):

    GO_dict = {
        "biological_process": [],
        "cellular_component": [],
        "molecular_function": []
    }

    for id in uniprot_ids:

        # Set the API URL with the gene ID and specify the format of the response (JSON)
        api_url = f"http://www.ebi.ac.uk/QuickGO/services/annotation/search?geneProductId={id}&format=json"

        # server+ext pour avoir l'url entier de notre requete
        s = requests.Session()
        retries = Retry(total=5,
                    backoff_factor=0.1,
                    status_forcelist=[400, 500, 502, 503, 504 ])
        s.mount('http://', HTTPAdapter(max_retries=retries))
        response = s.get(api_url)

        # il y a une vérification que la requete soit possible, sinon une erreur est levée

        # Parse the JSON response to extract the GO terms

        if 'results' in response.json().keys():

            for result in response.json()["results"]:
                if result['goId'] not in GO_dict[result['goAspect']]:
                    GO_dict[result['goAspect']].append(result['goId'])

    return GO_dict
