"""
VUC-2026 Script Agent
AI-powered script generation with human-fluidity

This agent generates scripts with high perplexity and burstiness,
eliminating AI fingerprints while maintaining viral potential.
"""

import logging
import asyncio
import json
import random
from typing import Dict, List, Any, Optional
from datetime import datetime
import time

from app.core.intelligence_objects import (
    ScriptIntelligence, AgentType, PriorityLevel,
    create_script_intelligence, create_consultation_object
)
from app.services.enhanced_ai_service import enhanced_ai_service

logger = logging.getLogger(__name__)

class ScriptAgent:
    """Script generation agent with human-like creativity"""
    
    def __init__(self):
        self.agent_id = "script_agent_v1"
        self.capabilities = {
            "script_types": ["educational", "entertainment", "business", "gaming", "technology"],
            "tones": ["professional", "casual", "emotional", "humorous", "dramatic"],
            "styles": ["storytelling", "tutorial", "review", "reaction", "analysis"],
            "max_confidence": 95.0,
            "processing_time": 30.0
        }
        self.human_fluidity_patterns = {
            "conversation_fillers": ["hımm", "şey", "yani", "aslında", "biraz"],
            "typing_variations": ["...", "----", "///", "***"],
            "emotional_markers": ["😊", "😎", "🤔", "😂", "🔥"],
            "natural_pauses": [", ", "...", "---"],
            "contractions": ["'nın", "'nın", "'ki", "'mi", "'de"]
        }
        self.ai_bypass_techniques = {
            "perplexity_boost": True,
            "burstiness_variation": True,
            "fingerprint_elimination": True,
            "semantic_diversity": True,
            "contextual_adaptation": True
        }
        self.success_patterns = []
    
    async def generate_script(self, request_data: Dict[str, Any]) -> ScriptIntelligence:
        """
        Generate script with human-like characteristics
        
        Args:
            request_data: Script generation request
            
        Returns:
            Script intelligence object
        """
        
        try:
            start_time = time.time()
            
            # Extract request parameters
            topic = request_data.get("topic", "")
            script_type = request_data.get("script_type", "educational")
            tone = request_data.get("tone", "professional")
            target_audience = request_data.get("target_audience", "general")
            duration_target = request_data.get("duration_target", 300)
            seo_keywords = request_data.get("seo_keywords", [])
            priority = request_data.get("priority", PriorityLevel.NORMAL)
            
            logger.info(f"Senaryo üretimi başlatıldı: {topic}")
            
            # Generate base script using AI
            base_script = await self._generate_base_script(
                topic, script_type, tone, target_audience, duration_target, seo_keywords
            )
            
            # Apply human-fluidity techniques
            humanized_script = await self._apply_human_fluidity(base_script)
            
            # Apply AI bypass techniques
            bypass_script = await self._apply_ai_bypass(humanized_script)
            
            # Calculate script metrics
            script_metrics = await self._calculate_script_metrics(bypass_script)
            
            # Determine confidence score
            confidence_score = await self._calculate_confidence_score(
                script_metrics, request_data
            )
            
            # Create intelligence object
            script_intelligence = create_script_intelligence(
                agent=AgentType.SCRIPT_AGENT,
                confidence_score=confidence_score,
                script_data={
                    "type": script_type,
                    "content": bypass_script,
                    "word_count": script_metrics["word_count"],
                    "seo_keywords": seo_keywords,
                    "hook_strength": script_metrics["hook_strength"],
                    "viral_potential": script_metrics["viral_potential"],
                    "emotional_tone": tone,
                    "target_audience": target_audience,
                    "content_pillar": self._determine_content_pillar(topic),
                    "estimated_duration": script_metrics["estimated_duration"],
                    "script_structure": script_metrics["structure"],
                    "engagement_hooks": script_metrics["engagement_hooks"]
                },
                priority=priority
            )
            
            # Set processing time
            script_intelligence.processing_time = time.time() - start_time
            
            # Log success pattern
            self._log_success_pattern(request_data, script_intelligence)
            
            logger.info(f"Senaryo üretildi: {script_intelligence.id} - Güven: {confidence_score}")
            
            return script_intelligence
            
        except Exception as e:
            logger.error(f"Senaryo üretim hatası: {e}")
            # Return low-confidence intelligence object
            return create_script_intelligence(
                agent=AgentType.SCRIPT_AGENT,
                confidence_score=25.0,
                script_data={
                    "type": request_data.get("script_type", "educational"),
                    "content": f"Hata: {str(e)}",
                    "word_count": 0,
                    "seo_keywords": [],
                    "hook_strength": 1.0,
                    "viral_potential": 1.0,
                    "emotional_tone": "error",
                    "target_audience": "unknown",
                    "content_pillar": "error",
                    "estimated_duration": 0,
                    "script_structure": {},
                    "engagement_hooks": []
                },
                priority=PriorityLevel.LOW
            )
    
    async def _generate_base_script(self, topic: str, script_type: str, tone: str,
                                target_audience: str, duration_target: int,
                                seo_keywords: List[str]) -> str:
        """Generate base script using enhanced AI service"""
        
        try:
            # Create prompt for script generation
            prompt = self._create_script_prompt(
                topic, script_type, tone, target_audience, duration_target, seo_keywords
            )
            
            # Generate script using enhanced AI service
            response = await enhanced_ai_service.generate_seo_script(
                topic=topic,
                target_keywords=seo_keywords,
                video_duration=duration_target,
                tone=tone
            )
            
            if response.get("success"):
                script_data = response.get("script", {})
                return script_data.get("content", "")
            else:
                # Fallback to basic generation
                return await self._fallback_script_generation(
                    topic, script_type, tone, duration_target
                )
                
        except Exception as e:
            logger.error(f"Temel senaryo üretim hatası: {e}")
            return await self._fallback_script_generation(
                topic, script_type, tone, duration_target
            )
    
    def _create_script_prompt(self, topic: str, script_type: str, tone: str,
                           target_audience: str, duration_target: int,
                           seo_keywords: List[str]) -> str:
        """Create detailed prompt for script generation"""
        
        word_count = int(duration_target / 2)  # 150 words per minute
        
        prompt = f"""
        Profesyonel senaryo yazarı olarak "{topic}" konusu için senaryo yaz.
        
        Senaryo Türü: {script_type}
        Ton: {tone}
        Hedef Kitle: {target_audience}
        Süre: {duration_target} saniye ({word_count} kelime)
        SEO Anahtar Kelimeler: {', '.join(seo_keywords)}
        
        YAPILACAKLAR:
        1. İnsan gibi doğal konuşma dili kullan
        2. Konuşma dolgularını (hımm, şey, yani) stratejik olarak yerleştir
        3. Duygusal ifadeler ve duraksamaları ekle
        4. İzleyici dikkatini çekecek güçlü kancalar oluştur
        5. SEO anahtar kelimelerini doğal olarak entegre et
        6. {script_type} formatına uygun yapı oluştur
        
        YAPISAL:
        - Giriş: İzleyiciyi yakalayan güçlü başlangıç
        - Ana İçerik: Değerli bilgiler ve hikaye anlatımı
        - Sonuç: Etkili çağrı ve özet
        
        İNSANLAŞTIRMA TEKNİKLERİ:
        - Konuşma varyasyonları ve ton değişimleri
        - Doğal duraksamalar ve düşünce anları
        - Duygusal dalgalanmalar
        - Kişisel dokunuşlar ve deneyimler
        
        LÜTFEN SADECE senaryo metnini ver, açıklama yapma.
        """
        
        return prompt
    
    async def _apply_human_fluidity(self, script: str) -> str:
        """Apply human-like fluidity patterns to script"""
        
        try:
            humanized_script = script
            
            # Add conversation fillers strategically
            if self.human_fluidity_patterns:
                humanized_script = self._add_conversation_fillers(humanized_script)
            
            # Add typing variations and pauses
            humanized_script = self._add_typing_variations(humanized_script)
            
            # Add emotional markers
            humanized_script = self._add_emotional_markers(humanized_script)
            
            # Add natural pauses
            humanized_script = self._add_natural_pauses(humanized_script)
            
            # Add contractions for natural speech
            humanized_script = self._add_contractions(humanized_script)
            
            return humanized_script
            
        except Exception as e:
            logger.error(f"İnsanlaştırma uygulama hatası: {e}")
            return script
    
    def _add_conversation_fillers(self, text: str) -> str:
        """Add strategic conversation fillers"""
        
        fillers = self.human_fluidity_patterns["conversation_fillers"]
        sentences = text.split('.')
        
        for i, sentence in enumerate(sentences):
            if len(sentence.strip()) > 50 and random.random() < 0.15:
                # Add filler to longer sentences
                filler = random.choice(fillers)
                words = sentence.split()
                if len(words) > 10:
                    insert_pos = random.randint(3, len(words) - 3)
                    words.insert(insert_pos, filler)
                    sentences[i] = ' '.join(words)
        
        return '. '.join(sentences)
    
    def _add_typing_variations(self, text: str) -> str:
        """Add typing variations and corrections"""
        
        variations = self.human_fluidity_patterns["typing_variations"]
        
        # Add occasional typing variations
        if random.random() < 0.1:
            words = text.split()
            if len(words) > 20:
                insert_pos = random.randint(10, len(words) - 5)
                words.insert(insert_pos, random.choice(variations))
                text = ' '.join(words)
        
        return text
    
    def _add_emotional_markers(self, text: str) -> str:
        """Add emotional markers"""
        
        markers = self.human_fluidity_patterns["emotional_markers"]
        
        # Add emotional markers at strategic points
        sentences = text.split('.')
        
        for i, sentence in enumerate(sentences):
            if len(sentence.strip()) > 30 and random.random() < 0.2:
                marker = random.choice(markers)
                sentences[i] = sentence.strip() + f" {marker}"
        
        return '. '.join(sentences)
    
    def _add_natural_pauses(self, text: str) -> str:
        """Add natural pauses"""
        
        pauses = self.human_fluidity_patterns["natural_pauses"]
        
        # Add pauses at natural break points
        sentences = text.split('.')
        
        for i, sentence in enumerate(sentences):
            if len(sentence.strip()) > 40 and random.random() < 0.15:
                pause = random.choice(pauses)
                words = sentence.split()
                if len(words) > 8:
                    insert_pos = random.randint(4, len(words) - 2)
                    words.insert(insert_pos, pause)
                    sentences[i] = ' '.join(words)
        
        return '. '.join(sentences)
    
    def _add_contractions(self, text: str) -> str:
        """Add natural contractions"""
        
        contractions = self.human_fluidity_patterns["contractions"]
        
        # Apply contractions
        for contraction in contractions:
            if random.random() < 0.1:
                text = text.replace(contraction.replace("'", ""), contraction)
        
        return text
    
    async def _apply_ai_bypass(self, script: str) -> str:
        """Apply AI bypass techniques"""
        
        try:
            bypassed_script = script
            
            if self.ai_bypass_techniques["perplexity_boost"]:
                bypassed_script = self._boost_perplexity(bypassed_script)
            
            if self.ai_bypass_techniques["burstiness_variation"]:
                bypassed_script = self._add_burstiness(bypassed_script)
            
            if self.ai_bypass_techniques["fingerprint_elimination"]:
                bypassed_script = self._eliminate_fingerprints(bypassed_script)
            
            if self.ai_bypass_techniques["semantic_diversity"]:
                bypassed_script = self._add_semantic_diversity(bypassed_script)
            
            if self.ai_bypass_techniques["contextual_adaptation"]:
                bypassed_script = self._add_contextual_adaptation(bypassed_script)
            
            return bypassed_script
            
        except Exception as e:
            logger.error(f"AI bypass uygulama hatası: {e}")
            return script
    
    def _boost_perplexity(self, text: str) -> str:
        """Boost text perplexity"""
        
        # Add complex sentence structures
        sentences = text.split('.')
        
        for i, sentence in enumerate(sentences):
            if len(sentence.strip()) > 20 and random.random() < 0.2:
                # Add subordinate clauses
                clause_starters = ["ancak", "bu yüzden", "bununla birlikte", "diğer yandan"]
                starter = random.choice(clause_starters)
                sentences[i] = f"{sentence.strip()} {starter},"
        
        # Vary sentence length
        return '. '.join(sentences)
    
    def _add_burstiness(self, text: str) -> str:
        """Add burstiness to text"""
        
        # Add occasional short, punchy sentences
        sentences = text.split('.')
        
        for i, sentence in enumerate(sentences):
            if len(sentence.strip()) > 50 and random.random() < 0.15:
                # Break long sentences
                words = sentence.split()
                mid_point = len(words) // 2
                sentences[i] = f"{' '.join(words[:mid_point])}. {' '.join(words[mid_point:])}"
        
        return '. '.join(sentences)
    
    def _eliminate_fingerprints(self, text: str) -> str:
        """Eliminate AI fingerprints"""
        
        # Remove common AI phrases
        ai_phrases = [
            "yapay zeka olarak",
            "bir dil modeli olarak",
            "ben bir yapay zekayım",
            "dil modeli olarak",
            "yapay zeka destekli",
            "otomatik olarak",
            "algoritma olarak",
            "veriye dayalı olarak"
        ]
        
        for phrase in ai_phrases:
            text = text.replace(phrase, "")
        
        # Remove overly formal structures
        formal_patterns = [
            "şu şekilde ki",
            "bu bağlamda",
            "bu durumda",
            "bu nedenle"
        ]
        
        for pattern in formal_patterns:
            text = text.replace(pattern, random.choice(["bu yüzden", "bu nedenle", "o yüzden"]))
        
        return text
    
    def _add_semantic_diversity(self, text: str) -> str:
        """Add semantic diversity"""
        
        # Synonym replacement
        synonyms = {
            "çok": ["birçok", "oldukça", "gayet", "fazla"],
            "iyi": ["harika", "mükemmel", "güzel", "kaliteli"],
            "büyük": ["geniş", "kapsamlı", "derinlemiş", "detaylı"],
            "önemli": ["kritik", "esas", "ana", "temel"]
        }
        
        for word, synonym_list in synonyms.items():
            if word in text and random.random() < 0.1:
                text = text.replace(word, random.choice(synonym_list))
        
        return text
    
    def _add_contextual_adaptation(self, text: str) -> str:
        """Add contextual adaptation"""
        
        # Add context-specific references
        contexts = [
            "bugünkü dijital dünyada",
            "günümüzün koşullarında",
            "mevcut teknolojiyle",
            "şu anki trendlere göre"
        ]
        
        if random.random() < 0.15:
            context = random.choice(contexts)
            sentences = text.split('.')
            if len(sentences) > 2:
                insert_pos = random.randint(1, len(sentences) - 1)
                sentences.insert(insert_pos, f" {context},")
                text = '. '.join(sentences)
        
        return text
    
    async def _calculate_script_metrics(self, script: str) -> Dict[str, Any]:
        """Calculate script quality metrics"""
        
        word_count = len(script.split())
        
        # Calculate hook strength
        hook_indicators = ["?", "!", "şaşırtıcı", "inanılmaz", "harika", "mükemmel"]
        hook_count = sum(1 for indicator in hook_indicators if indicator.lower() in script.lower())
        hook_strength = min(10.0, hook_count * 2.5)
        
        # Calculate viral potential
        viral_indicators = ["paylaş", "beğen", "yorum", "abone", "viral"]
        viral_count = sum(1 for indicator in viral_indicators if indicator.lower() in script.lower())
        viral_potential = min(10.0, viral_count * 2.0)
        
        # Estimate duration
        estimated_duration = word_count * 2  # 2 seconds per word
        
        # Analyze structure
        structure = {
            "introduction": script[:len(script)//4] if len(script) > 100 else script[:50],
            "main_content": script[len(script)//4:3*len(script)//4] if len(script) > 100 else script[50:150] if len(script) > 200 else "",
            "conclusion": script[3*len(script)//4:] if len(script) > 100 else script[150:] if len(script) > 200 else ""
        }
        
        # Extract engagement hooks
        engagement_hooks = []
        sentences = script.split('.')
        for sentence in sentences:
            if any(indicator in sentence.lower() for indicator in hook_indicators):
                engagement_hooks.append(sentence.strip())
        
        return {
            "word_count": word_count,
            "hook_strength": hook_strength,
            "viral_potential": viral_potential,
            "estimated_duration": estimated_duration,
            "structure": structure,
            "engagement_hooks": engagement_hooks[:5]  # Top 5 hooks
        }
    
    async def _calculate_confidence_score(self, script_metrics: Dict[str, Any],
                                      request_data: Dict[str, Any]) -> float:
        """Calculate confidence score for generated script"""
        
        base_score = 70.0
        
        # Word count appropriateness
        target_duration = request_data.get("duration_target", 300)
        target_word_count = target_duration / 2
        word_count = script_metrics["word_count"]
        
        if abs(word_count - target_word_count) / target_word_count < 0.1:
            base_score += 10
        elif abs(word_count - target_word_count) / target_word_count < 0.2:
            base_score += 5
        else:
            base_score -= 10
        
        # Hook strength
        hook_strength = script_metrics["hook_strength"]
        base_score += hook_strength * 2
        
        # Viral potential
        viral_potential = script_metrics["viral_potential"]
        base_score += viral_potential * 1.5
        
        # SEO keyword integration
        seo_keywords = request_data.get("seo_keywords", [])
        script_content = request_data.get("content", "")
        keyword_integration = sum(1 for keyword in seo_keywords if keyword.lower() in script_content.lower())
        
        if keyword_integration >= len(seo_keywords) * 0.8:
            base_score += 10
        elif keyword_integration >= len(seo_keywords) * 0.5:
            base_score += 5
        else:
            base_score -= 5
        
        # Script type match
        script_type = request_data.get("script_type", "educational")
        if script_type in self.capabilities["script_types"]:
            base_score += 5
        
        return min(95.0, max(25.0, base_score))
    
    def _determine_content_pillar(self, topic: str) -> str:
        """Determine content pillar based on topic"""
        
        topic_lower = topic.lower()
        
        if any(keyword in topic_lower for keyword in ["yapay zeka", "teknoloji", "yazılım", "programlama"]):
            return "technology"
        elif any(keyword in topic_lower for keyword in ["iş", "para", "girişim", "pazarlama"]):
            return "business"
        elif any(keyword in topic_lower for keyword in ["eğitim", "öğrenme", "kurs", "ders"]):
            return "education"
        elif any(keyword in topic_lower for keyword in ["oyun", "gaming", "e-spor"]):
            return "gaming"
        elif any(keyword in topic_lower for keyword in ["eğlence", "komedi", "müzik", "film"]):
            return "entertainment"
        else:
            return "general"
    
    async def _fallback_script_generation(self, topic: str, script_type: str,
                                     tone: str, duration_target: int) -> str:
        """Fallback script generation method"""
        
        word_count = int(duration_target / 2)
        
        # Simple template-based generation
        templates = {
            "educational": f"""
            Merhaba arkadaşlar! Bugün {topic} konusunu ele alacağız.
            
            Başlangıçta, {topic} nedir ve neden önemlidir bunu açıklayacağım.
            Ardından, adım adım nasıl yapılacağını göstereceğim.
            Son olarak, önemli ipuçları ve püf noktaları paylaşacağım.
            
            Umarım bu video işinize yarar! Beğenmeyi ve abone olmayı unutmayın!
            """,
            "entertainment": f"""
            Hayırlar! Bugün çok özel bir içerikle karşınızdayız.
            
            {topic} hakkında konuşacağız ve inanılmaz şeyler göstereceğim!
            Hazırsanız başlıyoruz!
            
            [İçerik buraya gelecek]
            
            Ne düşünüyorsunuz? Yorumlarda yazın!
            """,
            "business": f"""
            Değerli izleyicilerim,
            
            Bugün {topic} stratejisini masaya yatıracağız.
            
            Bu yöntemle nasıl başarılı olabileceğinizi adım adım anlatacağım.
            Deneyimlerimden elde ettiğim sonuçları paylaşacağım.
            
            Hazırsanız başlıyoruz!
            """
        }
        
        template = templates.get(script_type, templates["educational"])
        
        # Adjust word count
        words = template.split()
        if len(words) > word_count:
            template = ' '.join(words[:word_count])
        elif len(words) < word_count:
            # Add filler content
            filler = f" {topic} hakkında daha fazla detay verebilirim. Bu konu gerçekten çok önemli."
            template += filler * ((word_count - len(words)) // 10)
        
        return template
    
    def _log_success_pattern(self, request_data: Dict[str, Any], 
                           script_intelligence: ScriptIntelligence):
        """Log successful pattern for learning"""
        
        pattern = {
            "timestamp": datetime.now().isoformat(),
            "request": request_data,
            "result": {
                "confidence": script_intelligence.confidence.score,
                "word_count": script_intelligence.word_count,
                "hook_strength": script_intelligence.hook_strength,
                "viral_potential": script_intelligence.viral_potential,
                "script_type": script_intelligence.script_type,
                "tone": script_intelligence.emotional_tone
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
            "human_fluidity_patterns": self.human_fluidity_patterns,
            "ai_bypass_techniques": self.ai_bypass_techniques,
            "success_patterns_count": len(self.success_patterns),
            "average_confidence": sum(p["result"]["confidence"] for p in self.success_patterns) / max(1, len(self.success_patterns)),
            "last_generation": self.success_patterns[-1]["timestamp"] if self.success_patterns else None,
            "health_status": "healthy" if len(self.success_patterns) > 0 else "idle"
        }

# Global instance
script_agent = ScriptAgent()
