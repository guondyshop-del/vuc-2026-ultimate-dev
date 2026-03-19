"""
VUC-2026 İstanbul ve İlçeleri Veritabanı
Konum bazlı içerik optimizasyonu için İstanbul il ve ilçe bilgileri
"""

from typing import Dict, List, Any
from dataclasses import dataclass
from enum import Enum

class RegionType(Enum):
    EUROPEAN = "avrupa_yakasi"
    ASIAN = "asya_yakasi"
    CENTRAL = "merkez"
    SUBURBAN = "banliyö"
    INDUSTRIAL = "sanayi"
    TOURISTIC = "turistik"

class DemographicProfile(Enum):
    UPPER_CLASS = "üst_sınıf"
    MIDDLE_UPPER = "orta_üst"
    MIDDLE_CLASS = "orta_sınıf"
    WORKING_CLASS = "işçi_sınıfı"
    MIXED = "karişik"
    STUDENT = "öğrenci"
    FAMILY = "aile_odaklı"

@dataclass
class District:
    name: str
    code: str
    region: RegionType
    demographic: DemographicProfile
    population: int
    avg_income: str
    key_features: List[str]
    content_angles: List[str]
    competitor_density: float
    opportunity_score: float
    popular_keywords: List[str]

class IstanbulLocations:
    """İstanbul ve ilçeleri için konum bazlı içerik stratejileri"""
    
    def __init__(self):
        self.districts = self._initialize_districts()
        self.regional_strategies = self._initialize_regional_strategies()
        
    def _initialize_districts(self) -> Dict[str, District]:
        """İstanbul ilçelerini ve özelliklerini tanımla"""
        return {
            # Avrupa Yakası - Merkez ve Lüks
            "beyoglu": District(
                name="Beyoğlu",
                code="34", 
                region=RegionType.CENTRAL,
                demographic=DemographicProfile.MIXED,
                population=250000,
                avg_income="orta_üst",
                key_features=["İstiklal Caddesi", "Taksim", "Galata", "Cihangir", "Karaköy"],
                content_angles=["gece_hayatı", "sanat_galerileri", "tarihi_mekanlar", "kültürel_etkinlikler", "kafeler"],
                competitor_density=0.95,
                opportunity_score=0.65,
                popular_keywords=["taksim", "istiklal", "galata", "beyoğlu_gezilecek_yerler", "istanbul_gece_hayatı"]
            ),
            
            "sisli": District(
                name="Şişli",
                code="34",
                region=RegionType.CENTRAL,
                demographic=DemographicProfile.MIDDLE_UPPER,
                population=320000,
                avg_income="orta_üst",
                key_features=["Nişantaşı", "Mecidiyeköy", "Şişli Merkez", "City's", "Cevahir"],
                content_angles=["alışveriş_merkezleri", "lüks_mağazalar", "restoranlar", "iş_merkezleri", "modern_yaşam"],
                competitor_density=0.90,
                opportunity_score=0.70,
                popular_keywords=["nişantaşı", "mecidiyeköy", "şişli_alışveriş", "istanbul_lüks_yaşam", "city's"]
            ),
            
            "besiktas": District(
                name="Beşiktaş",
                code="34",
                region=RegionType.CENTRAL,
                demographic=DemographicProfile.UPPER_CLASS,
                population=180000,
                avg_income="üst_sınıf",
                key_features=["Beşiktaş Meydan", "Levent", "Etiler", "Akaretler", "Ortaköy"],
                content_angles=["spor_kültürü", "lüks_restoranlar", "marina", "modern_mimarlık", "boğaz_manzarası"],
                competitor_density=0.88,
                opportunity_score=0.72,
                popular_keywords=["beşiktaş", "levent", "etiler", "vodafone_park", "akaretler"]
            ),
            
            "kadikoy": District(
                name="Kadıköy",
                code="34",
                region=RegionType.ASIAN,
                demographic=DemographicProfile.MIDDLE_CLASS,
                population=480000,
                avg_income="orta_sınıf",
                key_features=["Kadıköy Meydan", "Bağdat Caddesi", "Moda", "Fenerbahçe", "Kalamış"],
                content_angles=["sahil_yürüyüşü", "kafeler", "balık_restoranları", "antika_pazarları", "spor_kültürü"],
                competitor_density=0.85,
                opportunity_score=0.75,
                popular_keywords=["kadıköy", "bağdat_caddesi", "moda", "fenerbahçe", "kalamış_park"]
            ),
            
            "uskudar": District(
                name="Üsküdar",
                code="34",
                region=RegionType.ASIAN,
                demographic=DemographicProfile.FAMILY,
                population=520000,
                avg_income="orta_sınıf",
                key_features=["Üsküdar Meydan", "Maiden's Tower", "Salacak", "Kuzguncuk", "Beylerbeyi"],
                content_angles=["tarihi_camiler", "boğaz_manzaraları", "osmanlı_mimarisi", "çay_bahçeleri", "aile_gezileri"],
                competitor_density=0.70,
                opportunity_score=0.80,
                popular_keywords=["üsküdar", "kız_kulesi", "salacak", "kuzguncuk", "boğaz_manzarası"]
            ),
            
            # Aile ve Çocuk Odaklı Bölgeler
            "ataşehir": District(
                name="Ataşehir",
                code="34",
                region=RegionType.ASIAN,
                demographic=DemographicProfile.FAMILY,
                population=400000,
                avg_income="orta_üst",
                key_features=["Ataşehir Merkez", "Palladium", "Brandium", "Yeni Sahra", "İstanbul"],
                content_angles=["aile_alışverişi", "parklar", "oyun_alanları", "modern_yaşam", "eğitim_kurumları"],
                competitor_density=0.75,
                opportunity_score=0.85,
                popular_keywords=["ataşehir", "palladium", "aile_gezisi", "çocuk_parkları", "istanbul_aile"]
            ),
            
            "beykoz": District(
                name="Beykoz",
                code="34",
                region=RegionType.ASIAN,
                demographic=DemographicProfile.FAMILY,
                population=250000,
                avg_income="orta_sınıf",
                key_features=["Beykoz Meydan", "Anadolu Hisarı", "Kavacık", "Riva", "Polonezköy"],
                content_angles=["doğa_yürüyüşleri", "orman_parkları", "köy_kahvaltıları", "su_sporları", "aile_piknikleri"],
                competitor_density=0.45,
                opportunity_score=0.90,
                popular_keywords=["beykoz", "polonezköy", "riva", "anadolu_hisarı", "orman_yürüyüşü"]
            ),
            
            "sariyer": District(
                name="Sarıyer",
                code="34",
                region=RegionType.EUROPEAN,
                demographic=DemographicProfile.UPPER_CLASS,
                population=350000,
                avg_income="üst_sınıf",
                key_features=["Sarıyer Merkez", "İstinye", "Tarabya", "Zekeriyaköy", "Kilyos"],
                content_angles=["boğaz_yazlıkları", "plajlar", "marinalar", "lüks_restoranlar", "doğa_sporları"],
                competitor_density=0.60,
                opportunity_score=0.82,
                popular_keywords=["sarıyer", "kilyos", "istinye", "tarabya", "boğaz_yazlıkları"]
            ),
            
            "bakırköy": District(
                name="Bakırköy",
                code="34",
                region=RegionType.EUROPEAN,
                demographic=DemographicProfile.MIDDLE_CLASS,
                population=220000,
                avg_income="orta_sınıf",
                key_features=["Bakırköy Meydan", "Ataköy", "Florya", "Yeşilköy", "İstanbul"],
                content_angles=["aile_alışverişi", "plajlar", "parklar", "marina", "modern_konut"],
                competitor_density=0.80,
                opportunity_score=0.78,
                popular_keywords=["bakırköy", "ataköy", "florya", "yesilköy", "aile_alışverişi"]
            ),
            
            "maltepe": District(
                name="Maltepe",
                code="34",
                region=RegionType.ASIAN,
                demographic=DemographicProfile.FAMILY,
                population=500000,
                avg_income="orta_sınıf",
                key_features=["Maltepe Merkez", "Küçükyalı", "Güzelyalı", "İdealtepe", "Sahil"],
                content_angles=["sahil_yürüyüşü", "aile_parkları", "kafeler", "spor_sahaları", "modern_yaşam"],
                competitor_density=0.70,
                opportunity_score=0.83,
                popular_keywords=["maltepe", "küçükyalı", "sahil_yürüyüşü", "aile_gezisi", "istanbul_asia"]
            ),
            
            # Sanayi ve İşçi Bölgeleri
            "esenyurt": District(
                name="Esenyurt",
                code="34",
                region=RegionType.SUBURBAN,
                demographic=DemographicProfile.WORKING_CLASS,
                population=900000,
                avg_income="işçi_sınıfı",
                key_features=["Esenyurt Merkez", "Esenkent", "İncirtepe", "Pırtınak", "Akçaburgaz"],
                content_angles=["uygun_fiyatlı_alışveriş", "aile_parkları", "yerel_pazarlar", "konut_projeleri", "ulaşım"],
                competitor_density=0.65,
                opportunity_score=0.88,
                popular_keywords=["esenyurt", "uygun_alışveriş", "aile_parkları", "konut_projeleri", "istanbul_avrupa"]
            ),
            
            "sultangazi": District(
                name="Sultangazi",
                code="34",
                region=RegionType.SUBURBAN,
                demographic=DemographicProfile.WORKING_CLASS,
                population=550000,
                avg_income="işçi_sınıfı",
                key_features=["Sultangazi Merkez", "Gaziosmanpaşa", "50. Yıl", "Habibler", "Yıldız"],
                content_angles=["yerel_kültür", "aile_gezileri", "uygun_restoranlar", "parklar", "topluluk_olayları"],
                competitor_density=0.55,
                opportunity_score=0.86,
                popular_keywords=["sultangazi", "gaziosmanpaşa", "aile_gezisi", "uygun_restoran", "istanbul_avrupa"]
            ),
            
            "pendik": District(
                name="Pendik",
                code="34",
                region=RegionType.ASIAN,
                demographic=DemographicProfile.MIXED,
                population=700000,
                avg_income="orta_sınıf",
                key_features=["Pendik Merkez", "Kurtköy", "Sabiha Gökçen", "Yenişehir", "Kaynarca"],
                content_angles=["havalimanı", "modern_konut", "aile_parkları", "teknoloji_bölgesi", "deniz"],
                competitor_density=0.60,
                opportunity_score=0.84,
                popular_keywords=["pendik", "sabiha_gökçen", "kurtköy", "modern_yaşam", "istanbul_asia"]
            ),
            
            # Turistik Bölgeler
            "fatih": District(
                name="Fatih",
                code="34",
                region=RegionType.TOURISTIC,
                demographic=DemographicProfile.MIXED,
                population=600000,
                avg_income="orta_sınıf",
                key_features=["Sultanahmet", "Eminönü", "Çemberlitaş", "Süleymaniye", "Grand Bazaar"],
                content_angles=["tarihi_mekanlar", "müze_turları", "osmanlı_mimarisi", "turistik_yerler", "kültürel_miras"],
                competitor_density=0.98,
                opportunity_score=0.55,
                popular_keywords=["sultanahmet", "eminönü", "ayasofya", "topkapı", "grand_bazaar"]
            ),
            
            "eyup": District(
                name="Eyüp",
                code="34",
                region=RegionType.TOURISTIC,
                demographic=DemographicProfile.MIXED,
                population=400000,
                avg_income="orta_sınıf",
                key_features=["Eyüp Sultan", "Pierre Loti", "Eyüp Meydan", "Golden Horn", "Miniatürk"],
                content_angles=["dini_turizm", "tarihi_mekanlar", "boğaz_manzarası", "kültürel_turlar", "kafeler"],
                competitor_density=0.75,
                opportunity_score=0.73,
                popular_keywords=["eyüp_sultan", "pierre_loti", "altın_boynuz", "dini_turizm", "istanbul_tarihi"]
            ),
            
            # Öğrenci Bölgeleri
            "beyazit": District(
                name="Beyazıt",
                code="34",
                region=RegionType.CENTRAL,
                demographic=DemographicProfile.STUDENT,
                population=150000,
                avg_income="öğrenci",
                key_features=["İstanbul Üniversitesi", "Grand Bazaar", "Beyazıt Meydan", "Sahaflar", "Kapalıçarşı"],
                content_angles=["üniversite_yaşamı", "uygun_fiyatlı_yemek", "kitapçılar", "öğrenci_aktiviteleri", "tarihi_mekanlar"],
                competitor_density=0.85,
                opportunity_score=0.68,
                popular_keywords=["beyazıt", "istanbul_üniversitesi", "sahaflar", "öğrenci_yaşamı", "uygun_yemek"]
            ),
            
            "arnavutköy": District(
                name="Arnavutköy",
                code="34",
                region=RegionType.SUBURBAN,
                demographic=DemographicProfile.WORKING_CLASS,
                population=250000,
                avg_income="işçi_sınıfı",
                key_features=["Arnavutköy Merkez", "Hadımköy", "Boğazköy", "Bolluca", "Taşoluk"],
                content_angles=["kırsal_yaşam", "doğa_yürüyüşleri", "köy_kahvaltıları", "uygun_fiyatlı_hayat", "aile_gezileri"],
                competitor_density=0.35,
                opportunity_score=0.92,
                popular_keywords=["arnavutköy", "kırsal_yaşam", "köy_kahvaltısı", "doğa_yürüyüşü", "uygun_hayat"]
            ),
            
            "silivri": District(
                name="Silivri",
                code="34",
                region=RegionType.SUBURBAN,
                demographic=DemographicProfile.FAMILY,
                population="180000",
                avg_income="orta_sınıf",
                key_features=["Silivri Merkez", "Kıyı", "Alipaşa", "Çanta", "Selimpaşa"],
                content_angles=["plajlar", "yazlık_yaşam", "deniz_kültürü", "aile_tatili", "balık_restoranları"],
                competitor_density=0.40,
                opportunity_score=0.89,
                popular_keywords=["silivri", "plaj", "yazlık", "deniz_tatili", "aile_gezisi"]
            )
        }
    
    def _initialize_regional_strategies(self) -> Dict[str, Any]:
        """Bölgesel içerik stratejileri"""
        return {
            "avrupa_yakasi": {
                "focus": ["modern_yaşam", "iş_kültürü", "lüks_alışveriş", "gece_hayatı"],
                "tone": "profesyonel_ve_hızlı",
                "content_types": ["vlog", "review", "rehber", "lifestyle"],
                "best_times": ["18:00", "20:00", "weekend"],
                "monetization": "yüksek"
            },
            "asya_yakasi": {
                "focus": ["aile_yaşamı", "doğa", "geleneksel_kültür", "sakin_yaşam"],
                "tone": "samimi_ve_aile_odaklı",
                "content_types": ["aile_vlog", "doğa_yürüyüşü", "kahvaltı_turları", "park_rehberi"],
                "best_times": ["09:00", "15:00", "weekend"],
                "monetization": "orta"
            },
            "merkez": {
                "focus": ["kültür", "sanat", "turizm", "tarih"],
                "tone": "bilgilendirici_ve_kültürel",
                "content_types": ["belgesel", "tarih_rehberi", "sanat_turu", "müze_gezisi"],
                "best_times": ["10:00", "14:00", "weekend"],
                "monetization": "yüksek"
            },
            "banliyö": {
                "focus": ["uygun_fiyatlı_yaşam", "aile_odaklı", "yerel_kültür", "komşuluk"],
                "tone": "gerçek_ve_yakın",
                "content_types": ["yerel_rehber", "pazar_turu", "aile_gezisi", "uygun_alışveriş"],
                "best_times": ["11:00", "16:00", "weekend"],
                "monetization": "orta"
            },
            "turistik": {
                "focus": ["tarih", "müze", "gastro", "alışveriş"],
                "tone": "bilgilendirici_ve_turistik",
                "content_types": ["tur_rehberi", "müze_turu", "yemek_rehberi", "alışveriş_kılavuzu"],
                "best_times": ["09:00", "13:00", "17:00"],
                "monetization": "çok_yüksek"
            }
        }
    
    def get_district_by_name(self, name: str) -> District:
        """İlçe adına göre district bilgisi döndür"""
        return self.districts.get(name.lower(), None)
    
    def get_districts_by_region(self, region: RegionType) -> List[District]:
        """Bölgeye göre ilçeleri filtrele"""
        return [district for district in self.districts.values() if district.region == region]
    
    def get_districts_by_demographic(self, demographic: DemographicProfile) -> List[District]:
        """Demografik profile göre ilçeleri filtrele"""
        return [district for district in self.districts.values() if district.demographic == demographic]
    
    def get_high_opportunity_districts(self, min_score: float = 0.80) -> List[District]:
        """Yüksek fırsat skoruna sahip ilçeleri döndür"""
        return [district for district in self.districts.values() if district.opportunity_score >= min_score]
    
    def get_family_friendly_districts(self) -> List[District]:
        """Aile dostu ilçeleri döndür"""
        family_demographics = [DemographicProfile.FAMILY, DemographicProfile.MIDDLE_CLASS]
        return [district for district in self.districts.values() 
                if district.demographic in family_demographics and 
                any("park" in feature.lower() or "aile" in feature.lower() for feature in district.key_features)]
    
    def generate_location_based_content_ideas(self, district: District, content_type: str = "family") -> List[str]:
        """Konum bazlı içerik fikirleri üret"""
        ideas = []
        
        if content_type == "family":
            ideas.extend([
                f"{district.name} Aile Gezi Rehberi: En İyi Parklar ve Oyun Alanları",
                f"{district.name} Uygun Fiyatlı Aile Restoranları",
                f"{district.name} Çocuklarla Gezilecek Yerler",
                f"{district.name} Hafta Sonu Aile Aktiviteleri"
            ])
        elif content_type == "kids":
            ideas.extend([
                f"{district.name} Çocuk Parkları ve Oyun Alanları",
                f"{district.name} Eğitici Çocuk Aktiviteleri",
                f"{district.name} Çocuk Dostu Kafeler",
                f"{district.name} Aile Piknik Alanları"
            ])
        elif content_type == "pregnancy":
            ideas.extend([
                f"{district.name} Hamilelik Dostu Mekanlar",
                f"{district.name} Anne ve Bebek Dükkanları",
                f"{district.name} Hamile Yoga ve Spor Merkezleri",
                f"{district.name} Doğum Hazırlık Kursları"
            ])
        
        return ideas
    
    def get_competitor_analysis_by_district(self, district: District) -> Dict[str, Any]:
        """İlçe bazlı rakip analizi"""
        return {
            "district": district.name,
            "competitor_density": district.competitor_density,
            "opportunity_score": district.opportunity_score,
            "market_saturation": "yüksek" if district.competitor_density > 0.8 else "orta" if district.competitor_density > 0.6 else "düşük",
            "content_gaps": self._identify_content_gaps(district),
            "recommended_angles": district.content_angles,
            "keyword_opportunities": district.popular_keywords
        }
    
    def _identify_content_gaps(self, district: District) -> List[str]:
        """İlçedeki içerik boşluklarını tespit et"""
        gaps = []
        
        if district.competitor_density > 0.8:
            gaps.append("niş_konulara_odaklan")
        
        if district.demographic == DemographicProfile.FAMILY and "park" not in [f.lower() for f in district.key_features]:
            gaps.append("aile_park_içeriği")
        
        if district.region == RegionType.SUBURBAN:
            gaps.append("yerel_kültür_vurgusu")
        
        if district.opportunity_score > 0.85:
            gaps.append("pazar_öncesi_üretim")
        
        return gaps
    
    def generate_seo_keywords(self, district: District, content_type: str = "general") -> List[str]:
        """SEO anahtar kelimeleri üret"""
        base_keywords = district.popular_keywords.copy()
        
        if content_type == "family":
            base_keywords.extend([
                f"{district.name.lower()} aile gezisi",
                f"{district.name.lower()} çocuk parkları",
                f"{district.name.lower()} aile dostu",
                f"{district.name.lower()} hafta sonu"
            ])
        elif content_type == "kids":
            base_keywords.extend([
                f"{district.name.lower()} çocuk aktiviteleri",
                f"{district.name.lower()} oyun alanları",
                f"{district.name.lower()} çocuk dostu mekanlar",
                f"{district.name.lower()} eğitici oyunlar"
            ])
        
        return list(set(base_keywords))
    
    def get_content_calendar_suggestions(self, district: District) -> Dict[str, List[str]]:
        """İlçe için içerik takvimi önerileri"""
        return {
            "weekdays": [
                f"{district.name} İş Sonrası Gezinti",
                f"{district.name} Akşam Yemeği Mekanları",
                f"{district.name} Kafe Kültürü"
            ],
            "weekends": [
                f"{district.name} Hafta Sonu Rehberi",
                f"{district.name} Aile Gezisi",
                f"{district.name} Sakin Köşeler"
            ],
            "seasonal": [
                f"{district.name} Bahar Festivalleri",
                f"{district.name} Yaz Aktiviteleri",
                f"{district.name} Sonbahar Lezzetleri",
                f"{district.name} Kış Mekanları"
            ]
        }
    
    def calculate_content_priority_score(self, district: District, content_type: str = "family") -> float:
        """İlçe ve içerik tipi için öncelik skoru hesapla"""
        base_score = district.opportunity_score
        
        # Demographic bonus
        if content_type == "family" and district.demographic in [DemographicProfile.FAMILY, DemographicProfile.MIDDLE_CLASS]:
            base_score += 0.1
        
        # Region bonus
        if district.region == RegionType.SUBURBAN and content_type == "family":
            base_score += 0.05
        
        # Competitor density penalty
        if district.competitor_density > 0.8:
            base_score -= 0.1
        
        return min(1.0, base_score)

# Global instance
istanbul_locations = IstanbulLocations()

# Utility functions
def get_best_districts_for_family_content(limit: int = 10) -> List[District]:
    """Aile içeriği için en iyi ilçeler"""
    family_districts = istanbul_locations.get_family_friendly_districts()
    return sorted(family_districts, key=lambda x: x.opportunity_score, reverse=True)[:limit]

def get_district_content_strategy(district_name: str, content_type: str = "family") -> Dict[str, Any]:
    """İlçe için tam içerik stratejisi"""
    district = istanbul_locations.get_district_by_name(district_name)
    if not district:
        return {"error": "District not found"}
    
    return {
        "district_info": {
            "name": district.name,
            "region": district.region.value,
            "demographic": district.demographic.value,
            "population": district.population,
            "avg_income": district.avg_income
        },
        "content_strategy": {
            "best_angles": district.content_angles,
            "content_ideas": istanbul_locations.generate_location_based_content_ideas(district, content_type),
            "seo_keywords": istanbul_locations.generate_seo_keywords(district, content_type),
            "competitor_analysis": istanbul_locations.get_competitor_analysis_by_district(district),
            "priority_score": istanbul_locations.calculate_content_priority_score(district, content_type),
            "calendar_suggestions": istanbul_locations.get_content_calendar_suggestions(district)
        }
    }

def get_istanbul_overview() -> Dict[str, Any]:
    """İstanbul genel içerik stratejisi özeti"""
    districts = list(istanbul_locations.districts.values())
    
    return {
        "total_districts": len(districts),
        "regional_distribution": {
            region.value: len([d for d in districts if d.region == region])
            for region in RegionType
        },
        "demographic_distribution": {
            demo.value: len([d for d in districts if d.demographic == demo])
            for demo in DemographicProfile
        },
        "top_opportunity_districts": [
            d.name for d in sorted(districts, key=lambda x: x.opportunity_score, reverse=True)[:10]
        ],
        "family_friendly_districts": [
            d.name for d in istanbul_locations.get_family_friendly_districts()
        ],
        "avg_opportunity_score": sum(d.opportunity_score for d in districts) / len(districts),
        "content_recommendations": {
            "high_priority": get_best_districts_for_family_content(5),
            "emerging_areas": istanbul_locations.get_districts_by_region(RegionType.SUBURBAN),
            "established_areas": istanbul_locations.get_districts_by_region(RegionType.CENTRAL)
        }
    }
