"""
GraphQL queries for disease-related operations
Defines query templates and validation for Pharos disease data
"""

from queries.field_definitions import (
    TARGET_BASIC_FIELDS,
    DISEASE_BASIC_FIELDS,
    LIGAND_BASIC_FIELDS,
    TARGET_DETAILED_FIELDS,
    DISEASE_FULL_FIELDS,
    LIGAND_DETAILED_FIELDS
)

import logging
from typing import Optional

logger = logging.getLogger(__name__)


# Disease with target associations
DISEASE_WITH_TARGETS_FIELDS = """
    name
    mondoID
    associationCount
    directAssociationCount
    uniprotDescription
    doDescription
    mondoDescription
    targetCounts {
        name
        value
    }
"""

# Disease IDs for cross-referencing
DISEASE_IDS_FIELDS = """
    dids {
        dataSrc
        id
    }
"""

def get_disease_query(query_type: str = 'basic') -> str:
    """
    Get the appropriate GraphQL query based on query type
    
    Args:
        query_type: Type of query ('basic', 'with_targets', 'with_ids', 'search')
        
    Returns:
        GraphQL query string
    """
    queries = {
        'basic': f"""
            query GetDisease($disease_name: String!) {{
                disease(name: $disease_name) {{
                    {DISEASE_BASIC_FIELDS}
                }}
            }}
        """,
        
        'with_targets': f"""
            query GetDiseaseWithTargets($disease_name: String!) {{
                disease(name: $disease_name) {{
                    {DISEASE_WITH_TARGETS_FIELDS}
                    targets {{
                        name
                        sym
                        tdl
                        uniprot
                    }}
                }}
            }}
        """,
        
        'with_ids': f"""
            query GetDiseaseWithIDs($disease_name: String!) {{
                disease(name: $disease_name) {{
                    {DISEASE_BASIC_FIELDS}
                    {DISEASE_IDS_FIELDS}
                }}
            }}
        """,
        
        'search': """
            query SearchDiseases($search_term: String!, $limit: Int) {
                diseases(filter: {term: $search_term}, top: $limit) {
                    count
                    diseases {
                        name
                        mondoID
                        associationCount
                        directAssociationCount
                        uniprotDescription
                        doDescription
                        mondoDescription
                        gard_rare
                    }
                }
            }
        """,
        
        'search_by_mondo': """
            query SearchDiseasesByMondo($mondo_id: String!) {
                disease(mondoID: $mondo_id) {
                    name
                    mondoID
                    associationCount
                    directAssociationCount
                    uniprotDescription
                    doDescription
                    mondoDescription
                    gard_rare
                }
            }
        """,
        
        'with_hierarchy': f"""
            query GetDiseaseWithHierarchy($disease_name: String!) {{
                disease(name: $disease_name) {{
                    {DISEASE_BASIC_FIELDS}
                    parents {{
                        name
                        mondoID
                    }}
                    children {{
                        name
                        mondoID
                    }}
                }}
            }}
        """
    }
    
    query = queries.get(query_type)
    
    if not query:
        logger.warning(f"Unknown query type '{query_type}', using 'basic'")
        query = queries['basic']
    
    return query

def validate_disease_name(disease_name: str) -> str:
    """
    Validate and clean disease name input
    
    Args:
        disease_name: Raw disease name from user input
        
    Returns:
        Cleaned disease name
        
    Raises:
        ValueError: If disease name is invalid
    """
    if not disease_name or not disease_name.strip():
        raise ValueError("Disease name cannot be empty")
    
    # Remove extra whitespace
    cleaned = disease_name.strip()
    
    # Check length (reasonable limits)
    if len(cleaned) < 2:
        raise ValueError("Disease name too short (minimum 2 characters)")
    
    if len(cleaned) > 200:
        raise ValueError("Disease name too long (maximum 200 characters)")
    
    logger.debug(f"Validated disease name: '{cleaned}'")
    return cleaned

def validate_mondo_id(mondo_id: str) -> str:
    """
    Validate MONDO ID format
    
    Args:
        mondo_id: MONDO identifier (e.g., MONDO:0005015)
        
    Returns:
        Cleaned MONDO ID
        
    Raises:
        ValueError: If MONDO ID format is invalid
    """
    if not mondo_id or not mondo_id.strip():
        raise ValueError("MONDO ID cannot be empty")
    
    cleaned = mondo_id.strip().upper()
    
    # Check MONDO ID format (should be MONDO:XXXXXXX)
    if not cleaned.startswith('MONDO:'):
        # Try to add prefix if just numbers provided
        if cleaned.isdigit():
            cleaned = f"MONDO:{cleaned.zfill(7)}"
        else:
            raise ValueError("MONDO ID must start with 'MONDO:' or be a numeric ID")
    
    # Validate format: MONDO:XXXXXXX (7 digits)
    parts = cleaned.split(':')
    if len(parts) != 2 or not parts[1].isdigit():
        raise ValueError("MONDO ID must be in format 'MONDO:XXXXXXX'")
    
    logger.debug(f"Validated MONDO ID: '{cleaned}'")
    return cleaned

def validate_disease_search_term(search_term: str) -> str:
    """
    Validate and clean disease search term
    
    Args:
        search_term: Raw search term from user input
        
    Returns:
        Cleaned search term
        
    Raises:
        ValueError: If search term is invalid
    """
    if not search_term or not search_term.strip():
        raise ValueError("Search term cannot be empty")
    
    cleaned = search_term.strip()
    
    # Check length
    if len(cleaned) < 2:
        raise ValueError("Search term too short (minimum 2 characters)")
    
    if len(cleaned) > 100:
        raise ValueError("Search term too long (maximum 100 characters)")
    
    logger.debug(f"Validated search term: '{cleaned}'")
    return cleaned

# Query building helpers
def build_disease_query_with_associations(disease_name: str, include_targets: bool = True) -> dict:
    """
    Build a comprehensive disease query with associations
    
    Args:
        disease_name: Disease name to query
        include_targets: Whether to include target associations
        
    Returns:
        Dictionary with 'query' and 'variables' keys
    """
    query_type = 'with_targets' if include_targets else 'basic'
    
    return {
        'query': get_disease_query(query_type),
        'variables': {'disease_name': validate_disease_name(disease_name)}
    }

def build_disease_search_query(search_term: str, limit: int = 10) -> dict:
    """
    Build a disease search query
    
    Args:
        search_term: Term to search for
        limit: Maximum number of results
        
    Returns:
        Dictionary with 'query' and 'variables' keys
    """
    return {
        'query': get_disease_query('search'),
        'variables': {
            'search_term': validate_disease_search_term(search_term),
            'limit': limit
        }
    }

# Example usage and testing
if __name__ == "__main__":
    print("Testing Disease Query Generation...")
    
    # Test 1: Basic disease query
    print("\n1. Basic disease query:")
    query = get_disease_query('basic')
    print(query)
    
    # Test 2: Disease with targets
    print("\n2. Disease with targets query:")
    query = get_disease_query('with_targets')
    print(query)
    
    # Test 3: Search query
    print("\n3. Disease search query:")
    query = get_disease_query('search')
    print(query)
    
    # Test 4: Validation
    print("\n4. Testing validation:")
    try:
        validated = validate_disease_name("  asthma  ")
        print(f"Valid disease name: '{validated}'")
        
        validated_mondo = validate_mondo_id("MONDO:0004979")
        print(f"Valid MONDO ID: '{validated_mondo}'")
        
        validated_search = validate_disease_search_term("lung cancer")
        print(f"Valid search term: '{validated_search}'")
    except ValueError as e:
        print(f"Validation error: {e}")
    
    # Test 5: Query builders
    print("\n5. Testing query builders:")
    query_dict = build_disease_query_with_associations("asthma", include_targets=True)
    print(f"Built query with variables: {query_dict['variables']}")
    
    search_dict = build_disease_search_query("cancer", limit=5)
    print(f"Built search query with variables: {search_dict['variables']}")
    
    print("\n✅ Disease queries module ready!")


# Basic disease fields for standard queries
# DISEASE_BASIC_FIELDS = """
#     name
#     mondoID
#     associationCount
#     directAssociationCount
#     gard_rare
#     datasource_count
#     uniprotDescription
#     doDescription
#     mondoDescription
# """