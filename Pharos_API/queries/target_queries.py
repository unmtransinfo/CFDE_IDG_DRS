"""
Target-related GraphQL queries for Pharos API
Focused on basic target information and simple cross-relationships
"""

from queries.field_definitions import (
    TARGET_BASIC_FIELDS,
    DISEASE_BASIC_FIELDS,
    LIGAND_BASIC_FIELDS,
    TARGET_DETAILED_FIELDS,
    DISEASE_FULL_FIELDS,
    LIGAND_DETAILED_FIELDS
)

# Core target queries
GET_TARGET_BASIC = """
query GetTargetBasic($gene_symbol: String!) {
    target(q: {sym: $gene_symbol}) {
        """ + TARGET_BASIC_FIELDS + """
    }
}
"""

SEARCH_TARGETS_BASIC = """
query SearchTargetsBasic($search_term: String!, $limit: Int = 10) {
    targets(filter: {term: $search_term}, top: $limit) {
        count
        targets {
            """ + TARGET_BASIC_FIELDS + """
        }
    }
}
"""

# Cross-relationship query for demonstration
GET_TARGET_WITH_DISEASES_COUNT = """
query GetTargetWithDiseasesCount($gene_symbol: String!) {
    target(q: {sym: $gene_symbol}) {
        """ + TARGET_BASIC_FIELDS + """
        diseaseCount: diseases {
            """ + DISEASE_BASIC_FIELDS + """
        }
    }
}
"""

# Alternative version that gets disease count more efficiently
GET_TARGET_WITH_TOP_DISEASES = """
query GetTargetWithTopDiseases($gene_symbol: String!) {
    target(q: {sym: $gene_symbol}) {
        """ + TARGET_BASIC_FIELDS + """
        topDiseases: diseases(top: 3) {
            """ + DISEASE_BASIC_FIELDS + """
        }
    }
}
"""

GET_TARGET_WITH_LIGANDS = f"""
query GetTargetWithLigands($gene_symbol: String!, $top: Int!) {{
    target(q: {{sym: $gene_symbol}}) {{
        {TARGET_BASIC_FIELDS}
        ligands(top: $top) {{
            {LIGAND_BASIC_FIELDS}
        }}
    }}
}}
"""

# Query registry - makes it easy to get queries by name
TARGET_QUERIES = {
    'basic': GET_TARGET_BASIC,
    'search': SEARCH_TARGETS_BASIC,
    'with_diseases_count': GET_TARGET_WITH_DISEASES_COUNT,
    'with_top_diseases': GET_TARGET_WITH_TOP_DISEASES,
    'with_ligands': GET_TARGET_WITH_LIGANDS
}



def get_target_query(query_name: str) -> str:
    """
    Get a target query by name
    
    Args:
        query_name: Name of the query ('basic', 'search', 'with_diseases_count', 'with_top_diseases')
        
    Returns:
        GraphQL query string
        
    Raises:
        KeyError: If query_name is not found
    """
    if query_name not in TARGET_QUERIES:
        available = ', '.join(TARGET_QUERIES.keys())
        raise KeyError(f"Query '{query_name}' not found. Available queries: {available}")
    
    return TARGET_QUERIES[query_name]

def get_available_target_queries() -> list:
    """
    Get list of available target query names
    
    Returns:
        List of query names
    """
    return list(TARGET_QUERIES.keys())

# Field mapping for CSV export (Galaxy-friendly column names)
CSV_FIELD_MAPPING = {
    'name': 'Target_Name',
    'sym': 'Gene_Symbol',
    'uniprot': 'UniProt_ID',
    'description': 'Description',
    'tdl': 'Development_Level',
    'fam': 'Protein_Family',
    'novelty': 'Novelty_Score'
}

def get_csv_headers() -> list:
    """
    Get CSV column headers for basic target data
    Galaxy-friendly column names
    
    Returns:
        List of column headers
    """
    return list(CSV_FIELD_MAPPING.values())

def map_target_data_for_csv(target_data: dict) -> dict:
    """
    Map target data from GraphQL response to CSV-friendly format
    
    Args:
        target_data: Target data from GraphQL response
        
    Returns:
        Dictionary with CSV-friendly field names
    """
    mapped_data = {}
    for pharos_field, csv_field in CSV_FIELD_MAPPING.items():
        mapped_data[csv_field] = target_data.get(pharos_field)
    return mapped_data

# Validation helpers
def validate_gene_symbol(gene_symbol: str) -> str:
    """
    Validate and clean gene symbol input
    
    Args:
        gene_symbol: Raw gene symbol input
        
    Returns:
        Cleaned gene symbol
        
    Raises:
        ValueError: If gene symbol is invalid
    """
    if not gene_symbol or not isinstance(gene_symbol, str):
        raise ValueError("Gene symbol must be a non-empty string")
    
    # Clean the gene symbol
    cleaned = gene_symbol.strip().upper()
    
    if not cleaned:
        raise ValueError("Gene symbol cannot be empty or just whitespace")
    
    # Basic validation - gene symbols are typically 1-20 characters, alphanumeric + some symbols
    if len(cleaned) > 20:
        raise ValueError("Gene symbol too long (max 20 characters)")
    
    return cleaned

def validate_search_term(search_term: str) -> str:
    """
    Validate and clean search term input
    
    Args:
        search_term: Raw search term input
        
    Returns:
        Cleaned search term
        
    Raises:
        ValueError: If search term is invalid
    """
    if not search_term or not isinstance(search_term, str):
        raise ValueError("Search term must be a non-empty string")
    
    cleaned = search_term.strip()
    
    if not cleaned:
        raise ValueError("Search term cannot be empty or just whitespace")
    
    if len(cleaned) < 2:
        raise ValueError("Search term too short (minimum 2 characters)")
    
    if len(cleaned) > 100:
        raise ValueError("Search term too long (max 100 characters)")
    
    return cleaned

if __name__ == "__main__":
    # Test the queries when run directly
    print("Available target queries:")
    for query_name in get_available_target_queries():
        print(f"  - {query_name}")
    
    print("\nCSV Headers:")
    print(get_csv_headers())
    
    print("\nSample query:")
    print(get_target_query('basic'))




# Essential field selections for basic target information
# TARGET_BASIC_FIELDS = """
#     name
#     sym
#     uniprot
#     description
#     tdl
#     fam
#     novelty
# """

# Disease information fields for cross-relationships  
# DISEASE_BASIC_FIELDS = """
#     name
#     mondoID
#     description
# """