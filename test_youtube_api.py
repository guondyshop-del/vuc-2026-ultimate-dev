#!/usr/bin/env python3
"""
VUC-2026 YouTube API Key Test Script
Tests the YouTube Data API integration with the provided API key
"""

import asyncio
import sys
import os

# Add the backend path to sys.path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from app.services.youtube_api_service import YouTubeAPIService

async def test_youtube_api_key():
    """Comprehensive test of YouTube API functionality"""
    
    print("🚀 VUC-2026 YouTube API Key Test")
    print("=" * 50)
    
    # Initialize service
    service = YouTubeAPIService()
    
    if not service.api_key:
        print("❌ YouTube API key not found!")
        return False
    
    print(f"✅ API Key loaded: {service.api_key[:20]}...")
    print(f"📊 Project ID: {service.project_id}")
    
    # Test 1: Search videos
    print("\n🔍 Testing video search...")
    try:
        videos = await service.search_videos("python programming", max_results=5)
        if videos:
            print(f"✅ Found {len(videos)} videos")
            for i, video in enumerate(videos[:3], 1):
                print(f"   {i}. {video.title[:50]}...")
        else:
            print("❌ No videos found")
            return False
    except Exception as e:
        print(f"❌ Search error: {str(e)}")
        return False
    
    # Test 2: Get video details
    print("\n📹 Testing video details...")
    try:
        if videos:
            video_details = await service.get_video_details([videos[0].video_id])
            if video_details:
                print(f"✅ Video details retrieved: {video_details[0].title[:50]}...")
            else:
                print("❌ Failed to get video details")
                return False
    except Exception as e:
        print(f"❌ Video details error: {str(e)}")
        return False
    
    # Test 3: Get trending videos
    print("\n🔥 Testing trending videos...")
    try:
        trending = await service.get_trending_videos(region_code="US", max_results=3)
        if trending:
            print(f"✅ Found {len(trending)} trending videos")
            for i, video in enumerate(trending[:2], 1):
                print(f"   {i}. {video.title[:50]}...")
        else:
            print("⚠️ No trending videos found (might be normal)")
    except Exception as e:
        print(f"⚠️ Trending videos error: {str(e)}")
    
    # Test 4: Get categories
    print("\n📂 Testing video categories...")
    try:
        categories = await service.get_video_categories(region_code="US")
        if categories:
            print(f"✅ Found {len(categories)} video categories")
        else:
            print("⚠️ No categories found")
    except Exception as e:
        print(f"⚠️ Categories error: {str(e)}")
    
    print("\n🎉 YouTube API Key Test Complete!")
    print("✅ API key is working correctly")
    return True

if __name__ == "__main__":
    success = asyncio.run(test_youtube_api_key())
    if success:
        print("\n🚀 VUC-2026 YouTube API integration is ready!")
    else:
        print("\n❌ YouTube API integration needs attention")
        sys.exit(1)
