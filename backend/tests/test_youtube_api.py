"""
VUC-2026 YouTube API Test Suite
Comprehensive testing for YouTube API integration
"""

import pytest
import asyncio
import json
from unittest.mock import Mock, patch, AsyncMock
from datetime import datetime, timedelta
import os
import sys

# Add the app directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from app.services.youtube_api_service import YouTubeAPIService, YouTubeVideo, YouTubeChannel, YouTubePlaylist
from app.services.youtube_auth_service import YouTubeAuthService, OAuthToken, UserProfile
from app.services.youtube_upload_service import YouTubeUploadService, VideoMetadata, UploadProgress
from app.services.youtube_analytics_service import YouTubeAnalyticsService, VideoAnalytics, ChannelAnalytics
from app.services.vuc_youtube_neural_core import VUCYouTubeNeuralCore, ContentStrategy

class TestYouTubeAPIService:
    """Test YouTube API Service"""
    
    @pytest.fixture
    def youtube_service(self):
        """Create YouTube API service instance"""
        with patch.dict(os.environ, {'YOUTUBE_API_KEY': 'test_api_key'}):
            return YouTubeAPIService()
    
    @pytest.mark.asyncio
    async def test_search_videos(self, youtube_service):
        """Test video search functionality"""
        with patch('aiohttp.ClientSession.get') as mock_get:
            # Mock response
            mock_response = Mock()
            mock_response.status = 200
            mock_response.json = AsyncMock(return_value={
                'items': [
                    {
                        'id': {'videoId': 'test_video_id'},
                        'snippet': {
                            'title': 'Test Video',
                            'description': 'Test Description',
                            'channelId': 'test_channel_id',
                            'channelTitle': 'Test Channel',
                            'publishedAt': '2024-01-01T00:00:00Z',
                            'tags': ['test', 'video'],
                            'categoryId': '22',
                            'thumbnails': {'high': {'url': 'http://test.com/thumb.jpg'}}
                        },
                        'statistics': {
                            'viewCount': '1000',
                            'likeCount': '100',
                            'commentCount': '10'
                        },
                        'contentDetails': {
                            'duration': 'PT5M30S'
                        }
                    }
                ]
            })
            
            mock_get.return_value.__aenter__.return_value = mock_response
            
            # Test search
            videos = await youtube_service.search_videos('test query', max_results=1)
            
            assert len(videos) == 1
            assert videos[0].video_id == 'test_video_id'
            assert videos[0].title == 'Test Video'
            assert videos[0].view_count == 1000
    
    @pytest.mark.asyncio
    async def test_get_video_details(self, youtube_service):
        """Test getting video details"""
        with patch('aiohttp.ClientSession.get') as mock_get:
            mock_response = Mock()
            mock_response.status = 200
            mock_response.json = AsyncMock(return_value={
                'items': [
                    {
                        'id': 'test_video_id',
                        'snippet': {
                            'title': 'Test Video',
                            'description': 'Test Description',
                            'channelId': 'test_channel_id',
                            'channelTitle': 'Test Channel',
                            'publishedAt': '2024-01-01T00:00:00Z',
                            'tags': ['test', 'video'],
                            'categoryId': '22',
                            'thumbnails': {'high': {'url': 'http://test.com/thumb.jpg'}}
                        },
                        'statistics': {
                            'viewCount': '1000',
                            'likeCount': '100',
                            'commentCount': '10'
                        },
                        'contentDetails': {
                            'duration': 'PT5M30S'
                        }
                    }
                ]
            })
            
            mock_get.return_value.__aenter__.return_value = mock_response
            
            videos = await youtube_service.get_video_details(['test_video_id'])
            
            assert len(videos) == 1
            assert videos[0].video_id == 'test_video_id'
    
    @pytest.mark.asyncio
    async def test_get_channel_details(self, youtube_service):
        """Test getting channel details"""
        with patch('aiohttp.ClientSession.get') as mock_get:
            mock_response = Mock()
            mock_response.status = 200
            mock_response.json = AsyncMock(return_value={
                'items': [
                    {
                        'id': 'test_channel_id',
                        'snippet': {
                            'title': 'Test Channel',
                            'description': 'Test Channel Description',
                            'publishedAt': '2024-01-01T00:00:00Z',
                            'country': 'US',
                            'thumbnails': {'high': {'url': 'http://test.com/channel.jpg'}}
                        },
                        'statistics': {
                            'subscriberCount': '10000',
                            'videoCount': '100',
                            'viewCount': '1000000'
                        }
                    }
                ]
            })
            
            mock_get.return_value.__aenter__.return_value = mock_response
            
            channel = await youtube_service.get_channel_details('test_channel_id')
            
            assert channel is not None
            assert channel.channel_id == 'test_channel_id'
            assert channel.title == 'Test Channel'
            assert channel.subscriber_count == 10000
    
    @pytest.mark.asyncio
    async def test_get_trending_videos(self, youtube_service):
        """Test getting trending videos"""
        with patch('aiohttp.ClientSession.get') as mock_get:
            mock_response = Mock()
            mock_response.status = 200
            mock_response.json = AsyncMock(return_value={
                'items': [
                    {
                        'id': 'trending_video_id',
                        'snippet': {
                            'title': 'Trending Video',
                            'description': 'Trending Description',
                            'channelId': 'trending_channel_id',
                            'channelTitle': 'Trending Channel',
                            'publishedAt': '2024-01-01T00:00:00Z',
                            'tags': ['trending', 'video'],
                            'categoryId': '22',
                            'thumbnails': {'high': {'url': 'http://test.com/trending.jpg'}}
                        },
                        'statistics': {
                            'viewCount': '1000000',
                            'likeCount': '100000',
                            'commentCount': '1000'
                        },
                        'contentDetails': {
                            'duration': 'PT10M0S'
                        }
                    }
                ]
            })
            
            mock_get.return_value.__aenter__.return_value = mock_response
            
            videos = await youtube_service.get_trending_videos(region_code='US')
            
            assert len(videos) == 1
            assert videos[0].video_id == 'trending_video_id'
    
    def test_parse_video_data(self, youtube_service):
        """Test video data parsing"""
        item = {
            'id': 'test_video_id',
            'snippet': {
                'title': 'Test Video',
                'description': 'Test Description',
                'channelId': 'test_channel_id',
                'channelTitle': 'Test Channel',
                'publishedAt': '2024-01-01T00:00:00Z',
                'tags': ['test', 'video'],
                'categoryId': '22',
                'thumbnails': {'high': {'url': 'http://test.com/thumb.jpg'}}
            },
            'statistics': {
                'viewCount': '1000',
                'likeCount': '100',
                'commentCount': '10'
            },
            'contentDetails': {
                'duration': 'PT5M30S'
            }
        }
        
        video = youtube_service._parse_video_data(item)
        
        assert video is not None
        assert video.video_id == 'test_video_id'
        assert video.title == 'Test Video'
        assert video.view_count == 1000

class TestYouTubeAuthService:
    """Test YouTube Auth Service"""
    
    @pytest.fixture
    def auth_service(self):
        """Create auth service instance"""
        with patch.dict(os.environ, {
            'GOOGLE_CLIENT_ID': 'test_client_id',
            'GOOGLE_CLIENT_SECRET': 'test_client_secret',
            'REDIS_URL': 'redis://localhost:6379/0'
        }):
            return YouTubeAuthService()
    
    def test_get_authorization_url(self, auth_service):
        """Test getting authorization URL"""
        with patch('secrets.token_urlsafe', return_value='test_state'):
            with patch('redis.from_url') as mock_redis:
                mock_client = Mock()
                mock_redis.return_value = mock_client
                
                auth_data = auth_service.get_authorization_url()
                
                assert 'authorization_url' in auth_data
                assert 'state' in auth_data
                assert auth_data['state'] == 'test_state'
                assert auth_data['expires_in'] == 600
    
    @pytest.mark.asyncio
    async def test_exchange_code_for_tokens(self, auth_service):
        """Test exchanging code for tokens"""
        with patch('redis.from_url') as mock_redis:
            mock_client = Mock()
            mock_redis.return_value = mock_client
            
            # Mock flow data
            mock_flow = Mock()
            mock_flow.credentials.token = 'access_token'
            mock_flow.credentials.refresh_token = 'refresh_token'
            mock_flow.credentials.expiry = 3600
            mock_flow.credentials.scopes = ['youtube.readonly']
            
            mock_client.get.return_value = pickle.dumps(mock_flow)
            mock_flow.fetch_token = Mock()
            
            token = await auth_service.exchange_code_for_tokens('test_code', 'test_state')
            
            assert token is not None
            assert token.access_token == 'access_token'
            assert token.refresh_token == 'refresh_token'
    
    @pytest.mark.asyncio
    async def test_get_user_profile(self, auth_service):
        """Test getting user profile"""
        with patch('redis.from_url') as mock_redis:
            mock_client = Mock()
            mock_redis.return_value = mock_client
            
            # Mock token
            token_data = {
                'access_token': 'access_token',
                'refresh_token': 'refresh_token',
                'token_uri': 'https://oauth2.googleapis.com/token',
                'client_id': 'test_client_id',
                'client_secret': 'test_client_secret',
                'scopes': ['youtube.readonly']
            }
            mock_client.get.return_value = json.dumps(token_data).encode()
            
            with patch('googleapiclient.discovery.build') as mock_build:
                mock_youtube = Mock()
                mock_build.return_value = mock_youtube
                
                mock_youtube.channels.return_value.list.return_value.execute.return_value = {
                    'items': [
                        {
                            'id': 'test_channel_id',
                            'snippet': {
                                'title': 'Test Channel',
                                'customUrl': 'testcustom',
                                'thumbnails': {'high': {'url': 'http://test.com/channel.jpg'}}
                            },
                            'statistics': {
                                'subscriberCount': '10000'
                            }
                        }
                    ]
                }
                
                profile = await auth_service.get_user_profile('test_state')
                
                assert profile is not None
                assert profile.channel_id == 'test_channel_id'
                assert profile.channel_title == 'Test Channel'

class TestYouTubeUploadService:
    """Test YouTube Upload Service"""
    
    @pytest.fixture
    def upload_service(self):
        """Create upload service instance"""
        return YouTubeUploadService()
    
    def test_validate_video_file(self, upload_service):
        """Test video file validation"""
        # Create a temporary test file
        test_file = 'test_video.mp4'
        with open(test_file, 'wb') as f:
            f.write(b'fake video content')
        
        try:
            validation = upload_service.validate_video_file(test_file)
            
            assert validation['valid'] == True
            assert 'file_size' in validation
            assert 'duration' in validation
            assert 'mime_type' in validation
        finally:
            os.remove(test_file)
    
    def test_get_mime_type(self, upload_service):
        """Test MIME type detection"""
        mime_type = upload_service._get_mime_type('test_video.mp4')
        assert mime_type == 'video/mp4'
        
        mime_type = upload_service._get_mime_type('test_file.txt')
        assert mime_type == 'text/plain'
    
    def test_wrap_text(self, upload_service):
        """Test text wrapping for thumbnails"""
        long_text = "This is a very long title that should be wrapped into multiple lines for better readability"
        lines = upload_service._wrap_text(long_text, 20)
        
        assert len(lines) > 1
        assert all(len(line) <= 20 for line in lines)

class TestYouTubeAnalyticsService:
    """Test YouTube Analytics Service"""
    
    @pytest.fixture
    def analytics_service(self):
        """Create analytics service instance"""
        return YouTubeAnalyticsService()
    
    @pytest.mark.asyncio
    async def test_get_real_time_metrics(self, analytics_service):
        """Test getting real-time metrics"""
        with patch('googleapiclient.discovery.build') as mock_build:
            mock_youtube = Mock()
            mock_build.return_value = mock_youtube
            
            mock_youtube.channels.return_value.list.return_value.execute.return_value = {
                'items': [
                    {
                        'statistics': {
                            'viewCount': '1000000',
                            'subscriberCount': '10000',
                            'videoCount': '100',
                            'commentCount': '5000'
                        }
                    }
                ]
            }
            
            metrics = await analytics_service.get_real_time_metrics('test_channel_id')
            
            assert 'views' in metrics
            assert 'subscribers' in metrics
            assert 'videos' in metrics
            assert 'comments' in metrics
            assert metrics['views'] == 1000000
    
    @pytest.mark.asyncio
    async def test_get_engagement_metrics(self, analytics_service):
        """Test getting engagement metrics"""
        with patch('googleapiclient.discovery.build') as mock_build:
            mock_youtube = Mock()
            mock_build.return_value = mock_youtube
            
            mock_youtube.videos.return_value.list.return_value.execute.return_value = {
                'items': [
                    {
                        'id': 'test_video_id',
                        'statistics': {
                            'viewCount': '10000',
                            'likeCount': '1000',
                            'commentCount': '100'
                        }
                    }
                ]
            }
            
            engagement = await analytics_service.get_engagement_metrics(['test_video_id'])
            
            assert 'test_video_id' in engagement
            assert 'engagement_rate' in engagement['test_video_id']
            assert 'like_rate' in engagement['test_video_id']
            assert 'comment_rate' in engagement['test_video_id']

class TestVUCYouTubeNeuralCore:
    """Test VUC YouTube Neural Core"""
    
    @pytest.fixture
    def neural_core(self):
        """Create neural core instance"""
        return VUCYouTubeNeuralCore()
    
    @pytest.mark.asyncio
    async def test_generate_content_strategy(self, neural_core):
        """Test content strategy generation"""
        video_topic = "How to cook pasta"
        target_audience = {
            'age_groups': 'mixed',
            'interests': 'cooking',
            'experience_level': 'beginner'
        }
        
        strategy = await neural_core.generate_content_strategy(video_topic, target_audience)
        
        assert strategy is not None
        assert strategy.title_optimization != ""
        assert strategy.description_optimization != ""
        assert isinstance(strategy.tags_optimization, list)
        assert isinstance(strategy.thumbnail_suggestions, list)
        assert isinstance(strategy.predicted_performance, float)
        assert isinstance(strategy.confidence_score, float)
    
    def test_extract_topic_features(self, neural_core):
        """Test topic feature extraction"""
        topic = "How to cook pasta like a professional chef"
        features = neural_core._extract_topic_features(topic)
        
        assert isinstance(features, np.ndarray)
        assert len(features) == 20  # Expected feature vector size
    
    def test_extract_audience_features(self, neural_core):
        """Test audience feature extraction"""
        audience = {
            'age_groups': {
                'age13-17': 10,
                'age18-24': 30,
                'age25-34': 40,
                'age35-44': 15,
                'age45-54': 5
            },
            'genders': {
                'male': 60,
                'female': 40
            },
            'devices': {
                'desktop': 50,
                'mobile': 45,
                'tablet': 5
            }
        }
        
        features = neural_core._extract_audience_features(audience)
        
        assert isinstance(features, np.ndarray)
        assert len(features) == 30  # Expected feature vector size
    
    @pytest.mark.asyncio
    async def test_analyze_trending_patterns(self, neural_core):
        """Test trending pattern analysis"""
        with patch('app.services.vuc_youtube_neural_core.youtube_service.get_trending_videos') as mock_trending:
            mock_trending.return_value = [
                Mock(
                    title="Trending video 1",
                    tags=["trending", "viral"],
                    view_count=1000000
                ),
                Mock(
                    title="Another trending video",
                    tags=["trending", "popular"],
                    view_count=500000
                )
            ]
            
            patterns = await neural_core.analyze_trending_patterns()
            
            assert len(patterns) > 0
            assert patterns[0].pattern_type == "viral_content"
            assert isinstance(patterns[0].keywords, list)
            assert isinstance(patterns[0].virality_score, float)

class TestIntegration:
    """Integration tests for YouTube services"""
    
    @pytest.mark.asyncio
    async def test_end_to_end_workflow(self):
        """Test complete workflow from search to upload"""
        # This would test the complete integration
        # For now, we'll just verify the services can be instantiated
        
        with patch.dict(os.environ, {
            'YOUTUBE_API_KEY': 'test_key',
            'GOOGLE_CLIENT_ID': 'test_client_id',
            'GOOGLE_CLIENT_SECRET': 'test_client_secret'
        }):
            youtube_service = YouTubeAPIService()
            auth_service = YouTubeAuthService()
            upload_service = YouTubeUploadService()
            analytics_service = YouTubeAnalyticsService()
            neural_core = VUCYouTubeNeuralCore()
            
            assert youtube_service is not None
            assert auth_service is not None
            assert upload_service is not None
            assert analytics_service is not None
            assert neural_core is not None

# Performance tests
class TestPerformance:
    """Performance tests for YouTube services"""
    
    @pytest.mark.asyncio
    async def test_search_performance(self):
        """Test search performance"""
        youtube_service = YouTubeAPIService()
        
        start_time = datetime.utcnow()
        
        # Mock the actual API call
        with patch('aiohttp.ClientSession.get') as mock_get:
            mock_response = Mock()
            mock_response.status = 200
            mock_response.json = AsyncMock(return_value={'items': []})
            mock_get.return_value.__aenter__.return_value = mock_response
            
            await youtube_service.search_videos('test query')
        
        end_time = datetime.utcnow()
        duration = (end_time - start_time).total_seconds()
        
        # Should complete within 5 seconds (including mock)
        assert duration < 5.0

# Error handling tests
class TestErrorHandling:
    """Test error handling in YouTube services"""
    
    @pytest.mark.asyncio
    async def test_api_error_handling(self):
        """Test API error handling"""
        youtube_service = YouTubeAPIService()
        
        with patch('aiohttp.ClientSession.get') as mock_get:
            mock_response = Mock()
            mock_response.status = 403
            mock_get.return_value.__aenter__.return_value = mock_response
            
            videos = await youtube_service.search_videos('test query')
            
            assert videos == []  # Should return empty list on error
    
    @pytest.mark.asyncio
    async def test_network_error_handling(self):
        """Test network error handling"""
        youtube_service = YouTubeAPIService()
        
        with patch('aiohttp.ClientSession.get') as mock_get:
            mock_get.side_effect = Exception("Network error")
            
            videos = await youtube_service.search_videos('test query')
            
            assert videos == []  # Should return empty list on network error

if __name__ == "__main__":
    # Run tests
    pytest.main([__file__, "-v"])
