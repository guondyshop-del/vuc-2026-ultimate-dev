'use client';

import { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { 
  Film, 
  Globe, 
  User, 
  Link2, 
  BarChart3, 
  Brain,
  Play,
  Settings,
  Zap,
  Shield,
  Eye,
  Upload,
  TrendingUp,
  Database,
  Monitor,
  Cpu,
  Activity
} from 'lucide-react';
import { Button } from '@/components/ui/button';

// Tab Components
import ProductionLab from './tabs/ProductionLab';
import MultiVerse from './tabs/MultiVerse';
import PersonaVault from './tabs/PersonaVault';
import Connections from './tabs/Connections';
import GlobalAnalytics from './tabs/GlobalAnalytics';

export default function OmniverseDashboard() {
  const [activeTab, setActiveTab] = useState('production');
  const [systemMetrics, setSystemMetrics] = useState({
    cpu: 45,
    memory: 62,
    gpu: 78,
    network: 89
  });

  useEffect(() => {
    const interval = setInterval(() => {
      setSystemMetrics(prev => ({
        cpu: Math.min(100, Math.max(0, prev.cpu + (Math.random() - 0.5) * 10)),
        memory: Math.min(100, Math.max(0, prev.memory + (Math.random() - 0.5) * 8)),
        gpu: Math.min(100, Math.max(0, prev.gpu + (Math.random() - 0.5) * 12)),
        network: Math.min(100, Math.max(0, prev.network + (Math.random() - 0.5) * 15))
      }));
    }, 3000);
    return () => clearInterval(interval);
  }, []);

  const tabs = [
    {
      id: 'production',
      label: '🎬 Production Lab',
      icon: Film,
      description: 'Gemini 2.0 Pro Scripting + ElevenLabs Voice + FFmpeg Master Rendering'
    },
    {
      id: 'multiverse',
      label: '🌌 Multi-Verse',
      icon: Globe,
      description: 'AI-Cutter (9:16) + Platform adaptation (TikTok/IG/X/FB)'
    },
    {
      id: 'persona',
      label: '👤 Persona Vault',
      icon: User,
      description: 'Proxy health + Device fingerprint management'
    },
    {
      id: 'connections',
      label: '🔌 Connections',
      icon: Link2,
      description: 'Encrypted API Vault + Step-by-step Documentation'
    },
    {
      id: 'analytics',
      label: '📈 Global Analytics',
      icon: BarChart3,
      description: 'Unified ROI, CPM, and Viral Velocity heatmaps'
    }
  ];

  const getMetricColor = (value: number) => {
    if (value < 50) return 'text-green-400';
    if (value < 80) return 'text-yellow-400';
    return 'text-red-400';
  };

  const getMetricBg = (value: number) => {
    if (value < 50) return 'bg-green-500/20';
    if (value < 80) return 'bg-yellow-500/20';
    return 'bg-red-500/20';
  };

  return (
    <div className="min-h-screen bg-gray-900 text-white">
      {/* Header */}
      <motion.div
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        className="bg-gray-800/50 backdrop-blur-lg border-b border-gray-700"
      >
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16">
            <div className="flex items-center space-x-4">
              <div className="p-2 bg-gradient-to-r from-purple-500 to-pink-600 rounded-lg">
                <Brain className="w-6 h-6 text-white" />
              </div>
              <div>
                <h1 className="text-xl font-bold text-white">VUC-2026 Neural Core</h1>
                <p className="text-xs text-gray-400">Multi-Verse Media Empire Manager</p>
              </div>
            </div>

            {/* System Metrics */}
            <div className="flex items-center space-x-4">
              <div className={`flex items-center space-x-2 px-3 py-1 rounded-lg ${getMetricBg(systemMetrics.cpu)}`}>
                <Cpu className={`w-3 h-3 ${getMetricColor(systemMetrics.cpu)}`} />
                <span className={`text-xs font-medium ${getMetricColor(systemMetrics.cpu)}`}>
                  CPU {systemMetrics.cpu}%
                </span>
              </div>
              <div className={`flex items-center space-x-2 px-3 py-1 rounded-lg ${getMetricBg(systemMetrics.memory)}`}>
                <Database className={`w-3 h-3 ${getMetricColor(systemMetrics.memory)}`} />
                <span className={`text-xs font-medium ${getMetricColor(systemMetrics.memory)}`}>
                  RAM {systemMetrics.memory}%
                </span>
              </div>
              <div className={`flex items-center space-x-2 px-3 py-1 rounded-lg ${getMetricBg(systemMetrics.gpu)}`}>
                <Monitor className={`w-3 h-3 ${getMetricColor(systemMetrics.gpu)}`} />
                <span className={`text-xs font-medium ${getMetricColor(systemMetrics.gpu)}`}>
                  GPU {systemMetrics.gpu}%
                </span>
              </div>
              <div className={`flex items-center space-x-2 px-3 py-1 rounded-lg ${getMetricBg(systemMetrics.network)}`}>
                <Activity className={`w-3 h-3 ${getMetricColor(systemMetrics.network)}`} />
                <span className={`text-xs font-medium ${getMetricColor(systemMetrics.network)}`}>
                  NET {systemMetrics.network}%
                </span>
              </div>
            </div>

            {/* Quick Actions */}
            <div className="flex items-center space-x-2">
              <Button variant="outline" size="sm" className="text-xs">
                <Shield className="w-3 h-3 mr-1" />
                Stealth 4.0
              </Button>
              <Button variant="outline" size="sm" className="text-xs">
                <Zap className="w-3 h-3 mr-1" />
                Auto-Pilot
              </Button>
            </div>
          </div>
        </div>
      </motion.div>

      {/* Main Content */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.3 }}
        >
          <Tabs value={activeTab} onValueChange={setActiveTab} className="space-y-6">
            <TabsList className="grid w-full grid-cols-5 bg-gray-800/50 border border-gray-700">
              {tabs.map((tab) => {
                const Icon = tab.icon;
                return (
                  <TabsTrigger
                    key={tab.id}
                    value={tab.id}
                    className="data-[state=active]:bg-gray-700 data-[state=active]:text-white text-gray-400 text-xs"
                  >
                    <div className="flex items-center space-x-2">
                      <Icon className="w-4 h-4" />
                      <span className="hidden md:inline">{tab.label.split(' ')[0]}</span>
                    </div>
                  </TabsTrigger>
                );
              })}
            </TabsList>

            <TabsContent value="production" className="space-y-4">
              <ProductionLab />
            </TabsContent>

            <TabsContent value="multiverse" className="space-y-4">
              <MultiVerse />
            </TabsContent>

            <TabsContent value="persona" className="space-y-4">
              <PersonaVault />
            </TabsContent>

            <TabsContent value="connections" className="space-y-4">
              <Connections />
            </TabsContent>

            <TabsContent value="analytics" className="space-y-4">
              <GlobalAnalytics />
            </TabsContent>
          </Tabs>
        </motion.div>
      </div>

      {/* Status Bar */}
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        className="fixed bottom-0 left-0 right-0 bg-gray-800/90 backdrop-blur-lg border-t border-gray-700"
      >
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-12 text-xs">
            <div className="flex items-center space-x-4">
              <div className="flex items-center space-x-2">
                <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></div>
                <span className="text-green-400">Sistem Aktif</span>
              </div>
              <div className="flex items-center space-x-2">
                <Eye className="w-3 h-3 text-blue-400" />
                <span className="text-blue-400">127 Kanal İzleniyor</span>
              </div>
              <div className="flex items-center space-x-2">
                <Upload className="w-3 h-3 text-purple-400" />
                <span className="text-purple-400">42 Video Kuyrukta</span>
              </div>
            </div>
            <div className="flex items-center space-x-4">
              <div className="flex items-center space-x-2">
                <TrendingUp className="w-3 h-3 text-green-400" />
                <span className="text-green-400">+34% Büyüme</span>
              </div>
              <div className="flex items-center space-x-2">
                <Zap className="w-3 h-3 text-yellow-400" />
                <span className="text-yellow-400">2.4M İzlenme</span>
              </div>
              <div className="flex items-center space-x-2">
                <Play className="w-3 h-3 text-purple-400" />
                <span className="text-purple-400">89% Otonom</span>
              </div>
            </div>
          </div>
        </div>
      </motion.div>
    </div>
  );
}
