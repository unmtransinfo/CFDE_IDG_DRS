"""
Pharos API Gateway - Main FastAPI Application
Connects Galaxy Project with Pharos GraphQL API for target, disease, and ligand data
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import logging
import sys
import os
from datetime import datetime

# Add current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

DEMO_MODE = os.getenv("DEMO_MODE", "false").lower() == "true"

# Import configuration and routers
from config import settings, validate_configuration
from api.targets import router as targets_router
from api.ligands import router as ligands_router
from services.graphql_client import check_pharos_connection
from services.ligand_service import check_ligand_service_health

# Configure logging
logging.basicConfig(
    level=getattr(logging, settings.log_level.upper()),
    format=settings.log_format,
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("pharos_api.log") if not settings.debug else logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

# Create FastAPI application
app = FastAPI(
    title=settings.app_title,
    description=settings.app_description,
    version=settings.app_version,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

# Configure CORS for Galaxy integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

# Include routers
app.include_router(targets_router)
app.include_router(ligands_router)

# Root endpoint
@app.get("/", tags=["root"])
async def root():
    """
    Root endpoint with API information
    """
    return {
        "message": "Welcome to Pharos API Gateway",
        "description": "FastAPI service connecting Galaxy Project with Pharos GraphQL API",
        "version": settings.app_version,
        "docs_url": "/docs",
        "redoc_url": "/redoc",
        "endpoints": {
            "targets": {
                "get_target": "/targets/{gene_symbol}",
                "search_targets": "/targets?search=term",
                "health_check": "/targets/health"
            },
            "ligands": {
                "get_ligand": "/ligands/{ligand_id}",
                "search_ligands": "/ligands?search=term",
                "health_check": "/ligands/health"
            }
        },
        "supported_formats": settings.supported_output_formats,
        "galaxy_integration": {
            "csv_export": "Add ?format=csv to any endpoint",
            "tsv_export": "Add ?format=tsv to any endpoint", 
            "pagination": "Use skip and limit parameters"
        }
    }


# # Health check endpoint
# @app.get("/health", tags=["monitoring"])
# async def health_check():
#     """
#     Simple health check for App Runner
#     """
#     return {"status": "healthy"}


# Health check endpoint
@app.get("/health", tags=["monitoring"])
async def health_check():
    """
    Comprehensive health check for the entire API
    """
    try:
        # Check configuration
        config_ok = validate_configuration()
        
        # Check Pharos connection
        pharos_status = await check_pharos_connection()
        
        # Check ligand service
        ligand_status = await check_ligand_service_health()
        
        # Overall health status
        overall_healthy = (
            config_ok and 
            pharos_status.get("status") == "healthy" and
            ligand_status.get("status") == "healthy"
        )
        
        return {
            "status": "healthy" if overall_healthy else "degraded",
            "timestamp": datetime.now().isoformat(),
            "service": "Pharos API Gateway",
            "version": settings.app_version,
            "checks": {
                "configuration": "ok" if config_ok else "error",
                "pharos_connection": pharos_status,
                "target_service": "available",
                "ligand_service": ligand_status.get("status"),
                "endpoints": {
                    "targets": "available",
                    "ligands": "available",
                    "diseases": "planned"
                }
            },
            "uptime_info": {
                "pharos_url": settings.pharos_api_url,
                "response_time_ms": pharos_status.get("response_time_ms"),
                "rate_limit": f"{settings.rate_limit_per_minute} req/min"
            }
        }
        
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        return JSONResponse(
            status_code=503,
            content={
                "status": "unhealthy",
                "timestamp": datetime.now().isoformat(),
                "error": str(e),
                "service": "Pharos API Gateway"
            }
        )

# API Info endpoint
@app.get("/info", tags=["information"])
async def api_info():
    """
    Detailed API information for developers and Galaxy integration
    """
    return {
        "api": {
            "name": settings.app_title,
            "version": settings.app_version,
            "description": settings.app_description
        },
        "data_source": {
            "name": "Pharos",
            "description": "NIH Common Fund Pharos database",
            "api_url": settings.pharos_api_url,
            "api_type": "GraphQL"
        },
        "endpoints": {
            "targets": {
                "single_target": {
                    "url": "/targets/{gene_symbol}",
                    "method": "GET", 
                    "description": "Get target information by gene symbol",
                    "parameters": {
                        "gene_symbol": "Gene symbol (e.g., EGFR, TP53)",
                        "format": "Response format (json, csv, tsv)"
                    },
                    "example": "/targets/EGFR?format=csv"
                },
                "search_targets": {
                    "url": "/targets",
                    "method": "GET",
                    "description": "Search targets by keyword",
                    "parameters": {
                        "search": "Search term (required)",
                        "skip": "Number of results to skip",
                        "limit": "Maximum results (1-100)",
                        "format": "Response format (json, csv, tsv)"
                    },
                    "example": "/targets?search=kinase&limit=10&format=csv"
                }
            },
            "ligands": {
                "single_ligand": {
                    "url": "/ligands/{ligand_id}",
                    "method": "GET",
                    "description": "Get ligand information by identifier",
                    "parameters": {
                        "ligand_id": "Ligand identifier (e.g., haloperidol, aspirin)",
                        "format": "Response format (json, csv, tsv)"
                    },
                    "example": "/ligands/aspirin?format=csv"
                },
                "search_ligands": {
                    "url": "/ligands",
                    "method": "GET",
                    "description": "Search ligands by keyword",
                    "parameters": {
                        "search": "Search term (required)",
                        "skip": "Number of results to skip",
                        "limit": "Maximum results (1-100)",
                        "format": "Response format (json, csv, tsv)"
                    },
                    "example": "/ligands?search=aspirin&limit=10&format=csv"
                }
            }
        },
        "galaxy_integration": {
            "csv_export": "All endpoints support CSV export with ?format=csv",
            "pagination": "Use skip/limit parameters for large datasets",
            "error_handling": "Consistent error responses with HTTP status codes",
            "batch_operations": "Planned for future version"
        },
        "rate_limits": {
            "requests_per_minute": settings.rate_limit_per_minute,
            "max_page_size": settings.max_page_size
        },
        "development": {
            "github": "https://github.com/your-repo/pharos-api-gateway",
            "documentation": "/docs",
            "openapi_spec": "/openapi.json"
        }
    }


# @app.on_event("startup")
# async def startup_event():
#     logger.info("Starting Pharos API Gateway...")

#     if not DEMO_MODE:
#         # Only run these checks if NOT in demo mode
#         if not validate_configuration():
#             raise RuntimeError("Invalid configuration")
        
#         try:
#             connection_status = await check_pharos_connection()
#             if connection_status["status"] != "healthy":
#                 logger.warning("Pharos connection degraded")
#         except Exception as e:
#             logger.error(f"Pharos connection failed: {e}")

#     logger.info("Pharos API Gateway startup complete")


# Startup event
@app.on_event("startup")
async def startup_event():
    """
    Application startup tasks
    """
    logger.info("Starting Pharos API Gateway...")
    logger.info(f"Version: {settings.app_version}")
    logger.info(f"Debug mode: {settings.debug}")
    logger.info(f"Pharos API URL: {settings.pharos_api_url}")
    
    # Validate configuration
    if not validate_configuration():
        logger.error("Configuration validation failed!")
        raise RuntimeError("Invalid configuration")
    
    # Test Pharos connection
    try:
        connection_status = await check_pharos_connection()
        if connection_status["status"] == "healthy":
            logger.info(f"✅ Connected to Pharos API (response time: {connection_status['response_time_ms']}ms)")
        else:
            logger.warning(f"⚠️ Pharos connection degraded: {connection_status}")
    except Exception as e:
        logger.error(f"❌ Failed to connect to Pharos API: {str(e)}")
        # Don't fail startup - API can still work for cached data or other sources
    
    logger.info("🚀 Pharos API Gateway started successfully!")
    logger.info(f"📖 API documentation available at: http://{settings.host}:{settings.port}/docs")

# Shutdown event  
@app.on_event("shutdown")
async def shutdown_event():
    """
    Application shutdown tasks
    """
    logger.info("Shutting down Pharos API Gateway...")
    logger.info("✅ Shutdown complete")

# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """
    Global exception handler for unhandled errors
    """
    logger.error(f"Unhandled exception: {str(exc)}", exc_info=True)
    
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "message": "An unexpected error occurred",
            "timestamp": datetime.now().isoformat(),
            "request_url": str(request.url) if hasattr(request, 'url') else "unknown"
        }
    )

# Custom 404 handler
@app.exception_handler(404)
async def not_found_handler(request, exc):
    """
    Custom 404 handler with helpful information
    """
    return JSONResponse(
        status_code=404,
        content={
            "error": "Not found",
            "message": f"The requested endpoint does not exist",
            "available_endpoints": [
                "/",
                "/health", 
                "/info",
                "/docs",
                "/targets/{gene_symbol}",
                "/targets?search=term",
                "/ligands/{ligand_id}",
                "/ligands?search=term"
            ],
            "timestamp": datetime.now().isoformat()
        }
    )

# Run the application
if __name__ == "__main__":
    import uvicorn
    
    logger.info("Starting development server...")
    uvicorn.run(
        "main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug,
        log_level=settings.log_level.lower()
    )



# """
# Pharos API Gateway - Main FastAPI Application
# Connects Galaxy Project with Pharos GraphQL API for target, disease, and ligand data
# """

# from fastapi import FastAPI, HTTPException
# from fastapi.middleware.cors import CORSMiddleware
# from fastapi.responses import JSONResponse
# import logging
# import sys
# import os
# from datetime import datetime

# # Add current directory to Python path
# sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# # Import configuration and routers
# from config import settings, validate_configuration
# from api.targets import router as targets_router
# from services.graphql_client import check_pharos_connection

# # Configure logging
# logging.basicConfig(
#     level=getattr(logging, settings.log_level.upper()),
#     format=settings.log_format,
#     handlers=[
#         logging.StreamHandler(),
#         logging.FileHandler("pharos_api.log") if not settings.debug else logging.StreamHandler()
#     ]
# )

# logger = logging.getLogger(__name__)

# # Create FastAPI application
# app = FastAPI(
#     title=settings.app_title,
#     description=settings.app_description,
#     version=settings.app_version,
#     docs_url="/docs",
#     redoc_url="/redoc",
#     openapi_url="/openapi.json"
# )

# # Configure CORS for Galaxy integration
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],  # Configure appropriately for production
#     allow_credentials=True,
#     allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
#     allow_headers=["*"],
# )

# # Include routers
# app.include_router(targets_router)

# # Root endpoint
# @app.get("/", tags=["root"])
# async def root():
#     """
#     Root endpoint with API information
#     """
#     return {
#         "message": "Welcome to Pharos API Gateway",
#         "description": "FastAPI service connecting Galaxy Project with Pharos GraphQL API",
#         "version": settings.app_version,
#         "docs_url": "/docs",
#         "redoc_url": "/redoc",
#         "endpoints": {
#             "targets": {
#                 "get_target": "/targets/{gene_symbol}",
#                 "search_targets": "/targets?search=term",
#                 "health_check": "/targets/health"
#             }
#         },
#         "supported_formats": settings.supported_output_formats,
#         "galaxy_integration": {
#             "csv_export": "Add ?format=csv to any endpoint",
#             "tsv_export": "Add ?format=tsv to any endpoint", 
#             "pagination": "Use skip and limit parameters"
#         }
#     }

# # Health check endpoint
# @app.get("/health", tags=["monitoring"])
# async def health_check():
#     """
#     Comprehensive health check for the entire API
#     """
#     try:
#         # Check configuration
#         config_ok = validate_configuration()
        
#         # Check Pharos connection
#         pharos_status = await check_pharos_connection()
        
#         # Overall health status
#         overall_healthy = (
#             config_ok and 
#             pharos_status.get("status") == "healthy"
#         )
        
#         return {
#             "status": "healthy" if overall_healthy else "degraded",
#             "timestamp": datetime.now().isoformat(),
#             "service": "Pharos API Gateway",
#             "version": settings.app_version,
#             "checks": {
#                 "configuration": "ok" if config_ok else "error",
#                 "pharos_connection": pharos_status,
#                 "endpoints": {
#                     "targets": "available",
#                     "diseases": "development", 
#                     "ligands": "planned"
#                 }
#             },
#             "uptime_info": {
#                 "pharos_url": settings.pharos_api_url,
#                 "response_time_ms": pharos_status.get("response_time_ms"),
#                 "rate_limit": f"{settings.rate_limit_per_minute} req/min"
#             }
#         }
        
#     except Exception as e:
#         logger.error(f"Health check failed: {str(e)}")
#         return JSONResponse(
#             status_code=503,
#             content={
#                 "status": "unhealthy",
#                 "timestamp": datetime.now().isoformat(),
#                 "error": str(e),
#                 "service": "Pharos API Gateway"
#             }
#         )

# # API Info endpoint
# @app.get("/info", tags=["information"])
# async def api_info():
#     """
#     Detailed API information for developers and Galaxy integration
#     """
#     return {
#         "api": {
#             "name": settings.app_title,
#             "version": settings.app_version,
#             "description": settings.app_description
#         },
#         "data_source": {
#             "name": "Pharos",
#             "description": "NIH Common Fund Pharos database",
#             "api_url": settings.pharos_api_url,
#             "api_type": "GraphQL"
#         },
#         "endpoints": {
#             "targets": {
#                 "single_target": {
#                     "url": "/targets/{gene_symbol}",
#                     "method": "GET", 
#                     "description": "Get target information by gene symbol",
#                     "parameters": {
#                         "gene_symbol": "Gene symbol (e.g., EGFR, TP53)",
#                         "format": "Response format (json, csv, tsv)"
#                     },
#                     "example": "/targets/EGFR?format=csv"
#                 },
#                 "search_targets": {
#                     "url": "/targets",
#                     "method": "GET",
#                     "description": "Search targets by keyword",
#                     "parameters": {
#                         "search": "Search term (required)",
#                         "skip": "Number of results to skip",
#                         "limit": "Maximum results (1-100)",
#                         "format": "Response format (json, csv, tsv)"
#                     },
#                     "example": "/targets?search=kinase&limit=10&format=csv"
#                 }
#             }
#         },
#         "galaxy_integration": {
#             "csv_export": "All endpoints support CSV export with ?format=csv",
#             "pagination": "Use skip/limit parameters for large datasets",
#             "error_handling": "Consistent error responses with HTTP status codes",
#             "batch_operations": "Planned for future version"
#         },
#         "rate_limits": {
#             "requests_per_minute": settings.rate_limit_per_minute,
#             "max_page_size": settings.max_page_size
#         },
#         "development": {
#             "github": "https://github.com/your-repo/pharos-api-gateway",
#             "documentation": "/docs",
#             "openapi_spec": "/openapi.json"
#         }
#     }

# # Startup event
# @app.on_event("startup")
# async def startup_event():
#     """
#     Application startup tasks
#     """
#     logger.info("Starting Pharos API Gateway...")
#     logger.info(f"Version: {settings.app_version}")
#     logger.info(f"Debug mode: {settings.debug}")
#     logger.info(f"Pharos API URL: {settings.pharos_api_url}")
    
#     # Validate configuration
#     if not validate_configuration():
#         logger.error("Configuration validation failed!")
#         raise RuntimeError("Invalid configuration")
    
#     # Test Pharos connection
#     try:
#         connection_status = await check_pharos_connection()
#         if connection_status["status"] == "healthy":
#             logger.info(f"✅ Connected to Pharos API (response time: {connection_status['response_time_ms']}ms)")
#         else:
#             logger.warning(f"⚠️ Pharos connection degraded: {connection_status}")
#     except Exception as e:
#         logger.error(f"❌ Failed to connect to Pharos API: {str(e)}")
#         # Don't fail startup - API can still work for cached data or other sources
    
#     logger.info("🚀 Pharos API Gateway started successfully!")
#     logger.info(f"📖 API documentation available at: http://{settings.host}:{settings.port}/docs")

# # Shutdown event  
# @app.on_event("shutdown")
# async def shutdown_event():
#     """
#     Application shutdown tasks
#     """
#     logger.info("Shutting down Pharos API Gateway...")
#     logger.info("✅ Shutdown complete")

# # Global exception handler
# @app.exception_handler(Exception)
# async def global_exception_handler(request, exc):
#     """
#     Global exception handler for unhandled errors
#     """
#     logger.error(f"Unhandled exception: {str(exc)}", exc_info=True)
    
#     return JSONResponse(
#         status_code=500,
#         content={
#             "error": "Internal server error",
#             "message": "An unexpected error occurred",
#             "timestamp": datetime.now().isoformat(),
#             "request_url": str(request.url) if hasattr(request, 'url') else "unknown"
#         }
#     )

# # Custom 404 handler
# @app.exception_handler(404)
# async def not_found_handler(request, exc):
#     """
#     Custom 404 handler with helpful information
#     """
#     return JSONResponse(
#         status_code=404,
#         content={
#             "error": "Not found",
#             "message": f"The requested endpoint does not exist",
#             "available_endpoints": [
#                 "/",
#                 "/health", 
#                 "/info",
#                 "/docs",
#                 "/targets/{gene_symbol}",
#                 "/targets?search=term"
#             ],
#             "timestamp": datetime.now().isoformat()
#         }
#     )

# # Run the application
# if __name__ == "__main__":
#     import uvicorn
    
#     logger.info("Starting development server...")
#     uvicorn.run(
#         "main:app",
#         host=settings.host,
#         port=settings.port,
#         reload=settings.debug,
#         log_level=settings.log_level.lower()
#     )