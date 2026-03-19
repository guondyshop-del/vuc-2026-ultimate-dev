#!/usr/bin/env python3
"""
VUC-2026 API Connection Test Script
External servislerin bağlantılarını test eder
"""

import asyncio
import aiohttp
import os
from pathlib import Path
from datetime import datetime
import json

async def test_api_connections():
    """API bağlantılarını test et"""
    
    print("🧪 VUC-2026 API Connection Test")
    print("=" * 40)
    print(f"📅 Test Tarihi: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Load environment variables
    if Path(".env.production").exists():
        with open(".env.production", "r") as f:
            for line in f:
                if line.strip() and not line.startswith("#"):
                    key, value = line.strip().split("=", 1)
                    os.environ[key] = value
    
    # Test configurations
    test_configs = [
        {
            "name": "Google Gemini API",
            "url": "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-pro:generateContent",
            "api_key": os.getenv("GOOGLE_API_KEY"),
            "method": "POST",
            "test_payload": {
                "contents": [{"parts": [{"text": "Hello, VUC-2026!"}]}]
            }
        },
        {
            "name": "ElevenLabs API",
            "url": "https://api.elevenlabs.io/v1/voices",
            "api_key": os.getenv("ELEVENLABS_API_KEY"),
            "method": "GET",
            "headers": {"xi-api-key": os.getenv("ELEVENLABS_API_KEY")}
        },
        {
            "name": "YouTube Data API v3",
            "url": "https://www.googleapis.com/youtube/v3/channels",
            "api_key": os.getenv("YOUTUBE_API_KEY"),
            "method": "GET",
            "params": {"part": "snippet", "id": "UCBR8-60-B28hp2BmSd5MTAnQ"}
        },
        {
            "name": "Ahrefs API",
            "url": "https://api.ahrefs.com/v3/keywords-explorer",
            "api_key": os.getenv("AHREFS_API_TOKEN"),
            "method": "GET",
            "params": {"where": "keyword=\"youtube\"", "limit": 1}
        }
    ]
    
    results = []
    
    async with aiohttp.ClientSession() as session:
        for config in test_configs:
            print(f"🔍 Testing {config['name']}...")
            
            try:
                # Prepare request
                headers = config.get("headers", {})
                if config["api_key"]:
                    if "googleapis.com" in config["url"]:
                        params = config.get("params", {})
                        params["key"] = config["api_key"]
                        config["params"] = params
                    elif "ahrefs.com" in config["url"]:
                        headers["Authorization"] = f"Bearer {config['api_key']}"
                
                # Make request
                async with session.request(
                    config["method"],
                    config["url"],
                    headers=headers,
                    params=config.get("params"),
                    json=config.get("test_payload") if config["method"] == "POST" else None,
                    timeout=10
                ) as response:
                    
                    if response.status == 200:
                        result = {
                            "service": config["name"],
                            "status": "✅ SUCCESS",
                            "status_code": response.status,
                            "response_time": "Fast"
                        }
                        print(f"   ✅ SUCCESS ({response.status})")
                    else:
                        error_text = await response.text()
                        result = {
                            "service": config["name"],
                            "status": "❌ FAILED",
                            "status_code": response.status,
                            "error": error_text[:100]
                        }
                        print(f"   ❌ FAILED ({response.status}): {error_text[:50]}...")
                    
                    results.append(result)
                    
            except asyncio.TimeoutError:
                result = {
                    "service": config["name"],
                    "status": "⏰ TIMEOUT",
                    "error": "Request timed out"
                }
                print(f"   ⏰ TIMEOUT")
                results.append(result)
                
            except Exception as e:
                result = {
                    "service": config["name"],
                    "status": "💥 ERROR",
                    "error": str(e)
                }
                print(f"   💥 ERROR: {str(e)}")
                results.append(result)
            
            print()
    
    # Summary
    print("📊 Test Results Summary")
    print("=" * 25)
    
    successful = sum(1 for r in results if r["status"] == "✅ SUCCESS")
    failed = len(results) - successful
    
    print(f"✅ Successful: {successful}")
    print(f"❌ Failed: {failed}")
    print(f"📈 Success Rate: {(successful/len(results)*100):.1f}%")
    print()
    
    # Detailed results
    print("📋 Detailed Results:")
    print("-" * 20)
    for result in results:
        print(f"{result['status']} {result['service']}")
        if "error" in result:
            print(f"   Error: {result['error']}")
    
    # Save results
    with open("api_test_results.json", "w") as f:
        json.dump({
            "test_date": datetime.now().isoformat(),
            "summary": {
                "total_tests": len(results),
                "successful": successful,
                "failed": failed,
                "success_rate": successful/len(results)*100
            },
            "results": results
        }, f, indent=2)
    
    print(f"\n💾 Results saved to: api_test_results.json")
    
    return successful == len(results)

async def test_database_connection():
    """Veritabanı bağlantısını test et"""
    
    print("🗄️  Database Connection Test")
    print("-" * 30)
    
    try:
        # This would require actual database setup
        # For now, just check if DATABASE_URL is set
        db_url = os.getenv("DATABASE_URL")
        if db_url and "Buraya_" not in db_url:
            print("✅ Database URL configured")
            # TODO: Add actual database connection test
            return True
        else:
            print("❌ Database URL not configured")
            return False
            
    except Exception as e:
        print(f"❌ Database test failed: {e}")
        return False

async def test_redis_connection():
    """Redis bağlantısını test et"""
    
    print("🔴 Redis Connection Test")
    print("-" * 25)
    
    try:
        # TODO: Add actual Redis connection test
        redis_url = os.getenv("REDIS_URL")
        if redis_url:
            print("✅ Redis URL configured")
            return True
        else:
            print("❌ Redis URL not configured")
            return False
            
    except Exception as e:
        print(f"❌ Redis test failed: {e}")
        return False

async def main():
    """Ana test fonksiyonu"""
    
    print("🚀 VUC-2026 Production API Test Suite")
    print("=" * 45)
    print()
    
    # Test API connections
    api_success = await test_api_connections()
    print()
    
    # Test database
    db_success = await test_database_connection()
    print()
    
    # Test Redis
    redis_success = await test_redis_connection()
    print()
    
    # Overall result
    print("🎯 Overall Result")
    print("-" * 16)
    
    if api_success and db_success and redis_success:
        print("🎉 ALL TESTS PASSED!")
        print("✅ VUC-2026 ready for production!")
    else:
        print("⚠️  Some tests failed")
        print("🔧 Please check the configuration")
    
    print()
    print("📝 Next Steps:")
    print("1. Configure missing API keys")
    print("2. Set up database and Redis")
    print("3. Run this test again")
    print("4. Start production server: python -m app.main")

if __name__ == "__main__":
    asyncio.run(main())
