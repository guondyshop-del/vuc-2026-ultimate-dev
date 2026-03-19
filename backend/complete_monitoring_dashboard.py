"""
VUC-2026 Complete System Monitoring Dashboard
Real-time monitoring for all production, healing, and AI systems
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Any
import json
import asyncio
import logging
import aiohttp
import time

app = FastAPI(
    title="VUC-2026 Complete Monitoring Dashboard",
    description="Comprehensive system monitoring for all VUC-2026 components",
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

# System Configuration
SYSTEM_ENDPOINTS = {
    "main_api": "http://127.0.0.1:8002",
    "production": "http://127.0.0.1:8003",
    "self_healing": "http://127.0.0.1:8004"  # Will create this
}

class SystemStatus(BaseModel):
    name: str
    status: str
    response_time: float
    last_check: datetime
    uptime_percentage: float
    error_rate: float
    details: Dict[str, Any] = {}

class AlertLevel(str):
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"

class SystemAlert(BaseModel):
    id: str
    level: AlertLevel
    title: str
    message: str
    component: str
    timestamp: datetime
    resolved: bool = False

class MonitoringDashboard:
    def __init__(self):
        self.systems_status = {}
        self.alerts = []
        self.performance_history = []
        self.logger = logging.getLogger("vuc_monitoring")
        
    async def check_all_systems(self) -> Dict[str, SystemStatus]:
        """Check health of all system components"""
        results = {}
        
        for system_name, base_url in SYSTEM_ENDPOINTS.items():
            try:
                start_time = time.time()
                
                # Check main health endpoint
                async with aiohttp.ClientSession() as session:
                    async with session.get(f"{base_url}/health", timeout=aiohttp.ClientTimeout(total=5)) as response:
                        if response.status == 200:
                            health_data = await response.json()
                            response_time = (time.time() - start_time) * 1000
                            
                            results[system_name] = SystemStatus(
                                name=system_name,
                                status="healthy",
                                response_time=response_time,
                                last_check=datetime.now(),
                                uptime_percentage=health_data.get("uptime_percentage", 99.5),
                                error_rate=health_data.get("error_rate", 0.1),
                                details=health_data
                            )
                        else:
                            raise Exception(f"HTTP {response.status}")
                            
            except Exception as e:
                results[system_name] = SystemStatus(
                    name=system_name,
                    status="error",
                    response_time=5000.0,
                    last_check=datetime.now(),
                    uptime_percentage=0.0,
                    error_rate=100.0,
                    details={"error": str(e)}
                )
                
                # Create alert
                await self.create_alert(
                    AlertLevel.ERROR,
                    f"System {system_name} Down",
                    f"Failed to connect to {system_name}: {str(e)}",
                    system_name
                )
        
        self.systems_status = results
        return results
    
    async def create_alert(self, level: AlertLevel, title: str, message: str, component: str):
        """Create a system alert"""
        alert = SystemAlert(
            id=f"alert_{int(time.time())}_{len(self.alerts)}",
            level=level,
            title=title,
            message=message,
            component=component,
            timestamp=datetime.now()
        )
        
        self.alerts.append(alert)
        
        # Keep only last 100 alerts
        if len(self.alerts) > 100:
            self.alerts = self.alerts[-100:]
    
    async def get_production_status(self) -> Dict[str, Any]:
        """Get production system status"""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(f"{SYSTEM_ENDPOINTS['production']}/api/production/dashboard", timeout=10) as response:
                    if response.status == 200:
                        return await response.json()
        except Exception as e:
            self.logger.error(f"Failed to get production status: {e}")
            return {"error": str(e)}
    
    async def get_empire_status(self) -> Dict[str, Any]:
        """Get family & kids empire status"""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(f"{SYSTEM_ENDPOINTS['main_api']}/api/family-kids-empire/status", timeout=10) as response:
                    if response.status == 200:
                        return await response.json()
        except Exception as e:
            self.logger.error(f"Failed to get empire status: {e}")
            return {"error": str(e)}
    
    async def get_self_healing_status(self) -> Dict[str, Any]:
        """Get self-healing system status"""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(f"{SYSTEM_ENDPOINTS['self_healing']}/api/self-healing/health", timeout=10) as response:
                    if response.status == 200:
                        return await response.json()
        except Exception as e:
            self.logger.error(f"Failed to get self-healing status: {e}")
            return {"error": str(e)}

# Initialize dashboard
monitoring_dashboard = MonitoringDashboard()

# API Endpoints
@app.get("/api/dashboard/overview")
async def get_dashboard_overview():
    """Get complete dashboard overview"""
    try:
        # Get all system statuses
        system_statuses = await monitoring_dashboard.check_all_systems()
        
        # Get detailed statuses
        production_status = await monitoring_dashboard.get_production_status()
        empire_status = await monitoring_dashboard.get_empire_status()
        healing_status = await monitoring_dashboard.get_self_healing_status()
        
        # Calculate overall health
        healthy_systems = len([s for s in system_statuses.values() if s.status == "healthy"])
        total_systems = len(system_statuses)
        overall_health = (healthy_systems / total_systems) * 100 if total_systems > 0 else 0
        
        return {
            "success": True,
            "timestamp": datetime.now().isoformat(),
            "overall_health": overall_health,
            "systems": {
                name: {
                    "status": status.status,
                    "response_time": status.response_time,
                    "uptime": status.uptime_percentage,
                    "error_rate": status.error_rate,
                    "last_check": status.last_check.isoformat()
                }
                for name, status in system_statuses.items()
            },
            "production": production_status,
            "empire": empire_status,
            "healing": healing_status,
            "alerts": [
                {
                    "id": alert.id,
                    "level": alert.level.value,
                    "title": alert.title,
                    "message": alert.message,
                    "component": alert.component,
                    "timestamp": alert.timestamp.isoformat(),
                    "resolved": alert.resolved
                }
                for alert in monitoring_dashboard.alerts[-20:]  # Last 20 alerts
            ]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get dashboard overview: {str(e)}")

@app.get("/api/dashboard/systems")
async def get_systems_status():
    """Get detailed system status"""
    try:
        system_statuses = await monitoring_dashboard.check_all_systems()
        
        return {
            "success": True,
            "systems": [
                {
                    "name": status.name,
                    "status": status.status,
                    "response_time": status.response_time,
                    "uptime": status.uptime_percentage,
                    "error_rate": status.error_rate,
                    "last_check": status.last_check.isoformat(),
                    "details": status.details
                }
                for status in system_statuses.values()
            ],
            "total_systems": len(system_statuses),
            "healthy_systems": len([s for s in system_statuses.values() if s.status == "healthy"]),
            "degraded_systems": len([s for s in system_statuses.values() if s.status == "degraded"]),
            "failed_systems": len([s for s in system_statuses.values() if s.status == "error"])
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get systems status: {str(e)}")

@app.get("/api/dashboard/alerts")
async def get_alerts(level: Optional[str] = None, resolved: Optional[bool] = None):
    """Get system alerts with filtering"""
    try:
        alerts = monitoring_dashboard.alerts
        
        # Apply filters
        if level:
            alerts = [a for a in alerts if a.level.value == level]
        
        if resolved is not None:
            alerts = [a for a in alerts if a.resolved == resolved]
        
        # Sort by timestamp (newest first)
        alerts.sort(key=lambda x: x.timestamp, reverse=True)
        
        return {
            "success": True,
            "total_alerts": len(alerts),
            "alerts": [
                {
                    "id": alert.id,
                    "level": alert.level.value,
                    "title": alert.title,
                    "message": alert.message,
                    "component": alert.component,
                    "timestamp": alert.timestamp.isoformat(),
                    "resolved": alert.resolved
                }
                for alert in alerts
            ]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get alerts: {str(e)}")

@app.post("/api/dashboard/alerts/{alert_id}/resolve")
async def resolve_alert(alert_id: str):
    """Mark an alert as resolved"""
    try:
        for alert in monitoring_dashboard.alerts:
            if alert.id == alert_id:
                alert.resolved = True
                return {
                    "success": True,
                    "message": f"Alert {alert_id} marked as resolved"
                }
        
        raise HTTPException(status_code=404, detail="Alert not found")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to resolve alert: {str(e)}")

@app.get("/api/dashboard/production")
async def get_production_dashboard():
    """Get production system dashboard"""
    try:
        production_status = await monitoring_dashboard.get_production_status()
        production_queue = None
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(f"{SYSTEM_ENDPOINTS['production']}/api/production/queue", timeout=10) as response:
                    if response.status == 200:
                        production_queue = await response.json()
        except:
            pass
        
        return {
            "success": True,
            "production": production_status,
            "queue": production_queue
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get production dashboard: {str(e)}")

@app.get("/api/dashboard/healing")
async def get_healing_dashboard():
    """Get self-healing dashboard"""
    try:
        healing_status = await monitoring_dashboard.get_self_healing_status()
        
        # Get additional healing data
        healing_issues = None
        healing_history = None
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(f"{SYSTEM_ENDPOINTS['self_healing']}/api/self-healing/issues", timeout=10) as response:
                    if response.status == 200:
                        healing_issues = await response.json()
                        
                async with session.get(f"{SYSTEM_ENDPOINTS['self_healing']}/api/self-healing/healing/history", timeout=10) as response:
                    if response.status == 200:
                        healing_history = await response.json()
        except:
            pass
        
        return {
            "success": True,
            "healing": healing_status,
            "issues": healing_issues,
            "history": healing_history
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get healing dashboard: {str(e)}")

# Main Dashboard HTML
@app.get("/", response_class=HTMLResponse)
async def serve_dashboard():
    """Serve the main monitoring dashboard"""
    return HTMLResponse(content="""
<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>VUC-2026 Complete System Monitoring</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/js/all.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        .status-healthy { background: linear-gradient(135deg, #10b981, #059669); }
        .status-degraded { background: linear-gradient(135deg, #f59e0b, #d97706); }
        .status-error { background: linear-gradient(135deg, #ef4444, #dc2626); }
        .alert-info { background: #3b82f6; }
        .alert-warning { background: #f59e0b; }
        .alert-error { background: #ef4444; }
        .alert-critical { background: #dc2626; }
        .metric-card {
            transition: all 0.3s ease;
            border: 1px solid #e5e7eb;
        }
        .metric-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 25px rgba(0,0,0,0.1);
        }
        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.5; }
        }
        .updating {
            animation: pulse 2s infinite;
        }
    </style>
</head>
<body class="bg-gray-100">
    <div class="container mx-auto p-6">
        <!-- Header -->
        <header class="bg-white rounded-lg shadow-lg p-6 mb-6">
            <div class="flex justify-between items-center">
                <div>
                    <h1 class="text-3xl font-bold text-gray-800">
                        <i class="fas fa-dashboard mr-3 text-purple-600"></i>
                        VUC-2026 Complete System Monitoring
                    </h1>
                    <p class="text-gray-600 mt-2">Real-time monitoring for all production, healing, and AI systems</p>
                </div>
                <div class="flex space-x-4">
                    <div class="text-center">
                        <div id="overallHealth" class="text-3xl font-bold text-green-600">--%</div>
                        <div class="text-sm text-gray-600">Overall Health</div>
                    </div>
                    <div class="text-center">
                        <div id="totalSystems" class="text-3xl font-bold text-blue-600">--</div>
                        <div class="text-sm text-gray-600">Total Systems</div>
                    </div>
                    <div class="text-center">
                        <div id="activeAlerts" class="text-3xl font-bold text-red-600">--</div>
                        <div class="text-sm text-gray-600">Active Alerts</div>
                    </div>
                </div>
            </div>
        </header>

        <!-- System Status Grid -->
        <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-6">
            <div class="bg-white rounded-lg shadow-lg p-6">
                <h3 class="text-lg font-bold text-gray-800 mb-4">System Components</h3>
                <div id="systemStatus" class="space-y-3">
                    <!-- System status will be loaded here -->
                </div>
            </div>
            
            <div class="bg-white rounded-lg shadow-lg p-6">
                <h3 class="text-lg font-bold text-gray-800 mb-4">Production Status</h3>
                <div id="productionStatus" class="space-y-3">
                    <!-- Production status will be loaded here -->
                </div>
            </div>
            
            <div class="bg-white rounded-lg shadow-lg p-6">
                <h3 class="text-lg font-bold text-gray-800 mb-4">Recent Alerts</h3>
                <div id="recentAlerts" class="space-y-2">
                    <!-- Recent alerts will be loaded here -->
                </div>
            </div>
        </div>

        <!-- Detailed Metrics -->
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
            <div class="bg-white rounded-lg shadow-lg p-6">
                <h3 class="text-lg font-bold text-gray-800 mb-4">System Performance</h3>
                <canvas id="performanceChart" width="400" height="200"></canvas>
            </div>
            
            <div class="bg-white rounded-lg shadow-lg p-6">
                <h3 class="text-lg font-bold text-gray-800 mb-4">Production Pipeline</h3>
                <canvas id="productionChart" width="400" height="200"></canvas>
            </div>
        </div>

        <!-- Detailed Sections -->
        <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
            <div class="bg-white rounded-lg shadow-lg p-6">
                <h3 class="text-lg font-bold text-gray-800 mb-4">Production Queue</h3>
                <div id="productionQueue" class="space-y-2">
                    <!-- Production queue will be loaded here -->
                </div>
            </div>
            
            <div class="bg-white rounded-lg shadow-lg p-6">
                <h3 class="text-lg font-bold text-gray-800 mb-4">Self-Healing Status</h3>
                <div id="healingStatus" class="space-y-2">
                    <!-- Healing status will be loaded here -->
                </div>
            </div>
            
            <div class="bg-white rounded-lg shadow-lg p-6">
                <h3 class="text-lg font-bold text-gray-800 mb-4">AI Decisions</h3>
                <div id="aiDecisions" class="space-y-2">
                    <!-- AI decisions will be loaded here -->
                </div>
            </div>
        </div>
    </div>

    <script>
        const API_BASE = window.location.origin;
        let performanceChart = null;
        let productionChart = null;
        let performanceData = {
            labels: [],
            datasets: []
        };
        let productionData = {
            labels: [],
            datasets: []
        };

        // Initialize
        document.addEventListener('DOMContentLoaded', function() {
            initializeCharts();
            loadDashboard();
            setInterval(loadDashboard, 5000); // Update every 5 seconds
        });

        // Initialize Charts
        function initializeCharts() {
            const perfCtx = document.getElementById('performanceChart').getContext('2d');
            performanceChart = new Chart(perfCtx, {
                type: 'line',
                data: performanceData,
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: {
                        y: {
                            beginAtZero: true,
                            max: 100
                        }
                    },
                    plugins: {
                        legend: {
                            position: 'bottom'
                        }
                    }
                }
            });

            const prodCtx = document.getElementById('productionChart').getContext('2d');
            productionChart = new Chart(prodCtx, {
                type: 'bar',
                data: productionData,
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: {
                        y: {
                            beginAtZero: true
                        }
                    },
                    plugins: {
                        legend: {
                            position: 'bottom'
                        }
                    }
                }
            });
        }

        // Load Dashboard Data
        async function loadDashboard() {
            try {
                const response = await fetch(`${API_BASE}/api/dashboard/overview`);
                const data = await response.json();
                
                if (data.success) {
                    updateOverview(data);
                    updateSystemStatus(data.systems);
                    updateProductionStatus(data.production);
                    updateAlerts(data.alerts);
                    updateCharts(data);
                }
            } catch (error) {
                console.error('Error loading dashboard:', error);
            }
        }

        // Update Overview
        function updateOverview(data) {
            document.getElementById('overallHealth').textContent = `${data.overall_health.toFixed(1)}%`;
            document.getElementById('totalSystems').textContent = Object.keys(data.systems).length;
            document.getElementById('activeAlerts').textContent = data.alerts.filter(a => !a.resolved).length;
            
            // Update health color
            const healthElement = document.getElementById('overallHealth');
            if (data.overall_health >= 90) {
                healthElement.className = 'text-3xl font-bold text-green-600';
            } else if (data.overall_health >= 70) {
                healthElement.className = 'text-3xl font-bold text-yellow-600';
            } else {
                healthElement.className = 'text-3xl font-bold text-red-600';
            }
        }

        // Update System Status
        function updateSystemStatus(systems) {
            const container = document.getElementById('systemStatus');
            const html = Object.entries(systems).map(([name, status]) => {
                const statusClass = status.status === 'healthy' ? 'status-healthy' : 
                                 status.status === 'degraded' ? 'status-degraded' : 'status-error';
                const statusIcon = status.status === 'healthy' ? 'fa-check-circle' : 
                                status.status === 'degraded' ? 'fa-exclamation-triangle' : 'fa-times-circle';
                
                return `
                    <div class="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                        <div class="flex items-center">
                            <div class="${statusClass} text-white p-2 rounded-full mr-3">
                                <i class="fas ${statusIcon}"></i>
                            </div>
                            <div>
                                <div class="font-semibold">${name}</div>
                                <div class="text-sm text-gray-600">${status.response_time.toFixed(0)}ms</div>
                            </div>
                        </div>
                        <div class="text-right">
                            <div class="text-sm font-semibold">${status.uptime.toFixed(1)}%</div>
                            <div class="text-xs text-gray-600">Uptime</div>
                        </div>
                    </div>
                `;
            }).join('');
            
            container.innerHTML = html;
        }

        // Update Production Status
        function updateProductionStatus(production) {
            const container = document.getElementById('productionStatus');
            
            if (production.error) {
                container.innerHTML = '<div class="text-red-600">Production system unavailable</div>';
                return;
            }
            
            const dashboard = production.dashboard_data;
            const overview = dashboard.overview;
            
            const html = `
                <div class="space-y-3">
                    <div class="flex justify-between">
                        <span>Produced Videos</span>
                        <span class="font-semibold">${overview.total_produced}</span>
                    </div>
                    <div class="flex justify-between">
                        <span>Currently Producing</span>
                        <span class="font-semibold">${overview.currently_producing}</span>
                    </div>
                    <div class="flex justify-between">
                        <span>Queue Size</span>
                        <span class="font-semibold">${overview.queue_size}</span>
                    </div>
                    <div class="flex justify-between">
                        <span>Production Rate</span>
                        <span class="font-semibold">${overview.production_rate_per_hour}/hr</span>
                    </div>
                </div>
            `;
            
            container.innerHTML = html;
        }

        // Update Alerts
        function updateAlerts(alerts) {
            const container = document.getElementById('recentAlerts');
            const recentAlerts = alerts.slice(0, 5);
            
            if (recentAlerts.length === 0) {
                container.innerHTML = '<div class="text-green-600">No active alerts</div>';
                return;
            }
            
            const html = recentAlerts.map(alert => {
                const alertClass = `alert-${alert.level}`;
                return `
                    <div class="p-2 ${alertClass} text-white rounded text-sm">
                        <div class="font-semibold">${alert.title}</div>
                        <div class="text-xs opacity-90">${alert.message}</div>
                        <div class="text-xs opacity-75 mt-1">${new Date(alert.timestamp).toLocaleString()}</div>
                    </div>
                `;
            }).join('');
            
            container.innerHTML = html;
        }

        // Update Charts
        function updateCharts(data) {
            // Update performance data
            const timestamp = new Date().toLocaleTimeString();
            
            // Add new data point
            if (performanceData.labels.length > 20) {
                performanceData.labels.shift();
                performanceData.datasets.forEach(dataset => dataset.data.shift());
            }
            
            performanceData.labels.push(timestamp);
            
            // Update system metrics
            if (!performanceData.datasets.length) {
                performanceData.datasets = [
                    {
                        label: 'CPU Usage',
                        data: [],
                        borderColor: 'rgb(255, 99, 132)',
                        backgroundColor: 'rgba(255, 99, 132, 0.2)',
                    },
                    {
                        label: 'Memory Usage',
                        data: [],
                        borderColor: 'rgb(54, 162, 235)',
                        backgroundColor: 'rgba(54, 162, 235, 0.2)',
                    }
                ];
            }
            
            // Add mock data for demonstration
            performanceData.datasets[0].data.push(Math.random() * 30 + 40);
            performanceData.datasets[1].data.push(Math.random() * 20 + 60);
            
            performanceChart.update();
            
            // Update production data
            if (data.production && data.production.dashboard_data) {
                const overview = data.production.dashboard_data.overview;
                
                productionData.labels = ['Produced', 'Producing', 'Queued'];
                productionData.datasets = [{
                    label: 'Production Status',
                    data: [overview.total_produced, overview.currently_producing, overview.queue_size],
                    backgroundColor: [
                        'rgba(75, 192, 192, 0.8)',
                        'rgba(255, 206, 86, 0.8)',
                        'rgba(255, 99, 132, 0.8)'
                    ]
                }];
                
                productionChart.update();
            }
        }
    </script>
</body>
</html>
    """)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8080, reload=True)
