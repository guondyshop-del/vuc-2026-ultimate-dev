"""
VUC-2026 Connection Manager Integration
Enhanced API mapper with ultimate connection resilience
"""

import asyncio
import logging
from typing import Dict, List, Optional, Any
from datetime import datetime
from app.core.connection_resilience import (
    connection_resilience, 
    ConnectionConfig, 
    ConnectionStrategy,
    ConnectionStatus
)
from app.services.full_stack_api_mapper import FullStackAPIMapper, APIEndpoint, APIType, APIStatus

logger = logging.getLogger(__name__)

class EnhancedAPIMapper(FullStackAPIMapper):
    """Enhanced API mapper with VUC-2026 connection resilience"""
    
    def __init__(self):
        super().__init__()
        self.connection_configs: Dict[str, ConnectionConfig] = {}
        self.resilience_enabled = True
        
    async def initialize(self):
        """Initialize with enhanced connection handling"""
        await super().initialize()
        await self._setup_connection_configs()
        await self._start_health_monitoring()
        
    async def _setup_connection_configs(self):
        """Setup connection configurations for all endpoints"""
        for endpoint_name, endpoint in self.endpoints.items():
            # Create connection config based on endpoint type
            config = self._create_connection_config(endpoint_name, endpoint)
            self.connection_configs[endpoint_name] = config
            
            # Start health monitoring
            if self.resilience_enabled:
                await connection_resilience.start_health_monitoring(config)
    
    def _create_connection_config(self, endpoint_name: str, endpoint: APIEndpoint) -> ConnectionConfig:
        """Create connection configuration based on endpoint type"""
        
        # Base configuration
        config = ConnectionConfig(
            url=endpoint.url,
            timeout=30.0,
            max_retries=5,
            retry_delay=1.0,
            max_retry_delay=300.0,
            backoff_multiplier=2.0,
            jitter=True,
            circuit_breaker_threshold=5,
            circuit_breaker_timeout=300.0,
            health_check_interval=30.0,
            connection_pool_size=100,
            keep_alive_timeout=30.0,
            dns_cache_timeout=300.0,
            ssl_verify=True,
            proxy_rotation=False,
            user_agent_rotation=True
        )
        
        # Configure based on API type
        if endpoint.api_type == APIType.PRODUCTION:
            # Production APIs - higher reliability
            config.max_retries = 3
            config.circuit_breaker_threshold = 3
            config.health_check_interval = 60.0
            
            # Add fallback URLs for critical services
            if endpoint_name == "gemini_scripting":
                config.fallback_urls = [
                    "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-pro:generateContent",
                    "https://generativelanguage.googleapis.com/v1/models/gemini-pro:generateContent"
                ]
            elif endpoint_name == "elevenlabs_voice":
                config.fallback_urls = [
                    "https://api.elevenlabs.io/v1/text-to-speech/rachel",
                    "https://api.elevenlabs.io/v1/text-to-speech/amy"
                ]
                
        elif endpoint.api_type == APIType.SEO_ANALYTICS:
            # SEO APIs - moderate reliability with rate limiting
            config.max_retries = 2
            config.circuit_breaker_threshold = 5
            config.health_check_interval = 120.0
            config.retry_delay = 2.0
            
            # Add fallback URLs
            if endpoint_name == "youtube_data":
                config.fallback_urls = [
                    "https://youtube.googleapis.com/youtube/v3",
                    "https://www.googleapis.com/youtube/v3"
                ]
                
        elif endpoint.api_type == APIType.STEALTH:
            # Stealth APIs - high resilience
            config.max_retries = 7
            config.circuit_breaker_threshold = 10
            config.health_check_interval = 90.0
            config.proxy_rotation = True
            
        elif endpoint.api_type == APIType.REVENUE:
            # Revenue APIs - critical for monetization
            config.max_retries = 4
            config.circuit_breaker_threshold = 3
            config.health_check_interval = 45.0
            
            # Add fallback URLs
            if endpoint_name == "amazon_affiliate":
                config.fallback_urls = [
                    "https://webservices.amazon.com/paapi5",
                    "https://webservices.amazon.co.uk/paapi5",
                    "https://webservices.amazon.de/paapi5"
                ]
        
        # Add custom headers based on endpoint config
        if hasattr(endpoint.config, 'gemini_api_key') and endpoint.config.gemini_api_key:
            config.custom_headers["Authorization"] = f"Bearer {endpoint.config.gemini_api_key}"
        elif hasattr(endpoint.config, 'elevenlabs_api_key') and endpoint.config.elevenlabs_api_key:
            config.custom_headers["xi-api-key"] = endpoint.config.elevenlabs_api_key
        elif hasattr(endpoint.config, 'youtube_data_api_key') and endpoint.config.youtube_data_api_key:
            config.custom_headers["Authorization"] = f"Bearer {endpoint.config.youtube_data_api_key}"
        
        return config
    
    async def call_api(self, endpoint_name: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Enhanced API call with resilience"""
        
        if endpoint_name not in self.endpoints:
            raise ValueError(f"Endpoint {endpoint_name} not found")
        
        endpoint = self.endpoints[endpoint_name]
        
        # Check if resilience is enabled
        if self.resilience_enabled and endpoint_name in self.connection_configs:
            config = self.connection_configs[endpoint_name]
            
            try:
                # Use resilience system
                result = await connection_resilience.make_request(
                    config=config,
                    method='POST',
                    data=payload,
                    strategy=ConnectionStrategy.EXPONENTIAL_BACKOFF
                )
                
                # Update endpoint status
                endpoint.status = APIStatus.ACTIVE
                endpoint.last_called = datetime.now()
                
                return result
                
            except Exception as e:
                # Update endpoint status
                endpoint.status = APIStatus.ERROR
                endpoint.error_count += 1
                
                # Fallback to original method if resilience fails
                logger.warning(f"Resilient call failed for {endpoint_name}, falling back: {e}")
                return await super().call_api(endpoint_name, payload)
        
        # Use original method
        return await super().call_api(endpoint_name, payload)
    
    async def get_enhanced_health_status(self) -> Dict[str, Dict[str, Any]]:
        """Get enhanced health status with connection metrics"""
        
        # Get original health status
        base_status = await self.get_api_health_status()
        
        # Add connection resilience metrics
        for endpoint_name in self.endpoints.keys():
            if endpoint_name in self.connection_configs:
                config = self.connection_configs[endpoint_name]
                connection_status = await connection_resilience.get_connection_status(config.url)
                
                if endpoint_name in base_status:
                    base_status[endpoint_name]["connection_resilience"] = connection_status
                else:
                    base_status[endpoint_name] = {
                        "name": endpoint_name,
                        "connection_resilience": connection_status
                    }
        
        return base_status
    
    async def _start_health_monitoring(self):
        """Start health monitoring for all endpoints"""
        for endpoint_name, config in self.connection_configs.items():
            try:
                await connection_resilience.start_health_monitoring(config)
            except Exception as e:
                logger.error(f"Failed to start health monitoring for {endpoint_name}: {e}")
    
    async def cleanup(self):
        """Enhanced cleanup"""
        await super().cleanup()
        await connection_resilience.cleanup()

# Enhanced instance
enhanced_api_mapper = EnhancedAPIMapper()
