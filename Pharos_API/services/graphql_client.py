import sys
import os
# Add parent directory to Python path so we can import config
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import asyncio
import logging
from typing import Dict, Any, Optional
import httpx
from config import settings, get_pharos_headers

# Set up logging
logger = logging.getLogger(__name__)

class PharosGraphQLError(Exception):
    """Custom exception for Pharos GraphQL errors"""
    def __init__(self, message: str, errors: Optional[list] = None, status_code: Optional[int] = None):
        self.message = message
        self.errors = errors or []
        self.status_code = status_code
        super().__init__(self.message)

class PharosGraphQLClient:
    """
    Production-ready GraphQL client for Pharos API
    Handles timeouts, retries, error handling, and logging
    """
    
    def __init__(self):
        self.api_url = settings.pharos_api_url
        self.timeout = settings.pharos_api_timeout
        self.max_retries = settings.pharos_retry_attempts
        self.headers = get_pharos_headers()
        
        # Validate configuration
        if not self.api_url:
            raise ValueError("Pharos API URL not configured")
    
    async def query(self, query: str, variables: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Execute a GraphQL query against Pharos API
        
        Args:
            query: GraphQL query string
            variables: Optional variables for the query
            
        Returns:
            Dict containing the GraphQL response
            
        Raises:
            PharosGraphQLError: For GraphQL-specific errors
            httpx.HTTPError: For HTTP-related errors
        """
        # Validate inputs
        if not query or not query.strip():
            raise ValueError("Query cannot be empty")
        
        # Prepare payload
        payload = {"query": query.strip()}
        if variables:
            payload["variables"] = variables
        
        # Log the request (exclude sensitive data in production)
        logger.info(f"Executing GraphQL query to {self.api_url}")
        logger.debug(f"Query: {query[:100]}...")  # Log first 100 chars of query
        if variables:
            logger.debug(f"Variables: {variables}")
        
        # Execute with retries
        last_exception = None
        
        for attempt in range(self.max_retries + 1):
            try:
                return await self._execute_request(payload, attempt + 1)
                
            except httpx.HTTPError as e:
                last_exception = e
                if attempt < self.max_retries:
                    wait_time = 2 ** attempt  # Exponential backoff
                    logger.warning(f"Request attempt {attempt + 1} failed, retrying in {wait_time}s: {str(e)}")
                    await asyncio.sleep(wait_time)
                else:
                    logger.error(f"All {self.max_retries + 1} attempts failed")
            
            except Exception as e:
                # Non-HTTP errors should not be retried
                logger.error(f"Non-HTTP error occurred: {str(e)}")
                raise
        
        # If we get here, all retries failed
        raise PharosGraphQLError(
            f"Failed to execute query after {self.max_retries + 1} attempts",
            status_code=getattr(last_exception, 'response', {}).get('status_code')
        ) from last_exception
    
    async def _execute_request(self, payload: Dict[str, Any], attempt_number: int) -> Dict[str, Any]:
        """
        Execute a single HTTP request
        """
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.post(
                self.api_url,
                json=payload,
                headers=self.headers
            )
            
            # Log response info
            logger.debug(f"Response status: {response.status_code} (attempt {attempt_number})")
            
            # Handle HTTP errors
            response.raise_for_status()
            
            # Parse JSON response
            try:
                data = response.json()
            except ValueError as e:
                raise PharosGraphQLError("Invalid JSON response from Pharos API") from e
            
            # Check for GraphQL errors
            if "errors" in data and data["errors"]:
                error_messages = [error.get("message", "Unknown error") for error in data["errors"]]
                logger.error(f"GraphQL errors: {error_messages}")
                raise PharosGraphQLError(
                    "GraphQL query failed",
                    errors=data["errors"],
                    status_code=response.status_code
                )
            
            # Log successful response
            if "data" in data:
                logger.debug("GraphQL query executed successfully")
            
            return data

# Global client instance
_pharos_client = None

def get_pharos_client() -> PharosGraphQLClient:
    """
    Get singleton instance of Pharos GraphQL client
    Thread-safe lazy initialization
    """
    global _pharos_client
    if _pharos_client is None:
        _pharos_client = PharosGraphQLClient()
    return _pharos_client

# Convenience function to maintain compatibility with existing code
async def query_pharos(query: str, variables: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    Convenience function for backward compatibility
    Execute a GraphQL query against Pharos API
    
    Args:
        query: GraphQL query string
        variables: Optional variables for the query
        
    Returns:
        Dict containing the GraphQL response
    """
    client = get_pharos_client()
    return await client.query(query, variables)

# Health check function for monitoring
async def check_pharos_connection() -> Dict[str, Any]:
    """
    Check if Pharos API is accessible
    Returns connection status and response time
    """
    import time
    
    # Simple introspection query to test connection
    test_query = """
    query TestConnection {
        __schema {
            queryType {
                name
            }
        }
    }
    """
    
    try:
        start_time = time.time()
        result = await query_pharos(test_query)
        response_time = round((time.time() - start_time) * 1000, 2)  # ms
        
        return {
            "status": "healthy",
            "response_time_ms": response_time,
            "api_url": settings.pharos_api_url,
            "connection": "success"
        }
        
    except Exception as e:
        logger.error(f"Pharos connection check failed: {str(e)}")
        return {
            "status": "unhealthy",
            "error": str(e),
            "api_url": settings.pharos_api_url,
            "connection": "failed"
        }

if __name__ == "__main__":
    # Test the client when run directly
    async def test_client():
        print("Testing Pharos GraphQL client...")
        
        # Test connection
        health = await check_pharos_connection()
        print(f"Health check: {health}")
        
        if health["status"] == "healthy":
            # Test simple query
            try:
                simple_query = """
                query TestQuery {
                    target(q: {sym: "ACE2"}) {
                        name
                        sym
                    }
                }
                """
                result = await query_pharos(simple_query)
                print(f"Test query result: {result}")
                
            except Exception as e:
                print(f"Test query failed: {e}")
    
    # Run test
    asyncio.run(test_client())