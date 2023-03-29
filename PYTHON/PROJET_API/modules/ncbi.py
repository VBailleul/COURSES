#!/usr/bin/python3
from Bio import Entrez
from modules.utils_ncbi import *
MAIL = "benjamin.marsac@univ-rouen.fr"


def ncbi(orga_nm: str, gene: str):
    Entrez.email = MAIL
    ids = get_ncbi_id(gene, orga_nm)
    full_name = get_full_name_ncbi(ids, "100", "gene", "xml")
    prot_ids = get_link_id(ids, "gene", "gene_protein_refseq")
    prot_accession = from_id_get_accession(prot_ids, "protein")
    rna_ids = get_link_id(ids, "gene", "gene_nuccore_refseqrna")
    rna_accession = from_id_get_accession(rna_ids, "nuccore")
    kegg_orga_id, kegg_gene_id = kegg_gene_id_conv(ids)
    pathway = get_kegg_pathway(kegg_orga_id, kegg_gene_id)
    output = {"ncbi_id": ids,
              "ncbi_name": full_name,
              "ncbi_prot": prot_accession,
              "ncbi_rna": rna_accession,
              "kegg_id": f"{kegg_orga_id}:{kegg_gene_id}",
              "kegg_pathway": pathway
              }

    return output


if __name__ == "__main__":
    dico = ncbi()
    print(dico)
