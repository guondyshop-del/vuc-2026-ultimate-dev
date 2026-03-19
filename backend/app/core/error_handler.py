"""
VUC-2026 Global Error Handler
Empire Auditor integration with comprehensive error tracking
"""

import logging
import traceback
import uuid
from typing import Dict, Any, Optional
from datetime import datetime
from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.middleware.base import BaseHTTPMiddleware

from ..schemas.core import ErrorResponse, EmpireAuditLog
from ..services.empire_auditor import EmpireAuditorService


class VUCException(Exception):
    """Base VUC-2026 exception with empire auditor integration"""
    
    def __init__(
        self,
        message: str,
        error_code: str = "VUC_ERROR",
        details: Optional[Dict[str, Any]] = None,
        severity: str = "medium",
        component: str = "system"
    ):
        self.message = message
        self.error_code = error_code
        self.details = details or {}
        self.severity = severity
        self.component = component
        self.session_id = str(uuid.uuid4())
        super().__init__(message)


class ValidationError(VUCException):
    """Pydantic validation error wrapper"""
    
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=message,
            error_code="VALIDATION_ERROR",
            details=details,
            severity="low",
            component="validation"
        )


class DatabaseError(VUCException):
    """Database operation error"""
    
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=message,
            error_code="DATABASE_ERROR",
            details=details,
            severity="high",
            component="database"
        )


class ExternalAPIError(VUCException):
    """External API (YouTube/TikTok) error"""
    
    def __init__(self, message: str, api_name: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=message,
            error_code=f"{api_name.upper()}_API_ERROR",
            details=details,
            severity="high",
            component=f"{api_name}_api"
        )


class ProcessingError(VUCException):
    """Video processing/rendering error"""
    
    def __init__(self, message: str, task_type: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=message,
            error_code=f"{task_type.upper()}_PROCESSING_ERROR",
            details=details,
            severity="medium",
            component=f"{task_type}_processor"
        )


class GlobalErrorHandler(BaseHTTPMiddleware):
    """Global error handling middleware with Empire Auditor integration"""
    
    def __init__(self, app):
        super().__init__(app)
        self.logger = logging.getLogger(__name__)
        self.auditor = EmpireAuditorService()
        
    async def dispatch(self, request: Request, call_next):
        try:
            response = await call_next(request)
            return response
            
        except VUCException as exc:
            # Handle VUC-specific exceptions
            await self._log_to_empire_auditor(exc, request)
            return self._create_vuc_error_response(exc)
            
        except HTTPException as exc:
            # Handle FastAPI HTTP exceptions
            vuc_exc = VUCException(
                message=exc.detail,
                error_code=f"HTTP_{exc.status_code}",
                severity="medium",
                component="http"
            )
            await self._log_to_empire_auditor(vuc_exc, request)
            return self._create_vuc_error_response(vuc_exc)
            
        except RequestValidationError as exc:
            # Handle Pydantic validation errors
            details = {"validation_errors": exc.errors()}
            vuc_exc = ValidationError(
                message="Request validation failed",
                details=details
            )
            await self._log_to_empire_auditor(vuc_exc, request)
            return self._create_vuc_error_response(vuc_exc)
            
        except StarletteHTTPException as exc:
            # Handle Starlette HTTP exceptions
            vuc_exc = VUCException(
                message=exc.detail,
                error_code=f"STARLETTE_HTTP_{exc.status_code}",
                severity="medium",
                component="http"
            )
            await self._log_to_empire_auditor(vuc_exc, request)
            return self._create_vuc_error_response(vuc_exc)
            
        except Exception as exc:
            # Handle unexpected exceptions
            vuc_exc = VUCException(
                message="Internal server error",
                error_code="INTERNAL_ERROR",
                details={
                    "exception_type": type(exc).__name__,
                    "traceback": traceback.format_exc()
                },
                severity="critical",
                component="system"
            )
            await self._log_to_empire_auditor(vuc_exc, request)
            return self._create_vuc_error_response(vuc_exc)
    
    async def _log_to_empire_auditor(self, exc: VUCException, request: Request):
        """Log error to Empire Auditor"""
        try:
            audit_log = EmpireAuditLog(
                event_type="error",
                severity=exc.severity,
                component=exc.component,
                message=exc.message,
                metadata={
                    "error_code": exc.error_code,
                    "details": exc.details,
                    "session_id": exc.session_id,
                    "request_path": str(request.url.path),
                    "request_method": request.method,
                    "user_agent": request.headers.get("user-agent"),
                    "client_ip": self._get_client_ip(request)
                }
            )
            
            await self.auditor.log_event(audit_log)
            
        except Exception as log_error:
            # Fallback logging if auditor fails
            self.logger.error(f"Failed to log to Empire Auditor: {log_error}")
            self.logger.error(f"Original error: {exc.message}")
    
    def _get_client_ip(self, request: Request) -> str:
        """Extract client IP from request"""
        forwarded_for = request.headers.get("x-forwarded-for")
        if forwarded_for:
            return forwarded_for.split(",")[0].strip()
        return request.client.host if request.client else "unknown"
    
    def _create_vuc_error_response(self, exc: VUCException) -> JSONResponse:
        """Create standardized error response"""
        error_response = ErrorResponse(
            error_code=exc.error_code,
            error_message=exc.message,
            details=exc.details
        )
        
        # Map severity to HTTP status codes
        status_code_map = {
            "low": 400,
            "medium": 400,
            "high": 500,
            "critical": 500
        }
        
        status_code = status_code_map.get(exc.severity, 500)
        
        return JSONResponse(
            status_code=status_code,
            content=error_response.model_dump()
        )


class DeadLetterQueueHandler:
    """Dead Letter Queue handler for failed tasks"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.auditor = EmpireAuditorService()
    
    async def handle_failed_task(
        self,
        task_id: str,
        task_type: str,
        error: Exception,
        retry_count: int,
        max_retries: int
    ):
        """Handle failed task and move to DLQ if needed"""
        
        if retry_count >= max_retries:
            # Move to Dead Letter Queue
            await self._move_to_dlq(
                task_id=task_id,
                task_type=task_type,
                error=error,
                retry_count=retry_count
            )
        else:
            # Schedule retry with exponential backoff
            await self._schedule_retry(
                task_id=task_id,
                task_type=task_type,
                error=error,
                retry_count=retry_count
            )
    
    async def _move_to_dlq(
        self,
        task_id: str,
        task_type: str,
        error: Exception,
        retry_count: int
    ):
        """Move failed task to Dead Letter Queue"""
        
        audit_log = EmpireAuditLog(
            event_type="dlq_move",
            severity="high",
            component=f"{task_type}_processor",
            message=f"Task {task_id} moved to DLQ after {retry_count} failures",
            metadata={
                "task_id": task_id,
                "task_type": task_type,
                "error": str(error),
                "retry_count": retry_count,
                "traceback": traceback.format_exc()
            }
        )
        
        await self.auditor.log_event(audit_log)
        self.logger.error(f"Task {task_id} moved to DLQ: {error}")
    
    async def _schedule_retry(
        self,
        task_id: str,
        task_type: str,
        error: Exception,
        retry_count: int
    ):
        """Schedule task retry with exponential backoff"""
        
        import math
        delay_seconds = min(300, math.pow(2, retry_count))  # Max 5 minutes
        
        audit_log = EmpireAuditLog(
            event_type="retry_schedule",
            severity="medium",
            component=f"{task_type}_processor",
            message=f"Task {task_id} scheduled for retry #{retry_count + 1}",
            metadata={
                "task_id": task_id,
                "task_type": task_type,
                "error": str(error),
                "retry_count": retry_count,
                "delay_seconds": delay_seconds
            }
        )
        
        await self.auditor.log_event(audit_log)
        self.logger.info(f"Task {task_id} scheduled for retry in {delay_seconds}s")
