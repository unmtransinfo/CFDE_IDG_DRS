"""
Target service layer - Business logic for target-related operations
Connects GraphQL queries, response models, and error handling
"""

import logging
import sys
import os
from typing import Optional, List, Dict, Any

# Add parent directory to Python path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.graphql_client import query_pharos, PharosGraphQLError
from queries.target_queries import get_target_query, validate_gene_symbol, validate_search_term
from schemas.responses import (
    TargetResponse, TargetSearchResponse, TargetWithDiseasesResponse,
    create_target_response, create_search_response, create_error_response,
    TargetWithDiseases, DiseaseBasic, TargetWithLigands, LigandBasic, TargetWithLigandsResponse
)

# Set up logging
logger = logging.getLogger(__name__)

class TargetService:
    """
    Service class for target-related business logic
    Handles all target operations and data transformation
    """

    @staticmethod
    async def get_target_basic(gene_symbol: str) -> TargetResponse:
        """
        Get basic target information by gene symbol
        
        Args:
            gene_symbol: Gene symbol (e.g., EGFR, TP53)
            
        Returns:
            TargetResponse with target data or error information
        """
        try:
            # Validate and clean input
            cleaned_symbol = validate_gene_symbol(gene_symbol)
            
            # Get the GraphQL query
            query = get_target_query('basic')
            variables = {"gene_symbol": cleaned_symbol}
            
            logger.info(f"Querying basic target info for: {cleaned_symbol}")
            
            # Execute GraphQL query
            result = await query_pharos(query, variables)
            
            # Extract target data
            target_data = None
            if result.get('data') and result['data'].get('target'):
                target_data = result['data']['target']
                logger.info(f"Found target: {target_data.get('name', 'Unknown')}")
            else:
                logger.warning(f"No target found for gene symbol: {cleaned_symbol}")
            
            # Create standardized response
            return create_target_response(
                target_data=target_data,
                gene_symbol=cleaned_symbol,
                success=target_data is not None
            )
            
        except ValueError as e:
            # Input validation error
            logger.error(f"Input validation error for gene symbol '{gene_symbol}': {str(e)}")
            return create_target_response(
                target_data=None,
                gene_symbol=gene_symbol,
                success=False,
                message=f"Invalid gene symbol: {str(e)}"
            )
            
        except PharosGraphQLError as e:
            # Pharos API specific error
            logger.error(f"Pharos API error for gene symbol '{gene_symbol}': {str(e)}")
            return create_target_response(
                target_data=None,
                gene_symbol=gene_symbol,
                success=False,
                message=f"Pharos API error: {str(e)}"
            )
            
        except Exception as e:
            # Unexpected error
            logger.error(f"Unexpected error for gene symbol '{gene_symbol}': {str(e)}")
            return create_target_response(
                target_data=None,
                gene_symbol=gene_symbol,
                success=False,
                message="An unexpected error occurred while fetching target data"
            )

    @staticmethod
    async def search_targets(search_term: str, skip: int = 0, limit: int = 10) -> TargetSearchResponse:
        """
        Search for targets by name or gene symbol
        
        Args:
            search_term: Search query (e.g., "kinase", "EGFR", "growth factor")
            skip: Number of results to skip (for pagination)
            limit: Maximum number of results to return
            
        Returns:
            TargetSearchResponse with search results and pagination
        """
        try:
            # Validate and clean input
            cleaned_term = validate_search_term(search_term)
            
            # Validate pagination parameters
            if skip < 0:
                raise ValueError("Skip parameter must be non-negative")
            if limit < 1 or limit > 100:
                raise ValueError("Limit must be between 1 and 100")
            
            # Get the GraphQL query
            query = get_target_query('search')
            # Note: GraphQL might not support skip directly, so we'll get more results and slice
            variables = {
                "search_term": cleaned_term,
                "limit": limit + skip  # Get extra results to handle skip
            }
            
            logger.info(f"Searching targets for: '{cleaned_term}' (skip={skip}, limit={limit})")
            
            # Execute GraphQL query
            result = await query_pharos(query, variables)
            
            # Extract search results
            targets_data = []
            total_count = 0
            
            if result.get('data') and result['data'].get('targets'):
                pharos_result = result['data']['targets']
                total_count = pharos_result.get('count', 0)
                
                if pharos_result.get('targets'):
                    all_targets = pharos_result['targets']
                    # Apply skip manually if needed
                    targets_data = all_targets[skip:skip + limit]
                    
            logger.info(f"Found {total_count} targets, returning {len(targets_data)} results")
            
            # Create standardized response
            return create_search_response(
                targets_data=targets_data,
                search_term=cleaned_term,
                total_count=total_count,
                skip=skip,
                limit=limit,
                success=True
            )
            
        except ValueError as e:
            # Input validation error
            logger.error(f"Input validation error for search '{search_term}': {str(e)}")
            return create_search_response(
                targets_data=[],
                search_term=search_term,
                total_count=0,
                skip=skip,
                limit=limit,
                success=False,
                message=f"Invalid search parameters: {str(e)}"
            )
            
        except PharosGraphQLError as e:
            # Pharos API specific error
            logger.error(f"Pharos API error for search '{search_term}': {str(e)}")
            return create_search_response(
                targets_data=[],
                search_term=search_term,
                total_count=0,
                skip=skip,
                limit=limit,
                success=False,
                message=f"Search failed: {str(e)}"
            )
            
        except Exception as e:
            # Unexpected error
            logger.error(f"Unexpected error for search '{search_term}': {str(e)}")
            return create_search_response(
                targets_data=[],
                search_term=search_term,
                total_count=0,
                skip=skip,
                limit=limit,
                success=False,
                message="An unexpected error occurred during search"
            )

    @staticmethod
    async def get_target_with_diseases(gene_symbol: str, max_diseases: int = 3) -> TargetWithDiseasesResponse:
        """
        Get target information with associated diseases (cross-relationship demo)
        
        Args:
            gene_symbol: Gene symbol (e.g., EGFR, TP53)
            max_diseases: Maximum number of diseases to return (default 3 for demo)
            
        Returns:
            TargetWithDiseasesResponse with target and disease data
        """
        try:
            # Validate and clean input
            cleaned_symbol = validate_gene_symbol(gene_symbol)
            
            # Use a query with top parameter to limit disease results
            query = """
            query GetTargetWithDiseases($gene_symbol: String!, $top: Int!) {
                target(q: {sym: $gene_symbol}) {
                    name
                    sym
                    uniprot
                    description
                    tdl
                    fam
                    novelty
                    diseases(top: $top) {
                        name
                        mondoID
                        doDescription
                        uniprotDescription
                    }
                }
            }
            """
            variables = {"gene_symbol": cleaned_symbol, "top": max_diseases}
            
            logger.info(f"Querying target with diseases for: {cleaned_symbol}")
            
            # Execute GraphQL query
            result = await query_pharos(query, variables)
            
            # Extract target and disease data
            target_data = None
            diseases_data = []
            
            if result.get('data') and result['data'].get('target'):
                target_raw = result['data']['target']
                
                # Extract basic target info
                target_data = {
                    'name': target_raw.get('name'),
                    'sym': target_raw.get('sym'),
                    'uniprot': target_raw.get('uniprot'),
                    'description': target_raw.get('description'),
                    'tdl': target_raw.get('tdl'),
                    'fam': target_raw.get('fam'),
                    'novelty': target_raw.get('novelty')
                }
                
                # Extract disease associations
                if target_raw.get('diseases'):
                    diseases_raw = target_raw['diseases']  # Already limited by top parameter
                    for disease in diseases_raw:
                        # Get best available description
                        description = disease.get('doDescription') or disease.get('uniprotDescription') or ""

                        disease_info = DiseaseBasic(
                            disease_name=disease.get('name'),
                            mondo_id=disease.get('mondoID'),
                            description=description
                        )
                        diseases_data.append(disease_info)
                
                logger.info(f"Found target with {len(diseases_data)} disease associations")
            else:
                logger.warning(f"No target found for gene symbol: {cleaned_symbol}")
            
            # Create response with target and disease data
            if target_data:
                target_with_diseases = TargetWithDiseases(
                    target_name=target_data.get('name'),
                    gene_symbol=target_data.get('sym'),
                    uniprot_id=target_data.get('uniprot'),
                    description=target_data.get('description'),
                    development_level=target_data.get('tdl'),
                    protein_family=target_data.get('fam'),
                    novelty_score=target_data.get('novelty'),
                    associated_diseases=diseases_data,
                    disease_count=len(diseases_data)
                )
                
                return TargetWithDiseasesResponse(
                    success=True,
                    message=f"Target found with {len(diseases_data)} disease associations",
                    gene_symbol_queried=cleaned_symbol,
                    data=target_with_diseases
                )
            else:
                return TargetWithDiseasesResponse(
                    success=False,
                    message="Target not found",
                    gene_symbol_queried=cleaned_symbol,
                    data=None
                )
                
        except ValueError as e:
            # Input validation error
            logger.error(f"Input validation error for gene symbol '{gene_symbol}': {str(e)}")
            return TargetWithDiseasesResponse(
                success=False,
                message=f"Invalid gene symbol: {str(e)}",
                gene_symbol_queried=gene_symbol,
                data=None
            )
            
        except PharosGraphQLError as e:
            # Pharos API specific error
            logger.error(f"Pharos API error for gene symbol '{gene_symbol}': {str(e)}")
            return TargetWithDiseasesResponse(
                success=False,
                message=f"Pharos API error: {str(e)}",
                gene_symbol_queried=gene_symbol,
                data=None
            )
            
        except Exception as e:
            # Unexpected error
            logger.error(f"Unexpected error for gene symbol '{gene_symbol}': {str(e)}")
            return TargetWithDiseasesResponse(
                success=False,
                message="An unexpected error occurred while fetching target data",
                gene_symbol_queried=gene_symbol,
                data=None
            )
    
    @staticmethod
    async def get_target_with_ligands(gene_symbol: str, max_ligands: int = 10) -> 'TargetWithLigandsResponse':
        """
        Get target information with associated ligands (drugs/compounds)
        
        Args:
            gene_symbol: Gene symbol (e.g., EGFR, TP53)
            max_ligands: Maximum number of ligands to return (default 10)
            
        Returns:
            TargetWithLigandsResponse with target and ligand data
        """
        try:
            # Validate and clean input
            cleaned_symbol = validate_gene_symbol(gene_symbol)
            
            # Use the query from target_queries
            from queries.target_queries import get_target_query
            query = get_target_query('with_ligands')
            variables = {"gene_symbol": cleaned_symbol, "top": max_ligands}
            
            logger.info(f"Querying target with ligands for: {cleaned_symbol}")
            
            # Execute GraphQL query
            result = await query_pharos(query, variables)
            
            # Extract target and ligand data
            target_data = None
            ligands_data = []
            
            if result.get('data') and result['data'].get('target'):
                target_raw = result['data']['target']
                
                # Extract basic target info
                target_data = {
                    'name': target_raw.get('name'),
                    'sym': target_raw.get('sym'),
                    'uniprot': target_raw.get('uniprot'),
                    'description': target_raw.get('description'),
                    'tdl': target_raw.get('tdl'),
                    'fam': target_raw.get('fam'),
                    'novelty': target_raw.get('novelty')
                }
                
                # Extract ligand associations
                if target_raw.get('ligands'):
                    ligands_raw = target_raw['ligands']  # Already limited by top parameter
                    for ligand in ligands_raw:
                        # Extract ChEMBL ID from synonyms if available
                        chembl_id = None
                        if ligand.get('synonyms'):
                            for syn in ligand['synonyms']:
                                value = syn.get('value', '')
                                if value.startswith('CHEMBL'):
                                    chembl_id = value
                                    break
                        
                        ligand_info = LigandBasic(
                            ligand_name=ligand.get('name'),
                            description=ligand.get('description'),
                            is_drug=ligand.get('isdrug'),
                            smiles=ligand.get('smiles'),
                            chembl_id=chembl_id,
                            activity_count=ligand.get('actcnt'),
                            target_count=ligand.get('targetCount')
                        )
                        ligands_data.append(ligand_info)
                
                logger.info(f"Found target with {len(ligands_data)} ligand associations")
            else:
                logger.warning(f"No target found for gene symbol: {cleaned_symbol}")
            
            # Create response with target and ligand data
            if target_data:
                target_with_ligands = TargetWithLigands(
                    target_name=target_data.get('name'),
                    gene_symbol=target_data.get('sym'),
                    uniprot_id=target_data.get('uniprot'),
                    description=target_data.get('description'),
                    development_level=target_data.get('tdl'),
                    protein_family=target_data.get('fam'),
                    novelty_score=target_data.get('novelty'),
                    associated_ligands=ligands_data,
                    ligand_count=len(ligands_data)
                )
                
                return TargetWithLigandsResponse(
                    success=True,
                    message=f"Target found with {len(ligands_data)} ligand associations",
                    gene_symbol_queried=cleaned_symbol,
                    data=target_with_ligands
                )
            else:
                return TargetWithLigandsResponse(
                    success=False,
                    message="Target not found",
                    gene_symbol_queried=cleaned_symbol,
                    data=None
                )
                
        except ValueError as e:
            # Input validation error
            logger.error(f"Input validation error for gene symbol '{gene_symbol}': {str(e)}")
            return TargetWithLigandsResponse(
                success=False,
                message=f"Invalid gene symbol: {str(e)}",
                gene_symbol_queried=gene_symbol,
                data=None
            )
            
        except PharosGraphQLError as e:
            # Pharos API specific error
            logger.error(f"Pharos API error for gene symbol '{gene_symbol}': {str(e)}")
            return TargetWithLigandsResponse(
                success=False,
                message=f"Pharos API error: {str(e)}",
                gene_symbol_queried=gene_symbol,
                data=None
            )
            
        except Exception as e:
            # Unexpected error
            logger.error(f"Unexpected error for gene symbol '{gene_symbol}': {str(e)}")
            return TargetWithLigandsResponse(
                success=False,
                message="An unexpected error occurred while fetching target data",
                gene_symbol_queried=gene_symbol,
                data=None
            )

# Convenience functions for direct use
async def get_target(gene_symbol: str) -> TargetResponse:
    """Convenience function to get basic target info"""
    return await TargetService.get_target_basic(gene_symbol)

async def search_targets_by_term(search_term: str, skip: int = 0, limit: int = 10) -> TargetSearchResponse:
    """Convenience function to search targets"""
    return await TargetService.search_targets(search_term, skip, limit)

async def get_target_diseases(gene_symbol: str) -> TargetWithDiseasesResponse:
    """Convenience function to get target with diseases"""
    return await TargetService.get_target_with_diseases(gene_symbol)

# Health check for target service
async def check_target_service_health() -> Dict[str, Any]:
    """
    Health check for the target service
    Tests basic functionality with a known target
    """
    try:
        # Test with a well-known target
        test_result = await TargetService.get_target_basic("ACE2")
        
        if test_result.success and test_result.data:
            return {
                "status": "healthy",
                "service": "target_service",
                "test_target": "ACE2",
                "test_result": "success"
            }
        else:
            return {
                "status": "degraded",
                "service": "target_service",
                "test_target": "ACE2",
                "test_result": "no_data",
                "message": test_result.message
            }
            
    except Exception as e:
        return {
            "status": "unhealthy",
            "service": "target_service",
            "error": str(e)
        }

if __name__ == "__main__":
    # Test the service when run directly
    import asyncio
    
    async def test_service():
        print("Testing Target Service...")
        
        # Test 1: Get basic target info
        print("\n1. Testing basic target retrieval...")
        result1 = await TargetService.get_target_basic("EGFR")
        print(f"Result: {result1.success}, Target: {result1.data.gene_symbol if result1.data else 'None'}")
        
        # Test 2: Search targets
        print("\n2. Testing target search...")
        result2 = await TargetService.search_targets("kinase", limit=5)
        print(f"Result: {result2.success}, Found: {len(result2.data)} targets")
        
        # Test 3: Target with diseases (skip for now - has query issues)
        print("\n3. Testing target with diseases... (SKIPPED - fixing query)")
        print("Result: Skipped, will fix disease query syntax later")
        
        # Test 4: Health check
        print("\n4. Testing service health...")
        health = await check_target_service_health()
        print(f"Health: {health['status']}")
    
    # Run tests
    asyncio.run(test_service())