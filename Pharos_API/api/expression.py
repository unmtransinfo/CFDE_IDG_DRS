"""
FastAPI endpoints for tissue expression queries
Provides REST API interface for target expression data
"""

import sys
import os
from fastapi import APIRouter, HTTPException, Path

# Add parent directory to Python path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.expression_service import (
    ExpressionService,
    check_expression_service_health,
)
from schemas.responses import ExpressionResponse, TissueExpressionCheck

# Create router for expression endpoints
router = APIRouter(
    prefix="/expression",
    tags=["expression"],
    responses={
        404: {"description": "Target not found"},
        500: {"description": "Internal server error"},
    },
)


@router.get("/health")
async def get_expression_service_health():
    """Health check for expression service"""
    return await check_expression_service_health()


@router.get("/{identifier}", response_model=ExpressionResponse)
async def get_target_expressions(
    identifier: str = Path(
        ...,
        description="UniProt accession (e.g., P04035) or gene symbol (e.g., HMGCR)",
        example="P04035",
    ),
) -> ExpressionResponse:
    """
    Get all tissue expression records for a target.

    Accepts either a UniProt accession (e.g., `P04035`) or a gene symbol
    (e.g., `HMGCR`). The endpoint auto-detects which identifier was passed.

    Returns all tissue expression records from Pharos data sources (HPA, GTEx, etc.)
    including tissue name, expression value, qualitative level, and UBERON ID.
    """
    try:
        result = await ExpressionService.get_expressions(identifier)

        if not result.success:
            # Differentiate not-found from other errors
            message = (result.message or "").lower()
            if "not found" in message:
                raise HTTPException(status_code=404, detail=result.message)
            raise HTTPException(status_code=400, detail=result.message)

        return result

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}",
        )


@router.get("/{identifier}/{uberon_id}", response_model=TissueExpressionCheck)
async def check_tissue_expression(
    identifier: str = Path(
        ...,
        description="UniProt accession or gene symbol",
        example="P04035",
    ),
    uberon_id: str = Path(
        ...,
        description="UBERON tissue ontology ID (e.g., UBERON:0001134 for skeletal muscle)",
        example="UBERON:0001134",
    ),
) -> TissueExpressionCheck:
    """
    Check whether a target is expressed in a specific tissue.

    - **identifier**: UniProt accession (e.g., `P04035`) or gene symbol (e.g., `HMGCR`)
    - **uberon_id**: UBERON ontology ID (e.g., `UBERON:0001134` for skeletal muscle)

    Returns an `expressed` boolean plus all matching expression records across
    data sources (HPA, GTEx, etc.) with quantitative and qualitative values.

    **Example**: `/expression/P04035/UBERON:0001134` — is HMGCR expressed in skeletal muscle?
    """
    try:
        result = await ExpressionService.get_expression_for_tissue(identifier, uberon_id)

        if not result.success:
            message = (result.message or "").lower()
            if "not found" in message:
                raise HTTPException(status_code=404, detail=result.message)
            raise HTTPException(status_code=400, detail=result.message)

        return result

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}",
        )
