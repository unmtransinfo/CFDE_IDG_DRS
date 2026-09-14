"""
Expression service layer - Business logic for tissue expression queries
"""

import logging
import sys
import os
from typing import Optional, Dict, Any

# Add parent directory for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.graphql_client import query_pharos, PharosGraphQLError
from queries.expression_queries import (
    get_expression_query,
    is_uniprot_accession,
    validate_identifier,
    validate_uberon_id,
)
from schemas.responses import (
    ExpressionRecord,
    ExpressionResponse,
    TissueExpressionCheck,
)

logger = logging.getLogger(__name__)


def _parse_expression_record(raw: dict) -> ExpressionRecord:
    """Convert a raw GraphQL expression dict into an ExpressionRecord"""
    uberon = raw.get('uberon') or {}
    value = raw.get('value')
    try:
        value = float(value) if value is not None else None
    except (TypeError, ValueError):
        value = None
    return ExpressionRecord(
        tissue=raw.get('tissue'),
        value=value,
        qual=raw.get('qual'),
        uberon_id=uberon.get('uid'),
        uberon_name=uberon.get('name'),
        source_type=raw.get('type'),
    )


class ExpressionService:
    """
    Service class for target tissue-expression queries.
    Accepts either a UniProt accession or a gene symbol as the identifier.
    """

    @staticmethod
    async def _fetch_target_expressions(identifier: str) -> Optional[Dict[str, Any]]:
        """
        Fetch a target (with expressions) by UniProt accession first, falling
        back to gene-symbol lookup if it doesn't look like a UniProt ID or the
        UniProt lookup returns nothing.
        """
        cleaned = validate_identifier(identifier)

        # Choose query order based on identifier shape
        if is_uniprot_accession(cleaned):
            query_order = [('by_uniprot', cleaned.upper()), ('by_sym', cleaned.upper())]
        else:
            query_order = [('by_sym', cleaned.upper()), ('by_uniprot', cleaned.upper())]

        for query_name, variable_value in query_order:
            try:
                query = get_expression_query(query_name)
                result = await query_pharos(query, {"identifier": variable_value})
                if result.get('data') and result['data'].get('target'):
                    return result['data']['target']
            except PharosGraphQLError as e:
                logger.warning(f"{query_name} failed for '{cleaned}': {e}")
                continue

        return None

    @staticmethod
    async def get_expressions(identifier: str) -> ExpressionResponse:
        """Get all tissue expression records for a target"""
        try:
            target = await ExpressionService._fetch_target_expressions(identifier)
            if not target:
                return ExpressionResponse(
                    success=False,
                    message=f"Target not found for identifier '{identifier}'",
                    identifier_queried=identifier,
                    expression_count=0,
                    expressions=[],
                )

            raw_expressions = target.get('expressions') or []
            records = [_parse_expression_record(e) for e in raw_expressions]

            logger.info(f"Found {len(records)} expression records for {identifier}")

            return ExpressionResponse(
                success=True,
                message=f"Found {len(records)} expression records",
                identifier_queried=identifier,
                uniprot=target.get('uniprot'),
                sym=target.get('sym'),
                name=target.get('name'),
                tdl=target.get('tdl'),
                expression_count=len(records),
                expressions=records,
            )

        except ValueError as e:
            logger.error(f"Invalid identifier '{identifier}': {e}")
            return ExpressionResponse(
                success=False,
                message=f"Invalid identifier: {e}",
                identifier_queried=identifier,
                expression_count=0,
                expressions=[],
            )
        except Exception as e:
            logger.error(f"Unexpected error for identifier '{identifier}': {e}")
            return ExpressionResponse(
                success=False,
                message="An unexpected error occurred while fetching expression data",
                identifier_queried=identifier,
                expression_count=0,
                expressions=[],
            )

    @staticmethod
    async def get_expression_for_tissue(
        identifier: str,
        uberon_id: str,
    ) -> TissueExpressionCheck:
        """
        Check whether a target is expressed in a specific tissue (by UBERON ID).
        Returns all matching expression records across sources (HPA, GTEx, etc.).
        """
        try:
            cleaned_uberon = validate_uberon_id(uberon_id)
            target = await ExpressionService._fetch_target_expressions(identifier)

            if not target:
                return TissueExpressionCheck(
                    success=False,
                    message=f"Target not found for identifier '{identifier}'",
                    identifier_queried=identifier,
                    uberon_id_queried=cleaned_uberon,
                    expressed=False,
                    matches=[],
                )

            raw_expressions = target.get('expressions') or []
            matches = []
            for e in raw_expressions:
                uberon = e.get('uberon') or {}
                if (uberon.get('uid') or '').upper() == cleaned_uberon:
                    matches.append(_parse_expression_record(e))

            expressed = False
            if matches:
                for m in matches:
                    has_numeric = m.value is not None and m.value > 0
                    has_qual = (
                        m.qual
                        and m.qual.strip().lower() not in ('not detected', 'none', '')
                    )
                    if has_numeric or has_qual:
                        expressed = True
                        break

            return TissueExpressionCheck(
                success=True,
                message=f"Found {len(matches)} matching record(s) for {cleaned_uberon}",
                identifier_queried=identifier,
                uberon_id_queried=cleaned_uberon,
                uniprot=target.get('uniprot'),
                sym=target.get('sym'),
                name=target.get('name'),
                tdl=target.get('tdl'),
                expressed=expressed,
                matches=matches,
            )

        except ValueError as e:
            logger.error(f"Invalid input ({identifier}, {uberon_id}): {e}")
            return TissueExpressionCheck(
                success=False,
                message=f"Invalid input: {e}",
                identifier_queried=identifier,
                uberon_id_queried=uberon_id,
                expressed=False,
                matches=[],
            )
        except Exception as e:
            logger.error(f"Unexpected error for ({identifier}, {uberon_id}): {e}")
            return TissueExpressionCheck(
                success=False,
                message="An unexpected error occurred while fetching expression data",
                identifier_queried=identifier,
                uberon_id_queried=uberon_id,
                expressed=False,
                matches=[],
            )


# Health check
async def check_expression_service_health() -> Dict[str, Any]:
    """Health check for the expression service"""
    try:
        test_result = await ExpressionService.get_expressions("HMGCR")
        if test_result.success and test_result.expression_count > 0:
            return {
                "status": "healthy",
                "service": "expression_service",
                "test_target": "HMGCR",
                "expression_records": test_result.expression_count,
            }
        return {
            "status": "degraded",
            "service": "expression_service",
            "test_target": "HMGCR",
            "message": test_result.message,
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "service": "expression_service",
            "error": str(e),
        }
