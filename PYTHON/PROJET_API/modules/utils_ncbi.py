#!/usr/bin/python3
from Bio import Entrez
from itertools import chain
import requests


def get_ncbi_id(gene: str, orga: str):                                                                                  # récupère les ID à partir d'un couple gene / organisme
    req = f"{gene} [Gene] AND \"{orga}\" [Orgn]"
    ids = ""
    tries = 0
    while len(ids) == 0 and tries < 5:
        handle = Entrez.esearch(db="gene", term=req, retmax=1)
        records = Entrez.read(handle)
        ids = records['IdList'][0]
        tries += 1
    return ids


def get_full_name_ncbi(ids: list | str, ret_max: str = "100", data_base: str = "gene", ret_mode: str = "xml"):      #grâce à l'ID d'un gène, récupère son nom entier si il existe
    handle = Entrez.efetch(db=data_base, id=ids,                                                                    #sinon récupère le nom du locus
                           retmax=ret_max, retmode=ret_mode)
    text = Entrez.parse(handle, data_base)
    for i in text:
        if 'Gene-ref_desc' in i["Entrezgene_gene"]["Gene-ref"]:
            return i["Entrezgene_gene"]["Gene-ref"]['Gene-ref_desc']
        else:
            return i["Entrezgene_gene"]["Gene-ref"]['Gene-ref_locus']


def get_link_id(ids: str, db_from: str, link: str):                                                                 # a partir des genes ID, cherche les liens disponibles entre deux banques de données proposées dans le lien
    handle = Entrez.elink(dbfrom=db_from, id=ids, linkname=link)                                                    # puis 
    res = Entrez.read(handle)
    if len(res[0]['LinkSetDb']) > 0:
        return chain.from_iterable([list(i.values()) for i in res[0]['LinkSetDb'][0]["Link"]])


def from_id_get_accession(ids: list | str, database: str):
    if ids is None:
        return []
    else:
        handle = Entrez.efetch(db=database, id=ids,
                               retmax="100", retmode="xml")
        text = Entrez.parse(handle, database)
        accession_nb = [i["GBSeq_primary-accession"] for i in text]

    return accession_nb


def kegg_gene_id_conv(ncbi_gene_id: str):
    server = f"https://rest.kegg.jp/conv/genes/ncbi-geneid:{ncbi_gene_id}"
    request = requests.get(server).text.rstrip("\n")
    if request != "":
        organism, kegg_id = request.split("\t")[1].split(":")
        return organism, kegg_id
    else:
        return None,None


def get_kegg_pathway(organism: str, kegg_id: str):
    kegg_pathway = list()
    if organism is None or kegg_id is None:
        return kegg_pathway
    server = f"https://rest.kegg.jp/link/pathway/{organism}:{kegg_id}"
    request = requests.get(server).text.rstrip("\n")
    kegg_pathway = [i.split("\t")[1].split(":")[1] for i in request.split(
        "\n")] if request != "" else kegg_pathway

    return kegg_pathway
