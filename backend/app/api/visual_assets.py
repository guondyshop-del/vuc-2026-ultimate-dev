"""
VUC-2026 Visual Asset API Router
Endpoints for brand generation, thumbnails, banners, and social media assets
"""

from fastapi import APIRouter, HTTPException, BackgroundTasks
from typing import List, Dict, Optional, Any
from pydantic import BaseModel, Field
from datetime import datetime
import asyncio

from ..services.visual_asset_engine import visual_asset_engine, AssetType, BrandStyle, AssetSpecification, BrandGuidelines, GeneratedAsset

# Pydantic models for API requests/responses
class GenerateBrandIdentityRequest(BaseModel):
    channel_name: str = Field(..., min_length=3, max_length=50)
    niche: str = Field(..., min_length=3, max_length=30)
    target_audience: str = Field(..., min_length=10, max_length=100)

class GenerateBrandIdentityResponse(BaseModel):
    success: bool
    brand_guidelines: BrandGuidelines
    processing_time_ms: float

class GenerateThumbnailRequest(BaseModel):
    video_title: str = Field(..., min_length=10, max_length=100)
    video_description: Optional[str] = None
    brand_guidelines: BrandGuidelines
    optimization_target: str = Field(default="youtube_algorithm")
    template_preference: Optional[str] = None

class GenerateThumbnailResponse(BaseModel):
    success: bool
    asset: GeneratedAsset
    performance_metrics: Dict[str, Any]
    processing_time_ms: float

class GenerateSocialAdRequest(BaseModel):
    campaign_name: str = Field(..., min_length=5, max_length=50)
    ad_copy: str = Field(..., min_length=20, max_length=200)
    brand_guidelines: BrandGuidelines
    target_platforms: List[str] = Field(default=["instagram", "facebook"])
    call_to_action: str = Field(default="Learn More")

class GenerateSocialAdResponse(BaseModel):
    success: bool
    assets: List[GeneratedAsset]
    platform_optimization: Dict[str, Dict[str, Any]]
    processing_time_ms: float

class GenerateBannerRequest(BaseModel):
    channel_name: str = Field(..., min_length=3, max_length=50)
    tagline: Optional[str] = None
    brand_guidelines: BrandGuidelines
    banner_type: str = Field(default="channel_header")

class GenerateBannerResponse(BaseModel):
    success: bool
    asset: GeneratedAsset
    banner_specs: Dict[str, Any]
    processing_time_ms: float

class BatchAssetGenerationRequest(BaseModel):
    video_titles: List[str] = Field(..., min_items=1, max_items=10)
    brand_guidelines: BrandGuidelines
    asset_types: List[AssetType] = Field(default=[AssetType.THUMBNAIL])
    optimization_level: str = Field(default="omnipotent")

class BatchAssetGenerationResponse(BaseModel):
    success: bool
    generated_assets: List[GeneratedAsset]
    total_processing_time_ms: float
    average_performance_score: float

router = APIRouter()

# Asset storage (in production, would use proper storage)
asset_storage = {
    "generated_assets": [],
    "brand_identities": {},
    "performance_tracking": {}
}

@router.post("/brand/identity", response_model=GenerateBrandIdentityResponse)
async def generate_brand_identity(request: GenerateBrandIdentityRequest):
    """Generate complete brand identity for channel"""
    
    try:
        start_time = datetime.now()
        
        # Generate brand guidelines
        brand_guidelines = await visual_asset_engine.generate_brand_identity(
            channel_name=request.channel_name,
            niche=request.niche,
            target_audience=request.target_audience
        )
        
        # Store brand identity
        brand_id = f"brand_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        asset_storage["brand_identities"][brand_id] = brand_guidelines
        
        processing_time = (datetime.now() - start_time).total_seconds() * 1000
        
        return GenerateBrandIdentityResponse(
            success=True,
            brand_guidelines=brand_guidelines,
            processing_time_ms=processing_time
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Brand identity generation failed: {str(e)}")

@router.post("/assets/thumbnail", response_model=GenerateThumbnailResponse)
async def generate_thumbnail(request: GenerateThumbnailRequest):
    """Generate YouTube thumbnail optimized for algorithm"""
    
    try:
        start_time = datetime.now()
        
        # Create asset specification
        spec = AssetSpecification(
            asset_type=AssetType.THUMBNAIL,
            width=1280,  # YouTube standard
            height=720,  # 16:9 ratio
            text_content=request.video_title,
            brand_guidelines=request.brand_guidelines,
            optimization_target=request.optimization_target
        )
        
        # Generate thumbnail
        asset = await visual_asset_engine.generate_thumbnail(spec)
        
        # Store asset
        asset_storage["generated_assets"].append(asset)
        
        # Get performance metrics
        performance_metrics = asset.metadata.get("performance_metrics", {})
        
        processing_time = (datetime.now() - start_time).total_seconds() * 1000
        
        return GenerateThumbnailResponse(
            success=True,
            asset=asset,
            performance_metrics=performance_metrics,
            processing_time_ms=processing_time
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Thumbnail generation failed: {str(e)}")

@router.post("/assets/social-ad", response_model=GenerateSocialAdResponse)
async def generate_social_ad(request: GenerateSocialAdRequest):
    """Generate social media ad for multiple platforms"""
    
    try:
        start_time = datetime.now()
        generated_assets = []
        platform_optimization = {}
        
        # Generate assets for each platform
        for platform in request.target_platforms:
            # Platform-specific dimensions
            if platform in ["instagram", "facebook"]:
                width, height = 1080, 1920  # 9:16 Story format
            elif platform == "tiktok":
                width, height = 1080, 1920  # 9:16 Reels format
            elif platform == "twitter":
                width, height = 1200, 675    # 16:9
            else:
                width, height = 1080, 1080  # 1:1 square
            
            # Create asset specification
            spec = AssetSpecification(
                asset_type=AssetType.SOCIAL_AD,
                width=width,
                height=height,
                text_content=request.ad_copy,
                brand_guidelines=request.brand_guidelines,
                optimization_target=f"{platform}_algorithm"
            )
            
            # Generate asset
            asset = await visual_asset_engine.generate_social_ad(spec)
            asset.metadata["target_platform"] = platform
            generated_assets.append(asset)
            
            # Platform-specific optimization notes
            platform_optimization[platform] = {
                "dimensions": f"{width}x{height}",
                "aspect_ratio": f"{width}:{height}",
                "optimal_text_length": len(request.ad_copy),
                "cta_placement": "bottom" if platform in ["instagram", "facebook"] else "overlay",
                "color_optimization": "high_contrast" if platform == "tiktok" else "brand_consistent"
            }
        
        # Store assets
        asset_storage["generated_assets"].extend(generated_assets)
        
        processing_time = (datetime.now() - start_time).total_seconds() * 1000
        
        return GenerateSocialAdResponse(
            success=True,
            assets=generated_assets,
            platform_optimization=platform_optimization,
            processing_time_ms=processing_time
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Social ad generation failed: {str(e)}")

@router.post("/assets/banner", response_model=GenerateBannerResponse)
async def generate_banner(request: GenerateBannerRequest):
    """Generate channel banner or header"""
    
    try:
        start_time = datetime.now()
        
        # Banner dimensions based on type
        if request.banner_type == "channel_header":
            width, height = 2560, 1440  # YouTube banner standard
        elif request.banner_type == "profile_banner":
            width, height = 1546, 423   # Facebook cover
        else:
            width, height = 2560, 1440  # Default
        
        # Create asset specification
        spec = AssetSpecification(
            asset_type=AssetType.BANNER,
            width=width,
            height=height,
            text_content=f"{request.channel_name}\n{request.tagline or ''}",
            brand_guidelines=request.brand_guidelines,
            optimization_target="brand_visibility"
        )
        
        # Generate banner (using thumbnail generation as base)
        asset = await visual_asset_engine.generate_thumbnail(spec)
        asset.asset_type = AssetType.BANNER
        asset.file_path = f"/banners/banner_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        
        # Banner specifications
        banner_specs = {
            "type": request.banner_type,
            "dimensions": f"{width}x{height}",
            "safe_area": {"width": width - 200, "height": height - 200, "x": 100, "y": 100},
            "file_size_estimate": "2-3 MB",
            "format": "PNG",
            "platform_compatibility": ["youtube", "facebook", "twitter"]
        }
        
        # Store asset
        asset_storage["generated_assets"].append(asset)
        
        processing_time = (datetime.now() - start_time).total_seconds() * 1000
        
        return GenerateBannerResponse(
            success=True,
            asset=asset,
            banner_specs=banner_specs,
            processing_time_ms=processing_time
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Banner generation failed: {str(e)}")

@router.post("/assets/batch", response_model=BatchAssetGenerationResponse)
async def generate_batch_assets(request: BatchAssetGenerationRequest):
    """Generate multiple assets in batch"""
    
    try:
        start_time = datetime.now()
        generated_assets = []
        
        # Generate assets for each video title
        for video_title in request.video_titles:
            for asset_type in request.asset_types:
                # Determine dimensions based on asset type
                if asset_type == AssetType.THUMBNAIL:
                    width, height = 1280, 720
                elif asset_type == AssetType.SOCIAL_AD:
                    width, height = 1080, 1920
                elif asset_type == AssetType.BANNER:
                    width, height = 2560, 1440
                else:
                    width, height = 1080, 1080
                
                # Create asset specification
                spec = AssetSpecification(
                    asset_type=asset_type,
                    width=width,
                    height=height,
                    text_content=video_title,
                    brand_guidelines=request.brand_guidelines,
                    optimization_target=request.optimization_level
                )
                
                # Generate asset
                if asset_type == AssetType.THUMBNAIL:
                    asset = await visual_asset_engine.generate_thumbnail(spec)
                elif asset_type == AssetType.SOCIAL_AD:
                    asset = await visual_asset_engine.generate_social_ad(spec)
                else:
                    asset = await visual_asset_engine.generate_thumbnail(spec)  # Use thumbnail for other types
                    asset.asset_type = asset_type
                
                generated_assets.append(asset)
        
        # Store assets
        asset_storage["generated_assets"].extend(generated_assets)
        
        # Calculate average performance score
        total_score = sum(asset.performance_score for asset in generated_assets)
        average_score = total_score / len(generated_assets) if generated_assets else 0.0
        
        processing_time = (datetime.now() - start_time).total_seconds() * 1000
        
        return BatchAssetGenerationResponse(
            success=True,
            generated_assets=generated_assets,
            total_processing_time_ms=processing_time,
            average_performance_score=average_score
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Batch asset generation failed: {str(e)}")

@router.get("/assets/{asset_id}")
async def get_asset(asset_id: str):
    """Get specific asset by ID"""
    
    # Search for asset
    asset = None
    for stored_asset in asset_storage["generated_assets"]:
        if stored_asset.asset_id == asset_id:
            asset = stored_asset
            break
    
    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found")
    
    return {
        "success": True,
        "asset": asset
    }

@router.get("/assets")
async def list_assets(asset_type: Optional[AssetType] = None, limit: int = 50):
    """List generated assets with optional filtering"""
    
    assets = asset_storage["generated_assets"]
    
    # Filter by asset type if specified
    if asset_type:
        assets = [asset for asset in assets if asset.asset_type == asset_type]
    
    # Sort by creation time (newest first)
    assets.sort(key=lambda x: x.created_at, reverse=True)
    
    # Apply limit
    assets = assets[:limit]
    
    return {
        "success": True,
        "total_assets": len(assets),
        "assets": assets,
        "filter": {"asset_type": asset_type.value if asset_type else None, "limit": limit}
    }

@router.get("/brand/list")
async def list_brand_identities():
    """List all generated brand identities"""
    
    brands = []
    for brand_id, guidelines in asset_storage["brand_identities"].items():
        brands.append({
            "brand_id": brand_id,
            "style": guidelines.style.value,
            "target_audience": guidelines.target_audience,
            "brand_tone": guidelines.brand_tone,
            "color_palette": guidelines.color_palette.dict()
        })
    
    return {
        "success": True,
        "total_brands": len(brands),
        "brands": brands
    }

@router.get("/brand/{brand_id}")
async def get_brand_identity(brand_id: str):
    """Get specific brand identity"""
    
    if brand_id not in asset_storage["brand_identities"]:
        raise HTTPException(status_code=404, detail="Brand identity not found")
    
    return {
        "success": True,
        "brand_id": brand_id,
        "brand_guidelines": asset_storage["brand_identities"][brand_id]
    }

@router.get("/performance/analytics")
async def get_performance_analytics():
    """Get performance analytics for generated assets"""
    
    assets = asset_storage["generated_assets"]
    
    if not assets:
        return {
            "success": True,
            "analytics": {
                "total_assets": 0,
                "average_performance_score": 0.0,
                "performance_by_type": {},
                "top_performing_assets": [],
                "performance_trends": []
            }
        }
    
    # Calculate overall metrics
    total_score = sum(asset.performance_score for asset in assets)
    average_score = total_score / len(assets)
    
    # Performance by asset type
    performance_by_type = {}
    for asset_type in AssetType:
        type_assets = [asset for asset in assets if asset.asset_type == asset_type]
        if type_assets:
            type_score = sum(asset.performance_score for asset in type_assets) / len(type_assets)
            performance_by_type[asset_type.value] = {
                "count": len(type_assets),
                "average_score": type_score,
                "best_score": max(asset.performance_score for asset in type_assets)
            }
    
    # Top performing assets
    top_assets = sorted(assets, key=lambda x: x.performance_score, reverse=True)[:10]
    
    # Performance trends (last 30 days)
    thirty_days_ago = datetime.now() - timedelta(days=30)
    recent_assets = [asset for asset in assets if asset.created_at >= thirty_days_ago]
    
    return {
        "success": True,
        "analytics": {
            "total_assets": len(assets),
            "average_performance_score": average_score,
            "performance_by_type": performance_by_type,
            "top_performing_assets": [
                {
                    "asset_id": asset.asset_id,
                    "asset_type": asset.asset_type.value,
                    "performance_score": asset.performance_score,
                    "created_at": asset.created_at.isoformat()
                }
                for asset in top_assets
            ],
            "recent_performance": {
                "last_30_days": len(recent_assets),
                "recent_average_score": sum(asset.performance_score for asset in recent_assets) / len(recent_assets) if recent_assets else 0.0
            }
        }
    }

@router.delete("/assets/{asset_id}")
async def delete_asset(asset_id: str):
    """Delete specific asset"""
    
    global asset_storage
    
    # Find and remove asset
    for i, asset in enumerate(asset_storage["generated_assets"]):
        if asset.asset_id == asset_id:
            del asset_storage["generated_assets"][i]
            return {
                "success": True,
                "message": f"Asset {asset_id} deleted successfully"
            }
    
    raise HTTPException(status_code=404, detail="Asset not found")

@router.post("/assets/optimize/{asset_id}")
async def optimize_asset(asset_id: str, optimization_target: str = "youtube_algorithm"):
    """Re-optimize existing asset for different target"""
    
    # Find asset
    asset = None
    for stored_asset in asset_storage["generated_assets"]:
        if stored_asset.asset_id == asset_id:
            asset = stored_asset
            break
    
    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found")
    
    try:
        # Re-create asset specification with new optimization target
        spec = AssetSpecification(
            asset_type=asset.asset_type,
            width=int(asset.metadata.get("width", 1280)),
            height=int(asset.metadata.get("height", 720)),
            text_content=asset.metadata.get("text_content", ""),
            brand_guidelines=asset.metadata.get("brand_guidelines"),
            optimization_target=optimization_target
        )
        
        # Re-generate asset
        if asset.asset_type == AssetType.THUMBNAIL:
            optimized_asset = await visual_asset_engine.generate_thumbnail(spec)
        elif asset.asset_type == AssetType.SOCIAL_AD:
            optimized_asset = await visual_asset_engine.generate_social_ad(spec)
        else:
            optimized_asset = await visual_asset_engine.generate_thumbnail(spec)
        
        # Update asset in storage
        for i, stored_asset in enumerate(asset_storage["generated_assets"]):
            if stored_asset.asset_id == asset_id:
                asset_storage["generated_assets"][i] = optimized_asset
                break
        
        return {
            "success": True,
            "optimized_asset": optimized_asset,
            "performance_improvement": optimized_asset.performance_score - asset.performance_score
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Asset optimization failed: {str(e)}")
