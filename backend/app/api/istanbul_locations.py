"""
VUC-2026 İstanbul Konum Bazlı İçerik API
İstanbul ilçeleri ve konum bazlı içerik stratejileri endpoint'leri
"""

from fastapi import APIRouter, HTTPException
from typing import Dict, List, Optional
from pydantic import BaseModel
from datetime import datetime

from app.data.istanbul_locations import (
    istanbul_locations,
    District,
    RegionType,
    DemographicProfile,
    get_best_districts_for_family_content,
    get_district_content_strategy,
    get_istanbul_overview
)

router = APIRouter(prefix="/api/istanbul-locations", tags=["istanbul-locations"])

class DistrictRequest(BaseModel):
    district_name: str
    content_type: Optional[str] = "family"

class ContentStrategyRequest(BaseModel):
    district_name: str
    content_type: Optional[str] = "family"
    include_competitor_analysis: bool = True
    include_seo_keywords: bool = True

class RegionalAnalysisRequest(BaseModel):
    region: str
    content_type: Optional[str] = "family"

@router.get("/overview", response_model=Dict)
async def get_istanbul_locations_overview():
    """İstanbul genel konum ve içerik stratejisi özeti"""
    try:
        overview = get_istanbul_overview()
        
        return {
            "success": True,
            "data": overview,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get Istanbul overview: {str(e)}"
        )

@router.get("/districts", response_model=Dict)
async def get_all_districts():
    """Tüm İstanbul ilçelerini listele"""
    try:
        districts = []
        
        for district_name, district in istanbul_locations.districts.items():
            districts.append({
                "name": district.name,
                "code": district.code,
                "region": district.region.value,
                "demographic": district.demographic.value,
                "population": district.population,
                "avg_income": district.avg_income,
                "opportunity_score": district.opportunity_score,
                "competitor_density": district.competitor_density,
                "key_features": district.key_features[:5],  # İlk 5 özellik
                "content_angles": district.content_angles[:3]   # İlk 3 içerik açısı
            })
        
        return {
            "success": True,
            "total_districts": len(districts),
            "data": districts,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get districts: {str(e)}"
        )

@router.get("/districts/{district_name}", response_model=Dict)
async def get_district_info(district_name: str):
    """Belirli bir ilçenin detaylı bilgisini döndür"""
    try:
        district = istanbul_locations.get_district_by_name(district_name)
        
        if not district:
            raise HTTPException(
                status_code=404,
                detail=f"District '{district_name}' not found"
            )
        
        return {
            "success": True,
            "data": {
                "name": district.name,
                "code": district.code,
                "region": district.region.value,
                "demographic": district.demographic.value,
                "population": district.population,
                "avg_income": district.avg_income,
                "opportunity_score": district.opportunity_score,
                "competitor_density": district.competitor_density,
                "key_features": district.key_features,
                "content_angles": district.content_angles,
                "popular_keywords": district.popular_keywords
            },
            "timestamp": datetime.now().isoformat()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get district info: {str(e)}"
        )

@router.post("/districts/{district_name}/content-strategy", response_model=Dict)
async def get_district_content_strategy_endpoint(
    district_name: str,
    request: ContentStrategyRequest
):
    """İlçe için tam içerik stratejisi oluştur"""
    try:
        strategy = get_district_content_strategy(district_name, request.content_type)
        
        if "error" in strategy:
            raise HTTPException(
                status_code=404,
                detail=strategy["error"]
            )
        
        return {
            "success": True,
            "district": district_name,
            "content_type": request.content_type,
            "data": strategy,
            "timestamp": datetime.now().isoformat()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate content strategy: {str(e)}"
        )

@router.get("/districts/region/{region_name}", response_model=Dict)
async def get_districts_by_region(region_name: str):
    """Bölgeye göre ilçeleri filtrele"""
    try:
        # Convert string to enum
        region_map = {
            "avrupa_yakasi": RegionType.EUROPEAN,
            "asya_yakasi": RegionType.ASIAN,
            "merkez": RegionType.CENTRAL,
            "banliyo": RegionType.SUBURBAN,
            "sanayi": RegionType.INDUSTRIAL,
            "turistik": RegionType.TOURISTIC
        }
        
        if region_name not in region_map:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid region. Available regions: {list(region_map.keys())}"
            )
        
        region = region_map[region_name]
        districts = istanbul_locations.get_districts_by_region(region)
        
        district_data = []
        for district in districts:
            district_data.append({
                "name": district.name,
                "demographic": district.demographic.value,
                "population": district.population,
                "opportunity_score": district.opportunity_score,
                "competitor_density": district.competitor_density,
                "key_features": district.key_features[:3]
            })
        
        # Sort by opportunity score
        district_data.sort(key=lambda x: x["opportunity_score"], reverse=True)
        
        return {
            "success": True,
            "region": region_name,
            "total_districts": len(district_data),
            "data": district_data,
            "timestamp": datetime.now().isoformat()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get districts by region: {str(e)}"
        )

@router.get("/districts/demographic/{demographic_name}", response_model=Dict)
async def get_districts_by_demographic(demographic_name: str):
    """Demografik profile göre ilçeleri filtrele"""
    try:
        # Convert string to enum
        demographic_map = {
            "ust_sinif": DemographicProfile.UPPER_CLASS,
            "orta_ust": DemographicProfile.MIDDLE_UPPER,
            "orta_sinif": DemographicProfile.MIDDLE_CLASS,
            "isci_sinifi": DemographicProfile.WORKING_CLASS,
            "karisik": DemographicProfile.MIXED,
            "ogrenci": DemographicProfile.STUDENT,
            "aile_odakli": DemographicProfile.FAMILY
        }
        
        if demographic_name not in demographic_map:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid demographic. Available demographics: {list(demographic_map.keys())}"
            )
        
        demographic = demographic_map[demographic_name]
        districts = istanbul_locations.get_districts_by_demographic(demographic)
        
        district_data = []
        for district in districts:
            district_data.append({
                "name": district.name,
                "region": district.region.value,
                "population": district.population,
                "opportunity_score": district.opportunity_score,
                "competitor_density": district.competitor_density,
                "content_angles": district.content_angles[:3]
            })
        
        # Sort by opportunity score
        district_data.sort(key=lambda x: x["opportunity_score"], reverse=True)
        
        return {
            "success": True,
            "demographic": demographic_name,
            "total_districts": len(district_data),
            "data": district_data,
            "timestamp": datetime.now().isoformat()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get districts by demographic: {str(e)}"
        )

@router.get("/high-opportunity-districts", response_model=Dict)
async def get_high_opportunity_districts(min_score: float = 0.80):
    """Yüksek fırsat skoruna sahip ilçeleri döndür"""
    try:
        districts = istanbul_locations.get_high_opportunity_districts(min_score)
        
        district_data = []
        for district in districts:
            district_data.append({
                "name": district.name,
                "region": district.region.value,
                "demographic": district.demographic.value,
                "population": district.population,
                "opportunity_score": district.opportunity_score,
                "competitor_density": district.competitor_density,
                "content_angles": district.content_angles[:3],
                "popular_keywords": district.popular_keywords[:5]
            })
        
        # Sort by opportunity score
        district_data.sort(key=lambda x: x["opportunity_score"], reverse=True)
        
        return {
            "success": True,
            "min_score": min_score,
            "total_districts": len(district_data),
            "data": district_data,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get high opportunity districts: {str(e)}"
        )

@router.get("/family-friendly-districts", response_model=Dict)
async def get_family_friendly_districts():
    """Aile dostu ilçeleri döndür"""
    try:
        districts = istanbul_locations.get_family_friendly_districts()
        
        district_data = []
        for district in districts:
            district_data.append({
                "name": district.name,
                "region": district.region.value,
                "population": district.population,
                "opportunity_score": district.opportunity_score,
                "competitor_density": district.competitor_density,
                "key_features": district.key_features,
                "content_angles": district.content_angles
            })
        
        # Sort by opportunity score
        district_data.sort(key=lambda x: x["opportunity_score"], reverse=True)
        
        return {
            "success": True,
            "total_districts": len(district_data),
            "data": district_data,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get family friendly districts: {str(e)}"
        )

@router.post("/districts/{district_name}/content-ideas", response_model=Dict)
async def get_district_content_ideas(
    district_name: str,
    request: DistrictRequest
):
    """İlçe için içerik fikirleri üret"""
    try:
        district = istanbul_locations.get_district_by_name(district_name)
        
        if not district:
            raise HTTPException(
                status_code=404,
                detail=f"District '{district_name}' not found"
            )
        
        content_ideas = istanbul_locations.generate_location_based_content_ideas(
            district, 
            request.content_type
        )
        
        return {
            "success": True,
            "district": district_name,
            "content_type": request.content_type,
            "data": {
                "ideas": content_ideas,
                "best_angles": district.content_angles,
                "popular_keywords": district.popular_keywords
            },
            "timestamp": datetime.now().isoformat()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate content ideas: {str(e)}"
        )

@router.post("/districts/{district_name}/seo-keywords", response_model=Dict)
async def get_district_seo_keywords(
    district_name: str,
    content_type: str = "general"
):
    """İlçe için SEO anahtar kelimeleri üret"""
    try:
        district = istanbul_locations.get_district_by_name(district_name)
        
        if not district:
            raise HTTPException(
                status_code=404,
                detail=f"District '{district_name}' not found"
            )
        
        keywords = istanbul_locations.generate_seo_keywords(district, content_type)
        
        return {
            "success": True,
            "district": district_name,
            "content_type": content_type,
            "data": {
                "keywords": keywords,
                "base_keywords": district.popular_keywords,
                "total_keywords": len(keywords)
            },
            "timestamp": datetime.now().isoformat()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate SEO keywords: {str(e)}"
        )

@router.post("/districts/{district_name}/competitor-analysis", response_model=Dict)
async def get_district_competitor_analysis(district_name: str):
    """İlçe için rakip analizi"""
    try:
        district = istanbul_locations.get_district_by_name(district_name)
        
        if not district:
            raise HTTPException(
                status_code=404,
                detail=f"District '{district_name}' not found"
            )
        
        analysis = istanbul_locations.get_competitor_analysis_by_district(district)
        
        return {
            "success": True,
            "district": district_name,
            "data": analysis,
            "timestamp": datetime.now().isoformat()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get competitor analysis: {str(e)}"
        )

@router.get("/regions", response_model=Dict)
async def get_available_regions():
    """Mevcut bölgeleri listele"""
    try:
        regions = []
        
        for region in RegionType:
            districts = istanbul_locations.get_districts_by_region(region)
            regions.append({
                "name": region.value,
                "display_name": region.value.replace("_", " ").title(),
                "district_count": len(districts),
                "avg_opportunity_score": sum(d.opportunity_score for d in districts) / len(districts),
                "description": istanbul_locations.regional_strategies.get(region.value, {}).get("focus", [])
            })
        
        return {
            "success": True,
            "total_regions": len(regions),
            "data": regions,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get regions: {str(e)}"
        )

@router.get("/demographics", response_model=Dict)
async def get_available_demographics():
    """Mevcut demografik profilleri listele"""
    try:
        demographics = []
        
        for demo in DemographicProfile:
            districts = istanbul_locations.get_districts_by_demographic(demo)
            demographics.append({
                "name": demo.value,
                "display_name": demo.value.replace("_", " ").title(),
                "district_count": len(districts),
                "avg_opportunity_score": sum(d.opportunity_score for d in districts) / len(districts),
                "total_population": sum(d.population for d in districts)
            })
        
        return {
            "success": True,
            "total_demographics": len(demographics),
            "data": demographics,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get demographics: {str(e)}"
        )

@router.post("/content-calendar", response_model=Dict)
async def get_district_content_calendar(district_name: str):
    """İlçe için içerik takvimi önerileri"""
    try:
        district = istanbul_locations.get_district_by_name(district_name)
        
        if not district:
            raise HTTPException(
                status_code=404,
                detail=f"District '{district_name}' not found"
            )
        
        calendar = istanbul_locations.get_content_calendar_suggestions(district)
        
        return {
            "success": True,
            "district": district_name,
            "data": calendar,
            "timestamp": datetime.now().isoformat()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get content calendar: {str(e)}"
        )

@router.get("/best-family-districts", response_model=Dict)
async def get_best_family_districts_endpoint(limit: int = 10):
    """Aile içeriği için en iyi ilçeler"""
    try:
        districts = get_best_districts_for_family_content(limit)
        
        district_data = []
        for district in districts:
            district_data.append({
                "name": district.name,
                "region": district.region.value,
                "demographic": district.demographic.value,
                "population": district.population,
                "opportunity_score": district.opportunity_score,
                "competitor_density": district.competitor_density,
                "content_angles": district.content_angles[:3],
                "key_features": district.key_features[:3]
            })
        
        return {
            "success": True,
            "limit": limit,
            "total_districts": len(district_data),
            "data": district_data,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get best family districts: {str(e)}"
        )

@router.get("/search", response_model=Dict)
async def search_districts(
    query: str,
    region: Optional[str] = None,
    demographic: Optional[str] = None,
    min_opportunity: Optional[float] = None
):
    """İlçeleri çoklu kriterlere göre ara"""
    try:
        all_districts = list(istanbul_locations.districts.values())
        filtered_districts = []
        
        for district in all_districts:
            # Text search
            if query.lower() not in district.name.lower() and \
               not any(query.lower() in feature.lower() for feature in district.key_features):
                continue
            
            # Region filter
            if region:
                region_map = {
                    "avrupa_yakasi": RegionType.EUROPEAN,
                    "asya_yakasi": RegionType.ASIAN,
                    "merkez": RegionType.CENTRAL,
                    "banliyo": RegionType.SUBURBAN,
                    "sanayi": RegionType.INDUSTRIAL,
                    "turistik": RegionType.TOURISTIC
                }
                if region in region_map and district.region != region_map[region]:
                    continue
            
            # Demographic filter
            if demographic:
                demographic_map = {
                    "ust_sinif": DemographicProfile.UPPER_CLASS,
                    "orta_ust": DemographicProfile.MIDDLE_UPPER,
                    "orta_sinif": DemographicProfile.MIDDLE_CLASS,
                    "isci_sinifi": DemographicProfile.WORKING_CLASS,
                    "karisik": DemographicProfile.MIXED,
                    "ogrenci": DemographicProfile.STUDENT,
                    "aile_odakli": DemographicProfile.FAMILY
                }
                if demographic in demographic_map and district.demographic != demographic_map[demographic]:
                    continue
            
            # Opportunity score filter
            if min_opportunity and district.opportunity_score < min_opportunity:
                continue
            
            filtered_districts.append(district)
        
        # Sort by opportunity score
        filtered_districts.sort(key=lambda x: x.opportunity_score, reverse=True)
        
        district_data = []
        for district in filtered_districts:
            district_data.append({
                "name": district.name,
                "region": district.region.value,
                "demographic": district.demographic.value,
                "population": district.population,
                "opportunity_score": district.opportunity_score,
                "competitor_density": district.competitor_density,
                "key_features": district.key_features[:3],
                "content_angles": district.content_angles[:2]
            })
        
        return {
            "success": True,
            "query": query,
            "filters": {
                "region": region,
                "demographic": demographic,
                "min_opportunity": min_opportunity
            },
            "total_results": len(district_data),
            "data": district_data,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to search districts: {str(e)}"
        )
