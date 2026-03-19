"""
VUC-2026 Connection Diagnostics API
Advanced connection troubleshooting and repair endpoints
"""

from fastapi import APIRouter, HTTPException, BackgroundTasks
from typing import Dict, List, Optional, Any
from pydantic import BaseModel, HttpUrl
import asyncio
import logging

from ..services.connection_diagnostics import connection_diagnostics

router = APIRouter(prefix="/api/connection-diagnostics", tags=["connection-diagnostics"])
logger = logging.getLogger(__name__)

class DiagnosticsRequest(BaseModel):
    url: HttpUrl
    comprehensive: bool = True

class RepairRequest(BaseModel):
    url: HttpUrl
    auto_repair: bool = True

@router.post("/diagnose")
async def diagnose_connection(request: DiagnosticsRequest):
    """Perform comprehensive connection diagnosis"""
    try:
        diagnosis = await connection_diagnostics.comprehensive_diagnosis(str(request.url))
        return diagnosis
        
    except Exception as e:
        logger.error(f"Connection diagnosis failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/repair")
async def repair_connection(request: RepairRequest, background_tasks: BackgroundTasks):
    """Attempt automatic connection repair"""
    try:
        if request.auto_repair:
            # Perform auto-repair
            repair_result = await connection_diagnostics.auto_repair(str(request.url))
            return repair_result
        else:
            # Schedule background repair
            background_tasks.add_task(
                connection_diagnostics.auto_repair, 
                str(request.url)
            )
            return {
                "message": "Connection repair initiated in background",
                "url": str(request.url),
                "timestamp": connection_diagnostics.logger.info("Repair initiated")
            }
            
    except Exception as e:
        logger.error(f"Connection repair failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/test/{endpoint_name}")
async def test_endpoint_endpoint(endpoint_name: str):
    """Test specific endpoint connectivity"""
    try:
        # Get endpoint URL from enhanced API mapper
        from ..services.enhanced_api_mapper import enhanced_api_mapper
        
        if endpoint_name not in enhanced_api_mapper.endpoints:
            raise HTTPException(status_code=404, detail=f"Endpoint {endpoint_name} not found")
        
        endpoint = enhanced_api_mapper.endpoints[endpoint_name]
        diagnosis = await connection_diagnostics.comprehensive_diagnosis(endpoint.url)
        
        return {
            "endpoint": endpoint_name,
            "url": endpoint.url,
            "diagnosis": diagnosis
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Endpoint test failed for {endpoint_name}: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/test/{endpoint_name}/repair")
async def repair_endpoint_endpoint(endpoint_name: str, background_tasks: BackgroundTasks):
    """Repair specific endpoint connectivity"""
    try:
        # Get endpoint URL from enhanced API mapper
        from ..services.enhanced_api_mapper import enhanced_api_mapper
        
        if endpoint_name not in enhanced_api_mapper.endpoints:
            raise HTTPException(status_code=404, detail=f"Endpoint {endpoint_name} not found")
        
        endpoint = enhanced_api_mapper.endpoints[endpoint_name]
        
        # Schedule repair
        background_tasks.add_task(
            connection_diagnostics.auto_repair,
            endpoint.url
        )
        
        return {
            "message": f"Endpoint repair initiated for {endpoint_name}",
            "endpoint": endpoint_name,
            "url": endpoint.url
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Endpoint repair failed for {endpoint_name}: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/tools")
async def get_diagnostic_tools():
    """Get available diagnostic tools"""
    return {
        "available_tools": [
            {
                "name": "dns_resolution",
                "description": "Test DNS resolution with multiple servers",
                "category": "network"
            },
            {
                "name": "network_connectivity",
                "description": "Test TCP connectivity to target",
                "category": "network"
            },
            {
                "name": "ssl_certificate",
                "description": "Test SSL certificate validity",
                "category": "security"
            },
            {
                "name": "http_response",
                "description": "Test HTTP response and headers",
                "category": "application"
            },
            {
                "name": "ping_test",
                "description": "Test ping connectivity",
                "category": "network"
            },
            {
                "name": "trace_route",
                "description": "Trace route to target",
                "category": "network"
            },
            {
                "name": "dns_servers",
                "description": "Test multiple DNS servers",
                "category": "network"
            },
            {
                "name": "port_scan",
                "description": "Scan common ports",
                "category": "network"
            }
        ],
        "auto_repair_actions": [
            "DNS cache clearing",
            "Connection pool reset",
            "Socket connection flush",
            "Circuit breaker reset",
            "Metrics reset"
        ]
    }

@router.get("/status")
async def get_diagnostics_status():
    """Get diagnostics system status"""
    try:
        from ..services.enhanced_api_mapper import enhanced_api_mapper
        from ..core.connection_resilience import connection_resilience
        
        # Get system status
        status = {
            "timestamp": connection_diagnostics.logger.info("Status check"),
            "diagnostics_available": True,
            "connection_resilience_active": True,
            "enhanced_mapper_active": True,
            "monitored_endpoints": len(enhanced_api_mapper.endpoints),
            "connection_pools": len(connection_resilience.pool_manager.pools),
            "circuit_breakers": len(connection_resilience.circuit_breaker.circuits),
            "dns_cache_entries": len(connection_resilience.dns_resolver.dns_cache),
            "health_check_tasks": len(connection_resilience.health_check_tasks)
        }
        
        return status
        
    except Exception as e:
        logger.error(f"Failed to get diagnostics status: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/bulk-diagnose")
async def bulk_diagnose_connections(urls: List[HttpUrl]):
    """Perform bulk diagnosis of multiple URLs"""
    try:
        results = []
        
        # Run diagnoses in parallel
        tasks = [
            connection_diagnostics.comprehensive_diagnosis(str(url))
            for url in urls
        ]
        
        diagnoses = await asyncio.gather(*tasks, return_exceptions=True)
        
        for url, diagnosis in zip(urls, diagnoses):
            if isinstance(diagnosis, Exception):
                results.append({
                    "url": str(url),
                    "status": "error",
                    "error": str(diagnosis)
                })
            else:
                results.append({
                    "url": str(url),
                    "status": "completed",
                    "diagnosis": diagnosis
                })
        
        # Generate summary
        successful = sum(1 for r in results if r["status"] == "completed")
        failed = len(results) - successful
        
        return {
            "timestamp": connection_diagnostics.logger.info("Bulk diagnosis completed"),
            "total_urls": len(urls),
            "successful": successful,
            "failed": failed,
            "results": results
        }
        
    except Exception as e:
        logger.error(f"Bulk diagnosis failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/recommendations")
async def get_connection_recommendations():
    """Get general connection optimization recommendations"""
    return {
        "timestamp": connection_diagnostics.logger.info("Recommendations requested"),
        "recommendations": {
            "dns_optimization": [
                "Use reliable DNS servers (8.8.8.8, 1.1.1.1)",
                "Enable DNS caching with appropriate TTL",
                "Monitor DNS resolution times",
                "Consider DNS load balancing for critical services"
            ],
            "connection_pooling": [
                "Use connection pooling for HTTP clients",
                "Configure appropriate pool sizes based on load",
                "Enable keep-alive connections",
                "Set reasonable connection timeouts"
            ],
            "circuit_breakers": [
                "Implement circuit breakers for external services",
                "Configure appropriate failure thresholds",
                "Set reasonable recovery timeouts",
                "Monitor circuit breaker states"
            ],
            "retry_strategies": [
                "Use exponential backoff for retries",
                "Implement jitter to prevent thundering herd",
                "Set maximum retry limits",
                "Consider different strategies for different error types"
            ],
            "ssl_optimization": [
                "Monitor SSL certificate expiration",
                "Use appropriate SSL/TLS versions",
                "Implement certificate pinning for critical services",
                "Regular security audits"
            ],
            "monitoring": [
                "Implement comprehensive health monitoring",
                "Track response times and success rates",
                "Set up alerts for degraded performance",
                "Regular connection testing"
            ]
        },
        "best_practices": [
            "Always handle network errors gracefully",
            "Implement proper logging for debugging",
            "Use timeouts for all network operations",
            "Monitor resource usage and connection limits",
            "Test failover scenarios regularly",
            "Keep dependencies updated",
            "Document connection configurations",
            "Use environment-specific settings"
        ]
    }
