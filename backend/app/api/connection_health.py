"""
VUC-2026 Connection Health Monitor API
Real-time connection monitoring and diagnostics
"""

from fastapi import APIRouter, HTTPException, BackgroundTasks
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
import asyncio
import logging

from ..services.enhanced_api_mapper import enhanced_api_mapper
from ..core.connection_resilience import connection_resilience, ConnectionStatus

router = APIRouter(prefix="/api/connection-health", tags=["connection-health"])
logger = logging.getLogger(__name__)

@router.get("/overview")
async def get_connection_overview():
    """Get comprehensive connection health overview"""
    try:
        # Get enhanced health status
        health_status = await enhanced_api_mapper.get_enhanced_health_status()
        
        # Calculate overall metrics
        total_endpoints = len(health_status)
        healthy_endpoints = 0
        degraded_endpoints = 0
        unhealthy_endpoints = 0
        total_requests = 0
        total_successful = 0
        total_failed = 0
        
        for endpoint_name, status in health_status.items():
            if "connection_resilience" in status:
                conn_status = status["connection_resilience"]
                status_val = conn_status["status"]
                
                if status_val == ConnectionStatus.HEALTHY.value:
                    healthy_endpoints += 1
                elif status_val == ConnectionStatus.DEGRADED.value:
                    degraded_endpoints += 1
                else:
                    unhealthy_endpoints += 1
                
                metrics = conn_status["metrics"]
                total_requests += metrics["total_requests"]
                total_successful += metrics["successful_requests"]
                total_failed += metrics["failed_requests"]
        
        # Calculate overall success rate
        overall_success_rate = (total_successful / total_requests * 100) if total_requests > 0 else 0
        
        return {
            "timestamp": datetime.now().isoformat(),
            "summary": {
                "total_endpoints": total_endpoints,
                "healthy_endpoints": healthy_endpoints,
                "degraded_endpoints": degraded_endpoints,
                "unhealthy_endpoints": unhealthy_endpoints,
                "overall_health_percentage": (healthy_endpoints / total_endpoints * 100) if total_endpoints > 0 else 0,
                "overall_success_rate": overall_success_rate,
                "total_requests": total_requests,
                "total_successful": total_successful,
                "total_failed": total_failed
            },
            "endpoints": health_status
        }
        
    except Exception as e:
        logger.error(f"Failed to get connection overview: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/endpoint/{endpoint_name}")
async def get_endpoint_health(endpoint_name: str):
    """Get detailed health information for specific endpoint"""
    try:
        health_status = await enhanced_api_mapper.get_enhanced_health_status()
        
        if endpoint_name not in health_status:
            raise HTTPException(status_code=404, detail=f"Endpoint {endpoint_name} not found")
        
        endpoint_status = health_status[endpoint_name]
        
        # Add additional diagnostics
        if endpoint_name in enhanced_api_mapper.endpoints:
            endpoint = enhanced_api_mapper.endpoints[endpoint_name]
            endpoint_status["endpoint_info"] = {
                "name": endpoint.name,
                "url": endpoint.url,
                "api_type": endpoint.api_type.value,
                "rate_limit": endpoint.rate_limit,
                "success_rate": endpoint.success_rate,
                "error_count": endpoint.error_count,
                "last_called": endpoint.last_called.isoformat() if endpoint.last_called else None
            }
        
        return endpoint_status
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get endpoint health for {endpoint_name}: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/test/{endpoint_name}")
async def test_endpoint_connection(endpoint_name: str, background_tasks: BackgroundTasks):
    """Test connection to specific endpoint"""
    try:
        if endpoint_name not in enhanced_api_mapper.endpoints:
            raise HTTPException(status_code=404, detail=f"Endpoint {endpoint_name} not found")
        
        # Schedule background test
        background_tasks.add_task(_perform_connection_test, endpoint_name)
        
        return {
            "message": f"Connection test initiated for {endpoint_name}",
            "endpoint": endpoint_name,
            "timestamp": datetime.now().isoformat()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to initiate test for {endpoint_name}: {e}")
        raise HTTPException(status_code=500, detail=str(e))

async def _perform_connection_test(endpoint_name: str):
    """Perform actual connection test"""
    try:
        endpoint = enhanced_api_mapper.endpoints[endpoint_name]
        
        # Create test payload
        test_payload = {
            "test": True,
            "timestamp": datetime.now().isoformat(),
            "source": "connection_health_test"
        }
        
        # Make test call
        result = await enhanced_api_mapper.call_api(endpoint_name, test_payload)
        
        logger.info(f"Connection test successful for {endpoint_name}: {result}")
        
    except Exception as e:
        logger.error(f"Connection test failed for {endpoint_name}: {e}")

@router.get("/metrics")
async def get_connection_metrics():
    """Get detailed connection metrics"""
    try:
        health_status = await enhanced_api_mapper.get_enhanced_health_status()
        
        metrics_summary = {
            "timestamp": datetime.now().isoformat(),
            "endpoints": {},
            "global_metrics": {
                "total_response_time": 0,
                "avg_response_time": 0,
                "min_response_time": float('inf'),
                "max_response_time": 0,
                "total_circuit_breaker_trips": 0,
                "total_fallback_activations": 0,
                "total_rate_limits": 0,
                "total_timeouts": 0,
                "total_dns_errors": 0,
                "total_ssl_errors": 0,
                "total_connection_errors": 0
            }
        }
        
        response_times = []
        
        for endpoint_name, status in health_status.items():
            if "connection_resilience" in status:
                conn_status = status["connection_resilience"]
                metrics = conn_status["metrics"]
                
                metrics_summary["endpoints"][endpoint_name] = {
                    "total_requests": metrics["total_requests"],
                    "successful_requests": metrics["successful_requests"],
                    "failed_requests": metrics["failed_requests"],
                    "success_rate": metrics["success_rate"],
                    "avg_response_time": metrics["avg_response_time"],
                    "min_response_time": metrics["min_response_time"],
                    "max_response_time": metrics["max_response_time"],
                    "timeouts": metrics["timeouts"],
                    "connection_errors": metrics["connection_errors"],
                    "dns_errors": metrics["dns_errors"],
                    "ssl_errors": metrics["ssl_errors"],
                    "rate_limits": metrics["rate_limits"],
                    "circuit_breaker_trips": metrics["circuit_breaker_trips"],
                    "fallback_activations": metrics["fallback_activations"],
                    "last_success": metrics["last_success"],
                    "last_failure": metrics["last_failure"]
                }
                
                # Update global metrics
                global_metrics = metrics_summary["global_metrics"]
                
                if metrics["avg_response_time"] > 0:
                    response_times.append(metrics["avg_response_time"])
                    global_metrics["total_response_time"] += metrics["avg_response_time"]
                    global_metrics["min_response_time"] = min(global_metrics["min_response_time"], metrics["min_response_time"])
                    global_metrics["max_response_time"] = max(global_metrics["max_response_time"], metrics["max_response_time"])
                
                global_metrics["total_circuit_breaker_trips"] += metrics["circuit_breaker_trips"]
                global_metrics["total_fallback_activations"] += metrics["fallback_activations"]
                global_metrics["total_rate_limits"] += metrics["rate_limits"]
                global_metrics["total_timeouts"] += metrics["timeouts"]
                global_metrics["total_dns_errors"] += metrics["dns_errors"]
                global_metrics["total_ssl_errors"] += metrics["ssl_errors"]
                global_metrics["total_connection_errors"] += metrics["connection_errors"]
        
        # Calculate averages
        if response_times:
            metrics_summary["global_metrics"]["avg_response_time"] = sum(response_times) / len(response_times)
        
        if metrics_summary["global_metrics"]["min_response_time"] == float('inf'):
            metrics_summary["global_metrics"]["min_response_time"] = 0
        
        return metrics_summary
        
    except Exception as e:
        logger.error(f"Failed to get connection metrics: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/reset/{endpoint_name}")
async def reset_endpoint_metrics(endpoint_name: str):
    """Reset metrics for specific endpoint"""
    try:
        # Reset circuit breaker
        if endpoint_name in connection_resilience.circuit_breaker.circuits:
            circuit = connection_resilience.circuit_breaker.circuits[endpoint_name]
            circuit['state'] = 'closed'
            circuit['failure_count'] = 0
            circuit['success_count'] = 0
            circuit['half_open_attempts'] = 0
        
        # Reset metrics
        if endpoint_name in connection_resilience.metrics:
            connection_resilience.metrics[endpoint_name] = connection_resilience.ConnectionMetrics()
        
        # Reset endpoint status
        if endpoint_name in enhanced_api_mapper.endpoints:
            endpoint = enhanced_api_mapper.endpoints[endpoint_name]
            endpoint.status = APIStatus.ACTIVE
            endpoint.error_count = 0
            endpoint.success_rate = 1.0
        
        return {
            "message": f"Metrics reset for {endpoint_name}",
            "endpoint": endpoint_name,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Failed to reset metrics for {endpoint_name}: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/alerts")
async def get_connection_alerts():
    """Get active connection alerts"""
    try:
        health_status = await enhanced_api_mapper.get_enhanced_health_status()
        alerts = []
        
        for endpoint_name, status in health_status.items():
            if "connection_resilience" in status:
                conn_status = status["connection_resilience"]
                metrics = conn_status["metrics"]
                circuit = conn_status["circuit_breaker"]
                
                # Check for various alert conditions
                alerts.extend(_generate_alerts(endpoint_name, metrics, circuit))
        
        # Sort alerts by severity
        alerts.sort(key=lambda x: x["severity"], reverse=True)
        
        return {
            "timestamp": datetime.now().isoformat(),
            "total_alerts": len(alerts),
            "alerts": alerts
        }
        
    except Exception as e:
        logger.error(f"Failed to get connection alerts: {e}")
        raise HTTPException(status_code=500, detail=str(e))

def _generate_alerts(endpoint_name: str, metrics: Dict[str, Any], circuit: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Generate alerts based on metrics"""
    alerts = []
    
    # Circuit breaker alerts
    if circuit["state"] == "open":
        alerts.append({
            "endpoint": endpoint_name,
            "type": "circuit_breaker_open",
            "severity": "critical",
            "message": f"Circuit breaker is open for {endpoint_name}",
            "details": f"Failure count: {circuit['failure_count']}, Opened at: {circuit['opened_at']}"
        })
    elif circuit["state"] == "half_open":
        alerts.append({
            "endpoint": endpoint_name,
            "type": "circuit_breaker_half_open",
            "severity": "warning",
            "message": f"Circuit breaker is half-open for {endpoint_name}",
            "details": f"Attempting recovery with {circuit['half_open_attempts']} attempts"
        })
    
    # Success rate alerts
    if metrics["success_rate"] < 50:
        alerts.append({
            "endpoint": endpoint_name,
            "type": "low_success_rate",
            "severity": "critical",
            "message": f"Very low success rate for {endpoint_name}",
            "details": f"Success rate: {metrics['success_rate']:.1f}%"
        })
    elif metrics["success_rate"] < 80:
        alerts.append({
            "endpoint": endpoint_name,
            "type": "degraded_success_rate",
            "severity": "warning",
            "message": f"Degraded success rate for {endpoint_name}",
            "details": f"Success rate: {metrics['success_rate']:.1f}%"
        })
    
    # Response time alerts
    if metrics["avg_response_time"] > 10:
        alerts.append({
            "endpoint": endpoint_name,
            "type": "high_response_time",
            "severity": "warning",
            "message": f"High response time for {endpoint_name}",
            "details": f"Avg response time: {metrics['avg_response_time']:.2f}s"
        })
    
    # Error rate alerts
    if metrics["rate_limits"] > 10:
        alerts.append({
            "endpoint": endpoint_name,
            "type": "high_rate_limiting",
            "severity": "warning",
            "message": f"High rate limiting for {endpoint_name}",
            "details": f"Rate limits: {metrics['rate_limits']}"
        })
    
    if metrics["timeouts"] > 5:
        alerts.append({
            "endpoint": endpoint_name,
            "type": "high_timeouts",
            "severity": "warning",
            "message": f"High timeout rate for {endpoint_name}",
            "details": f"Timeouts: {metrics['timeouts']}"
        })
    
    # DNS/SSL error alerts
    if metrics["dns_errors"] > 0:
        alerts.append({
            "endpoint": endpoint_name,
            "type": "dns_errors",
            "severity": "critical",
            "message": f"DNS errors detected for {endpoint_name}",
            "details": f"DNS errors: {metrics['dns_errors']}"
        })
    
    if metrics["ssl_errors"] > 0:
        alerts.append({
            "endpoint": endpoint_name,
            "type": "ssl_errors",
            "severity": "critical",
            "message": f"SSL errors detected for {endpoint_name}",
            "details": f"SSL errors: {metrics['ssl_errors']}"
        })
    
    return alerts
