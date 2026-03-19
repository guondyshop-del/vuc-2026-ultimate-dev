'use client';

import { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import styles from './ChannelManagement.module.css';
import {
  Brain,
  TrendingUp,
  Shield,
  Zap,
  BarChart3,
  Users,
  Eye,
  Clock,
  AlertTriangle,
  CheckCircle,
  Settings,
  Play,
  Pause,
  RefreshCw,
  Upload,
  Target,
  Calendar,
  DollarSign,
  Activity,
  Globe,
  Key,
  Database,
  Cpu,
  Network,
  Rocket
} from 'lucide-react';

interface Channel {
  id: number;
  name: string;
  channel_id: string;
  niche: string;
  language: string;
  is_active: boolean;
  auto_upload: boolean;
  health_score: number;
  subscribers: number;
  total_views: number;
  monthly_revenue: number;
  engagement_rate: number;
  last_sync: string;
  quota_usage: number;
  ai_optimization_enabled: boolean;
  performance_score: number;
  risk_level: string;
  growth_predictions: any;
}

interface BatchOperation {
  id: string;
  type: 'create' | 'optimize' | 'analyze' | 'sync';
  status: 'pending' | 'running' | 'completed' | 'failed';
  progress: number;
  total_items: number;
  processed_items: number;
  started_at: string;
  estimated_completion: string;
  errors: string[];
}

const ChannelManagement = () => {
  const [channels, setChannels] = useState<Channel[]>([]);
  const [selectedChannels, setSelectedChannels] = useState<number[]>([]);
  const [batchOperations, setBatchOperations] = useState<BatchOperation[]>([]);
  const [activeTab, setActiveTab] = useState<'overview' | 'batch' | 'ai' | 'analytics'>('overview');
  const [loading, setLoading] = useState(true);
  const [showBatchModal, setShowBatchModal] = useState(false);
  const [showAIModal, setShowAIModal] = useState(false);

  useEffect(() => {
    fetchChannels();
    fetchBatchOperations();
  }, []);

  const fetchChannels = async () => {
    try {
      const response = await fetch('/api/channels');
      const data = await response.json();
      if (data.success) {
        setChannels(data.channels);
      }
    } catch (error) {
      console.error('Kanallar yüklenirken hata:', error);
    } finally {
      setLoading(false);
    }
  };

  const fetchBatchOperations = async () => {
    try {
      const response = await fetch('/api/channel-management/batch-operations');
      const data = await response.json();
      if (data.success) {
        setBatchOperations(data.operations || []);
      }
    } catch (error) {
      console.error('Batch işlemleri yüklenirken hata:', error);
    }
  };

  const handleChannelSelection = (channelId: number) => {
    setSelectedChannels(prev => 
      prev.indexOf(channelId) > -1 
        ? prev.filter(id => id !== channelId)
        : [...prev, channelId]
    );
  };

  const handleSelectAll = () => {
    if (selectedChannels.length === channels.length) {
      setSelectedChannels([]);
    } else {
      setSelectedChannels(channels.map(c => c.id));
    }
  };

  const handleBatchOperation = async (operationType: string, operationData: any) => {
    try {
      const response = await fetch(`/api/channel-management/${operationType}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(operationData)
      });
      
      const data = await response.json();
      if (data.success) {
        fetchBatchOperations();
        fetchChannels();
      }
    } catch (error) {
      console.error('Batch işlemi hatası:', error);
    }
  };

  const handleAIOptimization = async (channelId: number) => {
    try {
      const response = await fetch(`/api/channel-management/${channelId}/auto-optimize`, {
        method: 'POST'
      });
      
      const data = await response.json();
      if (data.success) {
        fetchChannels();
      }
    } catch (error) {
      console.error('AI optimizasyonu hatası:', error);
    }
  };

  const getHealthColor = (score: number) => {
    if (score >= 90) return 'text-green-400';
    if (score >= 70) return 'text-yellow-400';
    return 'text-red-400';
  };

  const getRiskColor = (risk: string) => {
    switch (risk) {
      case 'low': return 'text-green-400';
      case 'medium': return 'text-yellow-400';
      case 'high': return 'text-red-400';
      case 'critical': return 'text-red-600';
      default: return 'text-gray-400';
    }
  };

  // Helper function to get progress bar width class
  const getProgressBarClass = (progress: number): string => {
    const rounded = Math.round(progress / 5) * 5; // Round to nearest 5
    return styles[`progressBarFillWidth${rounded}`] || styles.progressBarFillWidth0;
  };

  const formatNumber = (num: number) => {
    if (num >= 1000000) return `${(num / 1000000).toFixed(1)}M`;
    if (num >= 1000) return `${(num / 1000).toFixed(1)}K`;
    return num.toString();
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-900 flex items-center justify-center">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500"></div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-900 text-white p-6">
      {/* Header */}
      <div className="mb-8">
        <div className="flex items-center justify-between mb-6">
          <div className="flex items-center space-x-3">
            <Brain className="w-8 h-8 text-purple-500" />
            <h1 className="text-3xl font-bold">Gelişmiş Kanal Yönetimi</h1>
          </div>
          <div className="flex space-x-3">
            <button
              onClick={() => setShowBatchModal(true)}
              disabled={selectedChannels.length === 0}
              className="bg-blue-600 hover:bg-blue-700 disabled:bg-gray-600 px-4 py-2 rounded-lg flex items-center space-x-2 transition-colors"
            >
              <Database className="w-4 h-4" />
              <span>Batch İşlemi ({selectedChannels.length})</span>
            </button>
            <button
              onClick={() => setShowAIModal(true)}
              className="bg-purple-600 hover:bg-purple-700 px-4 py-2 rounded-lg flex items-center space-x-2 transition-colors"
            >
              <Cpu className="w-4 h-4" />
              <span>AI Analizi</span>
            </button>
          </div>
        </div>

        {/* Stats Overview */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
          <div className="bg-gray-800 rounded-lg p-6 border border-gray-700">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-gray-400 text-sm">Toplam Kanal</p>
                <p className="text-2xl font-bold">{channels.length}</p>
              </div>
              <Globe className="w-8 h-8 text-blue-400" />
            </div>
          </div>
          <div className="bg-gray-800 rounded-lg p-6 border border-gray-700">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-gray-400 text-sm">Aktif Kanal</p>
                <p className="text-2xl font-bold">{channels.filter(c => c.is_active).length}</p>
              </div>
              <Activity className="w-8 h-8 text-green-400" />
            </div>
          </div>
          <div className="bg-gray-800 rounded-lg p-6 border border-gray-700">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-gray-400 text-sm">AI Optimize</p>
                <p className="text-2xl font-bold">{channels.filter(c => c.ai_optimization_enabled).length}</p>
              </div>
              <Brain className="w-8 h-8 text-purple-400" />
            </div>
          </div>
          <div className="bg-gray-800 rounded-lg p-6 border border-gray-700">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-gray-400 text-sm">Ortalama Sağlık</p>
                <p className="text-2xl font-bold">
                  {channels.length > 0 ? Math.round(channels.reduce((sum, c) => sum + c.health_score, 0) / channels.length) : 0}%
                </p>
              </div>
              <Shield className="w-8 h-8 text-yellow-400" />
            </div>
          </div>
        </div>
      </div>

      {/* Tabs */}
      <div className="flex space-x-1 mb-6 border-b border-gray-700">
        {(['overview', 'batch', 'ai', 'analytics'] as const).map((tab) => (
          <button
            key={tab}
            onClick={() => setActiveTab(tab)}
            className={`px-4 py-2 capitalize transition-colors ${
              activeTab === tab
                ? 'text-blue-400 border-b-2 border-blue-400'
                : 'text-gray-400 hover:text-white'
            }`}
          >
            {tab === 'overview' && 'Genel Bakış'}
            {tab === 'batch' && 'Batch İşlemleri'}
            {tab === 'ai' && 'AI Yönetimi'}
            {tab === 'analytics' && 'Analitikler'}
          </button>
        ))}
      </div>

      {/* Tab Content */}
      {activeTab === 'overview' && (
        <div>
          {/* Channel Selection Controls */}
          <div className="flex items-center justify-between mb-6">
            <div className="flex items-center space-x-4">
              <label className="flex items-center space-x-2">
                <input
                  type="checkbox"
                  checked={selectedChannels.length === channels.length && channels.length > 0}
                  onChange={handleSelectAll}
                  className="w-4 h-4 text-blue-600 rounded"
                  title={`Tümünü seç (${selectedChannels.length}/${channels.length})`}
                  aria-label={`Tümünü seç (${selectedChannels.length}/${channels.length})`}
                />
                <span>Tümünü Seç ({selectedChannels.length}/{channels.length})</span>
              </label>
            </div>
            <div className="flex space-x-2">
              <button
                onClick={() => handleBatchOperation('sync', { channel_ids: selectedChannels })}
                disabled={selectedChannels.length === 0}
                className="bg-green-600 hover:bg-green-700 disabled:bg-gray-600 px-3 py-1 rounded text-sm transition-colors"
              >
                <RefreshCw className="w-3 h-3 inline mr-1" />
                Sync
              </button>
              <button
                onClick={() => handleBatchOperation('optimize', { channel_ids: selectedChannels })}
                disabled={selectedChannels.length === 0}
                className="bg-purple-600 hover:bg-purple-700 disabled:bg-gray-600 px-3 py-1 rounded text-sm transition-colors"
              >
                <Zap className="w-3 h-3 inline mr-1" />
                Optimize
              </button>
            </div>
          </div>

          {/* Channels Grid */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {channels.map((channel) => (
              <motion.div
                key={channel.id}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                className={`bg-gray-800 rounded-lg border ${
                  selectedChannels.indexOf(channel.id) > -1 ? 'border-blue-500' : 'border-gray-700'
                } hover:border-gray-600 transition-all cursor-pointer`}
                onClick={() => handleChannelSelection(channel.id)}
              >
                <div className="p-6">
                  {/* Channel Header */}
                  <div className="flex items-center justify-between mb-4">
                    <div className="flex items-center space-x-3">
                      <input
                        type="checkbox"
                        id={`channel-select-${channel.id}`}
                        checked={selectedChannels.indexOf(channel.id) > -1}
                        onChange={() => handleChannelSelection(channel.id)}
                        className="w-4 h-4 text-blue-600 rounded"
                        onClick={(e) => e.stopPropagation()}
                        title={`Kanal seç: ${channel.name}`}
                        aria-label={`Kanal seç: ${channel.name}`}
                      />
                      <div className="w-10 h-10 bg-gradient-to-br from-blue-500 to-purple-600 rounded-full flex items-center justify-center">
                        <Globe className="w-5 h-5 text-white" />
                      </div>
                      <div>
                        <h3 className="font-semibold text-lg">{channel.name}</h3>
                        <p className="text-gray-400 text-sm">@{channel.channel_id}</p>
                      </div>
                    </div>
                    <div className="flex items-center space-x-2">
                      {channel.is_active ? (
                        <CheckCircle className="w-4 h-4 text-green-400" />
                      ) : (
                        <Pause className="w-4 h-4 text-red-400" />
                      )}
                      {channel.ai_optimization_enabled && (
                        <Brain className="w-4 h-4 text-purple-400" />
                      )}
                    </div>
                  </div>

                  {/* Channel Stats */}
                  <div className="grid grid-cols-2 gap-4 mb-4">
                    <div>
                      <p className="text-gray-400 text-xs">Aboneler</p>
                      <p className="font-semibold">{formatNumber(channel.subscribers)}</p>
                    </div>
                    <div>
                      <p className="text-gray-400 text-xs">İzlenme</p>
                      <p className="font-semibold">{formatNumber(channel.total_views)}</p>
                    </div>
                    <div>
                      <p className="text-gray-400 text-xs">Etkileşim</p>
                      <p className="font-semibold">{channel.engagement_rate}%</p>
                    </div>
                    <div>
                      <p className="text-gray-400 text-xs">Gelir</p>
                      <p className="font-semibold">${formatNumber(channel.monthly_revenue)}</p>
                    </div>
                  </div>

                  {/* Health Indicators */}
                  <div className="flex items-center justify-between mb-4">
                    <div className="flex items-center space-x-2">
                      <Shield className="w-4 h-4 text-gray-400" />
                      <span className="text-sm text-gray-400">Sağlık</span>
                    </div>
                    <div className={`font-semibold ${getHealthColor(channel.health_score)}`}>
                      {channel.health_score}%
                    </div>
                  </div>

                  <div className="flex items-center justify-between mb-4">
                    <div className="flex items-center space-x-2">
                      <AlertTriangle className="w-4 h-4 text-gray-400" />
                      <span className="text-sm text-gray-400">Risk</span>
                    </div>
                    <div className={`font-semibold ${getRiskColor(channel.risk_level)}`}>
                      {channel.risk_level}
                    </div>
                  </div>

                  {/* Action Buttons */}
                  <div className="flex space-x-2">
                    <button
                      onClick={(e) => {
                        e.stopPropagation();
                        handleAIOptimization(channel.id);
                      }}
                      className="flex-1 bg-purple-600 hover:bg-purple-700 px-2 py-1 rounded text-xs transition-colors"
                    >
                      <Brain className="w-3 h-3 inline mr-1" />
                      AI Optimize
                    </button>
                    <button
                      onClick={(e) => {
                        e.stopPropagation();
                        handleBatchOperation('analyze', { channel_ids: [channel.id] });
                      }}
                      className="flex-1 bg-blue-600 hover:bg-blue-700 px-2 py-1 rounded text-xs transition-colors"
                    >
                      <BarChart3 className="w-3 h-3 inline mr-1" />
                      Analiz
                    </button>
                  </div>
                </div>
              </motion.div>
            ))}
          </div>
        </div>
      )}

      {activeTab === 'batch' && (
        <div>
          <h2 className="text-2xl font-bold mb-6">Batch İşlemleri</h2>
          
          {batchOperations.length === 0 ? (
            <div className="bg-gray-800 rounded-lg p-8 text-center">
              <Database className="w-12 h-12 text-gray-400 mx-auto mb-4" />
              <p className="text-gray-400">Aktif batch işlemi bulunmuyor</p>
            </div>
          ) : (
            <div className="space-y-4">
              {batchOperations.map((operation) => (
                <div key={operation.id} className="bg-gray-800 rounded-lg p-6 border border-gray-700">
                  <div className="flex items-center justify-between mb-4">
                    <div className="flex items-center space-x-3">
                      <div className={`w-3 h-3 rounded-full ${
                        operation.status === 'completed' ? 'bg-green-400' :
                        operation.status === 'running' ? 'bg-blue-400' :
                        operation.status === 'failed' ? 'bg-red-400' :
                        'bg-yellow-400'
                      }`} />
                      <div>
                        <h3 className="font-semibold">{operation.type}</h3>
                        <p className="text-gray-400 text-sm">
                          {operation.started_at} - {operation.estimated_completion}
                        </p>
                      </div>
                    </div>
                    <div className="flex items-center space-x-2">
                      <span className="text-sm text-gray-400">
                        {operation.processed_items}/{operation.total_items}
                      </span>
                      <span className="text-sm font-semibold">{operation.progress}%</span>
                    </div>
                  </div>
                  
                  <div className="w-full bg-gray-700 rounded-full h-2 mb-4">
                    <div className={`${styles.progressBarFill} ${getProgressBarClass(operation.progress)}`} />
                  </div>
                  
                  {operation.errors.length > 0 && (
                    <div className="bg-red-900/20 border border-red-500 rounded p-3">
                      <p className="text-red-400 text-sm">Hatalar:</p>
                      <ul className="text-red-300 text-xs mt-1">
                        {operation.errors.map((error, index) => (
                          <li key={index}>• {error}</li>
                        ))}
                      </ul>
                    </div>
                  )}
                </div>
              ))}
            </div>
          )}
        </div>
      )}

      {activeTab === 'ai' && (
        <div>
          <h2 className="text-2xl font-bold mb-6">AI Yönetimi</h2>
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div className="bg-gray-800 rounded-lg p-6 border border-gray-700">
              <div className="flex items-center justify-between mb-4">
                <h3 className="text-lg font-semibold">AI Optimizasyon Durumu</h3>
                <Brain className="w-6 h-6 text-purple-400" />
              </div>
              
              <div className="space-y-3">
                <div className="flex justify-between">
                  <span className="text-gray-400">Optimize Edilmiş Kanal</span>
                  <span>{channels.filter(c => c.ai_optimization_enabled).length}/{channels.length}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-400">Ortalama AI Skoru</span>
                  <span>87.3%</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-400">Son AI Güncellemesi</span>
                  <span>2 saat önce</span>
                </div>
              </div>
              
              <button
                onClick={() => handleBatchOperation('optimize', { channel_ids: selectedChannels })}
                disabled={selectedChannels.length === 0}
                className="w-full mt-4 bg-purple-600 hover:bg-purple-700 disabled:bg-gray-600 px-4 py-2 rounded-lg transition-colors"
              >
                Seçili Kanalları Optimize Et
              </button>
            </div>
            
            <div className="bg-gray-800 rounded-lg p-6 border border-gray-700">
              <div className="flex items-center justify-between mb-4">
                <h3 className="text-lg font-semibold">AI Tahminleri</h3>
                <TrendingUp className="w-6 h-6 text-green-400" />
              </div>
              
              <div className="space-y-3">
                <div className="flex justify-between">
                  <span className="text-gray-400">30 Günlük Büyüme</span>
                  <span className="text-green-400">+12.5%</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-400">Tahmini İzlenme</span>
                  <span>+245K</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-400">Güven Skoru</span>
                  <span>92.1%</span>
                </div>
              </div>
              
              <button
                onClick={() => setShowAIModal(true)}
                className="w-full mt-4 bg-blue-600 hover:bg-blue-700 px-4 py-2 rounded-lg transition-colors"
              >
                Detaylı AI Analizi
              </button>
            </div>
          </div>
        </div>
      )}

      {activeTab === 'analytics' && (
        <div>
          <h2 className="text-2xl font-bold mb-6">Gelişmiş Analitikler</h2>
          
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div className="bg-gray-800 rounded-lg p-6 border border-gray-700">
              <BarChart3 className="w-8 h-8 text-blue-400 mb-4" />
              <h3 className="text-lg font-semibold mb-2">Performans Trendleri</h3>
              <p className="text-gray-400 text-sm">Son 30 günlük performans analizi ve trendler</p>
            </div>
            
            <div className="bg-gray-800 rounded-lg p-6 border border-gray-700">
              <Target className="w-8 h-8 text-green-400 mb-4" />
              <h3 className="text-lg font-semibold mb-2">Hedef Karşılaştırma</h3>
              <p className="text-gray-400 text-sm">Belirlenen hedeflere ulaşma durumu</p>
            </div>
            
            <div className="bg-gray-800 rounded-lg p-6 border border-gray-700">
              <Rocket className="w-8 h-8 text-purple-400 mb-4" />
              <h3 className="text-lg font-semibold mb-2">Büyüme Stratejileri</h3>
              <p className="text-gray-400 text-sm">AI tarafından önerilen büyüme stratejileri</p>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default ChannelManagement;
