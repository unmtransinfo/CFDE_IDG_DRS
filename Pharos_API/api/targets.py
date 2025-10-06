"""
FastAPI endpoints for target-related operations
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

from services.target_service import TargetService, check_target_service_health
from schemas.responses import (
    TargetResponse, TargetSearchResponse, TargetWithDiseasesResponse,
    ErrorResponse
)
from config import settings

# Create router for target endpoints
router = APIRouter(
    prefix="/targets",
    tags=["targets"],
    responses={
        404: {"description": "Target not found"},
        500: {"description": "Internal server error"}
    }
)

@router.get("/health")
async def get_target_service_health():
    """
    Health check for target service
    
    Returns service status and basic functionality test
    """
    health_status = await check_target_service_health()
    return health_status

@router.get("/{gene_symbol}", response_model=TargetResponse)
async def get_target(
    gene_symbol: str = Path(
        ..., 
        description="Gene symbol (e.g., EGFR, TP53, ACE2)",
        example="EGFR"
    ),
    format: Optional[str] = Query(
        "json", 
        description="Response format: json or csv",
        regex="^(json|csv|tsv)$"
    )
) -> TargetResponse:
    """
    Get basic target information by gene symbol
    
    - **gene_symbol**: Gene symbol to query (case-insensitive)
    - **format**: Response format (json, csv, tsv)
    
    Returns detailed target information including:
    - Target name and gene symbol
    - UniProt ID and description  
    - Development level (Tclin, Tchem, Tbio, Tdark)
    - Protein family and novelty score
    """
    try:
        # Get target data from service
        result = await TargetService.get_target_basic(gene_symbol)
        
        # Handle CSV/TSV format requests
        if format.lower() in ["csv", "tsv"]:
            return await _format_target_as_csv(result, format.lower())
        
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

@router.get("", response_model=TargetSearchResponse)
async def search_targets(
    search: str = Query(
        ..., 
        description="Search term (gene symbol, target name, or keyword)",
        example="kinase",
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
) -> TargetSearchResponse:
    """
    Search for targets by name, gene symbol, or keyword
    
    - **search**: Search term (minimum 2 characters)
    - **skip**: Number of results to skip for pagination
    - **limit**: Maximum results per page (1-100)  
    - **format**: Response format (json, csv, tsv)
    
    Returns paginated list of matching targets with:
    - Total count and pagination info
    - Target details for each match
    - Search term used
    
    **Example searches:**
    - `kinase` - Find all targets containing "kinase"
    - `EGFR` - Find targets matching gene symbol
    - `growth factor` - Find targets with "growth factor" in name
    """
    try:
        # Get search results from service
        result = await TargetService.search_targets(search, skip, limit)
        
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

@router.get("/{gene_symbol}/diseases", response_model=TargetWithDiseasesResponse)
async def get_target_diseases(
    gene_symbol: str = Path(
        ...,
        description="Gene symbol (e.g., EGFR, TP53)",
        example="EGFR"  
    ),
    max_diseases: int = Query(
        5,
        description="Maximum number of diseases to return",
        ge=1,
        le=50
    )
) -> TargetWithDiseasesResponse:
    """
    Get target information with associated diseases (cross-relationship demo)
    
    **NOTE**: This endpoint is currently under development due to 
    GraphQL query syntax issues. Will be available in future version.
    
    - **gene_symbol**: Gene symbol to query
    - **max_diseases**: Maximum number of associated diseases to return
    
    Returns target info plus associated disease information.
    """
    # For now, return a helpful message about the feature being under development
    raise HTTPException(
        status_code=501,
        detail={
            "message": "Disease associations endpoint under development",
            "reason": "GraphQL query syntax needs refinement",
            "available_endpoints": [
                f"/targets/{gene_symbol}",
                "/targets?search=term"
            ],
            "estimated_completion": "Next version"
        }
    )

# Helper functions for CSV formatting
async def _format_target_as_csv(result: TargetResponse, format_type: str) -> Response:
    """
    Convert target response to CSV/TSV format
    """
    if not result.success or not result.data:
        raise HTTPException(status_code=404, detail="Target not found")
    
    # Prepare CSV data
    delimiter = "," if format_type == "csv" else "\t"
    output = io.StringIO()
    
    # CSV headers (Galaxy-friendly names)
    headers = [
        "Target_Name", "Gene_Symbol", "UniProt_ID", "Description",
        "Development_Level", "Protein_Family", "Novelty_Score"
    ]
    
    writer = csv.writer(output, delimiter=delimiter)
    writer.writerow(headers)
    
    # Data row
    data = result.data
    writer.writerow([
        data.target_name or "",
        data.gene_symbol or "",
        data.uniprot_id or "",
        data.description or "",
        data.development_level or "",
        data.protein_family or "",
        data.novelty_score or ""
    ])
    
    # Prepare response
    content = output.getvalue()
    media_type = "text/csv" if format_type == "csv" else "text/tab-separated-values"
    filename = f"target_{result.gene_symbol_queried}.{format_type}"
    
    return Response(
        content=content,
        media_type=media_type,
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )

async def _format_search_results_as_csv(result: TargetSearchResponse, format_type: str) -> Response:
    """
    Convert search results to CSV/TSV format
    """
    # Prepare CSV data
    delimiter = "," if format_type == "csv" else "\t"
    output = io.StringIO()
    
    # CSV headers
    headers = [
        "Target_Name", "Gene_Symbol", "UniProt_ID", "Description", 
        "Development_Level", "Protein_Family", "Novelty_Score"
    ]
    
    writer = csv.writer(output, delimiter=delimiter)
    writer.writerow(headers)
    
    # Data rows
    for target in result.data:
        writer.writerow([
            target.target_name or "",
            target.gene_symbol or "",
            target.uniprot_id or "",
            target.description or "",
            target.development_level or "",
            target.protein_family or "",
            target.novelty_score or ""
        ])
    
    # Prepare response
    content = output.getvalue()
    media_type = "text/csv" if format_type == "csv" else "text/tab-separated-values"
    filename = f"target_search_{result.search_term}.{format_type}"
    
    return Response(
        content=content,
        media_type=media_type,
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )

# Batch operations (future feature)
@router.post("/batch")
async def get_targets_batch():
    """
    Get multiple targets in a single request (future feature)
    
    **NOTE**: This endpoint will be implemented in future version
    to support batch operations like: POST /targets/batch with 
    body containing list of gene symbols.
    """
    raise HTTPException(
        status_code=501,
        detail={
            "message": "Batch operations not yet implemented",
            "planned_features": [
                "Multiple gene symbols in single request",
                "Bulk CSV export", 
                "Galaxy workflow integration"
            ],
            "workaround": "Use individual requests for now"
        }
    )

# Statistics endpoint for monitoring
@router.get("/stats")
async def get_target_stats():
    """
    Get statistics about target service usage (future feature)
    
    Will provide metrics like:
    - Most queried targets
    - Response times
    - Success rates
    - Popular search terms
    """
    raise HTTPException(
        status_code=501,
        detail={
            "message": "Statistics endpoint not yet implemented",
            "planned_metrics": [
                "Query frequency by target",
                "Average response times",
                "Success/error rates",
                "Popular search terms"
            ]
        }
    )