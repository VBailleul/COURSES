from modules.protein_utils import *
from modules.interpro import interpro
from modules.string_api import string_api
from modules.go_api import *
from modules.pdb_api import *


def protein(orga: str, gene: str):
    uniprot_ids = dict()
    uniprot_names = dict()
    prosite_ids = dict()
    uniprot_ids, uniprot_names = get_uniprot_accession_and_full_name(
        gene, orga)
    prosite_ids = list()
    prosite_ids = get_prosite_id(uniprot_ids)
    ipr_ids, ipr_links = interpro(uniprot_ids)
    string_links = string_api(uniprot_ids)
    pdb_ids = PDB_ID(uniprot_ids)
    go_terms = GO_api(uniprot_ids)
    output = {"uniprot_ids": uniprot_ids,
              "uniprot_names": uniprot_names,
              "prosite_ids": prosite_ids,
              "ipr_ids": ipr_ids,
              "ipr_links": ipr_links,
              "string_links": string_links,
              "pdb": pdb_ids,
              "go_biological_process": go_terms['biological_process'],
              "go_cellular_component": go_terms['cellular_component'],
              "go_molecular_function": go_terms['molecular_function']}

    return output


if __name__ == "__main__":
    protein()
