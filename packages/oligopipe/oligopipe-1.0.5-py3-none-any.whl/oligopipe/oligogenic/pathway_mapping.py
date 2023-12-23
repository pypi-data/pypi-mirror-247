from oligopipe.preprocess.annotation import Annotator


def get_pathway_data(genes, db_credentials, genome_build):
    annotator = Annotator(db_credentials, genome_build)

    try:
        gene_dict = {gene.strip().split(":")[0] : gene.strip().split(":")[1] for gene in genes.split(",")}
    except Exception as e:
        raise InputFormatException("Incorrect format for gene list.")

    annotator.annotation_repository.connect()
    if annotator.db_schema == 'old':
        query = '''select ensembl_gene_id, pathway_id, pathway_name, parent_pathway_ids 
                              FROM aaid
                              INNER JOIN protein_to_pathway USING(uniprot_acc)
                              INNER JOIN pathway USING(pathway_id)
                              INNER JOIN pathway_hierarchy USING(pathway_id)
                              WHERE ensembl_gene_id IN ({0})
                              AND pathway_source = 'Reactome'
                              ORDER BY ensembl_gene_id, pathway_id'''.format("'" + "','".join(gene_dict.keys()) + "'")
    elif annotator.db_schema == 'new':
        query = '''select ensembl_gene_id, pathway_id, pathway_name, parent_pathway_ids 
                          FROM protein
                          INNER JOIN protein_to_pathway USING(uniprot_acc)
                          INNER JOIN pathway USING(pathway_id)
                          INNER JOIN pathway_hierarchy USING(pathway_id)
                          WHERE ensembl_gene_id IN ({0})
                          AND pathway_source = 'Reactome'
                          ORDER BY ensembl_gene_id, pathway_id'''.format("'"+"','".join(gene_dict.keys())+"'")
    cur = annotator.annotation_repository.execute(query)

    uniq_ensembl_ids = set()
    reactome_id_to_pathway = {}
    parent_to_children_dict = {}
    top_parents = {}

    for row in cur.fetchall():
        ensembl_id, reactome_id, reactome_pathway, reactome_parents = row
        ensembl_gene = ensembl_id+":"+gene_dict[ensembl_id]
        uniq_ensembl_ids.add(ensembl_id)
        reactome_id_to_pathway[reactome_id] = reactome_pathway
        parents = reactome_parents.split(";") if reactome_parents is not None else []
        for parent in parents:
            parent_to_children_dict[parent] = parent_to_children_dict[parent] if parent in parent_to_children_dict else {}
            if reactome_id not in parent_to_children_dict[parent]:
                parent_to_children_dict[parent][reactome_id] = set()
            parent_to_children_dict[parent][reactome_id].add(ensembl_gene)
        if not reactome_parents:
            if reactome_id not in top_parents:
                top_parents[reactome_id] = set()
            top_parents[reactome_id].add(ensembl_gene)

    annotator.annotation_repository.disconnect()

    pathway_hierarchy_tree = {}

    top_parents["Unknown"] = [ensembl_id+":"+gene_dict[ensembl_id] for ensembl_id in (uniq_ensembl_ids ^ gene_dict.keys())]

    for top_parent, genes in top_parents.items():
        build_hierarchy_tree(top_parent, genes, pathway_hierarchy_tree, reactome_id_to_pathway, parent_to_children_dict)

    treemap_data = []
    pathway_hierarchy_tree = {
        "id": "",
        "name": "",
        "children": pathway_hierarchy_tree
    }

    transform_to_treemap_input(pathway_hierarchy_tree, treemap_data)

    return treemap_data[0]


def get_top_pathways(genes, limit, db_credentials, genome_build):
    annotator = Annotator(db_credentials, genome_build)

    gene_dict = {gene.strip().split(":")[0]: gene.strip().split(":")[1] for gene in genes.split(",")}
    annotator.annotation_repository.connect()

    if annotator.db_schema == 'old':
        query = '''SELECT pathway_name, pathway_id, count(ensembl_gene_id) as gene_count, (max(max_depth) * count(ensembl_gene_id)) as score 
                      FROM aaid
                      INNER JOIN protein_to_pathway USING(uniprot_acc)
                      INNER JOIN pathway USING(pathway_id)
                      INNER JOIN pathway_hierarchy USING(pathway_id)
                      WHERE ensembl_gene_id IN ({0})
                      GROUP BY pathway_id, pathway_name
                    UNION
                      SELECT DISTINCT NULL, NULL, ({1} - count(distinct(ensembl_gene_id))), 10000
                      FROM aaid
                      INNER JOIN protein_to_pathway USING(uniprot_acc)
                      WHERE ensembl_gene_id IN ({0})
                      ORDER BY score desc, gene_count desc
                      LIMIT {2}'''.format("'" + "','".join(gene_dict.keys()) + "'", len(gene_dict), limit + 1)
    elif annotator.db_schema == 'new':
        query = '''SELECT pathway_name, pathway_id, count(ensembl_gene_id) as gene_count, (max(max_depth) * count(ensembl_gene_id)) as score 
                  FROM protein
                  INNER JOIN protein_to_pathway USING(uniprot_acc)
                  INNER JOIN pathway USING(pathway_id)
                  INNER JOIN pathway_hierarchy USING(pathway_id)
                  WHERE ensembl_gene_id IN ({0})
                  GROUP BY pathway_id, pathway_name
                UNION
                  SELECT DISTINCT NULL, NULL, ({1} - count(distinct(ensembl_gene_id))), 10000
                  FROM protein
                  INNER JOIN protein_to_pathway USING(uniprot_acc)
                  WHERE ensembl_gene_id IN ({0})
                  ORDER BY score desc, gene_count desc
                  LIMIT {2}'''.format("'"+"','".join(gene_dict.keys())+"'", len(gene_dict), limit+1)

    cur = annotator.annotation_repository.execute(query)

    top_pathways = {'pathways': []}

    for row in cur.fetchall():
        reactome_pathway, reactome_id, gene_count, score = row
        if reactome_pathway is None:
            top_pathways["Unknown"] = gene_count
        else:
            top_pathways['pathways'].append({"pathway": reactome_pathway, "reactome_id":reactome_id, "gene_count": gene_count, "score": score})

    return top_pathways


def increment_dict(dictionary, target, value):
    dictionary[target] = dictionary[target] + value if target in dictionary else value


def build_hierarchy_tree(parent, genes, output, reactome_id_to_pathway, parent_to_children_dict):
    output[parent] = {}
    output[parent]["id"] = parent
    output[parent]["name"] = reactome_id_to_pathway[parent] if parent in reactome_id_to_pathway else parent
    output[parent]["genes"] = genes
    if parent in parent_to_children_dict:
        output[parent]["children"] = {}
        for child, genes in parent_to_children_dict[parent].items():
            build_hierarchy_tree(child, genes, output[parent]["children"], reactome_id_to_pathway, parent_to_children_dict)


def transform_to_treemap_input(parent, output, siblings=None):
    child = {"name": parent["name"], "id": parent["id"]}
    if "genes" in parent and len(parent["genes"]) > 0:
        size = get_size(parent)
        if siblings:
            size = float(size) * (len(getDescendantGenes(siblings)) / float(len(siblings)))
        if size > 0:
            child["size"] = size
    if "genes" in parent:
        child["genes"] = list(parent["genes"])
    children = set()
    if "children" in parent and parent["children"]:
        child["children"] = []
        children = list(parent["children"].values())
    output.append(child)
    for parent_child in children:
        transform_to_treemap_input(parent_child, child["children"], children)


def getDescendantGenes(children):
    descendant_genes = set()
    for child in children:
        descendant_genes = descendant_genes.union(child["genes"])
    return descendant_genes


def get_size(parent):
    if "children" in parent:
        descendant_genes = set()
        for key, child in parent["children"].items():
            descendant_genes = descendant_genes.union(child["genes"])
        return len(descendant_genes ^ parent["genes"])
    else:
        return len(parent["genes"])


class InputFormatException(Exception):
    pass
