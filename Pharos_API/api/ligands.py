"""
FastAPI endpoints for ligand-related operations
Provides REST API interface for Galaxy integration
"""

import sys
import os
from typing import Optional, List
from fastapi import APIRouter, HTTPException, Query, Path
from fastapi.responses import Response
import csv
import io

import logging

logger = logging.getLogger(__name__)

# Add parent directory to Python path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.ligand_service import LigandService, check_ligand_service_health
from schemas.responses import (
    LigandResponse, LigandSearchResponse, LigandWithTargetsResponse,
    ErrorResponse, LigandBatchResponse, LigandWithTargets
)
from config import settings
from schemas.requests import LigandBatchRequest

# Create router for ligand endpoints
router = APIRouter(
    prefix="/ligands",
    tags=["ligands"],
    responses={
        404: {"description": "Ligand not found"},
        500: {"description": "Internal server error"}
    }
)

@router.get("/health")
async def get_ligand_service_health():
    """
    Health check for ligand service
    
    Returns service status and basic functionality test
    """
    health_status = await check_ligand_service_health()
    return health_status

@router.get("/{ligand_id}", response_model=LigandResponse)
async def get_ligand(
    ligand_id: str = Path(
        ..., 
        description="Ligand identifier (name, ChEMBL ID, etc.)",
        example="haloperidol"
    ),
    format: Optional[str] = Query(
        "json", 
        description="Response format: json, csv, or tsv",
        regex="^(json|csv|tsv)$"
    )
) -> LigandResponse:
    """
    Get basic ligand information by ligand ID or name
    
    - **ligand_id**: Ligand identifier to query (name, ChEMBL ID, drug name)
    - **format**: Response format (json, csv, tsv)
    
    Returns detailed ligand information including:
    - Ligand name and description
    - Drug status (approved drug or compound)
    - Chemical structure (SMILES notation)
    - Activity count and target count
    - Synonyms and identifiers
    """
    try:
        # Get ligand data from service
        result = await LigandService.get_ligand_basic(ligand_id)
        
        # Handle CSV/TSV format requests
        if format.lower() in ["csv", "tsv"]:
            return await _format_ligand_as_csv(result, format.lower())
        
        # Return JSON response (default)
        if not result.success:
            raise HTTPException(status_code=404, detail=result.message)
            
        return result
        
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Internal server error: {str(e)}"
        )

@router.get("", response_model=LigandSearchResponse)
async def search_ligands(
    search: str = Query(
        ..., 
        description="Search term (ligand name, indication, or keyword)",
        example="aspirin",
        min_length=2,
        max_length=100
    ),
    skip: int = Query(
        0, 
        description="Number of results to skip (for pagination)",
        ge=0
    ),
    limit: int = Query(
        10,
        description="Maximum number of results to return",
        ge=1,
        le=100
    ),
    format: Optional[str] = Query(
        "json",
        description="Response format: json, csv, or tsv", 
        regex="^(json|csv|tsv)$"
    )
) -> LigandSearchResponse:
    """
    Search for ligands by name, indication, or keyword
    
    - **search**: Search term (minimum 2 characters)
    - **skip**: Number of results to skip for pagination
    - **limit**: Maximum results per page (1-100)  
    - **format**: Response format (json, csv, tsv)
    
    Returns paginated list of matching ligands with:
    - Total count and pagination info
    - Ligand details for each match
    - Search term used
    
    **Example searches:**
    - `aspirin` - Find ligands containing "aspirin"
    - `kinase` - Find kinase inhibitors
    - `cancer` - Find cancer-related compounds
    
    **Note**: Search matches against ligand names and descriptions in Pharos database
    """
    try:
        # Get search results from service
        result = await LigandService.search_ligands(search, skip, limit)
        
        # Handle CSV/TSV format requests
        if format.lower() in ["csv", "tsv"]:
            return await _format_search_results_as_csv(result, format.lower())
        
        # Return JSON response (default) 
        return result
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Search failed: {str(e)}"
        )

@router.get("/{ligand_id}/targets", response_model=LigandWithTargetsResponse)
async def get_ligand_targets(
    ligand_id: str = Path(
        ...,
        description="Ligand identifier (name, ChEMBL ID, etc.)",
        example="haloperidol"
    ),
    max_targets: int = Query(
        10,
        description="Maximum number of targets to return",
        ge=1,
        le=50
    ),
    format: Optional[str] = Query(
        "json",
        description="Response format: json, csv, or tsv",
        regex="^(json|csv|tsv)$"
    )
):
    """
    Get ligand information with associated targets (proteins)

    - **ligand_id**: Ligand identifier (name, ChEMBL ID, etc.)
    - **max_targets**: Maximum number of associated targets to return (1-50)
    - **format**: Response format (json, csv, tsv)

    Returns ligand info plus associated target information including:
    - Basic ligand information (name, ChEMBL ID, SMILES, drug status, etc.)
    - List of associated target proteins
    - Target details (gene symbol, UniProt ID, development level, etc.)

    **Example:**
    - `/ligands/haloperidol/targets` - Get haloperidol with target associations
    - `/ligands/aspirin/targets?max_targets=20` - Get aspirin with up to 20 targets
    - `/ligands/imatinib/targets?format=csv` - Download as CSV
    """
    try:
        # Get ligand with targets from service
        result = await LigandService.get_ligand_with_targets(ligand_id, max_targets)

        # Handle CSV/TSV format requests
        if format.lower() in ["csv", "tsv"]:
            return await _format_ligand_targets_as_csv(result, format.lower())

        # Return JSON response (default)
        if not result.success:
            raise HTTPException(status_code=404, detail=result.message)

        return result

    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )

# Helper functions for CSV formatting
async def _format_ligand_as_csv(result: LigandResponse, format_type: str) -> Response:
    """
    Convert ligand response to CSV/TSV format
    """
    if not result.success or not result.data:
        raise HTTPException(status_code=404, detail="Ligand not found")
    
    # Prepare CSV data
    delimiter = "," if format_type == "csv" else "\t"
    output = io.StringIO()
    
    # CSV headers (Galaxy-friendly names)
    headers = [
        "Ligand_Name", "Description", "Is_Drug", "Drug_Status",
        "SMILES", "Activity_Count", "Target_Count", "Synonyms", "ChEMBL_ID"
    ]
    
    writer = csv.writer(output, delimiter=delimiter)
    writer.writerow(headers)
    
    # Data row
    data = result.data
    writer.writerow([
        data.ligand_name or "",
        data.description or "",
        data.is_drug if data.is_drug is not None else "",
        data.drug_status or "",
        data.smiles or "",
        data.activity_count if data.activity_count is not None else "",
        data.target_count if data.target_count is not None else "",
        data.synonyms or "",
        data.chembl_id or ""
    ])
    
    # Prepare response
    content = output.getvalue()
    media_type = "text/csv" if format_type == "csv" else "text/tab-separated-values"
    filename = f"ligand_{result.ligand_id_queried}.{format_type}"
    
    return Response(
        content=content,
        media_type=media_type,
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )

async def _format_search_results_as_csv(result: LigandSearchResponse, format_type: str) -> Response:
    """
    Convert search results to CSV/TSV format
    """
    # Prepare CSV data
    delimiter = "," if format_type == "csv" else "\t"
    output = io.StringIO()
    
    # CSV headers
    headers = [
        "Ligand_Name", "Description", "Is_Drug", "Drug_Status",
        "SMILES", "Activity_Count", "Target_Count", "Synonyms", "ChEMBL_ID"
    ]
    
    writer = csv.writer(output, delimiter=delimiter)
    writer.writerow(headers)
    
    # Data rows
    for ligand in result.data:
        writer.writerow([
            ligand.ligand_name or "",
            ligand.description or "",
            ligand.is_drug if ligand.is_drug is not None else "",
            ligand.drug_status or "",
            ligand.smiles or "",
            ligand.activity_count if ligand.activity_count is not None else "",
            ligand.target_count if ligand.target_count is not None else "",
            ligand.synonyms or "",
            ligand.chembl_id or ""
        ])
    
    # Prepare response
    content = output.getvalue()
    media_type = "text/csv" if format_type == "csv" else "text/tab-separated-values"
    filename = f"ligand_search_{result.search_term}.{format_type}"
    
    return Response(
        content=content,
        media_type=media_type,
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )

@router.post("/batch", response_model=LigandBatchResponse)
async def get_ligands_batch(
    request: LigandBatchRequest
):
    """
    Get multiple ligands in a single batch request
    
    This endpoint allows querying multiple ligand identifiers at once, which is much more efficient
    than making individual requests for each ligand. Useful for Galaxy workflows processing
    lists of compounds from chemical screens, drug databases, or other high-throughput analyses.
    
    **Example Request Body:**
    ```json
    {
        "ligand_ids": ["haloperidol", "aspirin", "imatinib"],
        "format": "json"
    }
    ```
    
    **Features:**
    - Queries up to 100 ligand IDs per request
    - Parallel processing for fast results
    - Returns both successful and failed queries
    - Supports JSON, CSV, and TSV output formats
    
    **Use Cases:**
    - Process compound lists from chemical screens
    - Bulk lookup of drug information
    - Galaxy workflow integration for high-throughput data
    
    Args:
        request: LigandBatchRequest containing list of ligand IDs and format
        
    Returns:
        LigandBatchResponse with results for all queried ligand IDs
        
    Raises:
        HTTPException: If request validation fails (e.g., too many ligands, invalid format)
    """
    try:
        # Call the batch service method
        result = await LigandService.get_ligands_batch(request.ligand_ids)
        
        # Handle CSV/TSV format if requested
        if request.format.lower() in ["csv", "tsv"]:
            return await _format_batch_ligands_as_csv(result, request.format.lower())
        
        # Return JSON response
        return result
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error in batch ligands endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error processing batch request")

# Drug filtering endpoint
@router.get("/drugs")
async def get_approved_drugs(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100)
):
    """
    Get only approved drugs (filter isdrug=true) - Future feature
    
    Will provide filtered list of approved drugs only,
    excluding research compounds and investigational agents.
    """
    raise HTTPException(
        status_code=501,
        detail={
            "message": "Drug filtering not yet implemented",
            "workaround": "Use /ligands search and filter results by drug_status='Drug'",
            "planned_features": [
                "Filter by approval status",
                "Clinical trial phase filtering",
                "Indication-based search"
            ]
        }
    )


async def _format_ligand_targets_as_csv(result: LigandWithTargetsResponse, format_type: str) -> Response:
    """
    Convert ligand with targets response to CSV/TSV format
    """
    if not result.success or not result.data:
        raise HTTPException(status_code=404, detail="Ligand not found")

    # Prepare CSV data
    delimiter = "," if format_type == "csv" else "\t"
    output = io.StringIO()

    # CSV headers
    headers = [
        "Ligand_Name", "ChEMBL_ID", "Is_Drug", "SMILES",
        "Target_Name", "Gene_Symbol", "UniProt_ID", "Development_Level"
    ]

    writer = csv.writer(output, delimiter=delimiter)
    writer.writerow(headers)

    # Data rows - one row per target association
    data = result.data
    if data.associated_targets and len(data.associated_targets) > 0:
        for target in data.associated_targets:
            writer.writerow([
                data.ligand_name or "",
                data.chembl_id or "",
                "Yes" if data.is_drug else "No" if data.is_drug is False else "Unknown",
                (data.smiles[:50] + "...") if data.smiles and len(data.smiles) > 50 else (data.smiles or ""),
                target.target_name or "",
                target.gene_symbol or "",
                target.uniprot_id or "",
                target.development_level or ""
            ])
    else:
        # If no targets, still write one row with ligand info
        writer.writerow([
            data.ligand_name or "",
            data.chembl_id or "",
            "Yes" if data.is_drug else "No" if data.is_drug is False else "Unknown",
            (data.smiles[:50] + "...") if data.smiles and len(data.smiles) > 50 else (data.smiles or ""),
            "No associated targets",
            "",
            "",
            ""
        ])

    # Prepare response
    content = output.getvalue()
    media_type = "text/csv" if format_type == "csv" else "text/tab-separated-values"
    filename = f"ligand_{result.ligand_id_queried}_targets.{format_type}"

    return Response(
        content=content,
        media_type=media_type,
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )

async def _format_batch_ligands_as_csv(result: LigandBatchResponse, format_type: str) -> Response:
    """
    Convert batch ligand response to CSV/TSV format
    
    Args:
        result: LigandBatchResponse object
        format_type: "csv" or "tsv"
        
    Returns:
        Response with CSV/TSV content
    """
    delimiter = "," if format_type == "csv" else "\t"
    output = io.StringIO()
    
    # CSV headers
    headers = [
        "Ligand_ID",
        "Found",
        "Ligand_Name",
        "ChEMBL_ID",
        "Is_Drug",
        "SMILES",
        "Description",
        "Activity_Count",
        "Target_Count",
        "Error"
    ]
    
    writer = csv.writer(output, delimiter=delimiter)
    writer.writerow(headers)
    
    # Write data rows
    for item in result.results:
        if item.found and item.data:
            # Successful result
            writer.writerow([
                item.ligand_id,
                "true",
                item.data.ligand_name or "",
                item.data.chembl_id or "",
                "Yes" if item.data.is_drug else "No" if item.data.is_drug is False else "Unknown",
                (item.data.smiles[:50] + "...") if item.data.smiles and len(item.data.smiles) > 50 else (item.data.smiles or ""),
                (item.data.description[:100] + "...") if item.data.description and len(item.data.description) > 100 else (item.data.description or ""),
                str(item.data.activity_count) if item.data.activity_count is not None else "",
                str(item.data.target_count) if item.data.target_count is not None else "",
                ""
            ])
        else:
            # Failed result
            writer.writerow([
                item.ligand_id,
                "false",
                "",
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
    filename = f"ligands_batch_{len(result.results)}_items.{extension}"
    
    return Response(
        content=content,
        media_type=f"text/{format_type}",
        headers={
            "Content-Disposition": f"attachment; filename={filename}",
            "Content-Type": f"text/{format_type}; charset=utf-8"
        }
    )