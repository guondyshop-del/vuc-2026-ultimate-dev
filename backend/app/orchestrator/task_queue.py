"""
VUC-2026 Task Queue System
Advanced task distribution and management system
"""

import os
import asyncio
import json
import logging
import heapq
import uuid
from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from collections import defaultdict, deque
import redis
import pickle
from concurrent.futures import ThreadPoolExecutor
import threading

from .vuc_orchestrator import Task, TaskStatus, TaskPriority

logger = logging.getLogger(__name__)

class QueueType(Enum):
    """Queue type enumeration"""
    HIGH_PRIORITY = "high_priority"
    NORMAL_PRIORITY = "normal_priority"
    LOW_PRIORITY = "low_priority"
    BACKGROUND = "background"
    RETRY = "retry"

@dataclass
class QueueMetrics:
    """Queue performance metrics"""
    tasks_enqueued: int = 0
    tasks_dequeued: int = 0
    tasks_completed: int = 0
    tasks_failed: int = 0
    avg_wait_time: float = 0.0
    avg_execution_time: float = 0.0
    queue_depth: int = 0
    throughput_per_minute: float = 0.0
    last_activity: Optional[datetime] = None

@dataclass
class QueueConfig:
    """Queue configuration"""
    max_size: int = 1000
    max_concurrent_tasks: int = 10
    retry_attempts: int = 3
    retry_delay: int = 60  # seconds
    priority_weights: Dict[TaskPriority, float] = field(default_factory=lambda: {
        TaskPriority.CRITICAL: 1.0,
        TaskPriority.HIGH: 0.8,
        TaskPriority.NORMAL: 0.6,
        TaskPriority.LOW: 0.4,
        TaskPriority.BACKGROUND: 0.2
    })
    dead_letter_queue_size: int = 100

class TaskQueue:
    """
    Advanced task queue system with priority management and monitoring
    """
    
    def __init__(self, queue_type: QueueType = QueueType.NORMAL_PRIORITY):
        self.queue_type = queue_type
        self.redis_client = redis.from_url(os.getenv("REDIS_URL", "redis://localhost:6379/0"))
        
        # Queue storage
        self._queue: List[Task] = []
        self._processing: Dict[str, Task] = {}
        self._completed: deque = deque(maxlen=1000)
        self._failed: deque = deque(maxlen=500)
        self._dead_letter: deque = deque(maxlen=100)
        
        # Metrics
        self.metrics = QueueMetrics()
        
        # Configuration
        self.config = QueueConfig()
        
        # Thread pool for task processing
        self.executor = ThreadPoolExecutor(max_workers=self.config.max_concurrent_tasks)
        
        # Lock for thread safety
        self._lock = threading.RLock()
        
        # Initialize queue
        self._initialize_queue()
        self._start_queue_monitor()
    
    def _initialize_queue(self):
        """Initialize queue system"""
        try:
            # Load configuration
            self._load_queue_config()
            
            # Setup Redis keys
            self.redis_key = f"task_queue:{self.queue_type.value}"
            self.metrics_key = f"queue_metrics:{self.queue_type.value}"
            
            # Load existing tasks from Redis
            self._load_existing_tasks()
            
            logger.info(f"Task queue initialized: {self.queue_type.value}")
            
        except Exception as e:
            logger.error(f"Failed to initialize queue {self.queue_type.value}: {str(e)}")
            raise
    
    def _load_queue_config(self):
        """Load queue configuration"""
        try:
            config_file = f"vuc_memory/queue_configs/{self.queue_type.value}_config.json"
            if os.path.exists(config_file):
                with open(config_file, 'r') as f:
                    config_data = json.load(f)
                    self.config = QueueConfig(**config_data)
                    logger.info(f"Queue configuration loaded: {self.queue_type.value}")
        except Exception as e:
            logger.error(f"Error loading queue configuration: {str(e)}")
    
    def _load_existing_tasks(self):
        """Load existing tasks from Redis"""
        try:
            # Get queued tasks
            queued_tasks = self.redis_client.lrange(self.redis_key, 0, -1)
            for task_data in queued_tasks:
                task_dict = json.loads(task_data)
                task = self._deserialize_task(task_dict)
                heapq.heappush(self._queue, task)
                self.metrics.tasks_enqueued += 1
            
            # Get processing tasks
            processing_key = f"{self.redis_key}:processing"
            processing_tasks = self.redis_client.hgetall(processing_key)
            for task_id, task_data in processing_tasks.items():
                task_dict = json.loads(task_data)
                task = self._deserialize_task(task_dict)
                self._processing[task_id] = task
            
            logger.info(f"Loaded {len(self._queue)} queued tasks and {len(self._processing)} processing tasks")
            
        except Exception as e:
            logger.error(f"Error loading existing tasks: {str(e)}")
    
    def _start_queue_monitor(self):
        """Start queue monitoring thread"""
        try:
            monitor_thread = threading.Thread(
                target=self._queue_monitor_worker,
                daemon=True
            )
            monitor_thread.start()
            
            logger.info(f"Queue monitor started: {self.queue_type.value}")
            
        except Exception as e:
            logger.error(f"Error starting queue monitor: {str(e)}")
    
    def enqueue(self, task: Task) -> bool:
        """Add task to queue"""
        try:
            with self._lock:
                # Check queue size limit
                if len(self._queue) >= self.config.max_size:
                    logger.warning(f"Queue {self.queue_type.value} is full")
                    return False
                
                # Set queue timestamp
                task.metadata['queue_timestamp'] = datetime.utcnow().isoformat()
                task.metadata['queue_type'] = self.queue_type.value
                
                # Add to priority queue
                heapq.heappush(self._queue, task)
                
                # Store in Redis
                task_data = self._serialize_task(task)
                self.redis_client.lpush(self.redis_key, task_data)
                
                # Update metrics
                self.metrics.tasks_enqueued += 1
                self.metrics.queue_depth = len(self._queue)
                self.metrics.last_activity = datetime.utcnow()
                
                logger.info(f"Task enqueued: {task.id} to {self.queue_type.value}")
                return True
                
        except Exception as e:
            logger.error(f"Error enqueuing task {task.id}: {str(e)}")
            return False
    
    def dequeue(self) -> Optional[Task]:
        """Get next task from queue"""
        try:
            with self._lock:
                if not self._queue:
                    return None
                
                # Get highest priority task
                task = heapq.heappop(self._queue)
                
                # Update task status
                task.status = TaskStatus.RUNNING
                task.started_at = datetime.utcnow()
                
                # Move to processing
                self._processing[task.id] = task
                
                # Update Redis
                self.redis_client.lrem(self.redis_key, 1, self._serialize_task(task))
                processing_key = f"{self.redis_key}:processing"
                self.redis_client.hset(processing_key, task.id, self._serialize_task(task))
                
                # Update metrics
                self.metrics.tasks_dequeued += 1
                self.metrics.queue_depth = len(self._queue)
                
                logger.info(f"Task dequeued: {task.id} from {self.queue_type.value}")
                return task
                
        except Exception as e:
            logger.error(f"Error dequeuing task: {str(e)}")
            return None
    
    def complete_task(self, task_id: str, result: Any = None, error: str = None) -> bool:
        """Mark task as completed"""
        try:
            with self._lock:
                if task_id not in self._processing:
                    return False
                
                task = self._processing.pop(task_id)
                task.completed_at = datetime.utcnow()
                
                if error:
                    task.status = TaskStatus.FAILED
                    task.error = error
                    self._failed.append(task)
                    self.metrics.tasks_failed += 1
                else:
                    task.status = TaskStatus.COMPLETED
                    task.result = result
                    self._completed.append(task)
                    self.metrics.tasks_completed += 1
                
                # Calculate execution time
                if task.started_at:
                    execution_time = (task.completed_at - task.started_at).total_seconds()
                    self._update_execution_metrics(execution_time)
                
                # Update Redis
                processing_key = f"{self.redis_key}:processing"
                self.redis_client.hdel(processing_key, task_id)
                
                completed_key = f"{self.redis_key}:completed"
                self.redis_client.lpush(completed_key, self._serialize_task(task))
                
                # Trim completed tasks in Redis
                self.redis_client.ltrim(completed_key, 0, 999)
                
                logger.info(f"Task completed: {task_id} ({'SUCCESS' if not error else 'FAILED'})")
                return True
                
        except Exception as e:
            logger.error(f"Error completing task {task_id}: {str(e)}")
            return False
    
    def retry_task(self, task_id: str) -> bool:
        """Retry failed task"""
        try:
            with self._lock:
                # Find task in failed queue
                failed_task = None
                for i, task in enumerate(self._failed):
                    if task.id == task_id:
                        failed_task = self._failed.pop(i)
                        break
                
                if not failed_task:
                    return False
                
                # Check retry limit
                if failed_task.retry_count >= self.config.retry_attempts:
                    # Move to dead letter queue
                    self._dead_letter.append(failed_task)
                    logger.warning(f"Task {task_id} moved to dead letter queue")
                    return False
                
                # Reset task for retry
                failed_task.status = TaskStatus.RETRYING
                failed_task.retry_count += 1
                failed_task.started_at = None
                failed_task.completed_at = None
                failed_task.error = None
                
                # Add delay for retry
                retry_delay = timedelta(seconds=self.config.retry_delay * (2 ** failed_task.retry_count))
                failed_task.metadata['retry_after'] = (datetime.utcnow() + retry_delay).isoformat()
                
                # Re-enqueue task
                return self.enqueue(failed_task)
                
        except Exception as e:
            logger.error(f"Error retrying task {task_id}: {str(e)}")
            return False
    
    def get_queue_status(self) -> Dict[str, Any]:
        """Get queue status"""
        try:
            with self._lock:
                return {
                    'queue_type': self.queue_type.value,
                    'queue_depth': len(self._queue),
                    'processing_tasks': len(self._processing),
                    'completed_tasks': len(self._completed),
                    'failed_tasks': len(self._failed),
                    'dead_letter_tasks': len(self._dead_letter),
                    'metrics': {
                        'tasks_enqueued': self.metrics.tasks_enqueued,
                        'tasks_dequeued': self.metrics.tasks_dequeued,
                        'tasks_completed': self.metrics.tasks_completed,
                        'tasks_failed': self.metrics.tasks_failed,
                        'avg_wait_time': self.metrics.avg_wait_time,
                        'avg_execution_time': self.metrics.avg_execution_time,
                        'throughput_per_minute': self.metrics.throughput_per_minute,
                        'last_activity': self.metrics.last_activity.isoformat() if self.metrics.last_activity else None
                    },
                    'config': {
                        'max_size': self.config.max_size,
                        'max_concurrent_tasks': self.config.max_concurrent_tasks,
                        'retry_attempts': self.config.retry_attempts
                    }
                }
        except Exception as e:
            logger.error(f"Error getting queue status: {str(e)}")
            return {'error': str(e)}
    
    def get_pending_tasks(self, limit: int = 50) -> List[Dict[str, Any]]:
        """Get pending tasks"""
        try:
            with self._lock:
                tasks = []
                for task in self._queue[:limit]:
                    tasks.append({
                        'id': task.id,
                        'name': task.name,
                        'type': task.type,
                        'priority': task.priority.value,
                        'created_at': task.created_at.isoformat(),
                        'metadata': task.metadata
                    })
                return tasks
        except Exception as e:
            logger.error(f"Error getting pending tasks: {str(e)}")
            return []
    
    def get_processing_tasks(self) -> List[Dict[str, Any]]:
        """Get currently processing tasks"""
        try:
            with self._lock:
                tasks = []
                for task in self._processing.values():
                    tasks.append({
                        'id': task.id,
                        'name': task.name,
                        'type': task.type,
                        'priority': task.priority.value,
                        'started_at': task.started_at.isoformat() if task.started_at else None,
                        'metadata': task.metadata
                    })
                return tasks
        except Exception as e:
            logger.error(f"Error getting processing tasks: {str(e)}")
            return []
    
    def get_failed_tasks(self, limit: int = 50) -> List[Dict[str, Any]]:
        """Get failed tasks"""
        try:
            with self._lock:
                tasks = []
                for task in list(self._failed)[-limit:]:
                    tasks.append({
                        'id': task.id,
                        'name': task.name,
                        'type': task.type,
                        'priority': task.priority.value,
                        'error': task.error,
                        'retry_count': task.retry_count,
                        'completed_at': task.completed_at.isoformat() if task.completed_at else None,
                        'metadata': task.metadata
                    })
                return tasks
        except Exception as e:
            logger.error(f"Error getting failed tasks: {str(e)}")
            return []
    
    def clear_queue(self) -> bool:
        """Clear all tasks from queue"""
        try:
            with self._lock:
                # Move current tasks to failed queue
                for task in self._queue:
                    task.status = TaskStatus.CANCELLED
                    task.error = "Queue cleared"
                    self._failed.append(task)
                
                # Clear queue
                self._queue.clear()
                
                # Clear Redis
                self.redis_client.delete(self.redis_key)
                
                # Update metrics
                self.metrics.queue_depth = 0
                
                logger.info(f"Queue cleared: {self.queue_type.value}")
                return True
                
        except Exception as e:
            logger.error(f"Error clearing queue: {str(e)}")
            return False
    
    def _serialize_task(self, task: Task) -> str:
        """Serialize task for storage"""
        return json.dumps({
            'id': task.id,
            'name': task.name,
            'type': task.type,
            'priority': task.priority.value,
            'status': task.status.value,
            'agent_id': task.agent_id,
            'data': task.data,
            'result': task.result,
            'error': task.error,
            'created_at': task.created_at.isoformat(),
            'started_at': task.started_at.isoformat() if task.started_at else None,
            'completed_at': task.completed_at.isoformat() if task.completed_at else None,
            'retry_count': task.retry_count,
            'max_retries': task.max_retries,
            'timeout': task.timeout,
            'dependencies': task.dependencies,
            'metadata': task.metadata
        })
    
    def _deserialize_task(self, task_dict: Dict[str, Any]) -> Task:
        """Deserialize task from storage"""
        task = Task(
            id=task_dict['id'],
            name=task_dict['name'],
            type=task_dict['type'],
            priority=TaskPriority(task_dict['priority']),
            data=task_dict['data'],
            retry_count=task_dict.get('retry_count', 0),
            max_retries=task_dict.get('max_retries', 3),
            timeout=task_dict.get('timeout', 300),
            dependencies=task_dict.get('dependencies', []),
            metadata=task_dict.get('metadata', {})
        )
        
        task.status = TaskStatus(task_dict.get('status', 'pending'))
        task.agent_id = task_dict.get('agent_id')
        task.result = task_dict.get('result')
        task.error = task_dict.get('error')
        
        if task_dict.get('started_at'):
            task.started_at = datetime.fromisoformat(task_dict['started_at'])
        if task_dict.get('completed_at'):
            task.completed_at = datetime.fromisoformat(task_dict['completed_at'])
        
        return task
    
    def _update_execution_metrics(self, execution_time: float):
        """Update execution time metrics"""
        try:
            # Update average execution time
            total_completed = self.metrics.tasks_completed + self.metrics.tasks_failed
            if total_completed > 0:
                self.metrics.avg_execution_time = (
                    (self.metrics.avg_execution_time * (total_completed - 1) + execution_time) / total_completed
                )
            
            # Update throughput (tasks per minute)
            if self.metrics.last_activity:
                time_diff = (datetime.utcnow() - self.metrics.last_activity).total_seconds()
                if time_diff > 0:
                    self.metrics.throughput_per_minute = (total_completed / time_diff) * 60
            
        except Exception as e:
            logger.error(f"Error updating execution metrics: {str(e)}")
    
    def _queue_monitor_worker(self):
        """Background queue monitor worker"""
        while True:
            try:
                # Check for retry tasks
                self._process_retry_tasks()
                
                # Update metrics
                self._update_queue_metrics()
                
                # Clean up old tasks
                self._cleanup_old_tasks()
                
                # Sleep for next iteration
                import time
                time.sleep(30)  # Check every 30 seconds
                
            except Exception as e:
                logger.error(f"Error in queue monitor: {str(e)}")
                import time
                time.sleep(60)
    
    def _process_retry_tasks(self):
        """Process tasks ready for retry"""
        try:
            current_time = datetime.utcnow()
            retry_tasks = []
            
            # Check failed tasks for retry
            for task in list(self._failed):
                retry_after = task.metadata.get('retry_after')
                if retry_after:
                    retry_time = datetime.fromisoformat(retry_after)
                    if current_time >= retry_time:
                        retry_tasks.append(task)
            
            # Retry tasks
            for task in retry_tasks:
                self.retry_task(task.id)
                
        except Exception as e:
            logger.error(f"Error processing retry tasks: {str(e)}")
    
    def _update_queue_metrics(self):
        """Update queue metrics in Redis"""
        try:
            metrics_data = {
                'tasks_enqueued': self.metrics.tasks_enqueued,
                'tasks_dequeued': self.metrics.tasks_dequeued,
                'tasks_completed': self.metrics.tasks_completed,
                'tasks_failed': self.metrics.tasks_failed,
                'avg_wait_time': self.metrics.avg_wait_time,
                'avg_execution_time': self.metrics.avg_execution_time,
                'queue_depth': len(self._queue),
                'processing_tasks': len(self._processing),
                'throughput_per_minute': self.metrics.throughput_per_minute,
                'last_activity': self.metrics.last_activity.isoformat() if self.metrics.last_activity else None,
                'timestamp': datetime.utcnow().isoformat()
            }
            
            self.redis_client.hset(self.metrics_key, "metrics", json.dumps(metrics_data))
            
        except Exception as e:
            logger.error(f"Error updating queue metrics: {str(e)}")
    
    def _cleanup_old_tasks(self):
        """Clean up old completed and failed tasks"""
        try:
            cutoff_time = datetime.utcnow() - timedelta(hours=24)
            
            # Clean old completed tasks
            while self._completed and self._completed[0].completed_at < cutoff_time:
                self._completed.popleft()
            
            # Clean old failed tasks
            while self._failed and self._failed[0].completed_at < cutoff_time:
                self._failed.popleft()
            
            # Clean dead letter queue
            while len(self._dead_letter) > self.config.dead_letter_queue_size:
                self._dead_letter.popleft()
                
        except Exception as e:
            logger.error(f"Error cleaning up old tasks: {str(e)}")

class TaskQueueManager:
    """
    Manager for multiple task queues
    """
    
    def __init__(self):
        self.queues: Dict[QueueType, TaskQueue] = {}
        self.redis_client = redis.from_url(os.getenv("REDIS_URL", "redis://localhost:6379/0"))
        
        # Initialize queues
        self._initialize_queues()
        
        # Start global monitoring
        self._start_global_monitor()
    
    def _initialize_queues(self):
        """Initialize all queue types"""
        try:
            for queue_type in QueueType:
                self.queues[queue_type] = TaskQueue(queue_type)
            
            logger.info(f"Initialized {len(self.queues)} task queues")
            
        except Exception as e:
            logger.error(f"Error initializing queues: {str(e)}")
    
    def _start_global_monitor(self):
        """Start global queue monitoring"""
        try:
            import threading
            
            monitor_thread = threading.Thread(
                target=self._global_monitor_worker,
                daemon=True
            )
            monitor_thread.start()
            
            logger.info("Global queue monitor started")
            
        except Exception as e:
            logger.error(f"Error starting global monitor: {str(e)}")
    
    def enqueue_task(self, task: Task, queue_type: QueueType = QueueType.NORMAL_PRIORITY) -> bool:
        """Enqueue task to specific queue"""
        if queue_type not in self.queues:
            return False
        
        return self.queues[queue_type].enqueue(task)
    
    def get_next_task(self, queue_types: List[QueueType] = None) -> Optional[Task]:
        """Get next task from specified queues"""
        if queue_types is None:
            queue_types = [QueueType.HIGH_PRIORITY, QueueType.NORMAL_PRIORITY, QueueType.LOW_PRIORITY]
        
        # Check queues in priority order
        for queue_type in queue_types:
            if queue_type in self.queues:
                task = self.queues[queue_type].dequeue()
                if task:
                    return task
        
        return None
    
    def complete_task(self, task_id: str, result: Any = None, error: str = None) -> bool:
        """Complete task (find in any queue)"""
        for queue in self.queues.values():
            if queue.complete_task(task_id, result, error):
                return True
        return False
    
    def get_system_status(self) -> Dict[str, Any]:
        """Get system-wide queue status"""
        try:
            status = {
                'total_queues': len(self.queues),
                'queues': {},
                'system_metrics': {
                    'total_tasks_enqueued': 0,
                    'total_tasks_completed': 0,
                    'total_tasks_failed': 0,
                    'total_queue_depth': 0,
                    'total_processing_tasks': 0
                }
            }
            
            for queue_type, queue in self.queues.items():
                queue_status = queue.get_queue_status()
                status['queues'][queue_type.value] = queue_status
                
                # Aggregate system metrics
                metrics = queue_status.get('metrics', {})
                status['system_metrics']['total_tasks_enqueued'] += metrics.get('tasks_enqueued', 0)
                status['system_metrics']['total_tasks_completed'] += metrics.get('tasks_completed', 0)
                status['system_metrics']['total_tasks_failed'] += metrics.get('tasks_failed', 0)
                status['system_metrics']['total_queue_depth'] += queue_status.get('queue_depth', 0)
                status['system_metrics']['total_processing_tasks'] += queue_status.get('processing_tasks', 0)
            
            return status
            
        except Exception as e:
            logger.error(f"Error getting system status: {str(e)}")
            return {'error': str(e)}
    
    def _global_monitor_worker(self):
        """Global monitoring worker"""
        while True:
            try:
                # Check queue health
                self._check_queue_health()
                
                # Balance load between queues
                self._balance_queue_load()
                
                # Update global metrics
                self._update_global_metrics()
                
                import time
                time.sleep(60)  # Check every minute
                
            except Exception as e:
                logger.error(f"Error in global monitor: {str(e)}")
                import time
                time.sleep(120)
    
    def _check_queue_health(self):
        """Check health of all queues"""
        try:
            for queue_type, queue in self.queues.items():
                status = queue.get_queue_status()
                
                # Check for queue overflow
                if status['queue_depth'] > status['config']['max_size'] * 0.9:
                    logger.warning(f"Queue {queue_type.value} near capacity: {status['queue_depth']}")
                
                # Check for high failure rate
                metrics = status.get('metrics', {})
                total_tasks = metrics.get('tasks_completed', 0) + metrics.get('tasks_failed', 0)
                if total_tasks > 10:
                    failure_rate = metrics.get('tasks_failed', 0) / total_tasks
                    if failure_rate > 0.2:  # 20% failure rate
                        logger.warning(f"High failure rate in queue {queue_type.value}: {failure_rate:.2%}")
                
        except Exception as e:
            logger.error(f"Error checking queue health: {str(e)}")
    
    def _balance_queue_load(self):
        """Balance load between queues"""
        try:
            # Get queue depths
            queue_depths = {}
            for queue_type, queue in self.queues.items():
                status = queue.get_queue_status()
                queue_depths[queue_type] = status['queue_depth']
            
            # Find overloaded and underloaded queues
            avg_depth = sum(queue_depths.values()) / len(queue_depths)
            
            overloaded = [qt for qt, depth in queue_depths.items() if depth > avg_depth * 1.5]
            underloaded = [qt for qt, depth in queue_depths.items() if depth < avg_depth * 0.5]
            
            # Move tasks if needed (simplified logic)
            if overloaded and underloaded:
                logger.info(f"Load balancing needed: {len(overloaded)} overloaded, {len(underloaded)} underloaded")
                
        except Exception as e:
            logger.error(f"Error balancing queue load: {str(e)}")
    
    def _update_global_metrics(self):
        """Update global metrics in Redis"""
        try:
            system_status = self.get_system_status()
            self.redis_client.hset("task_queue_manager", "system_status", json.dumps(system_status))
            
        except Exception as e:
            logger.error(f"Error updating global metrics: {str(e)}")

# Global queue manager instance
task_queue_manager = TaskQueueManager()
