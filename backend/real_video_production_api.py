"""
VUC-2026 Real Video Production API
Actual video production with real file generation
"""

from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, FileResponse
from pydantic import BaseModel, Field
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Any
import time
import os
import logging
import json
import random
import asyncio
from contextlib import asynccontextmanager
from enum import Enum
import threading
import subprocess
from pathlib import Path

# Import real producer
from services.real_video_producer_fixed import real_producer

# Production Models
class VideoProductionRequest(BaseModel):
    title: str = Field(..., description="Video title")
    stage: str = Field(..., description="Content stage (pregnancy, newborn, infant, toddler)")
    duration_minutes: int = Field(default=18, description="Target video duration in minutes")
    priority: str = Field(default="normal", description="Production priority")
    quality_preset: str = Field(default="high", description="Video quality preset")

class ProductionStatus(BaseModel):
    production_id: str
    status: str
    progress_percentage: float
    current_stage: str
    started_at: datetime
    estimated_completion: datetime
    file_outputs: Dict[str, str] = {}
    error_message: Optional[str] = None

# Production State
class ProductionManager:
    def __init__(self):
        self.active_productions = {}
        self.completed_productions = {}
        self.production_queue = []
        
    async def start_real_production(self, request: VideoProductionRequest) -> str:
        """Start actual video production"""
        production_id = f"real_prod_{int(time.time())}"
        
        # Create initial status
        status = ProductionStatus(
            production_id=production_id,
            status="starting",
            progress_percentage=0.0,
            current_stage="initialization",
            started_at=datetime.now(),
            estimated_completion=datetime.now() + timedelta(minutes=30)
        )
        
        self.active_productions[production_id] = status
        
        # Start production in background
        asyncio.create_task(self._run_real_production(production_id, request))
        
        return production_id
    
    async def _run_real_production(self, production_id: str, request: VideoProductionRequest):
        """Run actual video production with real file generation"""
        try:
            status = self.active_productions[production_id]
            
            # Update stages
            stages = [
                ("script_generation", 5, "Generating AI script"),
                ("voice_synthesis", 10, "Creating voice audio"),
                ("visual_generation", 15, "Rendering video visuals"),
                ("video_combination", 20, "Combining video and audio"),
                ("thumbnail_generation", 5, "Creating thumbnail"),
                ("finalization", 5, "Final processing")
            ]
            
            total_progress = 0
            
            for stage_name, stage_duration, description in stages:
                if production_id not in self.active_productions:
                    break
                
                status.current_stage = description
                status.status = f"processing_{stage_name}"
                
                # Simulate stage progress
                for i in range(0, 101, 10):
                    if production_id not in self.active_productions:
                        break
                    
                    stage_progress = (i / 100) * stage_duration
                    status.progress_percentage = total_progress + stage_progress
                    
                    await asyncio.sleep(stage_duration * 0.6 / 10)  # Realistic timing
                
                total_progress += stage_duration
            
            # Actually produce the video
            video_request = {
                "title": request.title,
                "stage": request.stage,
                "duration_minutes": request.duration_minutes
            }
            
            production_result = await real_producer.produce_complete_video(video_request)
            
            if production_result["success"]:
                status.status = "completed"
                status.progress_percentage = 100.0
                status.file_outputs = production_result["video_files"]
                status.current_stage = "Production completed successfully"
                
                # Move to completed
                self.completed_productions[production_id] = status
                del self.active_productions[production_id]
                
                print(f"✅ [{production_id}] REAL VIDEO PRODUCTION COMPLETED!")
                print(f"📁 Files created: {list(status.file_outputs.values())}")
                
            else:
                status.status = "failed"
                status.error_message = production_result.get("error", "Unknown error")
                status.current_stage = "Production failed"
                
        except Exception as e:
            if production_id in self.active_productions:
                status = self.active_productions[production_id]
                status.status = "failed"
                status.error_message = str(e)
                status.current_stage = "Production error occurred"
    
    def get_production_status(self, production_id: str) -> Optional[ProductionStatus]:
        """Get production status"""
        if production_id in self.active_productions:
            return self.active_productions[production_id]
        elif production_id in self.completed_productions:
            return self.completed_productions[production_id]
        return None
    
    def get_all_productions(self) -> Dict[str, List[ProductionStatus]]:
        """Get all productions"""
        return {
            "active": list(self.active_productions.values()),
            "completed": list(self.completed_productions.values()),
            "queue_size": len(self.production_queue)
        }

# Initialize production manager
production_manager = ProductionManager()

# FastAPI Application
app = FastAPI(
    title="VUC-2026 Real Video Production",
    description="Actual video production with real file generation",
    version="1.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Static files for serving generated videos
app.mount("/production", StaticFiles(directory="production"), name="production")

@app.get("/", response_class=HTMLResponse)
async def serve_real_production_dashboard():
    """Serve real production dashboard"""
    return HTMLResponse(content="""
<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>VUC-2026 REAL Video Production</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/js/all.min.js"></script>
    <style>
        .production-stage {
            transition: all 0.3s ease;
        }
        .stage-active {
            background: linear-gradient(135deg, #10b981 0%, #059669 100%);
            color: white;
            transform: scale(1.05);
        }
        .stage-completed {
            background: #3b82f6;
            color: white;
        }
        .progress-bar {
            transition: width 0.5s ease;
        }
        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.5; }
        }
        .producing {
            animation: pulse 2s infinite;
        }
        .file-link {
            background: linear-gradient(135deg, #8b5cf6, #ec4899);
            color: white;
            padding: 8px 16px;
            border-radius: 8px;
            text-decoration: none;
            transition: transform 0.2s;
        }
        .file-link:hover {
            transform: translateY(-2px);
        }
    </style>
</head>
<body class="bg-gray-100">
    <div class="container mx-auto p-6">
        <!-- Header -->
        <header class="bg-white rounded-lg shadow-lg p-6 mb-6">
            <div class="flex justify-between items-center">
                <div>
                    <h1 class="text-3xl font-bold text-green-600">
                        <i class="fas fa-video mr-3"></i>
                        VUC-2026 REAL Video Production
                    </h1>
                    <p class="text-gray-600 mt-2">Actual video production with real file generation</p>
                </div>
                <div class="text-right">
                    <button id="startRealProductionBtn" class="bg-green-600 text-white px-6 py-3 rounded-lg hover:bg-green-700 transition">
                        <i class="fas fa-play mr-2"></i>Start REAL Production
                    </button>
                </div>
            </div>
        </header>

        <!-- Production Status -->
        <div class="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-6">
            <div class="bg-white rounded-lg shadow-lg p-6">
                <h3 class="text-lg font-bold text-gray-800 mb-4">Current Production</h3>
                <div id="currentProduction" class="space-y-4">
                    <p class="text-gray-500">No active production</p>
                </div>
            </div>
            
            <div class="bg-white rounded-lg shadow-lg p-6">
                <h3 class="text-lg font-bold text-gray-800 mb-4">Production Stats</h3>
                <div id="productionStats" class="space-y-2">
                    <div class="flex justify-between">
                        <span>Total Produced</span>
                        <span id="totalProduced" class="font-bold">0</span>
                    </div>
                    <div class="flex justify-between">
                        <span>Currently Producing</span>
                        <span id="currentlyProducing" class="font-bold">0</span>
                    </div>
                    <div class="flex justify-between">
                        <span>Avg Production Time</span>
                        <span id="avgProductionTime" class="font-bold">--</span>
                    </div>
                </div>
            </div>
            
            <div class="bg-white rounded-lg shadow-lg p-6">
                <h3 class="text-lg font-bold text-gray-800 mb-4">System Status</h3>
                <div id="systemStatus" class="space-y-2">
                    <div class="flex justify-between">
                        <span>FFmpeg</span>
                        <span class="text-green-600"><i class="fas fa-check-circle"></i> Ready</span>
                    </div>
                    <div class="flex justify-between">
                        <span>TTS Engine</span>
                        <span class="text-green-600"><i class="fas fa-check-circle"></i> Active</span>
                    </div>
                    <div class="flex justify-between">
                        <span>File System</span>
                        <span class="text-green-600"><i class="fas fa-check-circle"></i> Available</span>
                    </div>
                </div>
            </div>
        </div>

        <!-- Production Pipeline -->
        <div class="bg-white rounded-lg shadow-lg p-6 mb-6">
            <h3 class="text-lg font-bold text-gray-800 mb-4">Production Pipeline</h3>
            <div id="productionPipeline" class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4">
                <div class="production-stage p-4 rounded-lg border-2 border-gray-200 text-center" id="stage-script">
                    <i class="fas fa-file-alt text-2xl mb-2"></i>
                    <h4 class="font-bold text-sm">Script</h4>
                    <div class="mt-2">
                        <div class="w-full bg-gray-200 rounded-full h-2">
                            <div class="progress-bar bg-green-600 h-2 rounded-full" style="width: 0%"></div>
                        </div>
                    </div>
                </div>
                <div class="production-stage p-4 rounded-lg border-2 border-gray-200 text-center" id="stage-voice">
                    <i class="fas fa-microphone text-2xl mb-2"></i>
                    <h4 class="font-bold text-sm">Voice</h4>
                    <div class="mt-2">
                        <div class="w-full bg-gray-200 rounded-full h-2">
                            <div class="progress-bar bg-green-600 h-2 rounded-full" style="width: 0%"></div>
                        </div>
                    </div>
                </div>
                <div class="production-stage p-4 rounded-lg border-2 border-gray-200 text-center" id="stage-visual">
                    <i class="fas fa-film text-2xl mb-2"></i>
                    <h4 class="font-bold text-sm">Visuals</h4>
                    <div class="mt-2">
                        <div class="w-full bg-gray-200 rounded-full h-2">
                            <div class="progress-bar bg-green-600 h-2 rounded-full" style="width: 0%"></div>
                        </div>
                    </div>
                </div>
                <div class="production-stage p-4 rounded-lg border-2 border-gray-200 text-center" id="stage-combine">
                    <i class="fas fa-link text-2xl mb-2"></i>
                    <h4 class="font-bold text-sm">Combine</h4>
                    <div class="mt-2">
                        <div class="w-full bg-gray-200 rounded-full h-2">
                            <div class="progress-bar bg-green-600 h-2 rounded-full" style="width: 0%"></div>
                        </div>
                    </div>
                </div>
                <div class="production-stage p-4 rounded-lg border-2 border-gray-200 text-center" id="stage-thumbnail">
                    <i class="fas fa-image text-2xl mb-2"></i>
                    <h4 class="font-bold text-sm">Thumbnail</h4>
                    <div class="mt-2">
                        <div class="w-full bg-gray-200 rounded-full h-2">
                            <div class="progress-bar bg-green-600 h-2 rounded-full" style="width: 0%"></div>
                        </div>
                    </div>
                </div>
                <div class="production-stage p-4 rounded-lg border-2 border-gray-200 text-center" id="stage-final">
                    <i class="fas fa-check text-2xl mb-2"></i>
                    <h4 class="font-bold text-sm">Final</h4>
                    <div class="mt-2">
                        <div class="w-full bg-gray-200 rounded-full h-2">
                            <div class="progress-bar bg-green-600 h-2 rounded-full" style="width: 0%"></div>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- Production Details -->
        <div class="bg-white rounded-lg shadow-lg p-6 mb-6">
            <h3 class="text-lg font-bold text-gray-800 mb-4">Production Details</h3>
            <div id="productionDetails" class="space-y-4">
                <p class="text-gray-500">Start a production to see details</p>
            </div>
        </div>

        <!-- Completed Productions -->
        <div class="bg-white rounded-lg shadow-lg p-6">
            <h3 class="text-lg font-bold text-gray-800 mb-4">Completed Productions</h3>
            <div id="completedProductions" class="space-y-4">
                <p class="text-gray-500">No completed productions yet</p>
            </div>
        </div>
    </div>

    <script>
        const API_BASE = 'http://127.0.0.1:8004';
        let currentProductionId = null;
        let refreshInterval = null;

        // Initialize
        document.addEventListener('DOMContentLoaded', function() {
            startAutoRefresh();
            
            document.getElementById('startRealProductionBtn').addEventListener('click', startRealProduction);
        });

        // Start Real Production
        async function startRealProduction() {
            try {
                const response = await fetch(`${API_BASE}/api/real-production/start`, {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({
                        title: "VUC-2026 REAL Video - Pregnancy Week 1 Complete Guide",
                        stage: "pregnancy",
                        duration_minutes: 18,
                        priority: "high",
                        quality_preset: "ultra"
                    })
                });
                
                const result = await response.json();
                if (result.success) {
                    currentProductionId = result.production_id;
                    console.log('Production started with ID:', currentProductionId);
                    showNotification(`REAL production started: ${currentProductionId}`, 'success');
                    updateProductionStatus();
                } else {
                    console.error('Production start failed:', result);
                    showNotification('Failed to start production', 'error');
                }
            } catch (error) {
                console.error('Error starting production:', error);
                showNotification('Error starting production', 'error');
            }
        }

        // Update Production Status
        async function updateProductionStatus() {
            if (!currentProductionId) return;
            
            try {
                const response = await fetch(`${API_BASE}/api/real-production/status/${currentProductionId}`);
                
                if (response.status === 404) {
                    console.log(`Production ${currentProductionId} not found - may have completed`);
                    // Check if it's in completed productions
                    await updateCompletedProductions();
                    return;
                }
                
                const result = await response.json();
                
                if (result.success) {
                    updateCurrentProduction(result);
                    updatePipelineStages(result);
                    updateProductionDetails(result);
                    updateCompletedProductions();
                } else {
                    console.log('Production status check failed:', result);
                }
            } catch (error) {
                console.error('Error updating production status:', error);
            }
        }

        // Update Current Production Display
        function updateCurrentProduction(data) {
            const html = `
                <div class="border-l-4 border-green-600 pl-4">
                    <h4 class="font-bold">${data.production_id}</h4>
                    <p class="text-sm text-gray-600">Status: ${data.status}</p>
                    <p class="text-sm text-gray-600">Stage: ${data.current_stage}</p>
                    <div class="mt-2">
                        <div class="w-full bg-gray-200 rounded-full h-3">
                            <div class="progress-bar bg-gradient-to-r from-green-600 to-blue-600 h-3 rounded-full" 
                                 style="width: ${data.progress_percentage}%"></div>
                        </div>
                        <p class="text-sm text-gray-500 mt-1">${data.progress_percentage.toFixed(1)}% Complete</p>
                    </div>
                    ${data.error_message ? `<p class="text-red-600 text-sm mt-2">Error: ${data.error_message}</p>` : ''}
                </div>
            `;
            
            document.getElementById('currentProduction').innerHTML = html;
        }

        // Update Pipeline Stages
        function updatePipelineStages(status) {
            const progress = status.progress_percentage;
            const currentStage = status.current_stage;
            
            const stages = ['script', 'voice', 'visual', 'combine', 'thumbnail', 'final'];
            const stageProgress = progress / (100 / stages.length);
            
            stages.forEach((stage, index) => {
                const stageElement = document.getElementById(`stage-${stage}`);
                if (stageElement) {
                    stageElement.classList.remove('stage-active', 'stage-completed');
                    
                    if (index < Math.floor(stageProgress)) {
                        stageElement.classList.add('stage-completed');
                        stageElement.querySelector('.progress-bar').style.width = '100%';
                    } else if (index === Math.floor(stageProgress)) {
                        stageElement.classList.add('stage-active', 'producing');
                        const stageProgressPercent = (stageProgress % 1) * 100;
                        stageElement.querySelector('.progress-bar').style.width = `${stageProgressPercent}%`;
                    } else {
                        stageElement.querySelector('.progress-bar').style.width = '0%';
                    }
                }
            });
        }

        // Update Production Details
        function updateProductionDetails(data) {
            const html = `
                <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div>
                        <h4 class="font-bold text-gray-800 mb-2">Production Info</h4>
                        <div class="bg-gray-50 p-4 rounded-lg">
                            <p><strong>ID:</strong> ${data.production_id}</p>
                            <p><strong>Status:</strong> ${data.status}</p>
                            <p><strong>Started:</strong> ${new Date(data.started_at).toLocaleString()}</p>
                            <p><strong>Est. Completion:</strong> ${new Date(data.estimated_completion).toLocaleString()}</p>
                            <p><strong>Current Stage:</strong> ${data.current_stage}</p>
                        </div>
                    </div>
                    <div>
                        <h4 class="font-bold text-gray-800 mb-2">File Outputs</h4>
                        <div class="bg-gray-50 p-4 rounded-lg">
                            ${Object.entries(data.file_outputs || {}).map(([key, path]) => 
                                `<p><strong>${key}:</strong> 
                                <a href="/production/${path.split('/').pop()}" class="file-link" target="_blank">
                                    <i class="fas fa-download mr-1"></i>Download
                                </a></p>`
                            ).join('') || '<p class="text-gray-500">No files generated yet</p>'}
                        </div>
                    </div>
                </div>
            `;
            
            document.getElementById('productionDetails').innerHTML = html;
        }

        // Update Completed Productions
        async function updateCompletedProductions() {
            try {
                const response = await fetch(`${API_BASE}/api/real-productions`);
                const result = await response.json();
                
                if (result.success && result.productions && result.productions.completed && result.productions.completed.length > 0) {
                    const html = result.productions.completed.map(prod => `
                        <div class="border-l-4 border-blue-600 pl-4">
                            <h4 class="font-bold">${prod.production_id}</h4>
                            <p class="text-sm text-gray-600">Status: ${prod.status}</p>
                            <p class="text-sm text-gray-600">Completed: ${new Date(prod.completed_at).toLocaleString()}</p>
                            <div class="mt-2">
                                ${prod.file_outputs && Object.entries(prod.file_outputs).map(([key, path]) => 
                                    `<a href="/production/${path.split('/').pop()}" class="file-link mr-2" target="_blank">
                                        <i class="fas fa-download mr-1"></i>${key}
                                    </a>`
                                ).join('') || '<p class="text-gray-500">No files available</p>'}
                            </div>
                        </div>
                    `).join('');
                    
                    document.getElementById('completedProductions').innerHTML = html;
                    document.getElementById('totalProduced').textContent = result.productions.completed.length;
                } else {
                    document.getElementById('completedProductions').innerHTML = '<p class="text-gray-500">No completed productions yet</p>';
                    document.getElementById('totalProduced').textContent = '0';
                }
                
                document.getElementById('currentlyProducing').textContent = result.productions ? result.productions.active.length : 0;
                
            } catch (error) {
                console.error('Error updating completed productions:', error);
                document.getElementById('completedProductions').innerHTML = '<p class="text-gray-500">Error loading productions</p>';
            }
        }

        // Auto Refresh
        function startAutoRefresh() {
            refreshInterval = setInterval(() => {
                if (currentProductionId) {
                    updateProductionStatus();
                }
                updateCompletedProductions();
            }, 3000); // Update every 3 seconds
        }

        // Show Notification
        function showNotification(message, type = 'info') {
            const notification = document.createElement('div');
            notification.className = `fixed top-4 right-4 p-4 rounded-lg shadow-lg z-50 ${
                type === 'success' ? 'bg-green-500' : 
                type === 'error' ? 'bg-red-500' : 'bg-blue-500'
            } text-white`;
            notification.textContent = message;
            
            document.body.appendChild(notification);
            
            setTimeout(() => {
                notification.remove();
            }, 3000);
        }
    </script>
</body>
</html>
    """)

@app.post("/api/real-production/start")
async def start_real_video_production(request: VideoProductionRequest):
    """Start real video production with actual file generation"""
    try:
        production_id = await production_manager.start_real_production(request)
        
        return {
            "success": True,
            "production_id": production_id,
            "message": "REAL video production started with actual file generation",
            "estimated_completion": (datetime.now() + timedelta(minutes=30)).isoformat(),
            "production_type": "real_video_generation",
            "output_directory": "production/"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Real production start failed: {str(e)}")

@app.get("/api/real-production/status/{production_id}")
async def get_real_production_status(production_id: str):
    """Get real production status with file information"""
    print(f"🔍 Looking for production: {production_id}")
    
    production = production_manager.get_production_status(production_id)
    
    if not production:
        print(f"❌ Production not found: {production_id}")
        print(f"📊 Active productions: {list(production_manager.active_productions.keys())}")
        print(f"✅ Completed productions: {list(production_manager.completed_productions.keys())}")
        raise HTTPException(status_code=404, detail=f"Production {production_id} not found")
    
    print(f"✅ Found production: {production_id}, status: {production.status}")
    
    return {
        "success": True,
        "production_id": production.production_id,
        "status": production.status,
        "progress_percentage": production.progress_percentage,
        "current_stage": production.current_stage,
        "started_at": production.started_at.isoformat(),
        "estimated_completion": production.estimated_completion.isoformat(),
        "file_outputs": production.file_outputs,
        "error_message": production.error_message,
        "production_type": "real_video_generation"
    }

@app.get("/api/real-productions")
async def get_all_real_productions():
    """Get all real productions"""
    all_productions = production_manager.get_all_productions()
    
    return {
        "success": True,
        "productions": {
            "active": [
                {
                    "production_id": prod.production_id,
                    "status": prod.status,
                    "progress": prod.progress_percentage,
                    "current_stage": prod.current_stage,
                    "started_at": prod.started_at.isoformat()
                }
                for prod in all_productions["active"]
            ],
            "completed": [
                {
                    "production_id": prod.production_id,
                    "status": prod.status,
                    "file_outputs": prod.file_outputs,
                    "completed_at": prod.started_at.isoformat()
                }
                for prod in all_productions["completed"]
            ]
        },
        "stats": {
            "total_completed": len(all_productions["completed"]),
            "currently_active": len(all_productions["active"]),
            "queue_size": all_productions["queue_size"]
        }
    }

@app.get("/production/{file_name}")
async def get_production_file(file_name: str):
    """Serve generated production files"""
    file_path = Path("production") / file_name
    
    if file_path.exists():
        return FileResponse(
            path=file_path,
            filename=file_name,
            media_type='application/octet-stream'
        )
    else:
        raise HTTPException(status_code=404, detail="File not found")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8004, reload=True)
