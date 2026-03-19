"""
VUC-2026 Visual Asset Engine
Automatic brand generation, thumbnails, banners, and social media assets
"""

from typing import List, Dict, Optional, Tuple, Any
from pydantic import BaseModel, Field
from datetime import datetime
import asyncio
import json
import random
from enum import Enum
from PIL import Image, ImageDraw, ImageFont
import io
import base64

class AssetType(str, Enum):
    LOGO = "logo"
    BANNER = "banner"
    THUMBNAIL = "thumbnail"
    SOCIAL_AD = "social_ad"
    WATERMARK = "watermark"

class BrandStyle(str, Enum):
    PASTEL_FAMILY = "pastel_family"
    MODERN_MINIMAL = "modern_minimal"
    PLAYFUL_COLORFUL = "playful_colorful"
    PROFESSIONAL_EDUCATIONAL = "professional_educational"
    LUXURY_PREMIUM = "luxury_premium"

class ColorPalette(BaseModel):
    primary: str
    secondary: str
    accent: str
    background: str
    text_primary: str
    text_secondary: str

class BrandGuidelines(BaseModel):
    style: BrandStyle
    color_palette: ColorPalette
    font_family: str
    logo_variants: List[str]
    brand_tone: str
    target_audience: str

class AssetSpecification(BaseModel):
    asset_type: AssetType
    width: int
    height: int
    text_content: Optional[str] = None
    image_url: Optional[str] = None
    brand_guidelines: BrandGuidelines
    optimization_target: str = "youtube_algorithm"

class GeneratedAsset(BaseModel):
    asset_id: str
    asset_type: AssetType
    file_path: str
    base64_data: str
    metadata: Dict[str, Any]
    performance_score: float
    created_at: datetime

class VisualAssetEngine:
    """VUC-2026 Visual Asset Generation Engine"""
    
    def __init__(self):
        self.brand_style_configs = self._initialize_brand_styles()
        self.color_palettes = self._initialize_color_palettes()
        self.thumbnail_templates = self._initialize_thumbnail_templates()
        self.social_ad_templates = self._initialize_social_ad_templates()
        self.performance_analyzer = self._initialize_performance_analyzer()
        
    def _initialize_brand_styles(self) -> Dict[BrandStyle, Dict[str, Any]]:
        """Initialize brand style configurations"""
        return {
            BrandStyle.PASTEL_FAMILY: {
                "description": "Soft, warm colors perfect for family and baby content",
                "vibrancy": 0.6,
                "contrast": 0.7,
                "font_style": "rounded",
                "visual_elements": ["soft_shapes", "gentle_gradients", "cute_icons"]
            },
            BrandStyle.MODERN_MINIMAL: {
                "description": "Clean, minimalist design for educational content",
                "vibrancy": 0.8,
                "contrast": 0.9,
                "font_style": "sans_serif",
                "visual_elements": ["clean_lines", "white_space", "typography"]
            },
            BrandStyle.PLAYFUL_COLORFUL: {
                "description": "Bright, energetic design for kids entertainment",
                "vibrancy": 1.0,
                "contrast": 0.8,
                "font_style": "playful",
                "visual_elements": ["bright_colors", "fun_shapes", "cartoon_elements"]
            },
            BrandStyle.PROFESSIONAL_EDUCATIONAL: {
                "description": "Professional design for expert parenting advice",
                "vibrancy": 0.7,
                "contrast": 0.85,
                "font_style": "professional",
                "visual_elements": ["structured_layout", "charts", "professional_icons"]
            },
            BrandStyle.LUXURY_PREMIUM: {
                "description": "High-end design for premium parenting content",
                "vibrancy": 0.8,
                "contrast": 0.95,
                "font_style": "elegant",
                "visual_elements": ["gold_accents", "premium_textures", "sophisticated_layout"]
            }
        }
    
    def _initialize_color_palettes(self) -> Dict[BrandStyle, ColorPalette]:
        """Initialize color palettes for each brand style"""
        return {
            BrandStyle.PASTEL_FAMILY: ColorPalette(
                primary="#FFE5E5",
                secondary="#E5F3FF", 
                accent="#FFF5E5",
                background="#FFFFFF",
                text_primary="#4A4A4A",
                text_secondary="#7A7A7A"
            ),
            BrandStyle.MODERN_MINIMAL: ColorPalette(
                primary="#2C3E50",
                secondary="#3498DB",
                accent="#E74C3C",
                background="#FFFFFF",
                text_primary="#2C3E50",
                text_secondary="#7F8C8D"
            ),
            BrandStyle.PLAYFUL_COLORFUL: ColorPalette(
                primary="#FF6B6B",
                secondary="#4ECDC4",
                accent="#45B7D1",
                background="#F8F9FA",
                text_primary="#2C3E50",
                text_secondary="#7F8C8D"
            ),
            BrandStyle.PROFESSIONAL_EDUCATIONAL: ColorPalette(
                primary="#34495E",
                secondary="#3498DB",
                accent="#E67E22",
                background="#FFFFFF",
                text_primary="#2C3E50",
                text_secondary="#7F8C8D"
            ),
            BrandStyle.LUXURY_PREMIUM: ColorPalette(
                primary="#D4AF37",
                secondary="#1C1C1C",
                accent="#8B4513",
                background="#FAFAFA",
                text_primary="#1C1C1C",
                text_secondary="#666666"
            )
        }
    
    def _initialize_thumbnail_templates(self) -> List[Dict[str, Any]]:
        """Initialize YouTube thumbnail templates"""
        return [
            {
                "name": "split_screen",
                "description": "Split screen with text on one side, image on other",
                "text_position": "left",
                "image_position": "right",
                "background_style": "gradient"
            },
            {
                "name": "text_overlay",
                "description": "Full background image with text overlay",
                "text_position": "center",
                "image_position": "full",
                "background_style": "image"
            },
            {
                "name": "card_layout",
                "description": "Card-based layout with multiple elements",
                "text_position": "bottom",
                "image_position": "top",
                "background_style": "cards"
            },
            {
                "name": "minimal_focus",
                "description": "Minimal design with focus on text",
                "text_position": "center",
                "image_position": "accent",
                "background_style": "solid"
            },
            {
                "name": "dynamic_grid",
                "description": "Grid layout with multiple visual elements",
                "text_position": "overlay",
                "image_position": "grid",
                "background_style": "pattern"
            }
        ]
    
    def _initialize_social_ad_templates(self) -> List[Dict[str, Any]]:
        """Initialize social media ad templates (9:16)"""
        return [
            {
                "name": "story_vertical",
                "description": "Instagram/Facebook Story format",
                "aspect_ratio": "9:16",
                "text_layout": "vertical_stack",
                "cta_position": "bottom"
            },
            {
                "name": "reels_tiktok",
                "description": "Reels/TikTok optimized format",
                "aspect_ratio": "9:16",
                "text_layout": "top_title",
                "cta_position": "overlay"
            },
            {
                "name": "carousel_post",
                "description": "Carousel format for Instagram",
                "aspect_ratio": "1:1",
                "text_layout": "center_focus",
                "cta_position": "bottom"
            }
        ]
    
    def _initialize_performance_analyzer(self) -> Dict[str, Any]:
        """Initialize performance analysis parameters"""
        return {
            "thumbnail_metrics": {
                "contrast_ratio": {"min": 4.5, "weight": 0.3},
                "text_readability": {"min": 0.8, "weight": 0.25},
                "color_harmony": {"min": 0.7, "weight": 0.2},
                "visual_hierarchy": {"min": 0.8, "weight": 0.15},
                "emotional_impact": {"min": 0.6, "weight": 0.1}
            },
            "engagement_predictors": [
                "high_contrast_text",
                "emotional_faces",
                "bright_colors",
                "clear_value_proposition",
                "curiosity_gap"
            ]
        }
    
    async def generate_brand_identity(self, channel_name: str, niche: str, target_audience: str) -> BrandGuidelines:
        """Generate complete brand identity for the channel"""
        
        # Select appropriate brand style based on niche
        niche_style_mapping = {
            "baby": BrandStyle.PASTEL_FAMILY,
            "pregnancy": BrandStyle.PASTEL_FAMILY,
            "toddler": BrandStyle.PLAYFUL_COLORFUL,
            "parenting_education": BrandStyle.PROFESSIONAL_EDUCATIONAL,
            "montessori": BrandStyle.MODERN_MINIMAL,
            "premium_parenting": BrandStyle.LUXURY_PREMIUM
        }
        
        selected_style = niche_style_mapping.get(niche.lower(), BrandStyle.PASTEL_FAMILY)
        color_palette = self.color_palettes[selected_style]
        
        # Generate brand guidelines
        guidelines = BrandGuidelines(
            style=selected_style,
            color_palette=color_palette,
            font_family=self._select_font_family(selected_style),
            logo_variants=self._generate_logo_variants(channel_name, selected_style),
            brand_tone=self._determine_brand_tone(niche, target_audience),
            target_audience=target_audience
        )
        
        return guidelines
    
    def _select_font_family(self, style: BrandStyle) -> str:
        """Select appropriate font family for brand style"""
        font_mapping = {
            BrandStyle.PASTEL_FAMILY: "Quicksand",
            BrandStyle.MODERN_MINIMAL: "Inter",
            BrandStyle.PLAYFUL_COLORFUL: "Fredoka One",
            BrandStyle.PROFESSIONAL_EDUCATIONAL: "Roboto",
            BrandStyle.LUXURY_PREMIUM: "Playfair Display"
        }
        return font_mapping.get(style, "Inter")
    
    def _generate_logo_variants(self, channel_name: str, style: BrandStyle) -> List[str]:
        """Generate logo variants for different use cases"""
        return [
            f"{channel_name}_icon",  # Small icon version
            f"{channel_name}_horizontal",  # Horizontal layout
            f"{channel_name}_vertical",  # Vertical layout
            f"{channel_name}_monogram",  # Monogram/circle version
            f"{channel_name}_watermark"  # Transparent watermark
        ]
    
    def _determine_brand_tone(self, niche: str, target_audience: str) -> str:
        """Determine brand tone based on niche and audience"""
        if "baby" in niche.lower() or "pregnancy" in niche.lower():
            return "warm_caring_reassuring"
        elif "toddler" in niche.lower():
            return "playful_energetic_fun"
        elif "education" in niche.lower() or "montessori" in niche.lower():
            return "expert_trustworthy_informative"
        else:
            return "friendly_helpful_supportive"
    
    async def generate_thumbnail(self, spec: AssetSpecification) -> GeneratedAsset:
        """Generate YouTube thumbnail optimized for algorithm"""
        
        try:
            # Select template
            template = random.choice(self.thumbnail_templates)
            
            # Create image
            image = Image.new('RGB', (spec.width, spec.height), spec.brand_guidelines.color_palette.background)
            draw = ImageDraw.Draw(image)
            
            # Apply template design
            if template["name"] == "split_screen":
                image = self._create_split_screen_thumbnail(image, draw, spec, template)
            elif template["name"] == "text_overlay":
                image = self._create_text_overlay_thumbnail(image, draw, spec, template)
            elif template["name"] == "card_layout":
                image = self._create_card_layout_thumbnail(image, draw, spec, template)
            elif template["name"] == "minimal_focus":
                image = self._create_minimal_focus_thumbnail(image, draw, spec, template)
            else:
                image = self._create_dynamic_grid_thumbnail(image, draw, spec, template)
            
            # Convert to base64
            buffer = io.BytesIO()
            image.save(buffer, format='PNG')
            image_base64 = base64.b64encode(buffer.getvalue()).decode()
            
            # Calculate performance score
            performance_score = self._calculate_thumbnail_performance(image, spec)
            
            # Generate asset
            asset = GeneratedAsset(
                asset_id=f"thumb_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                asset_type=AssetType.THUMBNAIL,
                file_path=f"/thumbnails/thumbnail_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png",
                base64_data=image_base64,
                metadata={
                    "template": template["name"],
                    "brand_style": spec.brand_guidelines.style.value,
                    "performance_metrics": self._analyze_thumbnail_metrics(image),
                    "optimization_target": spec.optimization_target
                },
                performance_score=performance_score,
                created_at=datetime.now()
            )
            
            return asset
            
        except Exception as e:
            raise Exception(f"Thumbnail generation failed: {str(e)}")
    
    def _create_split_screen_thumbnail(self, image: Image, draw: ImageDraw, spec: AssetSpecification, template: Dict[str, Any]) -> Image:
        """Create split screen thumbnail layout"""
        
        # Split the image
        mid_x = spec.width // 2
        
        # Left side - text background
        left_color = spec.brand_guidelines.color_palette.primary
        draw.rectangle([0, 0, mid_x, spec.height], fill=left_color)
        
        # Right side - accent color
        right_color = spec.brand_guidelines.color_palette.secondary
        draw.rectangle([mid_x, 0, spec.width, spec.height], fill=right_color)
        
        # Add text on left side
        if spec.text_content:
            self._add_text_to_image(draw, spec.text_content, spec.brand_guidelines, 0, 0, mid_x, spec.height)
        
        # Add decorative elements
        self._add_decorative_elements(draw, spec.brand_guidelines, mid_x, 0, spec.width, spec.height)
        
        return image
    
    def _create_text_overlay_thumbnail(self, image: Image, draw: ImageDraw, spec: AssetSpecification, template: Dict[str, Any]) -> Image:
        """Create text overlay thumbnail layout"""
        
        # Create gradient background
        self._create_gradient_background(image, draw, spec.brand_guidelines.color_palette)
        
        # Add semi-transparent overlay for text readability
        overlay = Image.new('RGBA', (spec.width, spec.height), (0, 0, 0, 128))
        image.paste(overlay, (0, 0), overlay)
        
        # Add text in center
        if spec.text_content:
            self._add_text_to_image(draw, spec.text_content, spec.brand_guidelines, 0, 0, spec.width, spec.height)
        
        return image
    
    def _create_card_layout_thumbnail(self, image: Image, draw: ImageDraw, spec: AssetSpecification, template: Dict[str, Any]) -> Image:
        """Create card layout thumbnail"""
        
        # Background
        bg_color = spec.brand_guidelines.color_palette.background
        draw.rectangle([0, 0, spec.width, spec.height], fill=bg_color)
        
        # Top card area (70% of height)
        card_height = int(spec.height * 0.7)
        card_color = spec.brand_guidelines.color_palette.primary
        draw.rectangle([10, 10, spec.width - 10, card_height], fill=card_color, outline=spec.brand_guidelines.color_palette.accent, width=3)
        
        # Add visual elements in card
        self._add_visual_elements_to_card(draw, spec.brand_guidelines, 15, 15, spec.width - 25, card_height - 5)
        
        # Bottom text area
        text_area_y = card_height + 20
        if spec.text_content:
            self._add_text_to_image(draw, spec.text_content, spec.brand_guidelines, 20, text_area_y, spec.width - 20, spec.height - 20)
        
        return image
    
    def _create_minimal_focus_thumbnail(self, image: Image, draw: ImageDraw, spec: AssetSpecification, template: Dict[str, Any]) -> Image:
        """Create minimal focus thumbnail"""
        
        # Clean background
        bg_color = spec.brand_guidelines.color_palette.background
        draw.rectangle([0, 0, spec.width, spec.height], fill=bg_color)
        
        # Add subtle accent element
        accent_size = min(spec.width, spec.height) // 8
        accent_x = spec.width - accent_size - 20
        accent_y = 20
        draw.rectangle([accent_x, accent_y, accent_x + accent_size, accent_y + accent_size], 
                      fill=spec.brand_guidelines.color_palette.accent)
        
        # Add centered text
        if spec.text_content:
            self._add_centered_text(draw, spec.text_content, spec.brand_guidelines, spec.width, spec.height)
        
        return image
    
    def _create_dynamic_grid_thumbnail(self, image: Image, draw: ImageDraw, spec: AssetSpecification, template: Dict[str, Any]) -> Image:
        """Create dynamic grid thumbnail"""
        
        # Background
        bg_color = spec.brand_guidelines.color_palette.background
        draw.rectangle([0, 0, spec.width, spec.height], fill=bg_color)
        
        # Create 2x2 grid
        grid_width = (spec.width - 30) // 2
        grid_height = (spec.height - 30) // 2
        
        colors = [
            spec.brand_guidelines.color_palette.primary,
            spec.brand_guidelines.color_palette.secondary,
            spec.brand_guidelines.color_palette.accent,
            spec.brand_guidelines.color_palette.primary
        ]
        
        for i in range(2):
            for j in range(2):
                x = 10 + j * (grid_width + 10)
                y = 10 + i * (grid_height + 10)
                color_idx = i * 2 + j
                
                draw.rectangle([x, y, x + grid_width, y + grid_height], 
                             fill=colors[color_idx], outline=spec.brand_guidelines.color_palette.text_primary, width=2)
                
                # Add small decorative element in each grid
                self._add_small_grid_element(draw, x + 5, y + 5, grid_width - 10, grid_height - 10)
        
        # Overlay text
        if spec.text_content:
            # Add semi-transparent overlay
            overlay = Image.new('RGBA', (spec.width, spec.height), (0, 0, 0, 100))
            image.paste(overlay, (0, 0), overlay)
            
            self._add_text_to_image(draw, spec.text_content, spec.brand_guidelines, 20, spec.height // 3, spec.width - 20, 2 * spec.height // 3)
        
        return image
    
    def _add_text_to_image(self, draw: ImageDraw, text: str, guidelines: BrandGuidelines, x: int, y: int, width: int, height: int):
        """Add text to image with proper formatting"""
        
        # For demo purposes, use simple text rendering
        # In production, would use proper font loading
        text_color = guidelines.color_palette.text_primary
        
        # Split text into lines if too long
        words = text.split()
        lines = []
        current_line = ""
        
        for word in words:
            test_line = current_line + " " + word if current_line else word
            # Simple width estimation (would use font metrics in production)
            if len(test_line) < 30:  # Rough character limit per line
                current_line = test_line
            else:
                if current_line:
                    lines.append(current_line)
                current_line = word
        
        if current_line:
            lines.append(current_line)
        
        # Draw lines
        line_height = 40
        total_text_height = len(lines) * line_height
        start_y = y + (height - total_text_height) // 2
        
        for i, line in enumerate(lines):
            text_y = start_y + i * line_height
            # Simple text drawing (would use proper font in production)
            draw.text((x + 10, text_y), line.upper(), fill=text_color)
    
    def _add_centered_text(self, draw: ImageDraw, text: str, guidelines: BrandGuidelines, width: int, height: int):
        """Add centered text to image"""
        
        text_color = guidelines.color_palette.text_primary
        
        # Simple centered text (would use proper font metrics in production)
        text_width = len(text) * 8  # Rough estimate
        text_height = 40
        
        text_x = (width - text_width) // 2
        text_y = (height - text_height) // 2
        
        draw.text((text_x, text_y), text.upper(), fill=text_color)
    
    def _add_decorative_elements(self, draw: ImageDraw, guidelines: BrandGuidelines, x: int, y: int, width: int, height: int):
        """Add decorative elements to image"""
        
        # Add some simple shapes as decorative elements
        accent_color = guidelines.color_palette.accent
        
        # Add circles
        for i in range(3):
            circle_x = x + random.randint(10, width - 20)
            circle_y = y + random.randint(10, height - 20)
            radius = random.randint(5, 15)
            draw.ellipse([circle_x - radius, circle_y - radius, circle_x + radius, circle_y + radius], 
                        fill=accent_color, outline=guidelines.color_palette.text_primary)
    
    def _add_visual_elements_to_card(self, draw: ImageDraw, guidelines: BrandGuidelines, x: int, y: int, width: int, height: int):
        """Add visual elements to card area"""
        
        # Add simple geometric shapes
        colors = [guidelines.color_palette.accent, guidelines.color_palette.secondary]
        
        for i in range(5):
            shape_x = x + random.randint(10, width - 30)
            shape_y = y + random.randint(10, height - 30)
            shape_size = random.randint(20, 40)
            color = random.choice(colors)
            
            if random.choice([True, False]):
                draw.rectangle([shape_x, shape_y, shape_x + shape_size, shape_y + shape_size], fill=color)
            else:
                draw.ellipse([shape_x, shape_y, shape_x + shape_size, shape_y + shape_size], fill=color)
    
    def _add_small_grid_element(self, draw: ImageDraw, x: int, y: int, width: int, height: int):
        """Add small element to grid cell"""
        
        # Add simple icon-like element
        center_x = x + width // 2
        center_y = y + height // 2
        radius = min(width, height) // 4
        
        draw.ellipse([center_x - radius, center_y - radius, center_x + radius, center_y + radius], 
                    fill="white", outline="black")
    
    def _create_gradient_background(self, image: Image, draw: ImageDraw, color_palette: ColorPalette):
        """Create gradient background"""
        
        # Simple gradient simulation (would use proper gradient in production)
        width, height = image.size
        
        for y in range(height):
            # Calculate gradient color
            ratio = y / height
            r = int(int(color_palette.primary[1:3], 16) * (1 - ratio) + int(color_palette.secondary[1:3], 16) * ratio)
            g = int(int(color_palette.primary[3:5], 16) * (1 - ratio) + int(color_palette.secondary[3:5], 16) * ratio)
            b = int(int(color_palette.primary[5:7], 16) * (1 - ratio) + int(color_palette.secondary[5:7], 16) * ratio)
            
            color = (r, g, b)
            draw.line([(0, y), (width, y)], fill=color)
    
    def _calculate_thumbnail_performance(self, image: Image, spec: AssetSpecification) -> float:
        """Calculate performance score for thumbnail"""
        
        metrics = self._analyze_thumbnail_metrics(image)
        weights = self.performance_analyzer["thumbnail_metrics"]
        
        total_score = 0.0
        total_weight = 0.0
        
        for metric, value in metrics.items():
            if metric in weights:
                weight = weights[metric]["weight"]
                min_value = weights[metric]["min"]
                
                # Normalize score (0-1)
                normalized_score = min(1.0, max(0.0, (value - min_value) / (1.0 - min_value)))
                
                total_score += normalized_score * weight
                total_weight += weight
        
        return total_score / total_weight if total_weight > 0 else 0.5
    
    def _analyze_thumbnail_metrics(self, image: Image) -> Dict[str, float]:
        """Analyze thumbnail performance metrics"""
        
        # Simplified metric analysis (would use proper computer vision in production)
        width, height = image.size
        
        # Contrast ratio (simplified)
        pixels = list(image.getdata())
        unique_colors = len(set(pixels))
        contrast_ratio = min(1.0, unique_colors / 1000)
        
        # Text readability (placeholder)
        text_readability = 0.85
        
        # Color harmony (placeholder)
        color_harmony = 0.78
        
        # Visual hierarchy (placeholder)
        visual_hierarchy = 0.82
        
        # Emotional impact (placeholder)
        emotional_impact = 0.75
        
        return {
            "contrast_ratio": contrast_ratio,
            "text_readability": text_readability,
            "color_harmony": color_harmony,
            "visual_hierarchy": visual_hierarchy,
            "emotional_impact": emotional_impact
        }
    
    async def generate_social_ad(self, spec: AssetSpecification) -> GeneratedAsset:
        """Generate social media ad (9:16 format)"""
        
        # Select appropriate template
        template = random.choice(self.social_ad_templates)
        
        # Create vertical image
        image = Image.new('RGB', (spec.width, spec.height), spec.brand_guidelines.color_palette.background)
        draw = ImageDraw.Draw(image)
        
        # Apply template design
        if template["name"] == "story_vertical":
            image = self._create_story_vertical_ad(image, draw, spec, template)
        elif template["name"] == "reels_tiktok":
            image = self._create_reels_tiktok_ad(image, draw, spec, template)
        else:
            image = self._create_carousel_post_ad(image, draw, spec, template)
        
        # Convert to base64
        buffer = io.BytesIO()
        image.save(buffer, format='PNG')
        image_base64 = base64.b64encode(buffer.getvalue()).decode()
        
        # Generate asset
        asset = GeneratedAsset(
            asset_id=f"social_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            asset_type=AssetType.SOCIAL_AD,
            file_path=f"/social_ads/social_ad_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png",
            base64_data=image_base64,
            metadata={
                "template": template["name"],
                "aspect_ratio": f"{spec.width}:{spec.height}",
                "platform_optimized": ["instagram", "facebook", "tiktok"]
            },
            performance_score=0.8,  # Placeholder
            created_at=datetime.now()
        )
        
        return asset
    
    def _create_story_vertical_ad(self, image: Image, draw: ImageDraw, spec: AssetSpecification, template: Dict[str, Any]) -> Image:
        """Create Instagram/Facebook Story ad"""
        
        # Gradient background
        self._create_gradient_background(image, draw, spec.brand_guidelines.color_palette)
        
        # Add brand logo area at top
        logo_height = 80
        draw.rectangle([0, 0, spec.width, logo_height], fill=spec.brand_guidelines.color_palette.primary)
        
        # Add main content area
        content_y = logo_height + 20
        if spec.text_content:
            self._add_text_to_image(draw, spec.text_content, spec.brand_guidelines, 20, content_y, spec.width - 20, spec.height - 120)
        
        # Add CTA at bottom
        cta_height = 60
        cta_y = spec.height - cta_y - 20
        draw.rectangle([20, cta_y, spec.width - 20, cta_y + cta_height], 
                      fill=spec.brand_guidelines.color_palette.accent)
        
        # Add decorative elements
        self._add_decorative_elements(draw, spec.brand_guidelines, 0, content_y, spec.width, cta_y - 20)
        
        return image
    
    def _create_reels_tiktok_ad(self, image: Image, draw: ImageDraw, spec: AssetSpecification, template: Dict[str, Any]) -> Image:
        """Create Reels/TikTok optimized ad"""
        
        # Bright, attention-grabbing background
        bg_color = spec.brand_guidelines.color_palette.accent
        draw.rectangle([0, 0, spec.width, spec.height], fill=bg_color)
        
        # Add title at top
        title_height = 100
        title_bg = Image.new('RGBA', (spec.width, title_height), (0, 0, 0, 180))
        image.paste(title_bg, (0, 0))
        
        if spec.text_content:
            # Add title text
            self._add_text_to_image(draw, spec.text_content, spec.brand_guidelines, 20, 20, spec.width - 20, title_height - 20)
        
        # Add visual elements in middle
        visual_y = title_height + 50
        self._add_visual_elements_to_card(draw, spec.brand_guidelines, 20, visual_y, spec.width - 40, spec.height - visual_y - 150)
        
        # Add swipe-up indicator at bottom
        indicator_y = spec.height - 80
        draw.rectangle([20, indicator_y, spec.width - 20, indicator_y + 60], 
                      fill=spec.brand_guidelines.color_palette.primary)
        
        return image
    
    def _create_carousel_post_ad(self, image: Image, draw: ImageDraw, spec: AssetSpecification, template: Dict[str, Any]) -> Image:
        """Create Instagram carousel post ad"""
        
        # Square format (1:1) - adjust to spec dimensions
        bg_color = spec.brand_guidelines.color_palette.background
        draw.rectangle([0, 0, spec.width, spec.height], fill=bg_color)
        
        # Create central focal point
        center_size = min(spec.width, spec.height) // 2
        center_x = (spec.width - center_size) // 2
        center_y = (spec.height - center_size) // 2
        
        draw.rectangle([center_x, center_y, center_x + center_size, center_y + center_size], 
                      fill=spec.brand_guidelines.color_palette.primary, 
                      outline=spec.brand_guidelines.color_palette.accent, width=5)
        
        # Add text in center
        if spec.text_content:
            self._add_centered_text(draw, spec.text_content, spec.brand_guidelines, center_size, center_size)
        
        # Add decorative corners
        corner_size = 30
        corners = [
            (20, 20),
            (spec.width - corner_size - 20, 20),
            (20, spec.height - corner_size - 20),
            (spec.width - corner_size - 20, spec.height - corner_size - 20)
        ]
        
        for corner_x, corner_y in corners:
            draw.rectangle([corner_x, corner_y, corner_x + corner_size, corner_y + corner_size], 
                          fill=spec.brand_guidelines.color_palette.accent)
        
        return image

# Initialize the Visual Asset Engine
visual_asset_engine = VisualAssetEngine()
