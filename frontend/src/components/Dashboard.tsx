'use client';

import { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import styles from './Dashboard.module.css';

// Helper function to get progress width class
const getProgressWidthClass = (value: number): string => {
  const rounded = Math.round(value / 5) * 5; // Round to nearest 5
  return styles[`progressWidth${rounded}`] || styles.progressWidth0;
};
import { 
  BarChart3, 
  Play, 
  Users, 
  TrendingUp, 
  Settings, 
  Upload,
  Eye,
  Calendar,
  Zap,
  Shield,
  Brain,
  Globe,
  Activity,
  DollarSign,
  Clock,
  CheckCircle,
  AlertCircle,
  XCircle
} from 'lucide-react';

interface Channel {
  id: number;
  name: string;
  niche: string;
  subscribers: number;
  views: number;
  revenue: number;
  status: 'active' | 'pending' | 'error';
}

interface Video {
  id: number;
  title: string;
  status: 'planning' | 'scripting' | 'rendering' | 'uploading' | 'published';
  views: number;
  progress: number;
  scheduled_at: string;
}

interface SystemStats {
  cpu_usage: number;
  memory_usage: number;
  gpu_usage: number;
  active_tasks: number;
  queued_videos: number;
}

export default function Dashboard() {
  const [channels, setChannels] = useState<Channel[]>([]);
  const [videos, setVideos] = useState<Video[]>([]);
  const [systemStats, setSystemStats] = useState<SystemStats>({
    cpu_usage: 0,
    memory_usage: 0,
    gpu_usage: 0,
    active_tasks: 0,
    queued_videos: 0
  });
  const [selectedChannel, setSelectedChannel] = useState<number | null>(null);

  useEffect(() => {
    // Verileri çek
    fetchDashboardData();
    const interval = setInterval(fetchDashboardData, 5000); // 5 saniyede bir güncelle
    return () => clearInterval(interval);
  }, []);

  const fetchDashboardData = async () => {
    try {
      // Kanal verileri
      const channelsResponse = await fetch('/api/channels');
      if (channelsResponse.ok) {
        const channelsData = await channelsResponse.json();
        setChannels(channelsData);
      }

      // Video verileri
      const videosResponse = await fetch('/api/videos');
      if (videosResponse.ok) {
        const videosData = await videosResponse.json();
        setVideos(videosData);
      }

      // Sistem istatistikleri
      const statsResponse = await fetch('/api/analytics/system');
      if (statsResponse.ok) {
        const statsData = await statsResponse.json();
        setSystemStats(statsData);
      }
    } catch (error) {
      console.error('Dashboard verileri çekilemedi:', error);
    }
  };

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'active':
      case 'published':
        return <CheckCircle className="w-5 h-5 text-green-400" />;
      case 'pending':
      case 'planning':
      case 'scripting':
      case 'rendering':
      case 'uploading':
        return <AlertCircle className="w-5 h-5 text-yellow-400" />;
      case 'error':
        return <XCircle className="w-5 h-5 text-red-400" />;
      default:
        return <Clock className="w-5 h-5 text-gray-400" />;
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'active':
      case 'published':
        return 'status-active';
      case 'pending':
      case 'planning':
      case 'scripting':
      case 'rendering':
      case 'uploading':
        return 'status-pending';
      case 'error':
        return 'status-error';
      default:
        return 'bg-gray-500/20 text-gray-400';
    }
  };

  const getStatusText = (status: string) => {
    switch (status) {
      case 'active': return 'Aktif';
      case 'pending': return 'Beklemede';
      case 'error': return 'Hata';
      case 'planning': return 'Planlama';
      case 'scripting': return 'Senaryo';
      case 'rendering': return 'Render';
      case 'uploading': return 'Yükleme';
      case 'published': return 'Yayında';
      default: return status;
    }
  };

  const formatNumber = (num: number) => {
    if (num >= 1000000) return (num / 1000000).toFixed(1) + 'M';
    if (num >= 1000) return (num / 1000).toFixed(1) + 'K';
    return num.toString();
  };

  return (
    <div className="min-h-screen p-6">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          className="mb-8"
        >
          <h1 className="text-4xl font-bold mb-2">
            <span className="gradient-text">Misyon Kontrol Merkezi</span>
          </h1>
          <p className="text-gray-400">YouTube İmparatorluğunu buradan yönetin</p>
        </motion.div>

        {/* System Performance */}
        <motion.div
          initial={{ opacity: 0, scale: 0.95 }}
          animate={{ opacity: 1, scale: 1 }}
          className="glass-effect rounded-xl p-6 mb-8"
        >
          <h2 className="text-xl font-bold mb-6 flex items-center">
            <Activity className="w-6 h-6 mr-3 text-amber-500" />
            Sistem Performansı
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-5 gap-6">
            <div className="text-center">
              <div className="text-2xl font-bold text-blue-400 mb-2">
                {systemStats.cpu_usage.toFixed(1)}%
              </div>
              <div className="text-gray-400 text-sm">CPU Kullanımı</div>
              <div className={styles.progressBar}>
                <div 
                  className={`${styles.progressBarFill} ${styles.progressBarFillBlue} ${getProgressWidthClass(systemStats.cpu_usage)}`}
                />
              </div>
            </div>
            <div className="text-center">
              <div className="text-2xl font-bold text-green-400 mb-2">
                {systemStats.memory_usage.toFixed(1)}%
              </div>
              <div className="text-gray-400 text-sm">Bellek Kullanımı</div>
              <div className={styles.progressBar}>
                <div 
                  className={`${styles.progressBarFill} ${styles.progressBarFillGreen} ${getProgressWidthClass(systemStats.memory_usage)}`}
                />
              </div>
            </div>
            <div className="text-center">
              <div className="text-2xl font-bold text-purple-400 mb-2">
                {systemStats.gpu_usage.toFixed(1)}%
              </div>
              <div className="text-gray-400 text-sm">GPU Kullanımı</div>
              <div className={styles.progressBar}>
                <div 
                  className={`${styles.progressBarFill} ${styles.progressBarFillYellow} ${getProgressWidthClass(systemStats.gpu_usage)}`}
                />
              </div>
            </div>
            <div className="text-center">
              <div className="text-2xl font-bold text-yellow-400 mb-2">
                {systemStats.active_tasks}
              </div>
              <div className="text-gray-400 text-sm">Aktif Görev</div>
            </div>
            <div className="text-center">
              <div className="text-2xl font-bold text-red-400 mb-2">
                {systemStats.queued_videos}
              </div>
              <div className="text-gray-400 text-sm">Sıradaki Video</div>
            </div>
          </div>
        </motion.div>

        {/* Quick Stats */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
          {[
            { label: 'Toplam Kanal', value: channels.length, icon: Globe, color: 'from-blue-500 to-cyan-500' },
            { label: 'Aktif Video', value: videos.filter(v => v.status !== 'published').length, icon: Play, color: 'from-green-500 to-emerald-500' },
            { label: 'Toplam İzlenme', value: videos.reduce((sum, v) => sum + v.views, 0), icon: Eye, color: 'from-purple-500 to-pink-500' },
            { label: 'Tahmini Gelir', value: channels.reduce((sum, c) => sum + c.revenue, 0), icon: DollarSign, color: 'from-yellow-500 to-amber-500' }
          ].map((stat, index) => (
            <motion.div
              key={stat.label}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.3, delay: index * 0.1 }}
              className="glass-effect rounded-xl p-6 card-hover"
            >
              <div className={`w-12 h-12 rounded-lg bg-gradient-to-r ${stat.color} flex items-center justify-center mb-4`}>
                <stat.icon className="w-6 h-6 text-white" />
              </div>
              <div className="text-2xl font-bold mb-2">
                {stat.label === 'Tahmini Gelir' ? '$' + formatNumber(stat.value) : formatNumber(stat.value)}
              </div>
              <div className="text-gray-400 text-sm">{stat.label}</div>
            </motion.div>
          ))}
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Channels */}
          <motion.div
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            className="glass-effect rounded-xl p-6"
          >
            <h2 className="text-xl font-bold mb-6 flex items-center">
              <Users className="w-6 h-6 mr-3 text-amber-500" />
              Kanallar
            </h2>
            <div className="space-y-4">
              {channels.map((channel) => (
                <div
                  key={channel.id}
                  className={`p-4 rounded-lg border cursor-pointer transition-all duration-300 ${
                    selectedChannel === channel.id 
                      ? 'bg-amber-500/10 border-amber-500/30' 
                      : 'bg-gray-800/50 border-gray-700 hover:bg-gray-800'
                  }`}
                  onClick={() => setSelectedChannel(channel.id)}
                >
                  <div className="flex items-center justify-between mb-2">
                    <h3 className="font-semibold">{channel.name}</h3>
                    <div className="flex items-center gap-2">
                      {getStatusIcon(channel.status)}
                      <span className={`text-xs ${getStatusColor(channel.status)}`}>
                        {getStatusText(channel.status)}
                      </span>
                    </div>
                  </div>
                  <div className="grid grid-cols-3 gap-4 text-sm">
                    <div>
                      <div className="text-gray-400">Abone</div>
                      <div className="font-semibold">{formatNumber(channel.subscribers)}</div>
                    </div>
                    <div>
                      <div className="text-gray-400">İzlenme</div>
                      <div className="font-semibold">{formatNumber(channel.views)}</div>
                    </div>
                    <div>
                      <div className="text-gray-400">Gelir</div>
                      <div className="font-semibold">${formatNumber(channel.revenue)}</div>
                    </div>
                  </div>
                  <div className="mt-2">
                    <span className="text-xs text-gray-400">Niş: </span>
                    <span className="text-xs text-amber-400">{channel.niche}</span>
                  </div>
                </div>
              ))}
            </div>
          </motion.div>

          {/* Recent Videos */}
          <motion.div
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            className="glass-effect rounded-xl p-6"
          >
            <h2 className="text-xl font-bold mb-6 flex items-center">
              <Play className="w-6 h-6 mr-3 text-amber-500" />
              Son Videolar
            </h2>
            <div className="space-y-4">
              {videos.slice(0, 6).map((video) => (
                <div key={video.id} className="p-4 rounded-lg bg-gray-800/50 border border-gray-700">
                  <div className="flex items-center justify-between mb-2">
                    <h3 className="font-semibold text-sm truncate flex-1 mr-2">{video.title}</h3>
                    {getStatusIcon(video.status)}
                  </div>
                  <div className="flex items-center justify-between mb-2">
                    <span className={`text-xs ${getStatusColor(video.status)}`}>
                      {getStatusText(video.status)}
                    </span>
                    <span className="text-xs text-gray-400">
                      {formatNumber(video.views)} izlenme
                    </span>
                  </div>
                  {video.status !== 'published' && video.status !== 'planning' && (
                    <div className="w-full bg-gray-700 rounded-full h-2">
                      <div 
                        className={`${styles.progressBarFill} ${styles.progressBarFillYellow} ${getProgressWidthClass(video.progress)}`}
                      />
                    </div>
                  )}
                  <div className="text-xs text-gray-400 mt-2">
                    <Calendar className="w-3 h-3 inline mr-1" />
                    {new Date(video.scheduled_at).toLocaleDateString('tr-TR')}
                  </div>
                </div>
              ))}
            </div>
          </motion.div>
        </div>

        {/* Quick Actions */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="glass-effect rounded-xl p-6 mt-8"
        >
          <h2 className="text-xl font-bold mb-6 flex items-center">
            <Zap className="w-6 h-6 mr-3 text-amber-500" />
            Hızlı İşlemler
          </h2>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <button className="btn-primary flex items-center justify-center">
              <Brain className="w-5 h-5 mr-2" />
              AI Senaryo
            </button>
            <button className="btn-secondary flex items-center justify-center">
              <Upload className="w-5 h-5 mr-2" />
              Video Yükle
            </button>
            <button className="btn-success flex items-center justify-center">
              <Shield className="w-5 h-5 mr-2" />
              Koruma Aktif
            </button>
            <button className="btn-danger flex items-center justify-center">
              <Settings className="w-5 h-5 mr-2" />
              Ayarlar
            </button>
          </div>
        </motion.div>
      </div>
    </div>
  );
}
