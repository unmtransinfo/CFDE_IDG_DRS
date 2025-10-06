"""
Ligand service layer - Business logic for ligand-related operations
Connects GraphQL queries, response models, and error handling
"""

import logging
import sys
import os
from typing import Optional, List, Dict, Any

# Add parent directory to Python path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.graphql_client import query_pharos, PharosGraphQLError
from queries.ligand_queries import get_ligand_query, validate_ligand_id, validate_ligand_search_term
from schemas.responses import (
    LigandResponse, LigandSearchResponse,
    create_ligand_response, create_ligand_search_response
)

# Set up logging
logger = logging.getLogger(__name__)

class LigandService:
    """
    Service class for ligand-related business logic
    Handles all ligand operations and data transformation
    """

    @staticmethod
    async def get_ligand_basic(ligand_id: str) -> LigandResponse:
        """
        Get basic ligand information by ligand ID or name
        
        Args:
            ligand_id: Ligand identifier (name, ChEMBL ID, etc.)
            
        Returns:
            LigandResponse with ligand data or error information
        """
        try:
            # Validate and clean input
            cleaned_id = validate_ligand_id(ligand_id)
            
            # Get the GraphQL query
            query = get_ligand_query('basic')
            variables = {"ligand_id": cleaned_id}
            
            logger.info(f"Querying basic ligand info for: {cleaned_id}")
            
            # Execute GraphQL query
            result = await query_pharos(query, variables)
            
            # Extract ligand data
            ligand_data = None
            if result.get('data') and result['data'].get('ligand'):
                ligand_data = result['data']['ligand']
                logger.info(f"Found ligand: {ligand_data.get('name', 'Unknown')}")
            else:
                logger.warning(f"No ligand found for ID: {cleaned_id}")
            
            # Create standardized response
            return create_ligand_response(
                ligand_data=ligand_data,
                ligand_id=cleaned_id,
                success=ligand_data is not None
            )
            
        except ValueError as e:
            # Input validation error
            logger.error(f"Input validation error for ligand ID '{ligand_id}': {str(e)}")
            return create_ligand_response(
                ligand_data=None,
                ligand_id=ligand_id,
                success=False,
                message=f"Invalid ligand ID: {str(e)}"
            )
            
        except PharosGraphQLError as e:
            # Pharos API specific error
            logger.error(f"Pharos API error for ligand ID '{ligand_id}': {str(e)}")
            return create_ligand_response(
                ligand_data=None,
                ligand_id=ligand_id,
                success=False,
                message=f"Pharos API error: {str(e)}"
            )
            
        except Exception as e:
            # Unexpected error
            logger.error(f"Unexpected error for ligand ID '{ligand_id}': {str(e)}")
            return create_ligand_response(
                ligand_data=None,
                ligand_id=ligand_id,
                success=False,
                message="An unexpected error occurred while fetching ligand data"
            )

    @staticmethod
    async def search_ligands(search_term: str, skip: int = 0, limit: int = 10) -> LigandSearchResponse:
        """
        Search for ligands by name, indication, or keyword
        
        Args:
            search_term: Search query (ligand name, indication, keyword)
            skip: Number of results to skip (for pagination)
            limit: Maximum number of results to return
            
        Returns:
            LigandSearchResponse with search results and pagination
        """
        try:
            # Validate and clean input
            cleaned_term = validate_ligand_search_term(search_term)
            
            # Validate pagination parameters
            if skip < 0:
                raise ValueError("Skip parameter must be non-negative")
            if limit < 1 or limit > 100:
                raise ValueError("Limit must be between 1 and 100")
            
            # Get the GraphQL query
            query = get_ligand_query('search')
            # Note: GraphQL might not support skip directly, so we'll get more results and slice
            variables = {
                "search_term": cleaned_term,
                "limit": limit + skip  # Get extra results to handle skip
            }
            
            logger.info(f"Searching ligands for: '{cleaned_term}' (skip={skip}, limit={limit})")
            
            # Execute GraphQL query
            result = await query_pharos(query, variables)
            
            # Extract search results
            ligands_data = []
            total_count = 0
            
            if result.get('data') and result['data'].get('ligands'):
                pharos_result = result['data']['ligands']
                total_count = pharos_result.get('count', 0)
                
                if pharos_result.get('ligands'):
                    all_ligands = pharos_result['ligands']
                    # Apply skip manually if needed
                    ligands_data = all_ligands[skip:skip + limit]
            
            # Handle case where search structure might be different
            elif result.get('data') and result['data'].get('ligand'):
                # Single ligand returned instead of list
                single_ligand = result['data']['ligand']
                if single_ligand:
                    ligands_data = [single_ligand]
                    total_count = 1
                    
            logger.info(f"Found {total_count} ligands, returning {len(ligands_data)} results")
            
            # Create standardized response
            return create_ligand_search_response(
                ligands_data=ligands_data,
                search_term=cleaned_term,
                total_count=total_count,
                skip=skip,
                limit=limit,
                success=True
            )
            
        except ValueError as e:
            # Input validation error
            logger.error(f"Input validation error for search '{search_term}': {str(e)}")
            return create_ligand_search_response(
                ligands_data=[],
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
            
            # Try alternative search query if main one fails
            try:
                logger.info("Attempting alternative search query...")
                alt_query = get_ligand_query('search_alternative')
                alt_variables = {"search_term": cleaned_term}
                
                alt_result = await query_pharos(alt_query, alt_variables)
                
                # Process alternative result
                ligands_data = []
                total_count = 0
                
                if alt_result.get('data') and alt_result['data'].get('ligands'):
                    pharos_result = alt_result['data']['ligands']
                    total_count = pharos_result.get('count', 0)
                    
                    if pharos_result.get('ligands'):
                        all_ligands = pharos_result['ligands']
                        ligands_data = all_ligands[skip:skip + limit]
                
                return create_ligand_search_response(
                    ligands_data=ligands_data,
                    search_term=cleaned_term,
                    total_count=total_count,
                    skip=skip,
                    limit=limit,
                    success=True,
                    message="Search completed using alternative query"
                )
                
            except Exception as alt_e:
                logger.error(f"Alternative search also failed: {str(alt_e)}")
                return create_ligand_search_response(
                    ligands_data=[],
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
            return create_ligand_search_response(
                ligands_data=[],
                search_term=search_term,
                total_count=0,
                skip=skip,
                limit=limit,
                success=False,
                message="An unexpected error occurred during search"
            )

# Convenience functions for direct use
async def get_ligand(ligand_id: str) -> LigandResponse:
    """Convenience function to get basic ligand info"""
    return await LigandService.get_ligand_basic(ligand_id)

async def search_ligands_by_term(search_term: str, skip: int = 0, limit: int = 10) -> LigandSearchResponse:
    """Convenience function to search ligands"""
    return await LigandService.search_ligands(search_term, skip, limit)

# Health check for ligand service
async def check_ligand_service_health() -> Dict[str, Any]:
    """
    Health check for the ligand service
    Tests basic functionality with a known ligand
    """
    try:
        # Test with a well-known ligand from Pharos documentation
        test_result = await LigandService.get_ligand_basic("haloperidol")
        
        if test_result.success and test_result.data:
            return {
                "status": "healthy",
                "service": "ligand_service",
                "test_ligand": "haloperidol",
                "test_result": "success"
            }
        else:
            return {
                "status": "degraded",
                "service": "ligand_service",
                "test_ligand": "haloperidol",
                "test_result": "no_data",
                "message": test_result.message
            }
            
    except Exception as e:
        return {
            "status": "unhealthy",
            "service": "ligand_service",
            "error": str(e)
        }

# Data processing helpers
def extract_drug_properties(ligand_data: dict) -> Dict[str, Any]:
    """
    Extract drug-specific properties from ligand data
    Useful for filtering approved drugs vs compounds
    """
    properties = {
        "is_approved_drug": ligand_data.get('isdrug', False),
        "has_smiles": bool(ligand_data.get('smiles')),
        "has_molecular_weight": ligand_data.get('molweight') is not None,
        "synonym_count": len(ligand_data.get('synonyms', [])),
        "chembl_id": None
    }
    
    # Extract ChEMBL ID
    for synonym in ligand_data.get('synonyms', []):
        value = synonym.get('value', '')
        if value.startswith('CHEMBL'):
            properties['chembl_id'] = value
            break
    
    return properties

def categorize_ligand(ligand_data: dict) -> str:
    """
    Categorize ligand based on its properties
    Returns: 'approved_drug', 'investigational', 'compound', 'unknown'
    """
    is_drug = ligand_data.get('isdrug')
    
    if is_drug is True:
        return 'approved_drug'
    elif is_drug is False:
        # Check if it has drug-like properties
        if ligand_data.get('molweight') and ligand_data.get('smiles'):
            return 'compound'
        else:
            return 'unknown'
    else:
        return 'unknown'

if __name__ == "__main__":
    # Test the service when run directly
    import asyncio
    
    async def test_service():
        print("Testing Ligand Service...")
        
        # Test 1: Get basic ligand info
        print("\n1. Testing basic ligand retrieval...")
        result1 = await LigandService.get_ligand_basic("haloperidol")
        print(f"Result: {result1.success}, Ligand: {result1.data.ligand_name if result1.data else 'None'}")
        
        # Test 2: Search ligands
        print("\n2. Testing ligand search...")
        result2 = await LigandService.search_ligands("aspirin", limit=5)
        print(f"Result: {result2.success}, Found: {len(result2.data)} ligands")
        
        # Test 3: Alternative ligand ID
        print("\n3. Testing with alternative ligand ID...")
        result3 = await LigandService.get_ligand_basic("aspirin")
        print(f"Result: {result3.success}, Ligand: {result3.data.ligand_name if result3.data else 'None'}")
        
        # Test 4: Health check
        print("\n4. Testing service health...")
        health = await check_ligand_service_health()
        print(f"Health: {health['status']}")
        
        # Test 5: Data processing helpers
        if result1.success and result1.data:
            print("\n5. Testing data processing helpers...")
            # Convert LigandBasic back to dict format for testing
            sample_data = {
                'name': result1.data.ligand_name,
                'isdrug': result1.data.is_drug,
                'molweight': result1.data.molecular_weight,
                'smiles': result1.data.smiles,
                'synonyms': [{'value': result1.data.chembl_id}] if result1.data.chembl_id else []
            }
            
            properties = extract_drug_properties(sample_data)
            category = categorize_ligand(sample_data)
            print(f"Properties: {properties}")
            print(f"Category: {category}")
    
    # Run tests
    asyncio.run(test_service())