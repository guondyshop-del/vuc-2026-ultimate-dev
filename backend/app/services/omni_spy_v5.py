"""
VUC-2026 Omni-Spy 5.0
Competitor Annihilation Protocol

Script reverse-engineering, retention gap exploitation,
saliency mapping, and SEO dominance engine.
"""

import logging
import asyncio
import random
import re
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime
from collections import Counter

logger = logging.getLogger(__name__)


class OmniSpyV5:
    """
    Omni-Spy 5.0: Competitor Annihilation Module
    
    Features:
    - Script DNA extraction from top 5 viral videos
    - Retention gap exploitation via comment NLP
    - Saliency map dominance for thumbnails
    - SEO & tag stealing with LSI keyword injection
    """

    def __init__(self):
        self.spy_id = "omni_spy_v5"
        self.analysis_cache: Dict[str, Any] = {}
        
        # Structural DNA patterns for script analysis
        self.hook_patterns = [
            r"^(?:İşte|Şimdi|Bugün|Hemen|Dikkat|Şok|İnanılmaz|Kesinlikle|Mutlaka|Acil)",
            r"\d+ (?:şey|yol|adım|taktik|sır|ipucu|hata|gerçek|yöntem)",
            r"(?:yapıyorsan|yapmadan|bilmeden|öğrenmeden|denemeden)",
            r"(?:hayatını değiştirecek|kaçırmaman gereken|herkesin bilmek istediği)",
        ]
        
        self.cta_patterns = [
            r"(?:abone ol|like at|yorum yap|bildirimleri aç|kaydet|paylaş)",
            r"(?:sonraki videoda|gelecek videoda|devamı için|devam edelim)",
            r"(?:yorumlara yaz|düşüncelerini paylaş|sorularını sor)",
        ]

    async def annihilate_competitor(self, niche: str, primary_keyword: str,
                                     competitor_channel: Optional[str] = None) -> Dict[str, Any]:
        """
        Full competitor annihilation analysis pipeline.
        
        Args:
            niche: Target niche
            primary_keyword: Main keyword to dominate
            competitor_channel: Specific competitor to analyze
            
        Returns:
            Complete annihilation strategy with engineered superiority
        """
        try:
            logger.info(f"Omni-Spy 5.0 başlatıldı: {niche} - {primary_keyword}")
            
            # 1. Discover top 5 viral videos
            top_videos = await self._discover_viral_videos(niche, primary_keyword)
            
            # 2. Extract script DNA from each
            script_dnas = []
            for video in top_videos:
                dna = await self._extract_script_dna(video)
                script_dnas.append(dna)
            
            # 3. Find retention gaps from comments
            retention_gaps = await self._analyze_retention_gaps(top_videos)
            
            # 4. Generate saliency maps for thumbnails
            saliency_data = await self._analyze_thumbnail_saliency(top_videos)
            
            # 5. Extract and enhance SEO metadata
            seo_dominance = await self._extract_seo_dominance(top_videos, primary_keyword)
            
            # 6. Engineer superior content
            superior_script = self._engineer_superior_script(
                script_dnas, retention_gaps, primary_keyword
            )
            
            # 7. Generate optimal thumbnail strategy
            thumbnail_strategy = self._generate_thumbnail_strategy(saliency_data, niche)
            
            result = {
                "niche": niche,
                "primary_keyword": primary_keyword,
                "competitor_videos_analyzed": len(top_videos),
                "script_dnas": script_dnas,
                "retention_gaps": retention_gaps,
                "saliency_analysis": saliency_data,
                "seo_dominance": seo_dominance,
                "superior_content": superior_script,
                "thumbnail_strategy": thumbnail_strategy,
                "annihilation_score": self._calculate_annihilation_score(
                    script_dnas, retention_gaps, superior_script
                ),
                "execution_roadmap": self._generate_execution_roadmap(),
                "analyzed_at": datetime.now().isoformat()
            }
            
            self.analysis_cache[f"{niche}_{primary_keyword}"] = result
            
            logger.info(f"Annihilation tamamlandı: Skor {result['annihilation_score']:.1f}/10")
            return result
            
        except Exception as e:
            logger.error(f"Omni-Spy 5.0 hatası: {e}")
            return {"success": False, "error": str(e)}

    async def _discover_viral_videos(self, niche: str, keyword: str) -> List[Dict[str, Any]]:
        """Discover top 5 viral videos in niche via YouTube Data API simulation"""
        await asyncio.sleep(0.2)  # API simulation
        
        videos = []
        for i in range(5):
            views = random.randint(500000, 5000000)
            videos.append({
                "rank": i + 1,
                "video_id": f"viral_{niche}_{i+1}_{int(datetime.now().timestamp())}",
                "title": self._generate_viral_title(niche, keyword, i),
                "views": views,
                "likes": int(views * random.uniform(0.03, 0.08)),
                "comments": int(views * random.uniform(0.005, 0.02)),
                "duration_seconds": random.randint(180, 900),
                "ctr": random.uniform(6.0, 14.0),
                "retention_rate": random.uniform(0.45, 0.75),
                "channel_subs": random.randint(50000, 500000),
                "upload_date": (datetime.now() - timedelta(days=random.randint(7, 90))).isoformat()
            })
        
        return sorted(videos, key=lambda x: x["views"], reverse=True)

    def _generate_viral_title(self, niche: str, keyword: str, index: int) -> str:
        """Generate realistic viral video title"""
        templates = [
            f"{keyword} ile Para Kazanmanın {random.randint(3, 10)} Yolu! (Şok Edici)",
            f"Bu {keyword} Stratejisi ile {random.randint(1000, 10000)}₺ Kazandım",
            f"{keyword}'yi Bilmeyenler Çok Şey Kaybediyor!",
            f"{keyword} Uzmanı Oldum: İşte Sırlarım",
            f"{keyword} Rehberi 2026: Sadece Gerçekler"
        ]
        return templates[index % len(templates)]

    async def _extract_script_dna(self, video: Dict[str, Any]) -> Dict[str, Any]:
        """
        Extract structural DNA from video script.
        Analyzes: Hook structure, body pacing, CTA placement, emotional volatility.
        """
        # Simulated transcript analysis
        simulated_transcript = self._generate_simulated_transcript(video)
        
        # Extract hook (first 30 seconds ~ 75 words)
        words = simulated_transcript.split()
        hook_words = words[:75]
        hook = " ".join(hook_words)
        
        # Analyze hook patterns
        hook_matches = []
        for pattern in self.hook_patterns:
            if re.search(pattern, hook, re.IGNORECASE):
                hook_matches.append(pattern)
        
        # Extract body structure
        body_start = 75
        body_end = len(words) - 50  # Leave room for CTA
        body = " ".join(words[body_start:body_end])
        
        # Identify body segments (3-5 parts typical)
        segment_size = max(len(words[body_start:body_end]) // 4, 50)
        segments = []
        for i in range(0, len(words[body_start:body_end]), segment_size):
            seg_words = words[body_start:body_end][i:i+segment_size]
            segments.append({
                "index": len(segments) + 1,
                "word_count": len(seg_words),
                "preview": " ".join(seg_words[:10]) + "...",
                "emotional_intensity": random.uniform(0.3, 0.9)
            })
        
        # Extract CTA
        cta_words = words[-50:] if len(words) > 50 else words[-20:]
        cta = " ".join(cta_words)
        
        cta_matches = []
        for pattern in self.cta_patterns:
            if re.search(pattern, cta, re.IGNORECASE):
                cta_matches.append(pattern)
        
        # Calculate emotional volatility
        emotional_markers = self._count_emotional_markers(simulated_transcript)
        volatility = min(1.0, emotional_markers / max(len(words) / 100, 1))
        
        return {
            "video_id": video["video_id"],
            "hook": {
                "text": hook,
                "word_count": len(hook_words),
                "patterns_matched": hook_matches,
                "hook_strength": len(hook_matches) * 0.25 + 0.3,
                "has_numbers": bool(re.search(r'\d+', hook)),
                "has_power_words": len(hook_matches) > 0
            },
            "body": {
                "word_count": body_end - body_start,
                "segments": segments[:4],  # Max 4 segments
                "avg_segment_intensity": sum(s["emotional_intensity"] for s in segments) / max(len(segments), 1),
                "information_density": random.uniform(0.4, 0.8)
            },
            "cta": {
                "text": cta,
                "word_count": len(cta_words),
                "patterns_matched": cta_matches,
                "cta_strength": len(cta_matches) * 0.3 + 0.2,
                "placement": "end" if len(words) > 100 else "mid"
            },
            "emotional_volatility": round(volatility, 2),
            "total_words": len(words),
            "structural_formula": self._derive_structural_formula(hook_matches, segments, cta_matches)
        }

    def _generate_simulated_transcript(self, video: Dict[str, Any]) -> str:
        """Generate realistic transcript based on video metadata"""
        # Simulate word count based on duration
        word_count = (video["duration_seconds"] // 3) + random.randint(-20, 20)
        
        # Hook section
        hooks = [
            f"Bugün {video['views']:,} kişinin izlediği bu stratejiyi açıklıyorum.",
            f"Dikkat! Bu {random.randint(3, 7)} yöntemi bilmeden para kazanamazsınız.",
            f"İnanılmaz ama gerçek! Bu teknikle {random.randint(1000, 10000)}₺ kazandım.",
            f"Şok edici gerçek: Herkes bunu yanlış yapıyor!",
            f"Hemen izle! Bu fırsatı kaçırma!"
        ]
        
        # Body sections
        bodies = [
            "İlk olarak şunu anlamamız gerekiyor. Piyasa sürekli değişiyor ve eski yöntemler artık işe yaramıyor. "
            "Yeni trendleri takip etmek zorundayız. Özellikle yapay zeka araçları bu alanda devrim yaratıyor.",
            
            "İkinci strateji çok daha agresif. Rakiplerinizi analiz edip onların zayıf noktalarını kullanacaksınız. "
            "Bu etik değil gibi görünse bile iş dünyası böyle işler. Veri her şeydir.",
            
            "Üçüncü ve en kritik nokta: Tutarlılık. Bir gün çalışıp sonra bırakamazsınız. "
            "Her gün en az iki saat ayırmanız şart. Bu disiplin sizi zirveye taşıyacak.",
            
            "Dördüncü olarak, network'ünüzü genişletin. Tanıdığınız kişi sayısı doğrudan gelirinizi etkiler. "
            "Etkili insanlarla bağlantı kurun, onlardan öğrenin, ortak projeler yapın."
        ]
        
        # CTA section
        ctas = [
            "Abone olmayı ve bildirimleri açmayı unutma! Gelecek videoda daha fazla sırrı açıklayacağım. "
            "Yorumlara düşüncelerini yaz, en iyi yorumu sabitleyeceğim!",
            
            "Bu videoyu kaydet ve arkadaşlarınla paylaş! Daha fazla içerik için kanalıma abone ol. "
            "Açıklamadaki linkten ücretsiz rehberimi indirmeyi unutma!"
        ]
        
        transcript = random.choice(hooks) + " "
        for body in random.sample(bodies, k=min(3, len(bodies))):
            transcript += body + " "
        transcript += random.choice(ctas)
        
        return transcript

    def _count_emotional_markers(self, text: str) -> int:
        """Count emotional intensity markers in text"""
        markers = [
            "!", "şok", "inanılmaz", "harika", "mükemmel", "korkunç", "heyecan",
            "mutlaka", "kesinlikle", "asla", "her zaman", "acil", "hemen",
            "amazing", "incredible", "shocking", "must", "never", "always"
        ]
        text_lower = text.lower()
        return sum(1 for marker in markers if marker in text_lower)

    def _derive_structural_formula(self, hook_patterns: List[str],
                                    segments: List[Dict],
                                    cta_patterns: List[str]) -> str:
        """Derive structural formula like H3-B4-C2 (Hook 3 patterns, Body 4 segments, CTA 2 patterns)"""
        return f"H{len(hook_patterns)}-B{len(segments)}-C{len(cta_patterns)}"

    async def _analyze_retention_gaps(self, videos: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        NLP analysis of competitor comments to find retention gaps.
        Identifies: Missing information, confusion points, requests for follow-up.
        """
        gaps = []
        
        for video in videos:
            # Simulated comment analysis
            simulated_comments = self._generate_simulated_comments(video)
            
            # Analyze for gap indicators
            gap_indicators = {
                "missing_info": [
                    r"(?:anlamadım|sormak istiyorum|belirtmemişsin|eksik kalmış|daha detaylı)",
                    r"(?:didn't mention|forgot to say|what about|missing|more details)",
                    r"(?:nerede bulabilirim|nasıl yapacağız|hangi program|ne zaman)",
                ],
                "confusion": [
                    r"(?:kafam karıştı|nasıl oluyor|tam olarak|bi daha anlat|anlamıyorum)",
                    r"(?:confused|don't understand|explain again|not clear|how does)",
                ],
                "requests": [
                    r"(?:devamını bekliyorum|serinin devamı|bir sonraki video|daha fazla|part 2)",
                    r"(?:waiting for|next part|series continuation|more videos|part two)",
                    r"(?:bunu göster|şunu anlat|bununla ilgili|bu konuda)",
                ]
            }
            
            video_gaps = {
                "video_id": video["video_id"],
                "missing_info": [],
                "confusion_points": [],
                "content_requests": [],
                "sentiment_issues": []
            }
            
            for comment in simulated_comments:
                text = comment["text"].lower()
                
                for pattern in gap_indicators["missing_info"]:
                    if re.search(pattern, text):
                        video_gaps["missing_info"].append({
                            "comment_preview": comment["text"][:60],
                            "gap_type": "information_gap",
                            "urgency": "high" if comment["likes"] > 50 else "medium"
                        })
                        break
                
                for pattern in gap_indicators["confusion"]:
                    if re.search(pattern, text):
                        video_gaps["confusion_points"].append({
                            "comment_preview": comment["text"][:60],
                            "confusion_topic": self._extract_topic(text),
                            "clarity_needed": True
                        })
                        break
                
                for pattern in gap_indicators["requests"]:
                    if re.search(pattern, text):
                        video_gaps["content_requests"].append({
                            "request_type": "follow_up_content",
                            "topic": self._extract_topic(text),
                            "demand_strength": comment["likes"]
                        })
                        break
            
            gaps.append(video_gaps)
        
        # Aggregate gaps across all competitors
        aggregated = self._aggregate_retention_gaps(gaps)
        return aggregated

    def _generate_simulated_comments(self, video: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate realistic comments for analysis"""
        comment_count = min(50, int(video["comments"] * 0.01))  # Sample 1% of comments
        comments = []
        
        templates = [
            {"text": "Harika video! Ama {topic}'yi biraz daha detaylı anlatabilir misin?", "sentiment": "positive_gap"},
            {"text": "Kafam karıştı, {topic} kısmını anlamadım bi daha anlatır mısın?", "sentiment": "confused"},
            {"text": "Devamını bekliyorum! {topic} hakkında daha fazla içerik lütfen", "sentiment": "request"},
            {"text": "Bu strateji işe yarıyor mu deneyen var mı? {topic} için geçerli mi?", "sentiment": "skeptical"},
            {"text": "Nerede bulabiliriz bu araçları? {topic} linki var mı açıklamada?", "sentiment": "information_seeking"},
            {"text": "Şu bölümü anlamadım: {topic} - daha basit anlatım yapabilir misin?", "sentiment": "confused"},
            {"text": "Part 2 gelsin lütfen! {topic} devamı için sabırsızlanıyorum", "sentiment": "request"},
            {"text": "Başkaları da bu konuda video yapmış ama seninki daha iyi. {topic} eklersen süper olur", "sentiment": "positive_gap"}
        ]
        
        topics = ["para kazanma", "yapay zeka", "strateji", "araçlar", "öneriler", "örnekler", "detaylar", "uygulama"]
        
        for i in range(comment_count):
            template = random.choice(templates)
            topic = random.choice(topics)
            text = template["text"].format(topic=topic)
            
            comments.append({
                "comment_id": f"c_{video['video_id']}_{i}",
                "text": text,
                "likes": random.randint(1, 200),
                "replies": random.randint(0, 15),
                "sentiment": template["sentiment"],
                "is_top_comment": i < 5
            })
        
        return sorted(comments, key=lambda x: x["likes"], reverse=True)

    def _extract_topic(self, text: str) -> str:
        """Extract the main topic from gap comment"""
        # Simple extraction - look for quoted phrases or specific keywords
        quotes = re.findall(r'"([^"]+)"', text)
        if quotes:
            return quotes[0]
        
        # Look for keywords after prepositions
        keywords = re.findall(r'(?:about|regarding|on|hakkında|konusunda|için)\s+(\w+(?:\s+\w+){0,3})', text, re.IGNORECASE)
        if keywords:
            return keywords[0]
        
        return "general_topic"

    def _aggregate_retention_gaps(self, video_gaps: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Aggregate gaps across all competitors to find common opportunities"""
        all_missing = []
        all_confusion = []
        all_requests = []
        
        for vg in video_gaps:
            all_missing.extend(vg["missing_info"])
            all_confusion.extend(vg["confusion_points"])
            all_requests.extend(vg["content_requests"])
        
        # Find most common gap types
        missing_counter = Counter([m.get("gap_type") for m in all_missing])
        
        return [
            {
                "category": "high_priority_gaps",
                "total_missing_info": len(all_missing),
                "total_confusion_points": len(all_confusion),
                "total_content_requests": len(all_requests),
                "most_common_gaps": missing_counter.most_common(3),
                "exploitable_opportunities": [
                    "Detaylı araç kullanım rehberi eksik",
                    "Gerçek örnekler ve case studies az",
                    "Adım adım uygulama videosu talep ediliyor",
                    "Başlangıç seviyesi için basitleştirilmiş anlatım gerekli"
                ],
                "content_strategy": "Rakiplerin açıkladığı ama detaylandırmadığı konulara odaklan"
            }
        ]

    async def _analyze_thumbnail_saliency(self, videos: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Visual saliency mapping for thumbnail optimization.
        Identifies where human eyes focus and where competitors leave dead space.
        """
        await asyncio.sleep(0.1)
        
        # Simulated heatmap analysis
        heatmap_data = []
        
        for video in videos:
            # Generate simulated saliency data
            # Real implementation would use OpenCV + face detection + contrast analysis
            
            # Competitors typically put subject in center
            competitor_focus = {
                "primary_focus": {"x": 0.5, "y": 0.5, "radius": 0.25},  # Center
                "secondary_focuses": [
                    {"x": 0.2, "y": 0.8, "type": "text"},  # Bottom left text
                    {"x": 0.8, "y": 0.2, "type": "emoji"}  # Top right emoji
                ],
                "dead_zones": [
                    {"x": 0.1, "y": 0.1, "area": 0.05},  # Top left corner
                    {"x": 0.9, "y": 0.9, "area": 0.05}   # Bottom right corner
                ],
                "contrast_score": random.uniform(0.4, 0.8),
                "face_detected": random.random() > 0.3,
                "text_readability": random.uniform(0.5, 0.9)
            }
            
            heatmap_data.append({
                "video_id": video["video_id"],
                "views": video["views"],
                "saliency_profile": competitor_focus
            })
        
        # Find the winning pattern
        best_performer = max(heatmap_data, key=lambda x: x["views"])
        
        # Generate dominance strategy
        dominance_strategy = {
            "competitor_patterns": {
                "common_focus_point": "center",
                "text_placement": "bottom_third",
                "face_usage_rate": sum(1 for h in heatmap_data if h["saliency_profile"]["face_detected"]) / len(heatmap_data)
            },
            "your_advantage": {
                "primary_hook_placement": {
                    "x": 0.25, "y": 0.25,  # Top-left, where competitors have dead space
                    "rationale": "Rakiplerin ölü bıraktığı bölge, dikkat çekici kontrast"
                },
                "high_contrast_element": {
                    "type": "emoji_or_face",
                    "size": "30%_of_frame",
                    "position": "rule_of_thirds_intersection"
                },
                "text_strategy": {
                    "main_hook": "upper_left_quadrant",
                    "sub_text": "bottom_center",
                    "font_style": "bold_sans_serif",
                    "max_chars": 8
                }
            },
            "color_dominance": {
                "background": "complementary_to_competitor_dominant",
                "foreground": "maximum_contrast",
                "accent": "warm_tone_for_attention"
            }
        }
        
        return {
            "competitor_heatmap_analysis": heatmap_data,
            "best_performer_profile": best_performer,
            "dominance_strategy": dominance_strategy,
            "attention_grabbing_formula": "Hook_TopLeft + Face_CenterLeft + Text_BottomCenter"
        }

    async def _extract_seo_dominance(self, videos: List[Dict[str, Any]], 
                                      primary_keyword: str) -> Dict[str, Any]:
        """
        Extract and enhance SEO metadata for dominance.
        Steals tags but rewrites with higher-volume LSI keywords.
        """
        # Collect all competitor metadata
        all_tags = []
        all_titles = []
        all_descriptions = []
        
        for video in videos:
            # Simulated metadata extraction
            tags = self._generate_competitor_tags(video, primary_keyword)
            all_tags.extend(tags)
            all_titles.append(video["title"])
        
        # Analyze keyword frequency
        tag_counter = Counter(all_tags)
        
        # Find LSI (Latent Semantic Indexing) keywords
        lsi_keywords = self._generate_lsi_keywords(primary_keyword)
        
        # Generate superior metadata
        superior_metadata = {
            "title_templates": [
                f"{primary_keyword} Rehberi 2026: Sadece Gerçekler (Şok Edici)",
                f"Bu {primary_keyword} Stratejisi ile {random.randint(5000, 50000)}₺ Kazandım",
                f"{primary_keyword}'yi Bilmeyenler Kaybediyor! İşte Neden...",
                f"{primary_keyword} Uzmanı Oldum: {random.randint(5, 15)} Yıllık Tecrübe"
            ],
            "description_structure": {
                "hook": f"🎯 {primary_keyword} hakkında her şeyi öğrenmeye hazır mısın?",
                "social_proof": f"✅ {sum(v['views'] for v in videos):,}+ kişi bu bilgiyi kullanıyor",
                "value_prop": "💡 Sadece kanıtlanmış stratejiler, hayal satmıyoruz",
                "cta": "👇 Abone ol ve bildirimleri aç, kaçırma!"
            },
            "tags_stealed_enhanced": [
                # Original competitor tags
                *tag_counter.most_common(10),
                # Enhanced LSI keywords
                *[(kw, random.randint(50, 200)) for kw in lsi_keywords[:15]]
            ],
            "lsi_keyword_injection": lsi_keywords[:20],
            "timestamp_optimization": {
                "mention_at_0s": primary_keyword,
                "mention_at_30s": lsi_keywords[0],
                "mention_at_60s": lsi_keywords[1],
                "final_mention": lsi_keywords[2]
            }
        }
        
        return {
            "competitor_tag_analysis": dict(tag_counter.most_common(20)),
            "superior_metadata": superior_metadata,
            "keyword_dominance_score": min(10.0, len(lsi_keywords) * 0.5),
            "search_volume_projection": "high" if len(lsi_keywords) > 15 else "medium"
        }

    def _generate_competitor_tags(self, video: Dict[str, Any], primary: str) -> List[str]:
        """Generate realistic competitor tags"""
        return [
            primary,
            f"{primary} 2026",
            "para kazanma",
            "iş fikirleri",
            "online gelir",
            "yeni başlayanlar",
            "evden çalışma",
            "pasif gelir",
            "girişimcilik",
            "finansal özgürlük"
        ]

    def _generate_lsi_keywords(self, primary: str) -> List[str]:
        """Generate LSI keywords for semantic SEO dominance"""
        bases = {
            "yapay zeka": [
                "chatgpt", "ai araçları", "makine öğrenmesi", "automation",
                "content creation", "prompt engineering", "llm", "neural networks",
                "yapay zeka uygulamaları", "ai iş modelleri", "gpt-4", "claude",
                "content üretimi", "otomasyon", "veri analizi", "ai marketing"
            ],
            "para kazanma": [
                "online iş", "freelance", "remote work", "digital nomad",
                "e-ticaret", "affiliate marketing", "dropshipping", "blog monetization",
                "youtube geliri", "pasif gelir kaynakları", "yatırım", "borsa",
                "kripto para", "nft", "web3", "metaverse ekonomisi"
            ]
        }
        
        return bases.get(primary, [
            "tutorial", "guide", "how to", "best practices",
            "tips and tricks", "step by step", "beginner friendly",
            "advanced strategies", "case study", "real examples"
        ])

    def _engineer_superior_script(self, dnas: List[Dict[str, Any]], 
                                   gaps: List[Dict[str, Any]],
                                   primary_keyword: str) -> Dict[str, Any]:
        """
        Engineer a script with 20% higher emotional volatility
        and superior structural DNA.
        """
        # Analyze best performing DNA
        best_hook = max(dnas, key=lambda x: x["hook"]["hook_strength"])
        best_cta = max(dnas, key=lambda x: x["cta"]["cta_strength"])
        avg_volatility = sum(d["emotional_volatility"] for d in dnas) / len(dnas)
        
        # Target: 20% higher volatility
        target_volatility = min(1.0, avg_volatility * 1.2)
        
        # Generate engineered script structure
        superior = {
            "hook": {
                "formula": f"[ŞOK] + [RAKAM] + [{primary_keyword.upper()}] + [ZAMAN_BASKISI]",
                "example": f"Şok! Bu {primary_keyword} yöntemiyle 30 günde 15.000₺ kazandım! (Son 48 saat)",
                "target_duration_seconds": 8,
                "emotional_triggers": ["korku", "merak", "açgözlülük", "aciliyet"],
                "volatility_target": round(target_volatility, 2)
            },
            "body_structure": {
                "segment_count": 4,
                "segments": [
                    {
                        "index": 1,
                        "focus": gaps[0]["exploitable_opportunities"][0] if gaps else "Temel kavramlar",
                        "duration_seconds": 90,
                        "information_density": "high",
                        "visual_support": "screen_record"
                    },
                    {
                        "index": 2,
                        "focus": gaps[0]["exploitable_opportunities"][1] if gaps and len(gaps[0]["exploitable_opportunities"]) > 1 else "Strateji detayları",
                        "duration_seconds": 120,
                        "emotional_peak": True,
                        "pattern_interrupt": True
                    },
                    {
                        "index": 3,
                        "focus": "Rakiplerin anlatamadığı kritik nokta",
                        "duration_seconds": 90,
                        "retention_hook": "Bunu bilmeden kaybedersiniz"
                    },
                    {
                        "index": 4,
                        "focus": "Uygulama ve sonuçlar",
                        "duration_seconds": 60,
                        "proof_elements": ["ekran görüntüsü", "rakam", "tarih"]
                    }
                ]
            },
            "cta": {
                "formula": f"[DEĞER_TEKLİFİ] + [TOPLULUK_BASKISI] + [{primary_keyword}_VAADİ]",
                "primary_cta": f"Abone ol, {primary_keyword} serisinin devamı için zil butonuna bas!",
                "secondary_cta": f"Yoruma '{primary_keyword}' yaz, en iyi 10'a özel PDF göndereceğim!",
                "urgency_element": "48 saat içinde ilk 1000 yoruma yanıt garantisi"
            },
            "emotional_volatility": round(target_volatility, 2),
            "retention_gaps_addressed": len(gaps[0]["exploitable_opportunities"]) if gaps else 4,
            "competitive_advantage": "Rakiplerin detaylandırmadığı her noktayı 3x daha derinlemesine açıklıyoruz"
        }
        
        return superior

    def _generate_thumbnail_strategy(self, saliency_data: Dict[str, Any],
                                      niche: str) -> Dict[str, Any]:
        """Generate winning thumbnail strategy based on saliency analysis"""
        strategy = saliency_data["dominance_strategy"]
        
        return {
            "composition": {
                "rule": "rule_of_thirds_modified",
                "subject_placement": strategy["your_advantage"]["primary_hook_placement"],
                "text_layers": 2,
                "max_visual_elements": 3
            },
            "color_psychology": {
                "dominant_hue": self._get_niche_dominant_hue(niche),
                "complementary_action": strategy["color_dominance"]["foreground"],
                "contrast_ratio_target": 7.0  # WCAG AAA
            },
            "text_strategy": {
                "primary_hook": {
                    "max_chars": 6,
                    "style": "bold_uppercase",
                    "color": "high_contrast_to_bg",
                    "placement": "upper_left_quadrant"
                },
                "secondary_text": {
                    "max_chars": 12,
                    "style": "mixed_case",
                    "placement": "bottom_center"
                }
            },
            "face_strategy": {
                "include": True,
                "expression": "surprise_or_intrigue",
                "gaze_direction": "toward_text",
                "size_percent": 30
            },
            "emoji_icon": {
                "type": "reaction_emoji",
                "position": "near_hook_text",
                "scale": 1.5
            }
        }

    def _get_niche_dominant_hue(self, niche: str) -> str:
        """Get dominant hue for niche"""
        hues = {
            "technology": "blue_cyan",
            "business": "gold_orange",
            "education": "green_teal",
            "gaming": "purple_magenta",
            "entertainment": "red_pink"
        }
        return hues.get(niche, "blue")

    def _calculate_annihilation_score(self, dnas: List[Dict], 
                                     gaps: List[Dict], 
                                     superior: Dict) -> float:
        """Calculate overall annihilation effectiveness score"""
        scores = {
            "script_dna_improvement": min(10, sum(d["hook"]["hook_strength"] for d in dnas) / len(dnas) * 2),
            "retention_gap_coverage": min(10, len(gaps[0]["exploitable_opportunities"]) * 2) if gaps else 5,
            "emotional_volatility_boost": superior["emotional_volatility"] * 10,
            "structural_superiority": 8.0 if len(superior["body_structure"]["segments"]) >= 4 else 6.0
        }
        
        return round(sum(scores.values()) / len(scores), 1)

    def _generate_execution_roadmap(self) -> List[Dict[str, Any]]:
        """Generate step-by-step execution roadmap"""
        return [
            {
                "phase": 1,
                "name": "Araştırma & Analiz",
                "duration_hours": 2,
                "tasks": ["Rakip videoları izle", "Yorumları analiz et", "Script DNA çıkar"]
            },
            {
                "phase": 2,
                "name": "Script Üretimi",
                "duration_hours": 3,
                "tasks": ["Superior hook yaz", "4 segment oluştur", "CTA optimize et"]
            },
            {
                "phase": 3,
                "name": "Üretim",
                "duration_hours": 4,
                "tasks": ["Seslendirme", "Görsel edit", "B-roll ekle", "Caption animasyon"]
            },
            {
                "phase": 4,
                "name": "Optimizasyon & Yayın",
                "duration_hours": 2,
                "tasks": ["Thumbnail test", "SEO meta yaz", "Schedule at optimal time", "Cross-platform adapt"]
            }
        ]


# Global instance
omni_spy_v5 = OmniSpyV5()
