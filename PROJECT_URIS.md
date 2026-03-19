# VUC-2026 Project URI Structure

## 🌐 Application URLs

### Development Environment
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

### Production Environment (Docker)
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Database**: postgres:5432 (internal)
- **Redis**: redis:6379 (internal)

## 🛠️ API Endpoints Structure

### Core API Routes
```
http://localhost:8000/
├── / (Root - API Info)
├── /health (System Health)
├── /docs (Swagger Documentation)
├── /redoc (ReDoc Documentation)
└── /api/
    ├── /channels/ (Channel Management)
    ├── /channel-management/ (Advanced Channel Ops)
    ├── /videos/ (Video Management)
    ├── /scripts/ (AI Script Generation)
    ├── /analytics/ (Performance Analytics)
    ├── /settings/ (System Settings)
    └── /system-health/ (Health Monitoring)
```

### Frontend Routes
```
http://localhost:3000/
├── / (Dashboard/Home)
├── /war-room/ (Command Center)
├── /omniverse/ (Multi-Platform)
├── /empire/ (Neural Architecture)
├── /cofounder/ (AI Advisor)
├── /channels/ (Channel Management)
├── /memory/ (Analytics Vault)
├── /windows-ai/ (Local AI Services)
├── /management/ (Operations)
└── /onboarding/ (Setup Guide)
```

## 📁 File System Structure

### Backend Paths
```
c:\Users\onurk\youtube\CascadeProjects\2048\
├── backend/
│   ├── app/
│   │   ├── main.py (Application Entry)
│   │   ├── database.py (Database Config)
│   │   ├── api/ (API Routes)
│   │   ├── models/ (Database Models)
│   │   ├── services/ (Business Logic)
│   │   └── agents/ (AI Agents)
│   ├── requirements.txt (Dependencies)
│   └── venv/ (Python Virtual Environment)
├── frontend/
│   ├── src/
│   │   ├── app/ (Next.js Pages)
│   │   ├── components/ (React Components)
│   │   └── lib/ (Utilities)
│   ├── package.json (Dependencies)
│   └── next.config.js (Next.js Config)
├── .env (Environment Variables)
├── docker-compose.yml (Docker Services)
└── README.md (Project Documentation)
```

### Database Paths
```
Database: sqlite:///./database/vuc2026.db (Development)
PostgreSQL: postgresql+asyncpg://vuc2026_user:pass@localhost:5432/vuc2026 (Production)
```

### Redis Paths
```
Development: redis://:redis_pass@localhost:6379/0
Production: redis://:redis_pass@redis:6379/0 (Docker)
```

## 🐳 Docker Service URIs

### Container Network
```
postgres:5432 (Database)
redis:6379 (Cache/Queue)
backend:8000 (API Service)
frontend:3000 (Web App)
celery_worker: (Background Tasks)
celery_beat: (Task Scheduler)
```

### Volume Mounts
```
./backend/logs:/app/logs (Application Logs)
./backend/static:/app/static (Static Files)
./backend/temp:/app/temp (Temporary Files)
./vuc_memory:/app/vuc_memory (AI Memory)
postgres_data:/var/lib/postgresql/data (Database Data)
redis_data:/data (Redis Data)
```

## 🔧 Development Workflow URLs

### Local Development
1. **Backend**: `cd backend && .\venv\Scripts\activate && python -m uvicorn app.main:app --reload`
2. **Frontend**: `cd frontend && npm run dev`
3. **Database**: SQLite (auto-created)
4. **Redis**: Optional (install separately)

### Docker Development
1. **Full Stack**: `docker-compose up`
2. **Database Only**: `docker-compose up postgres redis`
3. **Backend Only**: `docker-compose up backend postgres redis`
4. **Frontend Only**: `docker-compose up frontend backend`

## 🌍 External Service URIs

### Google APIs
```
Google AI API: https://generativelanguage.googleapis.com/
YouTube Data API: https://www.googleapis.com/youtube/v3/
```

### Stock Media APIs
```
Pexels API: https://api.pexels.com/
Pixabay API: https://pixabay.com/api/
```

## 📊 Monitoring & Analytics

### Health Endpoints
```
/system/health (Overall Health)
/api/system-health/ (Detailed Health)
/health (Basic Health Check)
```

### Analytics Endpoints
```
/api/analytics/performance (Performance Metrics)
/api/analytics/channels (Channel Analytics)
/api/analytics/videos (Video Analytics)
```

This URI structure provides a complete mapping of all VUC-2026 system endpoints, routes, and service locations for both development and production environments.
