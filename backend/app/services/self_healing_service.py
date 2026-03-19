"""
VUC-2026 Self-Healing Service
Production-ready self-healing mechanisms with retry policies and auto-recovery
"""

import asyncio
import logging
import json
import time
import os
from datetime import datetime
from typing import Dict, Any, Optional, Callable
from functools import wraps
from enum import Enum

class RetryStrategy(Enum):
    """Retry strategy types"""
    EXPONENTIAL_BACKOFF = "exponential_backoff"
    LINEAR_BACKOFF = "linear_backoff"
    FIXED_DELAY = "fixed_delay"

class FallbackStrategy(Enum):
    """Fallback strategy types"""
    REDUCE_QUALITY = "reduce_quality"
    SCHEDULE_LATER = "schedule_later"
    USE_ALTERNATIVE = "use_alternative"
    SKIP_OPERATION = "skip_operation"

class SelfHealingService:
    """VUC-2026 Self-Healing Service"""
    
    def __init__(self, log_path: str = "../logs/self_healing.log"):
        self.log_path = log_path
        self.logger = self._setup_logger()
        
        # Retry policies from .windsurfrules
        self.render_retry_policy = {
            "max_retries": 3,
            "retry_delay": 30,
            "exponential_backoff": True,
            "fallback_strategy": "reduce_quality"
        }
        
        self.upload_retry_policy = {
            "max_retries": 5,
            "retry_delay": 60,
            "exponential_backoff": True,
            "fallback_strategy": "schedule_later"
        }
        
        # System alerts thresholds
        self.system_alerts = {
            "disk_space_below_10gb": True,
            "memory_usage_above_90": True,
            "api_quota_exhausted": True,
            "render_queue_overflow": True,
            "upload_failure_rate_above_20": True
        }
        
        # Performance settings
        self.performance_settings = {
            "max_concurrent_renders": 2,
            "max_concurrent_uploads": 1,
            "memory_threshold": 80,
            "cpu_threshold": 90,
            "gpu_threshold": 85
        }
    
    def _setup_logger(self) -> logging.Logger:
        """Setup self-healing logger"""
        logger = logging.getLogger("self_healing")
        logger.setLevel(logging.INFO)
        
        # Create logs directory if not exists
        os.makedirs(os.path.dirname(self.log_path), exist_ok=True)
        
        # File handler
        file_handler = logging.FileHandler(self.log_path, encoding='utf-8')
        file_handler.setLevel(logging.INFO)
        
        # Formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        file_handler.setFormatter(formatter)
        
        # Add handler if not already added
        if not logger.handlers:
            logger.addHandler(file_handler)
        
        return logger
    
    def retry_with_backoff(self, 
                          operation: Callable,
                          policy: Dict[str, Any],
                          operation_type: str = "general",
                          *args, **kwargs) -> Dict[str, Any]:
        """
        Execute operation with retry policy and exponential backoff
        
        Args:
            operation: Function to execute
            policy: Retry policy configuration
            operation_type: Type of operation for logging
            *args, **kwargs: Operation arguments
            
        Returns:
            Operation result with success status
        """
        max_retries = policy.get("max_retries", 3)
        retry_delay = policy.get("retry_delay", 30)
        exponential_backoff = policy.get("exponential_backoff", True)
        fallback_strategy = policy.get("fallback_strategy", "skip_operation")
        
        last_error = None
        attempt = 0
        
        while attempt <= max_retries:
            attempt += 1
            
            try:
                self.logger.info(f"Executing {operation_type} - Attempt {attempt}/{max_retries + 1}")
                
                # Execute the operation
                if asyncio.iscoroutinefunction(operation):
                    result = asyncio.run(operation(*args, **kwargs))
                else:
                    result = operation(*args, **kwargs)
                
                # Success - log and return
                if attempt > 1:
                    self.logger.info(f"{operation_type} succeeded after {attempt} attempts")
                
                return {
                    "success": True,
                    "result": result,
                    "attempts": attempt,
                    "operation_type": operation_type
                }
                
            except Exception as e:
                last_error = e
                
                # Log the error
                self.logger.error(f"{operation_type} failed - Attempt {attempt}/{max_retries + 1}: {str(e)}")
                
                # Check if we should retry
                if attempt <= max_retries:
                    # Calculate delay
                    if exponential_backoff:
                        delay = retry_delay * (2 ** (attempt - 1))
                    else:
                        delay = retry_delay
                    
                    self.logger.info(f"Retrying {operation_type} in {delay} seconds...")
                    
                    # Wait before retry
                    time.sleep(delay)
                else:
                    # Max retries reached - apply fallback strategy
                    self.logger.error(f"{operation_type} failed after {max_retries + 1} attempts - Applying fallback: {fallback_strategy}")
                    
                    return self._apply_fallback_strategy(
                        fallback_strategy, 
                        operation_type, 
                        last_error, 
                        *args, **kwargs
                    )
        
        # This should never be reached
        return {
            "success": False,
            "error": str(last_error),
            "attempts": attempt,
            "operation_type": operation_type
        }
    
    def _apply_fallback_strategy(self, 
                                strategy: str, 
                                operation_type: str, 
                                error: Exception,
                                *args, **kwargs) -> Dict[str, Any]:
        """Apply fallback strategy when operation fails"""
        
        if strategy == "reduce_quality":
            self.logger.info(f"Applying reduce_quality fallback for {operation_type}")
            return {
                "success": False,
                "fallback_applied": "reduce_quality",
                "error": f"Original error: {str(error)} - Fallback: Quality reduced",
                "operation_type": operation_type,
                "suggestion": "Try with lower quality settings"
            }
        
        elif strategy == "schedule_later":
            self.logger.info(f"Applying schedule_later fallback for {operation_type}")
            return {
                "success": False,
                "fallback_applied": "schedule_later",
                "error": f"Original error: {str(error)} - Fallback: Scheduled for later",
                "operation_type": operation_type,
                "suggestion": "Schedule operation for later time"
            }
        
        elif strategy == "use_alternative":
            self.logger.info(f"Applying use_alternative fallback for {operation_type}")
            return {
                "success": False,
                "fallback_applied": "use_alternative",
                "error": f"Original error: {str(error)} - Fallback: Use alternative method",
                "operation_type": operation_type,
                "suggestion": "Try alternative service or method"
            }
        
        else:  # skip_operation
            self.logger.info(f"Applying skip_operation fallback for {operation_type}")
            return {
                "success": False,
                "fallback_applied": "skip_operation",
                "error": f"Original error: {str(error)} - Fallback: Operation skipped",
                "operation_type": operation_type,
                "suggestion": "Operation skipped - continue with next step"
            }
    
    def check_system_health(self) -> Dict[str, Any]:
        """Check system health and return status"""
        import psutil
        
        health_status = {
            "timestamp": datetime.now().isoformat(),
            "overall_health": "healthy",
            "alerts": [],
            "metrics": {}
        }
        
        try:
            # Memory usage
            memory = psutil.virtual_memory()
            memory_percent = memory.percent
            health_status["metrics"]["memory_usage"] = memory_percent
            
            if memory_percent > self.performance_settings["memory_threshold"]:
                health_status["alerts"].append(f"High memory usage: {memory_percent}%")
                health_status["overall_health"] = "warning"
            
            # CPU usage
            cpu_percent = psutil.cpu_percent(interval=1)
            health_status["metrics"]["cpu_usage"] = cpu_percent
            
            if cpu_percent > self.performance_settings["cpu_threshold"]:
                health_status["alerts"].append(f"High CPU usage: {cpu_percent}%")
                health_status["overall_health"] = "warning"
            
            # Disk space
            disk = psutil.disk_usage('/')
            disk_free_gb = disk.free / (1024**3)
            health_status["metrics"]["disk_free_gb"] = disk_free_gb
            
            if disk_free_gb < 10:
                health_status["alerts"].append(f"Low disk space: {disk_free_gb:.1f}GB")
                health_status["overall_health"] = "critical"
            
            # GPU usage (if available)
            try:
                import GPUtil
                gpus = GPUtil.getGPUs()
                if gpus:
                    gpu = gpus[0]
                    gpu_percent = gpu.load * 100
                    health_status["metrics"]["gpu_usage"] = gpu_percent
                    
                    if gpu_percent > self.performance_settings["gpu_threshold"]:
                        health_status["alerts"].append(f"High GPU usage: {gpu_percent}%")
                        if health_status["overall_health"] == "healthy":
                            health_status["overall_health"] = "warning"
            except ImportError:
                health_status["metrics"]["gpu_usage"] = "N/A"
            
            # Log health check
            self.logger.info(f"System health check: {health_status['overall_health']}")
            
            if health_status["alerts"]:
                for alert in health_status["alerts"]:
                    self.logger.warning(alert)
            
            return health_status
            
        except Exception as e:
            self.logger.error(f"System health check failed: {str(e)}")
            return {
                "timestamp": datetime.now().isoformat(),
                "overall_health": "error",
                "alerts": [f"Health check failed: {str(e)}"],
                "metrics": {}
            }
    
    def log_recovery_event(self, 
                          operation_type: str, 
                          original_error: str, 
                          recovery_action: str, 
                          success: bool):
        """Log recovery event for analytics"""
        
        recovery_log = {
            "timestamp": datetime.now().isoformat(),
            "operation_type": operation_type,
            "original_error": original_error,
            "recovery_action": recovery_action,
            "success": success,
            "recovery_id": f"REC-{datetime.now().strftime('%Y%m%d%H%M%S')}"
        }
        
        self.logger.info(f"Recovery event: {json.dumps(recovery_log, ensure_ascii=False, indent=2)}")
        
        return recovery_log

# Decorator for automatic retry
def self_healing_retry(policy: Dict[str, Any], operation_type: str = "general"):
    """Decorator for automatic self-healing retry"""
    
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            healing_service = SelfHealingService()
            return healing_service.retry_with_backoff(
                func, policy, operation_type, *args, **kwargs
            )
        return wrapper
    return decorator

# Global self-healing service instance
self_healing_service = SelfHealingService()
