#!/usr/bin/python3
# -*- coding : uft-8 -*-
import requests
import re
from requests.adapters import HTTPAdapter, Retry

def string_api(uniprot_ids: list):
    results = []
    for uniprot_id in uniprot_ids:
        s = requests.Session()
        retries = Retry(total=5,
                    backoff_factor=0.1,
                    status_forcelist=[400, 500, 502, 503, 504 ])
        s.mount('http://', HTTPAdapter(max_retries=retries))
        r = s.get(
            'https://string-db.org/api/json/get_link?identifiers='+str(uniprot_id))
        res = r.json()
        found = True
        try:
            re.match('https', res[0])
        except:
            found = False
        if found == True and res[0] not in results:
            results.append(res[0])

    return (results)
