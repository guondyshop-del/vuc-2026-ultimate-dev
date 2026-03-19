"""
Self-Correcting Scripts with Health Check Layers
FFmpeg, ExifTool, and Scraping with automatic error recovery
"""

import asyncio
import subprocess
import logging
import json
import time
from typing import Dict, Any, Optional, List, Callable
from dataclasses import dataclass
from pathlib import Path
from datetime import datetime
from google.generativeai import GenerativeModel
import google.generativeai as genai

logger = logging.getLogger(__name__)

@dataclass
class ScriptExecution:
    """Script execution context"""
    script_name: str
    command: List[str]
    parameters: Dict[str, Any]
    health_checks: List[str]
    retry_count: int = 0
    max_retries: int = 3
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    success: bool = False
    error_message: Optional[str] = None
    ai_fix_applied: bool = False

class HealthCheckLayer:
    """Health check layer for script validation"""
    
    def __init__(self):
        self.health_checks = {
            "ffmpeg": self._check_ffmpeg_health,
            "exiftool": self._check_exiftool_health,
            "scraping": self._check_scraping_health,
            "network": self._check_network_health,
            "disk_space": self._check_disk_space,
            "memory": self._check_memory_health
        }
    
    async def run_health_checks(self, execution: ScriptExecution) -> Dict[str, Any]:
        """Run relevant health checks for script execution"""
        results = {}
        
        for check_name in execution.health_checks:
            if check_name in self.health_checks:
                try:
                    result = await self.health_checks[check_name](execution)
                    results[check_name] = result
                except Exception as e:
                    logger.error(f"Health check {check_name} failed: {str(e)}")
                    results[check_name] = {"status": "error", "message": str(e)}
        
        return results
    
    async def _check_ffmpeg_health(self, execution: ScriptExecution) -> Dict[str, Any]:
        """Check FFmpeg health and availability"""
        try:
            # Test FFmpeg installation
            result = await asyncio.create_subprocess_exec(
                "ffmpeg", "-version",
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            stdout, stderr = await result.communicate()
            
            if result.returncode == 0:
                version_info = stdout.decode().split('\n')[0]
                return {
                    "status": "healthy",
                    "version": version_info,
                    "message": "FFmpeg is available and functional"
                }
            else:
                return {
                    "status": "error",
                    "message": "FFmpeg not found or not working",
                    "error": stderr.decode()
                }
        except Exception as e:
            return {
                "status": "error",
                "message": f"FFmpeg health check failed: {str(e)}"
            }
    
    async def _check_exiftool_health(self, execution: ScriptExecution) -> Dict[str, Any]:
        """Check ExifTool health and availability"""
        try:
            # Test ExifTool installation
            result = await asyncio.create_subprocess_exec(
                "exiftool", "-ver",
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            stdout, stderr = await result.communicate()
            
            if result.returncode == 0:
                version = stdout.decode().strip()
                return {
                    "status": "healthy",
                    "version": version,
                    "message": "ExifTool is available and functional"
                }
            else:
                return {
                    "status": "error",
                    "message": "ExifTool not found or not working",
                    "error": stderr.decode()
                }
        except Exception as e:
            return {
                "status": "error",
                "message": f"ExifTool health check failed: {str(e)}"
            }
    
    async def _check_scraping_health(self, execution: ScriptExecution) -> Dict[str, Any]:
        """Check scraping dependencies health"""
        try:
            import requests
            import beautifulsoup4
            import selenium
            
            # Test network connectivity
            response = requests.get("https://www.google.com", timeout=5)
            
            if response.status_code == 200:
                return {
                    "status": "healthy",
                    "message": "Scraping dependencies are available",
                    "network_status": "connected",
                    "libraries": ["requests", "beautifulsoup4", "selenium"]
                }
            else:
                return {
                    "status": "warning",
                    "message": "Network connectivity issues detected",
                    "status_code": response.status_code
                }
        except Exception as e:
            return {
                "status": "error",
                "message": f"Scraping health check failed: {str(e)}"
            }
    
    async def _check_network_health(self, execution: ScriptExecution) -> Dict[str, Any]:
        """Check network connectivity"""
        try:
            import requests
            
            # Test multiple endpoints
            endpoints = [
                "https://www.google.com",
                "https://www.youtube.com",
                "https://api.github.com"
            ]
            
            results = {}
            for endpoint in endpoints:
                try:
                    response = requests.get(endpoint, timeout=3)
                    results[endpoint] = {
                        "status_code": response.status_code,
                        "response_time": response.elapsed.total_seconds()
                    }
                except Exception as e:
                    results[endpoint] = {"error": str(e)}
            
            # Overall network health
            healthy_endpoints = sum(1 for r in results.values() if "status_code" in r and r["status_code"] == 200)
            
            return {
                "status": "healthy" if healthy_endpoints >= 2 else "warning",
                "endpoints_tested": len(endpoints),
                "healthy_endpoints": healthy_endpoints,
                "details": results
            }
        except Exception as e:
            return {
                "status": "error",
                "message": f"Network health check failed: {str(e)}"
            }
    
    async def _check_disk_space(self, execution: ScriptExecution) -> Dict[str, Any]:
        """Check available disk space"""
        try:
            import shutil
            
            total, used, free = shutil.disk_usage("/")
            free_gb = free // (1024**3)
            
            if free_gb < 1:  # Less than 1GB
                return {
                    "status": "critical",
                    "message": f"Very low disk space: {free_gb}GB available",
                    "free_gb": free_gb,
                    "total_gb": total // (1024**3)
                }
            elif free_gb < 5:  # Less than 5GB
                return {
                    "status": "warning",
                    "message": f"Low disk space: {free_gb}GB available",
                    "free_gb": free_gb,
                    "total_gb": total // (1024**3)
                }
            else:
                return {
                    "status": "healthy",
                    "message": f"Sufficient disk space: {free_gb}GB available",
                    "free_gb": free_gb,
                    "total_gb": total // (1024**3)
                }
        except Exception as e:
            return {
                "status": "error",
                "message": f"Disk space check failed: {str(e)}"
            }
    
    async def _check_memory_health(self, execution: ScriptExecution) -> Dict[str, Any]:
        """Check available memory"""
        try:
            import psutil
            
            memory = psutil.virtual_memory()
            available_gb = memory.available // (1024**3)
            
            if memory.percent > 90:
                return {
                    "status": "critical",
                    "message": f"Very high memory usage: {memory.percent:.1f}%",
                    "available_gb": available_gb,
                    "usage_percent": memory.percent
                }
            elif memory.percent > 80:
                return {
                    "status": "warning",
                    "message": f"High memory usage: {memory.percent:.1f}%",
                    "available_gb": available_gb,
                    "usage_percent": memory.percent
                }
            else:
                return {
                    "status": "healthy",
                    "message": f"Normal memory usage: {memory.percent:.1f}%",
                    "available_gb": available_gb,
                    "usage_percent": memory.percent
                }
        except Exception as e:
            return {
                "status": "error",
                "message": f"Memory check failed: {str(e)}"
            }

class AIScriptDoctor:
    """AI-powered script error diagnosis and fixing"""
    
    def __init__(self, api_key: str):
        genai.configure(api_key=api_key)
        self.model = GenerativeModel('gemini-2.0-pro')
        self.fix_history: List[Dict] = []
    
    async def diagnose_and_fix(self, execution: ScriptExecution, error_output: str) -> Dict[str, Any]:
        """Diagnose error and provide AI-powered fix"""
        try:
            # Build diagnosis prompt
            prompt = self._build_diagnosis_prompt(execution, error_output)
            
            # Get AI diagnosis
            response = await asyncio.to_thread(self.model.generate_content, prompt)
            ai_text = response.text
            
            # Parse AI response
            diagnosis = self._parse_diagnosis_response(ai_text)
            
            # Apply fix if recommended
            if diagnosis.get("fix_available", False):
                fixed_execution = await self._apply_ai_fix(execution, diagnosis)
                return {
                    "diagnosis": diagnosis,
                    "fixed_execution": fixed_execution,
                    "ai_fix_applied": True
                }
            else:
                return {
                    "diagnosis": diagnosis,
                    "ai_fix_applied": False
                }
                
        except Exception as e:
            logger.error(f"AI diagnosis failed: {str(e)}")
            return {
                "diagnosis": {"error": str(e)},
                "ai_fix_applied": False
            }
    
    def _build_diagnosis_prompt(self, execution: ScriptExecution, error_output: str) -> str:
        """Build AI prompt for error diagnosis"""
        prompt = f"""
You are an expert system administrator and script doctor. Analyze this script execution error and provide a fix.

SCRIPT EXECUTION DETAILS:
- Script Name: {execution.script_name}
- Command: {' '.join(execution.command)}
- Parameters: {json.dumps(execution.parameters, indent=2)}
- Retry Count: {execution.retry_count}/{execution.max_retries}
- Error Output: {error_output}

TASKS:
1. Identify the root cause of the error
2. Determine if this is a configuration, dependency, or environmental issue
3. Provide specific fix recommendations
4. Suggest parameter modifications if needed
5. Recommend alternative approaches if the current method is failing

RESPONSE FORMAT (JSON):
{{
    "root_cause": "specific description of the root cause",
    "error_type": "configuration|dependency|environmental|permission|network",
    "fix_available": true/false,
    "recommended_fix": "detailed steps to fix the issue",
    "parameter_modifications": {{
        "param_name": "new_value"
    }},
    "alternative_approach": "alternative method if available",
    "confidence": 0.85,
    "prevention_tips": ["tips to prevent this error in the future"]
}}

Focus on practical, actionable solutions that can be applied automatically.
"""
        return prompt
    
    def _parse_diagnosis_response(self, ai_text: str) -> Dict[str, Any]:
        """Parse AI diagnosis response"""
        try:
            # Extract JSON from response
            start_idx = ai_text.find('{')
            end_idx = ai_text.rfind('}') + 1
            
            if start_idx != -1 and end_idx != -1:
                json_str = ai_text[start_idx:end_idx]
                return json.loads(json_str)
            else:
                return {
                    "root_cause": "Unable to parse AI response",
                    "fix_available": False,
                    "confidence": 0.3
                }
        except Exception as e:
            logger.error(f"Failed to parse AI diagnosis: {str(e)}")
            return {
                "root_cause": f"Parse error: {str(e)}",
                "fix_available": False,
                "confidence": 0.2
            }
    
    async def _apply_ai_fix(self, execution: ScriptExecution, diagnosis: Dict[str, Any]) -> ScriptExecution:
        """Apply AI-recommended fix to execution"""
        fixed_execution = ScriptExecution(
            script_name=execution.script_name,
            command=execution.command.copy(),
            parameters=execution.parameters.copy(),
            health_checks=execution.health_checks.copy(),
            retry_count=execution.retry_count + 1,
            max_retries=execution.max_retries
        )
        
        # Apply parameter modifications
        param_mods = diagnosis.get("parameter_modifications", {})
        for param, value in param_mods.items():
            if param in fixed_execution.parameters:
                try:
                    # Type conversion
                    if isinstance(fixed_execution.parameters[param], int):
                        fixed_execution.parameters[param] = int(value)
                    elif isinstance(fixed_execution.parameters[param], float):
                        fixed_execution.parameters[param] = float(value)
                    elif isinstance(fixed_execution.parameters[param], bool):
                        fixed_execution.parameters[param] = bool(value)
                    else:
                        fixed_execution.parameters[param] = str(value)
                except (ValueError, TypeError):
                    logger.warning(f"Failed to apply parameter fix for {param}")
        
        # Apply command modifications if needed
        if diagnosis.get("error_type") == "dependency":
            # Try alternative command or add flags
            if "ffmpeg" in execution.script_name.lower():
                # Add error resilience flags
                if "-y" not in fixed_execution.command:
                    fixed_execution.command.insert(1, "-y")
                if "-nostats" not in fixed_execution.command:
                    fixed_execution.command.insert(-1, "-nostats")
        
        fixed_execution.ai_fix_applied = True
        
        # Store fix in history
        self._store_fix_history(execution, diagnosis, fixed_execution)
        
        return fixed_execution
    
    def _store_fix_history(self, original: ScriptExecution, diagnosis: Dict, fixed: ScriptExecution):
        """Store fix history for learning"""
        fix_record = {
            "timestamp": datetime.now().isoformat(),
            "script_name": original.script_name,
            "error_type": diagnosis.get("error_type"),
            "root_cause": diagnosis.get("root_cause"),
            "fix_applied": diagnosis.get("recommended_fix"),
            "confidence": diagnosis.get("confidence"),
            "success": fixed.success if fixed.end_time else "pending"
        }
        
        self.fix_history.append(fix_record)
        
        # Keep only last 100 fixes
        if len(self.fix_history) > 100:
            self.fix_history = self.fix_history[-100:]

class SelfCorrectingScriptExecutor:
    """Main executor for self-correcting scripts"""
    
    def __init__(self, gemini_api_key: str):
        self.health_layer = HealthCheckLayer()
        self.ai_doctor = AIScriptDoctor(gemini_api_key)
        self.execution_history: List[ScriptExecution] = []
    
    async def execute_script(self, script_name: str, command: List[str], 
                           parameters: Dict[str, Any], 
                           health_checks: List[str] = None) -> ScriptExecution:
        """Execute script with self-correction capabilities"""
        
        if health_checks is None:
            health_checks = ["network", "disk_space", "memory"]
        
        execution = ScriptExecution(
            script_name=script_name,
            command=command,
            parameters=parameters,
            health_checks=health_checks
        )
        
        execution.start_time = datetime.now()
        
        try:
            # Run health checks first
            health_results = await self.health_layer.run_health_checks(execution)
            
            # Check for critical health issues
            critical_issues = [name for name, result in health_results.items() 
                             if result.get("status") == "critical"]
            
            if critical_issues:
                raise Exception(f"Critical health issues detected: {', '.join(critical_issues)}")
            
            # Execute the script
            result = await self._run_command(execution.command)
            
            if result.returncode == 0:
                execution.success = True
                logger.info(f"Script {script_name} executed successfully")
            else:
                error_output = result.stderr.decode() if result.stderr else "Unknown error"
                execution.error_message = error_output
                
                # Try self-correction
                if execution.retry_count < execution.max_retries:
                    logger.warning(f"Script {script_name} failed, attempting self-correction")
                    
                    # Get AI diagnosis and fix
                    fix_result = await self.ai_doctor.diagnose_and_fix(execution, error_output)
                    
                    if fix_result.get("ai_fix_applied", False):
                        fixed_execution = fix_result["fixed_execution"]
                        
                        # Retry with fixed execution
                        return await self.execute_script(
                            fixed_execution.script_name,
                            fixed_execution.command,
                            fixed_execution.parameters,
                            fixed_execution.health_checks
                        )
                    else:
                        logger.error(f"AI could not fix script {script_name}")
                else:
                    logger.error(f"Script {script_name} failed after {execution.max_retries} retries")
        
        except Exception as e:
            execution.error_message = str(e)
            execution.success = False
            logger.error(f"Script {script_name} execution failed: {str(e)}")
        
        finally:
            execution.end_time = datetime.now()
            self.execution_history.append(execution)
        
        return execution
    
    async def _run_command(self, command: List[str]) -> asyncio.subprocess.Process:
        """Run command with asyncio"""
        process = await asyncio.create_subprocess_exec(
            *command,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        
        stdout, stderr = await process.communicate()
        
        return process
    
    def get_execution_stats(self) -> Dict[str, Any]:
        """Get execution statistics"""
        if not self.execution_history:
            return {"total_executions": 0}
        
        total = len(self.execution_history)
        successful = sum(1 for e in self.execution_history if e.success)
        ai_fixed = sum(1 for e in self.execution_history if e.ai_fix_applied)
        
        return {
            "total_executions": total,
            "successful_executions": successful,
            "success_rate": successful / total * 100,
            "ai_fixes_applied": ai_fixed,
            "ai_fix_success_rate": ai_fixed / total * 100,
            "last_updated": datetime.now().isoformat()
        }

# Global executor instance
script_executor: Optional[SelfCorrectingScriptExecutor] = None

def get_script_executor() -> SelfCorrectingScriptExecutor:
    """Get or initialize script executor"""
    global script_executor
    if script_executor is None:
        api_key = "YOUR_GEMINI_API_KEY"  # Should come from environment
        script_executor = SelfCorrectingScriptExecutor(api_key)
    return script_executor
