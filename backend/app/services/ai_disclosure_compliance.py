"""
VUC-2026 AI Disclosure Compliance
YouTube AI etiketleme ve human-assisted loop sistemi
"""

import json
import time
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
import requests

class AIContentType(Enum):
    """AI içerik türleri"""
    DEEPFAKE = "deepfake"
    SYNTHETIC_VOICE = "synthetic_voice"
    AI_GENERATED_VISUALS = "ai_generated_visuals"
    AI_SCRIPT = "ai_generated_script"
    AI_EDITING = "ai_editing"
    HUMAN_ASSISTED = "human_assisted"

@dataclass
class AIDisclosure:
    """AI disclosure bilgileri"""
    content_type: AIContentType
    ai_percentage: float  # 0-100 arası AI katkı yüzdesi
    human_reviewed: bool
    disclosure_text: str
    youtube_api_label: str
    human_assistance_level: str  # "minimal", "moderate", "extensive"

class SmartDisclosure:
    """Akıllı AI disclosure sistemi"""
    
    def __init__(self, youtube_api_service):
        self.youtube_api = youtube_api_service
        self.disclosure_templates = {
            AIContentType.DEEPFAKE: "Bu videodaki kişiler yapay zeka tarafından oluşturulmuştur.",
            AIContentType.SYNTHETIC_VOICE: "Bu videodaki ses yapay zeka tarafından sentezlenmiştir.",
            AIContentType.AI_GENERATED_VISUALS: "Bu videodaki bazı görseller yapay zeka tarafından oluşturulmuştur.",
            AIContentType.AI_SCRIPT: "Bu videonun senaryosu yapay zeka yardımıyla hazırlanmıştır.",
            AIContentType.AI_EDITING: "Bu video yapay zeka ile düzenlenmiştir.",
            AIContentType.HUMAN_ASSISTED: "Bu video insan denetiminde yapay zeka destekli üretilmiştir."
        }
    
    def analyze_ai_content(self, video_metadata: Dict) -> List[AIContentType]:
        """Videodaki AI içeriklerini analiz et"""
        ai_content_types = []
        
        # Script AI tarafından mı oluşturuldu?
        if video_metadata.get('script_ai_generated', False):
            ai_content_types.append(AIContentType.AI_SCRIPT)
        
        # Synthetic voice kullanıldı mı?
        if video_metadata.get('synthetic_voice_used', False):
            ai_content_types.append(AIContentType.SYNTHETIC_VOICE)
        
        # AI generated visuals var mı?
        if video_metadata.get('ai_visuals_used', False):
            ai_content_types.append(AIContentType.AI_GENERATED_VISUALS)
        
        # AI editing kullanıldı mı?
        if video_metadata.get('ai_editing_used', False):
            ai_content_types.append(AIContentType.AI_EDITING)
        
        # Deepface/deepfake var mı?
        if video_metadata.get('deepfake_detected', False):
            ai_content_types.append(AIContentType.DEEPFAKE)
        
        return ai_content_types
    
    def calculate_ai_percentage(self, video_metadata: Dict) -> float:
        """AI katkı yüzdesini hesapla"""
        weights = {
            'script_ai_generated': 0.3,
            'synthetic_voice_used': 0.25,
            'ai_visuals_used': 0.2,
            'ai_editing_used': 0.15,
            'deepfake_detected': 0.1
        }
        
        ai_percentage = 0.0
        for factor, weight in weights.items():
            if video_metadata.get(factor, False):
                ai_percentage += weight * 100
        
        return min(ai_percentage, 100.0)
    
    def generate_disclosure_text(self, ai_content_types: List[AIContentType], ai_percentage: float) -> str:
        """YouTube disclosure metni oluştur"""
        if not ai_content_types:
            return ""
        
        # En kritik AI içerik tipini bul
        priority_order = [
            AIContentType.DEEPFAKE,
            AIContentType.SYNTHETIC_VOICE,
            AIContentType.AI_GENERATED_VISUALS,
            AIContentType.AI_SCRIPT,
            AIContentType.AI_EDITING
        ]
        
        primary_type = None
        for content_type in priority_order:
            if content_type in ai_content_types:
                primary_type = content_type
                break
        
        if primary_type:
            base_text = self.disclosure_templates[primary_type]
            
            # Ek AI içerikleri varsa ekle
            if len(ai_content_types) > 1:
                additional_types = [ct for ct in ai_content_types if ct != primary_type]
                additional_text = ", ".join([self.disclosure_templates[ct].lower() for ct in additional_types])
                base_text += f" Ayrıca {additional_text}."
            
            return base_text
        
        return ""
    
    def create_youtube_label(self, ai_content_types: List[AIContentType]) -> str:
        """YouTube API için label oluştur"""
        if AIContentType.DEEPFAKE in ai_content_types:
            return "altered_or_synthetic_content_deepfake"
        elif AIContentType.SYNTHETIC_VOICE in ai_content_types:
            return "altered_or_synthetic_content_voice"
        elif AIContentType.AI_GENERATED_VISUALS in ai_content_types:
            return "altered_or_synthetic_content_visual"
        elif ai_content_types:
            return "altered_or_synthetic_content_general"
        else:
            return "human_created_content"

class HumanAssistedLoop:
    """İnsan denetim loop'u"""
    
    def __init__(self, youtube_api_service):
        self.youtube_api = youtube_api_service
        self.pending_reviews = {}
        self.review_history = []
    
    def submit_for_review(self, video_id: str, video_path: str, ai_disclosure: AIDisclosure) -> str:
        """Videoyu insan denetimi için gönder"""
        review_id = f"review_{video_id}_{int(time.time())}"
        
        self.pending_reviews[review_id] = {
            "video_id": video_id,
            "video_path": video_path,
            "ai_disclosure": ai_disclosure,
            "submitted_at": datetime.now().isoformat(),
            "status": "pending_review",
            "human_reviewer": None,
            "review_notes": None,
            "approval_status": None
        }
        
        return review_id
    
    def create_review_interface(self, review_id: str) -> Dict:
        """İnsan denetim arayüzü verileri"""
        if review_id not in self.pending_reviews:
            return {"error": "Review not found"}
        
        review = self.pending_reviews[review_id]
        
        return {
            "review_id": review_id,
            "video_id": review["video_id"],
            "video_path": review["video_path"],
            "ai_disclosure": {
                "content_type": review["ai_disclosure"].content_type.value,
                "ai_percentage": review["ai_disclosure"].ai_percentage,
                "disclosure_text": review["ai_disclosure"].disclosure_text,
                "youtube_label": review["ai_disclosure"].youtube_api_label
            },
            "review_checklist": [
                {
                    "item": "İçerik uygun mu?",
                    "type": "boolean",
                    "required": True
                },
                {
                    "item": "AI disclosure metni doğru mu?",
                    "type": "boolean",
                    "required": True
                },
                {
                    "item": "Yayınlanmaya hazır mı?",
                    "type": "boolean",
                    "required": True
                },
                {
                    "item": "Ek notlar",
                    "type": "text",
                    "required": False
                }
            ],
            "preview_url": f"/api/videos/{review['video_id']}/preview",
            "submit_url": f"/api/reviews/{review_id}/submit"
        }
    
    def submit_review(self, review_id: str, reviewer_data: Dict) -> Dict:
        """İnsan denetim sonuçlarını gönder"""
        if review_id not in self.pending_reviews:
            return {"error": "Review not found"}
        
        review = self.pending_reviews[review_id]
        
        # Denetim sonuçlarını kaydet
        review["human_reviewer"] = reviewer_data.get("reviewer_name", "Human Reviewer")
        review["review_notes"] = reviewer_data.get("notes", "")
        review["approval_status"] = reviewer_data.get("approved", False)
        review["reviewed_at"] = datetime.now().isoformat()
        review["status"] = "completed"
        
        # History'e ekle
        self.review_history.append(review.copy())
        
        # Pending'den kaldır
        del self.pending_reviews[review_id]
        
        return {
            "success": True,
            "review_id": review_id,
            "approval_status": review["approval_status"],
            "human_assistance_level": self._calculate_assistance_level(review)
        }
    
    def _calculate_assistance_level(self, review: Dict) -> str:
        """İnsan yardım seviyesini hesapla"""
        ai_percentage = review["ai_disclosure"].ai_percentage
        review_notes_length = len(review.get("review_notes", ""))
        
        if ai_percentage > 80 and review_notes_length < 50:
            return "minimal"
        elif ai_percentage > 50:
            return "moderate"
        else:
            return "extensive"

class AIDisclosureCompliance:
    """Ana AI Disclosure Compliance sınıfı"""
    
    def __init__(self, youtube_api_service):
        self.smart_disclosure = SmartDisclosure(youtube_api_service)
        self.human_loop = HumanAssistedLoop(youtube_api_service)
    
    def process_video(self, video_id: str, video_path: str, video_metadata: Dict) -> Dict:
        """Videoyu AI disclosure sürecinden geçir"""
        
        # 1. AI içeriklerini analiz et
        ai_content_types = self.smart_disclosure.analyze_ai_content(video_metadata)
        
        # 2. AI katkı yüzdesini hesapla
        ai_percentage = self.smart_disclosure.calculate_ai_percentage(video_metadata)
        
        # 3. Disclosure metni oluştur
        disclosure_text = self.smart_disclosure.generate_disclosure_text(ai_content_types, ai_percentage)
        
        # 4. YouTube label oluştur
        youtube_label = self.smart_disclosure.create_youtube_label(ai_content_types)
        
        # 5. AI disclosure objesi oluştur
        ai_disclosure = AIDisclosure(
            content_type=ai_content_types[0] if ai_content_types else AIContentType.HUMAN_ASSISTED,
            ai_percentage=ai_percentage,
            human_reviewed=False,
            disclosure_text=disclosure_text,
            youtube_api_label=youtube_label,
            human_assistance_level="pending"
        )
        
        # 6. İnsan denetimine gönder
        review_id = self.human_loop.submit_for_review(video_id, video_path, ai_disclosure)
        
        # 7. Denetim arayüzü oluştur
        review_interface = self.human_loop.create_review_interface(review_id)
        
        return {
            "video_id": video_id,
            "review_id": review_id,
            "ai_disclosure": ai_disclosure,
            "review_interface": review_interface,
            "compliance_status": "pending_human_review",
            "next_step": "human_approval_required"
        }
    
    def apply_disclosure_to_youtube(self, video_id: str, ai_disclosure: AIDisclosure) -> bool:
        """YouTube'a disclosure uygula"""
        try:
            # YouTube API üzerinden disclosure label'ını uygula
            response = self.smart_disclosure.youtube_api.apply_content_label(
                video_id=video_id,
                label=ai_disclosure.youtube_api_label,
                disclosure_text=ai_disclosure.disclosure_text
            )
            
            return response.get("success", False)
        except Exception as e:
            print(f"YouTube disclosure application error: {e}")
            return False
    
    def get_compliance_report(self, video_id: str) -> Dict:
        """Uyumluluk raporu oluştur"""
        # Review history'den bul
        review = None
        for hist_review in self.human_loop.review_history:
            if hist_review["video_id"] == video_id:
                review = hist_review
                break
        
        if not review:
            return {"error": "No review found for video"}
        
        return {
            "video_id": video_id,
            "ai_disclosure": review["ai_disclosure"],
            "human_review": {
                "reviewer": review["human_reviewer"],
                "reviewed_at": review["reviewed_at"],
                "approval_status": review["approval_status"],
                "notes": review["review_notes"],
                "assistance_level": review["human_assistance_level"]
            },
            "youtube_compliance": {
                "disclosure_applied": True,
                "label": review["ai_disclosure"].youtube_api_label,
                "content_type": review["ai_disclosure"].content_type.value,
                "ai_percentage": review["ai_disclosure"].ai_percentage
            },
            "compliance_score": self._calculate_compliance_score(review)
        }
    
    def _calculate_compliance_score(self, review: Dict) -> int:
        """Uyumluluk skoru hesapla (0-100)"""
        base_score = 70
        
        # İnsan denetimi +20
        if review["approval_status"]:
            base_score += 20
        
        # AI disclosure metni +10
        if review["ai_disclosure"].disclosure_text:
            base_score += 10
        
        # İnsan yardım seviyesine göre bonus
        assistance_level = review["human_assistance_level"]
        if assistance_level == "extensive":
            base_score += 5
        elif assistance_level == "moderate":
            base_score += 3
        elif assistance_level == "minimal":
            base_score += 1
        
        return min(base_score, 100)
