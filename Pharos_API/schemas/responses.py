"""
Pydantic response models for Pharos API Gateway
Defines the structure of API responses for Galaxy integration
"""

from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

# Base models for common structures
class APIResponse(BaseModel):
    """Base response model with common metadata"""
    success: bool = True
    timestamp: datetime = Field(default_factory=datetime.now)
    message: Optional[str] = None

class PaginationInfo(BaseModel):
    """Pagination metadata for list responses"""
    total_count: int = Field(description="Total number of items available")
    returned_count: int = Field(description="Number of items in this response")
    skip: int = Field(description="Number of items skipped")
    limit: int = Field(description="Maximum items per page")

# Target-related response models
class TargetBasic(BaseModel):
    """
    Basic target information optimized for Galaxy CSV export
    Maps Pharos GraphQL fields to Galaxy-friendly names
    """
    target_name: Optional[str] = Field(None, description="Full protein/target name")
    gene_symbol: Optional[str] = Field(None, description="Gene symbol (e.g., EGFR, TP53)")
    uniprot_id: Optional[str] = Field(None, description="UniProt protein identifier")
    description: Optional[str] = Field(None, description="Brief target description")
    development_level: Optional[str] = Field(None, description="Target development level (Tclin, Tchem, Tbio, Tdark)")
    protein_family: Optional[str] = Field(None, description="Protein family classification")
    novelty_score: Optional[float] = Field(None, description="Novelty/knowledge score", ge=0, le=100)

    class Config:
        # Example for API documentation
        json_schema_extra = {
            "example": {
                "target_name": "Epidermal growth factor receptor",
                "gene_symbol": "EGFR",
                "uniprot_id": "P00533",
                "description": "Receptor tyrosine kinase binding ligands of the EGF family",
                "development_level": "Tclin",
                "protein_family": "Receptor tyrosine kinase",
                "novelty_score": 45.2
            }
        }

class DiseaseBasic(BaseModel):
    """
    Basic disease information for cross-relationship queries
    """
    disease_name: Optional[str] = Field(None, description="Disease name")
    mondo_id: Optional[str] = Field(None, description="MONDO disease identifier")
    description: Optional[str] = Field(None, description="Disease description")

    class Config:
        json_schema_extra = {
            "example": {
                "disease_name": "lung adenocarcinoma",
                "mondo_id": "MONDO:0005061",
                "description": "A non-small cell lung cancer that is characterized by the presence of adenocarcinoma."
            }
        }

# Single target response models
class TargetResponse(APIResponse):
    """
    Response model for single target queries
    Used by: GET /targets/{gene_symbol}
    """
    data: Optional[TargetBasic] = Field(None, description="Target information")
    gene_symbol_queried: str = Field(description="The gene symbol that was queried")

    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "timestamp": "2025-01-20T10:30:00Z",
                "message": "Target found successfully",
                "gene_symbol_queried": "EGFR",
                "data": {
                    "target_name": "Epidermal growth factor receptor",
                    "gene_symbol": "EGFR",
                    "uniprot_id": "P00533",
                    "development_level": "Tclin"
                }
            }
        }

# Search response models
class TargetSearchResponse(APIResponse):
    """
    Response model for target search queries
    Used by: GET /targets?search=kinase
    """
    data: List[TargetBasic] = Field(default_factory=list, description="List of matching targets")
    pagination: PaginationInfo = Field(description="Pagination information")
    search_term: str = Field(description="The search term that was used")

    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "timestamp": "2025-01-20T10:30:00Z",
                "message": "Found 156 targets matching 'kinase'",
                "search_term": "kinase",
                "data": [
                    {
                        "target_name": "Epidermal growth factor receptor",
                        "gene_symbol": "EGFR",
                        "development_level": "Tclin"
                    }
                ],
                "pagination": {
                    "total_count": 156,
                    "returned_count": 10,
                    "skip": 0,
                    "limit": 10
                }
            }
        }

# Cross-relationship response models
class TargetWithDiseases(TargetBasic):
    """
    Target information with associated diseases
    For cross-relationship demonstration
    """
    associated_diseases: List[DiseaseBasic] = Field(
        default_factory=list, 
        description="Diseases associated with this target"
    )
    disease_count: int = Field(0, description="Total number of associated diseases")

class TargetWithDiseasesResponse(APIResponse):
    """
    Response model for target queries with disease associations
    Used by: GET /targets/{gene_symbol}/diseases
    """
    data: Optional[TargetWithDiseases] = Field(None, description="Target with disease associations")
    gene_symbol_queried: str = Field(description="The gene symbol that was queried")

    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "timestamp": "2025-01-20T10:30:00Z",
                "message": "Target found with 12 disease associations",
                "gene_symbol_queried": "EGFR",
                "data": {
                    "target_name": "Epidermal growth factor receptor",
                    "gene_symbol": "EGFR",
                    "development_level": "Tclin",
                    "disease_count": 12,
                    "associated_diseases": [
                        {
                            "disease_name": "lung adenocarcinoma",
                            "mondo_id": "MONDO:0005061"
                        }
                    ]
                }
            }
        }

# Ligand-related response models
class LigandBasic(BaseModel):
    """
    Basic ligand information optimized for Galaxy CSV export
    Maps Pharos GraphQL fields to Galaxy-friendly names
    """
    ligand_name: Optional[str] = Field(None, description="Compound/drug name")
    description: Optional[str] = Field(None, description="Brief ligand description")
    is_drug: Optional[bool] = Field(None, description="Whether this is an approved drug")
    drug_status: Optional[str] = Field(None, description="Human-readable drug status (Drug/Compound/Unknown)")
    smiles: Optional[str] = Field(None, description="Chemical structure in SMILES format")
    molecular_weight: Optional[float] = Field(None, description="Molecular weight in Da", ge=0)
    synonyms: Optional[str] = Field(None, description="Alternative names (semicolon-separated)")
    chembl_id: Optional[str] = Field(None, description="ChEMBL database identifier")

    class Config:
        json_schema_extra = {
            "example": {
                "ligand_name": "Haloperidol",
                "description": "Typical antipsychotic drug",
                "is_drug": True,
                "drug_status": "Drug",
                "smiles": "C1CC(C[NH+]1CCCC(=O)C2=CC=C(C=C2)F)C3=CC=C(C=C3)Cl",
                "molecular_weight": 375.865,
                "synonyms": "Haldol; CHEMBL54; Serenace",
                "chembl_id": "CHEMBL54"
            }
        }

class LigandResponse(APIResponse):
    """
    Response model for single ligand queries
    Used by: GET /ligands/{ligand_id}
    """
    data: Optional[LigandBasic] = Field(None, description="Ligand information")
    ligand_id_queried: str = Field(description="The ligand ID that was queried")

    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "timestamp": "2025-01-20T10:30:00Z",
                "message": "Ligand found successfully",
                "ligand_id_queried": "haloperidol",
                "data": {
                    "ligand_name": "Haloperidol",
                    "description": "Typical antipsychotic drug",
                    "is_drug": True,
                    "drug_status": "Drug",
                    "molecular_weight": 375.865
                }
            }
        }

class LigandSearchResponse(APIResponse):
    """
    Response model for ligand search queries
    Used by: GET /ligands?search=term
    """
    data: List[LigandBasic] = Field(default_factory=list, description="List of matching ligands")
    pagination: PaginationInfo = Field(description="Pagination information")
    search_term: str = Field(description="The search term that was used")

    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "timestamp": "2025-01-20T10:30:00Z",
                "message": "Found 23 ligands matching 'antipsychotic'",
                "search_term": "antipsychotic",
                "data": [
                    {
                        "ligand_name": "Haloperidol",
                        "description": "Typical antipsychotic drug",
                        "is_drug": True,
                        "drug_status": "Drug",
                        "molecular_weight": 375.865
                    }
                ],
                "pagination": {
                    "total_count": 23,
                    "returned_count": 10,
                    "skip": 0,
                    "limit": 10
                }
            }
        }

# Error response models
class ErrorDetail(BaseModel):
    """Individual error detail"""
    field: Optional[str] = Field(None, description="Field that caused the error")
    message: str = Field(description="Error message")
    error_code: Optional[str] = Field(None, description="Machine-readable error code")

class ErrorResponse(BaseModel):
    """
    Standard error response format
    Used when API requests fail
    """
    success: bool = False
    timestamp: datetime = Field(default_factory=datetime.now)
    message: str = Field(description="Human-readable error message")
    errors: List[ErrorDetail] = Field(default_factory=list, description="Detailed error information")
    request_id: Optional[str] = Field(None, description="Unique request identifier for debugging")

    class Config:
        json_schema_extra = {
            "example": {
                "success": False,
                "timestamp": "2025-01-20T10:30:00Z",
                "message": "Target not found",
                "errors": [
                    {
                        "field": "gene_symbol",
                        "message": "Gene symbol 'INVALID' not found in Pharos database",
                        "error_code": "TARGET_NOT_FOUND"
                    }
                ]
            }
        }

# CSV export models
class CSVExportInfo(BaseModel):
    """
    Information about CSV export options
    For Galaxy integration planning
    """
    available_formats: List[str] = Field(default=["csv", "tsv", "json"])
    csv_headers: List[str] = Field(description="Column headers for CSV export")
    total_rows: int = Field(description="Number of data rows")
    export_timestamp: datetime = Field(default_factory=datetime.now)

class CSVExportResponse(BaseModel):
    """
    Response model for CSV export requests
    Future use for Galaxy data download
    """
    export_info: CSVExportInfo
    download_url: Optional[str] = Field(None, description="URL to download the CSV file")
    data: Optional[str] = Field(None, description="Inline CSV data (for small datasets)")

# Helper functions for response creation
def create_target_response(
    target_data: Optional[dict], 
    gene_symbol: str, 
    success: bool = True, 
    message: Optional[str] = None
) -> TargetResponse:
    """
    Create a standardized target response
    
    Args:
        target_data: Raw target data from GraphQL
        gene_symbol: Gene symbol that was queried
        success: Whether the query was successful
        message: Optional message
        
    Returns:
        Formatted TargetResponse
    """
    # Convert Pharos field names to Galaxy-friendly names
    formatted_data = None
    if target_data:
        formatted_data = TargetBasic(
            target_name=target_data.get('name'),
            gene_symbol=target_data.get('sym'),
            uniprot_id=target_data.get('uniprot'),
            description=target_data.get('description'),
            development_level=target_data.get('tdl'),
            protein_family=target_data.get('fam'),
            novelty_score=target_data.get('novelty')
        )
    
    return TargetResponse(
        success=success,
        message=message or ("Target found successfully" if target_data else "Target not found"),
        gene_symbol_queried=gene_symbol,
        data=formatted_data
    )

def create_search_response(
    targets_data: List[dict], 
    search_term: str,
    total_count: int,
    skip: int,
    limit: int,
    success: bool = True,
    message: Optional[str] = None
) -> TargetSearchResponse:
    """
    Create a standardized search response
    
    Args:
        targets_data: List of target data from GraphQL
        search_term: Search term that was used
        total_count: Total number of matching targets
        skip: Number of items skipped
        limit: Maximum items per page
        success: Whether the query was successful
        message: Optional message
        
    Returns:
        Formatted TargetSearchResponse
    """
    # Convert each target to Galaxy-friendly format
    formatted_targets = []
    for target_data in targets_data:
        formatted_target = TargetBasic(
            target_name=target_data.get('name'),
            gene_symbol=target_data.get('sym'),
            uniprot_id=target_data.get('uniprot'),
            description=target_data.get('description'),
            development_level=target_data.get('tdl'),
            protein_family=target_data.get('fam'),
            novelty_score=target_data.get('novelty')
        )
        formatted_targets.append(formatted_target)
    
    return TargetSearchResponse(
        success=success,
        message=message or f"Found {total_count} targets matching '{search_term}'",
        search_term=search_term,
        data=formatted_targets,
        pagination=PaginationInfo(
            total_count=total_count,
            returned_count=len(formatted_targets),
            skip=skip,
            limit=limit
        )
    )

def create_error_response(
    message: str,
    errors: Optional[List[dict]] = None,
    request_id: Optional[str] = None
) -> ErrorResponse:
    """
    Create a standardized error response
    
    Args:
        message: Main error message
        errors: List of detailed errors
        request_id: Unique request identifier
        
    Returns:
        Formatted ErrorResponse
    """
    error_details = []
    if errors:
        for error in errors:
            error_details.append(ErrorDetail(
                field=error.get('field'),
                message=error.get('message', 'Unknown error'),
                error_code=error.get('code')
            ))
    
    return ErrorResponse(
        message=message,
        errors=error_details,
        request_id=request_id
    )

# Ligand helper functions
def create_ligand_response(
    ligand_data: Optional[dict], 
    ligand_id: str, 
    success: bool = True, 
    message: Optional[str] = None
) -> LigandResponse:
    """
    Create a standardized ligand response
    
    Args:
        ligand_data: Raw ligand data from GraphQL
        ligand_id: Ligand ID that was queried
        success: Whether the query was successful
        message: Optional message
        
    Returns:
        Formatted LigandResponse
    """
    # Convert Pharos field names to Galaxy-friendly names
    formatted_data = None
    if ligand_data:
        # Handle synonyms - convert list to semicolon-separated string
        synonyms_str = ""
        chembl_id = ""
        if ligand_data.get('synonyms'):
            synonym_values = []
            for syn in ligand_data['synonyms']:
                value = syn.get('value', syn.get('name', ''))
                if value:
                    synonym_values.append(value)
                    # Extract ChEMBL ID if present
                    if value.startswith('CHEMBL') or 'chembl' in syn.get('name', '').lower():
                        chembl_id = value
            synonyms_str = "; ".join(synonym_values[:5])  # Limit to first 5 synonyms
        
        # Format drug status
        is_drug = ligand_data.get('isdrug')
        if is_drug is True:
            drug_status = "Drug"
        elif is_drug is False:
            drug_status = "Compound"
        else:
            drug_status = "Unknown"
        
        formatted_data = LigandBasic(
            ligand_name=ligand_data.get('name'),
            description=ligand_data.get('description'),
            is_drug=is_drug,
            drug_status=drug_status,
            smiles=ligand_data.get('smiles'),
            molecular_weight=ligand_data.get('molweight'),
            synonyms=synonyms_str,
            chembl_id=chembl_id
        )
    
    return LigandResponse(
        success=success,
        message=message or ("Ligand found successfully" if ligand_data else "Ligand not found"),
        ligand_id_queried=ligand_id,
        data=formatted_data
    )

def create_ligand_search_response(
    ligands_data: List[dict], 
    search_term: str,
    total_count: int,
    skip: int,
    limit: int,
    success: bool = True,
    message: Optional[str] = None
) -> LigandSearchResponse:
    """
    Create a standardized ligand search response
    
    Args:
        ligands_data: List of ligand data from GraphQL
        search_term: Search term that was used
        total_count: Total number of matching ligands
        skip: Number of items skipped
        limit: Maximum items per page
        success: Whether the query was successful
        message: Optional message
        
    Returns:
        Formatted LigandSearchResponse
    """
    # Convert each ligand to Galaxy-friendly format
    formatted_ligands = []
    for ligand_data in ligands_data:
        # Handle synonyms
        synonyms_str = ""
        chembl_id = ""
        if ligand_data.get('synonyms'):
            synonym_values = []
            for syn in ligand_data['synonyms']:
                value = syn.get('value', syn.get('name', ''))
                if value:
                    synonym_values.append(value)
                    if value.startswith('CHEMBL') or 'chembl' in syn.get('name', '').lower():
                        chembl_id = value
            synonyms_str = "; ".join(synonym_values[:3])  # Limit to 3 for search results
        
        # Format drug status
        is_drug = ligand_data.get('isdrug')
        if is_drug is True:
            drug_status = "Drug"
        elif is_drug is False:
            drug_status = "Compound"
        else:
            drug_status = "Unknown"
        
        formatted_ligand = LigandBasic(
            ligand_name=ligand_data.get('name'),
            description=ligand_data.get('description'),
            is_drug=is_drug,
            drug_status=drug_status,
            smiles=ligand_data.get('smiles'),
            molecular_weight=ligand_data.get('molweight'),
            synonyms=synonyms_str,
            chembl_id=chembl_id
        )
        formatted_ligands.append(formatted_ligand)
    
    return LigandSearchResponse(
        success=success,
        message=message or f"Found {total_count} ligands matching '{search_term}'",
        search_term=search_term,
        data=formatted_ligands,
        pagination=PaginationInfo(
            total_count=total_count,
            returned_count=len(formatted_ligands),
            skip=skip,
            limit=limit
        )
    )

if __name__ == "__main__":
    # Test the models when run directly
    print("Testing Pydantic response models...")
    
    # Test creating a target response
    sample_target_data = {
        'name': 'Epidermal growth factor receptor',
        'sym': 'EGFR',
        'uniprot': 'P00533',
        'tdl': 'Tclin',
        'novelty': 45.2
    }
    
    response = create_target_response(sample_target_data, 'EGFR')
    print("Sample target response:")
    print(response.model_dump_json(indent=2))
    
    print("\n" + "="*50)
    
    # Test creating a ligand response
    sample_ligand_data = {
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
    
    ligand_response = create_ligand_response(sample_ligand_data, 'haloperidol')
    print("Sample ligand response:")
    print(ligand_response.model_dump_json(indent=2))




# """
# Pydantic response models for Pharos API Gateway
# Defines the structure of API responses for Galaxy integration
# """

# from pydantic import BaseModel, Field
# from typing import Optional, List
# from datetime import datetime

# # Base models for common structures
# class APIResponse(BaseModel):
#     """Base response model with common metadata"""
#     success: bool = True
#     timestamp: datetime = Field(default_factory=datetime.now)
#     message: Optional[str] = None

# class PaginationInfo(BaseModel):
#     """Pagination metadata for list responses"""
#     total_count: int = Field(description="Total number of items available")
#     returned_count: int = Field(description="Number of items in this response")
#     skip: int = Field(description="Number of items skipped")
#     limit: int = Field(description="Maximum items per page")

# # Target-related response models
# class TargetBasic(BaseModel):
#     """
#     Basic target information optimized for Galaxy CSV export
#     Maps Pharos GraphQL fields to Galaxy-friendly names
#     """
#     target_name: Optional[str] = Field(None, description="Full protein/target name")
#     gene_symbol: Optional[str] = Field(None, description="Gene symbol (e.g., EGFR, TP53)")
#     uniprot_id: Optional[str] = Field(None, description="UniProt protein identifier")
#     description: Optional[str] = Field(None, description="Brief target description")
#     development_level: Optional[str] = Field(None, description="Target development level (Tclin, Tchem, Tbio, Tdark)")
#     protein_family: Optional[str] = Field(None, description="Protein family classification")
#     novelty_score: Optional[float] = Field(None, description="Novelty/knowledge score", ge=0, le=100)

#     class Config:
#         # Example for API documentation
#         json_schema_extra = {
#             "example": {
#                 "target_name": "Epidermal growth factor receptor",
#                 "gene_symbol": "EGFR",
#                 "uniprot_id": "P00533",
#                 "description": "Receptor tyrosine kinase binding ligands of the EGF family",
#                 "development_level": "Tclin",
#                 "protein_family": "Receptor tyrosine kinase",
#                 "novelty_score": 45.2
#             }
#         }

# class DiseaseBasic(BaseModel):
#     """
#     Basic disease information for cross-relationship queries
#     """
#     disease_name: Optional[str] = Field(None, description="Disease name")
#     mondo_id: Optional[str] = Field(None, description="MONDO disease identifier")
#     description: Optional[str] = Field(None, description="Disease description")

#     class Config:
#         json_schema_extra = {
#             "example": {
#                 "disease_name": "lung adenocarcinoma",
#                 "mondo_id": "MONDO:0005061",
#                 "description": "A non-small cell lung cancer that is characterized by the presence of adenocarcinoma."
#             }
#         }

# # Single target response models
# class TargetResponse(APIResponse):
#     """
#     Response model for single target queries
#     Used by: GET /targets/{gene_symbol}
#     """
#     data: Optional[TargetBasic] = Field(None, description="Target information")
#     gene_symbol_queried: str = Field(description="The gene symbol that was queried")

#     class Config:
#         json_schema_extra = {
#             "example": {
#                 "success": True,
#                 "timestamp": "2025-01-20T10:30:00Z",
#                 "message": "Target found successfully",
#                 "gene_symbol_queried": "EGFR",
#                 "data": {
#                     "target_name": "Epidermal growth factor receptor",
#                     "gene_symbol": "EGFR",
#                     "uniprot_id": "P00533",
#                     "development_level": "Tclin"
#                 }
#             }
#         }

# # Search response models
# class TargetSearchResponse(APIResponse):
#     """
#     Response model for target search queries
#     Used by: GET /targets?search=kinase
#     """
#     data: List[TargetBasic] = Field(default_factory=list, description="List of matching targets")
#     pagination: PaginationInfo = Field(description="Pagination information")
#     search_term: str = Field(description="The search term that was used")

#     class Config:
#         json_schema_extra = {
#             "example": {
#                 "success": True,
#                 "timestamp": "2025-01-20T10:30:00Z",
#                 "message": "Found 156 targets matching 'kinase'",
#                 "search_term": "kinase",
#                 "data": [
#                     {
#                         "target_name": "Epidermal growth factor receptor",
#                         "gene_symbol": "EGFR",
#                         "development_level": "Tclin"
#                     }
#                 ],
#                 "pagination": {
#                     "total_count": 156,
#                     "returned_count": 10,
#                     "skip": 0,
#                     "limit": 10
#                 }
#             }
#         }

# # Cross-relationship response models
# class TargetWithDiseases(TargetBasic):
#     """
#     Target information with associated diseases
#     For cross-relationship demonstration
#     """
#     associated_diseases: List[DiseaseBasic] = Field(
#         default_factory=list, 
#         description="Diseases associated with this target"
#     )
#     disease_count: int = Field(0, description="Total number of associated diseases")

# class TargetWithDiseasesResponse(APIResponse):
#     """
#     Response model for target queries with disease associations
#     Used by: GET /targets/{gene_symbol}/diseases
#     """
#     data: Optional[TargetWithDiseases] = Field(None, description="Target with disease associations")
#     gene_symbol_queried: str = Field(description="The gene symbol that was queried")

#     class Config:
#         json_schema_extra = {
#             "example": {
#                 "success": True,
#                 "timestamp": "2025-01-20T10:30:00Z",
#                 "message": "Target found with 12 disease associations",
#                 "gene_symbol_queried": "EGFR",
#                 "data": {
#                     "target_name": "Epidermal growth factor receptor",
#                     "gene_symbol": "EGFR",
#                     "development_level": "Tclin",
#                     "disease_count": 12,
#                     "associated_diseases": [
#                         {
#                             "disease_name": "lung adenocarcinoma",
#                             "mondo_id": "MONDO:0005061"
#                         }
#                     ]
#                 }
#             }
#         }

# # Error response models
# class ErrorDetail(BaseModel):
#     """Individual error detail"""
#     field: Optional[str] = Field(None, description="Field that caused the error")
#     message: str = Field(description="Error message")
#     error_code: Optional[str] = Field(None, description="Machine-readable error code")

# class ErrorResponse(BaseModel):
#     """
#     Standard error response format
#     Used when API requests fail
#     """
#     success: bool = False
#     timestamp: datetime = Field(default_factory=datetime.now)
#     message: str = Field(description="Human-readable error message")
#     errors: List[ErrorDetail] = Field(default_factory=list, description="Detailed error information")
#     request_id: Optional[str] = Field(None, description="Unique request identifier for debugging")

#     class Config:
#         json_schema_extra = {
#             "example": {
#                 "success": False,
#                 "timestamp": "2025-01-20T10:30:00Z",
#                 "message": "Target not found",
#                 "errors": [
#                     {
#                         "field": "gene_symbol",
#                         "message": "Gene symbol 'INVALID' not found in Pharos database",
#                         "error_code": "TARGET_NOT_FOUND"
#                     }
#                 ]
#             }
#         }

# # CSV export models
# class CSVExportInfo(BaseModel):
#     """
#     Information about CSV export options
#     For Galaxy integration planning
#     """
#     available_formats: List[str] = Field(default=["csv", "tsv", "json"])
#     csv_headers: List[str] = Field(description="Column headers for CSV export")
#     total_rows: int = Field(description="Number of data rows")
#     export_timestamp: datetime = Field(default_factory=datetime.now)

# class CSVExportResponse(BaseModel):
#     """
#     Response model for CSV export requests
#     Future use for Galaxy data download
#     """
#     export_info: CSVExportInfo
#     download_url: Optional[str] = Field(None, description="URL to download the CSV file")
#     data: Optional[str] = Field(None, description="Inline CSV data (for small datasets)")

# # Helper functions for response creation
# def create_target_response(
#     target_data: Optional[dict], 
#     gene_symbol: str, 
#     success: bool = True, 
#     message: Optional[str] = None
# ) -> TargetResponse:
#     """
#     Create a standardized target response
    
#     Args:
#         target_data: Raw target data from GraphQL
#         gene_symbol: Gene symbol that was queried
#         success: Whether the query was successful
#         message: Optional message
        
#     Returns:
#         Formatted TargetResponse
#     """
#     # Convert Pharos field names to Galaxy-friendly names
#     formatted_data = None
#     if target_data:
#         formatted_data = TargetBasic(
#             target_name=target_data.get('name'),
#             gene_symbol=target_data.get('sym'),
#             uniprot_id=target_data.get('uniprot'),
#             description=target_data.get('description'),
#             development_level=target_data.get('tdl'),
#             protein_family=target_data.get('fam'),
#             novelty_score=target_data.get('novelty')
#         )
    
#     return TargetResponse(
#         success=success,
#         message=message or ("Target found successfully" if target_data else "Target not found"),
#         gene_symbol_queried=gene_symbol,
#         data=formatted_data
#     )

# def create_search_response(
#     targets_data: List[dict], 
#     search_term: str,
#     total_count: int,
#     skip: int,
#     limit: int,
#     success: bool = True,
#     message: Optional[str] = None
# ) -> TargetSearchResponse:
#     """
#     Create a standardized search response
    
#     Args:
#         targets_data: List of target data from GraphQL
#         search_term: Search term that was used
#         total_count: Total number of matching targets
#         skip: Number of items skipped
#         limit: Maximum items per page
#         success: Whether the query was successful
#         message: Optional message
        
#     Returns:
#         Formatted TargetSearchResponse
#     """
#     # Convert each target to Galaxy-friendly format
#     formatted_targets = []
#     for target_data in targets_data:
#         formatted_target = TargetBasic(
#             target_name=target_data.get('name'),
#             gene_symbol=target_data.get('sym'),
#             uniprot_id=target_data.get('uniprot'),
#             description=target_data.get('description'),
#             development_level=target_data.get('tdl'),
#             protein_family=target_data.get('fam'),
#             novelty_score=target_data.get('novelty')
#         )
#         formatted_targets.append(formatted_target)
    
#     return TargetSearchResponse(
#         success=success,
#         message=message or f"Found {total_count} targets matching '{search_term}'",
#         search_term=search_term,
#         data=formatted_targets,
#         pagination=PaginationInfo(
#             total_count=total_count,
#             returned_count=len(formatted_targets),
#             skip=skip,
#             limit=limit
#         )
#     )

# def create_error_response(
#     message: str,
#     errors: Optional[List[dict]] = None,
#     request_id: Optional[str] = None
# ) -> ErrorResponse:
#     """
#     Create a standardized error response
    
#     Args:
#         message: Main error message
#         errors: List of detailed errors
#         request_id: Unique request identifier
        
#     Returns:
#         Formatted ErrorResponse
#     """
#     error_details = []
#     if errors:
#         for error in errors:
#             error_details.append(ErrorDetail(
#                 field=error.get('field'),
#                 message=error.get('message', 'Unknown error'),
#                 error_code=error.get('code')
#             ))
    
#     return ErrorResponse(
#         message=message,
#         errors=error_details,
#         request_id=request_id
#     )

# if __name__ == "__main__":
#     # Test the models when run directly
#     print("Testing Pydantic response models...")
    
#     # Test creating a target response
#     sample_target_data = {
#         'name': 'Epidermal growth factor receptor',
#         'sym': 'EGFR',
#         'uniprot': 'P00533',
#         'tdl': 'Tclin',
#         'novelty': 45.2
#     }
    
#     response = create_target_response(sample_target_data, 'EGFR')
#     print("Sample target response:")
#     print(response.model_dump_json(indent=2))