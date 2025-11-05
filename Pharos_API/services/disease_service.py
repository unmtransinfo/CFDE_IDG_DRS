"""
Disease service layer - Business logic for disease-related operations
Connects GraphQL queries, response models, and error handling
"""

import logging
import sys
import os
from typing import Optional, List, Dict, Any

# Add parent directory to Python path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.graphql_client import query_pharos, PharosGraphQLError
from queries.disease_queries import (
    get_disease_query, 
    validate_disease_name, 
    validate_mondo_id,
    validate_disease_search_term
)

from schemas.responses import (
    DiseaseResponse, 
    DiseaseSearchResponse,
    DiseaseWithTargetsResponse,
    create_disease_response, 
    create_disease_search_response,
    create_disease_with_targets_response
)

# Set up logging
logger = logging.getLogger(__name__)

class DiseaseService:
    """
    Service class for disease-related business logic
    Handles all disease operations and data transformation
    """

    @staticmethod
    async def get_disease_basic(disease_name: str) -> DiseaseResponse:
        """
        Get basic disease information by disease name
        
        Args:
            disease_name: Disease name or identifier
            
        Returns:
            DiseaseResponse with disease data or error information
        """
        try:
            # Validate and clean input
            cleaned_name = validate_disease_name(disease_name)
            
            # Get the GraphQL query
            query = get_disease_query('basic')
            variables = {"disease_name": cleaned_name}
            
            logger.info(f"Querying basic disease info for: {cleaned_name}")
            
            # Execute GraphQL query
            result = await query_pharos(query, variables)
            
            # Extract disease data
            disease_data = None
            if result.get('data') and result['data'].get('disease'):
                disease_data = result['data']['disease']
                logger.info(f"Found disease: {disease_data.get('name', 'Unknown')}")
            else:
                logger.warning(f"No disease found for name: {cleaned_name}")
            
            # Create standardized response
            return create_disease_response(
                disease_data=disease_data,
                disease_name=cleaned_name,
                success=disease_data is not None
            )
            
        except ValueError as e:
            # Input validation error
            logger.error(f"Input validation error for disease '{disease_name}': {str(e)}")
            return create_disease_response(
                disease_data=None,
                disease_name=disease_name,
                success=False,
                message=f"Invalid disease name: {str(e)}"
            )
            
        except PharosGraphQLError as e:
            # Pharos API specific error
            logger.error(f"Pharos API error for disease '{disease_name}': {str(e)}")
            return create_disease_response(
                disease_data=None,
                disease_name=disease_name,
                success=False,
                message=f"Pharos API error: {str(e)}"
            )
            
        except Exception as e:
            # Unexpected error
            logger.error(f"Unexpected error for disease '{disease_name}': {str(e)}")
            return create_disease_response(
                disease_data=None,
                disease_name=disease_name,
                success=False,
                message="An unexpected error occurred while fetching disease data"
            )

    @staticmethod
    async def get_disease_with_targets(disease_name: str) -> DiseaseWithTargetsResponse:
        """
        Get disease information with associated targets
        
        Args:
            disease_name: Disease name or identifier
            
        Returns:
            DiseaseWithTargetsResponse with disease and target data
        """
        try:
            # Validate and clean input
            cleaned_name = validate_disease_name(disease_name)
            
            # Get the GraphQL query with targets
            query = get_disease_query('with_targets')
            variables = {"disease_name": cleaned_name}
            
            logger.info(f"Querying disease with targets for: {cleaned_name}")
            
            # Execute GraphQL query
            result = await query_pharos(query, variables)
            
            # Extract disease data
            disease_data = None
            if result.get('data') and result['data'].get('disease'):
                disease_data = result['data']['disease']
                target_count = len(disease_data.get('targets', []))
                logger.info(f"Found disease: {disease_data.get('name')} with {target_count} targets")
            else:
                logger.warning(f"No disease found for name: {cleaned_name}")
            
            # Create standardized response
            return create_disease_with_targets_response(
                disease_data=disease_data,
                disease_name=cleaned_name,
                success=disease_data is not None
            )
            
        except ValueError as e:
            logger.error(f"Input validation error: {str(e)}")
            return create_disease_with_targets_response(
                disease_data=None,
                disease_name=disease_name,
                success=False,
                message=f"Invalid disease name: {str(e)}"
            )
            
        except PharosGraphQLError as e:
            logger.error(f"Pharos API error: {str(e)}")
            return create_disease_with_targets_response(
                disease_data=None,
                disease_name=disease_name,
                success=False,
                message=f"Pharos API error: {str(e)}"
            )
            
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            return create_disease_with_targets_response(
                disease_data=None,
                disease_name=disease_name,
                success=False,
                message="An unexpected error occurred"
            )

    @staticmethod
    async def get_disease_by_mondo_id(mondo_id: str) -> DiseaseResponse:
        """
        Get disease information by MONDO ID
        
        Args:
            mondo_id: MONDO identifier (e.g., MONDO:0004979)
            
        Returns:
            DiseaseResponse with disease data
        """
        try:
            # Validate and clean MONDO ID
            cleaned_mondo = validate_mondo_id(mondo_id)
            
            # Get the GraphQL query
            query = get_disease_query('search_by_mondo')
            variables = {"mondo_id": cleaned_mondo}
            
            logger.info(f"Querying disease by MONDO ID: {cleaned_mondo}")
            
            # Execute GraphQL query
            result = await query_pharos(query, variables)
            
            # Extract disease data
            disease_data = None
            if result.get('data') and result['data'].get('disease'):
                disease_data = result['data']['disease']
                logger.info(f"Found disease: {disease_data.get('name', 'Unknown')}")
            else:
                logger.warning(f"No disease found for MONDO ID: {cleaned_mondo}")
            
            # Create standardized response
            return create_disease_response(
                disease_data=disease_data,
                disease_name=cleaned_mondo,
                success=disease_data is not None
            )
            
        except ValueError as e:
            logger.error(f"MONDO ID validation error: {str(e)}")
            return create_disease_response(
                disease_data=None,
                disease_name=mondo_id,
                success=False,
                message=f"Invalid MONDO ID: {str(e)}"
            )
            
        except Exception as e:
            logger.error(f"Error fetching disease by MONDO ID: {str(e)}")
            return create_disease_response(
                disease_data=None,
                disease_name=mondo_id,
                success=False,
                message="An unexpected error occurred"
            )

    @staticmethod
    async def search_diseases(search_term: str, skip: int = 0, limit: int = 10) -> DiseaseSearchResponse:
        """
        Search for diseases by name or keyword
        
        Args:
            search_term: Search query (disease name, keyword)
            skip: Number of results to skip (for pagination)
            limit: Maximum number of results to return
            
        Returns:
            DiseaseSearchResponse with search results and pagination
        """
        try:
            # Validate and clean input
            cleaned_term = validate_disease_search_term(search_term)
            
            # Validate pagination parameters
            if skip < 0:
                raise ValueError("Skip parameter must be non-negative")
            if limit < 1 or limit > 100:
                raise ValueError("Limit must be between 1 and 100")
            
            # Get the GraphQL query
            query = get_disease_query('search')
            variables = {
                "search_term": cleaned_term,
                "limit": limit + skip  # Get extra results to handle skip
            }
            
            logger.info(f"Searching diseases for: '{cleaned_term}' (skip={skip}, limit={limit})")
            
            # Execute GraphQL query
            result = await query_pharos(query, variables)
            
            # Extract search results
            diseases_data = []
            total_count = 0
            
            if result.get('data') and result['data'].get('diseases'):
                pharos_result = result['data']['diseases']
                total_count = pharos_result.get('count', 0)
                
                if pharos_result.get('diseases'):
                    all_diseases = pharos_result['diseases']
                    # Apply skip manually if needed
                    diseases_data = all_diseases[skip:skip + limit]
            
            # Handle case where single disease is returned
            elif result.get('data') and result['data'].get('disease'):
                single_disease = result['data']['disease']
                if single_disease:
                    diseases_data = [single_disease]
                    total_count = 1
                    
            logger.info(f"Found {total_count} diseases, returning {len(diseases_data)} results")
            
            # Create standardized response
            return create_disease_search_response(
                diseases_data=diseases_data,
                search_term=cleaned_term,
                total_count=total_count,
                skip=skip,
                limit=limit,
                success=True
            )
            
        except ValueError as e:
            # Input validation error
            logger.error(f"Input validation error for search '{search_term}': {str(e)}")
            return create_disease_search_response(
                diseases_data=[],
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
            return create_disease_search_response(
                diseases_data=[],
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
            return create_disease_search_response(
                diseases_data=[],
                search_term=search_term,
                total_count=0,
                skip=skip,
                limit=limit,
                success=False,
                message="An unexpected error occurred during search"
            )

# Convenience functions for direct use
async def get_disease(disease_name: str) -> DiseaseResponse:
    """Convenience function to get basic disease info"""
    return await DiseaseService.get_disease_basic(disease_name)

async def get_disease_targets(disease_name: str) -> DiseaseWithTargetsResponse:
    """Convenience function to get disease with targets"""
    return await DiseaseService.get_disease_with_targets(disease_name)

async def search_diseases_by_term(search_term: str, skip: int = 0, limit: int = 10) -> DiseaseSearchResponse:
    """Convenience function to search diseases"""
    return await DiseaseService.search_diseases(search_term, skip, limit)

# Health check for disease service
async def check_disease_service_health() -> Dict[str, Any]:
    """
    Health check for the disease service
    Tests basic functionality with a known disease
    """
    try:
        # Test with a well-known disease
        test_result = await DiseaseService.get_disease_basic("asthma")
        
        if test_result.success and test_result.data:
            return {
                "status": "healthy",
                "service": "disease_service",
                "test_disease": "asthma",
                "test_result": "success"
            }
        else:
            return {
                "status": "degraded",
                "service": "disease_service",
                "test_disease": "asthma",
                "test_result": "no_data",
                "message": test_result.message
            }
            
    except Exception as e:
        return {
            "status": "unhealthy",
            "service": "disease_service",
            "error": str(e)
        }

# Data processing helpers
def extract_disease_properties(disease_data: dict) -> Dict[str, Any]:
    """
    Extract key properties from disease data
    """
    properties = {
        "is_rare": disease_data.get('gard_rare', False),
        "has_mondo_id": bool(disease_data.get('mondoID')),
        "association_count": disease_data.get('associationCount', 0),
        "direct_association_count": disease_data.get('directAssociationCount', 0),
        "has_description": any([
            disease_data.get('uniprotDescription'),
            disease_data.get('doDescription'),
            disease_data.get('mondoDescription')
        ]),
        "datasource_count": disease_data.get('datasource_count', 0)
    }
    
    return properties

def categorize_disease(disease_data: dict) -> str:
    """
    Categorize disease based on its properties
    Returns: 'rare', 'common', 'well_studied', 'emerging', 'unknown'
    """
    is_rare = disease_data.get('gard_rare')
    assoc_count = disease_data.get('associationCount', 0)
    datasource_count = disease_data.get('datasource_count', 0)
    
    if is_rare:
        return 'rare'
    elif assoc_count > 100 and datasource_count > 5:
        return 'well_studied'
    elif assoc_count > 20:
        return 'common'
    elif assoc_count > 0:
        return 'emerging'
    else:
        return 'unknown'

def get_best_description(disease_data: dict) -> Optional[str]:
    """
    Get the best available description for a disease
    Prioritizes: MONDO > DO > UniProt
    """
    descriptions = [
        disease_data.get('mondoDescription'),
        disease_data.get('doDescription'),
        disease_data.get('uniprotDescription')
    ]
    
    # Return first non-empty description
    for desc in descriptions:
        if desc and desc.strip():
            return desc.strip()
    
    return None

if __name__ == "__main__":
    # Test the service when run directly
    import asyncio
    
    async def test_service():
        print("Testing Disease Service...")
        
        # Test 1: Get basic disease info
        print("\n1. Testing basic disease retrieval...")
        result1 = await DiseaseService.get_disease_basic("asthma")
        print(f"Result: {result1.success}, Disease: {result1.data.disease_name if result1.data else 'None'}")
        
        # Test 2: Search diseases
        print("\n2. Testing disease search...")
        result2 = await DiseaseService.search_diseases("cancer", limit=5)
        print(f"Result: {result2.success}, Found: {len(result2.data)} diseases")
        
        # Test 3: Get disease with targets
        print("\n3. Testing disease with targets...")
        result3 = await DiseaseService.get_disease_with_targets("asthma")
        print(f"Result: {result3.success}, Disease: {result3.data.disease_name if result3.data else 'None'}")
        if result3.data:
            print(f"Associated targets: {result3.data.target_count}")
        
        # Test 4: Get disease by MONDO ID
        print("\n4. Testing disease by MONDO ID...")
        result4 = await DiseaseService.get_disease_by_mondo_id("MONDO:0004979")
        print(f"Result: {result4.success}, Disease: {result4.data.disease_name if result4.data else 'None'}")
        
        # Test 5: Health check
        print("\n5. Testing service health...")
        health = await check_disease_service_health()
        print(f"Health: {health['status']}")
        
        # Test 6: Data processing helpers
        if result1.success and result1.data:
            print("\n6. Testing data processing helpers...")
            # Create sample data dict
            sample_data = {
                'name': result1.data.disease_name,
                'gard_rare': result1.data.is_rare,
                'associationCount': result1.data.association_count,
                'mondoDescription': result1.data.description
            }
            
            properties = extract_disease_properties(sample_data)
            category = categorize_disease(sample_data)
            best_desc = get_best_description(sample_data)
            print(f"Properties: {properties}")
            print(f"Category: {category}")
            print(f"Best description: {best_desc[:100] if best_desc else 'None'}...")
    
    # Run tests
    asyncio.run(test_service())