"""
AI Orchestrator - LLM-Router for Dynamic AI-Endpoints
Gemini 2.0 Pro powered intelligent request routing and parameter optimization
"""

import asyncio
import json
import logging
from typing import Dict, Any, Optional, List
from dataclasses import dataclass
from fastapi import Request, HTTPException
from google.generativeai import GenerativeModel
import google.generativeai as genai
from datetime import datetime

logger = logging.getLogger(__name__)

@dataclass
class OrchestratedRequest:
    """AI-orchestrated request structure"""
    original_path: str
    method: str
    parameters: Dict[str, Any]
    optimized_parameters: Dict[str, Any]
    confidence_score: float
    processing_strategy: str
    estimated_success_rate: float
    ai_recommendations: List[str]

class AIOrchestrator:
    """AI-powered request orchestrator using Gemini 2.0 Pro"""
    
    def __init__(self, api_key: str):
        genai.configure(api_key=api_key)
        self.model = GenerativeModel('gemini-2.0-pro')
        self.request_history: List[Dict] = []
        self.success_patterns: Dict[str, Any] = {}
        
    async def orchestrate_request(self, request: Request, path: str, method: str, body: Dict[str, Any]) -> OrchestratedRequest:
        """Orchestrate and optimize incoming request using AI"""
        try:
            # Analyze request context
            request_context = await self._analyze_request_context(request, path, method, body)
            
            # Generate AI recommendations
            ai_analysis = await self._get_ai_recommendations(request_context)
            
            # Optimize parameters based on AI analysis
            optimized_params = await self._optimize_parameters(body, ai_analysis)
            
            # Determine processing strategy
            strategy = await self._determine_strategy(path, ai_analysis)
            
            # Calculate confidence and success rate
            confidence = self._calculate_confidence(ai_analysis, optimized_params)
            success_rate = self._estimate_success_rate(strategy, optimized_params)
            
            orchestrated_request = OrchestratedRequest(
                original_path=path,
                method=method,
                parameters=body,
                optimized_parameters=optimized_params,
                confidence_score=confidence,
                processing_strategy=strategy,
                estimated_success_rate=success_rate,
                ai_recommendations=ai_analysis.get("recommendations", [])
            )
            
            # Store for learning
            self._store_request_pattern(orchestrated_request)
            
            return orchestrated_request
            
        except Exception as e:
            logger.error(f"AI orchestration failed: {str(e)}")
            # Fallback to original request
            return OrchestratedRequest(
                original_path=path,
                method=method,
                parameters=body,
                optimized_parameters=body,
                confidence_score=0.5,
                processing_strategy="fallback",
                estimated_success_rate=0.7,
                ai_recommendations=["AI orchestration failed, using fallback"]
            )
    
    async def _analyze_request_context(self, request: Request, path: str, method: str, body: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze request context for AI processing"""
        context = {
            "path": path,
            "method": method,
            "body": body,
            "headers": dict(request.headers),
            "client_ip": request.client.host if request.client else "unknown",
            "timestamp": datetime.now().isoformat(),
            "user_agent": request.headers.get("user-agent", ""),
            "request_type": self._classify_request_type(path),
            "complexity": self._assess_complexity(body),
            "historical_patterns": self._get_historical_patterns(path)
        }
        return context
    
    def _classify_request_type(self, path: str) -> str:
        """Classify request type for AI analysis"""
        if "/production" in path:
            return "video_production"
        elif "/stealth" in path:
            return "stealth_operation"
        elif "/espionage" in path:
            return "competitive_analysis"
        elif "/self-healing" in path:
            return "system_maintenance"
        elif "/analytics" in path:
            return "data_analysis"
        else:
            return "general_api"
    
    def _assess_complexity(self, body: Dict[str, Any]) -> str:
        """Assess request complexity"""
        complexity_score = 0
        
        # Count parameters
        complexity_score += len(body) * 0.1
        
        # Check for nested objects
        for value in body.values():
            if isinstance(value, dict):
                complexity_score += len(value) * 0.2
            elif isinstance(value, list):
                complexity_score += len(value) * 0.15
        
        if complexity_score < 1:
            return "low"
        elif complexity_score < 3:
            return "medium"
        else:
            return "high"
    
    def _get_historical_patterns(self, path: str) -> Dict[str, Any]:
        """Get historical success patterns for this endpoint"""
        recent_requests = [r for r in self.request_history[-100:] if r.get("path") == path]
        
        if not recent_requests:
            return {"pattern_found": False}
        
        success_rate = sum(1 for r in recent_requests if r.get("success", False)) / len(recent_requests)
        avg_confidence = sum(r.get("confidence", 0) for r in recent_requests) / len(recent_requests)
        
        return {
            "pattern_found": True,
            "success_rate": success_rate,
            "avg_confidence": avg_confidence,
            "total_requests": len(recent_requests),
            "common_params": self._extract_common_parameters(recent_requests)
        }
    
    def _extract_common_parameters(self, requests: List[Dict]) -> Dict[str, Any]:
        """Extract commonly used parameters from historical requests"""
        param_frequency = {}
        
        for req in requests:
            params = req.get("parameters", {})
            for param, value in params.items():
                if param not in param_frequency:
                    param_frequency[param] = {}
                if isinstance(value, (str, int, float, bool)):
                    param_frequency[param][str(value)] = param_frequency[param].get(str(value), 0) + 1
        
        # Find most common values for each parameter
        common_params = {}
        for param, values in param_frequency.items():
            if values:
                most_common = max(values.items(), key=lambda x: x[1])
                if most_common[1] > len(requests) * 0.5:  # Appears in >50% of requests
                    common_params[param] = most_common[0]
        
        return common_params
    
    async def _get_ai_recommendations(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Get AI recommendations using Gemini 2.0 Pro"""
        try:
            prompt = self._build_ai_prompt(context)
            response = await asyncio.to_thread(self.model.generate_content, prompt)
            
            # Parse AI response
            ai_text = response.text
            recommendations = self._parse_ai_response(ai_text)
            
            return recommendations
            
        except Exception as e:
            logger.error(f"AI recommendation failed: {str(e)}")
            return {
                "recommendations": ["Use default parameters"],
                "confidence": 0.5,
                "strategy": "conservative"
            }
    
    def _build_ai_prompt(self, context: Dict[str, Any]) -> str:
        """Build AI prompt for request analysis"""
        prompt = f"""
You are an AI orchestrator for a media empire automation system. Analyze this request and provide optimal recommendations.

REQUEST CONTEXT:
- Path: {context['path']}
- Method: {context['method']}
- Request Type: {context['request_type']}
- Complexity: {context['complexity']}
- Parameters: {json.dumps(context['body'], indent=2)}
- Historical Patterns: {json.dumps(context['historical_patterns'], indent=2)}

TASKS:
1. Analyze the request for optimal parameter values
2. Identify potential issues or improvements
3. Recommend processing strategy
4. Estimate success probability
5. Provide specific parameter optimizations

RESPONSE FORMAT (JSON):
{{
    "recommendations": ["list of specific recommendations"],
    "parameter_optimizations": {{
        "param_name": "optimized_value"
    }},
    "strategy": "aggressive|balanced|conservative",
    "confidence": 0.85,
    "risk_factors": ["list of potential risks"],
    "success_factors": ["list of success factors"]
}}

Focus on: reliability, performance, and success rate optimization.
"""
        return prompt
    
    def _parse_ai_response(self, ai_text: str) -> Dict[str, Any]:
        """Parse AI response into structured format"""
        try:
            # Try to extract JSON from response
            start_idx = ai_text.find('{')
            end_idx = ai_text.rfind('}') + 1
            
            if start_idx != -1 and end_idx != -1:
                json_str = ai_text[start_idx:end_idx]
                return json.loads(json_str)
            else:
                # Fallback parsing
                return {
                    "recommendations": ["Default processing"],
                    "strategy": "balanced",
                    "confidence": 0.7
                }
        except Exception as e:
            logger.error(f"Failed to parse AI response: {str(e)}")
            return {
                "recommendations": ["Use fallback processing"],
                "strategy": "conservative",
                "confidence": 0.5
            }
    
    async def _optimize_parameters(self, original_params: Dict[str, Any], ai_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Optimize parameters based on AI recommendations"""
        optimized = original_params.copy()
        
        # Apply AI parameter optimizations
        param_optimizations = ai_analysis.get("parameter_optimizations", {})
        for param, value in param_optimizations.items():
            if param in optimized:
                try:
                    # Type conversion based on original parameter type
                    if isinstance(optimized[param], int):
                        optimized[param] = int(value)
                    elif isinstance(optimized[param], float):
                        optimized[param] = float(value)
                    elif isinstance(optimized[param], bool):
                        optimized[param] = bool(value)
                    else:
                        optimized[param] = str(value)
                except (ValueError, TypeError):
                    # Keep original if conversion fails
                    pass
        
        # Apply common historical parameters
        historical_params = self._get_historical_patterns("/production").get("common_params", {})
        for param, value in historical_params.items():
            if param not in optimized:
                # Add common parameter if not present
                optimized[param] = value
        
        return optimized
    
    async def _determine_strategy(self, path: str, ai_analysis: Dict[str, Any]) -> str:
        """Determine processing strategy based on AI analysis"""
        ai_strategy = ai_analysis.get("strategy", "balanced")
        
        # Adjust strategy based on request type
        if "stealth" in path:
            return "stealth_optimized"
        elif "production" in path:
            return "production_optimized"
        elif "espionage" in path:
            return "espionage_optimized"
        
        return ai_strategy
    
    def _calculate_confidence(self, ai_analysis: Dict[str, Any], optimized_params: Dict[str, Any]) -> float:
        """Calculate confidence score for the orchestrated request"""
        base_confidence = ai_analysis.get("confidence", 0.7)
        
        # Adjust based on parameter optimization quality
        param_quality = len(optimized_params) / 10  # Normalize to 0-1
        param_quality = min(1.0, param_quality)
        
        # Combine factors
        confidence = (base_confidence * 0.7) + (param_quality * 0.3)
        
        return min(1.0, confidence)
    
    def _estimate_success_rate(self, strategy: str, optimized_params: Dict[str, Any]) -> float:
        """Estimate success rate based on strategy and parameters"""
        base_rate = 0.8  # Base success rate
        
        # Adjust based on strategy
        strategy_multipliers = {
            "aggressive": 0.9,
            "balanced": 0.85,
            "conservative": 0.95,
            "stealth_optimized": 0.88,
            "production_optimized": 0.92,
            "espionage_optimized": 0.86
        }
        
        multiplier = strategy_multipliers.get(strategy, 0.85)
        
        # Adjust based on parameter completeness
        param_completeness = len(optimized_params) / 15  # Assuming 15 is optimal
        param_completeness = min(1.0, param_completeness)
        
        success_rate = base_rate * multiplier * (0.7 + param_completeness * 0.3)
        
        return min(1.0, success_rate)
    
    def _store_request_pattern(self, orchestrated_request: OrchestratedRequest):
        """Store request pattern for learning"""
        pattern = {
            "path": orchestrated_request.original_path,
            "method": orchestrated_request.method,
            "parameters": orchestrated_request.parameters,
            "optimized_parameters": orchestrated_request.optimized_parameters,
            "confidence": orchestrated_request.confidence_score,
            "strategy": orchestrated_request.processing_strategy,
            "timestamp": datetime.now().isoformat()
        }
        
        self.request_history.append(pattern)
        
        # Keep only last 1000 requests
        if len(self.request_history) > 1000:
            self.request_history = self.request_history[-1000:]
    
    def get_orchestration_stats(self) -> Dict[str, Any]:
        """Get orchestration statistics"""
        if not self.request_history:
            return {"total_requests": 0}
        
        total_requests = len(self.request_history)
        avg_confidence = sum(r.get("confidence", 0) for r in self.request_history) / total_requests
        
        strategy_counts = {}
        for req in self.request_history:
            strategy = req.get("strategy", "unknown")
            strategy_counts[strategy] = strategy_counts.get(strategy, 0) + 1
        
        return {
            "total_requests": total_requests,
            "avg_confidence": avg_confidence,
            "strategy_distribution": strategy_counts,
            "last_updated": datetime.now().isoformat()
        }

# Global AI Orchestrator instance
ai_orchestrator: Optional[AIOrchestrator] = None

def get_ai_orchestrator() -> AIOrchestrator:
    """Get or initialize AI orchestrator"""
    global ai_orchestrator
    if ai_orchestrator is None:
        api_key = "YOUR_GEMINI_API_KEY"  # Should come from environment
        ai_orchestrator = AIOrchestrator(api_key)
    return ai_orchestrator
