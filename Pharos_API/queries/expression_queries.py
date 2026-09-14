"""
Expression-related GraphQL queries for Pharos API
Tissue expression data (HPA, GTEx, etc.) by target
"""

import re

# Maximum number of expression records to request from Pharos in one call.
# Pharos caps the `top` argument at 999; asking for more silently truncates.
# The default (10) is far too small — it misses most tissues and most sources.
# At top=999 we typically get full coverage across HPA Protein, HPA RNA,
# HPM Protein, and JensenLab TISSUES.
EXPRESSIONS_TOP = 999

# Fields returned for each expression record
EXPRESSION_FIELDS = """
    tissue
    value
    qual
    type
    uberon {
        uid
        name
    }
"""

# Basic target-level fields we always return alongside expressions
TARGET_BASIC_FIELDS = """
    name
    sym
    uniprot
    tdl
"""

# Query: look up target by UniProt accession
GET_EXPRESSIONS_BY_UNIPROT = """
query GetExpressionsByUniProt($identifier: String!) {
    target(q: {uniprot: $identifier}) {
""" + TARGET_BASIC_FIELDS + """
        expressions(top: """ + str(EXPRESSIONS_TOP) + """) {
""" + EXPRESSION_FIELDS + """
        }
    }
}
"""

# Query: look up target by gene symbol
GET_EXPRESSIONS_BY_SYM = """
query GetExpressionsBySym($identifier: String!) {
    target(q: {sym: $identifier}) {
""" + TARGET_BASIC_FIELDS + """
        expressions(top: """ + str(EXPRESSIONS_TOP) + """) {
""" + EXPRESSION_FIELDS + """
        }
    }
}
"""

EXPRESSION_QUERIES = {
    'by_uniprot': GET_EXPRESSIONS_BY_UNIPROT,
    'by_sym': GET_EXPRESSIONS_BY_SYM,
}


def get_expression_query(query_name: str) -> str:
    """Get an expression query by name"""
    if query_name not in EXPRESSION_QUERIES:
        available = ', '.join(EXPRESSION_QUERIES.keys())
        raise KeyError(f"Query '{query_name}' not found. Available queries: {available}")
    return EXPRESSION_QUERIES[query_name]


# Official UniProt accession regex (simplified to the common forms)
UNIPROT_REGEX = re.compile(
    r'^[OPQ][0-9][A-Z0-9]{3}[0-9]$'
    r'|^[A-NR-Z][0-9]([A-Z][A-Z0-9]{2}[0-9]){1,2}$'
)


def is_uniprot_accession(identifier: str) -> bool:
    """Return True if the string looks like a UniProt accession (e.g., P04035)"""
    if not identifier:
        return False
    return bool(UNIPROT_REGEX.match(identifier.strip().upper()))


def validate_identifier(identifier: str) -> str:
    """Validate a target identifier (UniProt or gene symbol)"""
    if not identifier or not isinstance(identifier, str):
        raise ValueError("Identifier must be a non-empty string")
    cleaned = identifier.strip()
    if not cleaned:
        raise ValueError("Identifier cannot be empty or whitespace")
    if len(cleaned) > 20:
        raise ValueError("Identifier too long (max 20 characters)")
    return cleaned


def validate_uberon_id(uberon_id: str) -> str:
    """Validate and normalize a UBERON ID (e.g., UBERON:0001134)"""
    if not uberon_id or not isinstance(uberon_id, str):
        raise ValueError("UBERON ID must be a non-empty string")
    cleaned = uberon_id.strip().upper()
    if cleaned.isdigit():
        # Accept bare numeric form and prepend prefix
        cleaned = f"UBERON:{cleaned.zfill(7)}"
    if not cleaned.startswith("UBERON:"):
        raise ValueError("UBERON ID must start with 'UBERON:' (e.g., UBERON:0001134)")
    return cleaned