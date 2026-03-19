'use client';

import { motion } from 'framer-motion';
import { useState, useEffect, useCallback } from 'react';
import {
  Brain, Zap, TrendingUp, Shield, Globe, Video, Users,
  BarChart3, Activity, Target, DollarSign, Eye, Clock,
  AlertTriangle, CheckCircle, Cpu, Database, Rocket, Search,
  ChevronUp, ChevronDown, RefreshCw, PlayCircle
} from 'lucide-react';
import styles from './WarRoom.module.css';

const getWidthClass = (value: number): string => {
  const snapped = Math.min(100, Math.max(0, Math.round(value / 5) * 5));
  return (styles as Record<string, string>)[`w${snapped}`] || styles.w0;
};

interface SystemMetrics {
  cpu_percent: number;
  memory_percent: number;
  disk_percent: number;
  active_processes: number;
  timestamp: string;
}

interface AgentCard {
  key: string;
  label: string;
  icon: React.ElementType;
  color: string;
  health: string;
  confidence: number;
}

interface KPICard {
  label: string;
  value: string;
  change: number;
  icon: React.ElementType;
  color: string;
}

export default function WarRoomPage() {
  const [systemMetrics, setSystemMetrics] = useState<SystemMetrics | null>(null);
  const [agents, setAgents] = useState<Record<string, any>>({});
  const [pendingCount, setPendingCount] = useState(0);
  const [empireMetrics, setEmpireMetrics] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [lastUpdated, setLastUpdated] = useState<Date>(new Date());

  const fetchAll = useCallback(async () => {
    try {
      const [statusRes, agentsRes] = await Promise.all([
        fetch('http://localhost:8000/api/empire/status').catch(() => null),
        fetch('http://localhost:8000/api/empire/agents/status').catch(() => null),
      ]);

      if (statusRes?.ok) {
        const data = await statusRes.json();
        if (data.success) {
          setEmpireMetrics(data.empire_status?.empire_metrics);
          setPendingCount(data.empire_status?.pending_consultations?.length || 0);
          setSystemMetrics(data.empire_status?.real_time_analytics || null);
        }
      }

      if (agentsRes?.ok) {
        const data = await agentsRes.json();
        if (data.success) setAgents(data.agents || {});
      }
    } catch {
      // Silently fail — backend may not be running
    } finally {
      setLoading(false);
      setLastUpdated(new Date());
    }
  }, []);

  useEffect(() => {
    fetchAll();
    const interval = setInterval(fetchAll, 8000);
    return () => clearInterval(interval);
  }, [fetchAll]);

  // --- Mock data for demo when backend is offline ---
  const kpis: KPICard[] = [
    { label: 'Aylık Gelir', value: '$12,840', change: 18.5, icon: DollarSign, color: 'text-green-400' },
    { label: 'Toplam Görüntüleme', value: '2.4M', change: 23.1, icon: Eye, color: 'text-blue-400' },
    { label: 'Aktif Kanal', value: '8', change: 33.3, icon: Globe, color: 'text-purple-400' },
    { label: 'Video Üretimi/Gün', value: '14', change: 7.7, icon: Video, color: 'text-yellow-400' },
    { label: 'Ort. CTR', value: '%6.8', change: 12.4, icon: Target, color: 'text-pink-400' },
    { label: 'Otonom Karar', value: '%94', change: 2.1, icon: Brain, color: 'text-cyan-400' },
  ];

  const agentCards: AgentCard[] = [
    { key: 'script_agent', label: 'Script Ajans', icon: Brain, color: 'blue', health: agents.script_agent?.health_status || 'idle', confidence: agents.script_agent?.average_confidence || 82 },
    { key: 'media_agent', label: 'Medya Ajans', icon: Video, color: 'purple', health: agents.media_agent?.health_status || 'idle', confidence: agents.media_agent?.average_confidence || 78 },
    { key: 'seo_agent', label: 'SEO Ajans', icon: Search, color: 'green', health: agents.seo_agent?.health_status || 'idle', confidence: agents.seo_agent?.average_confidence || 85 },
    { key: 'upload_agent', label: 'Upload Ajans', icon: Rocket, color: 'yellow', health: agents.upload_agent?.health_status || 'idle', confidence: agents.upload_agent?.average_confidence || 91 },
  ];

  const cpuPct = systemMetrics?.cpu_percent ?? 42;
  const memPct = systemMetrics?.memory_percent ?? 58;
  const diskPct = systemMetrics?.disk_percent ?? 35;

  return (
    <div className="min-h-screen bg-gray-900 text-white p-6 space-y-6">
      {/* Header */}
      <motion.div initial={{ opacity: 0, y: -20 }} animate={{ opacity: 1, y: 0 }}>
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-4">
            <div className="p-3 bg-gradient-to-r from-red-600 to-orange-500 rounded-xl shadow-lg">
              <Shield className="w-8 h-8 text-white" />
            </div>
            <div>
              <h1 className="text-3xl font-black tracking-tight">
                <span className="bg-gradient-to-r from-red-400 to-orange-400 bg-clip-text text-transparent">
                  SAVAŞ ODASI
                </span>
              </h1>
              <p className="text-gray-400 text-sm">VUC-2026 Komuta Merkezi — Gerçek Zamanlı İzleme</p>
            </div>
          </div>

          <div className="flex items-center space-x-3">
            {pendingCount > 0 && (
              <motion.div
                animate={{ scale: [1, 1.05, 1] }}
                transition={{ repeat: Infinity, duration: 2 }}
                className="flex items-center space-x-2 px-4 py-2 bg-yellow-500/20 border border-yellow-500/40 rounded-lg"
              >
                <AlertTriangle className="w-4 h-4 text-yellow-400" />
                <span className="text-sm text-yellow-400 font-semibold">
                  {pendingCount} danışmanlık bekliyor
                </span>
              </motion.div>
            )}
            <button
              onClick={fetchAll}
              title="Yenile"
              className="p-2 bg-gray-800 rounded-lg hover:bg-gray-700 transition-colors"
            >
              <RefreshCw className={`w-5 h-5 ${loading ? 'animate-spin' : ''}`} />
            </button>
            <div className="text-xs text-gray-500">
              Son: {lastUpdated.toLocaleTimeString('tr-TR')}
            </div>
          </div>
        </div>
      </motion.div>

      {/* KPI Grid */}
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.1 }}
        className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4"
      >
        {kpis.map((kpi, i) => (
          <motion.div
            key={kpi.label}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: i * 0.05 }}
            className="bg-gray-800 rounded-xl p-4 border border-gray-700 hover:border-gray-600 transition-colors"
          >
            <div className="flex items-center justify-between mb-2">
              <kpi.icon className={`w-5 h-5 ${kpi.color}`} />
              <span className={`text-xs flex items-center space-x-0.5 ${kpi.change >= 0 ? 'text-green-400' : 'text-red-400'}`}>
                {kpi.change >= 0 ? <ChevronUp className="w-3 h-3" /> : <ChevronDown className="w-3 h-3" />}
                <span>{Math.abs(kpi.change)}%</span>
              </span>
            </div>
            <div className="text-xl font-bold">{kpi.value}</div>
            <div className="text-xs text-gray-400 mt-1">{kpi.label}</div>
          </motion.div>
        ))}
      </motion.div>

      {/* Main Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Agent Status */}
        <motion.div
          initial={{ opacity: 0, x: -20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ delay: 0.2 }}
          className="lg:col-span-1 space-y-4"
        >
          <h2 className="text-lg font-bold flex items-center space-x-2">
            <Cpu className="w-5 h-5 text-blue-400" />
            <span>Ajan Durumu</span>
          </h2>

          {agentCards.map((agent) => (
            <div key={agent.key} className="bg-gray-800 rounded-xl p-4 border border-gray-700">
              <div className="flex items-center justify-between mb-3">
                <div className="flex items-center space-x-2">
                  <agent.icon className={`w-5 h-5 text-${agent.color}-400`} />
                  <span className="font-medium text-sm">{agent.label}</span>
                </div>
                <span className={`text-xs px-2 py-0.5 rounded-full ${
                  agent.health === 'healthy' ? 'bg-green-500/20 text-green-400' :
                  agent.health === 'busy' ? 'bg-yellow-500/20 text-yellow-400' :
                  'bg-gray-600/50 text-gray-400'
                }`}>
                  {agent.health === 'healthy' ? 'Aktif' : agent.health === 'busy' ? 'Meşgul' : 'Bekleniyor'}
                </span>
              </div>
              <div>
                <div className="flex justify-between text-xs mb-1">
                  <span className="text-gray-400">Güven</span>
                  <span>{agent.confidence.toFixed(0)}%</span>
                </div>
                <div className={styles.progressBar}>
                  <div
                    className={`${styles.progressBarFill} ${(styles as Record<string, string>)[`progressBarFill${agent.color.charAt(0).toUpperCase() + agent.color.slice(1)}`] || styles.progressBarFillBlue} ${getWidthClass(agent.confidence)}`}
                  />
                </div>
              </div>
            </div>
          ))}

          {/* System Resources */}
          <div className="bg-gray-800 rounded-xl p-4 border border-gray-700">
            <h3 className="text-sm font-semibold mb-3 flex items-center space-x-2">
              <Activity className="w-4 h-4 text-cyan-400" />
              <span>Sistem Kaynakları</span>
            </h3>
            {[
              { label: 'CPU', value: cpuPct, color: 'blue' },
              { label: 'RAM', value: memPct, color: 'purple' },
              { label: 'Disk', value: diskPct, color: 'green' },
            ].map((resource) => (
              <div key={resource.label} className="mb-3 last:mb-0">
                <div className="flex justify-between text-xs mb-1">
                  <span className="text-gray-400">{resource.label}</span>
                  <span className={resource.value > 80 ? 'text-red-400' : 'text-gray-300'}>
                    %{resource.value.toFixed(0)}
                  </span>
                </div>
                <div className={styles.progressBar}>
                  <div
                    className={`${styles.progressBarFill} ${
                      resource.value > 80 ? styles.progressBarFillRed
                      : resource.value > 60 ? styles.progressBarFillYellow
                      : (styles as Record<string, string>)[`progressBarFill${resource.color.charAt(0).toUpperCase() + resource.color.slice(1)}`] || styles.progressBarFillBlue
                    } ${getWidthClass(resource.value)}`}
                  />
                </div>
              </div>
            ))}
          </div>
        </motion.div>

        {/* Center: Revenue & Analytics */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.3 }}
          className="lg:col-span-2 space-y-4"
        >
          {/* Revenue Chart Placeholder */}
          <div className="bg-gray-800 rounded-xl p-6 border border-gray-700">
            <div className="flex items-center justify-between mb-6">
              <h2 className="text-lg font-bold flex items-center space-x-2">
                <TrendingUp className="w-5 h-5 text-green-400" />
                <span>Gelir & Performans (Son 7 Gün)</span>
              </h2>
              <span className="text-xs text-gray-400 bg-gray-700 px-3 py-1 rounded-full">Canlı</span>
            </div>

            {/* Simulated bar chart */}
            <div className={`flex items-end justify-between space-x-2 h-32 ${styles.barChart}`}>
              {([65, 72, 58, 88, 92, 76, 100] as const).map((val, i) => (
                <div key={i} className="flex-1 flex flex-col items-center space-y-1">
                  <div
                    className={`w-full bg-gradient-to-t from-blue-600 to-purple-500 rounded-t-sm transition-all duration-700 hover:from-blue-500 hover:to-purple-400 ${styles[`barH${val}`]}`}
                  />
                  <span className="text-xs text-gray-500">
                    {['Pzt', 'Sal', 'Çar', 'Per', 'Cum', 'Cmt', 'Paz'][i]}
                  </span>
                </div>
              ))}
            </div>
          </div>

          {/* Channel Performance Table */}
          <div className="bg-gray-800 rounded-xl p-6 border border-gray-700">
            <h2 className="text-lg font-bold flex items-center space-x-2 mb-4">
              <Globe className="w-5 h-5 text-purple-400" />
              <span>Kanal Performansı</span>
            </h2>

            <div className="overflow-x-auto">
              <table className="w-full text-sm">
                <thead>
                  <tr className="text-gray-400 border-b border-gray-700">
                    <th className="text-left py-2 pr-4">Kanal</th>
                    <th className="text-right py-2 pr-4">Abone</th>
                    <th className="text-right py-2 pr-4">CTR</th>
                    <th className="text-right py-2 pr-4">CPM</th>
                    <th className="text-right py-2">Durum</th>
                  </tr>
                </thead>
                <tbody>
                  {[
                    { name: 'TechEmpire TR', subs: '125K', ctr: '6.8%', cpm: '$3.2', status: 'active' },
                    { name: 'MoneyMind', subs: '87K', ctr: '8.1%', cpm: '$4.7', status: 'active' },
                    { name: 'AI Dünyası', subs: '52K', ctr: '5.3%', cpm: '$2.9', status: 'active' },
                    { name: 'FinansGuru', subs: '34K', ctr: '7.2%', cpm: '$5.1', status: 'growing' },
                    { name: 'GamersHub TR', subs: '21K', ctr: '4.9%', cpm: '$1.8', status: 'growing' },
                  ].map((ch) => (
                    <tr key={ch.name} className="border-b border-gray-700/50 hover:bg-gray-700/30 transition-colors">
                      <td className="py-3 pr-4 font-medium">{ch.name}</td>
                      <td className="text-right py-3 pr-4 text-gray-300">{ch.subs}</td>
                      <td className="text-right py-3 pr-4 text-blue-400">{ch.ctr}</td>
                      <td className="text-right py-3 pr-4 text-green-400">{ch.cpm}</td>
                      <td className="text-right py-3">
                        <span className={`text-xs px-2 py-0.5 rounded-full ${
                          ch.status === 'active'
                            ? 'bg-green-500/20 text-green-400'
                            : 'bg-blue-500/20 text-blue-400'
                        }`}>
                          {ch.status === 'active' ? 'Aktif' : 'Büyüyor'}
                        </span>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>

          {/* Decision Engine Status */}
          <div className="bg-gray-800 rounded-xl p-6 border border-gray-700">
            <h2 className="text-lg font-bold flex items-center space-x-2 mb-4">
              <Brain className="w-5 h-5 text-cyan-400" />
              <span>Karar Motoru Durumu</span>
            </h2>

            <div className="grid grid-cols-3 gap-4">
              {[
                { label: 'Otonom (90+)', value: '94%', icon: Zap, color: 'green', desc: 'Tam otopilot' },
                { label: 'Danışma (75-89)', value: '5%', icon: Users, color: 'yellow', desc: 'Co-Founder onayı' },
                { label: 'Manuel (<75)', value: '1%', icon: AlertTriangle, color: 'red', desc: 'İnsan müdahalesi' },
              ].map((item) => (
                <div key={item.label} className={`bg-${item.color}-500/10 border border-${item.color}-500/20 rounded-lg p-4 text-center`}>
                  <item.icon className={`w-6 h-6 text-${item.color}-400 mx-auto mb-2`} />
                  <div className={`text-2xl font-bold text-${item.color}-400`}>{item.value}</div>
                  <div className="text-xs font-medium mt-1">{item.label}</div>
                  <div className="text-xs text-gray-500 mt-1">{item.desc}</div>
                </div>
              ))}
            </div>
          </div>
        </motion.div>
      </div>

      {/* Activity Log */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.4 }}
        className="bg-gray-800 rounded-xl p-6 border border-gray-700"
      >
        <h2 className="text-lg font-bold flex items-center space-x-2 mb-4">
          <Activity className="w-5 h-5 text-orange-400" />
          <span>Canlı Aktivite Akışı</span>
        </h2>

        <div className="space-y-2 max-h-48 overflow-y-auto">
          {[
            { time: '12:08', type: 'success', msg: 'Script Agent — "AI 2026 Rehberi" senaryosu üretildi (Güven: 93%)' },
            { time: '12:06', msg: 'SEO Agent — Başlık optimizasyonu tamamlandı. Tahmini CTR: %7.4', type: 'success' },
            { time: '12:04', msg: 'DevOps Agent — Redis bağlantısı yeniden kuruldu (3. deneme)', type: 'warning' },
            { time: '12:02', msg: 'Spy Agent — TechChannel123 rakip analizi: 5 içerik boşluğu tespit edildi', type: 'info' },
            { time: '11:58', msg: 'Upload Agent — "Para Kazanma 2026" yüklendi. Görüntüleme: 1.2K/saat', type: 'success' },
            { time: '11:55', msg: 'Sinematik Motor — Foley SFX tetiklendi: wind_ambient.mp3 (ts: 12.5s)', type: 'info' },
            { time: '11:52', msg: 'Co-Founder Desk — Karar bekliyor: "SEO skoru 82 — başlığı agresifleştireyim mi?"', type: 'warning' },
            { time: '11:49', msg: 'Ghost Persona — TechWizard_TR: 12 yorum, 3 yanıt, etkileşim +18%', type: 'success' },
          ].map((log, i) => (
            <div key={i} className={`flex items-start space-x-3 text-sm p-2 rounded-lg ${
              log.type === 'success' ? 'bg-green-500/5' :
              log.type === 'warning' ? 'bg-yellow-500/5' : 'bg-blue-500/5'
            }`}>
              <span className="text-gray-500 font-mono text-xs mt-0.5 flex-shrink-0">{log.time}</span>
              <div className={`w-1.5 h-1.5 rounded-full mt-1.5 flex-shrink-0 ${
                log.type === 'success' ? 'bg-green-400' :
                log.type === 'warning' ? 'bg-yellow-400' : 'bg-blue-400'
              }`} />
              <span className="text-gray-300">{log.msg}</span>
            </div>
          ))}
        </div>
      </motion.div>
    </div>
  );
}
