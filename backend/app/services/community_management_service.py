"""
VUC-2026 Omni-Responder & Community Management Service
AI-driven comment management with persona-based responses
"""

from typing import Dict, List, Optional, Tuple
from datetime import datetime, timedelta
import json
import re
from dataclasses import dataclass
from pydantic import BaseModel
from enum import Enum

from app.services.ai_service import AIService
from app.core.ai_intelligence import AIIntelligence

class CommenterPersona(Enum):
    """Commenter persona types"""
    EXPECTANT_MOTHER = "expectant_mother"
    PARENT_ADVICE = "parent_advice"
    KIDS_TOY_FEEDBACK = "kids_toy_feedback"
    GENERAL_AUDIENCE = "general_audience"
    TROLL_NEGATIVE = "troll_negative"
    SPAM_BOT = "spam_bot"

class ResponseTone(Enum):
    """Response tone types"""
    EMPATHETIC_REASSURING = "empathetic_reassuring"
    EXPERT_WARM = "expert_warm"
    FUN_ENGAGING = "fun_engaging"
    PROFESSIONAL = "professional"
    MODERATE_WARNING = "moderate_warning"
    IGNORE_DELETE = "ignore_delete"

@dataclass
class CommentAnalysis:
    """Comment analysis results"""
    persona: CommenterPersona
    sentiment: float  # -1.0 to 1.0
    urgency: float  # 0.0 to 1.0
    keywords: List[str]
    response_tone: ResponseTone
    confidence_score: float

class CommunityManagementService:
    """AI-driven community management service"""
    
    def __init__(self):
        self.ai_service = AIService()
        self.ai_intelligence = AIIntelligence()
        
        # Persona detection keywords
        self.persona_keywords = {
            CommenterPersona.EXPECTANT_MOTHER: [
                "pregnant", "pregnancy", "expecting", "baby bump", "due date",
                "trimester", "morning sickness", "cravings", "baby kicks",
                "nesting", "maternity", "first time mom", "pregnancy journey"
            ],
            CommenterPersona.PARENT_ADVICE: [
                "help", "advice", "how to", "what should", "recommendation",
                "suggestion", "experience", "struggling", "issue", "problem",
                "toddler", "newborn", "baby sleep", "feeding", "parenting"
            ],
            CommenterPersona.KIDS_TOY_FEEDBACK: [
                "toy", "play", "fun", "cool", "awesome", "love this",
                "want this", "birthday", "christmas", "gift", "kids",
                "children", "educational", "learning", "surprise egg"
            ],
            CommenterPersona.TROLL_NEGATIVE: [
                "stupid", "dumb", "fake", "garbage", "trash", "hate",
                "worst", "awful", "terrible", "dislike", "unsubscribe"
            ],
            CommenterPersona.SPAM_BOT: [
                "check out my", "visit my", "follow me", "subscribe to",
                "free money", "click here", "link in bio", "promotion",
                "discount", "offer", "buy now", "shop now"
            ]
        }
        
        # Response templates by tone
        self.response_templates = {
            ResponseTone.EMPATHETIC_REASSURING: {
                "pregnancy": [
                    "🤰 Congratulations on your pregnancy journey! Every moment is special. Have you checked out our week-by-week pregnancy series? It might help with what you're experiencing. 💕",
                    "Aw, those pregnancy emotions are so real! You're not alone in this. Remember to take it one day at a time. Sending you love and strength! 🌟",
                    "I remember those pregnancy days like it was yesterday! What you're feeling is completely normal. Here's our video on [specific topic] that might help: [link]"
                ],
                "general": [
                    "Thank you for sharing your journey! Your feelings are valid and important. We're here to support you every step of the way. 💖"
                ]
            },
            ResponseTone.EXPERT_WARM: {
                "parenting": [
                    "Great question! As a parenting community, we've found that [specific advice]. Have you tried our [specific video]? It walks you through the entire process step by step! 👶",
                    "You're not alone in this challenge! Many parents face this. Based on our experience, [expert advice]. Our [relevant video] covers this in detail with practical tips!",
                    "That's such a common concern! Here's what worked for our community: [specific solution]. We also have a comprehensive guide in our [video series] that you might find helpful."
                ],
                "product_recommendation": [
                    "For your specific need, I highly recommend checking out [affiliate product]. We've tested it extensively and it's been a game-changer for many parents in our community! 🌟 [affiliate link]",
                    "Based on your question, you might love [product category]. Our top recommendation is [specific product] - it's durable, safe, and kids absolutely love it! Here's where to get it: [affiliate link]"
                ]
            },
            ResponseTone.FUN_ENGAGING: {
                "toy_feedback": [
                    "🎉 Isn't it the coolest toy ever?! We had so much fun filming this! What's your favorite part? Let us know in the comments below! 🎈",
                    "YAY! So glad you love it! 🌈 Did you see the surprise at the end? Which toy should we unbox next? Comment below! 👇",
                    "AWESOME! 🚀 This toy is seriously amazing! Have you checked out our other [similar category] videos? There's so much more fun to discover! ✨"
                ],
                "general": [
                    "Thank you for your amazing comment! 😊 You made our day! Don't forget to like and subscribe for more fun content! 🎉"
                ]
            },
            ResponseTone.PROFESSIONAL: {
                "general": [
                    "Thank you for your feedback. We appreciate your engagement with our content. For more information, please visit our website or check our video description."
                ]
            },
            ResponseTone.MODERATE_WARNING: {
                "warning": [
                    "⚠️ Please keep comments respectful and family-friendly. We monitor this channel to ensure it remains a safe space for all viewers. Thank you for your understanding.",
                    "🚫 This comment violates our community guidelines. We're here to create a positive environment for families. Please review our community standards before commenting again."
                ]
            }
        }
        
        # Affiliate product database
        self.affiliate_products = {
            "baby_sleep": [
                {"name": "Hatch Baby Rest Sound Machine", "link": "affiliate_link_1", "commission": 0.10},
                {"name": "Love to Dream Swaddle", "link": "affiliate_link_2", "commission": 0.08}
            ],
            "feeding": [
                {"name": "MAM Baby Bottles", "link": "affiliate_link_3", "commission": 0.12},
                {"name": "Philips Avent Breast Pump", "link": "affiliate_link_4", "commission": 0.15}
            ],
            "toys": [
                {"name": "Melissa & Doug Wooden Toys", "link": "affiliate_link_5", "commission": 0.09},
                {"name": "Fisher-Price Infant Toys", "link": "affiliate_link_6", "commission": 0.07}
            ],
            "pregnancy": [
                {"name": "Belly Bandit Pregnancy Support", "link": "affiliate_link_7", "commission": 0.11},
                {"name": "What to Expect When You're Expecting Book", "link": "affiliate_link_8", "commission": 0.10}
            ]
        }

    async def analyze_comment(self, comment_text: str, video_context: Dict = None) -> CommentAnalysis:
        """
        Analyze comment and determine persona and response strategy
        """
        comment_lower = comment_text.lower()
        
        # Detect persona
        persona_scores = {}
        for persona, keywords in self.persona_keywords.items():
            score = sum(1 for keyword in keywords if keyword in comment_lower)
            persona_scores[persona] = score
        
        # Determine primary persona
        if persona_scores.get(CommenterPersona.SPAM_BOT, 0) >= 2:
            persona = CommenterPersona.SPAM_BOT
        elif persona_scores.get(CommenterPersona.TROLL_NEGATIVE, 0) >= 2:
            persona = CommenterPersona.TROLL_NEGATIVE
        elif persona_scores.get(CommenterPersona.EXPECTANT_MOTHER, 0) >= 1:
            persona = CommenterPersona.EXPECTANT_MOTHER
        elif persona_scores.get(CommenterPersona.PARENT_ADVICE, 0) >= 1:
            persona = CommenterPersona.PARENT_ADVICE
        elif persona_scores.get(CommenterPersona.KIDS_TOY_FEEDBACK, 0) >= 1:
            persona = CommenterPersona.KIDS_TOY_FEEDBACK
        else:
            persona = CommenterPersona.GENERAL_AUDIENCE
        
        # Determine sentiment (simplified)
        positive_words = ["love", "amazing", "great", "awesome", "best", "perfect", "thank", "helpful"]
        negative_words = ["hate", "terrible", "awful", "worst", "stupid", "fake", "garbage", "dislike"]
        
        positive_count = sum(1 for word in positive_words if word in comment_lower)
        negative_count = sum(1 for word in negative_words if word in comment_lower)
        
        sentiment = (positive_count - negative_count) / max(1, positive_count + negative_count)
        sentiment = max(-1.0, min(1.0, sentiment))
        
        # Determine urgency
        urgency_words = ["urgent", "help", "emergency", "asap", "immediately", "desperate"]
        urgency_score = sum(1 for word in urgency_words if word in comment_lower) / len(urgency_words)
        
        # Extract keywords
        keywords = []
        for persona_key, persona_keywords in self.persona_keywords.items():
            for keyword in persona_keywords:
                if keyword in comment_lower and keyword not in keywords:
                    keywords.append(keyword)
        
        # Determine response tone
        response_tone = self._determine_response_tone(persona, sentiment, urgency_score)
        
        # Calculate confidence
        max_persona_score = max(persona_scores.values()) if persona_scores else 0
        confidence_score = min(1.0, max_persona_score / 3.0)  # Normalize to 0-1
        
        return CommentAnalysis(
            persona=persona,
            sentiment=sentiment,
            urgency=urgency_score,
            keywords=keywords,
            response_tone=response_tone,
            confidence_score=confidence_score
        )

    def _determine_response_tone(self, 
                               persona: CommenterPersona, 
                               sentiment: float, 
                               urgency: float) -> ResponseTone:
        """
        Determine appropriate response tone based on analysis
        """
        if persona == CommenterPersona.SPAM_BOT:
            return ResponseTone.IGNORE_DELETE
        elif persona == CommenterPersona.TROLL_NEGATIVE:
            return ResponseTone.MODERATE_WARNING
        elif persona == CommenterPersona.EXPECTANT_MOTHER:
            return ResponseTone.EMPATHETIC_REASSURING
        elif persona == CommenterPersona.PARENT_ADVICE:
            return ResponseTone.EXPERT_WARM
        elif persona == CommenterPersona.KIDS_TOY_FEEDBACK:
            return ResponseTone.FUN_ENGAGING
        elif urgency > 0.5:
            return ResponseTone.EXPERT_WARM
        else:
            return ResponseTone.PROFESSIONAL

    async def generate_response(self, 
                              comment_analysis: CommentAnalysis,
                              video_context: Dict = None,
                              affiliate_enabled: bool = True) -> Dict:
        """
        Generate AI-powered response based on comment analysis
        """
        # Get response templates
        templates = self.response_templates.get(comment_analysis.response_tone, {})
        
        # Select appropriate template category
        if comment_analysis.persona == CommenterPersona.EXPECTANT_MOTHER:
            category = "pregnancy"
        elif comment_analysis.persona == CommenterPersona.PARENT_ADVICE:
            category = "parenting"
        elif comment_analysis.persona == CommenterPersona.KIDS_TOY_FEEDBACK:
            category = "toy_feedback"
        else:
            category = "general"
        
        # Get template
        category_templates = templates.get(category, templates.get("general", []))
        
        if not category_templates:
            # Generate AI response if no template available
            ai_response = await self._generate_ai_response(comment_analysis, video_context)
            return ai_response
        
        # Select template (rotate through options)
        template_index = hash(comment_analysis.keywords[0] if comment_analysis.keywords else "default") % len(category_templates)
        base_response = category_templates[template_index]
        
        # Add affiliate links if appropriate
        if affiliate_enabled and comment_analysis.response_tone == ResponseTone.EXPERT_WARM:
            affiliate_link = self._get_affiliate_link(comment_analysis.keywords)
            if affiliate_link:
                base_response += f" {affiliate_link}"
        
        # Add emojis based on persona
        emojis = self._get_persona_emojis(comment_analysis.persona)
        if emojis and not any(emoji in base_response for emoji in emojis):
            base_response += f" {emojis[0]}"
        
        return {
            "response_text": base_response,
            "persona": comment_analysis.persona.value,
            "tone": comment_analysis.response_tone.value,
            "confidence": comment_analysis.confidence_score,
            "includes_affiliate": affiliate_enabled and comment_analysis.response_tone == ResponseTone.EXPERT_WARM,
            "auto_post": True,
            "generated_at": datetime.now().isoformat()
        }

    async def _generate_ai_response(self, 
                                  comment_analysis: CommentAnalysis,
                                  video_context: Dict = None) -> Dict:
        """
        Generate AI response when templates are not available
        """
        prompt = f"""
        Generate a response for a YouTube comment based on this analysis:
        
        Commenter Persona: {comment_analysis.persona.value}
        Sentiment: {comment_analysis.sentiment}
        Urgency: {comment_analysis.urgency}
        Keywords: {', '.join(comment_analysis.keywords)}
        Response Tone: {comment_analysis.response_tone.value}
        
        Video Context: {video_context or 'General family/kids content'}
        
        Guidelines:
        - Keep response under 150 characters
        - Use appropriate emojis
        - Be helpful and family-friendly
        - Include call-to-action if appropriate
        - Avoid controversial topics
        """
        
        ai_response = await self.ai_service.generate_text(prompt)
        
        return {
            "response_text": ai_response[:200],  # Limit length
            "persona": comment_analysis.persona.value,
            "tone": comment_analysis.response_tone.value,
            "confidence": 0.7,  # Lower confidence for AI-generated
            "includes_affiliate": False,
            "auto_post": comment_analysis.confidence_score > 0.7,
            "generated_at": datetime.now().isoformat()
        }

    def _get_affiliate_link(self, keywords: List[str]) -> Optional[str]:
        """
        Get appropriate affiliate link based on keywords
        """
        keyword_lower = ' '.join(keywords).lower()
        
        for category, products in self.affiliate_products.items():
            if any(keyword in keyword_lower for keyword in [category, category.replace('_', ' ')]):
                product = products[0]  # Get top product
                return f"Check out {product['name']}: {product['link']}"
        
        return None

    def _get_persona_emojis(self, persona: CommenterPersona) -> List[str]:
        """
        Get appropriate emojis for persona
        """
        emoji_map = {
            CommenterPersona.EXPECTANT_MOTHER: ["🤰", "💕", "🌟"],
            CommenterPersona.PARENT_ADVICE: ["👶", "💡", "🌈"],
            CommenterPersona.KIDS_TOY_FEEDBACK: ["🎉", "🎈", "🚀"],
            CommenterPersona.GENERAL_AUDIENCE: ["😊", "👍", "💖"],
            CommenterPersona.TROLL_NEGATIVE: ["⚠️", "🚫"],
            CommenterPersona.SPAM_BOT: ["🤖", "📧"]
        }
        
        return emoji_map.get(persona, [])

    async def process_new_comments(self, 
                                 video_id: str,
                                 max_comments: int = 50,
                                 auto_reply: bool = True) -> Dict:
        """
        Process new comments for a video
        """
        try:
            # Fetch new comments (mock implementation)
            comments = await self._fetch_youtube_comments(video_id, max_comments)
            
            processed_comments = []
            auto_replies = []
            
            for comment in comments:
                # Analyze comment
                analysis = await self.analyze_comment(comment['text'], comment.get('context'))
                
                # Generate response
                if auto_reply and analysis.response_tone != ResponseTone.IGNORE_DELETE:
                    response = await self.generate_response(analysis, comment.get('context'))
                    
                    # Post response if confidence is high
                    if response.get('auto_post', False):
                        reply_result = await self._post_youtube_reply(
                            comment['id'], 
                            response['response_text']
                        )
                        
                        auto_replies.append({
                            "comment_id": comment['id'],
                            "response": response,
                            "reply_result": reply_result
                        })
                
                processed_comments.append({
                    "comment_id": comment['id'],
                    "text": comment['text'],
                    "analysis": analysis,
                    "processed_at": datetime.now().isoformat()
                })
            
            # Log processing for analytics
            await self.ai_intelligence.log_comment_processing(
                video_id=video_id,
                comments_processed=len(processed_comments),
                auto_replies_posted=len(auto_replies),
                persona_distribution=self._calculate_persona_distribution(processed_comments)
            )
            
            return {
                "video_id": video_id,
                "comments_processed": len(processed_comments),
                "auto_replies_posted": len(auto_replies),
                "processed_comments": processed_comments,
                "auto_replies": auto_replies,
                "processing_timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            raise Exception(f"Comment processing failed: {str(e)}")

    async def _fetch_youtube_comments(self, video_id: str, max_comments: int) -> List[Dict]:
        """
        Fetch comments from YouTube (mock implementation)
        """
        # This would integrate with YouTube Data API
        # For now, return mock data
        return [
            {
                "id": "comment_1",
                "text": "I'm 20 weeks pregnant and feeling so overwhelmed! Any advice?",
                "context": {"video_category": "pregnancy"}
            },
            {
                "id": "comment_2", 
                "text": "This toy looks amazing! My son would love this for his birthday!",
                "context": {"video_category": "toys"}
            },
            {
                "id": "comment_3",
                "text": "Help! My 6-month-old won't sleep through the night. What should I do?",
                "context": {"video_category": "baby_sleep"}
            }
        ][:max_comments]

    async def _post_youtube_reply(self, comment_id: str, reply_text: str) -> Dict:
        """
        Post reply to YouTube comment (mock implementation)
        """
        # This would integrate with YouTube Data API
        return {
            "success": True,
            "reply_id": f"reply_{comment_id}_{datetime.now().timestamp()}",
            "posted_at": datetime.now().isoformat()
        }

    def _calculate_persona_distribution(self, processed_comments: List[Dict]) -> Dict:
        """
        Calculate distribution of commenter personas
        """
        distribution = {}
        for comment in processed_comments:
            persona = comment['analysis'].persona.value
            distribution[persona] = distribution.get(persona, 0) + 1
        
        return distribution

    async def get_community_analytics(self, 
                                    video_id: str = None,
                                    time_range: str = "7_days") -> Dict:
        """
        Get community management analytics
        """
        try:
            analytics = await self.ai_intelligence.get_community_analytics(
                video_id=video_id,
                time_range=time_range
            )
            
            return {
                "analytics": analytics,
                "retrieved_at": datetime.now().isoformat()
            }
            
        except Exception as e:
            raise Exception(f"Analytics retrieval failed: {str(e)}")

    async def update_response_templates(self, 
                                     tone: ResponseTone,
                                     category: str,
                                     templates: List[str]) -> Dict:
        """
        Update response templates
        """
        try:
            if tone not in self.response_templates:
                self.response_templates[tone] = {}
            
            self.response_templates[tone][category] = templates
            
            return {
                "success": True,
                "tone": tone.value,
                "category": category,
                "template_count": len(templates),
                "updated_at": datetime.now().isoformat()
            }
            
        except Exception as e:
            raise Exception(f"Template update failed: {str(e)}")

    async def get_engagement_metrics(self, video_id: str) -> Dict:
        """
        Get engagement metrics for community management
        """
        try:
            metrics = await self.ai_intelligence.get_engagement_metrics(video_id)
            
            return {
                "video_id": video_id,
                "metrics": metrics,
                "retrieved_at": datetime.now().isoformat()
            }
            
        except Exception as e:
            raise Exception(f"Metrics retrieval failed: {str(e)}")
