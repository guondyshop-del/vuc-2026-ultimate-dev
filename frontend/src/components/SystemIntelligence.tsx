'use client';

import { useState, useEffect } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Progress } from '@/components/ui/progress';
import { 
  Brain, 
  Zap, 
  Activity, 
  TrendingUp, 
  Shield, 
  Cpu, 
  HardDrive, 
  Database, 
  Network, 
  AlertTriangle,
  CheckCircle,
  XCircle,
  RefreshCw,
  Play,
  Pause,
  Settings,
  BarChart3,
  Target,
  Rocket,
  Gauge
} from 'lucide-react';

interface SystemMetrics {
  cpu_percent: number;
  memory_percent: number;
  disk_usage: number;
  network_io: Record<string, number>;
  process_count: number;
  timestamp: string;
  performance_score: number;
}

interface OptimizationAction {
  action_type: string;
  priority: number;
  description: string;
  estimated_impact: number;
  execution_time: number;
}

interface SystemInsight {
  insight_type: string;
  severity: string;
  description: string;
  data: Record<string, any>;
  recommendations: string[];
  confidence: number;
  timestamp: string;
}

interface IntelligenceStatus {
  optimizer: {
    current_metrics: SystemMetrics;
    total_optimizations: number;
    successful_optimizations: number;
    success_rate: number;
    average_execution_time: number;
    recent_optimizations: any[];
    is_optimizing: boolean;
  };
  accelerator: {
    total_operations: number;
    successful_operations: number;
    success_rate: number;
    average_duration: number;
    cache_hit_rate: number;
    acceleration_factor: number;
    memory_cache_size: number;
    active_tasks: number;
  };
  intelligence: {
    patterns_detected: number;
    models_trained: number;
    feature_history_size: number;
    intelligence_capabilities: Record<string, boolean>;
  };
  overall_status: string;
  timestamp: string;
}

export default function SystemIntelligence() {
  const [status, setStatus] = useState<IntelligenceStatus | null>(null);
  const [metrics, setMetrics] = useState<SystemMetrics | null>(null);
  const [insights, setInsights] = useState<SystemInsight[]>([]);
  const [isOptimizing, setIsOptimizing] = useState(false);
  const [isAccelerating, setIsAccelerating] = useState(false);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [activeTab, setActiveTab] = useState<'overview' | 'optimizer' | 'accelerator' | 'intelligence' | 'insights'>('overview');
  const [refreshInterval, setRefreshInterval] = useState<NodeJS.Timeout | null>(null);

  useEffect(() => {
    fetchStatus();
    fetchMetrics();
    fetchInsights();
    
    // Set up auto-refresh
    const interval = setInterval(() => {
      fetchStatus();
      fetchMetrics();
    }, 5000);
    
    setRefreshInterval(interval);
    
    return () => {
      if (interval) clearInterval(interval);
    };
  }, []);

  const fetchStatus = async () => {
    try {
      const response = await fetch('/api/system-intelligence/status');
      const data = await response.json();
      setStatus(data);
    } catch (error) {
      console.error('Error fetching status:', error);
    }
  };

  const fetchMetrics = async () => {
    try {
      const response = await fetch('/api/system-intelligence/metrics');
      const data = await response.json();
      setMetrics(data.metrics);
    } catch (error) {
      console.error('Error fetching metrics:', error);
    }
  };

  const fetchInsights = async () => {
    try {
      const response = await fetch('/api/system-intelligence/insights');
      const data = await response.json();
      setInsights(data.insights);
    } catch (error) {
      console.error('Error fetching insights:', error);
    }
  };

  const handleOptimize = async () => {
    setIsOptimizing(true);
    try {
      const response = await fetch('/api/system-intelligence/optimize', { method: 'POST' });
      const data = await response.json();
      
      if (data.success) {
        // Refresh status after optimization
        setTimeout(() => {
          fetchStatus();
          fetchMetrics();
        }, 2000);
      }
    } catch (error) {
      console.error('Error optimizing:', error);
    } finally {
      setIsOptimizing(false);
    }
  };

  const handleAccelerate = async () => {
    setIsAccelerating(true);
    try {
      const response = await fetch('/api/system-intelligence/accelerate', { method: 'POST' });
      const data = await response.json();
      
      if (data.success) {
        setTimeout(() => {
          fetchStatus();
        }, 1000);
      }
    } catch (error) {
      console.error('Error accelerating:', error);
    } finally {
      setIsAccelerating(false);
    }
  };

  const handleAnalyze = async () => {
    setIsAnalyzing(true);
    try {
      const response = await fetch('/api/system-intelligence/analyze', { method: 'POST' });
      const data = await response.json();
      
      if (data.success) {
        setInsights(data.insights);
        setTimeout(() => {
          fetchStatus();
        }, 1000);
      }
    } catch (error) {
      console.error('Error analyzing:', error);
    } finally {
      setIsAnalyzing(false);
    }
  };

  const handleEmergencyOptimization = async () => {
    try {
      const response = await fetch('/api/system-intelligence/emergency-optimization', { method: 'POST' });
      const data = await response.json();
      
      if (data.success) {
        setTimeout(() => {
          fetchStatus();
          fetchMetrics();
        }, 1000);
      }
    } catch (error) {
      console.error('Error in emergency optimization:', error);
    }
  };

  const getHealthColor = (score: number) => {
    if (score >= 80) return 'text-green-500';
    if (score >= 60) return 'text-yellow-500';
    if (score >= 40) return 'text-orange-500';
    return 'text-red-500';
  };

  const getHealthIcon = (score: number) => {
    if (score >= 80) return <CheckCircle className="w-4 h-4 text-green-500" />;
    if (score >= 60) return <Activity className="w-4 h-4 text-yellow-500" />;
    if (score >= 40) return <AlertTriangle className="w-4 h-4 text-orange-500" />;
    return <XCircle className="w-4 h-4 text-red-500" />;
  };

  const getSeverityColor = (severity: string) => {
    switch (severity) {
      case 'critical': return 'text-red-500';
      case 'high': return 'text-orange-500';
      case 'medium': return 'text-yellow-500';
      case 'low': return 'text-blue-500';
      default: return 'text-gray-500';
    }
  };

  if (!status) {
    return (
      <div className="min-h-screen bg-gray-950 text-white p-6">
        <div className="flex items-center justify-center h-64">
          <RefreshCw className="w-8 h-8 animate-spin text-blue-500" />
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-950 text-white p-6">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold mb-2 flex items-center gap-3">
            <Brain className="w-8 h-8 text-blue-500" />
            System Intelligence
          </h1>
          <p className="text-gray-400">
            Advanced AI-powered system optimization, acceleration, and intelligence
          </p>
        </div>

        {/* Action Buttons */}
        <div className="flex flex-wrap gap-4 mb-8">
          <Button
            onClick={handleOptimize}
            disabled={isOptimizing}
            className="bg-blue-600 hover:bg-blue-700"
          >
            {isOptimizing ? (
              <RefreshCw className="w-4 h-4 mr-2 animate-spin" />
            ) : (
              <Zap className="w-4 h-4 mr-2" />
            )}
            {isOptimizing ? 'Optimizing...' : 'Optimize System'}
          </Button>
          
          <Button
            onClick={handleAccelerate}
            disabled={isAccelerating}
            variant="outline"
            className="border-green-500 text-green-500 hover:bg-green-500/10"
          >
            {isAccelerating ? (
              <RefreshCw className="w-4 h-4 mr-2 animate-spin" />
            ) : (
              <Rocket className="w-4 h-4 mr-2" />
            )}
            {isAccelerating ? 'Accelerating...' : 'Accelerate'}
          </Button>
          
          <Button
            onClick={handleAnalyze}
            disabled={isAnalyzing}
            variant="outline"
            className="border-purple-500 text-purple-500 hover:bg-purple-500/10"
          >
            {isAnalyzing ? (
              <RefreshCw className="w-4 h-4 mr-2 animate-spin" />
            ) : (
              <Brain className="w-4 h-4 mr-2" />
            )}
            {isAnalyzing ? 'Analyzing...' : 'Analyze Intelligence'}
          </Button>
          
          <Button
            onClick={handleEmergencyOptimization}
            variant="outline"
            className="border-red-500 text-red-500 hover:bg-red-500/10"
          >
            <Shield className="w-4 h-4 mr-2" />
            Emergency
          </Button>
        </div>

        {/* Health Score */}
        {metrics && (
          <Card className="bg-gray-800 border-gray-700 mb-8">
            <CardContent className="p-6">
              <div className="flex items-center justify-between">
                <div>
                  <h3 className="text-lg font-semibold mb-2">System Health Score</h3>
                  <div className="flex items-center gap-3">
                    <span className={`text-3xl font-bold ${getHealthColor(metrics.performance_score)}`}>
                      {metrics.performance_score.toFixed(1)}%
                    </span>
                    {getHealthIcon(metrics.performance_score)}
                  </div>
                </div>
                <div className="text-right">
                  <Progress value={metrics.performance_score} className="w-32 h-2" />
                  <p className="text-sm text-gray-400 mt-2">
                    Overall Health
                  </p>
                </div>
              </div>
            </CardContent>
          </Card>
        )}

        {/* Tabs */}
        <div className="border-b border-gray-700 mb-6">
          <div className="flex space-x-8">
            {[
              { id: 'overview', label: 'Overview', icon: Activity },
              { id: 'optimizer', label: 'Optimizer', icon: Settings },
              { id: 'accelerator', label: 'Accelerator', icon: Zap },
              { id: 'intelligence', label: 'Intelligence', icon: Brain },
              { id: 'insights', label: 'Insights', icon: Target }
            ].map(tab => (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id as any)}
                className={`flex items-center gap-2 pb-3 border-b-2 transition-colors ${
                  activeTab === tab.id
                    ? 'border-blue-500 text-blue-500'
                    : 'border-transparent text-gray-400 hover:text-gray-300'
                }`}
              >
                <tab.icon className="w-4 h-4" />
                {tab.label}
              </button>
            ))}
          </div>
        </div>

        {/* Tab Content */}
        <div className="space-y-6">
          {/* Overview Tab */}
          {activeTab === 'overview' && (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
              <Card className="bg-gray-800 border-gray-700">
                <CardContent className="p-4">
                  <div className="flex items-center justify-between mb-2">
                    <Cpu className="w-5 h-5 text-blue-500" />
                    <span className="text-sm text-gray-400">CPU</span>
                  </div>
                  <div className="text-2xl font-bold">
                    {metrics?.cpu_percent.toFixed(1)}%
                  </div>
                  <Progress value={metrics?.cpu_percent || 0} className="mt-2 h-2" />
                </CardContent>
              </Card>

              <Card className="bg-gray-800 border-gray-700">
                <CardContent className="p-4">
                  <div className="flex items-center justify-between mb-2">
                    <Database className="w-5 h-5 text-green-500" />
                    <span className="text-sm text-gray-400">Memory</span>
                  </div>
                  <div className="text-2xl font-bold">
                    {metrics?.memory_percent.toFixed(1)}%
                  </div>
                  <Progress value={metrics?.memory_percent || 0} className="mt-2 h-2" />
                </CardContent>
              </Card>

              <Card className="bg-gray-800 border-gray-700">
                <CardContent className="p-4">
                  <div className="flex items-center justify-between mb-2">
                    <HardDrive className="w-5 h-5 text-yellow-500" />
                    <span className="text-sm text-gray-400">Disk</span>
                  </div>
                  <div className="text-2xl font-bold">
                    {metrics?.disk_usage.toFixed(1)}%
                  </div>
                  <Progress value={metrics?.disk_usage || 0} className="mt-2 h-2" />
                </CardContent>
              </Card>

              <Card className="bg-gray-800 border-gray-700">
                <CardContent className="p-4">
                  <div className="flex items-center justify-between mb-2">
                    <Network className="w-5 h-5 text-purple-500" />
                    <span className="text-sm text-gray-400">Processes</span>
                  </div>
                  <div className="text-2xl font-bold">
                    {metrics?.process_count}
                  </div>
                  <p className="text-sm text-gray-400 mt-2">Active processes</p>
                </CardContent>
              </Card>
            </div>
          )}

          {/* Optimizer Tab */}
          {activeTab === 'optimizer' && (
            <div className="space-y-6">
              <Card className="bg-gray-800 border-gray-700">
                <CardHeader>
                  <CardTitle className="flex items-center gap-2">
                    <Settings className="w-6 h-6 text-blue-500" />
                    System Optimizer
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                    <div>
                      <h4 className="font-semibold mb-2">Optimization Statistics</h4>
                      <div className="space-y-2">
                        <div className="flex justify-between">
                          <span className="text-gray-400">Total Optimizations</span>
                          <span>{status.optimizer.total_optimizations}</span>
                        </div>
                        <div className="flex justify-between">
                          <span className="text-gray-400">Success Rate</span>
                          <span className="text-green-500">{status.optimizer.success_rate.toFixed(1)}%</span>
                        </div>
                        <div className="flex justify-between">
                          <span className="text-gray-400">Avg Execution Time</span>
                          <span>{status.optimizer.average_execution_time.toFixed(2)}s</span>
                        </div>
                      </div>
                    </div>
                    
                    <div>
                      <h4 className="font-semibold mb-2">Current Status</h4>
                      <div className="flex items-center gap-2">
                        <div className={`w-2 h-2 rounded-full ${
                          status.optimizer.is_optimizing ? 'bg-green-500' : 'bg-gray-500'
                        }`} />
                        <span>{status.optimizer.is_optimizing ? 'Optimizing' : 'Idle'}</span>
                      </div>
                    </div>
                    
                    <div>
                      <h4 className="font-semibold mb-2">Performance Score</h4>
                      <div className="text-2xl font-bold text-green-500">
                        {status.optimizer.current_metrics?.performance_score.toFixed(1)}%
                      </div>
                    </div>
                  </div>
                </CardContent>
              </Card>
            </div>
          )}

          {/* Accelerator Tab */}
          {activeTab === 'accelerator' && (
            <div className="space-y-6">
              <Card className="bg-gray-800 border-gray-700">
                <CardHeader>
                  <CardTitle className="flex items-center gap-2">
                    <Zap className="w-6 h-6 text-green-500" />
                    Performance Accelerator
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                    <div>
                      <h4 className="font-semibold mb-2">Acceleration Factor</h4>
                      <div className="text-2xl font-bold text-green-500">
                        {status.accelerator.acceleration_factor.toFixed(2)}x
                      </div>
                    </div>
                    
                    <div>
                      <h4 className="font-semibold mb-2">Cache Hit Rate</h4>
                      <div className="text-2xl font-bold text-blue-500">
                        {status.accelerator.cache_hit_rate.toFixed(1)}%
                      </div>
                    </div>
                    
                    <div>
                      <h4 className="font-semibold mb-2">Active Tasks</h4>
                      <div className="text-2xl font-bold text-purple-500">
                        {status.accelerator.active_tasks}
                      </div>
                    </div>
                    
                    <div>
                      <h4 className="font-semibold mb-2">Memory Cache</h4>
                      <div className="text-2xl font-bold text-yellow-500">
                        {status.accelerator.memory_cache_size}
                      </div>
                    </div>
                  </div>
                </CardContent>
              </Card>
            </div>
          )}

          {/* Intelligence Tab */}
          {activeTab === 'intelligence' && (
            <div className="space-y-6">
              <Card className="bg-gray-800 border-gray-700">
                <CardHeader>
                  <CardTitle className="flex items-center gap-2">
                    <Brain className="w-6 h-6 text-purple-500" />
                    Intelligence Engine
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                    <div>
                      <h4 className="font-semibold mb-4">AI Capabilities</h4>
                      <div className="space-y-2">
                        {Object.entries(status.intelligence.intelligence_capabilities).map(([capability, enabled]) => (
                          <div key={capability} className="flex items-center justify-between">
                            <span className="capitalize text-gray-400">{capability.replace('_', ' ')}</span>
                            <div className={`w-2 h-2 rounded-full ${
                              enabled ? 'bg-green-500' : 'bg-gray-500'
                            }`} />
                          </div>
                        ))}
                      </div>
                    </div>
                    
                    <div>
                      <h4 className="font-semibold mb-4">Learning Statistics</h4>
                      <div className="space-y-2">
                        <div className="flex justify-between">
                          <span className="text-gray-400">Patterns Detected</span>
                          <span>{status.intelligence.patterns_detected}</span>
                        </div>
                        <div className="flex justify-between">
                          <span className="text-gray-400">Models Trained</span>
                          <span>{status.intelligence.models_trained}</span>
                        </div>
                        <div className="flex justify-between">
                          <span className="text-gray-400">Feature History</span>
                          <span>{status.intelligence.feature_history_size}</span>
                        </div>
                      </div>
                    </div>
                  </div>
                </CardContent>
              </Card>
            </div>
          )}

          {/* Insights Tab */}
          {activeTab === 'insights' && (
            <div className="space-y-4">
              {insights.length === 0 ? (
                <Card className="bg-gray-800 border-gray-700">
                  <CardContent className="p-6 text-center">
                    <Brain className="w-12 h-12 text-gray-500 mx-auto mb-4" />
                    <p className="text-gray-400">No insights available. Run analysis to generate insights.</p>
                  </CardContent>
                </Card>
              ) : (
                insights.map((insight, index) => (
                  <Card key={index} className="bg-gray-800 border-gray-700">
                    <CardContent className="p-4">
                      <div className="flex items-start justify-between mb-3">
                        <div className="flex items-center gap-2">
                          <Target className="w-5 h-5 text-blue-500" />
                          <h3 className="font-semibold capitalize">{insight.insight_type}</h3>
                          <span className={`text-sm px-2 py-1 rounded ${getSeverityColor(insight.severity)}`}>
                            {insight.severity}
                          </span>
                        </div>
                        <span className="text-sm text-gray-400">
                          {(insight.confidence * 100).toFixed(1)}% confidence
                        </span>
                      </div>
                      
                      <p className="text-gray-300 mb-3">{insight.description}</p>
                      
                      {insight.recommendations.length > 0 && (
                        <div>
                          <h4 className="font-semibold mb-2">Recommendations:</h4>
                          <ul className="list-disc list-inside text-sm text-gray-400 space-y-1">
                            {insight.recommendations.map((rec, idx) => (
                              <li key={idx}>{rec}</li>
                            ))}
                          </ul>
                        </div>
                      )}
                    </CardContent>
                  </Card>
                ))
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
