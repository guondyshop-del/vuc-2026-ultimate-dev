"""
VUC-2026 Video Rendering Service
Otomatik video üretim pipeline'ı
"""

import logging
import asyncio
import subprocess
import os
import json
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime, timedelta
from pathlib import Path
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import tempfile
import shutil

logger = logging.getLogger(__name__)

class VideoRenderingService:
    """Video rendering servisi"""
    
    def __init__(self):
        self.temp_dir = Path("temp/video_rendering")
        self.output_dir = Path("outputs/videos")
        self.assets_dir = Path("assets/media")
        
        # Dizinleri oluştur
        self.temp_dir.mkdir(parents=True, exist_ok=True)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.assets_dir.mkdir(parents=True, exist_ok=True)
        
        # FFmpeg kontrolü
        self._check_ffmpeg()
    
    def _check_ffmpeg(self):
        """FFmpeg kurulu mu kontrol et"""
        try:
            subprocess.run(["ffmpeg", "-version"], capture_output=True, check=True)
            logger.info("FFmpeg bulundu")
        except (subprocess.CalledProcessError, FileNotFoundError):
            logger.warning("FFmpeg bulunamadı, mock rendering kullanılacak")
    
    async def render_video(
        self,
        script_data: Dict[str, Any],
        video_config: Dict[str, Any],
        media_assets: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """Video render et"""
        try:
            start_time = datetime.now()
            
            # Render job ID oluştur
            render_id = f"render_{int(start_time.timestamp())}"
            
            # Render sürecini başlat
            logger.info(f"Video render başlatıldı: {render_id}")
            
            # 1. Script'i parse et
            parsed_script = self._parse_script(script_data)
            
            # 2. Media assets hazırla
            prepared_assets = await self._prepare_media_assets(media_assets or {})
            
            # 3. Video segmentlerini oluştur
            video_segments = await self._create_video_segments(parsed_script, prepared_assets, video_config)
            
            # 4. Segmentleri birleştir
            final_video = await self._merge_segments(video_segments, render_id)
            
            # 5. Ses ekle
            video_with_audio = await self._add_audio(final_video, script_data, render_id)
            
            # 6. Altyazı ekle
            subtitled_video = await self._add_subtitles(video_with_audio, parsed_script, render_id)
            
            # 7. Shadowban shield uygula
            protected_video = await self._apply_shadowban_protection(subtitled_video, render_id)
            
            processing_time = (datetime.now() - start_time).total_seconds()
            
            return {
                "success": True,
                "render_id": render_id,
                "video_path": str(protected_video),
                "duration": video_config.get("duration_minutes", 10) * 60,
                "resolution": video_config.get("resolution", "1920x1080"),
                "fps": video_config.get("fps", 30),
                "processing_time": processing_time,
                "file_size": os.path.getsize(protected_video),
                "message": "Video başarıyla render edildi"
            }
            
        except Exception as e:
            logger.error(f"Video rendering failed: {e}")
            return {
                "success": False,
                "error": str(e),
                "message": "Video render başarısız"
            }
    
    def _parse_script(self, script_data: Dict[str, Any]) -> Dict[str, Any]:
        """Script'i parse et"""
        content = script_data.get("content", "")
        
        # Basit script parsing
        sections = []
        current_section = {"type": "intro", "content": "", "duration": 15}
        
        lines = content.split('\n')
        for line in lines:
            line = line.strip()
            
            if line.startswith("##"):
                # Yeni bölüm
                if current_section["content"]:
                    sections.append(current_section)
                
                section_title = line.replace("##", "").strip()
                section_type = "main"
                if "intro" in section_title.lower():
                    section_type = "intro"
                elif "sonuç" in section_title.lower() or "conclusion" in section_title.lower():
                    section_type = "outro"
                
                current_section = {
                    "type": section_type,
                    "title": section_title,
                    "content": "",
                    "duration": 30 if section_type == "main" else 15
                }
            elif line and not line.startswith("#"):
                current_section["content"] += line + " "
        
        if current_section["content"]:
            sections.append(current_section)
        
        return {
            "sections": sections,
            "total_duration": sum(section["duration"] for section in sections),
            "title": script_data.get("title", "Video")
        }
    
    async def _prepare_media_assets(self, media_assets: Dict[str, Any]) -> Dict[str, Any]:
        """Media assets hazırla"""
        prepared = {
            "background_music": media_assets.get("background_music", "default.mp3"),
            "video_clips": media_assets.get("video_clips", []),
            "images": media_assets.get("images", []),
            "sound_effects": media_assets.get("sound_effects", [])
        }
        
        # Default assets yoksa oluştur
        if not prepared["video_clips"]:
            prepared["video_clips"] = await self._generate_default_video_clips()
        
        if not prepared["images"]:
            prepared["images"] = await self._generate_default_images()
        
        return prepared
    
    async def _generate_default_video_clips(self) -> List[str]:
        """Default video klipler oluştur"""
        # Mock implementation - gerçek uygulamada stok videolar kullanılacak
        return [
            "tech_background_1.mp4",
            "tech_background_2.mp4", 
            "abstract_animation_1.mp4"
        ]
    
    async def _generate_default_images(self) -> List[str]:
        """Default görseller oluştur"""
        images = []
        
        # Basit renkli görseller oluştur
        colors = ["#3B82F6", "#8B5CF6", "#EC4899", "#10B981", "#F59E0B"]
        
        for i, color in enumerate(colors):
            image_path = self.temp_dir / f"generated_bg_{i}.png"
            
            # 1920x1080 görsel oluştur
            img = Image.new('RGB', (1920, 1080), color)
            draw = ImageDraw.Draw(img)
            
            # Basit desen ekle
            for x in range(0, 1920, 100):
                for y in range(0, 1080, 100):
                    draw.rectangle([x, y, x+50, y+50], fill="white", outline="white", width=2)
            
            img.save(image_path)
            images.append(str(image_path))
        
        return images
    
    async def _create_video_segments(
        self, 
        parsed_script: Dict[str, Any], 
        prepared_assets: Dict[str, Any],
        video_config: Dict[str, Any]
    ) -> List[str]:
        """Video segmentlerini oluştur"""
        segments = []
        sections = parsed_script.get("sections", [])
        
        for i, section in enumerate(sections):
            segment_path = self.temp_dir / f"segment_{i}.mp4"
            
            # Segment oluştur
            if self._is_ffmpeg_available():
                segment_path = await self._create_segment_with_ffmpeg(
                    section, prepared_assets, segment_path, video_config
                )
            else:
                segment_path = await self._create_mock_segment(segment_path, section)
            
            segments.append(str(segment_path))
        
        return segments
    
    def _is_ffmpeg_available(self) -> bool:
        """FFmpeg kullanılabilir mi"""
        try:
            subprocess.run(["ffmpeg", "-version"], capture_output=True, check=True)
            return True
        except:
            return False
    
    async def _create_segment_with_ffmpeg(
        self,
        section: Dict[str, Any],
        assets: Dict[str, Any],
        output_path: Path,
        config: Dict[str, Any]
    ) -> Path:
        """FFmpeg ile segment oluştur"""
        try:
            # Background video kullan
            bg_video = assets["video_clips"][i % len(assets["video_clips"])]
            bg_path = self.assets_dir / bg_video
            
            if not bg_path.exists():
                # Default görsel kullan
                bg_image = assets["images"][0]
                bg_path = Path(bg_image)
            
            duration = section.get("duration", 30)
            
            # FFmpeg komutu
            cmd = [
                "ffmpeg",
                "-y",  # Overwrite
                "-i", str(bg_path),
                "-t", str(duration),
                "-c:v", "libx264",
                "-preset", "fast",
                "-crf", "23",
                "-pix_fmt", "yuv420p",
                "-r", str(config.get("fps", 30)),
                "-vf", f"scale={config.get('resolution', '1920x1080').replace('x', ':')}",
                str(output_path)
            ]
            
            process = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            stdout, stderr = await process.communicate()
            
            if process.returncode != 0:
                logger.error(f"FFmpeg error: {stderr.decode()}")
                return await self._create_mock_segment(output_path, section)
            
            return output_path
            
        except Exception as e:
            logger.error(f"Segment creation failed: {e}")
            return await self._create_mock_segment(output_path, section)
    
    async def _create_mock_segment(self, output_path: Path, section: Dict[str, Any]) -> Path:
        """Mock segment oluştur"""
        # Basit renkli video oluştur
        duration = section.get("duration", 30)
        fps = 30
        
        # OpenCV ile basit video
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(str(output_path), fourcc, fps, (1920, 1080))
        
        frames = int(duration * fps)
        for frame_num in range(frames):
            # Gradient background
            frame = np.zeros((1080, 1920, 3), dtype=np.uint8)
            
            # Renk gradyanı
            for x in range(1920):
                color_value = int(255 * (x / 1920))
                frame[:, x] = [color_value, 100, 255 - color_value]
            
            # Section text
            cv2.putText(frame, section.get("title", "Video"), 
                       (100, 100), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 3)
            
            out.write(frame)
        
        out.release()
        return output_path
    
    async def _merge_segments(self, segments: List[str], render_id: str) -> Path:
        """Segmentleri birleştir"""
        try:
            output_path = self.output_dir / f"merged_{render_id}.mp4"
            
            if self._is_ffmpeg_available() and len(segments) > 1:
                # FFmpeg ile birleştir
                concat_file = self.temp_dir / f"concat_{render_id}.txt"
                
                with open(concat_file, 'w') as f:
                    for segment in segments:
                        f.write(f"file '{segment}'\n")
                
                cmd = [
                    "ffmpeg",
                    "-y",
                    "-f", "concat",
                    "-safe", "0",
                    "-i", str(concat_file),
                    "-c", "copy",
                    str(output_path)
                ]
                
                process = await asyncio.create_subprocess_exec(
                    *cmd,
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE
                )
                
                await process.communicate()
                
                if process.returncode == 0:
                    return output_path
            
            # Fallback: ilk segmenti kullan
            if segments:
                shutil.copy2(segments[0], output_path)
                return output_path
            else:
                # Boş video oluştur
                return await self._create_empty_video(output_path)
                
        except Exception as e:
            logger.error(f"Segment merge failed: {e}")
            return await self._create_empty_video(output_path)
    
    async def _create_empty_video(self, output_path: Path) -> Path:
        """Boş video oluştur"""
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(str(output_path), fourcc, 30, (1920, 1080))
        
        # 10 saniyelik siyah video
        for _ in range(300):
            frame = np.zeros((1080, 1920, 3), dtype=np.uint8)
            out.write(frame)
        
        out.release()
        return output_path
    
    async def _add_audio(self, video_path: Path, script_data: Dict[str, Any], render_id: str) -> Path:
        """Videoya ses ekle"""
        try:
            output_path = self.output_dir / f"audio_{render_id}.mp4"
            
            # Mock ses ekle - gerçek uygulamada TTS kullanılacak
            if self._is_ffmpeg_available():
                cmd = [
                    "ffmpeg",
                    "-y",
                    "-i", str(video_path),
                    "-i", "assets/audio/default.mp3",  # Default ses
                    "-c:v", "copy",
                    "-c:a", "aac",
                    "-shortest",
                    str(output_path)
                ]
                
                process = await asyncio.create_subprocess_exec(
                    *cmd,
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE
                )
                
                await process.communicate()
                
                if process.returncode == 0 and output_path.exists():
                    return output_path
            
            # Fallback: videoyu kopyala
            shutil.copy2(video_path, output_path)
            return output_path
            
        except Exception as e:
            logger.error(f"Audio addition failed: {e}")
            shutil.copy2(video_path, output_path)
            return output_path
    
    async def _add_subtitles(self, video_path: Path, parsed_script: Dict[str, Any], render_id: str) -> Path:
        """Altyazı ekle"""
        try:
            output_path = self.output_dir / f"subtitled_{render_id}.mp4"
            
            # Hormozi stili altyazı - çok renkli ve dikkat çekici
            if self._is_ffmpeg_available():
                # Altyazı dosyası oluştur
                subtitle_file = self.temp_dir / f"subs_{render_id}.srt"
                
                with open(subtitle_file, 'w', encoding='utf-8') as f:
                    current_time = 0
                    for section in parsed_script.get("sections", []):
                        duration = section.get("duration", 30)
                        
                        # Basit subtitle format
                        start_time = self._format_srt_time(current_time)
                        end_time = self._format_srt_time(current_time + duration)
                        
                        f.write(f"{len(f.readlines()) + 1}\n")
                        f.write(f"{start_time} --> {end_time}\n")
                        f.write(f"{section.get('title', '')}\n")
                        f.write(f"{section.get('content', '')[:100]}...\n\n")
                        
                        current_time += duration
                
                cmd = [
                    "ffmpeg",
                    "-y",
                    "-i", str(video_path),
                    "-i", str(subtitle_file),
                    "-c:v", "libx264",
                    "-c:a", "copy",
                    "-c:s", "mov_text",
                    "-metadata:s:s:0", "language=tur",
                    "-vf", "subtitles=subtitle_file",
                    str(output_path)
                ]
                
                process = await asyncio.create_subprocess_exec(
                    *cmd,
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE
                )
                
                await process.communicate()
                
                if process.returncode == 0 and output_path.exists():
                    return output_path
            
            # Fallback
            shutil.copy2(video_path, output_path)
            return output_path
            
        except Exception as e:
            logger.error(f"Subtitle addition failed: {e}")
            shutil.copy2(video_path, output_path)
            return output_path
    
    def _format_srt_time(self, seconds: float) -> str:
        """SRT zaman formatı"""
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        millis = int((seconds % 1) * 1000)
        return f"{hours:02d}:{minutes:02d}:{secs:02d},{millis:03d}"
    
    async def _apply_shadowban_protection(self, video_path: Path, render_id: str) -> Path:
        """Shadowban koruması uygula"""
        try:
            output_path = self.output_dir / f"protected_{render_id}.mp4"
            
            # Shadowban shield servisini çağır
            from .shadowban_shield import ShadowbanShield
            
            shield_config = {
                "pixel_noise_enabled": True,
                "pixel_noise_intensity": 0.1,
                "speed_variation_enabled": True,
                "speed_variation_range": (0.99, 1.01),
                "frame_jitter_enabled": True,
                "frame_jitter_intensity": 0.001
            }
            
            shield = ShadowbanShield(shield_config)
            
            video_assets = {
                "video_path": str(video_path),
                "duration": 600  # Mock duration
            }
            
            protected_assets = shield.apply_protection(video_assets)
            
            if protected_assets.get("video_path") and os.path.exists(protected_assets["video_path"]):
                return Path(protected_assets["video_path"])
            
            # Fallback: videoyu kopyala
            shutil.copy2(video_path, output_path)
            return output_path
            
        except Exception as e:
            logger.error(f"Shadowban protection failed: {e}")
            shutil.copy2(video_path, output_path)
            return output_path
    
    async def create_thumbnail(self, video_path: str, title: str, style: str = "default") -> str:
        """Video thumbnail oluştur"""
        try:
            thumbnail_path = self.output_dir / f"thumbnail_{int(datetime.now().timestamp())}.jpg"
            
            # Videodan frame al
            if self._is_ffmpeg_available():
                cmd = [
                    "ffmpeg",
                    "-y",
                    "-i", video_path,
                    "-ss", "00:00:05",  # 5. saniyeden frame al
                    "-vframes", "1",
                    "-q:v", "2",
                    str(thumbnail_path)
                ]
                
                process = await asyncio.create_subprocess_exec(
                    *cmd,
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE
                )
                
                await process.communicate()
                
                if thumbnail_path.exists():
                    # Thumbnail'a metin ekle
                    await self._add_text_to_thumbnail(thumbnail_path, title, style)
                    return str(thumbnail_path)
            
            # Fallback: default thumbnail
            return await self._create_default_thumbnail(title, style)
            
        except Exception as e:
            logger.error(f"Thumbnail creation failed: {e}")
            return await self._create_default_thumbnail(title, style)
    
    async def _add_text_to_thumbnail(self, thumbnail_path: Path, title: str, style: str):
        """Thumbnail'a metin ekle"""
        try:
            img = Image.open(thumbnail_path)
            draw = ImageDraw.Draw(img)
            
            # Hormozi stili - büyük, dikkat çekici metin
            try:
                font = ImageFont.truetype("arial.ttf", 60)
            except:
                font = ImageFont.load_default()
            
            # Metin kutusu
            text_bbox = draw.textbbox((0, 0), title, font=font)
            text_width = text_bbox[2] - text_bbox[0]
            text_height = text_bbox[3] - text_bbox[1]
            
            # Metni ortala
            x = (img.width - text_width) // 2
            y = img.height - text_height - 50
            
            # Arka plan kutusu
            padding = 20
            draw.rectangle(
                [x - padding, y - padding, x + text_width + padding, y + text_height + padding],
                fill="black"
            )
            
            # Metni çiz
            draw.text((x, y), title, fill="yellow", font=font)
            
            img.save(thumbnail_path)
            
        except Exception as e:
            logger.error(f"Text addition to thumbnail failed: {e}")
    
    async def _create_default_thumbnail(self, title: str, style: str) -> str:
        """Default thumbnail oluştur"""
        thumbnail_path = self.output_dir / f"default_thumb_{int(datetime.now().timestamp())}.jpg"
        
        # 1280x720 thumbnail
        img = Image.new('RGB', (1280, 720), '#1f2937')
        draw = ImageDraw.Draw(img)
        
        try:
            font = ImageFont.truetype("arial.ttf", 48)
        except:
            font = ImageFont.load_default()
        
        # Başlık ekle
        text_bbox = draw.textbbox((0, 0), title, font=font)
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]
        
        x = (1280 - text_width) // 2
        y = (720 - text_height) // 2
        
        draw.text((x, y), title, fill="white", font=font)
        
        img.save(thumbnail_path)
        return str(thumbnail_path)
    
    async def cleanup_temp_files(self, render_id: str):
        """Geçici dosyaları temizle"""
        try:
            pattern = f"*{render_id}*"
            for file_path in self.temp_dir.glob(pattern):
                try:
                    file_path.unlink()
                except:
                    pass
        except Exception as e:
            logger.error(f"Cleanup failed: {e}")
