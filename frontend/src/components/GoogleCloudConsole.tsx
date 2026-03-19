'use client';

import { useState, useEffect } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Progress } from '@/components/ui/progress';
import { 
  Cloud, 
  Server, 
  Database, 
  Shield, 
  Activity, 
  Settings, 
  Code, 
  FileText, 
  CheckCircle, 
  XCircle, 
  AlertTriangle,
  RefreshCw,
  Terminal,
  Globe,
  Lock,
  Cpu,
  HardDrive,
  Network,
  Zap,
  Eye,
  Download
} from 'lucide-react';

interface ServiceStatus {
  service_name: string;
  display_name: string;
  version: string;
  description: string;
  status: 'available' | 'permission_denied' | 'error';
  endpoints_count: number;
  endpoints: string[];
}

interface CloudDashboard {
  project_id: string;
  overview: {
    total_services: number;
    available_services: number;
    permission_denied: number;
    errors: number;
    resource_types: number;
  };
  services: Record<string, ServiceStatus>;
  resources: Record<string, any>;
  usage_metrics: Record<string, any>;
  generated_at: string;
}

interface ApiDocumentation {
  success: boolean;
  total_apis: number;
  project_id: string;
  services: Record<string, {
    name: string;
    version: string;
    description: string;
    endpoints: string[];
  }>;
  generated_at: string;
}

export default function GoogleCloudConsole() {
  const [dashboard, setDashboard] = useState<CloudDashboard | null>(null);
  const [apiDocs, setApiDocs] = useState<ApiDocumentation | null>(null);
  const [selectedService, setSelectedService] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState<'dashboard' | 'services' | 'resources' | 'apis' | 'documentation'>('dashboard');

  useEffect(() => {
    fetchDashboard();
    fetchApiDocumentation();
  }, []);

  const fetchDashboard = async () => {
    try {
      const response = await fetch('/api/google-cloud-console/dashboard');
      const data = await response.json();
      setDashboard(data.dashboard);
    } catch (error) {
      console.error('Error fetching dashboard:', error);
    } finally {
      setLoading(false);
    }
  };

  const fetchApiDocumentation = async () => {
    try {
      const response = await fetch('/api/google-cloud-console/api-documentation');
      const data = await response.json();
      setApiDocs(data);
    } catch (error) {
      console.error('Error fetching API documentation:', error);
    }
  };

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'available': return <CheckCircle className="w-4 h-4 text-green-500" />;
      case 'permission_denied': return <XCircle className="w-4 h-4 text-red-500" />;
      case 'error': return <AlertTriangle className="w-4 h-4 text-yellow-500" />;
      default: return <AlertTriangle className="w-4 h-4 text-gray-500" />;
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'available': return 'text-green-500';
      case 'permission_denied': return 'text-red-500';
      case 'error': return 'text-yellow-500';
      default: return 'text-gray-500';
    }
  };

  const getServiceIcon = (serviceName: string) => {
    const iconMap: Record<string, JSX.Element> = {
      compute: <Server className="w-5 h-5" />,
      storage: <HardDrive className="w-5 h-5" />,
      bigquery: <Database className="w-5 h-5" />,
      iam: <Shield className="w-5 h-5" />,
      monitoring: <Activity className="w-5 h-5" />,
      logging: <FileText className="w-5 h-5" />,
      pubsub: <Network className="w-5 h-5" />,
      ml: <Cpu className="w-5 h-5" />,
      container: <Globe className="w-5 h-5" />,
      functions: <Zap className="w-5 h-5" />,
      secretmanager: <Lock className="w-5 h-5" />
    };
    return iconMap[serviceName] || <Cloud className="w-5 h-5" />;
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-950 text-white p-6">
        <div className="max-w-7xl mx-auto">
          <div className="flex items-center justify-center h-64">
            <RefreshCw className="w-8 h-8 animate-spin text-blue-500" />
          </div>
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
            <Cloud className="w-8 h-8 text-blue-500" />
            Google Cloud Console
          </h1>
          <p className="text-gray-400">
            Complete Google Cloud services integration and management
          </p>
        </div>

        {/* Overview Cards */}
        {dashboard && (
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-8">
            <Card className="bg-gray-800 border-gray-700">
              <CardContent className="p-4">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-gray-400 text-sm">Total Services</p>
                    <p className="text-2xl font-bold text-blue-500">
                      {dashboard.overview.total_services}
                    </p>
                  </div>
                  <Cloud className="w-8 h-8 text-blue-500 opacity-50" />
                </div>
              </CardContent>
            </Card>

            <Card className="bg-gray-800 border-gray-700">
              <CardContent className="p-4">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-gray-400 text-sm">Available</p>
                    <p className="text-2xl font-bold text-green-500">
                      {dashboard.overview.available_services}
                    </p>
                  </div>
                  <CheckCircle className="w-8 h-8 text-green-500 opacity-50" />
                </div>
              </CardContent>
            </Card>

            <Card className="bg-gray-800 border-gray-700">
              <CardContent className="p-4">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-gray-400 text-sm">Permission Denied</p>
                    <p className="text-2xl font-bold text-red-500">
                      {dashboard.overview.permission_denied}
                    </p>
                  </div>
                  <XCircle className="w-8 h-8 text-red-500 opacity-50" />
                </div>
              </CardContent>
            </Card>

            <Card className="bg-gray-800 border-gray-700">
              <CardContent className="p-4">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-gray-400 text-sm">Resource Types</p>
                    <p className="text-2xl font-bold text-purple-500">
                      {dashboard.overview.resource_types}
                    </p>
                  </div>
                  <Server className="w-8 h-8 text-purple-500 opacity-50" />
                </div>
              </CardContent>
            </Card>
          </div>
        )}

        {/* Tabs */}
        <div className="border-b border-gray-700 mb-6">
          <div className="flex space-x-8">
            {[
              { id: 'dashboard', label: 'Dashboard', icon: Activity },
              { id: 'services', label: 'Services', icon: Settings },
              { id: 'resources', label: 'Resources', icon: Server },
              { id: 'apis', label: 'API Explorer', icon: Terminal },
              { id: 'documentation', label: 'Documentation', icon: FileText }
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
        <div className="space-y-4">
          {/* Dashboard Tab */}
          {activeTab === 'dashboard' && dashboard && (
            <div className="space-y-6">
              <Card className="bg-gray-800 border-gray-700">
                <CardHeader>
                  <CardTitle className="flex items-center gap-2">
                    <Activity className="w-6 h-6 text-blue-500" />
                    System Overview
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                    <div>
                      <h3 className="text-lg font-semibold mb-4">Service Health</h3>
                      <div className="space-y-3">
                        {Object.entries(dashboard.services).slice(0, 5).map(([name, service]) => (
                          <div key={name} className="flex items-center justify-between p-3 bg-gray-700 rounded-lg">
                            <div className="flex items-center gap-3">
                              {getServiceIcon(name)}
                              <div>
                                <div className="font-medium">{service.display_name}</div>
                                <div className="text-sm text-gray-400">{service.version}</div>
                              </div>
                            </div>
                            <div className={`flex items-center gap-2 ${getStatusColor(service.status)}`}>
                              {getStatusIcon(service.status)}
                              <span className="text-sm capitalize">{service.status.replace('_', ' ')}</span>
                            </div>
                          </div>
                        ))}
                      </div>
                    </div>
                    
                    <div>
                      <h3 className="text-lg font-semibold mb-4">Resource Summary</h3>
                      <div className="space-y-3">
                        {Object.entries(dashboard.resources).slice(0, 5).map(([type, data]) => (
                          <div key={type} className="p-3 bg-gray-700 rounded-lg">
                            <div className="font-medium capitalize">{type.replace('_', ' ')}</div>
                            <div className="text-sm text-gray-400">
                              {Array.isArray(data) ? `${data.length} items` : 'Available'}
                            </div>
                          </div>
                        ))}
                      </div>
                    </div>
                  </div>
                </CardContent>
              </Card>
            </div>
          )}

          {/* Services Tab */}
          {activeTab === 'services' && dashboard && (
            <div className="space-y-4">
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                {Object.entries(dashboard.services).map(([name, service]) => (
                  <Card key={name} className="bg-gray-800 border-gray-700">
                    <CardContent className="p-4">
                      <div className="flex items-start justify-between mb-3">
                        <div className="flex items-center gap-2">
                          {getServiceIcon(name)}
                          <h3 className="font-medium">{service.display_name}</h3>
                        </div>
                        {getStatusIcon(service.status)}
                      </div>
                      
                      <p className="text-sm text-gray-400 mb-3">{service.description}</p>
                      
                      <div className="flex items-center justify-between text-sm">
                        <span className="text-gray-400">Version: {service.version}</span>
                        <span className="text-gray-400">{service.endpoints_count} endpoints</span>
                      </div>
                      
                      <div className="mt-3">
                        <Progress 
                          value={service.status === 'available' ? 100 : service.status === 'permission_denied' ? 50 : 0}
                          className="h-2"
                        />
                      </div>
                    </CardContent>
                  </Card>
                ))}
              </div>
            </div>
          )}

          {/* Resources Tab */}
          {activeTab === 'resources' && dashboard && (
            <div className="space-y-4">
              {Object.entries(dashboard.resources).map(([type, data]) => (
                <Card key={type} className="bg-gray-800 border-gray-700">
                  <CardHeader>
                    <CardTitle className="flex items-center gap-2 capitalize">
                      {getServiceIcon(type)}
                      {type.replace('_', ' ')}
                    </CardTitle>
                  </CardHeader>
                  <CardContent>
                    {Array.isArray(data) ? (
                      <div className="space-y-2">
                        {data.slice(0, 10).map((item: any, index: number) => (
                          <div key={index} className="p-2 bg-gray-700 rounded text-sm">
                            <div className="font-medium">{item.name || item.id || `Resource ${index + 1}`}</div>
                            <div className="text-gray-400 text-xs">
                              {item.zone && `Zone: ${item.zone}`}
                              {item.status && `Status: ${item.status}`}
                              {item.sizeGb && `Size: ${item.sizeGb}GB`}
                            </div>
                          </div>
                        ))}
                        {data.length > 10 && (
                          <div className="text-center text-gray-400 text-sm">
                            ... and {data.length - 10} more
                          </div>
                        )}
                      </div>
                    ) : (
                      <div className="text-gray-400">
                        {typeof data === 'object' ? JSON.stringify(data, null, 2) : 'No data available'}
                      </div>
                    )}
                  </CardContent>
                </Card>
              ))}
            </div>
          )}

          {/* APIs Tab */}
          {activeTab === 'apis' && (
            <div className="space-y-4">
              <Card className="bg-gray-800 border-gray-700">
                <CardHeader>
                  <CardTitle className="flex items-center gap-2">
                    <Terminal className="w-6 h-6 text-blue-500" />
                    API Explorer
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <p className="text-gray-400 mb-4">
                    Explore and test Google Cloud API endpoints directly from the console.
                  </p>
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <Button className="bg-blue-600 hover:bg-blue-700">
                      <Code className="w-4 h-4 mr-2" />
                      Generate Client Code
                    </Button>
                    <Button variant="outline" className="border-green-500 text-green-500 hover:bg-green-500/10">
                      <Eye className="w-4 h-4 mr-2" />
                      View API Documentation
                    </Button>
                  </div>
                </CardContent>
              </Card>
            </div>
          )}

          {/* Documentation Tab */}
          {activeTab === 'documentation' && apiDocs && (
            <div className="space-y-4">
              <Card className="bg-gray-800 border-gray-700">
                <CardHeader>
                  <CardTitle className="flex items-center gap-2">
                    <FileText className="w-6 h-6 text-blue-500" />
                    API Documentation
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="mb-4">
                    <p className="text-gray-400">
                      Complete documentation for all {apiDocs.total_apis} Google Cloud APIs
                    </p>
                  </div>
                  
                  <div className="space-y-4">
                    {Object.entries(apiDocs.services).map(([name, service]) => (
                      <div key={name} className="p-4 bg-gray-700 rounded-lg">
                        <div className="flex items-center justify-between mb-2">
                          <h3 className="text-lg font-semibold">{service.name}</h3>
                          <span className="text-sm text-gray-400">{service.version}</span>
                        </div>
                        <p className="text-gray-400 mb-3">{service.description}</p>
                        <div className="flex items-center justify-between">
                          <span className="text-sm text-gray-400">{service.endpoints.length} endpoints</span>
                          <Button size="sm" variant="outline">
                            <Download className="w-3 h-3 mr-1" />
                            Export
                          </Button>
                        </div>
                      </div>
                    ))}
                  </div>
                </CardContent>
              </Card>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
