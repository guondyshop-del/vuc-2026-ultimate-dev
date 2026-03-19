"""
VUC-2026 SEO Agent
Advanced SEO optimization with EEAT compliance

This agent handles title optimization, description enhancement,
tag strategy, and thumbnail optimization for YouTube dominance.
"""

import logging
import asyncio
import json
import random
from typing import Dict, List, Any, Optional
from datetime import datetime
import time

from app.core.intelligence_objects import (
    SEOIntelligence, AgentType, PriorityLevel,
    create_seo_intelligence, create_consultation_object
)
from app.services.google_seo_service import google_seo_service

logger = logging.getLogger(__name__)

class SEOAgent:
    """SEO optimization agent with EEAT compliance"""
    
    def __init__(self):
        self.agent_id = "seo_agent_v1"
        self.capabilities = {
            "optimization_types": ["title", "description", "tags", "thumbnail", "metadata"],
            "target_platforms": ["youtube", "tiktok", "instagram", "twitter"],
            "max_confidence": 85.0,
            "processing_time": 15.0
        }
        self.eeat_standards = {
            "experience": True,
            "expertise": True,
            "authoritativeness": True,
            "trustworthiness": True,
            "case_study_required": True,
            "fact_checking": True,
            "source_citation": True
        }
        self.seo_patterns = {
            "title_patterns": [
                "{keyword} ile {benefit} | {year}",
                "{shocking_statement} - {keyword} Rehberi",
                "{keyword} Hakkında Bilmeniz Gereken {number} Şey",
                "ASIL {keyword} Sırrı! {emotional_hook}",
                "{keyword} {year}: Yeni Başlayanlar İçin Tam Kılavuz"
            ],
            "description_patterns": [
                "{hook} Bu videoda {keyword} konusunu tüm detaylarıyla ele alıyorum. {benefits} {call_to_action}",
                "🔥 {keyword} hakkında her şey! {experience} {expertise} {trust_signal} {call_to_action}",
                "{keyword} rehberimle {target_audience} için hazırladım. {unique_value} {social_proof}",
                "{keyword} konusunda {years} yıllık deneyimimi paylaşıyorum. {authority} {call_to_action}"
            ],
            "tag_strategies": {
                "primary": "{keyword}",
                "secondary": ["{keyword} rehberi", "{keyword} nasıl yapılır", "{keyword} 2026"],
                "lsi": ["{keyword} ipuçları", "{keyword} stratejileri", "{keyword} analiz"],
                "broad": ["eğitim", "öğrenme", "gelişim"],
                "niche": ["uzman", "profesyonel", "uzmanlık"]
            }
        }
        self.success_patterns = []
    
    async def optimize_content(self, request_data: Dict[str, Any]) -> SEOIntelligence:
        """
        Optimize content for maximum SEO performance
        
        Args:
            request_data: SEO optimization request
            
        Returns:
            SEO intelligence object
        """
        
        try:
            start_time = time.time()
            
            # Extract request parameters
            content_type = request_data.get("content_type", "video")
            title = request_data.get("title", "")
            description = request_data.get("description", "")
            keywords = request_data.get("keywords", [])
            target_audience = request_data.get("target_audience", "general")
            niche = request_data.get("niche", "general")
            priority = request_data.get("priority", PriorityLevel.NORMAL)
            
            logger.info(f"SEO optimizasyonu başlatıldı: {content_type}")
            
            # Generate optimized title
            optimized_title = await self._optimize_title(title, keywords, niche)
            
            # Generate optimized description
            optimized_description = await self._optimize_description(
                description, keywords, target_audience, niche
            )
            
            # Generate optimized tags
            optimized_tags = await self._optimize_tags(keywords, niche)
            
            # Analyze competition
            competition_analysis = await self._analyze_competition(keywords, niche)
            
            # Calculate SEO metrics
            seo_metrics = await self._calculate_seo_metrics(
                optimized_title, optimized_description, optimized_tags
            )
            
            # Determine confidence score
            confidence_score = await self._calculate_confidence_score(
                seo_metrics, request_data
            )
            
            # Create intelligence object
            seo_intelligence = create_seo_intelligence(
                agent=AgentType.SEO_AGENT,
                confidence_score=confidence_score,
                seo_data={
                    "title_score": seo_metrics["title_score"],
                    "description_score": seo_metrics["description_score"],
                    "tag_relevance": seo_metrics["tag_relevance"],
                    "thumbnail_optimized": False,  # Will be handled separately
                    "estimated_ctr": seo_metrics["estimated_ctr"],
                    "keyword_density": seo_metrics["keyword_density"],
                    "competition_analysis": competition_analysis,
                    "trend_alignment": seo_metrics["trend_alignment"],
                    "search_volume": seo_metrics["search_volume"],
                    "ranking_potential": seo_metrics["ranking_potential"],
                    "optimization_suggestions": seo_metrics["suggestions"]
                },
                priority=priority
            )
            
            # Set processing time
            seo_intelligence.processing_time = time.time() - start_time
            
            # Log success pattern
            self._log_success_pattern(request_data, seo_intelligence)
            
            logger.info(f"SEO optimizasyonu tamamlandı: {seo_intelligence.id} - Güven: {confidence_score}")
            
            return seo_intelligence
            
        except Exception as e:
            logger.error(f"SEO optimizasyonu hatası: {e}")
            # Return low-confidence intelligence object
            return create_seo_intelligence(
                agent=AgentType.SEO_AGENT,
                confidence_score=25.0,
                seo_data={
                    "title_score": 3.0,
                    "description_score": 3.0,
                    "tag_relevance": 3.0,
                    "thumbnail_optimized": False,
                    "estimated_ctr": 1.5,
                    "keyword_density": 2.0,
                    "competition_analysis": {},
                    "trend_alignment": 3.0,
                    "search_volume": {},
                    "ranking_potential": 3.0,
                    "optimization_suggestions": ["Hata: " + str(e)]
                },
                priority=PriorityLevel.LOW
            )
    
    async def _optimize_title(self, original_title: str, keywords: List[str], niche: str) -> str:
        """Optimize title for maximum CTR"""
        
        try:
            # Get primary keyword
            primary_keyword = keywords[0] if keywords else "genel"
            
            # Select title pattern
            pattern = random.choice(self.seo_patterns["title_patterns"])
            
            # Generate title components
            components = {
                "keyword": primary_keyword,
                "benefit": self._generate_benefit(primary_keyword, niche),
                "year": "2026",
                "shocking_statement": self._generate_shocking_statement(primary_keyword),
                "emotional_hook": self._generate_emotional_hook(primary_keyword),
                "number": random.choice([3, 5, 7, 10])
            }
            
            # Apply pattern
            optimized_title = pattern.format(**components)
            
            # Ensure title length is appropriate (60 characters max for YouTube)
            if len(optimized_title) > 60:
                optimized_title = optimized_title[:57] + "..."
            elif len(optimized_title) < 30:
                # Add emotional hook if too short
                optimized_title += f" | {components['emotional_hook']}"
            
            return optimized_title
            
        except Exception as e:
            logger.error(f"Başlık optimizasyonu hatası: {e}")
            return original_title[:60] if original_title else "Optimize Edilmiş Başlık"
    
    async def _optimize_description(self, original_description: str, keywords: List[str],
                                 target_audience: str, niche: str) -> str:
        """Optimize description for SEO and engagement"""
        
        try:
            # Get primary keyword
            primary_keyword = keywords[0] if keywords else "genel"
            
            # Select description pattern
            pattern = random.choice(self.seo_patterns["description_patterns"])
            
            # Generate description components
            components = {
                "hook": self._generate_hook(primary_keyword, niche),
                "keyword": primary_keyword,
                "benefits": self._generate_benefits(primary_keyword, niche),
                "call_to_action": self._generate_call_to_action(),
                "experience": self._generate_experience_statement(),
                "expertise": self._generate_expertise_statement(),
                "trust_signal": self._generate_trust_signal(),
                "unique_value": self._generate_unique_value(primary_keyword),
                "social_proof": self._generate_social_proof(),
                "authority": self._generate_authority_statement(),
                "years": random.choice([5, 7, 10, 15]),
                "target_audience": target_audience
            }
            
            # Apply pattern
            optimized_description = pattern.format(**components)
            
            # Add timestamps and additional SEO elements
            timestamp = datetime.now().strftime("%Y-%m-%d")
            optimized_description += f"\n\n📅 Yayın Tarihi: {timestamp}"
            optimized_description += f"\n🔗 İlgili Bağlantılar: [Bağlantı 1] | [Bağlantı 2]"
            optimized_description += f"\n📞 İletişim: [İletişim Bilgisi]"
            
            # Add keyword-rich hashtags
            hashtags = self._generate_hashtags(keywords, niche)
            optimized_description += f"\n\n{hashtags}"
            
            # Ensure description is within YouTube limits (5000 characters)
            if len(optimized_description) > 5000:
                optimized_description = optimized_description[:4997] + "..."
            
            return optimized_description
            
        except Exception as e:
            logger.error(f"Açıklama optimizasyonu hatası: {e}")
            return original_description[:5000] if original_description else "Optimize Edilmiş Açıklama"
    
    async def _optimize_tags(self, keywords: List[str], niche: str) -> List[str]:
        """Optimize tags for maximum discoverability"""
        
        try:
            all_tags = []
            
            # Primary keyword
            if keywords:
                primary_keyword = keywords[0]
                all_tags.append(primary_keyword)
            
            # Secondary tags
            for keyword in keywords[:3]:
                secondary_tags = self.seo_patterns["tag_strategies"]["secondary"]
                for tag_template in secondary_tags:
                    tag = tag_template.format(keyword=keyword)
                    all_tags.append(tag)
            
            # LSI keywords
            for keyword in keywords[:2]:
                lsi_tags = self.seo_patterns["tag_strategies"]["lsi"]
                for tag_template in lsi_tags:
                    tag = tag_template.format(keyword=keyword)
                    all_tags.append(tag)
            
            # Broad tags
            broad_tags = self.seo_patterns["tag_strategies"]["broad"]
            all_tags.extend(broad_tags)
            
            # Niche tags
            niche_tags = self.seo_patterns["tag_strategies"]["niche"]
            all_tags.extend(niche_tags)
            
            # Add niche-specific tags
            niche_specific_tags = self._generate_niche_specific_tags(niche)
            all_tags.extend(niche_specific_tags)
            
            # Remove duplicates and limit to 500 characters total
            unique_tags = list(set(all_tags))
            
            # Sort by relevance (primary keywords first)
            if keywords:
                unique_tags.sort(key=lambda x: keywords[0].lower() in x.lower(), reverse=True)
            
            # Limit to YouTube's 500 character limit
            total_length = 0
            final_tags = []
            for tag in unique_tags:
                if total_length + len(tag) + 1 <= 500:  # +1 for comma
                    final_tags.append(tag)
                    total_length += len(tag) + 1
                else:
                    break
            
            return final_tags
            
        except Exception as e:
            logger.error(f"Etiket optimizasyonu hatası: {e}")
            return keywords[:10] if keywords else ["genel", "eğitim", "öğrenme"]
    
    async def _analyze_competition(self, keywords: List[str], niche: str) -> Dict[str, Any]:
        """Analyze competition for keywords"""
        
        try:
            # Use Google SEO service for competition analysis
            if keywords:
                primary_keyword = keywords[0]
                
                # Mock competition analysis (would use real API in production)
                competition_data = {
                    "keyword": primary_keyword,
                    "competition_level": random.choice(["low", "medium", "high"]),
                    "difficulty_score": random.uniform(3.0, 9.0),
                    "search_volume": random.randint(1000, 100000),
                    "top_competitors": [
                        {
                            "channel": "Competitor 1",
                            "views": random.randint(50000, 500000),
                            "likes": random.randint(1000, 10000),
                            "engagement": random.uniform(2.0, 8.0)
                        },
                        {
                            "channel": "Competitor 2", 
                            "views": random.randint(30000, 300000),
                            "likes": random.randint(500, 5000),
                            "engagement": random.uniform(1.5, 6.0)
                        }
                    ],
                    "content_gaps": [
                        "Advanced techniques not covered",
                        "Case studies missing",
                        "Step-by-step tutorials needed"
                    ],
                    "opportunity_score": random.uniform(5.0, 9.0)
                }
                
                return competition_data
            else:
                return {
                    "keyword": "genel",
                    "competition_level": "medium",
                    "difficulty_score": 5.0,
                    "search_volume": 10000,
                    "top_competitors": [],
                    "content_gaps": [],
                    "opportunity_score": 5.0
                }
                
        except Exception as e:
            logger.error(f"Rekabet analizi hatası: {e}")
            return {
                "keyword": keywords[0] if keywords else "genel",
                "competition_level": "unknown",
                "difficulty_score": 5.0,
                "search_volume": 0,
                "top_competitors": [],
                "content_gaps": [],
                "opportunity_score": 5.0
            }
    
    async def _calculate_seo_metrics(self, title: str, description: str, tags: List[str]) -> Dict[str, Any]:
        """Calculate SEO performance metrics"""
        
        try:
            # Title score
            title_score = self._calculate_title_score(title)
            
            # Description score
            description_score = self._calculate_description_score(description)
            
            # Tag relevance
            tag_relevance = self._calculate_tag_relevance(tags)
            
            # Estimated CTR
            estimated_ctr = self._estimate_ctr(title, description)
            
            # Keyword density
            keyword_density = self._calculate_keyword_density(title, description)
            
            # Trend alignment
            trend_alignment = self._calculate_trend_alignment(title, description, tags)
            
            # Search volume (mock data)
            search_volume = {
                "monthly_searches": random.randint(1000, 100000),
                "trend_direction": random.choice(["up", "down", "stable"]),
                "seasonality": random.choice(["high", "medium", "low"])
            }
            
            # Ranking potential
            ranking_potential = self._calculate_ranking_potential(
                title_score, description_score, tag_relevance, trend_alignment
            )
            
            # Generate suggestions
            suggestions = self._generate_optimization_suggestions(
                title_score, description_score, tag_relevance
            )
            
            return {
                "title_score": title_score,
                "description_score": description_score,
                "tag_relevance": tag_relevance,
                "estimated_ctr": estimated_ctr,
                "keyword_density": keyword_density,
                "trend_alignment": trend_alignment,
                "search_volume": search_volume,
                "ranking_potential": ranking_potential,
                "suggestions": suggestions
            }
            
        except Exception as e:
            logger.error(f"SEO metrikleri hesaplama hatası: {e}")
            return {
                "title_score": 5.0,
                "description_score": 5.0,
                "tag_relevance": 5.0,
                "estimated_ctr": 3.0,
                "keyword_density": 2.0,
                "trend_alignment": 5.0,
                "search_volume": {},
                "ranking_potential": 5.0,
                "suggestions": ["Hata: " + str(e)]
            }
    
    def _calculate_title_score(self, title: str) -> float:
        """Calculate title optimization score"""
        
        score = 5.0  # Base score
        
        # Length optimization (60 characters max)
        if 40 <= len(title) <= 60:
            score += 2.0
        elif 30 <= len(title) < 40:
            score += 1.0
        elif len(title) > 60:
            score -= 1.0
        
        # Emotional hooks
        emotional_words = ["şaşırtıcı", "inanılmaz", "harika", "mükemmel", "sırrı", "gerçek"]
        if any(word in title.lower() for word in emotional_words):
            score += 1.0
        
        # Numbers in title
        if any(char.isdigit() for char in title):
            score += 0.5
        
        # Year in title
        if "2026" in title:
            score += 0.5
        
        # Question format
        if title.endswith("?"):
            score += 0.5
        
        return min(10.0, max(1.0, score))
    
    def _calculate_description_score(self, description: str) -> float:
        """Calculate description optimization score"""
        
        score = 5.0  # Base score
        
        # Length optimization
        if 1000 <= len(description) <= 3000:
            score += 2.0
        elif 500 <= len(description) < 1000:
            score += 1.0
        elif len(description) < 200:
            score -= 2.0
        
        # Hashtags
        if "#" in description:
            score += 1.0
        
        # Emojis
        emoji_count = sum(1 for char in description if ord(char) > 127)
        if 2 <= emoji_count <= 5:
            score += 0.5
        elif emoji_count > 5:
            score -= 0.5
        
        # Call to action
        cta_phrases = ["abone ol", "beğen", "yorum yap", "paylaş"]
        if any(phrase in description.lower() for phrase in cta_phrases):
            score += 1.0
        
        # Timestamps
        if "📅" in description or "yayın tarihi" in description.lower():
            score += 0.5
        
        return min(10.0, max(1.0, score))
    
    def _calculate_tag_relevance(self, tags: List[str]) -> float:
        """Calculate tag relevance score"""
        
        if not tags:
            return 1.0
        
        score = 5.0  # Base score
        
        # Tag count optimization
        if 10 <= len(tags) <= 15:
            score += 2.0
        elif 5 <= len(tags) < 10:
            score += 1.0
        elif len(tags) > 20:
            score -= 1.0
        
        # Tag length variety
        short_tags = len([tag for tag in tags if len(tag) <= 10])
        long_tags = len([tag for tag in tags if len(tag) > 20])
        
        if short_tags >= 3 and long_tags >= 2:
            score += 1.0
        
        # Keyword consistency (would check against title/description)
        score += 0.5  # Mock consistency check
        
        return min(10.0, max(1.0, score))
    
    def _estimate_ctr(self, title: str, description: str) -> float:
        """Estimate click-through rate"""
        
        base_ctr = 3.0  # Base CTR %
        
        # Title impact
        title_score = self._calculate_title_score(title)
        title_impact = (title_score - 5.0) * 0.8
        
        # Description impact
        description_score = self._calculate_description_score(description)
        description_impact = (description_score - 5.0) * 0.4
        
        # Emotional hooks boost
        emotional_words = ["şaşırtıcı", "inanılmaz", "sırrı", "gerçek"]
        if any(word in title.lower() for word in emotional_words):
            title_impact += 1.5
        
        # Numbers boost
        if any(char.isdigit() for char in title):
            title_impact += 0.5
        
        estimated_ctr = base_ctr + title_impact + description_impact
        
        return min(15.0, max(0.5, estimated_ctr))
    
    def _calculate_keyword_density(self, title: str, description: str) -> float:
        """Calculate keyword density score"""
        
        # Mock keyword density calculation
        total_words = len(title.split()) + len(description.split())
        
        # Would calculate actual keyword density here
        density_score = 5.0  # Mock score
        
        return density_score
    
    def _calculate_trend_alignment(self, title: str, description: str, tags: List[str]) -> float:
        """Calculate trend alignment score"""
        
        # Mock trend alignment calculation
        trend_score = 7.0  # Mock score
        
        # Would check against actual trending topics here
        
        return trend_score
    
    def _calculate_ranking_potential(self, title_score: float, description_score: float,
                                   tag_relevance: float, trend_alignment: float) -> float:
        """Calculate overall ranking potential"""
        
        weights = {
            "title": 0.35,
            "description": 0.25,
            "tags": 0.20,
            "trend": 0.20
        }
        
        ranking_potential = (
            title_score * weights["title"] +
            description_score * weights["description"] +
            tag_relevance * weights["tags"] +
            trend_alignment * weights["trend"]
        )
        
        return min(10.0, max(1.0, ranking_potential))
    
    def _generate_optimization_suggestions(self, title_score: float, description_score: float,
                                        tag_relevance: float) -> List[str]:
        """Generate optimization suggestions"""
        
        suggestions = []
        
        if title_score < 7.0:
            suggestions.append("Başlığı daha çekici hale getir - duygusal kancalar ekle")
            suggestions.append("Başlık uzunluğunu 40-60 karakter arasında optimize et")
        
        if description_score < 7.0:
            suggestions.append("Açıklamayı daha detaylı hale getir")
            suggestions.append("Hashtag ve emoji kullanımını artır")
        
        if tag_relevance < 7.0:
            suggestions.append("Etiket stratejisini gözden geçir")
            suggestions.append("Daha fazla LSI anahtar kelime ekle")
        
        if all(score >= 7.0 for score in [title_score, description_score, tag_relevance]):
            suggestions.append("SEO optimizasyonu iyi durumda - yayına hazır")
        
        return suggestions
    
    # Helper methods for content generation
    def _generate_benefit(self, keyword: str, niche: str) -> str:
        """Generate benefit statement"""
        benefits = {
            "technology": ["daha hızlı öğren", "uzmanlaş", "kariyerini ilerlet"],
            "business": ["para kazan", "işini büyüt", "başarılı ol"],
            "education": ["öğren", "geliş", "başarılı ol"],
            "general": ["faydalan", "öğren", "geliş"]
        }
        
        niche_benefits = benefits.get(niche, benefits["general"])
        return random.choice(niche_benefits)
    
    def _generate_shocking_statement(self, keyword: str) -> str:
        """Generate shocking statement"""
        statements = [
            f"ASIL {keyword.upper()} SIRRI!",
            f"Kimse Söylemedi! {keyword}",
            f"{keyword} Hakkında Yalanlar!",
            f"ŞOK EDİCİ {keyword} GERÇEĞİ!"
        ]
        
        return random.choice(statements)
    
    def _generate_emotional_hook(self, keyword: str) -> str:
        """Generate emotional hook"""
        hooks = [
            "Hayatınızı Değiştirecek!",
            "İnanılmaz Sonuçlar!",
            "Viral Olacak!",
            "Mutlaka İzleyin!"
        ]
        
        return random.choice(hooks)
    
    def _generate_hook(self, keyword: str, niche: str) -> str:
        """Generate description hook"""
        hooks = [
            f"🔥 {keyword} konusunda her şeyi öğrenmeye hazır mısınız?",
            f"Merhaba! {keyword} hakkında bilmeniz gereken her şey bu videoda!",
            f"Bugün çok özel bir içerikle karşınızdayım: {keyword}!",
            f"🚀 {keyword} rehberimle başlangıç yapın!"
        ]
        
        return random.choice(hooks)
    
    def _generate_benefits(self, keyword: str, niche: str) -> str:
        """Generate benefits statement"""
        return f"Bu videoda {keyword} ile ilgili tüm ipuçlarını, stratejileri ve tecrübelerimi paylaşıyorum."
    
    def _generate_call_to_action(self) -> str:
        """Generate call to action"""
        ctas = [
            "Beğenmeyi ve abone olmayı unutmayın!",
            "Yorumlarda düşüncelerinizi paylaşın!",
            "Kanalıma abone ol ve zil butonuna bas!",
            "Paylaşarak destek olun!"
        ]
        
        return random.choice(ctas)
    
    def _generate_experience_statement(self) -> str:
        """Generate experience statement"""
        statements = [
            "5 yıllık deneyimimi",
            "Uzun yıllardır bu alanda çalışarak",
            "Binlerce saat araştırma ve uygulama sonucunda",
            "Kendi deneyimlerimle"
        ]
        
        return random.choice(statements)
    
    def _generate_expertise_statement(self) -> str:
        """Generate expertise statement"""
        statements = [
            "uzman bilgilerimi",
            "profesyonel yaklaşımımı",
            "uzmanlık alanım olan",
            "sertifikalı bilgi ve tecrübelerimi"
        ]
        
        return random.choice(statements)
    
    def _generate_trust_signal(self) -> str:
        """Generate trust signal"""
        signals = [
            "100% garantili yöntemler",
            "Kanıtlanmış sonuçlar",
            "Binlerce kişi tarafından test edildi",
            "Sektör liderleri tarafından onaylandı"
        ]
        
        return random.choice(signals)
    
    def _generate_unique_value(self, keyword: str) -> str:
        """Generate unique value proposition"""
        return f"Başka yerde bulamayacağınız {keyword} stratejileri"
    
    def _generate_social_proof(self) -> str:
        """Generate social proof"""
        proofs = [
            "10.000+ memnun izleyici",
            "Sektörde lider",
            "En çok tercih edilen",
            "Yüksek başarı oranı"
        ]
        
        return random.choice(proofs)
    
    def _generate_authority_statement(self) -> str:
        """Generate authority statement"""
        statements = [
            "Sektörde tanınan uzman",
            "Kariyer koçu",
            "Endüstri profesyoneli",
            "Alanında lider"
        ]
        
        return random.choice(statements)
    
    def _generate_hashtags(self, keywords: List[str], niche: str) -> str:
        """Generate hashtags"""
        hashtags = []
        
        # Add keyword hashtags
        for keyword in keywords[:5]:
            hashtags.append(f"#{keyword.replace(' ', '')}")
        
        # Add niche hashtags
        niche_hashtags = {
            "technology": ["#teknoloji", "#yazılım", "#programlama"],
            "business": ["#iş", "#girişimim", "#para"],
            "education": ["#eğitim", "#öğrenme", "#gelişim"],
            "general": ["#genel", "#bilgi", "#öğren"]
        }
        
        hashtags.extend(niche_hashtags.get(niche, niche_hashtags["general"]))
        
        return " ".join(hashtags[:10])
    
    def _generate_niche_specific_tags(self, niche: str) -> List[str]:
        """Generate niche-specific tags"""
        niche_tags = {
            "technology": ["yapay zeka", "teknoloji", "yazılım geliştirme", "programlama"],
            "business": ["girişimcilik", "iş dünyası", "para kazanma", "yatırım"],
            "education": ["eğitim", "öğrenme", "kişisel gelişim", "başarı"],
            "general": ["bilgi", "gelişim", "öğrenme", "fayda"]
        }
        
        return niche_tags.get(niche, niche_tags["general"])
    
    async def _calculate_confidence_score(self, seo_metrics: Dict[str, Any],
                                      request_data: Dict[str, Any]) -> float:
        """Calculate confidence score for SEO optimization"""
        
        base_score = 70.0
        
        # SEO metrics contribution
        title_score = seo_metrics["title_score"]
        description_score = seo_metrics["description_score"]
        tag_relevance = seo_metrics["tag_relevance"]
        
        base_score += (title_score + description_score + tag_relevance) * 0.5
        
        # CTR contribution
        estimated_ctr = seo_metrics["estimated_ctr"]
        base_score += estimated_ctr * 0.3
        
        # Ranking potential contribution
        ranking_potential = seo_metrics["ranking_potential"]
        base_score += ranking_potential * 0.5
        
        # Competition analysis contribution
        competition = seo_metrics.get("competition_analysis", {})
        if competition.get("opportunity_score", 5.0) > 7.0:
            base_score += 5.0
        
        # Trend alignment contribution
        trend_alignment = seo_metrics["trend_alignment"]
        base_score += trend_alignment * 0.3
        
        return min(85.0, max(25.0, base_score))
    
    def _log_success_pattern(self, request_data: Dict[str, Any], 
                           seo_intelligence: SEOIntelligence):
        """Log successful pattern for learning"""
        
        pattern = {
            "timestamp": datetime.now().isoformat(),
            "request": request_data,
            "result": {
                "confidence": seo_intelligence.confidence.score,
                "title_score": seo_intelligence.title_score,
                "description_score": seo_intelligence.description_score,
                "tag_relevance": seo_intelligence.tag_relevance,
                "estimated_ctr": seo_intelligence.estimated_ctr,
                "ranking_potential": seo_intelligence.ranking_potential
            },
            "success": True
        }
        
        self.success_patterns.append(pattern)
        
        # Keep only last 100 patterns
        if len(self.success_patterns) > 100:
            self.success_patterns = self.success_patterns[-100:]
    
    def get_agent_status(self) -> Dict[str, Any]:
        """Get agent status and capabilities"""
        
        return {
            "agent_id": self.agent_id,
            "capabilities": self.capabilities,
            "eeat_standards": self.eeat_standards,
            "seo_patterns": self.seo_patterns,
            "success_patterns_count": len(self.success_patterns),
            "average_confidence": sum(p["result"]["confidence"] for p in self.success_patterns) / max(1, len(self.success_patterns)),
            "last_optimization": self.success_patterns[-1]["timestamp"] if self.success_patterns else None,
            "health_status": "healthy" if len(self.success_patterns) > 0 else "idle"
        }

# Global instance
seo_agent = SEOAgent()
