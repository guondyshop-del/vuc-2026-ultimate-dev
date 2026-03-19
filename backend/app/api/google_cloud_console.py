"""
VUC-2026 Google Cloud Console API
Complete Google Cloud Console endpoints integration with full documentation
"""

from fastapi import APIRouter, HTTPException, BackgroundTasks, Depends
from typing import Dict, List, Optional, Any
import asyncio
import logging
import os
from datetime import datetime

from ..services.google_cloud_console_service import google_cloud_console_service

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/google-cloud-console", tags=["Google Cloud Console"])

@router.get("/api-documentation")
async def get_all_api_documentation() -> Dict[str, Any]:
    """Get complete API documentation for all Google Cloud services"""
    try:
        result = await google_cloud_console_service.get_all_api_documentation()
        
        if not result["success"]:
            raise HTTPException(status_code=500, detail=result["error"])
        
        return result
        
    except Exception as e:
        logger.error(f"Error getting API documentation: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/services/{service_name}/status")
async def get_service_status(service_name: str) -> Dict[str, Any]:
    """
    Get status and basic information for a specific Google Cloud service
    
    Args:
        service_name: Name of the Google Cloud service
    """
    try:
        result = await google_cloud_console_service.get_service_status(service_name)
        
        if not result["success"]:
            raise HTTPException(status_code=404, detail=result["error"])
        
        return result
        
    except Exception as e:
        logger.error(f"Error getting service status: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/services/status")
async def get_all_services_status() -> Dict[str, Any]:
    """Get status for all available Google Cloud services"""
    try:
        result = await google_cloud_console_service.get_all_services_status()
        
        if not result["success"]:
            raise HTTPException(status_code=500, detail=result["error"])
        
        return result
        
    except Exception as e:
        logger.error(f"Error getting all services status: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/services/{service_name}/call/{endpoint:path}")
async def call_api_endpoint(
    service_name: str, 
    endpoint: str, 
    request_body: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Call a specific Google Cloud API endpoint
    
    Args:
        service_name: Name of the Google Cloud service
        endpoint: API endpoint to call (e.g., 'instances.list' or 'buckets.get')
        request_body: Optional request body parameters
    """
    try:
        # Prepare kwargs from request body
        kwargs = request_body or {}
        
        result = await google_cloud_console_service.call_api_endpoint(
            service_name, endpoint, **kwargs
        )
        
        if not result["success"]:
            raise HTTPException(status_code=400, detail=result["error"])
        
        return result
        
    except Exception as e:
        logger.error(f"Error calling API endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/project/resources")
async def get_project_resources() -> Dict[str, Any]:
    """Get all resources in the project across all services"""
    try:
        result = await google_cloud_console_service.get_project_resources()
        
        if not result["success"]:
            raise HTTPException(status_code=500, detail=result["error"])
        
        return result
        
    except Exception as e:
        logger.error(f"Error getting project resources: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/metrics/api-usage")
async def get_api_usage_metrics(days: int = 7) -> Dict[str, Any]:
    """
    Get API usage metrics for the project
    
    Args:
        days: Number of days to look back (default: 7)
    """
    try:
        if days > 90:
            raise HTTPException(status_code=400, detail="Days parameter too large. Maximum 90 days.")
        
        result = await google_cloud_console_service.get_api_usage_metrics(days)
        
        if not result["success"]:
            raise HTTPException(status_code=500, detail=result["error"])
        
        return result
        
    except Exception as e:
        logger.error(f"Error getting API usage metrics: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/code-generator/{service_name}")
async def generate_api_client_code(
    service_name: str, 
    language: str = "python"
) -> Dict[str, Any]:
    """
    Generate client code for a specific Google Cloud API
    
    Args:
        service_name: Name of the Google Cloud service
        language: Programming language for the client code (python, javascript)
    """
    try:
        if language not in ["python", "javascript"]:
            raise HTTPException(status_code=400, detail="Language must be 'python' or 'javascript'")
        
        result = await google_cloud_console_service.generate_api_client_code(
            service_name, language
        )
        
        if not result["success"]:
            raise HTTPException(status_code=404, detail=result["error"])
        
        return result
        
    except Exception as e:
        logger.error(f"Error generating client code: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# Compute Engine API Endpoints
@router.get("/compute/instances")
async def list_compute_instances(zone: Optional[str] = None) -> Dict[str, Any]:
    """List Compute Engine instances"""
    try:
        if zone:
            result = await google_cloud_console_service.call_api_endpoint(
                "compute", "instances.list", project=os.getenv("GOOGLE_CLOUD_PROJECT"), zone=zone
            )
        else:
            result = await google_cloud_console_service.call_api_endpoint(
                "compute", "instances.aggregatedList", project=os.getenv("GOOGLE_CLOUD_PROJECT")
            )
        
        if not result["success"]:
            raise HTTPException(status_code=500, detail=result["error"])
        
        return result
        
    except Exception as e:
        logger.error(f"Error listing compute instances: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/compute/zones")
async def list_compute_zones() -> Dict[str, Any]:
    """List Compute Engine zones"""
    try:
        result = await google_cloud_console_service.call_api_endpoint(
            "compute", "zones.list", project=os.getenv("GOOGLE_CLOUD_PROJECT")
        )
        
        if not result["success"]:
            raise HTTPException(status_code=500, detail=result["error"])
        
        return result
        
    except Exception as e:
        logger.error(f"Error listing compute zones: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# Cloud Storage API Endpoints
@router.get("/storage/buckets")
async def list_storage_buckets() -> Dict[str, Any]:
    """List Cloud Storage buckets"""
    try:
        result = await google_cloud_console_service.call_api_endpoint(
            "storage", "buckets.list", project=os.getenv("GOOGLE_CLOUD_PROJECT")
        )
        
        if not result["success"]:
            raise HTTPException(status_code=500, detail=result["error"])
        
        return result
        
    except Exception as e:
        logger.error(f"Error listing storage buckets: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# BigQuery API Endpoints
@router.get("/bigquery/datasets")
async def list_bigquery_datasets() -> Dict[str, Any]:
    """List BigQuery datasets"""
    try:
        result = await google_cloud_console_service.call_api_endpoint(
            "bigquery", "datasets.list", projectId=os.getenv("GOOGLE_CLOUD_PROJECT")
        )
        
        if not result["success"]:
            raise HTTPException(status_code=500, detail=result["error"])
        
        return result
        
    except Exception as e:
        logger.error(f"Error listing BigQuery datasets: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/bigquery/datasets/{dataset_id}/tables")
async def list_bigquery_tables(dataset_id: str) -> Dict[str, Any]:
    """List tables in a BigQuery dataset"""
    try:
        result = await google_cloud_console_service.call_api_endpoint(
            "bigquery", "tables.list", 
            projectId=os.getenv("GOOGLE_CLOUD_PROJECT"), 
            datasetId=dataset_id
        )
        
        if not result["success"]:
            raise HTTPException(status_code=500, detail=result["error"])
        
        return result
        
    except Exception as e:
        logger.error(f"Error listing BigQuery tables: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# IAM API Endpoints
@router.get("/iam/service-accounts")
async def list_service_accounts() -> Dict[str, Any]:
    """List IAM service accounts"""
    try:
        result = await google_cloud_console_service.call_api_endpoint(
            "iam", "projects.serviceAccounts.list", 
            name=f"projects/{os.getenv('GOOGLE_CLOUD_PROJECT')}"
        )
        
        if not result["success"]:
            raise HTTPException(status_code=500, detail=result["error"])
        
        return result
        
    except Exception as e:
        logger.error(f"Error listing service accounts: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# Cloud Monitoring API Endpoints
@router.get("/monitoring/metrics")
async def list_monitoring_metrics() -> Dict[str, Any]:
    """List available Cloud Monitoring metrics"""
    try:
        result = await google_cloud_console_service.call_api_endpoint(
            "monitoring", "projects.metricDescriptors.list", 
            name=f"projects/{os.getenv('GOOGLE_CLOUD_PROJECT')}"
        )
        
        if not result["success"]:
            raise HTTPException(status_code=500, detail=result["error"])
        
        return result
        
    except Exception as e:
        logger.error(f"Error listing monitoring metrics: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# Cloud Logging API Endpoints
@router.get("/logging/entries")
async def list_log_entries(
    filter: Optional[str] = None,
    limit: int = 100
) -> Dict[str, Any]:
    """
    List Cloud Logging entries
    
    Args:
        filter: Log filter expression
        limit: Maximum number of entries to return
    """
    try:
        if limit > 1000:
            raise HTTPException(status_code=400, detail="Limit too large. Maximum 1000 entries.")
        
        body = {
            "resourceNames": [f"projects/{os.getenv('GOOGLE_CLOUD_PROJECT')}"],
            "limit": limit
        }
        
        if filter:
            body["filter"] = filter
        
        result = await google_cloud_console_service.call_api_endpoint(
            "logging", "entries.list", body=body
        )
        
        if not result["success"]:
            raise HTTPException(status_code=500, detail=result["error"])
        
        return result
        
    except Exception as e:
        logger.error(f"Error listing log entries: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# Cloud Pub/Sub API Endpoints
@router.get("/pubsub/topics")
async def list_pubsub_topics() -> Dict[str, Any]:
    """List Cloud Pub/Sub topics"""
    try:
        result = await google_cloud_console_service.call_api_endpoint(
            "pubsub", "projects.topics.list", 
            project=f"projects/{os.getenv('GOOGLE_CLOUD_PROJECT')}"
        )
        
        if not result["success"]:
            raise HTTPException(status_code=500, detail=result["error"])
        
        return result
        
    except Exception as e:
        logger.error(f"Error listing Pub/Sub topics: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/pubsub/subscriptions")
async def list_pubsub_subscriptions() -> Dict[str, Any]:
    """List Cloud Pub/Sub subscriptions"""
    try:
        result = await google_cloud_console_service.call_api_endpoint(
            "pubsub", "projects.subscriptions.list", 
            project=f"projects/{os.getenv('GOOGLE_CLOUD_PROJECT')}"
        )
        
        if not result["success"]:
            raise HTTPException(status_code=500, detail=result["error"])
        
        return result
        
    except Exception as e:
        logger.error(f"Error listing Pub/Sub subscriptions: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# Cloud Functions API Endpoints
@router.get("/functions/list")
async def list_cloud_functions() -> Dict[str, Any]:
    """List Cloud Functions"""
    try:
        result = await google_cloud_console_service.call_api_endpoint(
            "functions", "projects.locations.functions.list",
            parent=f"projects/{os.getenv('GOOGLE_CLOUD_PROJECT')}/locations/-"
        )
        
        if not result["success"]:
            raise HTTPException(status_code=500, detail=result["error"])
        
        return result
        
    except Exception as e:
        logger.error(f"Error listing Cloud Functions: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# Cloud Run API Endpoints
@router.get("/run/services")
async def list_cloud_run_services() -> Dict[str, Any]:
    """List Cloud Run services"""
    try:
        result = await google_cloud_console_service.call_api_endpoint(
            "run", "projects.locations.services.list",
            parent=f"projects/{os.getenv('GOOGLE_CLOUD_PROJECT')}/locations/-"
        )
        
        if not result["success"]:
            raise HTTPException(status_code=500, detail=result["error"])
        
        return result
        
    except Exception as e:
        logger.error(f"Error listing Cloud Run services: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# Secret Manager API Endpoints
@router.get("/secretmanager/secrets")
async def list_secrets() -> Dict[str, Any]:
    """List Secret Manager secrets"""
    try:
        result = await google_cloud_console_service.call_api_endpoint(
            "secretmanager", "projects.secrets.list",
            parent=f"projects/{os.getenv('GOOGLE_CLOUD_PROJECT')}"
        )
        
        if not result["success"]:
            raise HTTPException(status_code=500, detail=result["error"])
        
        return result
        
    except Exception as e:
        logger.error(f"Error listing secrets: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# Cloud Build API Endpoints
@router.get("/cloudbuild/builds")
async def list_cloud_builds(limit: int = 100) -> Dict[str, Any]:
    """
    List Cloud Build builds
    
    Args:
        limit: Maximum number of builds to return
    """
    try:
        if limit > 1000:
            raise HTTPException(status_code=400, detail="Limit too large. Maximum 1000 builds.")
        
        result = await google_cloud_console_service.call_api_endpoint(
            "cloudbuild", "projects.builds.list",
            projectId=os.getenv("GOOGLE_CLOUD_PROJECT"),
            pageSize=limit
        )
        
        if not result["success"]:
            raise HTTPException(status_code=500, detail=result["error"])
        
        return result
        
    except Exception as e:
        logger.error(f"Error listing Cloud Builds: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# Artifact Registry API Endpoints
@router.get("/artifactregistry/repositories")
async def list_artifact_repositories() -> Dict[str, Any]:
    """List Artifact Registry repositories"""
    try:
        result = await google_cloud_console_service.call_api_endpoint(
            "artifactregistry", "projects.locations.repositories.list",
            parent=f"projects/{os.getenv('GOOGLE_CLOUD_PROJECT')}/locations/-"
        )
        
        if not result["success"]:
            raise HTTPException(status_code=500, detail=result["error"])
        
        return result
        
    except Exception as e:
        logger.error(f"Error listing Artifact Registry repositories: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# Cloud Scheduler API Endpoints
@router.get("/cloudscheduler/jobs")
async def list_scheduler_jobs() -> Dict[str, Any]:
    """List Cloud Scheduler jobs"""
    try:
        result = await google_cloud_console_service.call_api_endpoint(
            "cloudscheduler", "projects.locations.jobs.list",
            parent=f"projects/{os.getenv('GOOGLE_CLOUD_PROJECT')}/locations/-"
        )
        
        if not result["success"]:
            raise HTTPException(status_code=500, detail=result["error"])
        
        return result
        
    except Exception as e:
        logger.error(f"Error listing Cloud Scheduler jobs: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# Cloud Tasks API Endpoints
@router.get("/cloudtasks/queues")
async def list_task_queues() -> Dict[str, Any]:
    """List Cloud Task queues"""
    try:
        result = await google_cloud_console_service.call_api_endpoint(
            "tasks", "projects.locations.queues.list",
            parent=f"projects/{os.getenv('GOOGLE_CLOUD_PROJECT')}/locations/-"
        )
        
        if not result["success"]:
            raise HTTPException(status_code=500, detail=result["error"])
        
        return result
        
    except Exception as e:
        logger.error(f"Error listing Cloud Task queues: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# Kubernetes Engine API Endpoints
@router.get("/gke/clusters")
async def list_gke_clusters(zone: Optional[str] = None) -> Dict[str, Any]:
    """List Google Kubernetes Engine clusters"""
    try:
        if zone:
            result = await google_cloud_console_service.call_api_endpoint(
                "container", "projects.zones.clusters.list",
                projectId=os.getenv("GOOGLE_CLOUD_PROJECT"),
                zone=zone
            )
        else:
            result = await google_cloud_console_service.call_api_endpoint(
                "container", "projects.locations.clusters.list",
                parent=f"projects/{os.getenv('GOOGLE_CLOUD_PROJECT')}/locations/-"
            )
        
        if not result["success"]:
            raise HTTPException(status_code=500, detail=result["error"])
        
        return result
        
    except Exception as e:
        logger.error(f"Error listing GKE clusters: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# Cloud SQL API Endpoints
@router.get("/sql/instances")
async def list_sql_instances() -> Dict[str, Any]:
    """List Cloud SQL instances"""
    try:
        result = await google_cloud_console_service.call_api_endpoint(
            "sqladmin", "instances.list",
            project=os.getenv("GOOGLE_CLOUD_PROJECT")
        )
        
        if not result["success"]:
            raise HTTPException(status_code=500, detail=result["error"])
        
        return result
        
    except Exception as e:
        logger.error(f"Error listing SQL instances: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# Cloud DNS API Endpoints
@router.get("/dns/managed-zones")
async def list_dns_managed_zones() -> Dict[str, Any]:
    """List Cloud DNS managed zones"""
    try:
        result = await google_cloud_console_service.call_api_endpoint(
            "dns", "projects.managedZones.list",
            project=os.getenv("GOOGLE_CLOUD_PROJECT")
        )
        
        if not result["success"]:
            raise HTTPException(status_code=500, detail=result["error"])
        
        return result
        
    except Exception as e:
        logger.error(f"Error listing DNS managed zones: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/dashboard")
async def get_cloud_dashboard() -> Dict[str, Any]:
    """Get comprehensive Google Cloud dashboard overview"""
    try:
        # Get all services status
        services_status = await google_cloud_console_service.get_all_services_status()
        
        # Get project resources
        project_resources = await google_cloud_console_service.get_project_resources()
        
        # Get API usage metrics
        usage_metrics = await google_cloud_console_service.get_api_usage_metrics(7)
        
        dashboard = {
            "project_id": os.getenv("GOOGLE_CLOUD_PROJECT"),
            "overview": {
                "total_services": services_status.get("total_services", 0),
                "available_services": services_status.get("available_services", 0),
                "permission_denied": services_status.get("permission_denied", 0),
                "errors": services_status.get("errors", 0),
                "resource_types": project_resources.get("total_resource_types", 0)
            },
            "services": services_status.get("services", {}),
            "resources": project_resources.get("resources", {}),
            "usage_metrics": usage_metrics.get("metrics", {}),
            "generated_at": datetime.utcnow().isoformat()
        }
        
        return {
            "success": True,
            "dashboard": dashboard
        }
        
    except Exception as e:
        logger.error(f"Error generating cloud dashboard: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
