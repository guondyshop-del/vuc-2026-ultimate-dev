"""
VUC-2026 Persona Configuration Service
YouTube persona management and configuration
"""

import json
import os
from typing import Dict, List, Optional, Any
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class PersonaService:
    """Persona management service for YouTube automation"""
    
    def __init__(self):
        self.personas_file = "vuc_memory/personas.json"
        self.config_file = "vuc_memory/persona_config.json"
        self.load_personas()
    
    def load_personas(self):
        """Load personas from file or create defaults"""
        try:
            if os.path.exists(self.personas_file):
                with open(self.personas_file, 'r', encoding='utf-8') as f:
                    self.personas = json.load(f)
            else:
                self.personas = self._create_default_personas()
                self.save_personas()
        except Exception as e:
            logger.error(f"Error loading personas: {e}")
            self.personas = self._create_default_personas()
    
    def _create_default_personas(self) -> Dict[str, Any]:
        """Create default persona configurations"""
        return {
            "TechWizard_TR": {
                "id": "TechWizard_TR",
                "name": "Teknoloji Büyücüsü",
                "niche": "technology",
                "avatar": "🧙",
                "trust_score": 6.2,
                "description": "Yapay zeka ve teknoloji uzmanı",
                "content_style": {
                    "tone": "professional",
                    "complexity": "high",
                    "engagement_type": "educational"
                },
                "posting_schedule": {
                    "frequency": "daily",
                    "optimal_times": ["09:00", "18:00", "21:00"],
                    "days_active": ["monday", "tuesday", "wednesday", "thursday", "friday"]
                },
                "target_audience": {
                    "age_range": "25-45",
                    "interests": ["AI", "programming", "tech news", "gadgets"],
                    "location": "Turkey"
                },
                "content_themes": [
                    "AI tools review",
                    "Programming tutorials", 
                    "Tech trend analysis",
                    "Gadget comparisons"
                ],
                "content_standards": {
                    "min_word_count": 1500,
                    "target_word_count": 2000,
                    "max_word_count": 3000,
                    "min_paragraphs": 8,
                    "target_paragraphs": 12,
                    "required_sections": [
                        "giriş",
                        "ana_konu",
                        "detaylı_analiz",
                        "pratik_uygulamalar",
                        "sonuç"
                    ],
                    "seo_requirements": {
                        "keyword_density": 0.02,
                        "min_headings": 6,
                        "required_headings": ["h1", "h2", "h3"],
                        "min_lists": 2,
                        "min_images": 3
                    }
                }
            },
            "BusinessGuru_TR": {
                "id": "BusinessGuru_TR",
                "name": "İş Gurusu",
                "niche": "business",
                "avatar": "👨‍💼",
                "trust_score": 7.8,
                "description": "İş dünyası ve girişimcilik uzmanı",
                "content_style": {
                    "tone": "motivational",
                    "complexity": "medium",
                    "engagement_type": "inspirational"
                },
                "posting_schedule": {
                    "frequency": "weekly",
                    "optimal_times": ["07:00", "12:00", "20:00"],
                    "days_active": ["monday", "wednesday", "friday", "sunday"]
                },
                "target_audience": {
                    "age_range": "30-55",
                    "interests": ["entrepreneurship", "finance", "leadership", "marketing"],
                    "location": "Turkey"
                },
                "content_themes": [
                    "Startup strategies",
                    "Investment tips",
                    "Leadership lessons",
                    "Business case studies"
                ],
                "content_standards": {
                    "min_word_count": 1800,
                    "target_word_count": 2200,
                    "max_word_count": 3500,
                    "min_paragraphs": 10,
                    "target_paragraphs": 15,
                    "required_sections": [
                        "giriş",
                        "problemler",
                        "çözümler",
                        "vaka_çalışmaları",
                        "stratejiler",
                        "sonuç"
                    ],
                    "seo_requirements": {
                        "keyword_density": 0.025,
                        "min_headings": 8,
                        "required_headings": ["h1", "h2", "h3", "h4"],
                        "min_lists": 3,
                        "min_images": 4
                    }
                }
            },
            "ProGamer_TR": {
                "id": "ProGamer_TR",
                "name": "Pro Oyuncu",
                "niche": "gaming",
                "avatar": "🎮",
                "trust_score": 5.1,
                "description": "Profesyonel oyun yorumcusu",
                "content_style": {
                    "tone": "casual",
                    "complexity": "low",
                    "engagement_type": "entertaining"
                },
                "posting_schedule": {
                    "frequency": "daily",
                    "optimal_times": ["16:00", "20:00", "23:00"],
                    "days_active": ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
                },
                "target_audience": {
                    "age_range": "16-35",
                    "interests": ["gaming", "esports", "game reviews", "streaming"],
                    "location": "Turkey"
                },
                "content_themes": [
                    "Game reviews",
                    "Tournament coverage",
                    "Gaming tips",
                    "Esports news"
                ],
                "content_standards": {
                    "min_word_count": 1200,
                    "target_word_count": 1800,
                    "max_word_count": 2500,
                    "min_paragraphs": 6,
                    "target_paragraphs": 10,
                    "required_sections": [
                        "giriş",
                        "oyun_değerlendirme",
                        "taktikler",
                        "ipuçları",
                        "sonuç"
                    ],
                    "seo_requirements": {
                        "keyword_density": 0.015,
                        "min_headings": 5,
                        "required_headings": ["h1", "h2", "h3"],
                        "min_lists": 2,
                        "min_images": 5
                    }
                }
            }
        }
    
    def save_personas(self):
        """Save personas to file"""
        try:
            os.makedirs(os.path.dirname(self.personas_file), exist_ok=True)
            with open(self.personas_file, 'w', encoding='utf-8') as f:
                json.dump(self.personas, f, ensure_ascii=False, indent=2)
        except Exception as e:
            logger.error(f"Error saving personas: {e}")
    
    def get_persona(self, persona_id: str) -> Optional[Dict[str, Any]]:
        """Get specific persona by ID"""
        return self.personas.get(persona_id)
    
    def get_all_personas(self) -> Dict[str, Any]:
        """Get all personas"""
        return self.personas
    
    def create_persona(self, persona_data: Dict[str, Any]) -> bool:
        """Create new persona"""
        try:
            persona_id = persona_data.get("id")
            if not persona_id or persona_id in self.personas:
                return False
            
            # Set default values
            persona_data.setdefault("trust_score", 5.0)
            persona_data.setdefault("created_at", datetime.now().isoformat())
            
            self.personas[persona_id] = persona_data
            self.save_personas()
            return True
        except Exception as e:
            logger.error(f"Error creating persona: {e}")
            return False
    
    def update_persona(self, persona_id: str, updates: Dict[str, Any]) -> bool:
        """Update existing persona"""
        try:
            if persona_id not in self.personas:
                return False
            
            self.personas[persona_id].update(updates)
            self.personas[persona_id]["updated_at"] = datetime.now().isoformat()
            self.save_personas()
            return True
        except Exception as e:
            logger.error(f"Error updating persona: {e}")
            return False
    
    def delete_persona(self, persona_id: str) -> bool:
        """Delete persona"""
        try:
            if persona_id in self.personas:
                del self.personas[persona_id]
                self.save_personas()
                return True
            return False
        except Exception as e:
            logger.error(f"Error deleting persona: {e}")
            return False
    
    def get_persona_config(self) -> Dict[str, Any]:
        """Get persona configuration status"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except:
            pass
        
        # Default configuration
        return {
            "auto_switching": False,
            "trust_threshold": 6.0,
            "max_concurrent_personas": 3,
            "default_persona": "TechWizard_TR",
            "rotation_strategy": "trust_based",
            "content_generation": {
                "auto_titles": True,
                "auto_descriptions": True,
                "auto_tags": True,
                "auto_thumbnails": False
            }
        }
    
    def update_persona_config(self, config: Dict[str, Any]) -> bool:
        """Update persona configuration"""
        try:
            os.makedirs(os.path.dirname(self.config_file), exist_ok=True)
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            logger.error(f"Error updating persona config: {e}")
            return False
    
    def get_configuration_status(self) -> Dict[str, Any]:
        """Get configuration completion status"""
        personas = self.get_all_personas()
        config = self.get_persona_config()
        
        total_personas = len(personas)
        configured_personas = sum(1 for p in personas.values() 
                               if p.get("content_style") and p.get("posting_schedule"))
        
        return {
            "total_personas": total_personas,
            "configured_personas": configured_personas,
            "config_completed": configured_personas >= 2,
            "status": f"{configured_personas}/2"
        }

# Global instance
persona_service = PersonaService()
