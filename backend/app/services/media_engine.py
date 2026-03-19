import ffmpeg
import edge_tts
import asyncio
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import requests
import os
import logging
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime
import json
import random

logger = logging.getLogger(__name__)

class MediaEngine:
    """Medya üretim motoru - FFmpeg + edge-tts + Görsel işleme"""
    
    def __init__(self):
        self.temp_dir = "../temp"
        self.assets_dir = "../assets"
        self.output_dir = "../static/videos"
        
        # Dizinleri oluştur
        os.makedirs(self.temp_dir, exist_ok=True)
        os.makedirs(self.assets_dir, exist_ok=True)
        os.makedirs(self.output_dir, exist_ok=True)
        
        # Varsayılan ses profilleri
        self.voice_profiles = {
            "TR": "tr-TR-AhmetNeural",
            "EN": "en-US-JennyNeural",
            "DE": "de-DE-KatjaNeural", 
            "FR": "fr-FR-DeniseNeural",
            "ES": "es-ES-ElviraNeural"
        }
    
    async def generate_speech(self, text: str, language: str = "TR", 
                            voice_profile: str = None, output_path: str = None,
                            emotional_style: str = "engaging") -> str:
        """
        Metinden konuşma (TTS) oluştur - SSML destekli
        
        Args:
            text: Okunacak metin
            language: Dil kodu
            voice_profile: Özel ses profili
            output_path: Çıktı dosya yolu
            emotional_style: Duygusal üslup (engaging, serious, energetic, calm)
        
        Returns:
            Oluşturulan ses dosyasının yolu
        """
        
        if not voice_profile:
            voice_profile = self.voice_profiles.get(language, self.voice_profiles["TR"])
        
        if not output_path:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = os.path.join(self.temp_dir, f"speech_{timestamp}.mp3")
        
        try:
            # SSML formatında metin oluştur - duygusal vurgularla
            ssml_text = self._create_emotional_ssml(text, language, emotional_style)
            
            # edge-tts ile ses oluştur
            communicate = edge_tts.Communicate(ssml_text, voice_profile)
            await communicate.save(output_path)
            
            logger.info(f"Duygusal ses dosyası oluşturuldu: {output_path}")
            return output_path
            
        except Exception as e:
            logger.error(f"TTS oluşturma hatası: {e}")
            raise
    
    def _create_emotional_ssml(self, text: str, language: str, emotional_style: str) -> str:
        """Duygusal SSML oluştur"""
        
        # Duygusal stillere göre ayarlar
        style_configs = {
            "engaging": {
                "rate": "0.95",
                "pitch": "+5%",
                "volume": "+10%",
                "emphasis": "moderate",
                "pause_duration": "500ms"
            },
            "serious": {
                "rate": "0.85",
                "pitch": "-2%",
                "volume": "0%",
                "emphasis": "strong",
                "pause_duration": "700ms"
            },
            "energetic": {
                "rate": "1.15",
                "pitch": "+10%",
                "volume": "+15%",
                "emphasis": "strong",
                "pause_duration": "300ms"
            },
            "calm": {
                "rate": "0.90",
                "pitch": "0%",
                "volume": "-5%",
                "emphasis": "none",
                "pause_duration": "800ms"
            }
        }
        
        config = style_configs.get(emotional_style, style_configs["engaging"])
        
        # Metni cümlelere ayır ve SSML tag'leri ekle
        sentences = self._split_sentences(text)
        ssml_parts = []
        
        for i, sentence in enumerate(sentences):
            # Önemli kelimeleri vurgula
            emphasized_sentence = self._add_emphasis(sentence, config["emphasis"])
            
            # Cümleyi SSML formatına çevir
            if i == 0:
                # İlk cümle - daha güçlü
                ssml_sentence = f"""
                <prosody rate="{config["rate"]}" pitch="{config["pitch"]}" volume="{config["volume"]}">
                    <emphasis level="{config["emphasis"]}">{emphasized_sentence}</emphasis>
                </prosody>
                """
            else:
                # Diğer cümleler
                ssml_sentence = f"""
                <prosody rate="{config["rate"]}" pitch="{config["pitch"]}" volume="{config["volume"]}">
                    {emphasized_sentence}
                </prosody>
                <break time="{config["pause_duration"]}"/>
                """
            
            ssml_parts.append(ssml_sentence)
        
        # Tam SSML dokümanı oluştur
        ssml_text = f"""
        <speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xml:lang="{language}">
            {''.join(ssml_parts)}
        </speak>
        """
        
        return ssml_text.strip()
    
    def _split_sentences(self, text: str) -> List[str]:
        """Metni cümlelere ayır"""
        import re
        # Türkçe ve İngilizce cümle ayırıcıları
        sentences = re.split(r'[.!?]+', text)
        return [s.strip() for s in sentences if s.strip()]
    
    def _add_emphasis(self, sentence: str, emphasis_level: str) -> str:
        """Cümleye vurgu ekle"""
        if emphasis_level == "none":
            return sentence
        
        # Önemli kelimeleri tespit et
        important_words = [
            "şok", "inanılmaz", "kesinlikle", "tamamen", "mutlaka",
            "shock", "unbelievable", "absolutely", "completely", "must",
            "büyük", "harika", "mükemmel", "inanılmaz",
            "huge", "amazing", "perfect", "incredible"
        ]
        
        words = sentence.split()
        emphasized_words = []
        
        for word in words:
            word_clean = word.lower().strip('.,!?')
            if any(important_word in word_clean for important_word in important_words):
                # Önemli kelimeyi vurgula
                word_with_emphasis = f'<emphasis level="strong">{word}</emphasis>'
                emphasized_words.append(word_with_emphasis)
            else:
                emphasized_words.append(word)
        
        return ' '.join(emphasized_words)
    
    def fetch_stock_media(self, query: str, media_type: str = "video", 
                         duration: int = 30, count: int = 5) -> List[str]:
            Medya dosya yolları listesi
        """
        
        media_files = []
        
        # Pexels API (API key gerekli)
        try:
            # Burada gerçek API implementasyonu olacak
            # Şimdilik placeholder
            for i in range(count):
                # Simüle edilmiş medya dosyası
                filename = f"stock_{media_type}_{i}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp4"
                filepath = os.path.join(self.assets_dir, filename)
                
                # Gerçek implementasyonda burada indirme yapılacak
                media_files.append(filepath)
                
        except Exception as e:
            logger.error(f"Stok medya getirme hatası: {e}")
        
        return media_files
    
    def create_hormozi_captions(self, video_path: str, script_text: str, 
                             output_path: str = None) -> str:
        """
        Hormozi stili altyazı oluştur
        
        Args:
            video_path: Video dosya yolu
            script_text: Senaryo metni
            output_path: Çıktı dosya yolu
        
        Returns:
            Altyazılı video dosya yolu
        """
        
        if not output_path:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = os.path.join(self.output_dir, f"video_captions_{timestamp}.mp4")
        
        try:
            # Kelimeleri ve zamanlamaları hesapla
            words = script_text.split()
            total_duration = self._get_video_duration(video_path)
            words_per_second = len(words) / total_duration
            
            # FFmpeg ile altyazıları ekle
            caption_filter = self._create_hormozi_caption_filter(words, words_per_second)
            
            (
                ffmpeg
                .input(video_path)
                .filter('drawtext', **caption_filter)
                .output(output_path, vcodec='libx264', acodec='copy')
                .overwrite_output()
                .run(quiet=True)
            )
            
            logger.info(f"Hormozi altyazılı video oluşturuldu: {output_path}")
            return output_path
            
        except Exception as e:
            logger.error(f"Altyazı oluşturma hatası: {e}")
            raise
    
    def smart_crop_to_shorts(self, video_path: str, output_path: str = None) -> str:
        """
        16:9 videoyu 9:16 (Shorts) formatına akıllı kırp
        
        Args:
            video_path: Giriş video yolu
            output_path: Çıktı dosya yolu
        
        Returns:
            Kırpılmış video yolu
        """
        
        if not output_path:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = os.path.join(self.output_dir, f"shorts_{timestamp}.mp4")
        
        try:
            # Video bilgilerini al
            cap = cv2.VideoCapture(video_path)
            width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            fps = cap.get(cv2.CAP_PROP_FPS)
            cap.release()
            
            # 9:16 oranında merkez kırpma
            if width/height > 9/16:  # Geniş video
                crop_width = int(height * 9/16)
                crop_x = (width - crop_width) // 2
                crop_params = f"crop={crop_width}:{height}:{crop_x}:0"
            else:  # Dar video
                crop_height = int(width * 16/9)
                crop_y = (height - crop_height) // 2
                crop_params = f"crop={width}:{crop_height}:0:{crop_y}"
            
            # FFmpeg ile kırp
            (
                ffmpeg
                .input(video_path)
                .filter('crop', crop_params)
                .filter('scale', 1080, 1920)
                .output(output_path, vcodec='libx264', preset='fast', crf=23)
                .overwrite_output()
                .run(quiet=True)
            )
            
            logger.info(f"Shorts formatına çevrildi: {output_path}")
            return output_path
            
        except Exception as e:
            logger.error(f"Video kırpma hatası: {e}")
            raise
    
    def apply_sidechain_ducking(self, video_path: str, music_path: str, 
                              speech_path: str, output_path: str = None) -> str:
        """
        Sidechain ducking ile ses miksleme
        
        Args:
            video_path: Video dosya yolu
            music_path: Arka plan müziği
            speech_path: Konuşma dosyası
            output_path: Çıktı dosya yolu
        
        Returns:
            Mikslenmiş video yolu
        """
        
        if not output_path:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = os.path.join(self.output_dir, f"mixed_{timestamp}.mp4")
        
        try:
            # Sidechain ducking filtresi
            sidechain_filter = (
                f"[1:a]asplit=2[sc][mix];"
                f"[2:a]volume=0.15[music];"
                f"[music][sc]sidechaincompress=threshold=-30dB:ratio=4:release=200[ducked];"
                f"[ducked][mix]amix=inputs=2:weights=1 0.3"
            )
            
            # FFmpeg ile miksle
            (
                ffmpeg
                .input(video_path)
                .input(music_path)
                .input(speech_path)
                .filter_complex(sidechain_filter)
                .output(output_path, vcodec='copy', acodec='aac')
                .overwrite_output()
                .run(quiet=True)
            )
            
            logger.info(f"Sidechain miksleme tamamlandı: {output_path}")
            return output_path
            
        except Exception as e:
            logger.error(f"Ses miksleme hatası: {e}")
            raise
    
    def create_thumbnail(self, title: str, style: str = "hormozi", 
                        output_path: str = None) -> str:
        """
        Thumbnail oluştur
        
        Args:
            title: Video başlığı
            style: Thumbnail stili
            output_path: Çıktı dosya yolu
        
        Returns:
            Thumbnail dosya yolu
        """
        
        if not output_path:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = os.path.join(self.output_dir, f"thumbnail_{timestamp}.jpg")
        
        try:
            # Canvas oluştur
            img = Image.new('RGB', (1280, 720), color='black')
            draw = ImageDraw.Draw(img)
            
            if style == "hormozi":
                # Hormozi stili - sarı arka plan, kalın font
                img = Image.new('RGB', (1280, 720), color='yellow')
                draw = ImageDraw.Draw(img)
                
                # Başlığı yaz (font gerekli)
                # Burada font yükleme yapılacak
                title_lines = self._wrap_text(title, 30)
                y_pos = 200
                
                for line in title_lines:
                    # Basit text çizimi (gerçek implementasyonda font kullanılacak)
                    draw.text((100, y_pos), line.upper(), fill='black')
                    y_pos += 80
            
            elif style == "minimal":
                # Minimal stil
                img = Image.new('RGB', (1280, 720), color='white')
                draw = ImageDraw.Draw(img)
                draw.text((100, 300), title, fill='black')
            
            elif style == "bold":
                # Kalın stil
                img = Image.new('RGB', (1280, 720), color='red')
                draw = ImageDraw.Draw(img)
                draw.text((100, 300), title.upper(), fill='white')
            
            img.save(output_path)
            logger.info(f"Thumbnail oluşturuldu: {output_path}")
            return output_path
            
        except Exception as e:
            logger.error(f"Thumbnail oluşturma hatası: {e}")
            raise
    
    async def render_video(self, script_data: Dict[str, Any], media_files: List[str], 
                    output_path: str = None) -> str:
        """
        Tam video render işlemi
        
        Args:
            script_data: Senaryo verisi
            media_files: Medya dosyaları listesi
            output_path: Çıktı dosya yolu
        
        Returns:
            Render edilmiş video yolu
        """
        
        if not output_path:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = os.path.join(self.output_dir, f"final_video_{timestamp}.mp4")
        
        try:
            # Adım 1: Konuşma oluştur
            speech_text = script_data.get('main_content', '')
            speech_path = await self.generate_speech(speech_text)
            
            # Adım 2: Medya dosyalarını birleştir
            if media_files:
                # Video concatenation
                concat_list = os.path.join(self.temp_dir, "concat_list.txt")
                with open(concat_list, 'w') as f:
                    for media_file in media_files:
                        f.write(f"file '{media_file}'\n")
                
                merged_video = os.path.join(self.temp_dir, "merged_video.mp4")
                (
                    ffmpeg
                    .input(concat_list, format='concat', safe=0)
                    .output(merged_video, c='copy')
                    .overwrite_output()
                    .run(quiet=True)
                )
            else:
                # Varsayılan siyah video
                merged_video = self._create_placeholder_video(len(speech_text.split()) * 0.5)
            
            # Adım 3: Altyazı ekle
            captioned_video = self.create_hormozi_captions(merged_video, speech_text)
            
            # Adım 4: Ses miksleme
            # Arka plan müziği ekle
            music_path = self._get_background_music()
            if music_path and os.path.exists(music_path):
                final_video = self.apply_sidechain_ducking(captioned_video, music_path, speech_path)
            else:
                # Sadece konuşmayı ekle
                final_video = os.path.join(self.output_dir, f"final_{timestamp}.mp4")
                (
                    ffmpeg
                    .input(captioned_video)
                    .input(speech_path)
                    .output(final_video, vcodec='copy', acodec='aac')
                    .overwrite_output()
                    .run(quiet=True)
                )
            
            # Adım 5: Thumbnail oluştur
            title = script_data.get('title', 'Video Başlığı')
            thumbnail_path = self.create_thumbnail(title)
            
            logger.info(f"Video render tamamlandı: {final_video}")
            return final_video
            
        except Exception as e:
            logger.error(f"Video render hatası: {e}")
            raise
    
    def _get_video_duration(self, video_path: str) -> float:
        """Video süresini al"""
        try:
            probe = ffmpeg.probe(video_path)
            duration = float(probe['streams'][0]['duration'])
            return duration
        except:
            return 30.0  # Varsayılan süre
    
    def _create_hormozi_caption_filter(self, words: List[str], words_per_second: float) -> Dict:
        """Hormozi stili altyazı filtresi oluştur"""
        
        # Dinamik renkler ve fontlar
        colors = ['yellow', 'white', 'red', 'cyan']
        current_color = 0
        
        # Her kelime için zamanlama hesapla
        captions = []
        for i, word in enumerate(words):
            start_time = i / words_per_second
            end_time = (i + 1) / words_per_second
            
            color = colors[current_color % len(colors)]
            current_color += 1
            
            caption = {
                'text': word,
                'start': start_time,
                'end': end_time,
                'color': color,
                'fontsize': 48,
                'x': '(w-text_w)/2',
                'y': 'h-100'
            }
            captions.append(caption)
        
        # FFmpeg drawtext filter string oluştur
        filter_parts = []
        for caption in captions:
            filter_part = (
                f"drawtext=text='{caption['text']}':"
                f"fontsize={caption['fontsize']}:"
                f"fontcolor={caption['color']}:"
                f"x={caption['x']}:y={caption['y']}:"
                f"enable='between(t,{caption['start']},{caption['end']})'"
            )
            filter_parts.append(filter_part)
        
        return ','.join(filter_parts)
    
    def _wrap_text(self, text: str, max_chars: int) -> List[str]:
        """Metni satırlara böl"""
        words = text.split()
        lines = []
        current_line = ""
        
        for word in words:
            if len(current_line + word) <= max_chars:
                current_line += word + " "
            else:
                lines.append(current_line.strip())
                current_line = word + " "
        
        if current_line:
            lines.append(current_line.strip())
        
        return lines
    
    def _create_placeholder_video(self, duration: float) -> str:
        """Placeholder video oluştur"""
        output_path = os.path.join(self.temp_dir, "placeholder.mp4")
        
        (
            ffmpeg
            .input('color=c=black:s=1920x1080:d={duration}', f='lavfi')
            .output(output_path, vcodec='libx264', preset='fast', crf=23)
            .overwrite_output()
            .run(quiet=True)
        )
        
        return output_path
    
    def _get_background_music(self) -> str:
        """Arka plan müziği getir"""
        # Burada stok müzik kütüphanesi olacak
        music_files = [
            os.path.join(self.assets_dir, "background_music_1.mp3"),
            os.path.join(self.assets_dir, "background_music_2.mp3"),
        ]
        
        for music_file in music_files:
            if os.path.exists(music_file):
                return music_file
        
        return None
