"""
VUC-2026 YouTube Ad-Slot & Revenue Optimization Engine
Dynamic mid-roll placement with NLP engagement analysis
"""

from typing import Dict, List, Optional, Tuple
from datetime import datetime, timedelta
import json
import re
from dataclasses import dataclass
from pydantic import BaseModel

from app.services.ai_service import AIService
from app.core.ai_intelligence import AIIntelligence

@dataclass
class AdSlot:
    """Ad slot configuration"""
    position_seconds: int
    ad_type: str  # mid_roll, pre_roll, post_roll
    engagement_score: float
    predicted_cpm: float
    retention_impact: float

class EngagementAnalyzer(BaseModel):
    """NLP-based engagement analysis"""
    high_tension_points: List[int]
    drop_off_risk_points: List[int]
    optimal_ad_positions: List[int]
    overall_engagement_score: float

class AdSlotOptimizationService:
    """YouTube Ad-Slot & Revenue Optimization Service"""
    
    def __init__(self):
        self.ai_service = AIService()
        self.ai_intelligence = AIIntelligence()
        
        # Ad slot optimization parameters
        self.min_interval_between_ads = 180  # 3 minutes
        self.max_mid_rolls_per_10min = 2
        self.retention_threshold = 0.85
        self.coppa_cpm_adjustment = 0.7  # 30% lower CPM for kids content
        
        # High-tension keywords for engagement detection
        self.high_tension_keywords = [
            "shock", "surprise", "amazing", "incredible", "unbelievable",
            "wow", "omg", "can't believe", "mind blowing", "game changer",
            "finally", "at last", "the secret", "revealed", "exclusive",
            "never before", "first time", "breaking", "urgent", "important"
        ]
        
        # Drop-off risk indicators
        self.drop_off_indicators = [
            "boring", "slow", "complicated", "technical", "detailed",
            "explanation", "background", "history", "introduction", "overview"
        ]

    async def analyze_script_engagement(self, script: str, duration: int) -> EngagementAnalyzer:
        """
        Analyze script for engagement patterns using NLP
        """
        # Split script into sentences with timestamps
        sentences = self._parse_script_with_timing(script, duration)
        
        high_tension_points = []
        drop_off_risk_points = []
        
        for i, (timestamp, sentence) in enumerate(sentences):
            sentence_lower = sentence.lower()
            
            # Check for high-tension keywords
            tension_score = sum(1 for keyword in self.high_tension_keywords if keyword in sentence_lower)
            if tension_score > 0:
                high_tension_points.append(timestamp)
            
            # Check for drop-off risk indicators
            drop_off_score = sum(1 for indicator in self.drop_off_indicators if indicator in sentence_lower)
            if drop_off_score > 0:
                drop_off_risk_points.append(timestamp)
        
        # Calculate optimal ad positions (just before drop-off points)
        optimal_ad_positions = []
        for drop_point in drop_off_risk_points:
            # Place ad 30 seconds before potential drop-off
            ad_position = max(0, drop_point - 30)
            if ad_position > 60:  # Don't place ads in first minute
                optimal_ad_positions.append(ad_position)
        
        # Calculate overall engagement score
        total_sentences = len(sentences)
        high_tension_ratio = len(high_tension_points) / max(1, total_sentences)
        drop_off_ratio = len(drop_off_risk_points) / max(1, total_sentences)
        
        overall_engagement_score = min(1.0, high_tension_ratio * 2 - drop_off_ratio * 0.5 + 0.5)
        
        return EngagementAnalyzer(
            high_tension_points=high_tension_points,
            drop_off_risk_points=drop_off_risk_points,
            optimal_ad_positions=optimal_ad_positions,
            overall_engagement_score=overall_engagement_score
        )

    async def optimize_ad_slots(self, 
                               script: str,
                               duration: int,
                               is_kids_content: bool = False,
                               target_cpm: float = 2.5) -> List[AdSlot]:
        """
        Generate optimal ad slot placement strategy
        """
        # Analyze engagement patterns
        engagement = await self.analyze_script_engagement(script, duration)
        
        ad_slots = []
        
        # Pre-roll (always enabled)
        pre_roll_cpm = target_cpm * (self.coppa_cpm_adjustment if is_kids_content else 1.0)
        ad_slots.append(AdSlot(
            position_seconds=0,
            ad_type="pre_roll",
            engagement_score=1.0,
            predicted_cpm=pre_roll_cpm,
            retention_impact=0.02  # 2% retention loss for pre-roll
        ))
        
        # Mid-rolls based on engagement analysis
        if duration >= 480:  # Only add mid-rolls for videos 8+ minutes
            mid_roll_positions = self._calculate_mid_roll_positions(
                engagement.optimal_ad_positions,
                duration,
                is_kids_content
            )
            
            for position in mid_roll_positions:
                # Calculate CPM based on position and engagement
                position_cpm = self._calculate_position_cpm(
                    position, 
                    duration, 
                    engagement.overall_engagement_score,
                    target_cpm,
                    is_kids_content
                )
                
                # Calculate retention impact
                retention_impact = self._calculate_retention_impact(
                    position, 
                    duration, 
                    engagement.overall_engagement_score
                )
                
                ad_slots.append(AdSlot(
                    position_seconds=position,
                    ad_type="mid_roll",
                    engagement_score=engagement.overall_engagement_score,
                    predicted_cpm=position_cpm,
                    retention_impact=retention_impact
                ))
        
        # Post-roll (lower value but still revenue)
        post_roll_cpm = target_cpm * 0.6 * (self.coppa_cpm_adjustment if is_kids_content else 1.0)
        ad_slots.append(AdSlot(
            position_seconds=duration,
            ad_type="post_roll",
            engagement_score=0.3,
            predicted_cpm=post_roll_cpm,
            retention_impact=0.0  # No retention impact for post-roll
        ))
        
        return ad_slots

    def _parse_script_with_timing(self, script: str, duration: int) -> List[Tuple[int, str]]:
        """
        Parse script and estimate timing for each sentence
        """
        sentences = re.split(r'[.!?]+', script)
        sentences = [s.strip() for s in sentences if s.strip()]
        
        # Estimate reading speed: 150 words per minute = 2.5 words per second
        total_words = sum(len(sentence.split()) for sentence in sentences)
        words_per_second = total_words / max(1, duration)
        
        timed_sentences = []
        current_time = 0
        
        for sentence in sentences:
            word_count = len(sentence.split())
            sentence_duration = word_count / max(1, words_per_second)
            timed_sentences.append((int(current_time), sentence))
            current_time += sentence_duration
        
        return timed_sentences

    def _calculate_mid_roll_positions(self, 
                                    optimal_positions: List[int],
                                    duration: int,
                                    is_kids_content: bool) -> List[int]:
        """
        Calculate optimal mid-roll positions
        """
        positions = []
        
        # Filter positions based on constraints
        filtered_positions = []
        for pos in optimal_positions:
            if pos < duration - 60:  # Not in last minute
                filtered_positions.append(pos)
        
        # Sort and apply minimum interval constraint
        filtered_positions.sort()
        
        last_position = 0
        for pos in filtered_positions:
            if pos - last_position >= self.min_interval_between_ads:
                positions.append(pos)
                last_position = pos
        
        # Add strategic positions if no optimal positions found
        if not positions and duration >= 600:  # 10+ minutes
            # Place at 25%, 50%, and 75% marks
            positions = [
                int(duration * 0.25),
                int(duration * 0.5),
                int(duration * 0.75)
            ]
        
        # Limit number of mid-rolls
        max_mid_rolls = min(self.max_mid_rolls_per_10min, int(duration / 600))
        positions = positions[:max_mid_rolls]
        
        return positions

    def _calculate_position_cpm(self, 
                              position: int,
                              duration: int,
                              engagement_score: float,
                              base_cpm: float,
                              is_kids_content: bool) -> float:
        """
        Calculate CPM for specific ad position
        """
        # Base CPM adjustment
        cpm = base_cpm
        
        # COPPA adjustment
        if is_kids_content:
            cpm *= self.coppa_cpm_adjustment
        
        # Position-based adjustment (early positions get higher CPM)
        position_ratio = position / duration
        if position_ratio < 0.3:
            cpm *= 1.2  # 20% bonus for early positions
        elif position_ratio > 0.7:
            cpm *= 0.8  # 20% penalty for late positions
        
        # Engagement-based adjustment
        cpm *= (0.8 + engagement_score * 0.4)  # 0.8x to 1.2x based on engagement
        
        return round(cpm, 2)

    def _calculate_retention_impact(self, 
                                  position: int,
                                  duration: int,
                                  engagement_score: float) -> float:
        """
        Calculate retention impact of ad at specific position
        """
        # Base retention loss
        base_impact = 0.05  # 5% base retention loss per ad
        
        # Position-based adjustment
        position_ratio = position / duration
        if position_ratio < 0.2:
            base_impact *= 1.5  # Higher impact early in video
        elif position_ratio > 0.8:
            base_impact *= 0.5  # Lower impact near end
        
        # Engagement-based adjustment (high engagement reduces impact)
        base_impact *= (1.5 - engagement_score)
        
        return round(base_impact, 3)

    async def coppa_compliance_check(self, video_metadata: Dict) -> Dict:
        """
        COPPA compliance checker and automatic adjustments
        """
        is_made_for_kids = video_metadata.get('made_for_kids', False)
        
        if is_made_for_kids:
            # COPPA compliance adjustments
            compliance_actions = {
                "disable_targeted_ads": True,
                "disable_personalized_ads": True,
                "disable_data_collection": True,
                "enable_content_ratings": True,
                "adjust_metadata": True,
                "monetization_strategy": "brand_deals"
            }
            
            # Adjust tags for COPPA compliance
            forbidden_tags = ["adult", "mature", "violence", "inappropriate"]
            tags = video_metadata.get('tags', [])
            compliant_tags = [tag for tag in tags if not any(forbidden in tag.lower() for forbidden in forbidden_tags)]
            
            # Generate kid-friendly description
            description = video_metadata.get('description', '')
            if description:
                # Remove any potentially inappropriate content
                description = self._sanitize_description_for_kids(description)
            
            # Update metadata
            updated_metadata = video_metadata.copy()
            updated_metadata.update({
                "tags": compliant_tags,
                "description": description,
                "compliance_actions": compliance_actions,
                "cpm_adjustment": self.coppa_cpm_adjustment,
                "monetization_notes": "Brand deals and merch links recommended for COPPA compliance"
            })
            
            return updated_metadata
        
        return video_metadata

    def _sanitize_description_for_kids(self, description: str) -> str:
        """
        Sanitize description for kids content
        """
        # Remove potentially inappropriate content
        inappropriate_patterns = [
            r'http[s]?://[^\s]+',  # URLs
            r'\b(adult|mature|violence|inappropriate)\b',  # Inappropriate words
            r'@[^\s]+',  # Social media handles
            r'#\w+',  # Hashtags (except approved ones)
        ]
        
        sanitized = description
        for pattern in inappropriate_patterns:
            sanitized = re.sub(pattern, '', sanitized, flags=re.IGNORECASE)
        
        # Add kid-friendly disclaimer
        sanitized += "\n\n👨‍👩‍👧‍👦 Family-friendly content suitable for all ages!"
        
        return sanitized.strip()

    async def generate_ad_revenue_projection(self, 
                                           ad_slots: List[AdSlot],
                                           expected_views: int,
                                           duration: int) -> Dict:
        """
        Generate revenue projection for ad slots
        """
        total_revenue = 0
        slot_projections = []
        
        for slot in ad_slots:
            # Calculate expected ad impressions
            if slot.ad_type == "pre_roll":
                impression_rate = 0.95  # 95% of viewers see pre-roll
            elif slot.ad_type == "mid_roll":
                # Calculate retention at this position
                retention_at_position = 1.0 - (slot.position_seconds / duration) * 0.3  # 30% total drop-off
                retention_at_position *= (1 - slot.retention_impact)  # Account for ad impact
                impression_rate = max(0.1, retention_at_position)
            else:  # post_roll
                impression_rate = 0.3  # 30% of viewers watch to end
            
            impressions = expected_views * impression_rate
            revenue = (impressions / 1000) * slot.predicted_cpm
            
            slot_projections.append({
                "ad_type": slot.ad_type,
                "position_seconds": slot.position_seconds,
                "impression_rate": impression_rate,
                "expected_impressions": int(impressions),
                "cpm": slot.predicted_cpm,
                "projected_revenue": round(revenue, 2),
                "retention_impact": slot.retention_impact
            })
            
            total_revenue += revenue
        
        return {
            "total_projected_revenue": round(total_revenue, 2),
            "total_expected_impressions": sum(p["expected_impressions"] for p in slot_projections),
            "average_cpm": round(sum(p["cpm"] for p in slot_projections) / len(slot_projections), 2),
            "slot_projections": slot_projections,
            "revenue_per_1000_views": round((total_revenue / expected_views) * 1000, 2) if expected_views > 0 else 0
        }

    async def optimize_for_maximum_revenue(self, 
                                          script: str,
                                          duration: int,
                                          target_views: int,
                                          is_kids_content: bool = False) -> Dict:
        """
        Complete optimization for maximum revenue
        """
        # Generate ad slots
        ad_slots = await self.optimize_ad_slots(script, duration, is_kids_content)
        
        # Generate revenue projection
        revenue_projection = await self.generate_ad_revenue_projection(
            ad_slots, target_views, duration
        )
        
        # Generate optimization recommendations
        recommendations = self._generate_optimization_recommendations(
            ad_slots, revenue_projection, is_kids_content
        )
        
        return {
            "ad_slots": [
                {
                    "position_seconds": slot.position_seconds,
                    "ad_type": slot.ad_type,
                    "predicted_cpm": slot.predicted_cpm,
                    "retention_impact": slot.retention_impact,
                    "engagement_score": slot.engagement_score
                }
                for slot in ad_slots
            ],
            "revenue_projection": revenue_projection,
            "recommendations": recommendations,
            "coppa_compliant": is_kids_content,
            "optimization_timestamp": datetime.now().isoformat()
        }

    def _generate_optimization_recommendations(self, 
                                            ad_slots: List[AdSlot],
                                            revenue_projection: Dict,
                                            is_kids_content: bool) -> List[str]:
        """
        Generate optimization recommendations
        """
        recommendations = []
        
        total_revenue = revenue_projection["total_projected_revenue"]
        avg_cpm = revenue_projection["average_cpm"]
        total_retention_impact = sum(slot.retention_impact for slot in ad_slots if slot.ad_type != "post_roll")
        
        if is_kids_content:
            recommendations.append("COPPA compliance active: Lower CPM expected but brand-safe")
            recommendations.append("Focus on brand deals and merch links for additional revenue")
        
        if total_retention_impact > 0.15:
            recommendations.append("High retention impact detected: Consider reducing mid-roll frequency")
        
        if avg_cpm < 2.0:
            recommendations.append("Low CPM detected: Improve content quality or target different demographics")
        
        if len([slot for slot in ad_slots if slot.ad_type == "mid_roll"]) < 2 and len(ad_slots) > 3:
            recommendations.append("Consider adding more mid-roll slots for better monetization")
        
        if total_revenue > 100:
            recommendations.append("Strong revenue potential: Ensure content quality maintains viewer retention")
        
        return recommendations
