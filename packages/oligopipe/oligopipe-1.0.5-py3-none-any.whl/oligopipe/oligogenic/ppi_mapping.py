from oligopipe.preprocess.annotation import Annotator


def get_ppi_data(gene_dict, db_credentials, genome_build):
    annotator = Annotator(db_credentials, genome_build)

    annotator.annotation_repository.connect()

    if annotator.db_schema == 'old':
        canonical_transcript_query = """SELECT transcript_id FROM comppi_canonical_transcripts
                                            WHERE gene_id IN ({0})
                                         """.format("'" + "','".join(gene_dict.keys()) + "'")
    elif annotator.db_schema == 'new':
        canonical_transcript_query = """SELECT ensembl_can_transcript_id FROM gene
                                        WHERE ensembl_gene_id IN ({0})""".format("'"+"','".join(gene_dict.keys())+"'")
    cur = annotator.annotation_repository.execute(canonical_transcript_query)
    transcript_ids = [row[0] for row in cur]

    if annotator.db_schema == 'old':
        interaction_query = """SELECT interactorA, interactorB, score, a1.transcript_id, c1.cell_locations, a2.transcript_id, c2.cell_locations
                                   FROM comppi_interactions 
                                   LEFT JOIN comppi_uniprot_annotations as a1 ON (interactorA=a1.uniprot_acc)
                                   LEFT JOIN comppi_uniprot_annotations as a2 ON (interactorB=a2.uniprot_acc)
                                   LEFT JOIN comppi_cell_locations as c1 ON(interactorA=c1.protein_acc)
                                   LEFT JOIN comppi_cell_locations as c2 ON(interactorB=c2.protein_acc)
                                   WHERE (a1.transcript_id IN ({0})) OR (a2.transcript_id IN ({0}));
                                """.format("'" + "','".join(transcript_ids) + "'")
    elif annotator.db_schema == 'new':
        interaction_query = """SELECT distinct interactora_uniprot_acc, interactorb_uniprot_acc, score, p1.ensembl_can_transcript_id , c1.cell_locations, p2.ensembl_can_transcript_id , c2.cell_locations
                               FROM comppi_interactions 
                               LEFT JOIN protein as p1 ON (interactora_uniprot_acc=p1.uniprot_acc)
                               LEFT JOIN protein as p2 ON (interactorb_uniprot_acc=p2.uniprot_acc)
                               LEFT JOIN protein_cell_locations as c1 ON(interactora_uniprot_acc=c1.uniprot_acc)
                               LEFT JOIN protein_cell_locations as c2 ON(interactorb_uniprot_acc=c2.uniprot_acc)
                               WHERE (p1.ensembl_can_transcript_id  IN ({0})) OR (p2.ensembl_can_transcript_id IN ({0}));
                            """.format("'"+"','".join(transcript_ids)+"'")
    cur = annotator.annotation_repository.execute(interaction_query)
    interaction_data = cur.fetchall()

    # fetch gene_names from the interactors (preventing an extra join with big gene table in previous query)
    # create dict {ensembl_can_transcript_id: gene_name} to pass to build_ppi_graph along with results of interaction_query
    # need to include gene_names not present in the db via 'None'
    gene_names = {}
    interactors_transcript_ids = set()
    for row in interaction_data:
        interactors_transcript_ids.update((row[3], row[5]))
        gene_names[row[3]] = None
        gene_names[row[5]] = None

    gene_query = """SELECT ensembl_can_transcript_id, gene_name FROM gene
                    WHERE ensembl_can_transcript_id IN ({0})""".format("'"+"','".join(filter(None, interactors_transcript_ids))+"'")
    gene_cur = annotator.annotation_repository.execute(gene_query)
    for row in gene_cur:
        gene_names[row[0]] = row[1]

    annotator.annotation_repository.disconnect()

    graph_data = build_ppi_graph(interaction_data, gene_names)
    cleaned_graph_data = prune_graph_for_selected_genes(graph_data, gene_dict, transcript_ids)

    return cleaned_graph_data


def build_ppi_graph(interaction_data, gene_names):
    graph_data = {}
    for row in interaction_data:
        interactorA, interactorB, score, transcriptA, cell_locA, transcriptB, cell_locB = row
        if interactorA not in graph_data:
            graph_data[interactorA] = {}
            graph_data[interactorA]["links"] = {}
            graph_data[interactorA]["meta"] = {"gene": gene_names[transcriptA], "cell_locations":cell_locA, 'transcript': transcriptA}
        if interactorB not in graph_data:
            graph_data[interactorB] = {}
            graph_data[interactorB]["links"] = {}
            graph_data[interactorB]["meta"] = {"gene": gene_names[transcriptB], "cell_locations":cell_locB, 'transcript': transcriptB}
        graph_data[interactorA]["links"][interactorB] = score
        graph_data[interactorB]["links"][interactorA] = score
    return graph_data


def prune_graph_for_selected_genes(graph_data, gene_dict, transcript_ids):
    cleaned_graph_data = {}
    selected_proteins = set(filter(lambda p: graph_data[p]["meta"]["transcript"] in transcript_ids, graph_data.keys()))
    for interactorA in selected_proteins:
        cleaned_graph_data[interactorA] = {}
        cleaned_graph_data[interactorA]["links"] = {}
        cleaned_graph_data[interactorA]["meta"] = graph_data[interactorA]["meta"]
        cleaned_graph_data[interactorA]["selected"] = True
        for interactorB in graph_data[interactorA]["links"]:
            if interactorB in selected_proteins or len(set(graph_data[interactorB]["links"].keys()) & (set(selected_proteins) ^ {interactorA})) > 0:
                if interactorB not in selected_proteins and graph_data[interactorB]["meta"]["gene"] in gene_dict.values():
                    # TODO: Investigate if we could merge it instead of losing that info.
                    # Especially in the case where there is no direct interaction, it's interesting to keep it
                    continue
                if interactorB not in cleaned_graph_data:
                    cleaned_graph_data[interactorB] = {}
                    cleaned_graph_data[interactorB]["links"] = {}
                    cleaned_graph_data[interactorB]["selected"] = interactorB in selected_proteins
                cleaned_graph_data[interactorA]["links"][interactorB] = graph_data[interactorA]["links"][interactorB]
                cleaned_graph_data[interactorB]["links"][interactorA] = graph_data[interactorB]["links"][interactorA]
                cleaned_graph_data[interactorB]["meta"] = graph_data[interactorB]["meta"]
    # Add missing genes (with no protein mapped)
    gene_in_interactions = set(map(lambda p: cleaned_graph_data[p]["meta"]["gene"], cleaned_graph_data.keys()))
    for gene in gene_dict.values():
        if gene not in gene_in_interactions:
            node_id = "UNMAPPED_"+gene
            cleaned_graph_data[node_id] = {}
            cleaned_graph_data[node_id]["meta"] = {"gene": gene}
            cleaned_graph_data[node_id]["selected"] = True
            cleaned_graph_data[node_id]["unmapped"] = True

    return cleaned_graph_data
