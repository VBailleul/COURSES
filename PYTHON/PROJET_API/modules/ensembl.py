#!/usr/bin/python3
from modules.utils_ensm import *


def ensembl(orga: str, gene: str, species: list):
    if orga in species:
        id, transcrit, translate = get_lookup_content(orga, gene)
        url_orth = get_orth_url(id, species[orga])
        output = {"ensembl_id": id, "ensembl_reign": species[orga], "ensembl_orth": url_orth,
                  "ensembl_transcript": transcrit, "ensembl_translate": translate}
    else:
        output = {"ensembl_id": "data not found", "ensembl_reign": "data not found", "ensembl_orth": ["data not found"],
                  "ensembl_transcript": ["data not found"], "ensembl_translate": ["data not found"]}

    return output


if __name__ == "__main__":
    dico = ensembl()
