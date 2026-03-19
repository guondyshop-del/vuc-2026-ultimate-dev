"""
VUC-2026 Base Agent Framework
Foundation for all specialized agents in the orchestrator system
"""

import os
import asyncio
import json
import logging
import uuid
from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
import pickle
import redis
from celery import Celery

logger = logging.getLogger(__name__)

class AgentCapability(Enum):
    """Agent capability enumeration"""
    CONTENT_GENERATION = "content_generation"
    VIDEO_OPTIMIZATION = "video_optimization"
    THUMBNAIL_CREATION = "thumbnail_creation"
    DATA_ANALYSIS = "data_analysis"
    PERFORMANCE_TRACKING = "performance_tracking"
    TREND_DETECTION = "trend_detection"
    VIDEO_UPLOAD = "video_upload"
    METADATA_MANAGEMENT = "metadata_management"
    THUMBNAIL_UPLOAD = "thumbnail_upload"
    SEO_OPTIMIZATION = "seo_optimization"
    KEYWORD_RESEARCH = "keyword_research"
    RANKING_ANALYSIS = "ranking_analysis"
    SOCIAL_MEDIA = "social_media"
    COMMUNITY_MANAGEMENT = "community_management"
    ENGAGEMENT = "engagement"
    MARKET_RESEARCH = "market_research"
    COMPETITOR_ANALYSIS = "competitor_analysis"
    TREND_RESEARCH = "trend_research"

@dataclass
class AgentTask:
    """Agent task data structure"""
    id: str
    type: str
    data: Dict[str, Any]
    priority: int = 3
    timeout: int = 300
    created_at: datetime = field(default_factory=datetime.utcnow)
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    result: Optional[Any] = None
    error: Optional[str] = None
    status: str = "pending"
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class AgentMetrics:
    """Agent performance metrics"""
    tasks_completed: int = 0
    tasks_failed: int = 0
    avg_task_duration: float = 0.0
    success_rate: float = 0.0
    last_task_time: Optional[datetime] = None
    total_execution_time: float = 0.0
    resource_usage: Dict[str, float] = field(default_factory=dict)
    performance_history: List[Dict[str, Any]] = field(default_factory=list)

class BaseAgent(ABC):
    """
    Base agent class for all VUC-2026 specialized agents
    """
    
    def __init__(self, agent_id: str = None, name: str = None, agent_type: str = None):
        self.id = agent_id or str(uuid.uuid4())
        self.name = name or f"Agent-{self.id[:8]}"
        self.type = agent_type or "base"
        
        # Agent state
        self.status = "idle"
        self.current_task: Optional[AgentTask] = None
        self.task_history: List[str] = []
        
        # Capabilities and configuration
        self.capabilities: List[AgentCapability] = []
        self.specialized_tasks: List[str] = []
        self.config: Dict[str, Any] = {}
        
        # Performance tracking
        self.metrics = AgentMetrics()
        self.start_time = datetime.utcnow()
        
        # Resources
        self.redis_client = redis.from_url(os.getenv("REDIS_URL", "redis://localhost:6379/0"))
        self.celery_app = Celery(f'agent_{self.type}', broker=os.getenv("CELERY_BROKER_URL"))
        
        # Initialize agent
        self._initialize_agent()
        self._register_with_orchestrator()
    
    def _initialize_agent(self):
        """Initialize agent-specific configurations"""
        try:
            self._load_configuration()
            self._setup_capabilities()
            self._setup_task_handlers()
            self._start_background_tasks()
            
            logger.info(f"Agent initialized: {self.name} ({self.type})")
            
        except Exception as e:
            logger.error(f"Failed to initialize agent {self.name}: {str(e)}")
            raise
    
    def _load_configuration(self):
        """Load agent configuration"""
        try:
            config_file = f"vuc_memory/agent_configs/{self.type}_config.json"
            if os.path.exists(config_file):
                with open(config_file, 'r') as f:
                    self.config = json.load(f)
                    logger.info(f"Configuration loaded for {self.name}")
            else:
                # Default configuration
                self.config = {
                    'max_concurrent_tasks': 1,
                    'task_timeout': 300,
                    'retry_attempts': 3,
                    'resource_limits': {
                        'memory_mb': 512,
                        'cpu_percent': 50
                    }
                }
        except Exception as e:
            logger.error(f"Error loading configuration for {self.name}: {str(e)}")
    
    def _setup_capabilities(self):
        """Setup agent capabilities"""
        try:
            # This should be overridden by specialized agents
            pass
        except Exception as e:
            logger.error(f"Error setting up capabilities for {self.name}: {str(e)}")
    
    def _setup_task_handlers(self):
        """Setup task handlers"""
        try:
            # Register Celery task handlers
            self.celery_app.task(name=f'agents.{self.type}.execute_task', bind=True)(
                self._execute_task_celery
            )
            
            self.celery_app.task(name=f'agents.{self.type}.get_status', bind=True)(
                self._get_status_celery
            )
            
            logger.info(f"Task handlers setup for {self.name}")
            
        except Exception as e:
            logger.error(f"Error setting up task handlers for {self.name}: {str(e)}")
    
    def _start_background_tasks(self):
        """Start background agent tasks"""
        try:
            import threading
            
            # Health monitor
            health_thread = threading.Thread(
                target=self._health_monitor_worker,
                daemon=True
            )
            health_thread.start()
            
            # Performance reporter
            performance_thread = threading.Thread(
                target=self._performance_reporter_worker,
                daemon=True
            )
            performance_thread.start()
            
            logger.info(f"Background tasks started for {self.name}")
            
        except Exception as e:
            logger.error(f"Error starting background tasks for {self.name}: {str(e)}")
    
    def _register_with_orchestrator(self):
        """Register agent with orchestrator"""
        try:
            from .vuc_orchestrator import vuc_orchestrator
            
            agent_data = {
                'id': self.id,
                'name': self.name,
                'type': self.type,
                'capabilities': [cap.value for cap in self.capabilities],
                'specialized_tasks': self.specialized_tasks,
                'config': self.config,
                'registered_at': datetime.utcnow().isoformat()
            }
            
            self.redis_client.hset("orchestrator:agents", self.id, json.dumps(agent_data))
            
            logger.info(f"Agent registered with orchestrator: {self.name}")
            
        except Exception as e:
            logger.error(f"Error registering agent {self.name} with orchestrator: {str(e)}")
    
    @abstractmethod
    async def execute_task(self, task: AgentTask) -> Any:
        """Execute a task - must be implemented by specialized agents"""
        pass
    
    def _execute_task_celery(self, task_id: str, task_data: Dict[str, Any], agent_id: str = None):
        """Celery task execution wrapper"""
        try:
            # Create task object
            task = AgentTask(
                id=task_id,
                type=task_data.get('type', 'unknown'),
                data=task_data,
                priority=task_data.get('priority', 3),
                timeout=task_data.get('timeout', 300)
            )
            
            # Update status
            self.status = "busy"
            self.current_task = task
            task.status = "running"
            task.started_at = datetime.utcnow()
            
            # Execute task
            start_time = datetime.utcnow()
            
            try:
                result = asyncio.run(self.execute_task(task))
                
                # Update metrics
                duration = (datetime.utcnow() - start_time).total_seconds()
                self._update_task_metrics(True, duration)
                
                # Complete task
                task.result = result
                task.status = "completed"
                task.completed_at = datetime.utcnow()
                
                return result
                
            except Exception as e:
                # Update metrics
                duration = (datetime.utcnow() - start_time).total_seconds()
                self._update_task_metrics(False, duration)
                
                # Complete task with error
                task.error = str(e)
                task.status = "failed"
                task.completed_at = datetime.utcnow()
                
                logger.error(f"Task execution failed for {self.name}: {str(e)}")
                raise
                
            finally:
                # Reset agent state
                self.status = "idle"
                self.current_task = None
                self.task_history.append(task.id)
                
                # Keep only last 100 tasks in history
                if len(self.task_history) > 100:
                    self.task_history = self.task_history[-100:]
                
        except Exception as e:
            logger.error(f"Error in Celery task execution for {self.name}: {str(e)}")
            raise
    
    def _get_status_celery(self):
        """Get agent status via Celery"""
        try:
            return {
                'id': self.id,
                'name': self.name,
                'type': self.type,
                'status': self.status,
                'current_task': self.current_task.id if self.current_task else None,
                'metrics': {
                    'tasks_completed': self.metrics.tasks_completed,
                    'tasks_failed': self.metrics.tasks_failed,
                    'success_rate': self.metrics.success_rate,
                    'avg_task_duration': self.metrics.avg_task_duration,
                    'uptime': (datetime.utcnow() - self.start_time).total_seconds()
                },
                'capabilities': [cap.value for cap in self.capabilities],
                'last_heartbeat': datetime.utcnow().isoformat()
            }
        except Exception as e:
            logger.error(f"Error getting status for {self.name}: {str(e)}")
            return {'error': str(e)}
    
    def _update_task_metrics(self, success: bool, duration: float):
        """Update task performance metrics"""
        try:
            self.metrics.total_execution_time += duration
            
            if success:
                self.metrics.tasks_completed += 1
            else:
                self.metrics.tasks_failed += 1
            
            # Calculate success rate
            total_tasks = self.metrics.tasks_completed + self.metrics.tasks_failed
            if total_tasks > 0:
                self.metrics.success_rate = self.metrics.tasks_completed / total_tasks
            
            # Calculate average duration
            if total_tasks > 0:
                self.metrics.avg_task_duration = self.metrics.total_execution_time / total_tasks
            
            self.metrics.last_task_time = datetime.utcnow()
            
            # Store in performance history
            performance_record = {
                'timestamp': datetime.utcnow().isoformat(),
                'success': success,
                'duration': duration,
                'task_type': self.current_task.type if self.current_task else 'unknown'
            }
            
            self.metrics.performance_history.append(performance_record)
            
            # Keep only last 1000 records
            if len(self.metrics.performance_history) > 1000:
                self.metrics.performance_history = self.metrics.performance_history[-1000:]
            
            # Update Redis
            self.redis_client.hset(f"agent:{self.id}:metrics", "performance", json.dumps({
                'tasks_completed': self.metrics.tasks_completed,
                'tasks_failed': self.metrics.tasks_failed,
                'success_rate': self.metrics.success_rate,
                'avg_task_duration': self.metrics.avg_task_duration,
                'last_task_time': self.metrics.last_task_time.isoformat() if self.metrics.last_task_time else None
            }))
            
        except Exception as e:
            logger.error(f"Error updating metrics for {self.name}: {str(e)}")
    
    def _health_monitor_worker(self):
        """Background health monitor worker"""
        while True:
            try:
                # Check resource usage
                self._check_resource_usage()
                
                # Update heartbeat
                self._update_heartbeat()
                
                # Check for stuck tasks
                self._check_stuck_tasks()
                
                import time
                time.sleep(30)  # Check every 30 seconds
                
            except Exception as e:
                logger.error(f"Error in health monitor for {self.name}: {str(e)}")
                import time
                time.sleep(60)
    
    def _performance_reporter_worker(self):
        """Background performance reporter worker"""
        while True:
            try:
                # Report performance metrics
                self._report_performance_metrics()
                
                # Optimize performance
                self._optimize_performance()
                
                import time
                time.sleep(300)  # Report every 5 minutes
                
            except Exception as e:
                logger.error(f"Error in performance reporter for {self.name}: {str(e)}")
                import time
                time.sleep(600)
    
    def _check_resource_usage(self):
        """Check agent resource usage"""
        try:
            import psutil
            import os
            
            # Memory usage
            process = psutil.Process(os.getpid())
            memory_info = process.memory_info()
            memory_mb = memory_info.rss / 1024 / 1024
            
            # CPU usage
            cpu_percent = process.cpu_percent()
            
            # Update metrics
            self.metrics.resource_usage = {
                'memory_mb': memory_mb,
                'cpu_percent': cpu_percent,
                'threads': process.num_threads(),
                'open_files': len(process.open_files())
            }
            
            # Check limits
            memory_limit = self.config.get('resource_limits', {}).get('memory_mb', 512)
            cpu_limit = self.config.get('resource_limits', {}).get('cpu_percent', 50)
            
            if memory_mb > memory_limit:
                logger.warning(f"High memory usage for {self.name}: {memory_mb:.1f}MB")
            
            if cpu_percent > cpu_limit:
                logger.warning(f"High CPU usage for {self.name}: {cpu_percent:.1f}%")
                
        except Exception as e:
            logger.error(f"Error checking resource usage for {self.name}: {str(e)}")
    
    def _update_heartbeat(self):
        """Update agent heartbeat"""
        try:
            heartbeat_data = {
                'agent_id': self.id,
                'agent_name': self.name,
                'agent_type': self.type,
                'status': self.status,
                'current_task': self.current_task.id if self.current_task else None,
                'timestamp': datetime.utcnow().isoformat(),
                'resource_usage': self.metrics.resource_usage
            }
            
            self.redis_client.hset("orchestrator:agent_heartbeats", self.id, json.dumps(heartbeat_data))
            
        except Exception as e:
            logger.error(f"Error updating heartbeat for {self.name}: {str(e)}")
    
    def _check_stuck_tasks(self):
        """Check for stuck tasks"""
        try:
            if self.current_task and self.current_task.started_at:
                elapsed = (datetime.utcnow() - self.current_task.started_at).total_seconds()
                timeout = self.current_task.timeout or self.config.get('task_timeout', 300)
                
                if elapsed > timeout:
                    logger.warning(f"Task timeout for {self.name}: {self.current_task.id}")
                    
                    # Reset agent state
                    self.status = "idle"
                    self.current_task = None
                    
                    # Update metrics
                    self._update_task_metrics(False, elapsed)
                    
        except Exception as e:
            logger.error(f"Error checking stuck tasks for {self.name}: {str(e)}")
    
    def _report_performance_metrics(self):
        """Report performance metrics"""
        try:
            performance_report = {
                'agent_id': self.id,
                'agent_name': self.name,
                'agent_type': self.type,
                'timestamp': datetime.utcnow().isoformat(),
                'metrics': {
                    'tasks_completed': self.metrics.tasks_completed,
                    'tasks_failed': self.metrics.tasks_failed,
                    'success_rate': self.metrics.success_rate,
                    'avg_task_duration': self.metrics.avg_task_duration,
                    'total_execution_time': self.metrics.total_execution_time,
                    'resource_usage': self.metrics.resource_usage,
                    'uptime': (datetime.utcnow() - self.start_time).total_seconds()
                },
                'performance_history': self.metrics.performance_history[-10:]  # Last 10 records
            }
            
            self.redis_client.hset("orchestrator:agent_performance", self.id, json.dumps(performance_report))
            
        except Exception as e:
            logger.error(f"Error reporting performance metrics for {self.name}: {str(e)}")
    
    def _optimize_performance(self):
        """Optimize agent performance"""
        try:
            # Analyze recent performance
            recent_tasks = self.metrics.performance_history[-50:]  # Last 50 tasks
            
            if len(recent_tasks) > 10:
                # Calculate trends
                success_rate_trend = sum(1 for task in recent_tasks if task['success']) / len(recent_tasks)
                avg_duration_trend = sum(task['duration'] for task in recent_tasks) / len(recent_tasks)
                
                # Log performance insights
                logger.info(f"Performance summary for {self.name}:")
                logger.info(f"  Success rate: {success_rate_trend:.2%}")
                logger.info(f"  Avg duration: {avg_duration_trend:.2f}s")
                logger.info(f"  Tasks completed: {self.metrics.tasks_completed}")
                logger.info(f"  Tasks failed: {self.metrics.tasks_failed}")
                
                # Performance recommendations
                if success_rate_trend < 0.9:
                    logger.warning(f"Low success rate for {self.name}: {success_rate_trend:.2%}")
                
                if avg_duration_trend > self.config.get('task_timeout', 300) * 0.8:
                    logger.warning(f"High average duration for {self.name}: {avg_duration_trend:.2f}s")
                
        except Exception as e:
            logger.error(f"Error optimizing performance for {self.name}: {str(e)}")
    
    def get_status(self) -> Dict[str, Any]:
        """Get agent status"""
        try:
            return {
                'id': self.id,
                'name': self.name,
                'type': self.type,
                'status': self.status,
                'current_task': {
                    'id': self.current_task.id,
                    'type': self.current_task.type,
                    'started_at': self.current_task.started_at.isoformat() if self.current_task.started_at else None
                } if self.current_task else None,
                'capabilities': [cap.value for cap in self.capabilities],
                'specialized_tasks': self.specialized_tasks,
                'metrics': {
                    'tasks_completed': self.metrics.tasks_completed,
                    'tasks_failed': self.metrics.tasks_failed,
                    'success_rate': self.metrics.success_rate,
                    'avg_task_duration': self.metrics.avg_task_duration,
                    'last_task_time': self.metrics.last_task_time.isoformat() if self.metrics.last_task_time else None,
                    'total_execution_time': self.metrics.total_execution_time,
                    'resource_usage': self.metrics.resource_usage
                },
                'config': self.config,
                'start_time': self.start_time.isoformat(),
                'uptime': (datetime.utcnow() - self.start_time).total_seconds()
            }
        except Exception as e:
            logger.error(f"Error getting status for {self.name}: {str(e)}")
            return {'error': str(e)}
    
    def add_capability(self, capability: AgentCapability):
        """Add a capability to the agent"""
        if capability not in self.capabilities:
            self.capabilities.append(capability)
            logger.info(f"Added capability {capability.value} to {self.name}")
    
    def remove_capability(self, capability: AgentCapability):
        """Remove a capability from the agent"""
        if capability in self.capabilities:
            self.capabilities.remove(capability)
            logger.info(f"Removed capability {capability.value} from {self.name}")
    
    def add_specialized_task(self, task_type: str):
        """Add a specialized task type"""
        if task_type not in self.specialized_tasks:
            self.specialized_tasks.append(task_type)
            logger.info(f"Added specialized task {task_type} to {self.name}")
    
    def update_config(self, new_config: Dict[str, Any]):
        """Update agent configuration"""
        try:
            self.config.update(new_config)
            
            # Save configuration
            config_file = f"vuc_memory/agent_configs/{self.type}_config.json"
            os.makedirs(os.path.dirname(config_file), exist_ok=True)
            
            with open(config_file, 'w') as f:
                json.dump(self.config, f, indent=2)
            
            logger.info(f"Configuration updated for {self.name}")
            
        except Exception as e:
            logger.error(f"Error updating configuration for {self.name}: {str(e)}")
    
    def shutdown(self):
        """Shutdown agent gracefully"""
        try:
            logger.info(f"Shutting down agent: {self.name}")
            
            # Complete current task if possible
            if self.current_task:
                logger.warning(f"Agent {self.name} shutting down with active task: {self.current_task.id}")
            
            # Update status
            self.status = "shutdown"
            
            # Update Redis
            self.redis_client.hset("orchestrator:agents", self.id, json.dumps({
                'id': self.id,
                'name': self.name,
                'type': self.type,
                'status': 'shutdown',
                'shutdown_at': datetime.utcnow().isoformat()
            }))
            
            logger.info(f"Agent shutdown complete: {self.name}")
            
        except Exception as e:
            logger.error(f"Error shutting down agent {self.name}: {str(e)}")

# Agent registry for dynamic loading
AGENT_REGISTRY = {}

def register_agent(agent_class):
    """Register an agent class"""
    AGENT_REGISTRY[agent_class.__name__] = agent_class
    return agent_class

def get_agent_class(agent_type: str):
    """Get agent class by type"""
    return AGENT_REGISTRY.get(agent_type)

def create_agent(agent_type: str, **kwargs):
    """Create agent instance"""
    agent_class = get_agent_class(agent_type)
    if agent_class:
        return agent_class(**kwargs)
    else:
        raise ValueError(f"Unknown agent type: {agent_type}")
