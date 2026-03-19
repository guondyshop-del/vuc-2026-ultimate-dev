"""
Vectorized Memory System - PostgreSQL + pgvector
Store and retrieve trends, viral patterns, and user preferences as vectors
"""

import asyncio
import logging
import json
import numpy as np
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime, timedelta
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Text, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.dialects.postgresql import UUID
import uuid

# Temporarily disabled due to missing dependency
try:
    from sentence_transformers import SentenceTransformer
    SENTENCE_TRANSFORMERS_AVAILABLE = True
except ImportError:
    SENTENCE_TRANSFORMERS_AVAILABLE = False

try:
    import google.generativeai as genai
    from google.generativeai import GenerativeModel
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False

logger = logging.getLogger(__name__)

Base = declarative_base()

class MemoryVector(Base):
    """Memory vector storage table"""
    __tablename__ = "memory_vectors"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    content_type = Column(String(50), nullable=False)  # trend_pattern, viral_video, user_preference
    content_id = Column(String(255), nullable=False)
    vector = Column(Text, nullable=False)  # JSON string of vector
    extra_data = Column(JSON, nullable=True)  # Renamed from metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    embedding_model = Column(String(100), default="all-MiniLM-L6-v2")
    similarity_score = Column(Float, default=0.0)

class TrendPattern(Base):
    """Trend pattern storage table"""
    __tablename__ = "trend_patterns"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    trend_name = Column(String(255), nullable=False)
    niche = Column(String(100), nullable=False)
    trend_score = Column(Float, nullable=False)
    growth_rate = Column(Float, nullable=False)
    keywords = Column(JSON, nullable=True)
    extra_data = Column(JSON, nullable=True)  # Renamed from metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class VectorizedMemorySystem:
    """Vectorized memory system for intelligent content storage and retrieval"""
    
    def __init__(self, database_url: str, gemini_api_key: str):
        self.engine = create_engine(database_url)
        self.SessionLocal = sessionmaker(bind=self.engine)
        
        # Initialize embedding model
        if SENTENCE_TRANSFORMERS_AVAILABLE:
            self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
        else:
            self.embedding_model = None
        
        # Initialize Gemini for analysis
        if GEMINI_AVAILABLE:
            genai.configure(api_key=gemini_api_key)
            self.gemini_model = GenerativeModel('gemini-2.0-pro')
        else:
            self.gemini_model = None
        
        # Create tables
        Base.metadata.create_all(bind=self.engine)
        
        logger.info("Vectorized Memory System initialized")
    
    def get_session(self) -> Session:
        """Get database session"""
        return self.SessionLocal()
    
    async def store_trend_pattern(self, trend_data: Dict[str, Any]) -> str:
        """Store trend pattern as vector"""
        if not self.embedding_model:
            logger.warning("Embedding model not available, skipping trend storage")
            return ""
            
        session = self.get_session()
        try:
            trend_text = self._create_trend_text(trend_data)
            
            # Generate embedding
            embedding = self.embedding_model.encode(trend_text)
            vector_str = json.dumps(embedding.tolist())
            
            # Store memory vector
            memory_vector = MemoryVector(
                content_type="trend_pattern",
                content_id=trend_data.get("trend_name", f"trend_{uuid.uuid4()}"),
                vector=vector_str,
                extra_data=trend_data,
                embedding_model="all-MiniLM-L6-v2"
            )
            session.add(memory_vector)
            session.commit()
            
            logger.info(f"Stored trend pattern: {trend_data.get('trend_name')}")
            return str(memory_vector.id)
            
        except Exception as e:
            session.rollback()
            logger.error(f"Failed to store trend pattern: {str(e)}")
            raise
        finally:
            session.close()
    
    async def store_viral_video(self, video_data: Dict[str, Any]) -> str:
        """Store viral video as vector"""
        if not self.embedding_model:
            logger.warning("Embedding model not available, skipping video storage")
            return ""
            
        session = self.get_session()
        try:
            video_text = self._create_video_text(video_data)
            
            # Generate embedding
            embedding = self.embedding_model.encode(video_text)
            vector_str = json.dumps(embedding.tolist())
            
            # Store memory vector
            memory_vector = MemoryVector(
                content_type="viral_video",
                content_id=video_data.get("video_id", f"video_{uuid.uuid4()}"),
                vector=vector_str,
                extra_data=video_data,
                embedding_model="all-MiniLM-L6-v2"
            )
            session.add(memory_vector)
            session.commit()
            
            logger.info(f"Stored viral video: {video_data.get('video_id')}")
            return str(memory_vector.id)
            
        except Exception as e:
            session.rollback()
            logger.error(f"Failed to store viral video: {str(e)}")
            raise
        finally:
            session.close()
    
    async def store_user_preference(self, user_data: Dict[str, Any]) -> str:
        """Store user preference as vector"""
        if not self.embedding_model:
            logger.warning("Embedding model not available, skipping user storage")
            return ""
            
        session = self.get_session()
        try:
            user_text = self._create_user_text(user_data)
            
            # Generate embedding
            embedding = self.embedding_model.encode(user_text)
            vector_str = json.dumps(embedding.tolist())
            
            # Store memory vector
            memory_vector = MemoryVector(
                content_type="user_preference",
                content_id=user_data.get("user_id", f"user_{uuid.uuid4()}"),
                vector=vector_str,
                extra_data=user_data,
                embedding_model="all-MiniLM-L6-v2"
            )
            session.add(memory_vector)
            session.commit()
            
            logger.info(f"Stored user preference: {user_data.get('user_id')}")
            return str(memory_vector.id)
            
        except Exception as e:
            session.rollback()
            logger.error(f"Failed to store user preference: {str(e)}")
            raise
        finally:
            session.close()
    
    async def search_similar_content(self, query: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Search for similar content using vector similarity"""
        if not self.embedding_model:
            logger.warning("Embedding model not available, returning empty results")
            return []
            
        session = self.get_session()
        try:
            # Generate query embedding
            query_embedding = self.embedding_model.encode(query["query_text"])
            
            # Get all vectors of the specified type
            vectors = session.query(MemoryVector).filter(
                MemoryVector.content_type == query.get("content_type", "trend_pattern")
            ).all()
            
            # Calculate similarities
            results = []
            for vector in vectors:
                stored_embedding = np.array(json.loads(vector.vector))
                similarity = np.dot(query_embedding, stored_embedding) / (
                    np.linalg.norm(query_embedding) * np.linalg.norm(stored_embedding)
                )
                
                if similarity > query.get("min_similarity", 0.5):
                    results.append({
                        "content_id": vector.content_id,
                        "similarity_score": float(similarity),
                        "extra_data": vector.extra_data,
                        "created_at": vector.created_at.isoformat()
                    })
            
            # Sort by similarity
            results.sort(key=lambda x: x["similarity_score"], reverse=True)
            
            return results[:query.get("limit", 10)]
            
        except Exception as e:
            logger.error(f"Error searching similar content: {e}")
            return []
        finally:
            session.close()
    
    def _create_trend_text(self, trend_data: Dict[str, Any]) -> str:
        """Create text representation for trend embedding"""
        return f"""
        Trend: {trend_data.get('trend_name', '')}
        Niche: {trend_data.get('niche', '')}
        Score: {trend_data.get('trend_score', 0)}
        Growth: {trend_data.get('growth_rate', 0)}%
        Keywords: {', '.join(trend_data.get('keywords', []))}
        Description: {trend_data.get('description', '')}
        """
    
    def _create_video_text(self, video_data: Dict[str, Any]) -> str:
        """Create text representation for video embedding"""
        return f"""
        Video: {video_data.get('title', '')}
        Description: {video_data.get('description', '')}
        Tags: {', '.join(video_data.get('tags', []))}
        Category: {video_data.get('category', '')}
        Duration: {video_data.get('duration', 0)}s
        Views: {video_data.get('views', 0)}
        Engagement: {video_data.get('engagement_rate', 0)}%
        """
    
    def _create_user_text(self, user_data: Dict[str, Any]) -> str:
        """Create text representation for user embedding"""
        return f"""
        User: {user_data.get('user_id', '')}
        Interests: {', '.join(user_data.get('interests', []))}
        Preferences: {', '.join(user_data.get('preferences', []))}
        Watch History: {', '.join(user_data.get('watch_history', []))}
        Engagement Level: {user_data.get('engagement_level', '')}
        """
    
    async def get_memory_stats(self) -> Dict[str, Any]:
        """Get memory system statistics"""
        session = self.get_session()
        try:
            trend_count = session.query(MemoryVector).filter(
                MemoryVector.content_type == "trend_pattern"
            ).count()
            
            video_count = session.query(MemoryVector).filter(
                MemoryVector.content_type == "viral_video"
            ).count()
            
            user_count = session.query(MemoryVector).filter(
                MemoryVector.content_type == "user_preference"
            ).count()
            
            return {
                "trend_patterns": trend_count,
                "viral_videos": video_count,
                "user_preferences": user_count,
                "embedding_model": "all-MiniLM-L6-v2",
                "last_updated": datetime.now().isoformat()
            }
            
        finally:
            session.close()

# Global instance for API import
def get_vectorized_memory(database_url: str, gemini_api_key: str) -> VectorizedMemorySystem:
    """Get vectorized memory system instance"""
    return VectorizedMemorySystem(database_url, gemini_api_key)
