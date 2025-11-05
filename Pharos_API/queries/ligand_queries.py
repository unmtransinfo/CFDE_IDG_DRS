"""
Ligand-related GraphQL queries for Pharos API
Focused on basic ligand information and chemical properties
"""

from queries.field_definitions import (
    TARGET_BASIC_FIELDS,
    DISEASE_BASIC_FIELDS,
    LIGAND_BASIC_FIELDS
)


# Core ligand queries
GET_LIGAND_BASIC = """
query GetLigandBasic($ligand_id: String!) {
    ligand(ligid: $ligand_id) {
        """ + LIGAND_BASIC_FIELDS + """
    }
}
"""

SEARCH_LIGANDS_BASIC = """
query SearchLigandsBasic($search_term: String!, $limit: Int = 10) {
    ligands(filter: {term: $search_term}, top: $limit) {
        count
        ligands {
            """ + LIGAND_BASIC_FIELDS + """
        }
    }
}
"""

# Alternative search query if the above structure doesn't work
SEARCH_LIGANDS_ALTERNATIVE = """
query SearchLigandsAlternative($search_term: String!) {
    ligands(filter: {term: $search_term}) {
        count
        ligands {
            """ + LIGAND_BASIC_FIELDS + """
        }
    }
}
"""

GET_LIGAND_WITH_TARGETS = f"""
query GetLigandWithTargets($ligand_id: String!) {{
    ligand(ligid: $ligand_id) {{
        {LIGAND_BASIC_FIELDS}
        activities {{
            target {{
                {TARGET_BASIC_FIELDS}
            }}
        }}
    }}
}}
"""

# Query registry - makes it easy to get queries by name
LIGAND_QUERIES = {
    'basic': GET_LIGAND_BASIC,
    'search': SEARCH_LIGANDS_BASIC,
    'search_alternative': SEARCH_LIGANDS_ALTERNATIVE,
    'with_targets': GET_LIGAND_WITH_TARGETS  # Add this line
}


def get_ligand_query(query_name: str) -> str:
    """
    Get a ligand query by name
    
    Args:
        query_name: Name of the query ('basic', 'search', 'search_alternative')
        
    Returns:
        GraphQL query string
        
    Raises:
        KeyError: If query_name is not found
    """
    if query_name not in LIGAND_QUERIES:
        available = ', '.join(LIGAND_QUERIES.keys())
        raise KeyError(f"Query '{query_name}' not found. Available queries: {available}")
    
    return LIGAND_QUERIES[query_name]

def get_available_ligand_queries() -> list:
    """
    Get list of available ligand query names
    
    Returns:
        List of query names
    """
    return list(LIGAND_QUERIES.keys())

# Field mapping for CSV export (Galaxy-friendly column names)
CSV_FIELD_MAPPING = {
    'name': 'Ligand_Name',
    'description': 'Description',
    'isdrug': 'Is_Drug',
    'smiles': 'SMILES',
    'actcnt': 'Activity_Count',
    'targetCount': 'Target_Count',
    'synonyms': 'Synonyms'
}

def get_csv_headers() -> list:
    """
    Get CSV column headers for basic ligand data
    Galaxy-friendly column names
    
    Returns:
        List of column headers
    """
    return list(CSV_FIELD_MAPPING.values())

def map_ligand_data_for_csv(ligand_data: dict) -> dict:
    """
    Map ligand data from GraphQL response to CSV-friendly format
    
    Args:
        ligand_data: Ligand data from GraphQL response
        
    Returns:
        Dictionary with CSV-friendly field names
    """
    mapped_data = {}
    
    for pharos_field, csv_field in CSV_FIELD_MAPPING.items():
        if pharos_field == 'synonyms':
            # Handle synonyms specially - convert list to comma-separated string
            synonyms = ligand_data.get('synonyms', [])
            if synonyms:
                synonym_names = [syn.get('value', syn.get('name', '')) for syn in synonyms]
                mapped_data[csv_field] = '; '.join(synonym_names[:3])  # Limit to first 3 synonyms
            else:
                mapped_data[csv_field] = ""
        else:
            mapped_data[csv_field] = ligand_data.get(pharos_field)
    
    return mapped_data

# Validation helpers
def validate_ligand_id(ligand_id: str) -> str:
    """
    Validate and clean ligand ID input
    
    Args:
        ligand_id: Raw ligand ID input (can be name, ChEMBL ID, etc.)
        
    Returns:
        Cleaned ligand ID
        
    Raises:
        ValueError: If ligand ID is invalid
    """
    if not ligand_id or not isinstance(ligand_id, str):
        raise ValueError("Ligand ID must be a non-empty string")
    
    # Clean the ligand ID
    cleaned = ligand_id.strip()
    
    if not cleaned:
        raise ValueError("Ligand ID cannot be empty or just whitespace")
    
    # Ligand IDs can be longer than gene symbols, so allow more characters
    if len(cleaned) > 100:
        raise ValueError("Ligand ID too long (max 100 characters)")
    
    return cleaned

def validate_ligand_search_term(search_term: str) -> str:
    """
    Validate and clean ligand search term input
    
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

# Helper function to extract ChEMBL ID from synonyms
def extract_chembl_id(ligand_data: dict) -> str:
    """
    Extract ChEMBL ID from ligand synonyms if available
    
    Args:
        ligand_data: Ligand data from GraphQL response
        
    Returns:
        ChEMBL ID if found, empty string otherwise
    """
    synonyms = ligand_data.get('synonyms', [])
    
    for synonym in synonyms:
        name = synonym.get('name', '').lower()
        value = synonym.get('value', '')
        
        # Look for ChEMBL ID patterns
        if 'chembl' in name or value.startswith('CHEMBL'):
            return value
    
    return ""

# Helper function to format drug status
def format_drug_status(isdrug: bool) -> str:
    """
    Convert boolean isdrug to human-readable status
    
    Args:
        isdrug: Boolean indicating if ligand is a drug
        
    Returns:
        Human-readable drug status
    """
    if isdrug is True:
        return "Drug"
    elif isdrug is False:
        return "Compound"
    else:
        return "Unknown"

# Test queries for debugging
TEST_LIGAND_IDS = [
    "haloperidol",      # From Pharos documentation example
    "aspirin",          # Common drug
    "CHEMBL25",         # ChEMBL ID format
    "imatinib"          # Cancer drug
]

if __name__ == "__main__":
    # Test the queries when run directly
    print("Available ligand queries:")
    for query_name in get_available_ligand_queries():
        print(f"  - {query_name}")
    
    print("\nCSV Headers:")
    print(get_csv_headers())
    
    print("\nSample query:")
    print(get_ligand_query('basic'))
    
    print("\nTest ligand IDs:")
    for test_id in TEST_LIGAND_IDS:
        try:
            cleaned = validate_ligand_id(test_id)
            print(f"  ✅ {test_id} → {cleaned}")
        except ValueError as e:
            print(f"  ❌ {test_id} → Error: {e}")
    
    print("\nSample data mapping:")
    sample_data = {
        'name': 'Haloperidol',
        'description': 'Typical antipsychotic drug',
        'isdrug': True,
        'smiles': 'C1CC(C[NH+]1CCCC(=O)C2=CC=C(C=C2)F)C3=CC=C(C=C3)Cl',
        'molweight': 375.865,
        'synonyms': [
            {'name': 'chembl_id', 'value': 'CHEMBL54'},
            {'name': 'brand_name', 'value': 'Haldol'}
        ]
    }
    
    mapped = map_ligand_data_for_csv(sample_data)
    print("Mapped data:", mapped)



# Essential field selections for basic ligand information
# LIGAND_BASIC_FIELDS = """
#     name
#     description
#     isdrug
#     smiles
#     actcnt
#     targetCount
#     synonyms {
#         name
#         value
#     }
# """