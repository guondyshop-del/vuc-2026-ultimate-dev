"""
VUC-2026 Workflow Engine
Advanced workflow orchestration and task sequencing system
"""

import os
import asyncio
import json
import logging
import uuid
from typing import Dict, List, Optional, Any, Callable, Set
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from collections import defaultdict, deque
import networkx as nx
import redis
import pickle
import threading
from concurrent.futures import ThreadPoolExecutor

from .vuc_orchestrator import Task, TaskStatus, TaskPriority
from .task_queue import task_queue_manager, QueueType
from .agents.base_agent import BaseAgent

logger = logging.getLogger(__name__)

class WorkflowStatus(Enum):
    """Workflow status enumeration"""
    PENDING = "pending"
    RUNNING = "running"
    PAUSED = "paused"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"

class TaskExecutionMode(Enum):
    """Task execution mode"""
    SEQUENTIAL = "sequential"
    PARALLEL = "parallel"
    CONDITIONAL = "conditional"
    PIPELINE = "pipeline"

@dataclass
class WorkflowStep:
    """Workflow step definition"""
    id: str
    name: str
    task_type: str
    execution_mode: TaskExecutionMode = TaskExecutionMode.SEQUENTIAL
    dependencies: List[str] = field(default_factory=list)
    conditions: Dict[str, Any] = field(default_factory=dict)
    task_data: Dict[str, Any] = field(default_factory=dict)
    agent_type: Optional[str] = None
    priority: TaskPriority = TaskPriority.NORMAL
    timeout: int = 300
    retry_count: int = 0
    max_retries: int = 3
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def __hash__(self):
        return hash(self.id)

@dataclass
class WorkflowDefinition:
    """Workflow definition"""
    id: str
    name: str
    description: str
    steps: List[WorkflowStep] = field(default_factory=list)
    triggers: List[Dict[str, Any]] = field(default_factory=list)
    variables: Dict[str, Any] = field(default_factory=dict)
    settings: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
    version: int = 1

@dataclass
class WorkflowInstance:
    """Workflow instance (execution)"""
    id: str
    workflow_id: str
    status: WorkflowStatus = WorkflowStatus.PENDING
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    current_step: Optional[str] = None
    completed_steps: Set[str] = field(default_factory=set)
    failed_steps: Set[str] = field(default_factory=set)
    step_results: Dict[str, Any] = field(default_factory=dict)
    step_errors: Dict[str, str] = field(default_factory=dict)
    variables: Dict[str, Any] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)

class WorkflowEngine:
    """
    Advanced workflow engine for task orchestration
    """
    
    def __init__(self):
        self.redis_client = redis.from_url(os.getenv("REDIS_URL", "redis://localhost:6379/0"))
        
        # Workflow storage
        self.workflows: Dict[str, WorkflowDefinition] = {}
        self.instances: Dict[str, WorkflowInstance] = {}
        
        # Execution state
        self.running_workflows: Dict[str, WorkflowInstance] = {}
        self.paused_workflows: Dict[str, WorkflowInstance] = {}
        
        # Task tracking
        self.workflow_tasks: Dict[str, Dict[str, str]] = defaultdict(dict)  # workflow_id -> step_id -> task_id
        
        # Thread pool for workflow execution
        self.executor = ThreadPoolExecutor(max_workers=10)
        
        # Lock for thread safety
        self._lock = threading.RLock()
        
        # Initialize workflow engine
        self._initialize_engine()
        self._start_workflow_monitor()
    
    def _initialize_engine(self):
        """Initialize workflow engine"""
        try:
            # Load workflow definitions
            self._load_workflow_definitions()
            
            # Load running instances
            self._load_workflow_instances()
            
            # Setup Redis keys
            self.workflows_key = "workflow_engine:workflows"
            self.instances_key = "workflow_engine:instances"
            self.running_key = "workflow_engine:running"
            
            logger.info("Workflow engine initialized")
            
        except Exception as e:
            logger.error(f"Failed to initialize workflow engine: {str(e)}")
            raise
    
    def _load_workflow_definitions(self):
        """Load workflow definitions from storage"""
        try:
            # Load from Redis
            workflow_data = self.redis_client.hgetall(self.workflows_key)
            for workflow_id, data in workflow_data.items():
                workflow_dict = json.loads(data)
                workflow = self._deserialize_workflow(workflow_dict)
                self.workflows[workflow_id] = workflow
            
            # Load from file system
            workflow_dir = "vuc_memory/workflows"
            if os.path.exists(workflow_dir):
                for filename in os.listdir(workflow_dir):
                    if filename.endswith('.json'):
                        filepath = os.path.join(workflow_dir, filename)
                        with open(filepath, 'r') as f:
                            workflow_dict = json.load(f)
                            workflow = self._deserialize_workflow(workflow_dict)
                            self.workflows[workflow.id] = workflow
            
            logger.info(f"Loaded {len(self.workflows)} workflow definitions")
            
        except Exception as e:
            logger.error(f"Error loading workflow definitions: {str(e)}")
    
    def _load_workflow_instances(self):
        """Load workflow instances from storage"""
        try:
            # Load from Redis
            instance_data = self.redis_client.hgetall(self.instances_key)
            for instance_id, data in instance_data.items():
                instance_dict = json.loads(data)
                instance = self._deserialize_instance(instance_dict)
                self.instances[instance_id] = instance
                
                # Add to running or paused if appropriate
                if instance.status == WorkflowStatus.RUNNING:
                    self.running_workflows[instance_id] = instance
                elif instance.status == WorkflowStatus.PAUSED:
                    self.paused_workflows[instance_id] = instance
            
            logger.info(f"Loaded {len(self.instances)} workflow instances")
            
        except Exception as e:
            logger.error(f"Error loading workflow instances: {str(e)}")
    
    def _start_workflow_monitor(self):
        """Start workflow monitoring thread"""
        try:
            monitor_thread = threading.Thread(
                target=self._workflow_monitor_worker,
                daemon=True
            )
            monitor_thread.start()
            
            logger.info("Workflow monitor started")
            
        except Exception as e:
            logger.error(f"Error starting workflow monitor: {str(e)}")
    
    def create_workflow(self, 
                       name: str,
                       description: str,
                       steps: List[Dict[str, Any]],
                       triggers: List[Dict[str, Any]] = None,
                       variables: Dict[str, Any] = None,
                       settings: Dict[str, Any] = None) -> str:
        """Create a new workflow definition"""
        try:
            workflow_id = str(uuid.uuid4())
            
            # Convert step dictionaries to WorkflowStep objects
            workflow_steps = []
            for step_data in steps:
                step = WorkflowStep(
                    id=step_data.get('id', str(uuid.uuid4())),
                    name=step_data.get('name', ''),
                    task_type=step_data.get('task_type', ''),
                    execution_mode=TaskExecutionMode(step_data.get('execution_mode', 'sequential')),
                    dependencies=step_data.get('dependencies', []),
                    conditions=step_data.get('conditions', {}),
                    task_data=step_data.get('task_data', {}),
                    agent_type=step_data.get('agent_type'),
                    priority=TaskPriority(step_data.get('priority', 3)),
                    timeout=step_data.get('timeout', 300),
                    max_retries=step_data.get('max_retries', 3),
                    metadata=step_data.get('metadata', {})
                )
                workflow_steps.append(step)
            
            # Create workflow definition
            workflow = WorkflowDefinition(
                id=workflow_id,
                name=name,
                description=description,
                steps=workflow_steps,
                triggers=triggers or [],
                variables=variables or {},
                settings=settings or {}
            )
            
            # Validate workflow
            if not self._validate_workflow(workflow):
                raise ValueError("Invalid workflow definition")
            
            # Store workflow
            self.workflows[workflow_id] = workflow
            
            # Save to Redis
            self.redis_client.hset(self.workflows_key, workflow_id, self._serialize_workflow(workflow))
            
            # Save to file system
            self._save_workflow_to_file(workflow)
            
            logger.info(f"Workflow created: {name} ({workflow_id})")
            return workflow_id
            
        except Exception as e:
            logger.error(f"Error creating workflow: {str(e)}")
            raise
    
    def start_workflow(self, 
                      workflow_id: str,
                      variables: Dict[str, Any] = None,
                      metadata: Dict[str, Any] = None) -> str:
        """Start a workflow instance"""
        try:
            if workflow_id not in self.workflows:
                raise ValueError(f"Workflow not found: {workflow_id}")
            
            workflow = self.workflows[workflow_id]
            
            # Create workflow instance
            instance_id = str(uuid.uuid4())
            instance = WorkflowInstance(
                id=instance_id,
                workflow_id=workflow_id,
                variables=variables or {},
                metadata=metadata or {}
            )
            
            # Initialize with workflow variables
            instance.variables.update(workflow.variables)
            
            # Store instance
            self.instances[instance_id] = instance
            self.running_workflows[instance_id] = instance
            
            # Save to Redis
            self.redis_client.hset(self.instances_key, instance_id, self._serialize_instance(instance))
            self.redis_client.hset(self.running_key, instance_id, json.dumps({
                'instance_id': instance_id,
                'workflow_id': workflow_id,
                'started_at': datetime.utcnow().isoformat()
            }))
            
            # Start execution
            self.executor.submit(self._execute_workflow, instance)
            
            logger.info(f"Workflow started: {workflow.name} ({instance_id})")
            return instance_id
            
        except Exception as e:
            logger.error(f"Error starting workflow: {str(e)}")
            raise
    
    def pause_workflow(self, instance_id: str) -> bool:
        """Pause a running workflow"""
        try:
            if instance_id not in self.running_workflows:
                return False
            
            instance = self.running_workflows.pop(instance_id)
            instance.status = WorkflowStatus.PAUSED
            instance.updated_at = datetime.utcnow()
            
            self.paused_workflows[instance_id] = instance
            
            # Update Redis
            self.redis_client.hset(self.instances_key, instance_id, self._serialize_instance(instance))
            self.redis_client.hdel(self.running_key, instance_id)
            
            logger.info(f"Workflow paused: {instance_id}")
            return True
            
        except Exception as e:
            logger.error(f"Error pausing workflow {instance_id}: {str(e)}")
            return False
    
    def resume_workflow(self, instance_id: str) -> bool:
        """Resume a paused workflow"""
        try:
            if instance_id not in self.paused_workflows:
                return False
            
            instance = self.paused_workflows.pop(instance_id)
            instance.status = WorkflowStatus.RUNNING
            instance.updated_at = datetime.utcnow()
            
            self.running_workflows[instance_id] = instance
            
            # Update Redis
            self.redis_client.hset(self.instances_key, instance_id, self._serialize_instance(instance))
            self.redis_client.hset(self.running_key, instance_id, json.dumps({
                'instance_id': instance_id,
                'workflow_id': instance.workflow_id,
                'resumed_at': datetime.utcnow().isoformat()
            }))
            
            # Resume execution
            self.executor.submit(self._execute_workflow, instance)
            
            logger.info(f"Workflow resumed: {instance_id}")
            return True
            
        except Exception as e:
            logger.error(f"Error resuming workflow {instance_id}: {str(e)}")
            return False
    
    def cancel_workflow(self, instance_id: str) -> bool:
        """Cancel a workflow"""
        try:
            if instance_id not in self.instances:
                return False
            
            instance = self.instances[instance_id]
            instance.status = WorkflowStatus.CANCELLED
            instance.updated_at = datetime.utcnow()
            
            # Remove from running/paused
            self.running_workflows.pop(instance_id, None)
            self.paused_workflows.pop(instance_id, None)
            
            # Cancel associated tasks
            self._cancel_workflow_tasks(instance_id)
            
            # Update Redis
            self.redis_client.hset(self.instances_key, instance_id, self._serialize_instance(instance))
            self.redis_client.hdel(self.running_key, instance_id)
            
            logger.info(f"Workflow cancelled: {instance_id}")
            return True
            
        except Exception as e:
            logger.error(f"Error cancelling workflow {instance_id}: {str(e)}")
            return False
    
    def get_workflow_status(self, instance_id: str) -> Optional[Dict[str, Any]]:
        """Get workflow instance status"""
        try:
            if instance_id not in self.instances:
                return None
            
            instance = self.instances[instance_id]
            workflow = self.workflows.get(instance.workflow_id)
            
            if not workflow:
                return None
            
            # Calculate progress
            total_steps = len(workflow.steps)
            completed_steps = len(instance.completed_steps)
            progress = (completed_steps / total_steps) * 100 if total_steps > 0 else 0
            
            return {
                'instance_id': instance.id,
                'workflow_id': instance.workflow_id,
                'workflow_name': workflow.name,
                'status': instance.status.value,
                'progress': progress,
                'current_step': instance.current_step,
                'completed_steps': list(instance.completed_steps),
                'failed_steps': list(instance.failed_steps),
                'total_steps': total_steps,
                'started_at': instance.started_at.isoformat() if instance.started_at else None,
                'completed_at': instance.completed_at.isoformat() if instance.completed_at else None,
                'created_at': instance.created_at.isoformat(),
                'updated_at': instance.updated_at.isoformat(),
                'variables': instance.variables,
                'metadata': instance.metadata
            }
            
        except Exception as e:
            logger.error(f"Error getting workflow status {instance_id}: {str(e)}")
            return None
    
    def get_workflow_definitions(self) -> List[Dict[str, Any]]:
        """Get all workflow definitions"""
        try:
            workflows = []
            for workflow in self.workflows.values():
                workflows.append({
                    'id': workflow.id,
                    'name': workflow.name,
                    'description': workflow.description,
                    'steps_count': len(workflow.steps),
                    'triggers_count': len(workflow.triggers),
                    'variables_count': len(workflow.variables),
                    'created_at': workflow.created_at.isoformat(),
                    'updated_at': workflow.updated_at.isoformat(),
                    'version': workflow.version
                })
            return workflows
            
        except Exception as e:
            logger.error(f"Error getting workflow definitions: {str(e)}")
            return []
    
    def get_workflow_instances(self, workflow_id: str = None) -> List[Dict[str, Any]]:
        """Get workflow instances"""
        try:
            instances = []
            for instance in self.instances.values():
                if workflow_id and instance.workflow_id != workflow_id:
                    continue
                
                workflow = self.workflows.get(instance.workflow_id)
                instances.append({
                    'id': instance.id,
                    'workflow_id': instance.workflow_id,
                    'workflow_name': workflow.name if workflow else 'Unknown',
                    'status': instance.status.value,
                    'progress': len(instance.completed_steps) / len(workflow.steps) * 100 if workflow else 0,
                    'started_at': instance.started_at.isoformat() if instance.started_at else None,
                    'completed_at': instance.completed_at.isoformat() if instance.completed_at else None,
                    'created_at': instance.created_at.isoformat()
                })
            return instances
            
        except Exception as e:
            logger.error(f"Error getting workflow instances: {str(e)}")
            return []
    
    def _execute_workflow(self, instance: WorkflowInstance):
        """Execute workflow instance"""
        try:
            workflow = self.workflows.get(instance.workflow_id)
            if not workflow:
                logger.error(f"Workflow not found: {instance.workflow_id}")
                return
            
            instance.status = WorkflowStatus.RUNNING
            instance.started_at = datetime.utcnow()
            instance.updated_at = datetime.utcnow()
            
            # Build dependency graph
            graph = self._build_dependency_graph(workflow.steps)
            
            # Execute steps in dependency order
            while instance.status == WorkflowStatus.RUNNING:
                # Find next executable steps
                ready_steps = self._get_ready_steps(workflow.steps, instance, graph)
                
                if not ready_steps:
                    # Check if workflow is complete
                    if len(instance.completed_steps) == len(workflow.steps):
                        instance.status = WorkflowStatus.COMPLETED
                        instance.completed_at = datetime.utcnow()
                    elif len(instance.failed_steps) > 0:
                        instance.status = WorkflowStatus.FAILED
                        instance.completed_at = datetime.utcnow()
                    break
                
                # Execute ready steps
                for step in ready_steps:
                    if instance.status != WorkflowStatus.RUNNING:
                        break
                    
                    success = self._execute_step(step, instance, workflow)
                    
                    if not success:
                        instance.failed_steps.add(step.id)
                        # Check if workflow should continue
                        if workflow.settings.get('fail_fast', False):
                            instance.status = WorkflowStatus.FAILED
                            break
                
                # Update instance
                instance.updated_at = datetime.utcnow()
                self.redis_client.hset(self.instances_key, instance.id, self._serialize_instance(instance))
                
                # Small delay to prevent busy waiting
                import time
                time.sleep(0.1)
            
            # Remove from running workflows
            self.running_workflows.pop(instance.id, None)
            
            # Update Redis
            self.redis_client.hset(self.instances_key, instance.id, self._serialize_instance(instance))
            self.redis_client.hdel(self.running_key, instance.id)
            
            logger.info(f"Workflow execution completed: {instance.id} ({instance.status.value})")
            
        except Exception as e:
            logger.error(f"Error executing workflow {instance.id}: {str(e)}")
            instance.status = WorkflowStatus.FAILED
            instance.completed_at = datetime.utcnow()
            instance.step_errors['execution_error'] = str(e)
    
    def _build_dependency_graph(self, steps: List[WorkflowStep]) -> nx.DiGraph:
        """Build dependency graph for workflow steps"""
        try:
            graph = nx.DiGraph()
            
            # Add nodes
            for step in steps:
                graph.add_node(step.id, step=step)
            
            # Add edges (dependencies)
            for step in steps:
                for dep_id in step.dependencies:
                    if dep_id in graph.nodes:
                        graph.add_edge(dep_id, step.id)
            
            # Check for cycles
            if not nx.is_directed_acyclic_graph(graph):
                raise ValueError("Workflow contains dependency cycles")
            
            return graph
            
        except Exception as e:
            logger.error(f"Error building dependency graph: {str(e)}")
            raise
    
    def _get_ready_steps(self, 
                        steps: List[WorkflowStep], 
                        instance: WorkflowInstance, 
                        graph: nx.DiGraph) -> List[WorkflowStep]:
        """Get steps ready for execution"""
        try:
            ready_steps = []
            
            for step in steps:
                # Skip if already completed or failed
                if step.id in instance.completed_steps or step.id in instance.failed_steps:
                    continue
                
                # Skip if currently executing
                if instance.current_step == step.id:
                    continue
                
                # Check dependencies
                dependencies_met = all(
                    dep_id in instance.completed_steps 
                    for dep_id in step.dependencies
                )
                
                if dependencies_met:
                    # Check conditions
                    if self._evaluate_conditions(step.conditions, instance):
                        ready_steps.append(step)
            
            return ready_steps
            
        except Exception as e:
            logger.error(f"Error getting ready steps: {str(e)}")
            return []
    
    def _evaluate_conditions(self, conditions: Dict[str, Any], instance: WorkflowInstance) -> bool:
        """Evaluate step conditions"""
        try:
            if not conditions:
                return True
            
            # Simple condition evaluation (can be extended)
            for condition_key, condition_value in conditions.items():
                if condition_key.startswith('variable.'):
                    var_name = condition_key[9:]  # Remove 'variable.' prefix
                    actual_value = instance.variables.get(var_name)
                    
                    if actual_value != condition_value:
                        return False
                elif condition_key.startswith('step_result.'):
                    step_id = condition_key[12:]  # Remove 'step_result.' prefix
                    actual_value = instance.step_results.get(step_id)
                    
                    if actual_value != condition_value:
                        return False
            
            return True
            
        except Exception as e:
            logger.error(f"Error evaluating conditions: {str(e)}")
            return False
    
    def _execute_step(self, step: WorkflowStep, instance: WorkflowInstance, workflow: WorkflowDefinition) -> bool:
        """Execute a single workflow step"""
        try:
            instance.current_step = step.id
            
            # Create task for step
            task_id = self._create_task_for_step(step, instance)
            
            if not task_id:
                return False
            
            # Track task
            self.workflow_tasks[instance.workflow_id][step.id] = task_id
            
            # Wait for task completion
            success = self._wait_for_task_completion(task_id, step.timeout)
            
            if success:
                instance.completed_steps.add(step.id)
                instance.current_step = None
            else:
                instance.step_errors[step.id] = "Task execution failed"
            
            return success
            
        except Exception as e:
            logger.error(f"Error executing step {step.id}: {str(e)}")
            instance.step_errors[step.id] = str(e)
            return False
    
    def _create_task_for_step(self, step: WorkflowStep, instance: WorkflowInstance) -> Optional[str]:
        """Create task for workflow step"""
        try:
            # Prepare task data
            task_data = step.task_data.copy()
            task_data.update({
                'workflow_id': instance.workflow_id,
                'instance_id': instance.id,
                'step_id': step.id,
                'variables': instance.variables
            })
            
            # Create task
            from .vuc_orchestrator import vuc_orchestrator
            task_id = vuc_orchestrator.create_task(
                name=f"{step.name} (Workflow: {instance.workflow_id})",
                task_type=step.task_type,
                data=task_data,
                priority=step.priority,
                agent_id=step.agent_type,
                timeout=step.timeout
            )
            
            return task_id
            
        except Exception as e:
            logger.error(f"Error creating task for step {step.id}: {str(e)}")
            return None
    
    def _wait_for_task_completion(self, task_id: str, timeout: int) -> bool:
        """Wait for task completion"""
        try:
            start_time = datetime.utcnow()
            
            while True:
                # Check timeout
                if (datetime.utcnow() - start_time).total_seconds() > timeout:
                    logger.warning(f"Task {task_id} timed out")
                    return False
                
                # Check task status
                from .vuc_orchestrator import vuc_orchestrator
                if task_id in vuc_orchestrator.tasks:
                    task = vuc_orchestrator.tasks[task_id]
                    if task.status == TaskStatus.COMPLETED:
                        return True
                    elif task.status == TaskStatus.FAILED:
                        return False
                
                # Sleep before next check
                import time
                time.sleep(1)
                
        except Exception as e:
            logger.error(f"Error waiting for task completion {task_id}: {str(e)}")
            return False
    
    def _cancel_workflow_tasks(self, instance_id: str):
        """Cancel all tasks for a workflow"""
        try:
            if instance_id not in self.workflow_tasks:
                return
            
            step_tasks = self.workflow_tasks[instance_id]
            
            for step_id, task_id in step_tasks.items():
                # Cancel task (implementation depends on task queue system)
                try:
                    from .vuc_orchestrator import vuc_orchestrator
                    if task_id in vuc_orchestrator.tasks:
                        task = vuc_orchestrator.tasks[task_id]
                        task.status = TaskStatus.CANCELLED
                except Exception as e:
                    logger.error(f"Error cancelling task {task_id}: {str(e)}")
            
            # Clear task tracking
            del self.workflow_tasks[instance_id]
            
        except Exception as e:
            logger.error(f"Error cancelling workflow tasks {instance_id}: {str(e)}")
    
    def _validate_workflow(self, workflow: WorkflowDefinition) -> bool:
        """Validate workflow definition"""
        try:
            # Check for required fields
            if not workflow.name or not workflow.steps:
                return False
            
            # Check step IDs are unique
            step_ids = [step.id for step in workflow.steps]
            if len(step_ids) != len(set(step_ids)):
                return False
            
            # Check dependencies exist
            all_step_ids = set(step_ids)
            for step in workflow.steps:
                for dep_id in step.dependencies:
                    if dep_id not in all_step_ids:
                        return False
            
            return True
            
        except Exception as e:
            logger.error(f"Error validating workflow: {str(e)}")
            return False
    
    def _serialize_workflow(self, workflow: WorkflowDefinition) -> str:
        """Serialize workflow for storage"""
        return json.dumps({
            'id': workflow.id,
            'name': workflow.name,
            'description': workflow.description,
            'steps': [
                {
                    'id': step.id,
                    'name': step.name,
                    'task_type': step.task_type,
                    'execution_mode': step.execution_mode.value,
                    'dependencies': step.dependencies,
                    'conditions': step.conditions,
                    'task_data': step.task_data,
                    'agent_type': step.agent_type,
                    'priority': step.priority.value,
                    'timeout': step.timeout,
                    'max_retries': step.max_retries,
                    'metadata': step.metadata
                }
                for step in workflow.steps
            ],
            'triggers': workflow.triggers,
            'variables': workflow.variables,
            'settings': workflow.settings,
            'created_at': workflow.created_at.isoformat(),
            'updated_at': workflow.updated_at.isoformat(),
            'version': workflow.version
        })
    
    def _deserialize_workflow(self, data: Dict[str, Any]) -> WorkflowDefinition:
        """Deserialize workflow from storage"""
        steps = []
        for step_data in data['steps']:
            step = WorkflowStep(
                id=step_data['id'],
                name=step_data['name'],
                task_type=step_data['task_type'],
                execution_mode=TaskExecutionMode(step_data['execution_mode']),
                dependencies=step_data['dependencies'],
                conditions=step_data['conditions'],
                task_data=step_data['task_data'],
                agent_type=step_data.get('agent_type'),
                priority=TaskPriority(step_data['priority']),
                timeout=step_data['timeout'],
                max_retries=step_data['max_retries'],
                metadata=step_data['metadata']
            )
            steps.append(step)
        
        return WorkflowDefinition(
            id=data['id'],
            name=data['name'],
            description=data['description'],
            steps=steps,
            triggers=data['triggers'],
            variables=data['variables'],
            settings=data['settings'],
            created_at=datetime.fromisoformat(data['created_at']),
            updated_at=datetime.fromisoformat(data['updated_at']),
            version=data['version']
        )
    
    def _serialize_instance(self, instance: WorkflowInstance) -> str:
        """Serialize instance for storage"""
        return json.dumps({
            'id': instance.id,
            'workflow_id': instance.workflow_id,
            'status': instance.status.value,
            'started_at': instance.started_at.isoformat() if instance.started_at else None,
            'completed_at': instance.completed_at.isoformat() if instance.completed_at else None,
            'current_step': instance.current_step,
            'completed_steps': list(instance.completed_steps),
            'failed_steps': list(instance.failed_steps),
            'step_results': instance.step_results,
            'step_errors': instance.step_errors,
            'variables': instance.variables,
            'metadata': instance.metadata,
            'created_at': instance.created_at.isoformat(),
            'updated_at': instance.updated_at.isoformat()
        })
    
    def _deserialize_instance(self, data: Dict[str, Any]) -> WorkflowInstance:
        """Deserialize instance from storage"""
        return WorkflowInstance(
            id=data['id'],
            workflow_id=data['workflow_id'],
            status=WorkflowStatus(data['status']),
            started_at=datetime.fromisoformat(data['started_at']) if data['started_at'] else None,
            completed_at=datetime.fromisoformat(data['completed_at']) if data['completed_at'] else None,
            current_step=data['current_step'],
            completed_steps=set(data['completed_steps']),
            failed_steps=set(data['failed_steps']),
            step_results=data['step_results'],
            step_errors=data['step_errors'],
            variables=data['variables'],
            metadata=data['metadata'],
            created_at=datetime.fromisoformat(data['created_at']),
            updated_at=datetime.fromisoformat(data['updated_at'])
        )
    
    def _save_workflow_to_file(self, workflow: WorkflowDefinition):
        """Save workflow to file system"""
        try:
            workflow_dir = "vuc_memory/workflows"
            os.makedirs(workflow_dir, exist_ok=True)
            
            filename = f"{workflow.id}.json"
            filepath = os.path.join(workflow_dir, filename)
            
            with open(filepath, 'w') as f:
                json.dump(json.loads(self._serialize_workflow(workflow)), f, indent=2)
            
        except Exception as e:
            logger.error(f"Error saving workflow to file: {str(e)}")
    
    def _workflow_monitor_worker(self):
        """Background workflow monitor worker"""
        while True:
            try:
                # Check for stuck workflows
                self._check_stuck_workflows()
                
                # Update workflow metrics
                self._update_workflow_metrics()
                
                # Process workflow triggers
                self._process_workflow_triggers()
                
                # Clean up old instances
                self._cleanup_old_instances()
                
                import time
                time.sleep(60)  # Check every minute
                
            except Exception as e:
                logger.error(f"Error in workflow monitor: {str(e)}")
                import time
                time.sleep(120)
    
    def _check_stuck_workflows(self):
        """Check for stuck workflows"""
        try:
            current_time = datetime.utcnow()
            timeout_threshold = timedelta(hours=1)  # 1 hour timeout
            
            for instance_id, instance in list(self.running_workflows.items()):
                if instance.started_at and (current_time - instance.started_at) > timeout_threshold:
                    logger.warning(f"Workflow {instance_id} appears to be stuck")
                    
                    # Option 1: Pause the workflow
                    # self.pause_workflow(instance_id)
                    
                    # Option 2: Mark as failed
                    instance.status = WorkflowStatus.FAILED
                    instance.step_errors['timeout'] = "Workflow execution timeout"
                    
                    self.running_workflows.pop(instance_id, None)
                    self.redis_client.hset(self.instances_key, instance_id, self._serialize_instance(instance))
                    self.redis_client.hdel(self.running_key, instance_id)
                    
        except Exception as e:
            logger.error(f"Error checking stuck workflows: {str(e)}")
    
    def _update_workflow_metrics(self):
        """Update workflow metrics"""
        try:
            metrics = {
                'total_workflows': len(self.workflows),
                'total_instances': len(self.instances),
                'running_instances': len(self.running_workflows),
                'paused_instances': len(self.paused_workflows),
                'completed_instances': len([i for i in self.instances.values() if i.status == WorkflowStatus.COMPLETED]),
                'failed_instances': len([i for i in self.instances.values() if i.status == WorkflowStatus.FAILED]),
                'timestamp': datetime.utcnow().isoformat()
            }
            
            self.redis_client.hset("workflow_engine:metrics", "metrics", json.dumps(metrics))
            
        except Exception as e:
            logger.error(f"Error updating workflow metrics: {str(e)}")
    
    def _process_workflow_triggers(self):
        """Process workflow triggers"""
        try:
            for workflow in self.workflows.values():
                for trigger in workflow.triggers:
                    if self._evaluate_trigger(trigger, workflow):
                        # Start workflow instance
                        self.start_workflow(
                            workflow.id,
                            variables=trigger.get('variables', {}),
                            metadata={'trigger_type': trigger.get('type', 'manual')}
                        )
                        
        except Exception as e:
            logger.error(f"Error processing workflow triggers: {str(e)}")
    
    def _evaluate_trigger(self, trigger: Dict[str, Any], workflow: WorkflowDefinition) -> bool:
        """Evaluate workflow trigger"""
        try:
            trigger_type = trigger.get('type', 'manual')
            
            if trigger_type == 'manual':
                return False  # Manual triggers are handled separately
            elif trigger_type == 'schedule':
                # Check if scheduled time has arrived
                schedule_time = trigger.get('schedule_time')
                if schedule_time:
                    scheduled = datetime.fromisoformat(schedule_time)
                    return datetime.utcnow() >= scheduled
            elif trigger_type == 'event':
                # Check if event has occurred
                # This would integrate with an event system
                return False
            
            return False
            
        except Exception as e:
            logger.error(f"Error evaluating trigger: {str(e)}")
            return False
    
    def _cleanup_old_instances(self):
        """Clean up old workflow instances"""
        try:
            cutoff_time = datetime.utcnow() - timedelta(days=7)
            
            old_instances = [
                instance_id for instance_id, instance in self.instances.items()
                if instance.created_at < cutoff_time and instance.status in [WorkflowStatus.COMPLETED, WorkflowStatus.FAILED, WorkflowStatus.CANCELLED]
            ]
            
            for instance_id in old_instances:
                # Remove from storage
                self.instances.pop(instance_id, None)
                self.redis_client.hdel(self.instances_key, instance_id)
                
                # Clean up task tracking
                self.workflow_tasks.pop(instance_id, None)
            
            if old_instances:
                logger.info(f"Cleaned up {len(old_instances)} old workflow instances")
                
        except Exception as e:
            logger.error(f"Error cleaning up old instances: {str(e)}")

# Global workflow engine instance
workflow_engine = WorkflowEngine()
