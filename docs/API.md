# VUC-2026 API Documentation

## Overview

VUC-2026 Ultimate Dev++ provides a comprehensive REST API for YouTube automation and content management. The API is built with FastAPI and follows RESTful principles.

## Base URL

```
Development: http://localhost:8000
Production: https://your-domain.com
```

## Authentication

### API Key Authentication

```http
Authorization: Bearer YOUR_API_KEY
```

### OAuth 2.0 (YouTube Integration)

```http
Authorization: Bearer YOUTUBE_OAUTH_TOKEN
```

## API Endpoints

### 🎯 Channels

#### Get All Channels
```http
GET /api/channels
```

**Response:**
```json
{
  "channels": [
    {
      "id": "channel_123",
      "name": "Tech Wizard Channel",
      "niche": "technology",
      "subscriber_count": 15000,
      "video_count": 245,
      "created_at": "2026-03-19T10:00:00Z"
    }
  ]
}
```

#### Create Channel
```http
POST /api/channels
```

**Request Body:**
```json
{
  "name": "New Tech Channel",
  "niche": "technology",
  "target_audience": "developers",
  "content_strategy": "tutorials",
  "youtube_api_key": "AIzaSy...",
  "oauth_token": "ya29..."
}
```

#### Get Channel Details
```http
GET /api/channels/{channel_id}
```

#### Update Channel
```http
PUT /api/channels/{channel_id}
```

#### Delete Channel
```http
DELETE /api/channels/{channel_id}
```

### 🎬 Videos

#### Get All Videos
```http
GET /api/videos
```

**Query Parameters:**
- `channel_id`: Filter by channel
- `status`: Filter by status (draft, rendering, uploaded, published)
- `limit`: Number of results (default: 50)
- `offset`: Pagination offset

#### Create Video
```http
POST /api/videos
```

**Request Body:**
```json
{
  "channel_id": "channel_123",
  "title": "10 Amazing Python Tricks",
  "description": "In this video, we'll explore...",
  "tags": ["python", "programming", "tutorial"],
  "script_id": "script_456",
  "thumbnail_url": "https://example.com/thumb.jpg",
  "scheduled_time": "2026-03-20T15:00:00Z"
}
```

#### Get Video Details
```http
GET /api/videos/{video_id}
```

#### Update Video
```http
PUT /api/videos/{video_id}
```

#### Delete Video
```http
DELETE /api/videos/{video_id}
```

#### Upload Video
```http
POST /api/videos/{video_id}/upload
```

**Request Body (multipart/form-data):**
- `video_file`: Video file (MP4, MOV)
- `thumbnail`: Thumbnail image (JPG, PNG)
- `title`: Video title
- `description`: Video description
- `tags`: Video tags (comma-separated)

### 🧠 Scripts

#### Generate Script
```http
POST /api/scripts/generate
```

**Request Body:**
```json
{
  "topic": "AI in Web Development",
  "niche": "technology",
  "target_audience": "developers",
  "tone": "educational",
  "duration_minutes": 10,
  "keywords": ["AI", "web development", "machine learning"],
  "script_style": "hormozi"
}
```

**Response:**
```json
{
  "script_id": "script_789",
  "title": "How AI is Revolutionizing Web Development",
  "content": "Hey everyone! Today we're diving deep into...",
  "estimated_duration": 9.5,
  "seo_score": 85,
  "viral_potential": 78,
  "confidence_score": 92
}
```

#### Get Script
```http
GET /api/scripts/{script_id}
```

#### Update Script
```http
PUT /api/scripts/{script_id}
```

#### Get Script History
```http
GET /api/scripts/{script_id}/history
```

### 🕵️ Competitor Analysis

#### Analyze Competitor
```http
POST /api/competitors/analyze
```

**Request Body:**
```json
{
  "channel_url": "https://youtube.com/c/competitor",
  "analysis_depth": "deep",
  "metrics": ["vph", "engagement", "content_gap", "thumbnail_performance"]
}
```

**Response:**
```json
{
  "competitor_id": "comp_123",
  "channel_info": {
    "name": "Competitor Channel",
    "subscribers": 50000,
    "video_count": 500
  },
  "analysis": {
    "vph_trends": [1200, 1500, 1800, 2100],
    "top_performing_videos": [
      {
        "title": "Best Video Ever",
        "views": 1000000,
        "vph": 2500,
        "engagement_rate": 0.08
      }
    ],
    "content_gaps": ["advanced topics", "case studies"],
    "thumbnail_patterns": ["bright_colors", "face_overlay"],
    "posting_schedule": ["Monday", "Wednesday", "Friday"],
    "average_video_duration": 12.5
  }
}
```

#### Get Competitor List
```http
GET /api/competitors
```

#### Update Competitor Analysis
```http
PUT /api/competitors/{competitor_id}
```

### 📊 Analytics

#### Get Channel Analytics
```http
GET /api/analytics/channel/{channel_id}
```

**Query Parameters:**
- `start_date`: Start date (ISO 8601)
- `end_date`: End date (ISO 8601)
- `metrics`: Comma-separated metrics list

**Response:**
```json
{
  "period": {
    "start": "2026-03-01T00:00:00Z",
    "end": "2026-03-19T23:59:59Z"
  },
  "metrics": {
    "views": 150000,
    "watch_time_minutes": 450000,
    "subscribers_gained": 2500,
    "revenue_usd": 1250.50,
    "engagement_rate": 0.065,
    "click_through_rate": 0.045
  },
  "top_videos": [
    {
      "video_id": "video_123",
      "title": "Most Popular Video",
      "views": 50000,
      "vph": 2100
    }
  ],
  "audience_demographics": {
    "age_groups": {"18-24": 0.25, "25-34": 0.35, "35-44": 0.20},
    "gender": {"male": 0.65, "female": 0.35},
    "top_countries": ["US", "UK", "CA", "AU"]
  }
}
```

#### Get Video Analytics
```http
GET /api/analytics/video/{video_id}
```

#### Get Performance Trends
```http
GET /api/analytics/trends
```

#### Get Revenue Report
```http
GET /api/analytics/revenue
```

### 🤖 AI Services

#### AI Content Optimization
```http
POST /api/ai/optimize-content
```

**Request Body:**
```json
{
  "content_type": "title",
  "content": "My Video Title",
  "target_audience": "developers",
  "niche": "technology",
  "optimization_goals": ["click_through_rate", "seo"]
}
```

**Response:**
```json
{
  "optimized_content": "10 JavaScript Tricks Every Developer Should Know",
  "improvement_score": 85,
  "reasoning": "More specific, includes numbers, targets developer curiosity",
  "alternatives": [
    "JavaScript Secrets Revealed",
    "Developer's JavaScript Toolkit"
  ]
}
```

#### AI Thumbnail Analysis
```http
POST /api/ai/analyze-thumbnail
```

**Request Body (multipart/form-data):**
- `thumbnail`: Thumbnail image file
- `target_audience`: Target audience
- `niche`: Content niche

#### AI Comment Generation
```http
POST /api/ai/generate-comments
```

**Request Body:**
```json
{
  "video_id": "video_123",
  "comment_count": 10,
  "persona_types": ["tech_wizard", "curious_student"],
  "engagement_goal": "spark_discussion"
}
```

### 🎨 Media Processing

#### Generate Audio
```http
POST /api/media/generate-audio
```

**Request Body:**
```json
{
  "script_text": "Welcome to my channel...",
  "voice_style": "professional_male",
  "ssml_enabled": true,
  "output_format": "mp3",
  "sample_rate": 44100
}
```

#### Generate Video
```http
POST /api/media/generate-video
```

**Request Body:**
```json
{
  "script_id": "script_123",
  "visual_style": "tech_modern",
  "background_music": "upbeat_tech",
  "caption_style": "hormozi",
  "resolution": "1080p",
  "fps": 30,
  "duration_minutes": 10
}
```

#### Get Render Status
```http
GET /api/media/render-status/{render_id}
```

**Response:**
```json
{
  "render_id": "render_456",
  "status": "rendering",
  "progress": 75,
  "estimated_completion": "2026-03-19T14:30:00Z",
  "current_stage": "Adding captions",
  "stages_completed": ["script_analysis", "audio_generation", "video_composition"],
  "stages_remaining": ["caption_rendering", "final_export"]
}
```

### 🛡️ Security & Privacy

#### Get Anonymity Level
```http
GET /api/security/anonymity-level
```

#### Rotate IP Address
```http
POST /api/security/rotate-ip
```

#### Get Proxy Status
```http
GET /api/security/proxy-status
```

### ⚙️ System

#### Get System Status
```http
GET /api/system/status
```

**Response:**
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "uptime_seconds": 86400,
  "services": {
    "api": "running",
    "redis": "running",
    "celery": "running",
    "database": "running"
  },
  "resources": {
    "cpu_usage": 45.2,
    "memory_usage": 67.8,
    "disk_usage": 23.1,
    "gpu_usage": 78.5
  },
  "active_tasks": {
    "rendering": 3,
    "uploading": 1,
    "analyzing": 2
  }
}
```

#### Get Health Check
```http
GET /api/health
```

#### Get Metrics
```http
GET /api/metrics
```

## Error Handling

### Standard Error Response

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid input parameters",
    "details": {
      "field": "title",
      "issue": "Title cannot be empty"
    },
    "timestamp": "2026-03-19T12:00:00Z",
    "request_id": "req_123456"
  }
}
```

### Common Error Codes

- `400 BAD_REQUEST`: Invalid request parameters
- `401 UNAUTHORIZED`: Authentication required
- `403 FORBIDDEN`: Insufficient permissions
- `404 NOT_FOUND`: Resource not found
- `429 RATE_LIMITED`: Too many requests
- `500 INTERNAL_ERROR`: Server error
- `503 SERVICE_UNAVAILABLE`: Service temporarily unavailable

## Rate Limiting

- **Standard API**: 1000 requests/hour
- **Premium API**: 10000 requests/hour
- **Enterprise API**: Unlimited

## SDKs & Libraries

### Python SDK
```python
from vuc2026 import VUCClient

client = VUCClient(api_key="your_api_key")
channels = client.channels.list()
video = client.videos.create(channel_id="123", title="My Video")
```

### JavaScript SDK
```javascript
import { VUCClient } from 'vuc2026-js';

const client = new VUCClient({ apiKey: 'your_api_key' });
const channels = await client.channels.list();
const video = await client.videos.create({ channelId: '123', title: 'My Video' });
```

## Webhooks

### Configure Webhook
```http
POST /api/webhooks
```

**Request Body:**
```json
{
  "url": "https://your-app.com/webhook",
  "events": ["video.uploaded", "video.published", "render.completed"],
  "secret": "webhook_secret"
}
```

### Webhook Events

- `video.uploaded`: Video successfully uploaded to YouTube
- `video.published`: Video published and made public
- `render.completed`: Video rendering completed
- `script.generated`: New script generated
- `analysis.completed`: Competitor analysis completed

## Support

- **Documentation**: https://docs.vuc2026.com
- **API Reference**: https://api.vuc2026.com/docs
- **Support Email**: support@vuc2026.com
- **Discord Community**: https://discord.gg/vuc2026

---

**VUC-2026 Ultimate Dev++ API Documentation**

*Last updated: March 19, 2026*
