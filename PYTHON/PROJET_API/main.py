import sys
from PyQt5.QtWidgets import QApplication
from modules.ensembl import ensembl
from modules.ncbi import ncbi
from modules.global_utils import *
from modules.utils_ensm import get_species
from modules.protein import protein
from time import perf_counter
from modules.interface import Window

def main():
    dico_ncbi = dict()
    dico_ensembl = dict()
    dico_proteins = dict()
    app = QApplication(sys.argv)
    launcher = Window()
    launcher.show()
    app.exec()
    save_file = launcher.get_save_file()
    texte = launcher.get_text()
    if save_file == '' or texte == '':
        return
    a = perf_counter()
    species = get_species()   # check toutes les espèces présentes dans la bdd de ensembl
    for line in texte:
        gene, orga = gene_orga(line)
        print(f"Collecting information for {orga} {gene} ...")
        orga_nm = orga_normalizer(orga)
        dico_ncbi[f"{orga}/{gene}"] = ncbi(orga_nm, gene)
        dico_ensembl[f"{orga}/{gene}"] = ensembl(orga, gene, species)
        dico_proteins[f"{orga}/{gene}"] = protein(orga_nm, gene)
        print(f"... Done.")
    res = {k: (dico_ncbi[k] | dico_ensembl[k] | dico_proteins[k])
        for k in dico_ncbi.keys()}
    html_head_begin(save_file)
    script(save_file)
    css(save_file)
    html_head_end(save_file)
    html_table_head(save_file)
    html_table_body(save_file, res)
    html_tail(save_file)
    print(f"Over in {perf_counter() - a} sec")
    

if __name__ == "__main__":
    main()