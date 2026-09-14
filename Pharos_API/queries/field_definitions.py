"""
Shared GraphQL field definitions for all query files
Ensures consistency across all queries
"""

# Target field definitions
TARGET_BASIC_FIELDS = """
    name
    sym
    uniprot
    description
    tdl
    fam
    novelty
"""

TARGET_DETAILED_FIELDS = """
    name
    sym
    uniprot
    description
    tdl
    fam
    novelty
    seq
"""

# Disease field definitions
DISEASE_BASIC_FIELDS = """
    name
    mondoID
    doDescription
    uniprotDescription
"""

DISEASE_FULL_FIELDS = """
    name
    mondoID
    associationCount
    directAssociationCount
    gard_rare
    datasource_count
    uniprotDescription
    doDescription
    mondoDescription
"""

# Ligand field definitions
LIGAND_BASIC_FIELDS = """
    name
    description
    isdrug
    smiles
    actcnt
    targetCount
    synonyms {
        name
        value
    }
"""

LIGAND_DETAILED_FIELDS = """
    name
    description
    isdrug
    smiles
    actcnt
    targetCount
    molweight
    synonyms {
        name
        value
    }
"""