"""
VUC-2026 Upload API Endpoints
Video yükleme ve medya yönetimi için endpoint'ler
"""

from fastapi import APIRouter, HTTPException, UploadFile, File, BackgroundTasks
from fastapi.responses import JSONResponse
from typing import Dict, List, Any, Optional
import logging
import os
import uuid
from datetime import datetime

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/upload", tags=["upload"])

@router.post("/video")
async def upload_video(
    background_tasks: BackgroundTasks,
    video: UploadFile = File(...),
    title: str = "",
    description: str = "",
    tags: str = ""
) -> Dict[str, Any]:
    """Video yükle"""
    try:
        # Benzersiz dosya adı oluştur
        file_id = str(uuid.uuid4())
        file_extension = os.path.splitext(video.filename)[1]
        filename = f"{file_id}{file_extension}"
        
        # Videoyu kaydet
        upload_dir = "uploads/videos"
        os.makedirs(upload_dir, exist_ok=True)
        
        file_path = os.path.join(upload_dir, filename)
        
        with open(file_path, "wb") as buffer:
            content = await video.read()
            buffer.write(content)
        
        # Video bilgileri
        video_info = {
            "file_id": file_id,
            "filename": filename,
            "original_name": video.filename,
            "title": title,
            "description": description,
            "tags": [tag.strip() for tag in tags.split(",") if tag.strip()],
            "file_size": len(content),
            "content_type": video.content_type,
            "upload_time": datetime.now().isoformat(),
            "status": "uploaded"
        }
        
        # Arka planda video işleme
        background_tasks.add_task(process_uploaded_video, file_path, video_info)
        
        return {
            "success": True,
            "video_info": video_info,
            "message": "Video başarıyla yüklendi, işleme başladı"
        }
        
    except Exception as e:
        logger.error(f"Video yükleme hatası: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/image")
async def upload_image(
    image: UploadFile = File(...),
    category: str = "thumbnail"
) -> Dict[str, Any]:
    """Görüntü yükle"""
    try:
        # Benzersiz dosya adı oluştur
        file_id = str(uuid.uuid4())
        file_extension = os.path.splitext(image.filename)[1]
        filename = f"{file_id}{file_extension}"
        
        # Görüntüyü kaydet
        upload_dir = f"uploads/images/{category}"
        os.makedirs(upload_dir, exist_ok=True)
        
        file_path = os.path.join(upload_dir, filename)
        
        with open(file_path, "wb") as buffer:
            content = await image.read()
            buffer.write(content)
        
        image_info = {
            "file_id": file_id,
            "filename": filename,
            "original_name": image.filename,
            "category": category,
            "file_size": len(content),
            "content_type": image.content_type,
            "upload_time": datetime.now().isoformat(),
            "file_path": file_path
        }
        
        return {
            "success": True,
            "image_info": image_info,
            "message": "Görüntü başarıyla yüklendi"
        }
        
    except Exception as e:
        logger.error(f"Görüntü yükleme hatası: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/audio")
async def upload_audio(
    audio: UploadFile = File(...),
    language: str = "tr"
) -> Dict[str, Any]:
    """Ses dosyası yükle"""
    try:
        # Benzersiz dosya adı oluştur
        file_id = str(uuid.uuid4())
        file_extension = os.path.splitext(audio.filename)[1]
        filename = f"{file_id}{file_extension}"
        
        # Ses dosyasını kaydet
        upload_dir = "uploads/audio"
        os.makedirs(upload_dir, exist_ok=True)
        
        file_path = os.path.join(upload_dir, filename)
        
        with open(file_path, "wb") as buffer:
            content = await audio.read()
            buffer.write(content)
        
        audio_info = {
            "file_id": file_id,
            "filename": filename,
            "original_name": audio.filename,
            "language": language,
            "file_size": len(content),
            "content_type": audio.content_type,
            "upload_time": datetime.now().isoformat(),
            "file_path": file_path
        }
        
        return {
            "success": True,
            "audio_info": audio_info,
            "message": "Ses dosyası başarıyla yüklendi"
        }
        
    except Exception as e:
        logger.error(f"Ses dosyası yükleme hatası: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/uploads")
async def get_uploads(
    file_type: str = "video",
    limit: int = 50,
    offset: int = 0
) -> Dict[str, Any]:
    """Yüklenen dosyaları listele"""
    try:
        upload_dir = f"uploads/{file_type}"
        uploads = []
        
        if os.path.exists(upload_dir):
            files = os.listdir(upload_dir)
            files.sort(key=lambda x: os.path.getmtime(os.path.join(upload_dir, x)), reverse=True)
            
            for filename in files[offset:offset + limit]:
                file_path = os.path.join(upload_dir, filename)
                stat = os.stat(file_path)
                
                uploads.append({
                    "filename": filename,
                    "file_size": stat.st_size,
                    "upload_time": datetime.fromtimestamp(stat.st_mtime).isoformat(),
                    "file_path": file_path
                })
        
        return {
            "success": True,
            "uploads": uploads,
            "total": len(uploads),
            "file_type": file_type
        }
        
    except Exception as e:
        logger.error(f"Yüklenen dosyaları listeleme hatası: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/upload/{file_id}")
async def delete_upload(file_id: str, file_type: str = "video") -> Dict[str, Any]:
    """Yüklenen dosyayı sil"""
    try:
        upload_dir = f"uploads/{file_type}"
        
        # Dosyayı bul
        target_file = None
        if os.path.exists(upload_dir):
            for filename in os.listdir(upload_dir):
                if filename.startswith(file_id):
                    target_file = os.path.join(upload_dir, filename)
                    break
        
        if not target_file or not os.path.exists(target_file):
            raise HTTPException(status_code=404, detail="Dosya bulunamadı")
        
        # Dosyayı sil
        os.remove(target_file)
        
        return {
            "success": True,
            "message": "Dosya başarıyla silindi",
            "file_id": file_id,
            "file_type": file_type
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Dosya silme hatası: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/upload/{file_id}/info")
async def get_upload_info(file_id: str, file_type: str = "video") -> Dict[str, Any]:
    """Yüklenen dosya bilgisini al"""
    try:
        upload_dir = f"uploads/{file_type}"
        
        # Dosyayı bul
        target_file = None
        if os.path.exists(upload_dir):
            for filename in os.listdir(upload_dir):
                if filename.startswith(file_id):
                    target_file = os.path.join(upload_dir, filename)
                    break
        
        if not target_file or not os.path.exists(target_file):
            raise HTTPException(status_code=404, detail="Dosya bulunamadı")
        
        # Dosya bilgileri
        stat = os.stat(target_file)
        
        file_info = {
            "file_id": file_id,
            "filename": os.path.basename(target_file),
            "file_size": stat.st_size,
            "upload_time": datetime.fromtimestamp(stat.st_mtime).isoformat(),
            "file_path": target_file,
            "file_type": file_type
        }
        
        return {
            "success": True,
            "file_info": file_info
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Dosya bilgisi alma hatası: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Arka plan görevleri
async def process_uploaded_video(file_path: str, video_info: Dict[str, Any]):
    """Yüklenen videoyu işle"""
    try:
        # Video analiz et
        # Thumbnail oluştur
        # Metadata çıkar
        # Veritabanına kaydet
        
        logger.info(f"Video işleme başladı: {video_info['file_id']}")
        
        # Burada video işleme adımları yapılacak
        # Şimdilik loglama
        
        logger.info(f"Video işleme tamamlandı: {video_info['file_id']}")
        
    except Exception as e:
        logger.error(f"Video işleme hatası: {e}")

# Yardımcı fonksiyonlar
def get_file_size_mb(size_bytes: int) -> float:
    """Byte'ı MB'ye çevir"""
    return round(size_bytes / (1024 * 1024), 2)

def is_valid_video_file(filename: str) -> bool:
    """Geçerli video dosyası kontrolü"""
    valid_extensions = ['.mp4', '.avi', '.mov', '.mkv', '.wmv', '.flv', '.webm']
    return any(filename.lower().endswith(ext) for ext in valid_extensions)

def is_valid_image_file(filename: str) -> bool:
    """Geçerli görüntü dosyası kontrolü"""
    valid_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp']
    return any(filename.lower().endswith(ext) for ext in valid_extensions)

def is_valid_audio_file(filename: str) -> bool:
    """Geçerli ses dosyası kontrolü"""
    valid_extensions = ['.mp3', '.wav', '.flac', '.aac', '.ogg', '.m4a']
    return any(filename.lower().endswith(ext) for ext in valid_extensions)
