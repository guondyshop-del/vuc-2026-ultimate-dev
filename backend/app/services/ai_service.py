import google.generativeai as genai
import json
import logging
from typing import Dict, List, Any, Optional
from datetime import datetime
import re

logger = logging.getLogger(__name__)

class AIService:
    """Gemini 2.0 Pro AI Servisi"""
    
    def __init__(self, api_key: str):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-2.0-pro')
        self.vision_model = genai.GenerativeModel('gemini-2.0-pro-vision')
    
    def generate_script(self, topic: str, language: str = "TR", style: str = "engaging", 
                       target_duration: int = 300, keywords: List[str] = None) -> Dict[str, Any]:
        """
        Video senaryosu oluştur
        
        Args:
            topic: Video konusu
            language: Dil (TR, EN, DE, FR, ES)
            style: Stil (engaging, educational, entertainment)
            target_duration: Hedef süre (saniye)
            keywords: Hedef anahtar kelimeler
        """
        
        # Prompt oluştur
        prompt = self._create_script_prompt(topic, language, style, target_duration, keywords)
        
        try:
            response = self.model.generate_content(prompt)
            script_text = response.text
            
            # Senaryoyu parse et
            parsed_script = self._parse_script(script_text, language)
            
            return {
                "success": True,
                "script": parsed_script,
                "raw_text": script_text,
                "metadata": {
                    "topic": topic,
                    "language": language,
                    "style": style,
                    "target_duration": target_duration,
                    "generated_at": datetime.now().isoformat()
                }
            }
            
        except Exception as e:
            logger.error(f"Senaryo oluşturma hatası: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def analyze_thumbnail_performance(self, thumbnail_url: str, title: str, 
                                    niche: str) -> Dict[str, Any]:
        """Thumbnail performansını analiz et"""
        
        prompt = f"""
        Bu thumbnail ve başlık kombinasyonunu analiz et ve YouTube'da ne kadar etkili olacağını değerlendir.
        
        Başlık: {title}
        Niş: {niche}
        
        Şu metrikleri tahmin et (1-10 arası puan):
        - Tıklanma Oranı (CTR) potansiyeli
        - Dikkat çekme gücü
        - Profesyonellik
        - Duygusal etki
        - Trend uyumluluğu
        
        Ayrıca thumbnail'de şu elementleri tespit et:
        - Yüz ifadeleri
        - Renk kullanımı
        - Metin varlığı
        - Kontrast seviyesi
        
        Sonuçları JSON formatında döndür.
        """
        
        try:
            # Vision model ile thumbnail analiz et
            response = self.vision_model.generate_content([
                prompt,
                thumbnail_url
            ])
            
            analysis_text = response.text
            
            # JSON kısmını extract et
            json_match = re.search(r'\{.*\}', analysis_text, re.DOTALL)
            if json_match:
                analysis_data = json.loads(json_match.group())
            else:
                analysis_data = {"error": "JSON parse edilemedi"}
            
            return {
                "success": True,
                "analysis": analysis_data,
                "raw_response": analysis_text
            }
            
        except Exception as e:
            logger.error(f"Thumbnail analiz hatası: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def generate_content_ideas(self, niche: str, language: str = "TR", 
                              count: int = 10) -> List[Dict[str, Any]]:
        """İçerik fikirleri oluştur"""
        
        prompt = f"""
        {niche} nişinde viral olabilecek {count} tane video fikri oluştur.
        Dil: {language}
        
        Her fikir için şu bilgileri ver:
        - Başlık (attention-grabbing)
        - Kısa açıklama
        - Hedef kitle
        - Tahmini izlenme potansiyeli (düşük/orta/yüksek)
        - Üretim zorluğu (kolay/orta/zor)
        - Trend potansiyeli (1-10)
        
        Sonuçları JSON array formatında döndür.
        """
        
        try:
            response = self.model.generate_content(prompt)
            response_text = response.text
            
            # JSON array extract et
            json_match = re.search(r'\[.*\]', response_text, re.DOTALL)
            if json_match:
                ideas = json.loads(json_match.group())
            else:
                # Manuel parse et
                ideas = self._parse_ideas_manually(response_text)
            
            return {
                "success": True,
                "ideas": ideas,
                "niche": niche,
                "language": language
            }
            
        except Exception as e:
            logger.error(f"İçerik fikri oluşturma hatası: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def generate_persona_responses(self, video_id: str, comments: List[str], 
                                 personas: List[str] = None) -> List[Dict[str, Any]]:
        """Persona tabanlı yorum yanıtları oluştur"""
        
        if not personas:
            personas = [
                "destekleyici ve teşvik edici",
                "meraklı ve soru soran", 
                "espri anlayışlı ve neşeli",
                "uzman ve bilgilendirici",
                "samimi ve kişisel"
            ]
        
        responses = []
        
        for i, comment in enumerate(comments):
            persona = personas[i % len(personas)]
            
            prompt = f"""
            Bu yoruma "{persona}" bir persona olarak yanıt ver.
            Yorum: "{comment}"
            
            Yanıt şu özelliklerde olmalı:
            - Doğal ve samimi
            - Persona'ya uygun ton
            - Etkileşimi teşvik edici
            - Kısa ve öz (maksimum 50 kelime)
            - Türkçe
            
            Sadece yanıt metnini döndür, açıklama yapma.
            """
            
            try:
                response = self.model.generate_content(prompt)
                response_text = response.text.strip()
                
                responses.append({
                    "comment": comment,
                    "persona": persona,
                    "response": response_text,
                    "timestamp": datetime.now().isoformat()
                })
                
            except Exception as e:
                logger.error(f"Persona yanıtı oluşturma hatası: {e}")
                continue
        
        return {
            "success": True,
            "responses": responses,
            "video_id": video_id
        }
    
    def optimize_seo(self, title: str, description: str, tags: List[str], 
                    niche: str, language: str = "TR") -> Dict[str, Any]:
        """SEO optimizasyonu"""
        
        prompt = f"""
        Bu video metadatasını YouTube SEO'su için optimize et.
        
        Başlık: {title}
        Açıklama: {description}
        Etiketler: {', '.join(tags)}
        Niş: {niche}
        Dil: {language}
        
        Şu elementleri optimize et:
        1. SEO dostu başlık (60 karakter içinde)
        2. Optimizeli açıklama (ilk 2 satır önemli)
        3. Etkili etiketler (geniş ve niş spesifik)
        4. Anahtar kelime yoğunluğu
        5. Trend uyumluluğu
        
        Sonuçları JSON formatında döndür:
        {{
            "optimized_title": "...",
            "optimized_description": "...",
            "optimized_tags": ["...", "..."],
            "seo_score": 85,
            "suggestions": ["...", "..."]
        }}
        """
        
        try:
            response = self.model.generate_content(prompt)
            response_text = response.text
            
            # JSON extract et
            json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
            if json_match:
                seo_data = json.loads(json_match.group())
            else:
                seo_data = {"error": "JSON parse edilemedi"}
            
            return {
                "success": True,
                "seo_optimization": seo_data,
                "original_metadata": {
                    "title": title,
                    "description": description,
                    "tags": tags
                }
            }
            
        except Exception as e:
            logger.error(f"SEO optimizasyonu hatası: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def _create_script_prompt(self, topic: str, language: str, style: str, 
                            target_duration: int, keywords: List[str]) -> str:
        """Senaryo prompt'u oluştur"""
        
        language_instructions = {
            "TR": "Senaryoyu Türkçe yazın",
            "EN": "Write the script in English",
            "DE": "Schreiben Sie das Skript auf Deutsch",
            "FR": "Écrivez le script en français",
            "ES": "Escribe el guion en español"
        }
        
        style_instructions = {
            "engaging": "Dikkat çekici, enerjik ve izleyiciyi bağlayan",
            "educational": "Bilgilendirici, öğretici ve net",
            "entertainment": "Eğlenceli, komik ve viral potansiyeli yüksek"
        }
        
        keywords_str = ", ".join(keywords) if keywords else ""
        
        prompt = f"""
        YouTube için {target_duration} saniyelik ({int(target_duration/60)} dakika) video senaryosu oluştur.
        
        Konu: {topic}
        Dil: {language_instructions.get(language, language_instructions["TR"])}
        Stil: {style_instructions.get(style, style_instructions["engaging"])}
        Hedef anahtar kelimeler: {keywords_str}
        
        Senaryo şu yapıda olmalı:
        
        1. KANCA (Hook) - İlk 3 saniye:
        - Dikkat çekici açılış
        - Şok eden veya merak uyandıran ifade
        
        2. ANA İÇERİK ({target_duration-30} saniye):
        - 3-4 ana bölüm
        - Her bölüm 15-20 saniye
        - Görsel efektler ve geçişler için notlar
        
        3. EYLEM ÇAĞRISI (CTA) - Son 10 saniye:
        - Abone olma çağrısı
        - Yorum teşviki
        - Sonraki video hint'i
        
        Format:
        {{
            "title": "Dikkat çekici başlık",
            "hook": "3 saniyelik kancı metni",
            "main_content": [
                {{
                    "section": 1,
                    "text": "Bölüm metni",
                    "duration": 20,
                    "visual_notes": "Görsel notlar"
                }}
            ],
            "cta": "Eylem çağrısı metni",
            "estimated_retention": 85,
            "emotional_arc": ["curiosity", "excitement", "satisfaction"],
            "keywords_used": ["keyword1", "keyword2"]
        }}
        """
        
        return prompt
    
    def _parse_script(self, script_text: str, language: str) -> Dict[str, Any]:
        """Senaryo metnini parse et"""
        try:
            # JSON extract et
            json_match = re.search(r'\{.*\}', script_text, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
            else:
                # Manuel parse et
                return self._parse_script_manually(script_text, language)
        except:
            return {
                "title": "Oluşturulan Senaryo",
                "hook": script_text[:200],
                "main_content": [{"section": 1, "text": script_text, "duration": 300}],
                "cta": "Abone olun ve yorum yapın!",
                "estimated_retention": 75
            }
    
    def _parse_script_manually(self, text: str, language: str) -> Dict[str, Any]:
        """Manuel senaryo parse"""
        lines = text.split('\n')
        lines = [line.strip() for line in lines if line.strip()]
        
        # Basit parse logic
        hook = lines[0] if lines else "Dikkat çekici başlangıç"
        main_content = text
        cta = "Abone olun ve bildirimleri açın!"
        
        return {
            "title": "AI Oluşturulan Senaryo",
            "hook": hook,
            "main_content": [{"section": 1, "text": main_content, "duration": 300}],
            "cta": cta,
            "estimated_retention": 75
        }
    
    def _parse_ideas_manually(self, text: str) -> List[Dict[str, Any]]:
        """Manuel içerik fikri parse"""
        # Basit parse - gerçek implementasyonda daha gelişmiş olmalı
        ideas = []
        lines = text.split('\n')
        
        current_idea = {}
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            if line.startswith(('1.', '2.', '3.', '4.', '5.', '6.', '7.', '8.', '9.', '10.')):
                if current_idea:
                    ideas.append(current_idea)
                current_idea = {"title": line[3:].strip()}
            elif line.startswith('-'):
                if "başlık" in line.lower():
                    current_idea["title"] = line.split(':', 1)[1].strip() if ':' in line else line[1:].strip()
        
        if current_idea:
            ideas.append(current_idea)
        
        # Eğer parse edilemediyse varsayılan fikirler döndür
        if not ideas:
            ideas = [
                {"title": "Nişinizle ilgili viral video fikri 1"},
                {"title": "Nişinizle ilgili viral video fikri 2"},
                {"title": "Nişinizle ilgili viral video fikri 3"}
            ]
        
        return ideas
