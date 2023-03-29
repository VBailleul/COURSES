def gene_orga(line: str):
    gene, orga = line.rstrip().split(",")

    return gene, orga


def orga_normalizer(orga: str):

    return orga.capitalize().replace("_", " ")


def html_head_begin(output: str):
    with open(output, "w") as f:
        f.write("<!DOCTYPE html>\n<html>\n<head>\n")


def html_tail(output: str):
    with open(output, "a") as f:
        f.write("</html>\n")


def script(output: str):
    with open(output, "a") as f:
        f.write("""    <script src="https://code.jquery.com/jquery-3.5.1.js"></script>
    <script src="https://cdn.datatables.net/1.13.3/js/jquery.dataTables.min.js"></script>
    <script type="text/javascript" language="javascript" src="https://cdn.datatables.net/fixedcolumns/3.3.0/js/dataTables.fixedColumns.min.js"></script>
    <link rel="stylesheet" href="https://cdn.datatables.net/1.13.3/css/jquery.dataTables.min.css">
    <script>
        $(document).ready(function () {
    $('#gene').DataTable({
			scrollY: 700,
			scrollX: true,
			fixedColumns: {leftColumns: 2}
        })
            ;
});
    </script>\n""")


def html_head_end(output: str):
    with open(output, "a") as f:
        f.write("</head>\n")


def css(output: str):
    with open(output, "a") as f:
        f.write("""<style>
        table.dataTable thead tr {
        margin: 0;
        margin-bottom: 10px;
        border: 1px solid #f8ffff;
        background-color:#145299;
        color:aliceblue;
        text-align:center;
        }
        h1{
        padding-top: 15px;
        color:#2F4F4F;
        text-align:center;
        font-size:35px;
        }
        th{
        border: 1px solid #ffffff;
        font-size: .9em;
        }
        td{
        font-size: .8em;
	background-color: white;
        }
        a:link{
            color:#145299;
            text-decoration: none;
        }
        a:visited{
            color:#991497;
            text-decoration: none;
        }
        .scroll {white-space:nowrap;
        max-height: 80px;
        max-width: 230px;
        overflow: auto;
        }
    </style>\n""")


def html_table_head(output: str):
    with open(output, "a") as f:
        f.write("""<body>
<table id="gene" class="stripe cell-border">
<thead>
<tr>
<th colspan="2">Query</th>
<th colspan="5">NCBI data</th>
<th colspan="5">Ensembl data</th>
<th colspan="2">Uniprot data</th>
<th colspan="1">Prosite</th>
<th colspan="1">STRING</th>
<th colspan="1">PDB</th>
<th colspan="2">Interpro</th>
<th colspan="3">Gene Ontologies(s)</th>
<th colspan="2">KEGG</th>
</tr>
<tr>
<th>Gene symbol</th>
<th>Organism</th>
<th>Gene access number</th>
<th>Genome browser</th>
<th>Official full name</th>
<th>RNA access number(s)</th>
<th>Protein access number(s)</th>
<th>Gene access number</th>
<th>Genome browser</th>
<th>RNA access number(s)</th>
<th>Protein access number(s)</th>
<th>Orthologous gene(s)</th>
<th>Protein access number(s)</th>
<th>Protein name(s)</th>
<th>Motifs and domains</th>
<th>Protein interactions</th>
<th>3D protein structure</th>
<th>Domain ID</th>
<th>Interpro Browser</th>
<th>Function</th>
<th>Cellular component</th>
<th>Biological process</th>
<th>ID</th>
<th>Pathways</th>
</tr>
</thead>\n""")


def html_table_body(output: str, query_output: dict):
    with open(output, "a") as f:
        f.write("<tbody>\n")
        for i in query_output.keys():
            orga, gene = i.split("/")
            f.write(f"""<tr>\n
<td>\n<i>{gene}</i>\n</td>\n
<td>\n<i>{orga}</i>\n</td>\n""")
            f.write("<td>\n<div class='scroll'>\n")
            if query_output[i]["ncbi_id"] is not None:
                f.write(
                    f"\t{query_output[i]['ncbi_id']}\n</div>\n</td>\n<td>\n<div class='scroll'>\n\t<a href=https://www.ncbi.nlm.nih.gov/gene/{query_output[i]['ncbi_id']}>Genome Browser</a><br>\n")
            else:
                f.write(
                    f"\tData not found\n</div>\n</td>\n<td>\n<div class='scroll'>\nData not found")
            f.write(
                f"</div>\n</td>\n<td>\n<div class='scroll'>\n{query_output[i]['ncbi_name']}</div>\n</td>\n")
            f.write("<td>\n<div class='scroll'>\n")
            if len(query_output[i]["ncbi_rna"]) != 0:
                for j in query_output[i]["ncbi_rna"]:
                    f.write(
                        f"\t<a href=https://www.ncbi.nlm.nih.gov/nuccore/{j}>{j}</a><br>\n")
            else:
                f.write(f"\tData not found\n")
            f.write("</div>\n</td>\n")
            f.write("<td>\n<div class='scroll'>\n")
            if len(query_output[i]["ncbi_prot"]) != 0:
                for j in query_output[i]["ncbi_prot"]:
                    f.write(
                        f"<a href=https://www.ncbi.nlm.nih.gov/protein/{j}>{j}</a><br>\n")
            else:
                f.write(f"\tData not found\n")
            f.write("</div>\n</td>\n")
            if query_output[i]['ensembl_id'] != "data not found":
                f.write(
                    f"<td>\n<div class='scroll'>\n{query_output[i]['ensembl_id']}</div>\n</td>\n<td>\n<div class='scroll'>\n<a href=https://{query_output[i]['ensembl_reign']}.ensembl.org/{orga}/Gene/summary?g={query_output[i]['ensembl_id']}>Genome Browser</a></div>\n</td>\n<td>\n<div class='scroll'>\n")
                for j in query_output[i]["ensembl_translate"]:
                    f.write(
                        f"\t<a href=https://{query_output[i]['ensembl_reign']}.ensembl.org/{orga}/Transcript/ProteinSummary?g={query_output[i]['ensembl_id']};p={j}>{j}</a><br>\n")
                f.write("</div>\n</td>\n<td>\n<div class='scroll'>\n")
                for j in query_output[i]["ensembl_transcript"]:
                    f.write(
                        f"\t<a href=https://{query_output[i]['ensembl_reign']}.ensembl.org/{orga}/Transcript/Summary?g={query_output[i]['ensembl_id']};p={j}>{j}</a><br>\n")
                f.write("</div>\n</td>\n<td>\n<div class='scroll'>\n")
                for j in query_output[i]["ensembl_orth"]:
                    f.write(
                        f"\t<a href={j}>{j.split('=')[2]}</a><br>\n")
                f.write("</div>\n</td>")
            else:
                [f.write("<td>\n<div class='scroll'>\nData not found</div>\n</td>\n")
                 for i in range(5)]
            f.write("<td>\n<div class='scroll'>\n")
            for j in query_output[i]["uniprot_ids"]:
                if "Data not found" not in j:
                    f.write(
                        f"\t<a href=https://www.uniprot.org/uniprotkb/{j}>{j}</a><br>\n")
                else:
                    f.write(f"\t{j}\n")
            f.write("</div>\n</td>\n<td>\n<div class='scroll'>\n\t")
            for j in query_output[i]["uniprot_names"]:
                if "Data not found" not in j:
                    f.write(f"\t{j}<br>\n")
                else:
                    f.write(f"\t{j}\n")
            f.write("</div>\n</td>\n<td>\n<div class='scroll'>\n\t")
            for j in query_output[i]["prosite_ids"]:
                if "Data not found" not in j:
                    f.write(
                        f"\t<a href=https://prosite.expasy.org/{j}>{j}</a><br>\n")
                else:
                    f.write(f"\t{j}\n")
            f.write("</div>\n</td>\t<td>\n<div class='scroll'>\n\t")
            if len(query_output[i]["string_links"]) != 0:
                for j in query_output[i]["string_links"]:
                    f.write(f"\t<a href={j}>{j.split('=')[1]}</a><br>\n")
            else:
                f.write(f"\tData not found\n")
            f.write("</div>\n</td>\t<td>\n<div class='scroll'>\n\t")
            if len(query_output[i]["pdb"]) != 0:
                for j in query_output[i]["pdb"]:
                    f.write(
                        f"\t<a href=https://www.rcsb.org/structure/{j}>{j}</a><br>\n")
            else:
                f.write(f"\tData not found\n")
            f.write("</div>\n</td>\t<td>\n<div class='scroll'>\n\t")
            if len(query_output[i]["ipr_ids"]) != 0:
                for j in query_output[i]["ipr_ids"]:
                    f.write(
                        f"\t<a href=https://www.ebi.ac.uk/interpro/entry/InterPro/{j}>{j}<br>\n")
            else:
                f.write(f"\tData not found\n")
            f.write("</div>\n</td>\t<td>\n<div class='scroll'>\n\t")
            if len(query_output[i]["ipr_links"]) != 0:
                for j in query_output[i]["ipr_links"]:
                    f.write(f"\t<a href={j}>{j.split('/')[-2]}</a><br>\n")
            else:
                f.write(f"\tData not found\n")
            f.write("</div>\n</td>\t<td>\n<div class='scroll'>\n\t")
            if len(query_output[i]["go_biological_process"]) != 0:
                for j in query_output[i]["go_biological_process"]:
                    f.write(
                        f"\t<a href=http://amigo.geneontology.org/amigo/term/{j}>{j}</a><br>\n")
            else:
                f.write(f"\tData not found\n")
            f.write("</div>\n</td>\t<td>\n<div class='scroll'>\n\t")
            if len(query_output[i]["go_cellular_component"]) != 0:
                for j in query_output[i]["go_cellular_component"]:
                    f.write(
                        f"\t<a href=http://amigo.geneontology.org/amigo/term/{j}>{j}</a><br>\n")
            else:
                f.write(f"\tData not found\n")
            f.write("</div>\n</td>\t<td>\n<div class='scroll'>\n\t")
            if len(query_output[i]["go_molecular_function"]) != 0:
                for j in query_output[i]["go_molecular_function"]:
                    f.write(
                        f"\t<a href=http://amigo.geneontology.org/amigo/term/{j}>{j}</a><br>\n")
            else:
                f.write(f"\tData not found\n")
            f.write("</div>\n</td>\t<td>\n<div class='scroll'>\n\t")
            if query_output[i]["kegg_id"] != "None:None":
                f.write(f"\t{query_output[i]['kegg_id']}<br>\n")
            else:
                f.write(f"\tData not found\n")
            f.write("</div>\n</td>\t<td>\n<div class='scroll'>\n\t")
            if len(query_output[i]["kegg_pathway"]) != 0:
                for j in query_output[i]["kegg_pathway"]:
                    f.write(
                        f"\t<a href=https://www.genome.jp/dbget-bin/www_bget?{j}>{j}</a><br>\n")
            else:
                f.write(f"\tData not found\n")
            f.write("</div>\n</td>\t")
        f.write("""</tbody>
                    </table>\n
                    </body>\n""")
