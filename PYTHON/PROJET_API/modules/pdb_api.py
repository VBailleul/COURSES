import requests


def PDB_ID(UniProtIDs=list):

    request = requests.post(
        f"https://rest.uniprot.org/idmapping/run",
        data={"from": "UniProtKB_AC-ID", "to": "PDB", "ids": UniProtIDs},
    )

    jobID = request.json()["jobId"]
    response = requests.get(
        f"https://rest.uniprot.org/idmapping/status/{jobID}")

    pdb_ids = []

    # if "failedIds" in response.json().keys():
    #   return "No data found"
    if 'results' in response.json().keys():
        for result in response.json()['results']:
            if result['to'] not in pdb_ids:
                pdb_ids.append(result['to'])

    else:
        return "No data"

    return pdb_ids
