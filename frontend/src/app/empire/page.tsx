'use client';

import { motion } from 'framer-motion';
import { useState, useEffect } from 'react';
import { 
  Brain, 
  Network, 
  Zap, 
  Shield, 
  TrendingUp, 
  Users, 
  BarChart3,
  Cpu,
  Activity,
  AlertTriangle,
  CheckCircle,
  Clock,
  Target,
  Rocket,
  Globe,
  Database,
  MessageSquare,
  Settings,
  PlayCircle,
  Upload,
  Video,
  Search,
  Eye
} from 'lucide-react';

interface EmpireStatus {
  empire_metrics: {
    total_channels: number;
    active_campaigns: number;
    monthly_revenue: number;
    success_rate: number;
  };
  active_intelligence_objects: number;
  agent_communications: number;
  decision_history: number;
  confidence_thresholds: {
    autonomous: number;
    consult_threshold: number;
    manual_required: number;
  };
  system_health: {
    uptime: string;
    error_rate: string;
    response_time: string;
    autonomous_rate: string;
  };
  recent_decisions: any[];
  pending_consultations: any[];
}

interface AgentStatus {
  agent_id: string;
  capabilities: any;
  health_status: string;
  average_confidence?: number;
  last_generation?: string;
}

interface CampaignData {
  topic: string;
  script_type: string;
  tone: string;
  target_audience: string;
  duration_target: number;
  seo_keywords: string[];
  resolution: string;
  fps: number;
  codec: string;
  shadowban_shield: boolean;
  device_type: string;
  title: string;
  description: string;
  tags: string[];
  category: string;
  privacy_status: string;
  video_file: {
    size_mb: number;
  };
  use_proxy: boolean;
  priority: string;
}

export default function EmpirePage() {
  const [empireStatus, setEmpireStatus] = useState<EmpireStatus | null>(null);
  const [agents, setAgents] = useState<Record<string, AgentStatus>>({});
  const [activeCampaign, setActiveCampaign] = useState<CampaignData | null>(null);
  const [campaignResults, setCampaignResults] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [selectedAgent, setSelectedAgent] = useState<string | null>(null);

  useEffect(() => {
    fetchEmpireStatus();
    fetchAgentStatus();
    
    const interval = setInterval(() => {
      fetchEmpireStatus();
      fetchAgentStatus();
    }, 5000); // Update every 5 seconds
    
    return () => clearInterval(interval);
  }, []);

  const fetchEmpireStatus = async () => {
    try {
      const response = await fetch('/api/empire/status');
      const data = await response.json();
      
      if (data.success) {
        setEmpireStatus(data.empire_status);
      }
    } catch (error) {
      console.error('Empire durumu alınamadı:', error);
    } finally {
      setLoading(false);
    }
  };

  const fetchAgentStatus = async () => {
    try {
      const response = await fetch('/api/empire/agents/status');
      const data = await response.json();
      
      if (data.success) {
        setAgents(data.agents);
      }
    } catch (error) {
      console.error('Ajan durumu alınamadı:', error);
    }
  };

  const executeCampaign = async () => {
    if (!activeCampaign) return;

    setLoading(true);
    try {
      const response = await fetch('/api/empire/campaign/execute', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(activeCampaign),
      });

      const data = await response.json();
      
      if (data.success) {
        setCampaignResults(data.results);
        setActiveCampaign(null);
      }
    } catch (error) {
      console.error('Kampanya yürütme hatası:', error);
    } finally {
      setLoading(false);
    }
  };

  const getHealthColor = (status: string) => {
    switch (status) {
      case 'healthy': return 'text-green-500';
      case 'degraded': return 'text-yellow-500';
      case 'critical': return 'text-red-500';
      default: return 'text-gray-500';
    }
  };

  const getProgressBarClass = (percentage: number) => {
    if (percentage === 0) return 'progressBarFillWidth0';
    if (percentage <= 5) return 'progressBarFillWidth5';
    if (percentage <= 10) return 'progressBarFillWidth10';
    if (percentage <= 15) return 'progressBarFillWidth15';
    if (percentage <= 20) return 'progressBarFillWidth20';
    if (percentage <= 25) return 'progressBarFillWidth25';
    if (percentage <= 30) return 'progressBarFillWidth30';
    if (percentage <= 35) return 'progressBarFillWidth35';
    if (percentage <= 40) return 'progressBarFillWidth40';
    if (percentage <= 45) return 'progressBarFillWidth45';
    if (percentage <= 50) return 'progressBarFillWidth50';
    if (percentage <= 55) return 'progressBarFillWidth55';
    if (percentage <= 60) return 'progressBarFillWidth60';
    if (percentage <= 65) return 'progressBarFillWidth65';
    if (percentage <= 70) return 'progressBarFillWidth70';
    if (percentage <= 75) return 'progressBarFillWidth75';
    if (percentage <= 80) return 'progressBarFillWidth80';
    if (percentage <= 85) return 'progressBarFillWidth85';
    if (percentage <= 90) return 'progressBarFillWidth90';
    if (percentage <= 95) return 'progressBarFillWidth95';
    return 'progressBarFillWidth100';
  };

  if (loading && !empireStatus) {
    return (
      <div className="min-h-screen bg-gray-900 text-white flex items-center justify-center">
        <div className="flex flex-col items-center space-y-4">
          <Brain className="w-16 h-16 animate-pulse text-blue-500" />
          <p className="text-xl">VUC-2026 Neural Architecture yükleniyor...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-900 text-white p-6">
      {/* Header */}
      <motion.div
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        className="mb-8"
      >
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-4">
            <Brain className="w-12 h-12 text-blue-500" />
            <div>
              <h1 className="text-4xl font-bold bg-gradient-to-r from-blue-400 to-purple-600 bg-clip-text text-transparent">
                VUC-2026 Empire Control
              </h1>
              <p className="text-gray-400">Neural Architecture & Multi-Agent System</p>
            </div>
          </div>
          <div className="flex items-center space-x-4">
            <div className={`flex items-center space-x-2 px-4 py-2 rounded-lg ${
              empireStatus?.system_health.uptime === '24/7' ? 'bg-green-500/20 text-green-400' : 'bg-red-500/20 text-red-400'
            }`}>
              <Activity className="w-4 h-4" />
              <span className="text-sm font-medium">
                {empireStatus?.system_health.uptime || 'Loading...'}
              </span>
            </div>
          </div>
        </div>
      </motion.div>

      {/* Empire Metrics */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.1 }}
        className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8"
      >
        <div className="bg-gray-800 rounded-xl p-6 border border-gray-700">
          <div className="flex items-center justify-between mb-4">
            <div className="flex items-center space-x-3">
              <div className="p-2 bg-blue-500/20 rounded-lg">
                <Globe className="w-6 h-6 text-blue-500" />
              </div>
              <div>
                <p className="text-gray-400 text-sm">Toplam Kanallar</p>
                <p className="text-2xl font-bold">{empireStatus?.empire_metrics.total_channels || 0}</p>
              </div>
            </div>
          </div>
        </div>

        <div className="bg-gray-800 rounded-xl p-6 border border-gray-700">
          <div className="flex items-center justify-between mb-4">
            <div className="flex items-center space-x-3">
              <div className="p-2 bg-green-500/20 rounded-lg">
                <Rocket className="w-6 h-6 text-green-500" />
              </div>
              <div>
                <p className="text-gray-400 text-sm">Aktif Kampanyalar</p>
                <p className="text-2xl font-bold">{empireStatus?.empire_metrics.active_campaigns || 0}</p>
              </div>
            </div>
          </div>
        </div>

        <div className="bg-gray-800 rounded-xl p-6 border border-gray-700">
          <div className="flex items-center justify-between mb-4">
            <div className="flex items-center space-x-3">
              <div className="p-2 bg-yellow-500/20 rounded-lg">
                <TrendingUp className="w-6 h-6 text-yellow-500" />
              </div>
              <div>
                <p className="text-gray-400 text-sm">Aylık Gelir</p>
                <p className="text-2xl font-bold">${empireStatus?.empire_metrics.monthly_revenue || 0}</p>
              </div>
            </div>
          </div>
        </div>

        <div className="bg-gray-800 rounded-xl p-6 border border-gray-700">
          <div className="flex items-center justify-between mb-4">
            <div className="flex items-center space-x-3">
              <div className="p-2 bg-purple-500/20 rounded-lg">
                <Target className="w-6 h-6 text-purple-500" />
              </div>
              <div>
                <p className="text-gray-400 text-sm">Başarım Oranı</p>
                <p className="text-2xl font-bold">{empireStatus?.empire_metrics.success_rate || 0}%</p>
              </div>
            </div>
          </div>
        </div>
      </motion.div>

      {/* Agent Status */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.2 }}
        className="mb-8"
      >
        <h2 className="text-2xl font-bold mb-6 flex items-center space-x-3">
          <Network className="w-6 h-6 text-blue-500" />
          <span>Multi-Agent System</span>
        </h2>
        
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          {Object.entries(agents).map(([agentName, agentData]) => (
            <motion.div
              key={agentName}
              whileHover={{ scale: 1.02 }}
              className="bg-gray-800 rounded-xl p-6 border border-gray-700 cursor-pointer"
              onClick={() => setSelectedAgent(agentName)}
            >
              <div className="flex items-center justify-between mb-4">
                <div className="flex items-center space-x-3">
                  <Cpu className={`w-6 h-6 ${getHealthColor(agentData.health_status)}`} />
                  <div>
                    <p className="font-semibold capitalize">{agentName.replace('_agent', '')}</p>
                    <p className={`text-sm ${getHealthColor(agentData.health_status)}`}>
                      {agentData.health_status}
                    </p>
                  </div>
                </div>
              </div>
              
              {agentData.average_confidence && (
                <div className="mb-4">
                  <div className="flex justify-between text-sm mb-2">
                    <span className="text-gray-400">Güven Seviyesi</span>
                    <span>{agentData.average_confidence.toFixed(1)}%</span>
                  </div>
                  <div className="w-full bg-gray-700 rounded-full h-2">
                    <div 
                      className={`progressBarFill ${getProgressBarClass(Math.round(agentData.average_confidence))}`}
                    />
                  </div>
                </div>
              )}
              
              {agentData.last_generation && (
                <div className="text-xs text-gray-500">
                  Son işlem: {new Date(agentData.last_generation).toLocaleTimeString('tr-TR')}
                </div>
              )}
            </motion.div>
          ))}
        </div>
      </motion.div>

      {/* Campaign Control */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.3 }}
        className="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8"
      >
        {/* Campaign Form */}
        <div className="bg-gray-800 rounded-xl p-6 border border-gray-700">
          <h2 className="text-xl font-bold mb-6 flex items-center space-x-3">
            <PlayCircle className="w-6 h-6 text-green-500" />
            <span>Kampanya Kontrol</span>
          </h2>
          
          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-400 mb-2">Konu</label>
              <input
                type="text"
                className="w-full px-4 py-2 bg-gray-700 border border-gray-600 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                placeholder="Video konusu..."
                value={activeCampaign?.topic || ''}
                onChange={(e) => setActiveCampaign({
                  ...activeCampaign,
                  topic: e.target.value
                } as CampaignData)}
              />
            </div>
            
            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-400 mb-2">Script Türü</label>
                <select 
                  className="w-full px-4 py-2 bg-gray-700 border border-gray-600 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  title="Script türünü seçin"
                >
                  <option value="educational">Eğitici</option>
                  <option value="entertainment">Eğlence</option>
                  <option value="business">İş</option>
                </select>
              </div>
              
              <div>
                <label className="block text-sm font-medium text-gray-400 mb-2">Ton</label>
                <select 
                  className="w-full px-4 py-2 bg-gray-700 border border-gray-600 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  title="Video tonunu seçin"
                >
                  <option value="professional">Profesyonel</option>
                  <option value="casual">Samimi</option>
                  <option value="emotional">Duygusal</option>
                </select>
              </div>
            </div>
            
            <div>
              <label className="block text-sm font-medium text-gray-400 mb-2">SEO Anahtar Kelimeler</label>
              <input
                type="text"
                className="w-full px-4 py-2 bg-gray-700 border border-gray-600 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                placeholder="anahtar1, anahtar2, anahtar3"
                value={activeCampaign?.seo_keywords?.join(', ') || ''}
                onChange={(e) => setActiveCampaign({
                  ...activeCampaign,
                  seo_keywords: e.target.value.split(',').map(k => k.trim()).filter(k => k)
                } as CampaignData)}
              />
            </div>
            
            <div>
              <label className="block text-sm font-medium text-gray-400 mb-2">Başlık</label>
              <input
                type="text"
                className="w-full px-4 py-2 bg-gray-700 border border-gray-600 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                placeholder="Video başlığı..."
                value={activeCampaign?.title || ''}
                onChange={(e) => setActiveCampaign({
                  ...activeCampaign,
                  title: e.target.value
                } as CampaignData)}
              />
            </div>
            
            <button
              onClick={executeCampaign}
              disabled={!activeCampaign?.topic || loading}
              className="w-full py-3 bg-gradient-to-r from-blue-500 to-purple-600 text-white font-semibold rounded-lg hover:from-blue-600 hover:to-purple-700 transition-all disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center space-x-2"
            >
              {loading ? (
                <>
                  <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin" />
                  <span>İşleniyor...</span>
                </>
              ) : (
                <>
                  <Rocket className="w-5 h-5" />
                  <span>Kampanyayı Başlat</span>
                </>
              )}
            </button>
          </div>
        </div>

        {/* Campaign Results */}
        <div className="bg-gray-800 rounded-xl p-6 border border-gray-700">
          <h2 className="text-xl font-bold mb-6 flex items-center space-x-3">
            <BarChart3 className="w-6 h-6 text-purple-500" />
            <span>Kampanya Sonuçları</span>
          </h2>
          
          {campaignResults.length > 0 ? (
            <div className="space-y-4">
              {campaignResults.map((result, index) => (
                <div key={index} className="bg-gray-700 rounded-lg p-4">
                  <div className="flex items-center justify-between mb-2">
                    <div className="flex items-center space-x-3">
                      <div className={`w-3 h-3 rounded-full ${
                        result.orchestration?.success ? 'bg-green-500' : 'bg-red-500'
                      }`} />
                      <span className="font-medium">Adım {result.step}: {result.agent}</span>
                    </div>
                    <span className={`text-sm ${
                      result.orchestration?.success ? 'text-green-400' : 'text-red-400'
                    }`}>
                      {result.orchestration?.success ? 'Başarılı' : 'Başarısız'}
                    </span>
                  </div>
                  
                  {result.orchestration?.confidence && (
                    <div className="mb-2">
                      <div className="flex justify-between text-sm mb-1">
                        <span className="text-gray-400">Güven</span>
                        <span>{result.orchestration.confidence.toFixed(1)}%</span>
                      </div>
                      <div className="w-full bg-gray-600 rounded-full h-1">
                        <div 
                          className={`progressBarFill ${getProgressBarClass(Math.round(result.orchestration.confidence))}`}
                        />
                      </div>
                    </div>
                  )}
                  
                  {result.orchestration?.decision && (
                    <div className="text-sm text-gray-400">
                      Karar: {result.orchestration.decision.type}
                    </div>
                  )}
                </div>
              ))}
            </div>
          ) : (
            <div className="text-center py-12 text-gray-500">
              <Video className="w-12 h-12 mx-auto mb-4 opacity-50" />
              <p>Henüz kampanya sonucu yok</p>
              <p className="text-sm mt-2">Kampanya başlatmak için formu doldurun</p>
            </div>
          )}
        </div>
      </motion.div>

      {/* Pending Consultations */}
      {empireStatus?.pending_consultations && empireStatus.pending_consultations.length > 0 && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.4 }}
          className="bg-yellow-500/10 border border-yellow-500/30 rounded-xl p-6 mb-8"
        >
          <h2 className="text-xl font-bold mb-4 flex items-center space-x-3">
            <MessageSquare className="w-6 h-6 text-yellow-500" />
            <span>Bekleyen Co-Founder Danışmanlıkları</span>
            <span className="bg-yellow-500 text-black text-sm px-2 py-1 rounded-full">
              {empireStatus.pending_consultations.length}
            </span>
          </h2>
          
          <div className="space-y-3">
            {empireStatus.pending_consultations.map((consultation, index) => (
              <div key={index} className="bg-gray-800 rounded-lg p-4">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="font-medium">{consultation.consultation?.question}</p>
                    <p className="text-sm text-gray-400 mt-1">
                      Ajan: {consultation.consultation?.agent} | Güven: {consultation.consultation?.confidence_score}%
                    </p>
                  </div>
                  <div className="flex space-x-2">
                    <button className="px-3 py-1 bg-green-500 text-white text-sm rounded hover:bg-green-600">
                      Onayla
                    </button>
                    <button className="px-3 py-1 bg-yellow-500 text-white text-sm rounded hover:bg-yellow-600">
                      Revize
                    </button>
                    <button className="px-3 py-1 bg-red-500 text-white text-sm rounded hover:bg-red-600">
                      Reddet
                    </button>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </motion.div>
      )}

      {/* System Health */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.5 }}
        className="bg-gray-800 rounded-xl p-6 border border-gray-700"
      >
        <h2 className="text-xl font-bold mb-6 flex items-center space-x-3">
          <Shield className="w-6 h-6 text-green-500" />
          <span>Sistem Sağlığı</span>
        </h2>
        
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
          <div className="text-center">
            <div className="text-3xl font-bold text-green-400 mb-2">
              {empireStatus?.system_health.uptime || '24/7'}
            </div>
            <p className="text-gray-400 text-sm">Çalışma Süresi</p>
          </div>
          
          <div className="text-center">
            <div className="text-3xl font-bold text-yellow-400 mb-2">
              {empireStatus?.system_health.error_rate || '0.1%'}
            </div>
            <p className="text-gray-400 text-sm">Hata Oranı</p>
          </div>
          
          <div className="text-center">
            <div className="text-3xl font-bold text-blue-400 mb-2">
              {empireStatus?.system_health.response_time || '<100ms'}
            </div>
            <p className="text-gray-400 text-sm">Yanıt Süresi</p>
          </div>
          
          <div className="text-center">
            <div className="text-3xl font-bold text-purple-400 mb-2">
              {empireStatus?.system_health.autonomous_rate || '95%'}
            </div>
            <p className="text-gray-400 text-sm">Otonom Oran</p>
          </div>
        </div>
      </motion.div>
    </div>
  );
}
