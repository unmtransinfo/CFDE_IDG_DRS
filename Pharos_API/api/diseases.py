"""
FastAPI endpoints for disease-related operations
Provides REST API interface for Galaxy integration
"""

import sys
import os
from typing import Optional, List
from fastapi import APIRouter, HTTPException, Query, Path
from fastapi.responses import Response
import logging
import csv
import io

# Add parent directory to Python path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
logger = logging.getLogger(__name__)

from services.disease_service import DiseaseService, check_disease_service_health
from schemas.responses import (
    DiseaseResponse, 
    DiseaseSearchResponse,
    DiseaseWithTargetsResponse,
    DiseaseBatchResponse,
    ErrorResponse
)
from schemas.requests import DiseaseBatchRequest 
from config import settings

# Create router for disease endpoints
router = APIRouter(
    prefix="/diseases",
    tags=["diseases"],
    responses={
        404: {"description": "Disease not found"},
        500: {"description": "Internal server error"}
    }
)

@router.get("/health")
async def get_disease_service_health():
    """
    Health check for disease service
    
    Returns service status and basic functionality test
    """
    health_status = await check_disease_service_health()
    return health_status

@router.get("/{disease_name}", response_model=DiseaseResponse)
async def get_disease(
    disease_name: str = Path(
        ..., 
        description="Disease name (e.g., asthma, diabetes, cancer)",
        example="asthma"
    ),
    format: str = Query(
        "json",
        description="Response format: json, csv, or tsv",
        regex="^(json|csv|tsv)$"
    )
):
    """
    Get detailed information about a specific disease
    
    **Parameters:**
    - **disease_name**: Disease name to query
    - **format**: Output format (json, csv, tsv)
    
    **Returns:**
    - Disease information including MONDO ID, description, and association counts
    
    **Example:**
    - `/diseases/asthma` - Get asthma information as JSON
    - `/diseases/asthma?format=csv` - Download asthma data as CSV
    """
    try:
        # Get disease data from service
        result = await DiseaseService.get_disease_basic(disease_name)
        
        # Handle not found
        if not result.success or not result.data:
            raise HTTPException(
                status_code=404,
                detail=f"Disease '{disease_name}' not found in Pharos database"
            )
        
        # Return based on format
        if format == "json":
            return result
        
        elif format in ["csv", "tsv"]:
            # Prepare CSV data
            delimiter = ',' if format == 'csv' else '\t'
            
            output = io.StringIO()
            writer = csv.writer(output, delimiter=delimiter)
            
            # Write headers
            headers = [
                "Disease_Name",
                "MONDO_ID",
                "Description",
                "Association_Count",
                "Direct_Association_Count",
                "Is_Rare_Disease",
                "Datasource_Count"
            ]
            writer.writerow(headers)
            
            # Write data
            disease = result.data
            writer.writerow([
                disease.disease_name or "",
                disease.mondo_id or "",
                (disease.description[:200] + "...") if disease.description and len(disease.description) > 200 else (disease.description or ""),
                disease.association_count or 0,
                disease.direct_association_count or 0,
                "Yes" if disease.is_rare else "No",
                disease.datasource_count or 0
            ])
            
            # Return as downloadable file
            content = output.getvalue()
            filename = f"disease_{disease_name.replace(' ', '_')}.{format}"
            
            return Response(
                content=content,
                media_type=f"text/{format}",
                headers={"Content-Disposition": f"attachment; filename={filename}"}
            )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )

@router.get("/{disease_name}/targets", response_model=DiseaseWithTargetsResponse)
async def get_disease_targets(
    disease_name: str = Path(
        ...,
        description="Disease name to query",
        example="asthma"
    ),
    format: str = Query(
        "json",
        description="Response format: json, csv, or tsv",
        regex="^(json|csv|tsv)$"
    )
):
    """
    Get disease information with associated targets
    
    **Parameters:**
    - **disease_name**: Disease name to query
    - **format**: Output format (json, csv, tsv)
    
    **Returns:**
    - Disease information with list of associated targets
    
    **Example:**
    - `/diseases/asthma/targets` - Get asthma with target associations
    - `/diseases/asthma/targets?format=csv` - Download as CSV
    """
    try:
        # Get disease with targets from service
        result = await DiseaseService.get_disease_with_targets(disease_name)
        
        # Handle not found
        if not result.success or not result.data:
            raise HTTPException(
                status_code=404,
                detail=f"Disease '{disease_name}' not found"
            )
        
        # Return based on format
        if format == "json":
            return result
        
        elif format in ["csv", "tsv"]:
            # Prepare CSV data with targets
            delimiter = ',' if format == 'csv' else '\t'
            
            output = io.StringIO()
            writer = csv.writer(output, delimiter=delimiter)
            
            # Write headers
            headers = [
                "Disease_Name",
                "MONDO_ID",
                "Target_Name",
                "Gene_Symbol",
                "UniProt_ID",
                "Development_Level"
            ]
            writer.writerow(headers)
            
            # Write data for each target
            disease = result.data
            if disease.associated_targets:
                for target in disease.associated_targets:
                    writer.writerow([
                        disease.disease_name or "",
                        disease.mondo_id or "",
                        target.target_name or "",
                        target.gene_symbol or "",
                        target.uniprot_id or "",
                        target.development_level or ""
                    ])
            else:
                # Write disease info even if no targets
                writer.writerow([
                    disease.disease_name or "",
                    disease.mondo_id or "",
                    "No targets found",
                    "",
                    "",
                    ""
                ])
            
            # Return as downloadable file
            content = output.getvalue()
            filename = f"disease_{disease_name.replace(' ', '_')}_targets.{format}"
            
            return Response(
                content=content,
                media_type=f"text/{format}",
                headers={"Content-Disposition": f"attachment; filename={filename}"}
            )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )

@router.get("/", response_model=DiseaseSearchResponse)
async def search_diseases(
    search: str = Query(
        ...,
        description="Search term to find diseases",
        min_length=2,
        example="cancer"
    ),
    skip: int = Query(
        0,
        description="Number of results to skip (pagination)",
        ge=0
    ),
    limit: int = Query(
        10,
        description="Maximum number of results to return",
        ge=1,
        le=100
    ),
    format: str = Query(
        "json",
        description="Response format: json, csv, or tsv",
        regex="^(json|csv|tsv)$"
    )
):
    """
    Search for diseases by name or keyword
    
    **Parameters:**
    - **search**: Search term (required, min 2 characters)
    - **skip**: Results to skip for pagination (default: 0)
    - **limit**: Maximum results to return (1-100, default: 10)
    - **format**: Output format (json, csv, tsv)
    
    **Returns:**
    - List of diseases matching the search term with pagination info
    
    **Examples:**
    - `/diseases?search=cancer` - Search for cancer-related diseases
    - `/diseases?search=lung&limit=20` - Get 20 lung-related diseases
    - `/diseases?search=diabetes&format=csv` - Download as CSV
    """
    try:
        # Search diseases using service
        result = await DiseaseService.search_diseases(search, skip, limit)
        
        # Return based on format
        if format == "json":
            return result
        
        elif format in ["csv", "tsv"]:
            # Prepare CSV data
            delimiter = ',' if format == 'csv' else '\t'
            
            output = io.StringIO()
            writer = csv.writer(output, delimiter=delimiter)
            
            # Write headers
            headers = [
                "Disease_Name",
                "MONDO_ID",
                "Description",
                "Association_Count",
                "Direct_Association_Count",
                "Is_Rare_Disease",
                "Datasource_Count"
            ]
            writer.writerow(headers)
            
            # Write data for each disease
            for disease in result.data:
                writer.writerow([
                    disease.disease_name or "",
                    disease.mondo_id or "",
                    (disease.description[:200] + "...") if disease.description and len(disease.description) > 200 else (disease.description or ""),
                    disease.association_count or 0,
                    disease.direct_association_count or 0,
                    "Yes" if disease.is_rare else "No",
                    disease.datasource_count or 0
                ])
            
            # Return as downloadable file
            content = output.getvalue()
            filename = f"disease_search_{search.replace(' ', '_')}.{format}"
            
            return Response(
                content=content,
                media_type=f"text/{format}",
                headers={"Content-Disposition": f"attachment; filename={filename}"}
            )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )
    
@router.post("/batch", response_model=DiseaseBatchResponse)
async def get_diseases_batch(
    request: DiseaseBatchRequest
):
    """
    Get multiple diseases in a single batch request
    
    This endpoint allows querying multiple disease names at once, which is much more efficient
    than making individual requests for each disease. Useful for Galaxy workflows processing
    lists of diseases from GWAS studies, clinical trials, or other biomedical analyses.
    
    **Example Request Body:**
    ```json
    {
        "disease_names": ["asthma", "diabetes mellitus", "alzheimer disease"],
        "format": "json"
    }
    ```
    
    **Features:**
    - Queries up to 100 disease names per request
    - Parallel processing for fast results
    - Returns both successful and failed queries
    - Supports JSON, CSV, and TSV output formats
    
    **Use Cases:**
    - Process disease lists from GWAS studies
    - Bulk lookup of disease information
    - Galaxy workflow integration for phenotype analysis
    
    Args:
        request: DiseaseBatchRequest containing list of disease names and format
        
    Returns:
        DiseaseBatchResponse with results for all queried disease names
        
    Raises:
        HTTPException: If request validation fails (e.g., too many diseases, invalid format)
    """
    try:
        # Call the batch service method
        result = await DiseaseService.get_diseases_batch(request.disease_names)
        
        # Handle CSV/TSV format if requested
        if request.format.lower() in ["csv", "tsv"]:
            return await _format_batch_diseases_as_csv(result, request.format.lower())
        
        # Return JSON response
        return result
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error in batch diseases endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error processing batch request")

@router.get("/mondo/{mondo_id}", response_model=DiseaseResponse)
async def get_disease_by_mondo_id(
    mondo_id: str = Path(
        ...,
        description="MONDO disease identifier (e.g., MONDO:0004979)",
        example="MONDO:0004979"
    ),
    format: str = Query(
        "json",
        description="Response format: json, csv, or tsv",
        regex="^(json|csv|tsv)$"
    )
):
    """
    Get disease information by MONDO ID
    
    **Parameters:**
    - **mondo_id**: MONDO identifier (e.g., MONDO:0004979 for asthma)
    - **format**: Output format (json, csv, tsv)
    
    **Returns:**
    - Disease information for the specified MONDO ID
    
    **Example:**
    - `/diseases/mondo/MONDO:0004979` - Get disease by MONDO ID
    - `/diseases/mondo/MONDO:0004979?format=csv` - Download as CSV
    """
    try:
        # Get disease by MONDO ID from service
        result = await DiseaseService.get_disease_by_mondo_id(mondo_id)
        
        # Handle not found
        if not result.success or not result.data:
            raise HTTPException(
                status_code=404,
                detail=f"Disease with MONDO ID '{mondo_id}' not found"
            )
        
        # Return based on format
        if format == "json":
            return result
        
        elif format in ["csv", "tsv"]:
            # Prepare CSV data
            delimiter = ',' if format == 'csv' else '\t'
            
            output = io.StringIO()
            writer = csv.writer(output, delimiter=delimiter)
            
            # Write headers
            headers = [
                "Disease_Name",
                "MONDO_ID",
                "Description",
                "Association_Count",
                "Direct_Association_Count",
                "Is_Rare_Disease",
                "Datasource_Count"
            ]
            writer.writerow(headers)
            
            # Write data
            disease = result.data
            writer.writerow([
                disease.disease_name or "",
                disease.mondo_id or "",
                (disease.description[:200] + "...") if disease.description and len(disease.description) > 200 else (disease.description or ""),
                disease.association_count or 0,
                disease.direct_association_count or 0,
                "Yes" if disease.is_rare else "No",
                disease.datasource_count or 0
            ])
            
            # Return as downloadable file
            content = output.getvalue()
            filename = f"disease_{mondo_id.replace(':', '_')}.{format}"
            
            return Response(
                content=content,
                media_type=f"text/{format}",
                headers={"Content-Disposition": f"attachment; filename={filename}"}
            )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )
    
async def _format_batch_diseases_as_csv(result: DiseaseBatchResponse, format_type: str) -> Response:
    """
    Convert batch disease response to CSV/TSV format
    
    Args:
        result: DiseaseBatchResponse object
        format_type: "csv" or "tsv"
        
    Returns:
        Response with CSV/TSV content
    """
    delimiter = "," if format_type == "csv" else "\t"
    output = io.StringIO()
    
    # CSV headers - SIMPLIFIED
    headers = [
        "Disease_Name",
        "Found",
        "MONDO_ID",
        "Description",  # ← SINGLE DESCRIPTION FIELD
        "Association_Count",
        "Direct_Association_Count",
        "Is_Rare_Disease",
        "Datasource_Count",
        "Error"
    ]
    
    writer = csv.writer(output, delimiter=delimiter)
    writer.writerow(headers)
    
    # Write data rows
    for item in result.results:
        if item.found and item.data:
            # Successful result
            writer.writerow([
                item.disease_name,
                "true",
                item.data.mondo_id or "",
                (item.data.description[:150] + "...") if item.data.description and len(item.data.description) > 150 else (item.data.description or ""),  # ← ONLY description
                str(item.data.association_count) if item.data.association_count is not None else "",
                str(item.data.direct_association_count) if item.data.direct_association_count is not None else "",
                "Yes" if item.data.is_rare else "No" if item.data.is_rare is False else "Unknown",
                str(item.data.datasource_count) if item.data.datasource_count is not None else "",
                ""
            ])
        else:
            # Failed result - 9 columns total
            writer.writerow([
                item.disease_name,
                "false",
                "",
                "",
                "",
                "",
                "",
                "",
                item.error or "Not found"
            ])
    
    # Create response
    content = output.getvalue()
    extension = format_type
    filename = f"diseases_batch_{len(result.results)}_items.{extension}"
    
    return Response(
        content=content,
        media_type=f"text/{format_type}",
        headers={
            "Content-Disposition": f"attachment; filename={filename}",
            "Content-Type": f"text/{format_type}; charset=utf-8"
        }
    )
    
# async def _format_batch_diseases_as_csv(result: DiseaseBatchResponse, format_type: str) -> Response:
#     """
#     Convert batch disease response to CSV/TSV format
    
#     Args:
#         result: DiseaseBatchResponse object
#         format_type: "csv" or "tsv"
        
#     Returns:
#         Response with CSV/TSV content
#     """
#     delimiter = "," if format_type == "csv" else "\t"
#     output = io.StringIO()
    
#     # CSV headers
#     headers = [
#         "Disease_Name",
#         "Found",
#         "MONDO_ID",
#         "UniProt_Description",
#         "DO_Description",
#         "MONDO_Description",
#         "Association_Count",
#         "Direct_Association_Count",
#         "Is_Rare_Disease",
#         "Datasource_Count",
#         "Error"
#     ]
    
#     writer = csv.writer(output, delimiter=delimiter)
#     writer.writerow(headers)
    
#     # Write data rows
#     for item in result.results:
#         if item.found and item.data:
#             # Successful result
#             writer.writerow([
#                 item.disease_name,
#                 "true",
#                 item.data.mondo_id or "",
#                 (item.data.uniprot_description[:100] + "...") if item.data.uniprot_description and len(item.data.uniprot_description) > 100 else (item.data.uniprot_description or ""),
#                 (item.data.do_description[:100] + "...") if item.data.do_description and len(item.data.do_description) > 100 else (item.data.do_description or ""),
#                 (item.data.mondo_description[:100] + "...") if item.data.mondo_description and len(item.data.mondo_description) > 100 else (item.data.mondo_description or ""),
#                 str(item.data.association_count) if item.data.association_count is not None else "",
#                 str(item.data.direct_association_count) if item.data.direct_association_count is not None else "",
#                 "Yes" if item.data.is_rare else "No" if item.data.is_rare is False else "Unknown",
#                 str(item.data.datasource_count) if item.data.datasource_count is not None else "",
#                 ""
#             ])
#         else:
#             # Failed result
#             writer.writerow([
#                 item.disease_name,
#                 "false",
#                 "",
#                 "",
#                 "",
#                 "",
#                 "",
#                 "",
#                 "",
#                 "",
#                 item.error or "Not found"
#             ])
    
#     # Create response
#     content = output.getvalue()
#     extension = format_type
#     filename = f"diseases_batch_{len(result.results)}_items.{extension}"
    
#     return Response(
#         content=content,
#         media_type=f"text/{format_type}",
#         headers={
#             "Content-Disposition": f"attachment; filename={filename}",
#             "Content-Type": f"text/{format_type}; charset=utf-8"
#         }
#     )

# CSV column information endpoint
@router.get("/info/csv-columns")
async def get_csv_column_info():
    """
    Get information about available CSV export columns
    
    Useful for Galaxy tool developers to understand data structure
    """
    return {
        "basic_disease_columns": [
            {"name": "Disease_Name", "type": "string", "description": "Full disease name"},
            {"name": "MONDO_ID", "type": "string", "description": "MONDO database identifier"},
            {"name": "Description", "type": "string", "description": "Disease description"},
            {"name": "Association_Count", "type": "integer", "description": "Total target associations"},
            {"name": "Direct_Association_Count", "type": "integer", "description": "Direct target associations"},
            {"name": "Is_Rare_Disease", "type": "boolean", "description": "GARD rare disease flag"},
            {"name": "Datasource_Count", "type": "integer", "description": "Number of data sources"}
        ],
        "disease_targets_columns": [
            {"name": "Disease_Name", "type": "string", "description": "Full disease name"},
            {"name": "MONDO_ID", "type": "string", "description": "MONDO database identifier"},
            {"name": "Target_Name", "type": "string", "description": "Associated target protein name"},
            {"name": "Gene_Symbol", "type": "string", "description": "Target gene symbol"},
            {"name": "UniProt_ID", "type": "string", "description": "UniProt identifier"},
            {"name": "Development_Level", "type": "string", "description": "Target development level (TDL)"}
        ],
        "supported_formats": ["json", "csv", "tsv"],
        "galaxy_integration": {
            "csv_delimiter": ",",
            "tsv_delimiter": "\\t",
            "encoding": "utf-8"
        }
    }