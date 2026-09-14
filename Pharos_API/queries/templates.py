# queries/templates.py
"""
GraphQL query templates for Pharos API
Organized by entity type with common field selections
"""

# Common field fragments to reuse
FRAGMENTS = {
    'target_basic': """
        name
        sym  
        uniprot
        description
        tdl
        fam
        novelty
    """,
    
    'target_detailed': """
        name
        sym
        uniprot
        description
        tdl
        fam
        novelty
        seq
        props {
            name
            value
        }
        xrefs {
            name
            value
        }
    """,
    
    'disease_basic': """
        name
        mondoID
        description
        doID
    """,
    
    'ligand_basic': """
        name
        ims
        smiles
        description
        molweight
        props {
            name
            value
        }
    """
}

# TARGET QUERIES
TARGET_QUERIES = {
    'get_target_basic': """
    query GetTargetBasic($id: String!) {
        target(q: {sym: $id}) {
            """ + FRAGMENTS['target_basic'] + """
        }
    }
    """,
    
    'get_target_detailed': """
    query GetTargetDetailed($id: String!) {
        target(q: {sym: $id}) {
            """ + FRAGMENTS['target_detailed'] + """
        }
    }
    """,
    
    'search_targets': """
    query SearchTargets($query: String!, $top: Int = 10) {
        targets(filter: {term: $query}, top: $top) {
            count
            targets {
                """ + FRAGMENTS['target_basic'] + """
            }
        }
    }
    """,
    
    'get_target_diseases': """
    query GetTargetDiseases($id: String!) {
        target(q: {sym: $id}) {
            name
            sym
            diseases {
                """ + FRAGMENTS['disease_basic'] + """
                associationType
                evidence
            }
        }
    }
    """,
    
    'get_target_ligands': """
    query GetTargetLigands($id: String!) {
        target(q: {sym: $id}) {
            name
            sym
            ligands {
                """ + FRAGMENTS['ligand_basic'] + """
                activities {
                    type
                    value
                    moa
                }
            }
        }
    }
    """,
    
    'get_target_pathways': """
    query GetTargetPathways($id: String!) {
        target(q: {sym: $id}) {
            name
            sym
            pantherPaths {
                name
                pcid
                url
            }
            pathways {
                name
                pwtype
                url
            }
        }
    }
    """
}

# DISEASE QUERIES  
DISEASE_QUERIES = {
    'get_disease_basic': """
    query GetDiseaseBasic($id: String!) {
        disease(name: $id) {
            """ + FRAGMENTS['disease_basic'] + """
        }
    }
    """,
    
    'search_diseases': """
    query SearchDiseases($query: String!, $top: Int = 10) {
        diseases(filter: {term: $query}, top: $top) {
            count
            diseases {
                """ + FRAGMENTS['disease_basic'] + """
            }
        }
    }
    """,
    
    'get_disease_targets': """
    query GetDiseaseTargets($id: String!) {
        disease(name: $id) {
            name
            mondoID
            targets {
                """ + FRAGMENTS['target_basic'] + """
                associationType
                score
            }
        }
    }
    """,
    
    'get_disease_drugs': """
    query GetDiseaseDrugs($id: String!) {
        disease(name: $id) {
            name
            mondoID
            ligands {
                """ + FRAGMENTS['ligand_basic'] + """
                activities {
                    type
                    value
                }
            }
        }
    }
    """
}

# LIGAND QUERIES
LIGAND_QUERIES = {
    'get_ligand_basic': """
    query GetLigandBasic($id: String!) {
        ligand(ligid: $id) {
            """ + FRAGMENTS['ligand_basic'] + """
        }
    }
    """,
    
    'search_ligands': """
    query SearchLigands($query: String!, $top: Int = 10) {
        ligands(filter: {term: $query}, top: $top) {
            count
            ligands {
                """ + FRAGMENTS['ligand_basic'] + """
            }
        }
    }
    """,
    
    'get_ligand_targets': """
    query GetLigandTargets($id: String!) {
        ligand(ligid: $id) {
            name
            ims
            targets {
                """ + FRAGMENTS['target_basic'] + """
                activities {
                    type
                    value
                    moa
                    reference
                }
            }
        }
    }
    """,
    
    'get_ligand_diseases': """
    query GetLigandDiseases($id: String!) {
        ligand(ligid: $id) {
            name
            ims  
            diseases {
                """ + FRAGMENTS['disease_basic'] + """
            }
        }
    }
    """
}

# Combine all queries
ALL_QUERIES = {
    **TARGET_QUERIES,
    **DISEASE_QUERIES, 
    **LIGAND_QUERIES
}

def get_query(query_name: str) -> str:
    """Get a query template by name"""
    return ALL_QUERIES.get(query_name, "")

def list_available_queries() -> list:
    """List all available query names"""
    return list(ALL_QUERIES.keys())

def get_queries_by_entity(entity_type: str) -> dict:
    """Get all queries for a specific entity type"""
    entity_queries = {
        'target': TARGET_QUERIES,
        'disease': DISEASE_QUERIES,
        'ligand': LIGAND_QUERIES
    }
    return entity_queries.get(entity_type.lower(), {})