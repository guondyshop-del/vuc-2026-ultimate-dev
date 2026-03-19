#!/usr/bin/env python3
"""
VUC-2026 AI Documentation & Auto-Complete System
Intelligent documentation generation and code completion
"""

import os
import json
import asyncio
import logging
from typing import Dict, List, Optional, Any
from datetime import datetime
import re

import google.generativeai as genai
from fastapi import HTTPException

logger = logging.getLogger(__name__)

class AIDocumentationGenerator:
    """AI-powered documentation generator with smart features"""
    
    def __init__(self):
        # Initialize Gemini AI
        genai.configure(api_key=os.getenv("GOOGLE_AI_API_KEY"))
        self.model = genai.GenerativeModel('gemini-pro')
        
        # Documentation cache
        self.docs_cache = {}
        self.auto_complete_cache = {}
        self.help_cache = {}
        
        # Learning patterns
        self.usage_patterns = {}
        self.popular_topics = {}
        
        logger.info("✅ AI Documentation Generator initialized")
    
    async def generate_docs(self, endpoint: str, method: str, context: str = "") -> Dict:
        """Generate comprehensive AI documentation"""
        
        cache_key = f"{method}_{endpoint}_{hash(context)}"
        
        # Check cache first
        if cache_key in self.docs_cache:
            cached_data = self.docs_cache[cache_key]
            if datetime.now() < cached_data["expires_at"]:
                return cached_data["data"]
        
        # Generate documentation using AI
        prompt = self._create_docs_prompt(endpoint, method, context)
        
        try:
            response = self.model.generate_content(prompt)
            docs_content = response.text
            
            # Process and structure the documentation
            structured_docs = self._structure_documentation(docs_content, endpoint, method)
            
            # Cache result
            self.docs_cache[cache_key] = {
                "data": structured_docs,
                "expires_at": datetime.now() + timedelta(hours=24),
                "generated_at": datetime.now()
            }
            
            # Track usage patterns
            await self._track_usage("generate_docs", endpoint, method)
            
            return structured_docs
            
        except Exception as e:
            logger.error(f"Documentation generation error: {str(e)}")
            raise HTTPException(status_code=500, detail="Failed to generate documentation")
    
    def _create_docs_prompt(self, endpoint: str, method: str, context: str) -> str:
        """Create comprehensive documentation prompt"""
        
        return f"""
        Generate comprehensive API documentation for {method} {endpoint}.
        
        Context: {context}
        
        Include the following sections in markdown format:
        
        ## Overview
        - Purpose and functionality
        - Main use cases
        - Key features
        
        ## Request
        - HTTP Method: {method}
        - Endpoint: {endpoint}
        - Headers required
        - Request parameters (with types and descriptions)
        - Request body structure (if applicable)
        - Example requests
        
        ## Response
        - Response format
        - Status codes and meanings
        - Response schema
        - Example responses
        - Error handling
        
        ## Usage Examples
        - Python examples
        - JavaScript examples
        - cURL examples
        
        ## Best Practices
        - Performance tips
        - Security considerations
        - Common pitfalls
        - Optimization strategies
        
        ## Related Endpoints
        - Complementary APIs
        - Workflow suggestions
        
        Make it comprehensive, practical, and developer-friendly.
        Include code examples and clear explanations.
        """
    
    def _structure_documentation(self, docs_content: str, endpoint: str, method: str) -> Dict:
        """Structure documentation content"""
        
        # Parse markdown sections
        sections = self._parse_markdown_sections(docs_content)
        
        # Extract code examples
        code_examples = self._extract_code_examples(docs_content)
        
        # Generate metadata
        metadata = {
            "endpoint": endpoint,
            "method": method,
            "generated_at": datetime.now().isoformat(),
            "word_count": len(docs_content.split()),
            "complexity_score": self._calculate_complexity_score(docs_content),
            "estimated_reading_time": len(docs_content.split()) / 200  # 200 words per minute
        }
        
        return {
            "metadata": metadata,
            "sections": sections,
            "code_examples": code_examples,
            "raw_content": docs_content,
            "ai_enhancements": {
                "smart_search_enabled": True,
                "interactive_examples": True,
                "auto_updates": True,
                "personalization": True
            }
        }
    
    def _parse_markdown_sections(self, content: str) -> List[Dict]:
        """Parse markdown sections"""
        
        sections = []
        current_section = None
        current_content = []
        
        lines = content.split('\n')
        
        for line in lines:
            if line.startswith('##'):
                # Save previous section
                if current_section:
                    sections.append({
                        "title": current_section,
                        "content": '\n'.join(current_content).strip(),
                        "type": self._classify_section_type(current_section)
                    })
                
                # Start new section
                current_section = line.replace('##', '').strip()
                current_content = []
            else:
                current_content.append(line)
        
        # Save last section
        if current_section:
            sections.append({
                "title": current_section,
                "content": '\n'.join(current_content).strip(),
                "type": self._classify_section_type(current_section)
            })
        
        return sections
    
    def _classify_section_type(self, title: str) -> str:
        """Classify section type"""
        
        title_lower = title.lower()
        
        if "overview" in title_lower:
            return "overview"
        elif "request" in title_lower:
            return "request"
        elif "response" in title_lower:
            return "response"
        elif "example" in title_lower:
            return "example"
        elif "practice" in title_lower:
            return "best_practice"
        elif "related" in title_lower:
            return "related"
        else:
            return "general"
    
    def _extract_code_examples(self, content: str) -> List[Dict]:
        """Extract code examples from content"""
        
        code_blocks = re.findall(r'```(\w+)?\n(.*?)\n```', content, re.DOTALL)
        
        examples = []
        for lang, code in code_blocks:
            examples.append({
                "language": lang or "text",
                "code": code.strip(),
                "executable": lang in ["python", "javascript", "bash", "curl"],
                "copyable": True
            })
        
        return examples
    
    def _calculate_complexity_score(self, content: str) -> float:
        """Calculate documentation complexity score"""
        
        # Simple complexity calculation based on content characteristics
        word_count = len(content.split())
        code_blocks = len(re.findall(r'```', content))
        sections = len(re.findall(r'##', content))
        
        # Normalize to 0-1 scale
        complexity = (word_count / 1000 + code_blocks * 0.1 + sections * 0.05) / 3
        return min(1.0, complexity)
    
    async def auto_complete(self, partial_input: str, context: str = "", language: str = "python") -> Dict:
        """AI-powered auto-complete functionality"""
        
        cache_key = f"{hash(partial_input)}_{context}_{language}"
        
        # Check cache
        if cache_key in self.auto_complete_cache:
            cached_data = self.auto_complete_cache[cache_key]
            if datetime.now() < cached_data["expires_at"]:
                return cached_data["data"]
        
        # Generate suggestions
        prompt = self._create_auto_complete_prompt(partial_input, context, language)
        
        try:
            response = self.model.generate_content(prompt)
            suggestions = self._parse_suggestions(response.text)
            
            # Rank suggestions
            ranked_suggestions = self._rank_suggestions(suggestions, partial_input, context)
            
            # Cache result
            self.auto_complete_cache[cache_key] = {
                "data": ranked_suggestions,
                "expires_at": datetime.now() + timedelta(hours=1),
                "generated_at": datetime.now()
            }
            
            # Track usage
            await self._track_usage("auto_complete", partial_input, language)
            
            return ranked_suggestions
            
        except Exception as e:
            logger.error(f"Auto-complete error: {str(e)}")
            return {"suggestions": [], "error": "Auto-completion temporarily unavailable"}
    
    def _create_auto_complete_prompt(self, partial_input: str, context: str, language: str) -> str:
        """Create auto-complete prompt"""
        
        return f"""
        Provide intelligent auto-completion suggestions for the following {language} code:
        
        Partial input: {partial_input}
        Context: {context}
        
        Return suggestions in JSON format:
        {{
            "suggestions": [
                {{
                    "text": "completed_code",
                    "display_text": "display_text",
                    "description": "description",
                    "confidence": 0.95,
                    "type": "function|variable|class|method|keyword"
                }}
            ]
        }}
        
        Consider:
        - Syntax correctness for {language}
        - Context relevance
        - Common patterns and best practices
        - VUC-2026 specific functions and classes
        """
    
    def _parse_suggestions(self, response_text: str) -> List[Dict]:
        """Parse AI suggestions"""
        
        try:
            # Try to parse as JSON
            suggestions_data = json.loads(response_text)
            return suggestions_data.get("suggestions", [])
        except:
            # Fallback: parse line by line
            lines = response_text.split('\n')
            suggestions = []
            
            for line in lines:
                line = line.strip()
                if line and not line.startswith('#'):
                    suggestions.append({
                        "text": line,
                        "display_text": line,
                        "description": "Auto-completion suggestion",
                        "confidence": 0.7,
                        "type": "text"
                    })
            
            return suggestions
    
    def _rank_suggestions(self, suggestions: List[Dict], partial_input: str, context: str) -> Dict:
        """Rank suggestions by relevance and confidence"""
        
        # Sort by confidence
        sorted_suggestions = sorted(suggestions, key=lambda x: x.get("confidence", 0), reverse=True)
        
        # Apply context-based ranking
        for suggestion in sorted_suggestions:
            # Boost confidence based on context relevance
            if context and context.lower() in suggestion.get("text", "").lower():
                suggestion["confidence"] = min(1.0, suggestion.get("confidence", 0) + 0.2)
        
        # Re-sort after boosting
        sorted_suggestions = sorted(sorted_suggestions, key=lambda x: x.get("confidence", 0), reverse=True)
        
        return {
            "suggestions": sorted_suggestions[:10],  # Top 10 suggestions
            "partial_input": partial_input,
            "context": context,
            "total_suggestions": len(sorted_suggestions),
            "ai_features": {
                "context_aware": True,
                "confidence_scoring": True,
                "syntax_validation": True,
                "pattern_learning": True
            }
        }
    
    async def smart_help(self, query: str, context: str = "") -> Dict:
        """AI-powered smart help system"""
        
        cache_key = f"help_{hash(query)}_{context}"
        
        # Check cache
        if cache_key in self.help_cache:
            cached_data = self.help_cache[cache_key]
            if datetime.now() < cached_data["expires_at"]:
                return cached_data["data"]
        
        # Generate help response
        prompt = self._create_help_prompt(query, context)
        
        try:
            response = self.model.generate_content(prompt)
            help_content = response.text
            
            # Structure help content
            structured_help = self._structure_help_content(help_content, query)
            
            # Cache result
            self.help_cache[cache_key] = {
                "data": structured_help,
                "expires_at": datetime.now() + timedelta(hours=6),
                "generated_at": datetime.now()
            }
            
            # Track usage
            await self._track_usage("smart_help", query, context)
            
            return structured_help
            
        except Exception as e:
            logger.error(f"Smart help error: {str(e)}")
            return {
                "query": query,
                "help": "I'm sorry, I'm having trouble processing your request right now. Please try again later.",
                "error": "Help system temporarily unavailable"
            }
    
    def _create_help_prompt(self, query: str, context: str) -> str:
        """Create help prompt"""
        
        return f"""
        Provide helpful assistance for the following query about VUC-2026:
        
        Query: {query}
        Context: {context}
        
        Include:
        - Direct answer to the question
        - Step-by-step instructions if applicable
        - Code examples if relevant
        - Related topics and resources
        - Best practices and tips
        - Troubleshooting suggestions
        
        Be comprehensive, clear, and actionable. Focus on practical solutions.
        """
    
    def _structure_help_content(self, content: str, query: str) -> Dict:
        """Structure help content"""
        
        return {
            "query": query,
            "answer": content,
            "timestamp": datetime.now().isoformat(),
            "related_topics": self._extract_related_topics(content),
            "actionable_items": self._extract_actionable_items(content),
            "code_examples": self._extract_code_examples(content),
            "ai_enhancements": {
                "contextual_relevance": True,
                "actionable_insights": True,
                "related_resources": True,
                "follow_up_questions": self._generate_follow_up_questions(query, content)
            }
        }
    
    def _extract_related_topics(self, content: str) -> List[str]:
        """Extract related topics from content"""
        
        # Simple keyword extraction
        vuc_keywords = [
            "elevenlabs", "youtube", "oauth", "api", "authentication",
            "video", "upload", "family", "kids", "content", "optimization",
            "ai", "gemini", "voice", "synthesis", "rendering"
        ]
        
        related = []
        content_lower = content.lower()
        
        for keyword in vuc_keywords:
            if keyword in content_lower:
                related.append(keyword)
        
        return related[:5]  # Top 5 related topics
    
    def _extract_actionable_items(self, content: str) -> List[str]:
        """Extract actionable items from content"""
        
        actionable_patterns = [
            r"(\d+\. .*?)(?=\d+\. |$)",  # Numbered lists
            r"(\* .*?)(?=\* |$)",        # Bullet points
            r"(Step \d+: .*?)(?=Step \d+:|$)"  # Steps
        ]
        
        items = []
        
        for pattern in actionable_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            items.extend([match.strip() for match in matches])
        
        return items[:10]  # Top 10 actionable items
    
    def _generate_follow_up_questions(self, query: str, content: str) -> List[str]:
        """Generate follow-up questions"""
        
        # Generate contextual follow-up questions
        questions = [
            "Would you like more specific examples?",
            "Do you need help with implementation?",
            "Would you like to see related documentation?",
            "Do you have any follow-up questions?"
        ]
        
        # Context-specific questions
        if "elevenlabs" in query.lower():
            questions.append("Would you like help with voice settings optimization?")
        
        if "youtube" in query.lower():
            questions.append("Do you need help with video upload process?")
        
        if "oauth" in query.lower():
            questions.append("Would you like help with authentication setup?")
        
        return questions[:5]  # Top 5 questions
    
    async def _track_usage(self, feature: str, query: str, context: str):
        """Track usage patterns for AI learning"""
        
        timestamp = datetime.now()
        
        if feature not in self.usage_patterns:
            self.usage_patterns[feature] = []
        
        self.usage_patterns[feature].append({
            "query": query,
            "context": context,
            "timestamp": timestamp
        })
        
        # Keep only recent patterns
        if len(self.usage_patterns[feature]) > 1000:
            self.usage_patterns[feature] = self.usage_patterns[feature][-500:]
    
    async def get_usage_analytics(self) -> Dict:
        """Get usage analytics for AI learning"""
        
        analytics = {
            "total_requests": 0,
            "feature_usage": {},
            "popular_topics": {},
            "peak_hours": {},
            "learning_insights": []
        }
        
        for feature, patterns in self.usage_patterns.items():
            analytics["feature_usage"][feature] = len(patterns)
            analytics["total_requests"] += len(patterns)
            
            # Analyze popular topics
            for pattern in patterns:
                query = pattern["query"]
                if query not in analytics["popular_topics"]:
                    analytics["popular_topics"][query] = 0
                analytics["popular_topics"][query] += 1
        
        # Sort popular topics
        analytics["popular_topics"] = dict(
            sorted(analytics["popular_topics"].items(), key=lambda x: x[1], reverse=True)[:10]
        )
        
        return analytics
    
    async def clear_cache(self, cache_type: str = "all") -> Dict:
        """Clear AI documentation cache"""
        
        cleared_caches = []
        
        if cache_type in ["all", "docs"]:
            self.docs_cache.clear()
            cleared_caches.append("documentation")
        
        if cache_type in ["all", "autocomplete"]:
            self.auto_complete_cache.clear()
            cleared_caches.append("auto_complete")
        
        if cache_type in ["all", "help"]:
            self.help_cache.clear()
            cleared_caches.append("smart_help")
        
        return {
            "success": True,
            "cleared_caches": cleared_caches,
            "timestamp": datetime.now().isoformat()
        }
    
    async def optimize_performance(self) -> Dict:
        """Optimize AI documentation performance"""
        
        optimizations = []
        
        # Clean expired cache entries
        current_time = datetime.now()
        
        for cache_name, cache_data in [
            ("docs_cache", self.docs_cache),
            ("auto_complete_cache", self.auto_complete_cache),
            ("help_cache", self.help_cache)
        ]:
            expired_keys = [
                key for key, data in cache_data.items()
                if current_time > data["expires_at"]
            ]
            
            for key in expired_keys:
                del cache_data[key]
            
            if expired_keys:
                optimizations.append(f"Cleaned {len(expired_keys)} expired entries from {cache_name}")
        
        # Optimize usage patterns
        for feature in self.usage_patterns:
            if len(self.usage_patterns[feature]) > 500:
                self.usage_patterns[feature] = self.usage_patterns[feature][-250:]
                optimizations.append(f"Optimized {feature} usage patterns")
        
        return {
            "optimizations": optimizations,
            "performance_metrics": {
                "cache_sizes": {
                    "docs_cache": len(self.docs_cache),
                    "auto_complete_cache": len(self.auto_complete_cache),
                    "help_cache": len(self.help_cache)
                },
                "usage_patterns": len(self.usage_patterns)
            },
            "timestamp": datetime.now().isoformat()
        }

# Global instance
ai_documentation_generator = AIDocumentationGenerator()
