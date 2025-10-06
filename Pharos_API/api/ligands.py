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

# Add parent directory to Python path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.ligand_service import LigandService, check_ligand_service_health
from schemas.responses import (
    LigandResponse, LigandSearchResponse,
    ErrorResponse
)
from config import settings

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

@router.get("/{ligand_id}/targets")
async def get_ligand_targets(
    ligand_id: str = Path(
        ...,
        description="Ligand identifier",
        example="haloperidol"  
    ),
    max_targets: int = Query(
        5,
        description="Maximum number of targets to return",
        ge=1,
        le=50
    )
):
    """
    Get ligand information with target interactions (cross-relationship feature)
    
    **NOTE**: This endpoint is planned for future version.
    
    - **ligand_id**: Ligand identifier to query
    - **max_targets**: Maximum number of associated targets to return
    
    Will return ligand info plus target interaction data including:
    - Target proteins that bind this ligand
    - Activity measurements (IC50, Ki, etc.)
    - Mechanism of action
    """
    raise HTTPException(
        status_code=501,
        detail={
            "message": "Ligand-target interactions endpoint planned for future version",
            "available_endpoints": [
                f"/ligands/{ligand_id}",
                "/ligands?search=term"
            ],
            "planned_features": [
                "Target binding data",
                "Activity measurements",
                "Mechanism of action"
            ],
            "estimated_completion": "Next version"
        }
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

# Batch operations (future feature)
@router.post("/batch")
async def get_ligands_batch():
    """
    Get multiple ligands in a single request (future feature)
    
    **NOTE**: This endpoint will be implemented in future version
    to support batch operations like: POST /ligands/batch with 
    body containing list of ligand identifiers.
    """
    raise HTTPException(
        status_code=501,
        detail={
            "message": "Batch operations not yet implemented",
            "planned_features": [
                "Multiple ligands in single request",
                "Bulk CSV export", 
                "Galaxy workflow integration",
                "Chemical structure-based search"
            ],
            "workaround": "Use individual requests for now"
        }
    )

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